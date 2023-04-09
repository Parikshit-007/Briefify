from django.shortcuts import redirect,render
from googletrans import Translator
from webapp.models import Summary

def translator(request, summary_id):
    translator = Translator()
    if request.method == 'POST':
        destination = request.POST.get('language')
    else:    
       destination = "hi"

    summary = Summary.objects.get(id=int(summary_id))
    summary_text = summary.summary_text

    lines = summary_text.splitlines()
    translated_lines = []

    for line in lines:
        result = translator.detect(line)
        if result.lang != destination:
            out = translator.translate(line, dest=destination)
            translated_lines.append(out.text)
        else:
            translated_lines.append(line)

  
    translated_text = "\n".join(translated_lines)
    context = {
    'summary_text': summary.summary_text,
    'summary_words': summary.summary_words,
    'duration': summary.duration,
    'title': summary.title,
    'out': translated_text,}

    return render(request, 'final_translate.html',context)


def tt(request, summary_id):
    summary=Summary.objects.get(id=summary_id)
    context = {
    'summary_id': summary_id,
    'summary_text': summary.summary_text,
    'summary_words': summary.summary_words,
    'duration': summary.duration,
    'title': summary.title,
    'transcript_words': summary.transcript_words,
    }
    return render (request, 'translate.html', context)