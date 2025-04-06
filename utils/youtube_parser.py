from typing import Optional

from youtube_transcript_api import YouTubeTranscriptApi
from exceptions import YoutubeParserError
from config import LANGUAGE


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
                    item.text
                    for item in transcript if item.duration
                ]
            )

            return transcript_text
        except Exception as e:
            raise YoutubeParserError(f"Failed to fetch transcript for video {video_url}: {e}")
