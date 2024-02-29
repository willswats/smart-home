from enum import Enum
from tkinter import (
    LEFT,
    RIGHT,
    BooleanVar,
    Button,
    Checkbutton,
    E,
    Frame,
    Label,
    OptionMenu,
    PhotoImage,
    Spinbox,
    StringVar,
    Tk,
    Toplevel,
    W,
)
from typing import Dict

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
            print("Error: invalid smart device number.")
    return smart_devices


def set_up_home():
    smart_home = SmartHome()
    smart_devices = get_smart_devices()
    for smart_device in smart_devices:
        smart_home.add_device(smart_device)
    return smart_home


class Utilities:
    @staticmethod
    def create_checkbox_smart_device_switched_on(
        frame: Frame, smart_device: SmartDevice
    ):
        bool_checkbutton_switched_on = BooleanVar(
            frame, smart_device.get_switched_on()
        )
        checkbutton_switched_on = Checkbutton(
            frame,
            variable=bool_checkbutton_switched_on,
            onvalue=True,
            offvalue=False,
            command=lambda: Utilities.set_smart_device_switched_on(
                smart_device, bool_checkbutton_switched_on
            ),
        )

        return bool_checkbutton_switched_on, checkbutton_switched_on

    @staticmethod
    def create_spinbox_smart_plug_consumption_rate(
        frame: Frame, smart_plug: SmartPlug
    ):
        text_spinbox_consumption_rate = StringVar(
            frame,
            f"{smart_plug.get_consumption_rate()}",
        )
        spinbox_consumption_rate = Spinbox(
            frame,
            textvariable=text_spinbox_consumption_rate,
            from_=0,
            to=150,
            width=9,
            command=lambda: Utilities.set_smart_plug_consumption_rate(
                smart_plug, text_spinbox_consumption_rate
            ),
        )
        # Spinbox command is only executed when arrows are pressed, this
        # creates a way to submit upon pressing return
        spinbox_consumption_rate.bind(
            "<Return>",
            lambda _: Utilities.set_smart_plug_consumption_rate_validate(
                smart_plug, text_spinbox_consumption_rate
            ),
        )

        return text_spinbox_consumption_rate, spinbox_consumption_rate

    @staticmethod
    def create_option_menu_smart_air_fryer_cooking_mode(
        frame: Frame, smart_air_fryer: SmartAirFryer
    ):
        cooking_mode_options = [
            cooking_mode.value for cooking_mode in CookingModes
        ]

        text_option_menu_cooking_mode = StringVar(
            frame,
            f"{smart_air_fryer.get_cooking_mode()}",
        )
        option_menu_cooking_mode = OptionMenu(
            frame,
            text_option_menu_cooking_mode,
            *cooking_mode_options,
            command=lambda _: Utilities.set_smart_air_fryer_cooking_mode(
                smart_air_fryer, text_option_menu_cooking_mode
            ),
        )
        return text_option_menu_cooking_mode, option_menu_cooking_mode

    @staticmethod
    def set_smart_device_switched_on(
        smart_plug: SmartDevice,
        bool_checkbutton_switched_on: BooleanVar,
    ):
        switched_on = bool_checkbutton_switched_on.get()
        if switched_on != smart_plug.get_switched_on():
            smart_plug.toggle_switch()

    @staticmethod
    def set_smart_plug_consumption_rate(
        smart_plug: SmartPlug,
        text_spinbox_consumption_rate: StringVar,
    ):
        text_consumption_rate = text_spinbox_consumption_rate.get()
        try:
            smart_plug.set_consumption_rate(int(text_consumption_rate))
        except Exception as error:
            raise error

    # This is needed for the Spinbox bind on return, because
    # I am raising an error in set_smart_plug_consumption_rate to ensure
    # that a device is not added, even when the validation fails
    # (by using try except later on in the code)
    @staticmethod
    def set_smart_plug_consumption_rate_validate(
        smart_plug: SmartPlug,
        text_spinbox_consumption_rate: StringVar,
    ):
        try:
            Utilities.set_smart_plug_consumption_rate(
                smart_plug, text_spinbox_consumption_rate
            )
        except Exception as error:
            print("Error", error)

    @staticmethod
    def set_smart_air_fryer_cooking_mode(
        smart_air_fryer: SmartAirFryer,
        text_option_menu_cooking_mode: StringVar,
    ):
        text_cooking_mode = text_option_menu_cooking_mode.get()
        smart_air_fryer.set_cooking_mode(text_cooking_mode)

    @staticmethod
    def set_smart_plug(
        smart_plug: SmartPlug,
        bool_checkbutton_switched_on: BooleanVar,
        text_spinbox_consumption_rate: StringVar,
    ):
        Utilities.set_smart_device_switched_on(
            smart_plug, bool_checkbutton_switched_on
        )
        Utilities.set_smart_plug_consumption_rate(
            smart_plug, text_spinbox_consumption_rate
        )

    @staticmethod
    def set_smart_air_fryer(
        smart_air_fryer: SmartAirFryer,
        bool_checkbutton_switched_on: BooleanVar,
        text_option_menu_cooking_mode: StringVar,
    ):
        Utilities.set_smart_device_switched_on(
            smart_air_fryer, bool_checkbutton_switched_on
        )
        Utilities.set_smart_air_fryer_cooking_mode(
            smart_air_fryer, text_option_menu_cooking_mode
        )

    @staticmethod
    def add_edit_create_widgets_smart_device(
        frame: Frame, smart_device: SmartDevice
    ) -> tuple[BooleanVar, list[Frame | Label | Checkbutton]]:
        frame_switched_on = Frame(frame)

        label_switched_on = Label(
            frame_switched_on,
            text="Switched on: ",
            font=("sans-serif", 10),
        )

        (
            bool_checkbutton_switched_on,
            checkbutton_switched_on,
        ) = Utilities.create_checkbox_smart_device_switched_on(
            frame_switched_on, smart_device
        )

        label_switched_on.pack(side=LEFT, anchor=W)
        checkbutton_switched_on.pack(side=RIGHT, anchor=W)
        frame_switched_on.pack(fill="both")

        return (
            bool_checkbutton_switched_on,
            [
                frame_switched_on,
                label_switched_on,
                checkbutton_switched_on,
            ],
        )

    @staticmethod
    def add_edit_create_widgets_smart_plug(
        frame: Frame, smart_plug: SmartPlug
    ) -> tuple[StringVar, list[Frame | Label | Spinbox]]:
        frame_consumption_rate = Frame(frame)

        label_consumption_rate = Label(
            frame_consumption_rate,
            text="Consumption rate: ",
            font=("sans-serif", 10),
        )

        (
            text_spinbox_consumption_rate,
            spinbox_consumption_rate,
        ) = Utilities.create_spinbox_smart_plug_consumption_rate(
            frame_consumption_rate, smart_plug
        )

        label_consumption_rate.pack(side=LEFT, anchor=W)
        spinbox_consumption_rate.pack(side=RIGHT, anchor=E)
        frame_consumption_rate.pack(fill="both")

        return (
            text_spinbox_consumption_rate,
            [
                frame_consumption_rate,
                label_consumption_rate,
                spinbox_consumption_rate,
            ],
        )

    @staticmethod
    def add_edit_create_widgets_smart_air_fryer(
        frame: Frame, smart_air_fryer: SmartAirFryer
    ) -> tuple[StringVar, list[Frame | Label | OptionMenu]]:
        frame_cooking_mode = Frame(frame)

        label_cooking_modes = Label(
            frame_cooking_mode,
            text="Cooking modes: ",
            font=("sans-serif", 10),
        )

        (
            text_option_menu_cooking_mode,
            option_menu_cooking_mode,
        ) = Utilities.create_option_menu_smart_air_fryer_cooking_mode(
            frame_cooking_mode, smart_air_fryer
        )

        label_cooking_modes.pack(side=LEFT, anchor=W)
        option_menu_cooking_mode.pack(side=RIGHT, anchor=E)
        frame_cooking_mode.pack(fill="both")

        return (
            text_option_menu_cooking_mode,
            [
                frame_cooking_mode,
                label_cooking_modes,
                option_menu_cooking_mode,
            ],
        )


class SmartHomeSystem:
    def __init__(self, home: SmartHome):
        self.win = Tk()
        self.win.title("Smart Home System")
        self.win.resizable(False, False)

        self.main_frame = Frame(self.win)
        self.main_frame.pack(padx=10, pady=10)

        self.smart_device_frames = Frame(self.main_frame)

        self.home = home
        self.smart_devices = self.home.get_devices()

        self.images = {
            "smart_plug_image": PhotoImage(file="./assets/plug.png"),
            "smart_air_fryer_image": PhotoImage(file="./assets/pot.png"),
            "toggle_button_image": PhotoImage(file="./assets/toggle.png"),
            "edit_button_image": PhotoImage(file="./assets/edit.png"),
            "delete_button_image": PhotoImage(file="./assets/delete.png"),
            "add_button_image": PhotoImage(file="./assets/add.png"),
            "submit_button_image": PhotoImage(file="./assets/check.png"),
            "toggle_all_button_off": PhotoImage(
                file="./assets/toggle-off.png"
            ),
            "toggle_all_button_on": PhotoImage(file="./assets/toggle-on.png"),
        }

    def run(self):
        for image in self.images:
            self.images[image] = self.images[image].subsample(8, 8)
        self.create_widgets()
        self.win.mainloop()

    # Update methods
    def update_smart_device(self, smart_device: SmartDevice):
        smart_device.set_bool_var_value(smart_device.get_switched_on())
        if isinstance(smart_device, SmartPlug):
            smart_device.set_string_var_value(
                smart_device.get_consumption_rate()
            )
        elif isinstance(smart_device, SmartAirFryer):
            smart_device.set_string_var_value(smart_device.get_cooking_mode())

    def update_all_smart_device(self):
        for smart_device in self.smart_devices:
            self.update_smart_device(smart_device)

    # Button methods
    def button_toggle(self, smart_device: SmartDevice):
        smart_device.toggle_switch()
        self.update_smart_device(smart_device)

    def button_delete(self, smart_device: SmartDevice):
        smart_device_index = self.smart_devices.index(smart_device)
        self.home.remove_device_at(smart_device_index)
        smart_device.delete_gui_objects()

    def button_toggle_all(self, button_toggle_all):
        self.home.toggle_switch_all()
        self.update_all_smart_device()

        if self.home.get_switch_all_state() is False:
            button_toggle_all.config(
                image=self.images["toggle_all_button_off"]
            )
        elif self.home.get_switch_all_state() is True:
            button_toggle_all.config(image=self.images["toggle_all_button_on"])

    def button_edit(self, smart_device: SmartDevice):
        smart_home_system_edit = SmartHomeSystemEdit(self.win, self.images)
        smart_home_system_edit.edit_create_widgets(smart_device)

    def button_add(self):
        smart_home_system_add = SmartHomeSystemAdd(
            self.win,
            self.home,
            self.main_frame,
            self.smart_device_frames,
            self.images,
        )
        smart_home_system_add.add_create_widgets()

    # Create widgets methods
    def create_widgets_buttons_smart_device(
        self, frame: Frame, smart_device: SmartDevice
    ):
        button_toggle_smart_device = Button(
            frame,
            text="Toggle",
            image=self.images["toggle_button_image"],
            command=lambda smart_device=smart_device: self.button_toggle(
                smart_device
            ),
        )
        button_edit_smart_device = Button(
            frame,
            text="Edit",
            image=self.images["edit_button_image"],
            command=lambda smart_device=smart_device: self.button_edit(
                smart_device
            ),
        )
        button_delete_smart_device = Button(
            frame,
            text="Delete",
            image=self.images["delete_button_image"],
            command=lambda smart_device=smart_device: self.button_delete(
                smart_device
            ),
        )

        button_delete_smart_device.pack(side=RIGHT, anchor=E, padx=5)
        button_edit_smart_device.pack(side=RIGHT, anchor=E)
        button_toggle_smart_device.pack(side=RIGHT, anchor=E, padx=5)

        return (
            button_toggle_smart_device,
            button_edit_smart_device,
            button_delete_smart_device,
        )

    def create_widgets_smart_device(
        self,
        smart_device: SmartDevice,
        smart_device_image: PhotoImage,
        smart_device_text_title: str,
    ):
        smart_device_frame = Frame(self.smart_device_frames)

        label_smart_device_image = Label(
            smart_device_frame, image=smart_device_image
        )
        label_smart_device_title = Label(
            smart_device_frame,
            text=smart_device_text_title,
            font=("sans-serif", 12, "bold"),
        )

        label_smart_device_switched_on = Label(
            smart_device_frame,
            text="Switched on:",
            font=("sans-serif", 10),
        )
        (
            bool_checkbutton_switched_on,
            checkbutton_switched_on,
        ) = Utilities.create_checkbox_smart_device_switched_on(
            smart_device_frame, smart_device
        )
        smart_device.set_bool_var(bool_checkbutton_switched_on)

        label_smart_device_image.pack(side=LEFT, anchor=W)
        label_smart_device_title.pack(side=LEFT, anchor=W)

        if isinstance(smart_device, SmartPlug):
            label_smart_device_switched_on.pack(
                side=LEFT, anchor=W, padx=(40, 0)
            )
            checkbutton_switched_on.pack(side=LEFT, anchor=W)
            label_smart_plug_consumption_rate = Label(
                smart_device_frame,
                text="Consumption rate:",
                font=("sans-serif", 10),
            )
            (
                text_spinbox_consumption_rate,
                spinbox_consumption_rate,
            ) = Utilities.create_spinbox_smart_plug_consumption_rate(
                smart_device_frame, smart_device
            )
            smart_device.set_string_var(text_spinbox_consumption_rate)
            label_smart_plug_consumption_rate.pack(side=LEFT, anchor=W)
            spinbox_consumption_rate.pack(side=LEFT, anchor=W)
            smart_device.add_gui_objects(
                [label_smart_plug_consumption_rate, spinbox_consumption_rate]
            )
        elif isinstance(smart_device, SmartAirFryer):
            label_smart_device_switched_on.pack(side=LEFT, anchor=W)
            checkbutton_switched_on.pack(side=LEFT, anchor=W)
            label_smart_air_fryer_cooking_mode = Label(
                smart_device_frame,
                text="Cooking mode:",
                font=("sans-serif", 10),
            )
            (
                text_option_menu_cooking_mode,
                option_menu_cooking_mode,
            ) = Utilities.create_option_menu_smart_air_fryer_cooking_mode(
                smart_device_frame, smart_device
            )
            smart_device.set_string_var(text_option_menu_cooking_mode)
            label_smart_air_fryer_cooking_mode.pack(
                side=LEFT, anchor=W, padx=(0, 20)
            )
            option_menu_cooking_mode.pack(side=LEFT, anchor=W)
            smart_device.add_gui_objects(
                [label_smart_air_fryer_cooking_mode, option_menu_cooking_mode]
            )

        (
            button_toggle_smart_device,
            button_edit_smart_device,
            button_delete_smart_device,
        ) = self.create_widgets_buttons_smart_device(
            smart_device_frame, smart_device
        )

        smart_device_frame.pack(fill="both")

        smart_device.add_gui_objects(
            [
                smart_device_frame,
                label_smart_device_image,
                label_smart_device_title,
                label_smart_device_switched_on,
                checkbutton_switched_on,
                button_toggle_smart_device,
                button_edit_smart_device,
                button_delete_smart_device,
            ]
        )

    def create_widgets_smart_plug(self, smart_plug: SmartPlug):
        smart_device_image = self.images["smart_plug_image"]
        smart_device_text_title = "Smart Plug:"
        self.create_widgets_smart_device(
            smart_plug, smart_device_image, smart_device_text_title
        )

    def create_widgets_smart_air_fryer(self, smart_air_fryer: SmartAirFryer):
        smart_device_image = self.images["smart_air_fryer_image"]
        smart_device_text_title = "Smart Air Fryer:"
        self.create_widgets_smart_device(
            smart_air_fryer, smart_device_image, smart_device_text_title
        )

    def create_widgets(self):
        button_top_frame = Frame(self.main_frame)

        button_toggle_all = Button(
            button_top_frame,
            text="Toggle all",
            image=self.images["toggle_all_button_off"],
            command=lambda: self.button_toggle_all(button_toggle_all),
        )

        button_add = Button(
            self.main_frame,
            text="Add",
            image=self.images["add_button_image"],
            command=self.button_add,
        )

        button_toggle_all.pack(side=LEFT)
        button_top_frame.pack(anchor=W)

        for smart_device in self.smart_devices:
            if isinstance(smart_device, SmartPlug):
                self.create_widgets_smart_plug(smart_device)
            elif isinstance(smart_device, SmartAirFryer):
                self.create_widgets_smart_air_fryer(smart_device)

        self.smart_device_frames.pack()
        button_add.pack(side=LEFT)


class SmartHomeSystemEdit(SmartHomeSystem):
    def __init__(self, win, images):
        self.edit_window = Toplevel(win)
        self.edit_window.title("Edit")
        self.edit_window.resizable(False, False)

        self.edit_window_frame = Frame(self.edit_window)
        self.edit_window_frame.pack(padx=10, pady=10, fill="both")

        self.images = images

    # Button methods
    def edit_button_submit_smart_plug(
        self,
        smart_plug: SmartPlug,
        bool_checkbutton_switched_on: BooleanVar,
        text_spinbox_consumption_rate: StringVar,
    ):
        try:
            Utilities.set_smart_plug(
                smart_plug,
                bool_checkbutton_switched_on,
                text_spinbox_consumption_rate,
            )
            self.update_smart_device(smart_plug)
        except Exception as error:
            print("Error:", error)

    def edit_button_submit_smart_air_fryer(
        self,
        smart_air_fryer: SmartAirFryer,
        bool_checkbutton_switched_on: BooleanVar,
        text_option_menu_cooking_mode: StringVar,
    ):
        Utilities.set_smart_air_fryer(
            smart_air_fryer,
            bool_checkbutton_switched_on,
            text_option_menu_cooking_mode,
        )
        self.update_smart_device(smart_air_fryer)

    # Create widgets methods
    def edit_create_widgets(self, smart_device: SmartDevice):
        bool_checkbutton_switched_on = (
            Utilities.add_edit_create_widgets_smart_device(
                self.edit_window_frame, smart_device
            )[0]
        )

        if isinstance(smart_device, SmartPlug):
            text_spinbox_consumption_rate = (
                Utilities.add_edit_create_widgets_smart_plug(
                    self.edit_window_frame, smart_device
                )[0]
            )
            edit_button_submit = Button(
                self.edit_window_frame,
                text="Submit",
                image=self.images["submit_button_image"],
                command=lambda: self.edit_button_submit_smart_plug(
                    smart_device,
                    bool_checkbutton_switched_on,
                    text_spinbox_consumption_rate,
                ),
            )
            edit_button_submit.pack(side=LEFT, anchor=W)
        elif isinstance(smart_device, SmartAirFryer):
            text_option_menu_cooking_mode = (
                Utilities.add_edit_create_widgets_smart_air_fryer(
                    self.edit_window_frame, smart_device
                )
            )[0]
            edit_button_submit = Button(
                self.edit_window_frame,
                text="Submit",
                image=self.images["submit_button_image"],
                command=lambda: self.edit_button_submit_smart_air_fryer(
                    smart_device,
                    bool_checkbutton_switched_on,
                    text_option_menu_cooking_mode,
                ),
            )
            edit_button_submit.pack(side=LEFT, anchor=W)


class SmartHomeSystemAdd(SmartHomeSystem):
    def __init__(
        self,
        win: Tk,
        home: SmartHome,
        main_frame: Frame,
        smart_device_frames: Frame,
        images: Dict[str, PhotoImage],
    ):
        self.win = win
        self.home = home
        self.smart_devices = self.home.get_devices()
        self.main_frame = main_frame
        self.smart_device_frames = smart_device_frames

        self.images = images

        self.add_window = Toplevel(win)
        self.add_window.title("Add")
        self.add_window.resizable(False, False)
        self.add_window.geometry("300x150")

        self.add_window_frame = Frame(self.add_window)
        self.add_window_frame.pack(padx=10, pady=10, fill="both")

        self.smart_device_states = {
            "smart_device": "Smart Plug",
            "smart_plug_switched_on": False,
            "smart_plug_consumption_rate": 150,
            "smart_air_fryer_switched_on": False,
            "smart_air_fryer_cooking_mode": CookingModes.HEALTHY.value,
        }

        self.gui_objects = []

    def add_gui_objects(self, gui_objects):
        for gui_object in gui_objects:
            self.gui_objects.append(gui_object)

    def delete_gui_objects(self):
        if len(self.gui_objects) > 0:
            for gui_object in self.gui_objects:
                gui_object.destroy()

    def add_option_menu_submit(self, selected_smart_device: StringVar | str):
        # Delete existing objects if there are any (switch device)
        self.delete_gui_objects()

        # The selected_smart_device can be StringVar | str as the command for
        # the OptionMenu seems to call get() on it automatically,
        # however, it is still passed in as a StringVar
        selected_smart_device = (
            selected_smart_device.get()
            if isinstance(selected_smart_device, StringVar)
            else selected_smart_device
        )

        match selected_smart_device:
            case "Smart Plug":
                smart_plug = SmartPlug(
                    self.smart_device_states["smart_plug_consumption_rate"]
                )
                # Set the options of the last selected smart device
                try:
                    Utilities.set_smart_plug(
                        smart_plug,
                        BooleanVar(
                            self.add_window_frame,
                            self.smart_device_states["smart_plug_switched_on"],
                        ),
                        StringVar(
                            self.add_window_frame,
                            str(
                                self.smart_device_states[
                                    "smart_plug_consumption_rate"
                                ]
                            ),
                        ),
                    )
                except Exception as error:
                    print("Error:", error)

                (
                    text_option_menu_switched_on,
                    gui_objects_smart_device,
                ) = Utilities.add_edit_create_widgets_smart_device(
                    self.add_window_frame, smart_plug
                )
                (
                    text_spinbox_consumption_rate,
                    gui_objects_smart_plug,
                ) = Utilities.add_edit_create_widgets_smart_plug(
                    self.add_window_frame, smart_plug
                )
                button_add_submit_smart_plug = Button(
                    self.add_window_frame,
                    text="Submit",
                    image=self.images["submit_button_image"],
                    command=lambda: self.add_button_submit_smart_plug(
                        smart_plug,
                        text_option_menu_switched_on,
                        text_spinbox_consumption_rate,
                    ),
                )
                button_add_submit_smart_plug.pack(side=LEFT, anchor=W, pady=5)

                self.add_gui_objects(
                    [
                        *gui_objects_smart_device,
                        *gui_objects_smart_plug,
                        button_add_submit_smart_plug,
                    ]
                )

            case "Smart Air Fryer":
                smart_air_fryer = SmartAirFryer()
                # Set the options of the last selected smart device
                Utilities.set_smart_air_fryer(
                    smart_air_fryer,
                    BooleanVar(
                        self.add_window_frame,
                        self.smart_device_states[
                            "smart_air_fryer_switched_on"
                        ],
                    ),
                    StringVar(
                        self.add_window_frame,
                        self.smart_device_states[
                            "smart_air_fryer_cooking_mode"
                        ],
                    ),
                )

                (
                    text_option_menu_switched_on,
                    gui_objects_smart_device,
                ) = Utilities.add_edit_create_widgets_smart_device(
                    self.add_window_frame, smart_air_fryer
                )

                (
                    text_option_menu_cooking_mode,
                    gui_objects_smart_air_fryer,
                ) = Utilities.add_edit_create_widgets_smart_air_fryer(
                    self.add_window_frame, smart_air_fryer
                )
                button_add_submit_smart_air_fryer = Button(
                    self.add_window_frame,
                    text="Submit",
                    image=self.images["submit_button_image"],
                    command=lambda: self.add_button_submit_smart_air_fryer(
                        smart_air_fryer,
                        text_option_menu_switched_on,
                        text_option_menu_cooking_mode,
                    ),
                )
                button_add_submit_smart_air_fryer.pack(
                    side=LEFT, anchor=W, pady=5
                )

                self.add_gui_objects(
                    [
                        *gui_objects_smart_device,
                        *gui_objects_smart_air_fryer,
                        button_add_submit_smart_air_fryer,
                    ]
                )

    def set_selected_smart_plug(
        self, bool_checkbutton_switched_on, text_spinbox_consumption_rate
    ):
        self.smart_device_states["smart_device"] = "Smart Plug"
        self.smart_device_states[
            "smart_plug_switched_on"
        ] = bool_checkbutton_switched_on.get()
        self.smart_device_states["smart_plug_consumption_rate"] = int(
            text_spinbox_consumption_rate.get()
        )

    def set_selected_smart_air_fryer(
        self, bool_checkbutton_switched_on, text_option_menu_cooking_mode
    ):
        self.smart_device_states["smart_device"] = "Smart Air Fryer"
        self.smart_device_states[
            "smart_air_fryer_switched_on"
        ] = bool_checkbutton_switched_on.get()
        self.smart_device_states[
            "smart_air_fryer_cooking_mode"
        ] = text_option_menu_cooking_mode.get()

    # Button methods
    def add_button_submit_smart_plug(
        self,
        smart_plug: SmartPlug,
        bool_checkbutton_switched_on: BooleanVar,
        text_spinbox_consumption_rate: StringVar,
    ):
        try:
            Utilities.set_smart_plug(
                smart_plug,
                bool_checkbutton_switched_on,
                text_spinbox_consumption_rate,
            )
            self.home.add_device(smart_plug)
            self.create_widgets_smart_plug(smart_plug)

            # Save the options of the last selected smart device
            self.set_selected_smart_plug(
                bool_checkbutton_switched_on, text_spinbox_consumption_rate
            )

            # Call the options menu again so that a new SmartPlug object is
            # created each time
            self.add_option_menu_submit(
                StringVar(
                    self.add_window_frame,
                    self.smart_device_states["smart_device"],
                )
            )
        except Exception as error:
            print("Error:", error)

    def add_button_submit_smart_air_fryer(
        self,
        smart_air_fryer: SmartAirFryer,
        bool_checkbutton_switched_on: BooleanVar,
        text_option_menu_cooking_mode: StringVar,
    ):
        Utilities.set_smart_air_fryer(
            smart_air_fryer,
            bool_checkbutton_switched_on,
            text_option_menu_cooking_mode,
        )

        self.home.add_device(smart_air_fryer)
        self.create_widgets_smart_air_fryer(smart_air_fryer)
        # Save the options of the last selected smart device
        self.set_selected_smart_air_fryer(
            bool_checkbutton_switched_on, text_option_menu_cooking_mode
        )
        # Call the options menu again so that a new SmartAirFryer object is
        # created each time
        self.add_option_menu_submit(
            StringVar(
                self.add_window_frame, self.smart_device_states["smart_device"]
            )
        )

    # Create widgets methods
    def add_create_widgets(self):
        frame_pick_smart_device = Frame(self.add_window_frame)

        label_pick_smart_device = Label(
            frame_pick_smart_device,
            text="Pick device: ",
            font=("sans-serif", 10),
        )

        pick_smart_device_options = ["Smart Plug", "Smart Air Fryer"]
        text_option_menu_pick_smart_device = StringVar(
            frame_pick_smart_device,
            "Select a device",
        )
        option_menu_pick_smart_device = OptionMenu(
            frame_pick_smart_device,
            text_option_menu_pick_smart_device,
            *pick_smart_device_options,
            command=lambda selected_smart_device: self.add_option_menu_submit(
                selected_smart_device
            ),
        )

        label_pick_smart_device.pack(side=LEFT, anchor=W)
        option_menu_pick_smart_device.pack(side=RIGHT, anchor=E)
        frame_pick_smart_device.pack(fill="both")


def main():
    home = set_up_home()
    smart_home_system = SmartHomeSystem(home)
    smart_home_system.run()


main()
