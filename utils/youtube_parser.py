from typing import Optional

from youtube_transcript_api import YouTubeTranscriptApi

from config import LANGUAGE
from loggings import logger


class YoutubeParser:
    def __init__(self):
        self._client = YouTubeTranscriptApi()

    def fetch(self, video_url: str) -> Optional[str]:
        """
        Fetch the transcript of a YouTube video.
        :param video_url:
        :return:
        """
        # Extract the video ID from the URL
        video_id = video_url.split("v=")[-1]
        if "&" in video_id:
            video_id = video_id.split("&")[0]

        try:
            # Get the transcript
            transcript = self._client.fetch(video_id, languages=(LANGUAGE, "pt", "pt-BR", "en-US",))  # Specify the language

            # Combine the transcript into a single string
            transcript_text = " ".join(
                [
                    f"{item.start} - {item.start + item.duration}: {item.text}"
                    for item in transcript
                ]
            )

            return transcript_text
        except Exception as e:
            logger(f"Failed to fetch transcript for video {video_url}: {e}", level="error")
