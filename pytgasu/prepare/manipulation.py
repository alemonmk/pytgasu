import subprocess
from enum import Flag
from functools import partial
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
def _w2x_upscale(w2x_path, d, scalebywidth):
    """Upscale all png in ``d`` using waifu2x."""
    path_to_w2x_caffe = w2x_path

    w2x_std_params = [
        '-l', 'png', '-e', 'png', '-d', '8',
        '-m', 'auto_scale', '-n', '2',
        '-p', 'gpu',  # TODO: auto detect
        '-c', '256'
    ]
    w2x_partial_cmdline = [path_to_w2x_caffe] + w2x_std_params

    scale_by = ('-h', '-w')[int(scalebywidth)]
    w2x_full_cmdline = w2x_partial_cmdline + [scale_by, '512', '-i', str(d), '-o', str(d)]
    subprocess.run(w2x_full_cmdline, encoding='utf-16-le')


def _pil_scale(d, scalebywidth=None):
    """*scale all png in ``d`` using Pillow."""
    # scalebywidth is unused here
    for fp in d.iterdir():
        with Image.open(fp) as i:
            scale_ratio = 512 / max(i.size)
            final_size = tuple(int(x * scale_ratio) for x in i.size)
            resized = i.resize(final_size, resample=Image.LANCZOS)
            
            
            resized.save(fp=fp, format='PNG')

def _transparentize(d, t):
    for fp in d.iterdir():
        with Image.open(fp) as resized:
            resized = resized.convert('RGBA')
            datas = resized.getdata()
            newData = []
            for item in datas:
                if item[0] == t[0] and item[1] == t[1] and item[2] == t[2]:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)

            resized.putdata(newData)
            resized.save(fp=fp, format='PNG')

def _shrink_png(imgs):
    """Reduce size of all ``img``s specified using Pillow."""
    for fn in imgs:
        with Image.open(fn) as i:
            i.save(fp=fn, format='PNG', optimize=True)
# endregion


def prepare_image_files(set_dir, w2x_path, transparent):
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
 
    _upscale = partial(_w2x_upscale, w2x_path)\
        if platform == 'win32' and w2x_path is not None\
        else _pil_scale
    
    _upscale(directories[ProcessTags.UPBYWIDTH], scalebywidth=True)
    _upscale(directories[ProcessTags.UPBYHEIGHT], scalebywidth=False)
    _pil_scale(directories[ProcessTags.DOWNSCALE])

    _move_from_dir_with_tags(directories, set_dir)

    if transparent is not None and len(transparent) == 3:
        _transparentize(set_dir, transparent)

    _shrink_png([fn for fn in list(zip(*imgs))[0] if fn.stat().st_size > 350 * 1000])
