import os
import contextlib
from . import ffmpeg_handler

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union
    from pathlib import Path


def migrate_audio_streams(
    upscaled_video: 'Union[str, Path]', original_video: 'Union[str, Path]', output_path: 'Union[str, Path]'
) -> None:
    """ migrate audio streams

    Args:
        upscaled_video (str): path of upscaled video.
        original_video (str): path of original video.
        output_path (str): path to output result.

    Raises:
        FileExistsError: when output path exists and isn't a directory
    """
    ffmpeg_handler.migrate_audio_streams(
        upscaled_video=upscaled_video,
        original_video=original_video,
        output_path=output_path,
    )

    with contextlib.suppress(FileNotFoundError):
        os.remove(upscaled_video)

