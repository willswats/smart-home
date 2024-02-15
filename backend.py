from enum import Enum


class SmartDevice:
    def __init__(self):
        self.switched_on = False

    def get_switched_on(self):
        return self.switched_on

    def toggle_switch(self):
        self.switched_on = not self.switched_on


class SmartPlug(SmartDevice):
    def __init__(self, consumption_rate):
        super().__init__()
        if consumption_rate >= 0 and consumption_rate <= 150:
            self.consumption_rate = consumption_rate
        else:
            raise ValueError("Invalid consumption rate")

    def __str__(self):
        output = "- Smart Plug:\n"
        output += f"  - Switched on: {self.switched_on}\n"
        output += f"  - Consumption rate: {self.consumption_rate}\n"
        return output

    def get_consumption_rate(self):
        return self.consumption_rate

    def set_consumption_rate(self, rate):
        if rate >= 0 and rate <= 150:
            self.consumption_rate = rate
        else:
            raise ValueError("Invalid consumption rate")


def test_smart_plug():
    smart_plug = SmartPlug(150)
    smart_plug.toggle_switch()
    print(smart_plug.get_switched_on())
    print(smart_plug.get_consumption_rate())
    smart_plug.set_consumption_rate(149)
    print(smart_plug.get_consumption_rate())
    print(smart_plug)


# test_smart_plug()


class CookingModes(Enum):
    HEALTHY = "Healthy"
    DEFROST = "Defrost"
    CRISPY = "Crispy"


class SmartAirFryer(SmartDevice):
    def __init__(self):
        super().__init__()
        self.cooking_mode = CookingModes.HEALTHY.value

    def __str__(self):
        output = "- Smart Air Fryer:\n"
        output += f"  - Switched on: {self.switched_on}\n"
        output += f"  - Cooking mode: {self.cooking_mode}\n"
        return output

    def get_cooking_mode(self):
        return self.cooking_mode

    def set_cooking_mode(self, cooking_mode):
        if isinstance(cooking_mode, CookingModes):
            self.cooking_mode = cooking_mode.value
        else:
            raise ValueError("Invalid cooking mode")


def test_smart_air_fryer():
    smart_air_fryer = SmartAirFryer()
    smart_air_fryer.toggle_switch()
    print(smart_air_fryer.get_switched_on())
    print(smart_air_fryer.get_cooking_mode())
    smart_air_fryer.set_cooking_mode(CookingModes.DEFROST)
    print(smart_air_fryer.get_cooking_mode())
    print(smart_air_fryer)


# test_smart_air_fryer()


class SmartHome:
    def __init__(self):
        self.devices = []

    def __str__(self):
        output = "Smart Home Devices:\n"
        for device in self.devices:
            output += f"{device}"
        return output

    def get_devices(self):
        return self.devices

    def get_device_at(self, index):
        return self.devices[index]

    def add_device(self, device):
        if isinstance(device, SmartDevice):
            self.devices.append(device)
        else:
            raise ValueError("Invalid device")

    def toggle_switch(self, index):
        self.devices[index].toggle_switch()

    def turn_on_all(self):
        for device in self.devices:
            if device.get_switched_on() is False:
                device.toggle_switch()

    def turn_off_all(self):
        for device in self.devices:
            if device.get_switched_on() is True:
                device.toggle_switch()


def test_smart_home():
    smart_home = SmartHome()
    smart_plug_1 = SmartPlug(45)
    smart_plug_2 = SmartPlug(45)
    smart_air_fryer = SmartAirFryer()
    smart_plug_1.toggle_switch()
    smart_plug_1.set_consumption_rate(150)
    smart_plug_2.set_consumption_rate(25)
    smart_air_fryer.set_cooking_mode(CookingModes.CRISPY)
    smart_home.add_device(smart_plug_1)
    smart_home.add_device(smart_plug_2)
    smart_home.add_device(smart_air_fryer)
    smart_home.toggle_switch(1)
    print(smart_home)


test_smart_home()
