from tkinter import Frame, Label, Tk
from option_view.option_page import OptionPage
from tools.constants import Constants
from data_streamer.gui_database_manager import GuiDatabaseManager


class FarmBeatsApp:
    """
    FarmBeatsApp is the overall class representing the GUI. This is
    instantiated whenever the user starts the app.
    """

    def __init__(self, master: Tk, db: GuiDatabaseManager):
        """
        __init__ creates an instance of FarmBeatsApp.

        :param master: This is the root window of the GUI.
        :type master: Tk
        :param db: Azure database to access data from
            sensors and actuators.
        :type db: GuiDatabaseManager
        """
        self.u = 0
        self.main = master
        self.label_frame = Frame(self.main)
        self.label = None
        self.label_frame_setup()
        self._db_manager: GuiDatabaseManager = db
        OptionPage(
            self.main,
            self.label_frame,
            self.label,
            self._db_manager,
        )
        self.reset_plant_profile()

    def label_frame_setup(self):
        """
        label_frame_setup displays the title of the to label_frame.
        """
        self.label = Label(self.label_frame, text="IoT FarmBeats", width=60)
        self.label.config(
            background=Constants.BACKGROUND.value, font=("Courier", 25)
        )
        self.label.pack()
        self.label_frame.pack()

    def reset_plant_profile(self):
        """
        reset_plant_profile copies information from
        default_plant_profile_info.ini to plant_profile_info.ini,
        ensuring the starting config file is always valid.
        """
        with open("tools/default_plant_profile_info.ini", "r") as input:
            with open("tools/plant_profile_info.ini", "w+") as f:
                f.write(input.read())


def main():
    """
    main is the main funciton that starts the GUI app by creating
    the GuiDatabaseManager and FarmBeatsApp object.
    """
    try:
        with GuiDatabaseManager() as db:
            root = Tk()
            root.geometry("1200x600")
            root.config(bg=Constants.BACKGROUND.value)
            root.resizable(False, False)
            FarmBeatsApp(root, db)
            root.mainloop()
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
