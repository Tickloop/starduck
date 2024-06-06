import requests
import re
import json
from pytube import YouTube
from typing import List

class Mix:
    def __init__(self, url : str) -> None:
        self.url = url
        self._videos = []
        self.init()
        
    def init(self) -> None:
        pattern = 'var ytInitialData = (.+?);'
        html = requests.get(self.url)
        raw_data = re.findall(pattern, html.text, re.S)
        if raw_data:
            data = json.loads(raw_data[0])
            videos = data['contents']['twoColumnWatchNextResults']['playlist']['playlist']['contents']
            self._videos = [ YouTube( f'https://www.youtube.com/watch?v={video["playlistPanelVideoRenderer"]["videoId"]}' ) for video in videos ]

    @property
    def videos(self) -> List[YouTube]:
        return self._videos

m = Mix('https://www.youtube.com/watch?v=mNEUkkoUoIA&list=RDmNEUkkoUoIA&start_radio=1')
print(m.videos)