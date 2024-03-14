from enum import Enum
from typing import List, Self


class SmartDevice:
    def __init__(self: Self) -> None:
        self.switched_on: bool = False

    def get_switched_on(self: Self) -> bool:
        return self.switched_on

    def toggle_switch(self: Self) -> None:
        self.switched_on = not self.switched_on


class SmartPlug(SmartDevice):
    def __init__(self: Self, consumption_rate: int) -> None:
        super().__init__()
        self.error_message: str = "invalid consumption rate (>= 0 and <= 150)."
        self.consumption_rate: int = 150
        self.set_consumption_rate(consumption_rate)

    def __str__(self: Self) -> str:
        output = f"Smart Plug: {'On' if self.switched_on is True else 'Off'}, "
        output += f"Consumption rate: {self.consumption_rate}"
        return output

    def get_consumption_rate(self: Self) -> int:
        return self.consumption_rate

    def set_consumption_rate(self: Self, rate: int) -> None:
        if rate >= 0 and rate <= 150:
            self.consumption_rate = rate
        else:
            raise ValueError(self.error_message)


def test_smart_plug() -> None:
    smart_plug: SmartPlug = SmartPlug(45)
    smart_plug.toggle_switch()
    print(smart_plug.get_switched_on())
    print(smart_plug.get_consumption_rate())
    smart_plug.set_consumption_rate(149)
    print(smart_plug.get_consumption_rate())
    print(smart_plug)


test_smart_plug()


class CookingModes(Enum):
    HEALTHY = "Healthy"
    DEFROST = "Defrost"
    CRISPY = "Crispy"


class SmartAirFryer(SmartDevice):
    def __init__(self: Self) -> None:
        super().__init__()
        self.cooking_mode: str = CookingModes.HEALTHY.value

    def __str__(self: Self) -> str:
        output = (
            f"Smart Air Fryer: {'On' if self.switched_on is True else 'Off'}, "
        )
        output += f"Cooking mode: {self.cooking_mode}"
        return output

    def get_cooking_mode(self: Self) -> str:
        return self.cooking_mode

    def set_cooking_mode(self: Self, cooking_mode: str) -> None:
        cooking_modes: List[str] = [
            cooking_mode.value for cooking_mode in CookingModes
        ]
        if cooking_mode in cooking_modes:
            self.cooking_mode = cooking_mode
        else:
            raise ValueError("invalid cooking mode.")


def test_smart_air_fryer() -> None:
    smart_air_fryer: SmartAirFryer = SmartAirFryer()
    smart_air_fryer.toggle_switch()
    print(smart_air_fryer.get_switched_on())
    print(smart_air_fryer.get_cooking_mode())
    smart_air_fryer.set_cooking_mode(CookingModes.DEFROST.value)
    print(smart_air_fryer.get_cooking_mode())
    print(smart_air_fryer)


test_smart_air_fryer()


class SmartHome:
    def __init__(self: Self) -> None:
        self.devices: List[SmartDevice] = []
        self.switch_all_state: bool = False

    def __str__(self: Self) -> str:
        output = "Smart Home Devices:"
        for device in self.devices:
            output += f"\n  - {device}"
        return output

    def get_devices(self: Self) -> List[SmartDevice]:
        return self.devices

    def get_device_at(self: Self, index: int) -> SmartDevice | None:
        if index < len(self.devices):
            return self.devices[index]

    def get_switch_all_state(self: Self) -> bool:
        return self.switch_all_state

    def remove_device_at(self: Self, index: int) -> SmartDevice | None:
        if index < len(self.devices):
            return self.devices.remove(self.devices[index])

    def add_device(self: Self, device: SmartDevice) -> None:
        if isinstance(device, SmartDevice):
            self.devices.append(device)
        else:
            raise ValueError("invalid device.")

    def toggle_switch(self: Self, index: int) -> None:
        if index < len(self.devices):
            self.devices[index].toggle_switch()

    def turn_on_all(self: Self) -> None:
        for device in self.devices:
            if device.get_switched_on() is False:
                device.toggle_switch()

    def turn_off_all(self: Self) -> None:
        for device in self.devices:
            if device.get_switched_on() is True:
                device.toggle_switch()

    def toggle_switch_all(self: Self) -> None:
        if self.switch_all_state is False:
            self.switch_all_state = True
            self.turn_on_all()
        elif self.switch_all_state is True:
            self.switch_all_state = False
            self.turn_off_all()

    def delete_all_devices(self: Self) -> None:
        self.devices = []


def test_smart_home() -> None:
    smart_home: SmartHome = SmartHome()
    smart_plug_1: SmartPlug = SmartPlug(45)
    smart_plug_2: SmartPlug = SmartPlug(45)
    smart_air_fryer: SmartAirFryer = SmartAirFryer()
    smart_plug_1.toggle_switch()
    smart_plug_1.set_consumption_rate(150)
    smart_plug_2.set_consumption_rate(25)
    smart_air_fryer.set_cooking_mode(CookingModes.CRISPY.value)
    smart_home.add_device(smart_plug_1)
    smart_home.add_device(smart_plug_2)
    smart_home.add_device(smart_air_fryer)
    smart_home.toggle_switch(2)
    print(smart_home)
    smart_home.turn_on_all()
    print(smart_home)
    smart_home.remove_device_at(0)
    print(smart_home)


test_smart_home()
