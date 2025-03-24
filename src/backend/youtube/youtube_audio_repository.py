import asyncio
import logging
from logging import Logger
from pathlib import Path
from typing import Any

from yt_dlp import YoutubeDL
from yt_dlp.postprocessor.ffmpeg import ACODECS

from audio_nest.domain.audio import Audio
from audio_nest.domain.audio_codec import AudioCodec
from audio_nest.services.i_audio_repository import IAudioRepository


class YoutubeAudioRepository(IAudioRepository):
    _log: Logger = logging.getLogger(__name__)
    _url_template: str = 'https://www.youtube.com/watch?v={video_id}'
    _output_file_template: str = '{output_file_path}.%(ext)s'
    _bit_rate_kbps: int
    _codec: AudioCodec
    _file_extension: str
    _ffmpeg_path: Path
    _download_directory_path: Path

    def __init__(self, bit_rate_kbps: int, codec: AudioCodec, ffmpeg_path: Path, download_directory_path: Path) -> None:
        self._bit_rate_kbps = bit_rate_kbps
        self._codec = codec
        self._file_extension = ACODECS[codec][0]
        self._ffmpeg_path = ffmpeg_path
        self._download_directory_path = download_directory_path

    async def get_audio_from_source(self, source_id: str) -> Audio:
        self._log.debug(f'Getting audio from YouTube video \'{source_id}\'...')
        audio: Audio = Audio(
            source_id=source_id,
            file_path=self._download_directory_path.joinpath(f'{source_id}.{self._file_extension}'),
            bit_rate_kbps=self._bit_rate_kbps,
            codec=self._codec
        )
        if not audio.file_path.exists():
            await asyncio.to_thread(self._download_audio_from_youtube, video_id=source_id)
        self._log.debug(f'Audio from YouTube video \'{source_id}\' retrieved')
        return audio

    def _download_audio_from_youtube(self, video_id: str) -> None:
        youtube_downloader_options: dict[str, Any] = {
            'ffmpeg_location': self._ffmpeg_path,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'logger': self._log,
            'nocheckcertificate': True,
            'outtmpl': self._output_file_template.format(
                output_file_path=self._download_directory_path.joinpath(video_id)
            ),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self._codec,
                    'preferredquality': str(self._bit_rate_kbps)
                }
            ],
            'prefer_ffmpeg': True,
            'writethumbnail': False
        }
        youtube_downloader: YoutubeDL
        with YoutubeDL(youtube_downloader_options) as youtube_downloader:
            youtube_downloader.download([self._url_template.format(video_id=video_id)])
