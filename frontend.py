from backend import CookingModes, SmartAirFryer, SmartHome, SmartPlug


def check_valid_device_num(device_num):
    valid_device_nums = ["1", "2"]
    device_num_clean = device_num.lower().strip()
    if device_num_clean in valid_device_nums:
        return True
    return False


def get_smart_devices():
    device_nums = []
    print("Add 5 devices to your smart home:")
    print("  1. Smart Plug")
    print("  2. Smart Air Fryer")
    while len(device_nums) < 5:
        device_num = input("Enter device number: ")
        if check_valid_device_num(device_num):
            print("Added device.")
            device_nums.append(device_num)
        else:
            print("Invalid device number.")
    return device_nums


def set_up_home():
    smart_home = SmartHome()
    print(get_smart_devices())


class SmartHomeSystem:
    pass


def main():
    set_up_home()


main()
