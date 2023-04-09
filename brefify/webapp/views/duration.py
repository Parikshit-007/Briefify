import subprocess
from webapp.models import Video
myid= Video.objects.get('id')
video= Video.objects.get(myid=id)
def get_length(filename):
    
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
   
    return float(result.stdout)
a = get_length(video.title)/60

print("%.2f" % a + " min")

