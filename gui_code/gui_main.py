from tkinter import Frame, Label, Tk
from matplotlib import style
import time
from option_page import OptionPage

style.use("ggplot")

PADDING = 15
GREEN = "#64975E"
AMBER = "#D2A833"
RED = "#C34A4D"
BACKGROUND = "#E7F5EF"
TIME_INTERVAL = 1
TIME_AT_START = time.time()


class FarmBeatsApp:
    def __init__(self, master):
        self.u = 0
        self.main = master
        self.label_frame = Frame(self.main)
        self.label = None
        self.label_frame_setup()
        self.option_frame = Frame(self.main, bg="white")
        self.profile_frame = Frame(self.main, bg="white")
        OptionPage(self.option_frame, self.profile_frame, self.label_frame, self.label)

    def label_frame_setup(self):
        self.label = Label(self.label_frame, text="IoT FarmBeats", width=60)
        self.label.config(background=BACKGROUND, font=("Courier", 25))
        self.label.pack()
        self.label_frame.pack()


def main():
    root = Tk()
    root.geometry("900x600")
    root.config(bg=BACKGROUND)
    root.resizable(False, False)
    FarmBeatsApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
