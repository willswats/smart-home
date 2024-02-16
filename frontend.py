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
        # self.main_frame.grid(padx=10, pady=10)

        self.devices_frame = Frame(self.win)
        self.devices_frame.pack(padx=10, pady=10)

        self.smart_plug_string_vars = []
        self.smart_air_fryer_string_vars = []

        self.home = home

    def run(self):
        self.create_widgets()
        self.win.mainloop()

    def update_string_vars(self, smart_device):
        if isinstance(smart_device, SmartPlug):
            for string_var in self.smart_plug_string_vars:
                string_var.set(
                    f"Smart Plug: {smart_device.get_switched_on()}, Consumption rate: {smart_device.get_consumption_rate()}"
                )
        elif isinstance(smart_device, SmartAirFryer):
            for string_var in self.smart_air_fryer_string_vars:
                string_var.set(
                    f"Smart Air Fryer: {smart_device.get_switched_on()}, Cooking mode: {smart_device.get_cooking_mode()}",
                )

    def button_toggle_switch(self, smart_device):
        smart_device.toggle_switch()
        self.update_string_vars(smart_device)

    def create_widgets_per_device(self):
        smart_devices = self.home.get_devices()
        for smart_device in smart_devices:
            if isinstance(smart_device, SmartPlug):
                label_smart_plug_text = StringVar(
                    self.devices_frame,
                    f"Smart Plug: {smart_device.get_switched_on()}, Consumption rate: {smart_device.get_consumption_rate()}",
                )
                self.smart_plug_string_vars.append(label_smart_plug_text)

                label_smart_plug = Label(
                    self.devices_frame, textvariable=label_smart_plug_text
                )
                label_smart_plug.pack()

                button_toggle = Button(
                    self.devices_frame,
                    text="Toggle",
                    command=lambda smart_device=smart_device: self.button_toggle_switch(
                        smart_device
                    ),
                )
                button_toggle.pack()

            elif isinstance(smart_device, SmartAirFryer):
                label_smart_air_fryer_text = StringVar(
                    self.devices_frame,
                    f"Smart Air Fryer: {smart_device.get_switched_on()}, Cooking mode: {smart_device.get_cooking_mode()}",
                )
                self.smart_air_fryer_string_vars.append(label_smart_air_fryer_text)

                label_smart_air_fryer = Label(
                    self.devices_frame, textvariable=label_smart_air_fryer_text
                )
                label_smart_air_fryer.pack()

    def create_widgets(self):
        # button_turn_on_all = Button(
        #     self.main_frame, text="Turn on all", command=self.home.turn_off_all
        # )
        # button_turn_on_all.grid(column=0, row=0)

        # button_turn_off_all = Button(
        #     self.main_frame, text="Turn off all", command=self.home.turn_off_all
        # )
        # button_turn_off_all.grid(column=2, row=0)

        self.create_widgets_per_device()

        # button_add = Button(self.main_frame, text="Add")
        # button_add.grid(column=0, row=2)


def main():
    home = set_up_home()
    smart_home_system = SmartHomeSystem(home)
    smart_home_system.run()


main()
