import spacy
import re
from webapp.models import Summary,Video
from django.shortcuts import render

def action_words(request, video_id):
    video = Video.objects.get(id=video_id)
    nlp = spacy.load("en_core_web_sm")
    file_path = f'media/main/videos/{video.title}.txt'
    keywords = ["task", "complete", "to do", "assignment", "project", "work", "job", "duty", "responsibility",
            "assign", "assigned", "assigning", "delegate", "delegated", "delegating", "direct", "directed", "directing",
            "instruct", "instructed", "instructing", "charge", "charged", "charging", "enjoin", "enjoined", "enjoining",
            "order", "ordered", "ordering", "command", "commanded", "commanding", "tell", "told", "telling",
            "perform", "performed", "performing", "execute", "executed", "executing", "accomplish", "accomplished", "accomplishing",
            "fulfill", "fulfilled", "fulfilling", "follow", "followed", "following", "carry out", "carried out", "carrying out",
            "implement", "implemented", "implementing", "enforce", "enforced", "enforcing", "enact", "enacted", "enacting",
            "can you please", "i need you to", "could you", "please make sure to", "Announced ",
            "don't forget to", "i'm assigning you to", "you're responsible for", "i want you to",
            "it's your duty to", "please ensure that you", "due date"]
    highlight_color = ''

    # read in file and highlight tasks
    highlighted_sentences = set()
    with open(file_path, "r") as f:
        for line in f:
            doc = nlp(line.strip())
            for token in doc:
                # check if token is a task-related keyword
                if re.match("|".join(keywords), token.text, re.IGNORECASE):
                    highlighted_sentence = highlight_color + \
                        token.sent.text.strip()
                    highlighted_sentences.add(highlighted_sentence)
                    break

    # create context dictionary
    context = {
        'video_id': video_id,
        'highlighted_sentences': highlighted_sentences,
        'video': video,
        
    }

    # render template
    return render(request, 'action_words.html', context)
