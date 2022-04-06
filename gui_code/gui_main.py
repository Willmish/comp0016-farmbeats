from tkinter import Frame, Label, Tk
from option_view.option_page import OptionPage
from tools.constants import Constants
from data_streamer.gui_database_manager import GuiDatabaseManager


class FarmBeatsApp:
    def __init__(self, master, db: GuiDatabaseManager):
        self.u = 0
        self.main = master
        self.label_frame = Frame(self.main)
        self.label = None
        self.label_frame_setup()
        self.option_frame = Frame(self.main, bg="white")
        self.profile_frame = Frame(self.main, bg="white")
        self._db_manager: GuiDatabaseManager = db
        OptionPage(
            self.option_frame,
            self.profile_frame,
            self.label_frame,
            self.label,
            self._db_manager,
        )

    def label_frame_setup(self):
        self.label = Label(self.label_frame, text="IoT FarmBeats", width=60)
        self.label.config(
            background=Constants.BACKGROUND.value, font=("Courier", 25)
        )
        self.label.pack()
        self.label_frame.pack()


def main():
    with GuiDatabaseManager() as db:
        root = Tk()
        root.geometry("1200x600")
        root.config(bg=Constants.BACKGROUND.value)
        root.resizable(False, False)
        FarmBeatsApp(root, db)

        root.mainloop()


if __name__ == "__main__":
    main()
