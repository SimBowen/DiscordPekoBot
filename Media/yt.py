from datetime import timedelta
from urllib.parse import parse_qs, urlparse
import googleapiclient.discovery
from dotenv import load_dotenv
import os
load_dotenv()



APIkey = os.getenv('YT_API')
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = APIkey)




class ytplaylist:
    def __init__(self,url):
        self.url = url
        self.urllist = self.parse_playlist(url,50)
        self.ytvideolist = self.create_ytvideolist(self.urllist)
        self.seconds = self.duration(self.ytvideolist)

    #calls the yt api to return a list of video urls
    classmethod
    def parse_playlist(self,url, max_size):
        url_list = []
        query = parse_qs(urlparse(url).query, keep_blank_values=True)
        playlist_id = query["list"][0]
        request = youtube.playlistItems().list(part = "snippet",playlistId = playlist_id,maxResults = max_size)
        response = request.execute()
        playlist_items = []
        while request is not None:
            response = request.execute()
            playlist_items += response["items"]
            request = youtube.playlistItems().list_next(request, response)
            for t in playlist_items:
                link = f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}'
                print(link)
                if link not in url_list:
                    if len(url_list)>max_size:
                        break
                    url_list.append(link)
        return url_list

    #converts the list of urls into ytvideo objects
    classmethod
    def create_ytvideolist(self,urllist):
        ytvideolist = []
        for link in urllist:
            ytvideolist.append(ytvideo(link))
        return ytvideolist

    #return the duration of all videos in seconds
    classmethod
    def duration(self,ytvideolist):
        duration = 0
        for video in ytvideolist:
            duration += video.seconds
        return duration



class ytvideo:
    def __init__(self,input,requestor):
        self.requestor = requestor
        self.url = self.geturl(input)
        self.data = self.getdata(self.url)
        self.duration = self.data['contentDetails']['duration']
        self.title = self.data['snippet']['title']
        self.thumbnail = self.data['snippet']['thumbnails']['default']['url']
        self.seconds = self.ytDurationToSeconds(self.duration)
        self.time = self.duration_parsing(self.seconds)

    classmethod
    def geturl(self, input):
        if 'youtube.com' in input:
            return input
        else:
            return self.ytSearch(input)

    
    classmethod
    def ytSearch(self,input):
        request = youtube.search().list(part="snippet",maxResults=5,q=input)
        response = request.execute()
        id = response["items"][0]["id"]["videoId"]
        url = f"https://www.youtube.com/watch?v={id}"
        return url


    classmethod
    def getdata(self,url):
        video_id = url.replace('https://www.youtube.com/watch?v=','')[0:11]
        request = youtube.videos().list(part="snippet,contentDetails",id=video_id)
        response = request.execute()
        all_data=response['items'][0]
        return all_data

    classmethod
    def ytDurationToSeconds(self,duration): #eg P1W2DT6H21M32S
        week = 0
        day  = 0
        hour = 0
        min  = 0
        sec  = 0
        duration = duration.lower()
        value = ''
        for c in duration:
            if c.isdigit():
                value += c
                continue
            elif c == 'p':
                pass
            elif c == 't':
                pass
            elif c == 'w':
                week = int(value) * 604800
            elif c == 'd':
                day = int(value)  * 86400
            elif c == 'h':
                hour = int(value) * 3600
            elif c == 'm':
                min = int(value)  * 60
            elif c == 's':
                sec = int(value)

            value = ''
        return week + day + hour + min + sec
    classmethod
    def duration_parsing(self, input):
        return str(timedelta(seconds=input))


