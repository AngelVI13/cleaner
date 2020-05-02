import os
from typing import Dict
import matplotlib.pyplot as plt


KILOBYTE = 10 ** 3
MEGABYTE = 10 ** 6
GIGABYTE = 10 ** 9


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
        self.__directory = directory
        self.__size = get_dir_size(directory)
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
        self.__size = get_dir_size(path)

    def _create_plot(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

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
        labels = content_info.keys()
        dir_size = sum(content_info.values())
        sizes = [(size / dir_size) * 100 for size in content_info.values()]
        wedges, plt_labels = self.ax.pie(sizes, labels=labels)
        self.ax.axis("equal")

        self.make_picker(self.fig, wedges)

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

        try:
            plt.show()
        except AttributeError:
            # For some reason when closing diagram it throws AttributeError
            pass

    def make_picker(self, fig, wedges):
        def onclick(event):
            wedge = event.artist
            label = wedge.get_label()

            path, *_ = label.split("\n")
            self.directory = path
            self.show_figure()

        # Make wedges selectable
        for wedge in wedges:
            wedge.set_picker(True)

        fig.canvas.mpl_connect("pick_event", onclick)


if __name__ == "__main__":
    DirPlot("..")
