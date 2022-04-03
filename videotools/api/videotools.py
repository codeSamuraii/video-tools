import ffmpeg
from pathlib import Path

from .types import Dest, Source


class VideoTools:

    def __init__(self, source_video: Source, dest_video: Dest = ''):
        self.source = self.process_source(source_video)
        self.dest = self.process_dest(dest_video, self.source)
        self.stream = self.get_stream(self.source)

    @staticmethod
    def get_stream(source):
        try:
            probe = ffmpeg.probe(source)
        except ffmpeg.Error as e:
            message = e.stderr.decode().splitlines()[-1]
            raise Exception(message)

        if probe['streams'][0]['codec_type'] == 'video':
            return True
        else:
            return False

    @staticmethod
    def process_source(source: Source) -> Path:
        path = Path(source)
        if not path.is_file():
            raise FileNotFoundError(f"'{source.resolve()}' not found")
        return path

    @staticmethod
    def process_dest(dest: Dest, source: Path) -> Path:
        path = Path(dest)
        default_name = f'{source.stem}_output{source.suffix}'
        default_path = source.with_name(default_name)

        if path.is_dir():
            return path.joinpath(default_name).with_suffix(source.suffix)
        if path.is_file() and not path.is_symlink():
            return path

        return default_path
