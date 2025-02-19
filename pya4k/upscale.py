import os
import tempfile
from pathlib import Path

from . import ac
from . import ffmpeg_handler
from .ac import AC
from .ac import VideoProcessor
from .ac import Parameters
from .ac import Codec

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union, Optional
    from typing import List


def _sanitize_input_paths(input_paths: 'Union[str, Path, List[Union[str, Path]]]') -> 'List[Path]':
    """sanitize input file paths

    Args:
        input_paths (any): input paths variable to sanitize
    """
    sanitized_list = []

    # if input is single file in string format
    # convert it into pathlib.Path object
    if isinstance(input_paths, str):
        sanitized_list.append(Path(input_paths))

    # if the input is single file instead of a list
    # convert it into a list
    elif isinstance(input_paths, Path):
        sanitized_list.append(input_paths)

    # if the input is already a list
    # make sure all elements are path objects
    elif isinstance(input_paths, list):
        for path in input_paths:

            # if the path is not a pathlib.Path object
            # convert it into an object
            if not isinstance(path, Path):
                sanitized_list.append(Path(path))

            # otherwise, the path is clean
            else:
                sanitized_list.append(path)

    # return the sanitized lsit
    return sanitized_list


def show_upscaled_image(
    source_path: Path,
    parameters: Parameters = Parameters(),
    GPU_mode: bool = False,
    ACNet: bool = True,
) -> None:
    """display an image processed by Anime4K09 or ACNet

    Args:
        source_path: input file path.
        parameters (Parameters, optional): custom arguments passed to Anime4KCPP.
        GPU_mode (bool, optional): enable GPU mode. Defaults to False.
        ACNet (bool, optional): enable ACNet mode. Defaults to True.

    Raises:
        ACError
    """
    if GPU_mode:
        if ACNet:
            ac_object = AC(
                managerList=ac.ManagerList([ac.OpenCLACNetManager(pID=0, dID=0)]),
                parameters=parameters,
                type=ac.ProcessorType.OpenCL_ACNet,
            )
        else:
            ac_object = AC(
                managerList=ac.ManagerList([ac.OpenCLACNetManager(pID=0, dID=0)]),
                parameters=parameters,
                type=ac.ProcessorType.OpenCL_Anime4K09,
            )
    else:
        if ACNet:
            ac_object = AC(
                managerList=None,
                parameters=parameters,
                type=ac.ProcessorType.CPU_ACNet,
            )
        else:
            ac_object = AC(
                managerList=None,
                parameters=parameters,
                type=ac.ProcessorType.CPU_Anime4K09,
            )
    ac_object.load_image(str(source_path))
    ac_object.process()
    ac_object.show_image()


def upscale_images(
    input_paths: 'Union[str, Path, List[Union[str, Path]]]',
    output_suffix: str = "_output",
    output_path: 'Optional[Path]' = None,
    parameters: Parameters = Parameters(),
    GPU_mode: bool = False,
    ACNet: bool = True,
) -> None:
    """upscale a list of image files with Anime4K

    Args:
        input_paths (list): list of input file paths
        output_suffix (str, optional): output files. Defaults to "_output".
        output_path (pathlib.Path, optional): parent directory of output paths. Defaults to None.
        parameters (Parameters, optional): custom arguments passed to Anime4KCPP.
        GPU_mode (bool, optional): enable GPU mode. Defaults to False.
        ACNet (bool, optional): enable ACNet mode. Defaults to True.

    Raises:
        FileExistsError: when output path exists and isn't a directory
        ACError
    """

    # sanitize input list
    _input_paths: 'List[Path]' = _sanitize_input_paths(input_paths)

    # if destination path unspecified
    if output_path is None:

        # destination path is first input file's parent directory
        output_path = _input_paths[0].parent

    # if destination path doesn't exist
    if not output_path.exists():
        # create directory and its parents if necessary
        output_path.mkdir(parents=True, exist_ok=True)

    # else if it already exists but isn't a directory
    elif not output_path.is_dir():
        raise FileExistsError("destination path already exists and isn't a directory")

    # create Anime4K object
    if GPU_mode:
        if ACNet:
            ac_object = AC(
                managerList=ac.ManagerList([ac.OpenCLACNetManager(pID=0, dID=0)]),
                parameters=parameters,
                type=ac.ProcessorType.OpenCL_ACNet,
            )
        else:
            ac_object = AC(
                managerList=ac.ManagerList([ac.OpenCLACNetManager(pID=0, dID=0)]),
                parameters=parameters,
                type=ac.ProcessorType.OpenCL_Anime4K09,
            )
    else:
        if ACNet:
            ac_object = AC(
                managerList=None,
                parameters=parameters,
                type=ac.ProcessorType.CPU_ACNet,
            )
        else:
            ac_object = AC(
                managerList=None,
                parameters=parameters,
                type=ac.ProcessorType.CPU_Anime4K09,
            )

    # process each of the files in the list
    for path in _input_paths:

        # anime4k load and process image
        ac_object.load_image(str(path))
        ac_object.process()

        # construct destination file path object
        output_file_path = output_path.joinpath(
            (path.stem + output_suffix + path.suffix)
        )

        print(f"Saving file to: {output_file_path}")
        ac_object.save_image(str(output_file_path))


def upscale_videos(
    input_paths: 'Union[str, Path, List[Union[str, Path]]]',
    output_suffix: str = "_output",
    output_path: 'Optional[Path]' = None,
    parameters: Parameters = Parameters(),
    GPU_mode: bool = False,
    ACNet: bool = True,
    codec: int = Codec.MP4V,
) -> None:
    # FIXME: Too many RAM usage because too many parallel tasks.. Make limit! or etc.
    """upscale a list of video files with Anime4k

    Args:
        input_paths (list): list of input file paths
        output_suffix (str, optional): output files suffix. Defaults to "_output".
        output_path (pathlib.Path, optional): parent directory of output paths. Defaults to None.
        parameters (Parameters, optional): custom arguments passed to Anime4KCPP.
        GPU_mode (bool, optional): enable GPU mode. Defaults to False.
        ACNet (bool, optional): enable ACNet mode. Defaults to True.
        codec (Codec, optional): codec for video encodeing.  Defaults to MP4V

    Raises:
        FileExistsError: when output path exists and isn't a directory
        ACError
    """

    # sanitize input list
    input_paths_: 'List[Path]' = _sanitize_input_paths(input_paths)

    # if destination path unspecified
    if output_path is None:

        # destination path is first input file's parent directory
        output_path = input_paths_[0].parent

    # if destination path doesn't exist
    if not output_path.exists():
        # create directory and its parents if necessary
        output_path.mkdir(parents=True, exist_ok=True)

    # else if it already exists but isn't a directory
    # ??
    elif not output_path.is_dir():
        raise FileExistsError("destination path already exists and isn't a directory")

    # create anime4k object
    if GPU_mode:
        if ACNet:
            ac_object = AC(
                managerList=ac.ManagerList([ac.OpenCLACNetManager(pID=0, dID=0)]),
                parameters=parameters,
                type=ac.ProcessorType.OpenCL_ACNet,
            )
        else:
            ac_object = AC(
                managerList=ac.ManagerList([ac.OpenCLACNetManager(pID=0, dID=0)]),
                parameters=parameters,
                type=ac.ProcessorType.OpenCL_Anime4K09,
            )
    else:
        if ACNet:
            ac_object = AC(
                managerList=None,
                parameters=parameters,
                type=ac.ProcessorType.CPU_ACNet,
            )
        else:
            ac_object = AC(
                managerList=None,
                parameters=parameters,
                type=ac.ProcessorType.CPU_Anime4K09,
            )

    video_processor = VideoProcessor(ac_object)

    # process each of the files in the list
    for path in input_paths_:

        # create temporary directory to save the upscaled video
        temporary_directory = Path(tempfile.mkdtemp())
        temporary_video_file_path = temporary_directory.joinpath("temp.mp4")

        # process and save video file to temp/temp.mp4
        video_processor.load_video(str(path))
        video_processor.set_save_video_info(str(temporary_video_file_path), codec)
        video_processor.process_with_progress()
        video_processor.save_video()

        ffmpeg_handler.migrate_audio_streams(
            upscaled_video=temporary_video_file_path,
            original_video=path,
            output_path=output_path.joinpath(path.stem + output_suffix + path.suffix),
        )
        # clean up temp video after we're done with it
        os.remove(temporary_video_file_path)

