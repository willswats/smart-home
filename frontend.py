from enum import Enum
from tkinter import Button, Frame, Label, Tk, StringVar

from backend import SmartAirFryer, SmartHome, SmartPlug


class SmartDeviceNums(Enum):
    SMART_PLUG = "1"
    SMART_AIR_FRYER = "2"


def check_valid_device_num(smart_device_num):
    valid_smart_device_nums = [
        smart_device_num.value for smart_device_num in SmartDeviceNums
    ]
    smart_device_num_clean = smart_device_num.lower().strip()
    if smart_device_num_clean in valid_smart_device_nums:
        return True
    return False


def get_smart_device(smart_device_num):
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


class SmartHomeSystem:
    def __init__(self, home: SmartHome):
        self.win = Tk()
        self.win.resizable(False, False)

        self.main_frame = Frame(self.win)
        self.main_frame.pack(padx=10, pady=10)

        self.home = home
        self.smart_devices = self.home.get_devices()

    def run(self):
        self.create_widgets()
        self.win.mainloop()

    def update_text_label_smart_device(self, smart_device):
        smart_device.set_string_var_text(f"{smart_device}")

    def update_all_text_label_smart_device(self):
        for smart_device in self.smart_devices:
            smart_device.set_string_var_text(f"{smart_device}")

    def button_toggle(self, smart_device):
        smart_device.toggle_switch()
        self.update_text_label_smart_device(smart_device)

    def button_delete(self, smart_device):
        self.smart_devices.remove(smart_device)
        smart_device.delete_gui_objects()

    def button_turn_on_all(self):
        self.home.turn_on_all()
        self.update_all_text_label_smart_device()

    def button_turn_off_all(self):
        self.home.turn_off_all()
        self.update_all_text_label_smart_device()

    def create_widgets_per_device(self):
        for smart_device in self.smart_devices:
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
            button_delete_smart_device = Button(
                self.main_frame,
                text="Delete",
                command=lambda smart_device=smart_device: self.button_delete(
                    smart_device
                ),
            )

            label_smart_device.pack()
            button_toggle_smart_device.pack()
            button_delete_smart_device.pack()

            smart_device.add_gui_objects(
                [
                    label_smart_device,
                    button_toggle_smart_device,
                    button_delete_smart_device,
                ]
            )

    def create_widgets(self):
        button_turn_on_all = Button(
            self.main_frame, text="Turn on all", command=self.button_turn_on_all
        )
        button_turn_on_all.pack()

        button_turn_off_all = Button(
            self.main_frame, text="Turn off all", command=self.button_turn_off_all
        )
        button_turn_off_all.pack()

        self.create_widgets_per_device()

        button_add = Button(self.main_frame, text="Add")
        button_add.pack()


def main():
    home = set_up_home()
    smart_home_system = SmartHomeSystem(home)
    smart_home_system.run()


main()
