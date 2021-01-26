# pojo class

class VideoData:

    def __init__(self, videoName: str, videoUrl: str,
                 commentsPath: str, videoView, comments, commentsCount) -> None:
        self.videoName = videoName
        self.videoUrl = videoUrl
        self.commentsPath = commentsPath
        self.commentsCount = commentsCount
        self.comments = comments
        self.videoView = videoView


    def __str__(self):
        return "VideoName = " + self.videoName + " VideoUrl = " + self.videoUrl
