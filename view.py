from tkinter import filedialog
from tkinter import *


class Viewer:
    def __init__(self):
        self.path_list = list()
        self.show()

    def open_song(self):
        file_paths = filedialog.askopenfilenames(initialdir='/', title='Choose song',
                                                 filetypes=(('mp4', '*.m4a'), ('mp4', '*.mp4')))
        file_paths = list(file_paths)
        self.path_list = file_paths

    def show(self):
        window = Tk()
        window.title('Tag your music')
        label1 = Label(window, text='Welcome')
        label1.pack()
        button1 = Button(window, text='Choose song', command=self.open_song)
        button1.pack()

        window.mainloop()

v = Viewer()