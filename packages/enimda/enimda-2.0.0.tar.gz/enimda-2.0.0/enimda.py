from random import shuffle

from PIL import Image
import numpy as np

__author__ = 'Anton Smolin'
__copyright__ = 'Copyright (C) 2016-2017 Anton Smolin'
__license__ = 'MIT'
__version__ = '2.0.0'


def _entropy(*, signal):
    """Calculate entropy

    :param signal: 1D signal
    :returns: entropy"""

    _, counts = np.unique(signal, return_counts=True)
    probs = counts / signal.size

    return -np.sum(probs * np.log2(probs))


def _randoms(*, count, limit=None):
    """Get random indexes of values range

    :param count: items count
    :param limit: limits items count if exceeds this
    :returns: set of indexes"""

    randoms = list(range(count))

    if limit is None:
        return set(randoms)

    shuffle(randoms)

    return set(randoms[:limit])


class ENIMDA:
    """ENIMDA class"""

    __multiplier = None
    __frames = None

    def __init__(self, *, fp, size=None, frames=None):
        """Load image

        :param fp: path to file or file object
        :param size: image will be resized to this one
        :param frames: max frames to analyze for GIFs
        :returns: None"""

        self.__multiplier = 1.0
        self.__frames = []

        with Image.open(fp) as image:
            frame_count = 0
            while True:
                frame_count += 1
                try:
                    image.seek(frame_count)
                except EOFError:
                    break
            frame_set = _randoms(count=frame_count, limit=frames)

        with Image.open(fp) as image:
            for frame_index in range(frame_count):
                try:
                    image.seek(frame_index)
                except EOFError:
                    break

                if frame_index not in frame_set:
                    continue

                frame = image.copy()
                if size is not None and \
                        (size < image.width or size < image.height):
                    frame.thumbnail((size, size), resample=Image.NEAREST)
                    self.__multiplier = image.width / frame.width \
                        if image.width > image.height \
                        else image.height / frame.height
                self.__frames.append(frame.convert('L'))

    def __scan(self,
               *,
               frame,
               rows=0.25,
               columns=None,
               threshold=0.5,
               fast=True):
        """Find borders for frame

        :param frame: frame
        :param rows: percent of rows (frame height) to analyze
        :param columns: columns limit
        :param threshold: algorithm agressiveness
        :param fast: only one iteration will be used
        :returns: tuple of border offsets"""

        arr = np.array(frame)
        borders = []

        for side in range(4):
            rot = np.rot90(arr, k=side) if side else arr
            h, w = rot.shape

            if columns is not None:
                rot = np.hstack([
                    rot[0:h, r:r + 1]
                    for r in _randoms(count=w, limit=columns)
                ])
                h, w = rot.shape

            height = round(rows * h)

            border = 0
            while True:
                for start in range(border + 1, height + 1):
                    if _entropy(signal=rot[border:start, 0:w].flatten()) > 0.0:
                        break

                subborder = 0
                delta = threshold
                for center in reversed(range(start, height + 1)):
                    upper = _entropy(signal=rot[border:center, 0:w].flatten())
                    lower = _entropy(
                        signal=rot[center:2 * center - border, 0:w].flatten())
                    diff = upper / lower if lower != 0.0 else delta

                    if diff < delta and diff < threshold:
                        subborder = center
                        delta = diff

                if subborder == 0 or border == subborder:
                    break

                border = subborder

                if fast:
                    break

            borders.append(round(self.__multiplier * border))

        return tuple(borders)

    def scan(self, *, rows=0.25, columns=None, threshold=0.5, fast=True):
        """Find borders for all frames

        :param rows: percent of rows (image height) to analyze
        :param columns: columns limit
        :param threshold: algorithm agressiveness
        :param fast: only one iteration will be used
        :returns: tuple of border offsets"""

        borders = [
            self.__scan(
                frame=frame,
                rows=rows,
                columns=columns,
                threshold=threshold,
                fast=fast) for frame in self.__frames
        ]

        return tuple(
            min(border[side] for border in borders) for side in range(4))
