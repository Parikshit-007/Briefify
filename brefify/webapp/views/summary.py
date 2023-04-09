from webapp.models import UserProfile
from django.shortcuts import redirect, render
import os
from django.conf import settings
from webapp.models import Video, Summary
from webapp.forms import VideoForm
import whisper
from django.http import HttpResponse
import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import subprocess
def process_video(request, video_id):
    # Get the video object
    try:
        video = Video.objects.get(id=int(video_id))
    except Video.DoesNotExist:
        # Handle the case where no video with the specified ID exists
        return HttpResponse("Video not found")

    # Set the input and output file paths for mp3 conversion
    input_path_mp3 = os.path.join(settings.BASE_DIR, f'media/main/videos/{video.title}.mp4')
    output_path_mp3 = os.path.join(settings.BASE_DIR, f'media/main/videos/{video.title}.mp3')

    # execute the ffmpeg command to convert video to mp3
    command_mp3 = f"ffmpeg -i {input_path_mp3} {output_path_mp3}"
    os.system(command_mp3)


    # Set the input and output file paths for transcription
    input_path_transcription = output_path_mp3
    output_path_transcription = os.path.join(settings.BASE_DIR, f'media/main/videos/{video.title}.txt')

    # Execute the whisper transcription command
    model = whisper.load_model("base")
    result = model.transcribe(input_path_transcription)
    transcript = result["text"]
    transcript_words = len(transcript.split())
    # Save the transcription to a file
    with open(output_path_transcription, 'w', encoding='utf-8') as file:
       file.write(transcript)


    # Summarize the transcript
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
    #tokenizer
    sentences = nltk.tokenize.sent_tokenize(transcript)

    length = 0
    chunk = ""
    chunks = []
    count = -1

    for sentence in sentences:
        count += 1
        combined_length = len(tokenizer.tokenize(sentence)) + length

        if combined_length <= tokenizer.max_len_single_sentence:
            chunk += sentence + " "
            length = combined_length

            if count == len(sentences) - 1:
                chunks.append(chunk.strip())

        else:
            chunks.append(chunk.strip())
            length = 0
            chunk = ""
            chunk += sentence + " "
            length = len(tokenizer.tokenize(sentence))

    inputs = [tokenizer(chunk, return_tensors="pt") for chunk in chunks]
    summary = []

    for input in inputs:
        output = model.generate(**input, max_length=int(len(input['input_ids'][0])/2), min_length=0)
        summary.append(tokenizer.decode(*output, skip_special_tokens=True))

    # Save the summary to a file
    output_path_summary = os.path.join(settings.BASE_DIR, f'media/{video.title}_summary.txt')
    with open(output_path_summary, 'w', encoding='utf-8') as file:
        file.write("\n".join(summary))

    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries","format=duration", "-of","default=noprint_wrappers=1:nokey=1", f'media/main/videos/{video.title}.mp4'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    duration = ("%.2f" % (float(result.stdout)/60) + " min")
   # print (a)

    summary_text = "\n".join(summary)
    summary_words= len(summary_text.split())
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user_profile = UserProfile.objects.get(id=user_id)
    # Create the Summary object with the video summary and save it to the database
    summary_obj = Summary.objects.create(user=user_profile, video=video, summary_text=summary_text,summary_words=summary_words, transcript_words=transcript_words, duration=duration)
    summary_obj.save()
  #  request.session['transcript_words'] = transcript_words
  #  request.session['summary_words'] = summary_words
   # request.session['duration'] = duration
    # Render a response to the user
    context = {'video': video, 'summary': summary_text, 'summary_words': summary_words, 'transcript_words': transcript_words, 'duration':duration}
    return render(request, 'summary.html', context)

# Close the function
