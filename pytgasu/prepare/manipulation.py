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
            return image.size
    except IOError:
        return None  # not a picture or just 404


def _categorise_with_tagging(file_list):
    # actually take in a list of (path, dimensions)
    # return a list of (path, tags=list)
    # heavily customised, no value of reuse
    ret = list()
    for t in file_list:
        tags = ProcessTags.NOPROCESS
        if not any([x == 512 for x in t[1]]):
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
    for tag, dst in dirs_with_tags.items():
        dst.mkdir(exist_ok=False)
        for f in {fp for (fp, ftag) in src_with_tags if ftag == tag}:
            f.rename(dst.joinpath(f.name))


def _move_from_dir_with_tags(dirs_with_tags, dst):
    # src/* -> dst/*; rm src/
    for tag, src in dirs_with_tags.items():
        for f in src.iterdir():
            f.rename(dst.joinpath(f.name))
        src.rmdir()
# endregion


# region image operations
def _w2x_upscale(d, scale_by_width):
    """Upscale all png in ``d`` using waifu2x."""
    path_to_w2x_caffe = ''

    w2x_std_params = [
        '-l', 'png:bmp:jpg', '-e', 'png', '-d', '8',
        '-m', 'noise_scale', '-n', '2',
        '-p', 'gpu',
        '-c', '256'
    ]
    w2x_partial_cmdline = [path_to_w2x_caffe] + w2x_std_params

    scale_by = ('-h', '-w')[int(scale_by_width)]
    w2x_full_cmdline = w2x_partial_cmdline + [scale_by, '512', '-i', str(d), '-o', str(d)]
    subprocess.run(w2x_full_cmdline, encoding='utf-16-le')


def _pil_scale(d, scale_by_width=None):
    """*scale all png in ``d`` using Pillow."""
    # scale_by_width is unused here
    for fp in d.iterdir():
        with Image.open(fp) as i:
            scale_ratio = 512 / max(i.size)
            final_size = tuple(int(x * scale_ratio) for x in i.size)
            resized = i.resize(final_size, resample=Image.LANCZOS)
            resized.save(fp=fp, format='PNG')


def _shrink_png(imgs):
    """Reduce size of all ``img``s specified using Pillow."""
    for fn in imgs:
        with Image.open(fn) as i:
            i.save(fp=fn, format='PNG', optimize=True)
# endregion


def prepare_image_files(set_dir):
    from pathlib import Path

    set_dir = Path(set_dir)
    imgs = sorted([set_dir.glob(f'*.{fmt}') for fmt in ['png', 'bmp', 'jpg']])
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

    _upscale(directories[ProcessTags.UPBYWIDTH], scale_by_width=True)
    _upscale(directories[ProcessTags.UPBYHEIGHT], scale_by_width=False)
    _pil_scale(directories[ProcessTags.DOWNSCALE])

    _move_from_dir_with_tags(directories, set_dir)

    _shrink_png([fn for fn in list(zip(*imgs))[0] if fn.stat().st_size > 512 * 1000])
