from pathlib import Path

import ffmpeg

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union


def migrate_audio_streams(upscaled_video: 'Union[str, Path]', original_video: 'Union[str, Path]', output_path: 'Union[str, Path]') -> None:
    upscaled_video = Path(upscaled_video)
    original_video = Path(original_video)
    output_path = Path(output_path)
    upscaled_input = ffmpeg.input(str(upscaled_video.absolute()))
    original_input = ffmpeg.input(str(original_video.absolute()))

    # find upscaled video stream and original audio stream
    upscaled_video = upscaled_input.video
    original_audio = original_input.audio

    # create output file with selected streams
    output = ffmpeg.output(
        upscaled_video, original_audio, str(output_path.absolute()), c="copy"
    )
    output.run()
