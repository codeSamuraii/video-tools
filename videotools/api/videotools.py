import ffmpeg
from pathlib import Path

from .types import Dest, Source


class VideoTools:

    def __init__(self, source_video: Source, dest_video: Dest = ''):
        self.source = self.process_source(source_video)
        self.dest = self.process_dest(dest_video)

    @staticmethod
    def check_ffmpeg():
        print(ffmpeg)

    @staticmethod
    def process_source(source: Source) -> Path:
        path = Path(source)
        if not path.is_file():
            raise FileNotFoundError
        return path

    def process_dest(self, dest: Dest) -> Path:
        path = Path(dest)
        default_name = f'{self.source.stem}_output'
        default_path = self.source.with_name(default_name)

        if path.is_dir():
            return path / default_name
        if path.is_file() and not path.is_symlink():
            return path

        return default_path
