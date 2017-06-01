import subprocess
from enum import Flag
from PIL import Image

__all__ = ['prepare_image_files']


# region utilities
class ProcessTags(Flag):
    # temporary flags
    UPSCALE = 4
    BYWIDTH = 2
    BYHEIGHT = 1
    # final flags
    NOPROCESS = 0
    UPBYWIDTH = UPSCALE | BYWIDTH
    UPBYHEIGHT = UPSCALE | BYHEIGHT
    DOWNSCALE = 8


def _get_img_dimensions(fn):
    try:
        with Image.open(fn) as image:
            return image.size if image.format == 'PNG' else False
    except IOError:
        return False  # not a picture or just 404


def _categorise_with_tagging(file_list):
    # actually take in a list of (path, dimensions)
    # return a list of (path, tags=list)
    # heavily customised, no value of reuse
    ret = list()
    for t in file_list:
        tags = ProcessTags.NOPROCESS
        if not any([x - 512 == 0 for x in t[1]]):
            if max(t[1]) < 512:
                tags |= ProcessTags.UPSCALE
            else:
                tags |= ProcessTags.DOWNSCALE
        if tags == ProcessTags.UPSCALE:
            w, h = t[1]
            if w >= h:
                tags |= ProcessTags.BYWIDTH
            else:
                tags |= ProcessTags.BYHEIGHT
        entry = (t[0], tags)
        ret.append(entry)
    return ret


def _move_to_dir_by_tags(src_with_tags, dirs_with_tags):
    # mkdir dst; [file] -> dst/
    for dst, tag in dirs_with_tags:
        dst.mkdir(exist_ok=False)
        for f in {fp for (fp, ftag) in src_with_tags if ftag == tag}:
            f.rename(dst.joinpath(f.name))


def _move_from_dir_with_tags(dirs_with_tags, dst):
    # src/* -> dst/*; rm src/
    for src, t in dirs_with_tags:
        for f in src.iterdir():
            f.rename(dst.joinpath(f.name))
        src.rmdir()
# endregion


# region image operations
# w2x upscaling
def _w2x_upscale(d=None, scalebywidth):
    pass


# conventional scaling
def _pil_scale(d, scalebywidth=None):
    pass


# optimize png
def _shrink_png(imgs):
    pass
# endregion


def prepare_image_files(set_dir):
    from pathlib import Path

    set_dir = Path(set_dir)
    # TODO: include bmp & jpg support
    imgs = sorted(set_dir.glob('*.png'))
    imgs = [(p, d) for p, d in zip(imgs, [_get_img_dimensions(fn) for fn in imgs]) if d]
    imgs = _categorise_with_tagging(imgs)

    directories = {
        ProcessTags.UPBYWIDTH: set_dir / 'uw',
        ProcessTags.UPBYHEIGHT: set_dir / 'uh',
        ProcessTags.DOWNSCALE: set_dir / 'd',
    }
    _move_to_dir_by_tags(imgs, directories)

    from sys import platform
    _upscale = _w2x_upscale if platform == 'win32' else _pil_scale

    _upscale(directories[ProcessTags.UPBYWIDTH], scalebywidth=True)
    _upscale(directories[ProcessTags.UPBYHEIGHT], scalebywidth=False)
    _pil_scale(directories[ProcessTags.DOWNSCALE])

    _move_from_dir_with_tags(directories, set_dir)

    _shrink_png([fn for fn in list(zip(*imgs))[0] if fn.stat().st_size > 350 * 1000])
