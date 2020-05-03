import os
from typing import Dict

KILOBYTE = 10 ** 3
MEGABYTE = 10 ** 6
GIGABYTE = 10 ** 9


def get_size_str(size: int) -> str:
    """Get a string representation of the item's size.
    Depending on the size, the value is converted to KiB/MiB/GiB.

    :param size: Item's size in bytes
    :return: The string representation of the item's size
    """
    if 0 <= size < MEGABYTE:
        return f"{size/KILOBYTE:.2f} KiB"
    elif MEGABYTE <= size < GIGABYTE:
        return f"{size/MEGABYTE:.2f} MiB"
    else:
        return f"{size/GIGABYTE:.2f} GiB"


def get_dir_size(start_path: str = ".") -> int:
    """Computes size of a directory in bytes.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def get_dir_info(directory: str) -> Dict[str, int]:
    """Get dictionary of every file/dir in a current directory and its
    respective size in bytes.

    :param directory: Target directory which to get info for
    :return: Dictionary with file/dir and corresponding byte size
    """
    if not os.path.isdir(directory):
        return {}

    items = os.listdir(directory)
    items = [os.path.join(directory, item) for item in items]

    sizes = []
    for item in items:
        if os.path.isfile(item):
            sizes.append(os.path.getsize(item))
            continue

        sizes.append(get_dir_size(item))

    return dict(zip(items, sizes))
