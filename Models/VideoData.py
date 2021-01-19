# pojo class

class VideoData:

    def __init__(self, videoName: str, videoUrl: str, commentsPath: str, likeDislikeRatio: str, commentsCount: str) -> None:
        self.videoName = videoName
        self.videoUrl = videoUrl
        self.commentsPath = commentsPath
        self.likeDislikeRatio = likeDislikeRatio
        self.commentsCount = commentsCount


    def __str__(self):
        return "VideoName = " + self.videoName + " VideoUrl = " + self.videoUrl
