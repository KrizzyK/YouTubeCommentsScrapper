# pojo class

class VideoData:

    def __init__(self, videoName: str, videoUrl: str) -> None:
        self.videoName = videoName
        self.videoUrl = videoUrl

    def __str__(self):
        return "VideoName = " + self.videoName + " VideoUrl = " + self.videoUrl
