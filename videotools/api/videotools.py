import ffmpeg
from pathlib import Path
from typing import TypeVar, Optional

Source = TypeVar('Source', str, Path)
Dest = Optional[Source]


class VideoTools:

    def __init__(self, source_video: Source, dest_video: Dest):
        self.source = self.process_source(source_video)
        if self.dest_video is None:
            print(ffmpeg)
            print('Dest none')

    @staticmethod
    def process_source(source: Source) -> Path:
        path = Path(source)
        if not source.is_file():
            raise FileNotFoundError
        return path
