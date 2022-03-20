from tkinter import Frame, Label, Tk
from option_page import OptionPage
from constants import Constants


class FarmBeatsApp:
    def __init__(self, master):
        self.u = 0
        self.main = master
        self.label_frame = Frame(self.main)
        self.label = None
        self.label_frame_setup()
        self.option_frame = Frame(self.main, bg="white")
        self.profile_frame = Frame(self.main, bg="white")
        OptionPage(
            self.option_frame, self.profile_frame, self.label_frame, self.label
        )

    def label_frame_setup(self):
        self.label = Label(self.label_frame, text="IoT FarmBeats", width=60)
        self.label.config(
            background=Constants.BACKGROUND, font=("Courier", 25)
        )
        self.label.pack()
        self.label_frame.pack()


def main():
    root = Tk()
    root.geometry("900x600")
    root.config(bg=Constants.BACKGROUND)
    root.resizable(False, False)
    FarmBeatsApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
