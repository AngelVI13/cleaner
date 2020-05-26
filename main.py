import os
import time
from typing import Dict
from operator import itemgetter
from collections import OrderedDict
from helpers import get_dir_size, get_dir_info, get_size_str


class DirPlot:
    def __init__(self, directory, top):
        self.__directory = directory
        self.__size = get_dir_size(directory)

        # Calculate directory content info
        content_info = get_dir_info(self.directory)
        content_info = self._format_dir_info(content_info)

        filename = f"{time.time()}.txt"

        print(f"\nShowing results for: {self.directory}\n")

        lines = []
        col_width = max(len(dir_) for dir_ in content_info.keys()) + 2  # padding
        for idx, (dir_, size) in enumerate(content_info.items()):
            line = f"{str(idx+1)} " + "".join([dir_.ljust(col_width), size.ljust(col_width)])
            lines.append(line)
            print(line)

            if idx + 1 == top:
                break

        # write results to file
        with open(filename, "w") as f:
            lines.insert(0, directory)
            f.writelines(f"{line}\n" for line in lines)

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

    def _format_dir_info(self, dir_info: Dict[str, int]) -> Dict[str, str]:
        # exclude empty directories
        dir_info = {dir_: size for dir_, size in dir_info.items() if size > 0}
        # sort entries based on file size
        dir_info = {k: v for k, v in reversed(sorted(dir_info.items(), key=itemgetter(1)))}

        info = OrderedDict()
        for dir_, size in dir_info.items():
            info[os.path.basename(dir_)] = get_size_str(size)

        return info


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if len(args) == 0:
        print("No path provided")
        sys.exit()
    elif len(args) >= 2:
        path, top, *_ = args
        top = int(top)
    else:
        path, *_ = args
        top = 10

    start = time.time()
    DirPlot(os.path.abspath(path), top)
    end = time.time() - start
    print(f"Duration: {end}")
