from pytube import YouTube
import os
  
class pytubemp3():
    def __init__(self, url):
        self.url = url
    classmethod
    def extractMP3(self):
        yt = YouTube(self.url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path='.')
        os.rename(out_file, 'temp.mp3')
        print(yt.title + " has been successfully downloaded.")
    classmethod
    def deleteMP3(self):
        if os.path.exists("temp.mp3"):
            os.remove("temp.mp3")
        else:
            print("The mp3 does not exist!") 