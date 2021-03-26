import asyncio
import discord
import youtube_dl
from urllib.parse import parse_qs, urlparse
import googleapiclient.discovery





youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "AIzaSyDZOcdGIepf75qkTS0stb6f_-5XsUB5INs")




ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.seconds = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)






class ytplaylist:
    def __init__(self,url):
        self.url = url
        self.urllist = self.parse_playlist(url,50)
        self.ytvideolist = self.create_ytvideolist(self.urllist)
        self.seconds = self.duration(self.ytvideolist)

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

    classmethod
    def create_ytvideolist(self,urllist):
        ytvideolist = []
        for link in urllist:
            ytvideolist.append(ytvideo(link))
        return ytvideolist

    classmethod
    def duration(self,ytvideolist):
        duration = 0
        for video in ytvideolist:
            duration += video.seconds
        return duration



class ytvideo:
    def __init__(self,input):
        self.url = self.geturl(input)
        self.data = self.getdata(self.url)
        self.duration = self.data['contentDetails']['duration']
        self.title = self.data['snippet']['title']
        self.seconds = self.ytDurationToSeconds(self.duration)

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
        video_id = url.replace('https://www.youtube.com/watch?v=','')
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


