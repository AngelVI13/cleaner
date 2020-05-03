import os
from typing import Dict
from contextlib import suppress
import matplotlib.pyplot as plt


KILOBYTE = 10 ** 3
MEGABYTE = 10 ** 6
GIGABYTE = 10 ** 9


def get_size_str(size: int) -> str:
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


class DirPlot:
    def __init__(self, directory):
        # todo add keyboard_handlers to delete or go up or down a folder
        # todo https://matplotlib.org/3.1.1/users/event_handling.html
        self.__directory = directory
        self.__size = get_dir_size(directory)
        self._selected = None  # selected element from the pie chart

        self._create_plot()

        self.show_figure()

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, _value):
        raise RuntimeError("Setting `size` attribute directly not allowed.")

    @property
    def directory(self):
        return self.__directory

    @directory.setter
    def directory(self, path):
        self.__directory = path
        self.__size = (
            get_dir_size(path) if os.path.isdir(path) else os.path.getsize(path)
        )

    def _create_plot(self):
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect("pick_event", self.onclick)
        self.ax = self.fig.add_subplot(111)

    def onclick(self, event):
        wedge = event.artist
        label = wedge.get_label()

        if self._selected is None or self._selected != label:
            # 1st case - Nothing is selected
            # 2nd case - Something is selected but we clicked on something else
            self._selected = label
        else:  # self._selected == label
            path, *_ = label.split("\n")
            self.directory = path
            self._selected = None  # reset selection

        self._update_plot_data()

    def _update_plot_data(self):
        # Clear existing data on plot
        self.ax.clear()

        # Calculate directory content info
        content_info = get_dir_info(self.directory)
        content_info = self._format_dir_info(content_info)

        # Set plot title
        title = f"Path: {self.directory} ({get_size_str(self.size)})"
        self.ax.set_title(title)

        # Calculate chart item proportions
        labels = list(content_info.keys())
        dir_size = sum(content_info.values())
        sizes = [(size / dir_size) * 100 for size in content_info.values()]

        # Exploded parts
        exploded = [0 for _ in range(len(labels))]
        if self._selected:
            # explode selected part of the pie chart
            with suppress(ValueError):
                exploded[labels.index(self._selected)] = 0.1

        # Add data to axis
        wedges, plt_labels = self.ax.pie(sizes, labels=labels, explode=exploded)
        self.ax.axis("equal")
        self.ax.figure.canvas.draw()

        # Make wedges selectable
        self.make_picker(wedges)

    def _format_dir_info(self, dir_info: Dict[str, int]) -> Dict[str, int]:
        # exclude empty directories
        dir_info = {dir_: size for dir_, size in dir_info.items() if size > 0}

        info = {}
        for dir_, size in dir_info.items():
            dir_ += f"\n{get_size_str(size)}"
            info[dir_] = size

        return info

    def show_figure(self) -> None:
        self._update_plot_data()

        plt.show()

    def make_picker(self, wedges):
        # Make wedges selectable
        for wedge in wedges:
            wedge.set_picker(True)


if __name__ == "__main__":
    DirPlot("..")
