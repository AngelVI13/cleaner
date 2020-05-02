from random import randint
from typing import Dict
import matplotlib.pyplot as plt


def main():
    directories = ["dir1", "dir2", "dir3", "fileA", "fileB"]
    sizes = [randint(0, 5000) for _ in range(len(directories))]
    # add directory/file size next to the label for better readability
    directories = [dir_ + f"\n({sizes[i]})" for i, dir_ in enumerate(directories)]
    dir_info = dict(zip(directories, sizes))
    show_figure(dir_info)


def show_figure(dir_info: Dict[str, float]):
    # Make an example pie plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    labels = dir_info.keys()
    dir_size = sum(dir_info.values())
    sizes = [(size/dir_size) * 100 for size in dir_info.values()]
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
