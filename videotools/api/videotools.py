import ffmpeg
from pathlib import Path

from .types import Dest, Source


class FileIO:
    """Class that sanitizes string inputs for source and dest."""

    def __init__(self, source_video: Source, dest_video: Dest = ''):
        self.source = self.process_source(source_video)
        self.dest = self.process_dest(dest_video, self.source)
        self.probe = self.check_video_input(self.source)

    @staticmethod
    def check_video_input(source: Source) -> dict:
        try:
            probe = ffmpeg.probe(source)
        except ffmpeg.Error as e:
            message = e.stderr.decode().splitlines()[-1]
            raise Exception(message)

        return probe

    @staticmethod
    def process_source(source: Source) -> Path:
        """Check that the source file exists and store its path."""
        path = Path(source)
        if not path.is_file():
            raise FileNotFoundError(f"'{source.resolve()}' not found")
        return path

    @staticmethod
    def process_dest(dest: Dest, source: Path) -> Path:
        """Process the destination input string and return a coherent path."""
        path = Path(dest)
        default_name = f'{source.stem}_output{source.suffix}'
        default_path = source.with_name(default_name)

        if path.is_dir():
            return path.joinpath(default_name).with_suffix(source.suffix)
        if path.is_file() and not path.is_symlink():
            return path

        return default_path

    def reduce_size_to(self, size_bytes: int):
        """Reduce the video to provided size (in bytes)."""
        input_size_bits = self.source.stat().st_size * 8
        input_length_seconds = float(self.probe['format']['duration'])
        bitrate = int(input_size_bits / input_length_seconds)

        stream = (
            ffmpeg
            .input(str(self.source))
            .output(str(self.dest), video_bitrate=bitrate)
            .run_async()
        )

        return stream.communicate()
