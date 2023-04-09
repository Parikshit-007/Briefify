import os
from os import path
import whisper

with open('transcript.txt','r') as file:
    article = file.read()

a=int(len(article.split())/2)


from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
checkpoint = "sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)




import nltk
# nltk.download('punkt')               one time thing

command2mp3 = "ffmpeg -i conan.mp4 conan.mp3"
command2wav = "ffmpeg -i conan.mp3 conan.wav"
os.system(command2mp3)
os.system(command2wav)

def speech_to_text():
    model = whisper.load_model("base")
    result = model.transcribe("conan.mp3")
    transcript = result["text"]
    file = open('transcript.txt', 'w')
    file.write(transcript)
    file.close

class Summary:
    sentences = nltk.tokenize.sent_tokenize(article)
    length = 0
    chunk = ""
    chunks = []
    count = -1
    for sentence in sentences:
       
       count += 1
       combined_length = len(tokenizer.tokenize(sentence)) + length # add the no. of sentence tokens to the length counter
       if combined_length  <= tokenizer.max_len_single_sentence: # if it doesn't exceed
          
          chunk += sentence + " " # add the sentence to the chunk
          length = combined_length # update the length counter
          if count == len(sentences) - 1:
            chunks.append(chunk.strip()) # save the chunk

    # if it is the last sentence
       else: 
          chunks.append(chunk.strip()) # save the chunk
    
    # reset 
    length = 0 
    chunk = ""

    # take care of the overflow sentence
    chunk += sentence + " "
    length = len(tokenizer.tokenize(sentence))
    len(chunks)
    inputs = [tokenizer(chunk, return_tensors="pt") for chunk in chunks]
    b=[]
    for input in inputs:
       output = model.generate(**input,max_length= a , min_length=0)
       b.append(tokenizer.decode(*output, skip_special_tokens=True))
    file = open('summary.txt', 'w')
    for x in b:
       file.write(x)
file.close








  
  # print('Generated Shape:', output.shape)

  