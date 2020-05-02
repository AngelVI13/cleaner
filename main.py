import os
from typing import Dict
import matplotlib.pyplot as plt


KILOBYTE = 10 ** 3
MEGABYTE = 10 ** 6
GIGABYTE = 10 ** 9


def main():
    dir_info = get_dir_info("..")
    # exclude empty directories
    dir_info = {dir_: size for dir_, size in dir_info.items() if size > 0}

    info = {}
    for dir_, size in dir_info.items():
        dir_ += f"\n{get_size_str(size)}"
        info[dir_] = size

    show_figure(info)


def get_size_str(size: int) -> str:
    if 0 < size < MEGABYTE:
        return f"{size/KILOBYTE:.2f} KiB"
    elif MEGABYTE < size < GIGABYTE:
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
    items = os.listdir(directory)
    items = [os.path.join(directory, item) for item in items]

    sizes = []
    for item in items:
        if os.path.isfile(item):
            sizes.append(os.path.getsize(item))
            continue

        sizes.append(get_dir_size(item))

    return dict(zip(items, sizes))


def show_figure(dir_info: Dict[str, float]) -> None:
    # Make an example pie plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    labels = dir_info.keys()
    dir_size = sum(dir_info.values())
    sizes = [(size / dir_size) * 100 for size in dir_info.values()]
    wedges, plt_labels = ax.pie(sizes, labels=labels)
    ax.axis("equal")

    make_picker(fig, wedges)
    plt.show()


def make_picker(fig, wedges):
    def onclick(event):
        wedge = event.artist
        label = wedge.get_label()
        print(label)

    # Make wedges selectable
    for wedge in wedges:
        wedge.set_picker(True)

    fig.canvas.mpl_connect("pick_event", onclick)


if __name__ == "__main__":
    main()
