from typing import List

from dataDownload.VideoData import VideoData


class ChannelData:
    # not sure if this is necessary yet
    channelName = ''
    iconPath = ''
    videosData = []
    # not ideal, but I let it stay for now
    subsCount = ''

    def __init__(self, channelName: str, subsCount: str, iconPath: str, videosData: List[VideoData]):
        self.channelName = channelName
        self.subsCount = subsCount
        self.iconPath = iconPath
        self.videosData = videosData

    def __str__(self):
        vidData = [video.__str__() for video in self.videosData]
        return "ChannelName = " + self.channelName + ", SubsCount = " + self.subsCount + ", iconPath = " + self.iconPath + ", videosData =\n" + " ".join(vidData)