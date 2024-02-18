from enum import Enum
from tkinter import (
    Button,
    Entry,
    Frame,
    Label,
    OptionMenu,
    StringVar,
    Tk,
    Toplevel,
)

from backend import (
    CookingModes,
    SmartAirFryer,
    SmartDevice,
    SmartHome,
    SmartPlug,
)


class SmartDeviceNums(Enum):
    SMART_PLUG = "1"
    SMART_AIR_FRYER = "2"


def check_valid_device_num(smart_device_num: str):
    valid_smart_device_nums = [
        smart_device_num.value for smart_device_num in SmartDeviceNums
    ]
    smart_device_num_clean = smart_device_num.lower().strip()
    if smart_device_num_clean in valid_smart_device_nums:
        return True
    return False


def get_smart_device(smart_device_num: str):
    match smart_device_num:
        case SmartDeviceNums.SMART_PLUG.value:
            while True:
                try:
                    consumption_rate = int(input("Enter consumption rate:"))
                    smart_plug = SmartPlug(consumption_rate)
                    print("Added Smart Plug.")
                    return smart_plug
                except ValueError as error:
                    print("Error:", error)
        case SmartDeviceNums.SMART_AIR_FRYER.value:
            smart_air_fryer = SmartAirFryer()
            print("Added Smart Air Fryer.")
            return smart_air_fryer


def get_smart_devices():
    smart_devices = []
    print("Add 5 smart devices to your smart home:")
    print(f"  {SmartDeviceNums.SMART_PLUG.value}. Smart Plug")
    print(f"  {SmartDeviceNums.SMART_AIR_FRYER.value}. Smart Air Fryer")
    while len(smart_devices) < 5:
        smart_device_num = input("Enter smart device number: ")
        if check_valid_device_num(smart_device_num):
            smart_device = get_smart_device(smart_device_num)
            smart_devices.append(smart_device)
        else:
            print("Error: Invalid smart device number.")
    return smart_devices


def set_up_home():
    smart_home = SmartHome()
    smart_devices = get_smart_devices()
    for smart_device in smart_devices:
        smart_home.add_device(smart_device)
    return smart_home


class SmartHomeSystemUtilities:
    @staticmethod
    def set_smart_plug(
        smart_plug: SmartPlug,
        text_options_menu_switched_on: StringVar,
        text_entry_consumption_rate: StringVar,
    ):
        # TODO: error check and provide feedback to user (try, except)
        switched_on = (
            True if text_options_menu_switched_on.get() == "On" else False
        )
        if switched_on != smart_plug.get_switched_on():
            smart_plug.toggle_switch()

        text_consumption_rate = text_entry_consumption_rate.get()
        smart_plug.set_consumption_rate(int(text_consumption_rate))

    @staticmethod
    def set_smart_air_fryer(
        smart_air_fryer: SmartAirFryer,
        text_options_menu_switched_on: StringVar,
        text_options_menu_cooking_mode: StringVar,
    ):
        switched_on = (
            True if text_options_menu_switched_on.get() == "On" else False
        )
        if switched_on != smart_air_fryer.get_switched_on():
            smart_air_fryer.toggle_switch()

        text_cooking_mode = text_options_menu_cooking_mode.get()
        smart_air_fryer.set_cooking_mode(text_cooking_mode)

    @staticmethod
    def add_edit_create_widgets_smart_device(
        frame: Frame, smart_device: SmartDevice
    ) -> tuple[StringVar, list[Label | OptionMenu]]:
        label_switched_on = Label(frame, text="Switched on: ")

        switched_on_options = ["On", "Off"]
        text_options_menu_switched_on = StringVar(
            frame,
            f"{'On' if smart_device.get_switched_on() else 'Off'}",
        )
        options_menu_switched_on = OptionMenu(
            frame,
            text_options_menu_switched_on,
            *switched_on_options,
        )

        label_switched_on.pack()
        options_menu_switched_on.pack()

        return (
            text_options_menu_switched_on,
            [label_switched_on, options_menu_switched_on],
        )

    @staticmethod
    def add_edit_create_widgets_smart_plug(
        frame: Frame, smart_plug: SmartPlug
    ) -> tuple[StringVar, list[Label | Entry]]:
        label_consumption_rate = Label(frame, text="Consumption rate: ")

        text_entry_consumption_rate = StringVar(
            frame,
            f"{smart_plug.get_consumption_rate()}",
        )
        entry_consumption_rate = Entry(
            frame, textvariable=text_entry_consumption_rate
        )

        label_consumption_rate.pack()
        entry_consumption_rate.pack()

        return (
            text_entry_consumption_rate,
            [label_consumption_rate, entry_consumption_rate],
        )

    @staticmethod
    def add_edit_create_widgets_smart_air_fryer(
        frame: Frame, smart_air_fryer: SmartAirFryer
    ) -> tuple[StringVar, list[Label | OptionMenu]]:
        label_cooking_modes = Label(frame, text="Cooking modes: ")

        cooking_mode_options = [
            cooking_mode.value for cooking_mode in CookingModes
        ]
        text_options_menu_cooking_mode = StringVar(
            frame,
            f"{smart_air_fryer.get_cooking_mode()}",
        )
        options_menu_cooking_mode = OptionMenu(
            frame,
            text_options_menu_cooking_mode,
            *cooking_mode_options,
        )

        label_cooking_modes.pack()
        options_menu_cooking_mode.pack()

        return (
            text_options_menu_cooking_mode,
            [label_cooking_modes, options_menu_cooking_mode],
        )


class SmartHomeSystem:
    def __init__(self, home: SmartHome):
        self.win = Tk()
        self.win.title("Smart Home System")
        self.win.resizable(False, False)

        self.main_frame = Frame(self.win)
        self.main_frame.pack(padx=10, pady=10)

        self.home = home
        self.smart_devices = self.home.get_devices()

    def run(self):
        self.create_widgets()
        self.win.mainloop()

    # Update methods
    def update_text_label_smart_device(self, smart_device: SmartDevice):
        smart_device.set_string_var_text(f"{smart_device}")

    def update_all_text_label_smart_device(self):
        for smart_device in self.smart_devices:
            smart_device.set_string_var_text(f"{smart_device}")

    # Button methods
    def button_toggle(self, smart_device: SmartDevice):
        smart_device.toggle_switch()
        self.update_text_label_smart_device(smart_device)

    def button_delete(self, smart_device: SmartDevice):
        self.smart_devices.remove(smart_device)
        smart_device.delete_gui_objects()

    def button_turn_on_all(self):
        self.home.turn_on_all()
        self.update_all_text_label_smart_device()

    def button_turn_off_all(self):
        self.home.turn_off_all()
        self.update_all_text_label_smart_device()

    def button_edit(self, smart_device: SmartDevice):
        smart_home_system_edit = SmartHomeSystemEdit(self.win)
        smart_home_system_edit.edit_create_widgets(smart_device)

    def button_add(self):
        smart_home_system_add = SmartHomeSystemAdd(
            self.win, self.home, self.main_frame
        )
        smart_home_system_add.add_create_widgets()

    # Create widgets methods
    def create_widgets_smart_device(self, smart_device: SmartDevice):
        text_label_smart_device = StringVar(self.main_frame, f"{smart_device}")
        smart_device.set_string_var(text_label_smart_device)

        label_smart_device = Label(
            self.main_frame, textvariable=text_label_smart_device
        )
        button_toggle_smart_device = Button(
            self.main_frame,
            text="Toggle",
            command=lambda smart_device=smart_device: self.button_toggle(
                smart_device
            ),
        )
        button_edit_smart_device = Button(
            self.main_frame,
            text="Edit",
            command=lambda smart_device=smart_device: self.button_edit(
                smart_device
            ),
        )
        button_delete_smart_device = Button(
            self.main_frame,
            text="Delete",
            command=lambda smart_device=smart_device: self.button_delete(
                smart_device
            ),
        )

        label_smart_device.pack()
        button_toggle_smart_device.pack()
        button_edit_smart_device.pack()
        button_delete_smart_device.pack()

        smart_device.add_gui_objects(
            [
                label_smart_device,
                button_toggle_smart_device,
                button_edit_smart_device,
                button_delete_smart_device,
            ]
        )

    def create_widgets(self):
        button_turn_on_all = Button(
            self.main_frame,
            text="Turn on all",
            command=self.button_turn_on_all,
        )
        button_turn_on_all.pack()

        button_turn_off_all = Button(
            self.main_frame,
            text="Turn off all",
            command=self.button_turn_off_all,
        )
        button_turn_off_all.pack()

        for smart_device in self.smart_devices:
            self.create_widgets_smart_device(smart_device)

        button_add = Button(
            self.main_frame, text="Add", command=self.button_add
        )
        button_add.pack()


class SmartHomeSystemEdit(SmartHomeSystem):
    def __init__(self, win):
        self.edit_window = Toplevel(win)
        self.edit_window.title("Edit")
        self.edit_window.resizable(False, False)

        self.edit_window_frame = Frame(self.edit_window)
        self.edit_window_frame.pack(padx=10, pady=10)

    # Button methods
    def edit_button_submit_smart_plug(
        self,
        smart_plug: SmartPlug,
        text_options_menu_switched_on: StringVar,
        text_entry_consumption_rate: StringVar,
    ):
        SmartHomeSystemUtilities.set_smart_plug(
            smart_plug,
            text_options_menu_switched_on,
            text_entry_consumption_rate,
        )
        self.update_text_label_smart_device(smart_plug)

    def edit_button_submit_smart_air_fryer(
        self,
        smart_air_fryer: SmartAirFryer,
        text_options_menu_switched_on: StringVar,
        text_options_menu_cooking_mode: StringVar,
    ):
        SmartHomeSystemUtilities.set_smart_air_fryer(
            smart_air_fryer,
            text_options_menu_switched_on,
            text_options_menu_cooking_mode,
        )
        self.update_text_label_smart_device(smart_air_fryer)

    # Create widgets methods
    def edit_create_widgets(self, smart_device: SmartDevice):
        text_options_menu_switched_on = (
            SmartHomeSystemUtilities.add_edit_create_widgets_smart_device(
                self.edit_window_frame, smart_device
            )[0]
        )

        if isinstance(smart_device, SmartPlug):
            text_entry_consumption_rate = (
                SmartHomeSystemUtilities.add_edit_create_widgets_smart_plug(
                    self.edit_window_frame, smart_device
                )[0]
            )
            edit_button_submit = Button(
                self.edit_window_frame,
                text="Submit",
                command=lambda: self.edit_button_submit_smart_plug(
                    smart_device,
                    text_options_menu_switched_on,
                    text_entry_consumption_rate,
                ),
            )
            edit_button_submit.pack()
        elif isinstance(smart_device, SmartAirFryer):
            text_options_menu_cooking_mode = (
                SmartHomeSystemUtilities.add_edit_create_widgets_smart_air_fryer(
                    self.edit_window_frame, smart_device
                )
            )[0]
            edit_button_submit = Button(
                self.edit_window_frame,
                text="Submit",
                command=lambda: self.edit_button_submit_smart_air_fryer(
                    smart_device,
                    text_options_menu_switched_on,
                    text_options_menu_cooking_mode,
                ),
            )
            edit_button_submit.pack()


class SmartHomeSystemAdd(SmartHomeSystem):
    def __init__(self, win: Tk, home: SmartHome, main_frame: Frame):
        self.win = win
        self.home = home
        self.smart_devices = self.home.get_devices()
        self.main_frame = main_frame

        self.add_window = Toplevel(win)
        self.add_window.title("Add")
        self.add_window.resizable(False, False)
        self.add_window.geometry("200x250")

        self.add_window_frame = Frame(self.add_window)
        self.add_window_frame.pack(padx=10, pady=10)

        self.selected_smart_device = "Smart Plug"
        self.gui_objects = []

    def add_gui_objects(self, gui_objects):
        for gui_object in gui_objects:
            self.gui_objects.append(gui_object)

    def delete_gui_objects(self):
        if len(self.gui_objects) > 0:
            for gui_object in self.gui_objects:
                gui_object.destroy()

    def add_options_menu_submit(self, selected_smart_device: StringVar | str):
        self.delete_gui_objects()

        # The selected_smart_device can be StringVar | str as the command for
        # the OptionsMenu seems to call get() on it automatically,
        # however, it is still passed in as a StringVar
        selected_smart_device = (
            selected_smart_device.get()
            if isinstance(selected_smart_device, StringVar)
            else selected_smart_device
        )

        match selected_smart_device:
            case "Smart Plug":
                smart_plug = SmartPlug(150)
                (
                    text_options_menu_switched_on,
                    gui_objects_smart_device,
                ) = SmartHomeSystemUtilities.add_edit_create_widgets_smart_device(  # noqa: E501
                    self.add_window_frame, smart_plug
                )
                (
                    text_entry_consumption_rate,
                    gui_objects_smart_plug,
                ) = SmartHomeSystemUtilities.add_edit_create_widgets_smart_plug(  # noqa: E501
                    self.add_window_frame, smart_plug
                )
                button_add_submit_smart_plug = Button(
                    self.add_window_frame,
                    text="Submit",
                    command=lambda: self.add_button_submit_smart_plug(
                        smart_plug,
                        text_options_menu_switched_on,
                        text_entry_consumption_rate,
                    ),
                )
                button_add_submit_smart_plug.pack()

                self.add_gui_objects(
                    [
                        *gui_objects_smart_device,
                        *gui_objects_smart_plug,
                        button_add_submit_smart_plug,
                    ]
                )

            case "Smart Air Fryer":
                smart_air_fryer = SmartAirFryer()
                (
                    text_options_menu_switched_on,
                    gui_objects_smart_device,
                ) = SmartHomeSystemUtilities.add_edit_create_widgets_smart_device(  # noqa: E501
                    self.add_window_frame, smart_air_fryer
                )

                (
                    text_options_menu_cooking_mode,
                    gui_objects_smart_air_fryer,
                ) = SmartHomeSystemUtilities.add_edit_create_widgets_smart_air_fryer(  # noqa: E501
                    self.add_window_frame, smart_air_fryer
                )
                button_add_submit_smart_air_fryer = Button(
                    self.add_window_frame,
                    text="Submit",
                    command=lambda: self.add_button_submit_smart_air_fryer(
                        smart_air_fryer,
                        text_options_menu_switched_on,
                        text_options_menu_cooking_mode,
                    ),
                )
                button_add_submit_smart_air_fryer.pack()

                self.add_gui_objects(
                    [
                        *gui_objects_smart_device,
                        *gui_objects_smart_air_fryer,
                        button_add_submit_smart_air_fryer,
                    ]
                )

    # Button methods
    def add_button_submit_smart_plug(
        self,
        smart_plug: SmartPlug,
        text_options_menu_switched_on: StringVar,
        text_entry_consumption_rate: StringVar,
    ):
        SmartHomeSystemUtilities.set_smart_plug(
            smart_plug,
            text_options_menu_switched_on,
            text_entry_consumption_rate,
        )

        self.home.add_device(smart_plug)
        self.create_widgets_smart_device(smart_plug)
        # Save the last selected smart device
        self.selected_smart_device = "Smart Plug"
        # Call the options menu again so that a new SmartPlug object is
        # created each time
        self.add_options_menu_submit(
            StringVar(self.add_window_frame, self.selected_smart_device)
        )

    def add_button_submit_smart_air_fryer(
        self,
        smart_air_fryer: SmartAirFryer,
        text_options_menu_switched_on: StringVar,
        text_options_menu_cooking_mode: StringVar,
    ):
        SmartHomeSystemUtilities.set_smart_air_fryer(
            smart_air_fryer,
            text_options_menu_switched_on,
            text_options_menu_cooking_mode,
        )

        self.home.add_device(smart_air_fryer)
        self.create_widgets_smart_device(smart_air_fryer)
        # Save the last selected smart device
        self.selected_smart_device = "Smart Air Fryer"
        # Call the options menu again so that a new SmartAirFryer object is
        # created each time
        self.add_options_menu_submit(
            StringVar(self.add_window_frame, self.selected_smart_device)
        )

    # Create widgets methods
    def add_create_widgets(self):
        label_pick_smart_device = Label(
            self.add_window_frame, text="Pick device: "
        )

        pick_smart_device_options = ["Smart Plug", "Smart Air Fryer"]
        text_options_menu_pick_smart_device = StringVar(
            self.add_window_frame,
            "Select a device",
        )
        options_menu_pick_smart_device = OptionMenu(
            self.add_window_frame,
            text_options_menu_pick_smart_device,
            *pick_smart_device_options,
            command=lambda selected_smart_device: self.add_options_menu_submit(
                selected_smart_device
            ),
        )

        label_pick_smart_device.pack()
        options_menu_pick_smart_device.pack()


def main():
    home = set_up_home()
    smart_home_system = SmartHomeSystem(home)
    smart_home_system.run()


main()
