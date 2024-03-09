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


# Used in accessibility (distinguish Label from another
# when changing font size)
class SmartDeviceTitles(Enum):
    SMART_PLUG = "Smart Plug:"
    SMART_AIR_FRYER = "Smart Air Fryer:"


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


class SmartDeviceGui:
    def __init__(self, smart_device: SmartDevice):
        self.smart_device = smart_device
        # bool_var is used to set and get the switched_on Checkbox value
        # on the GUI
        self.bool_var: BooleanVar | None = None
        # string_var is used to set and get the consumption_rate Spinbox and
        # cooking_mode OptionMenu for a SmartPlug or SmartAirFryer on the GUI
        self.string_var: StringVar | None = None
        self.widgets = []

    def get_smart_device(self):
        return self.smart_device

    def get_string_var(self):
        return self.string_var

    def set_string_var(self, string_var):
        self.string_var = string_var

    def set_string_var_value(self, value):
        if self.string_var is not None:
            self.string_var.set(value)

    def get_bool_var(self):
        return self.bool_var

    def set_bool_var(self, bool_var):
        self.bool_var = bool_var

    def set_bool_var_value(self, value):
        if self.bool_var is not None:
            self.bool_var.set(value)

    def toggle_smart_device(self):
        self.smart_device.toggle_switch()
        self.update_smart_device()

    def set_smart_device_switched_on(
        self,
        bool_checkbutton_switched_on: BooleanVar,
    ):
        switched_on = bool_checkbutton_switched_on.get()
        if switched_on != self.smart_device.get_switched_on():
            self.smart_device.toggle_switch()

    def get_widgets(self):
        return self.widgets

    def add_widgets(self, widgets):
        for widget in widgets:
            self.widgets.append(widget)

    def delete_widgets(self):
        for widget in self.widgets:
            widget.destroy()

    def update_smart_device(self):
        self.set_bool_var_value(self.smart_device.get_switched_on())
        if isinstance(self.smart_device, SmartPlug):
            self.set_string_var_value(self.smart_device.get_consumption_rate())
        elif isinstance(self.smart_device, SmartAirFryer):
            self.set_string_var_value(self.smart_device.get_cooking_mode())


class SmartPlugGui(SmartDeviceGui):
    def __init__(self, smart_plug: SmartPlug):
        super().__init__(smart_plug)
        self.smart_device = smart_plug

    def get_smart_device(self):
        return self.smart_device

    def set_smart_plug_consumption_rate(
        self,
        text_spinbox_consumption_rate: StringVar,
    ):
        text_consumption_rate = text_spinbox_consumption_rate.get()
        try:
            self.smart_device.set_consumption_rate(int(text_consumption_rate))
        except Exception as error:
            raise error

    # This is needed for the Spinbox bind on return, because
    # I am raising an error in set_smart_plug_consumption_rate to ensure
    # that a device is not added, even when the validation fails
    def set_smart_plug_consumption_rate_validate(
        self,
        text_spinbox_consumption_rate: StringVar,
    ):
        try:
            self.set_smart_plug_consumption_rate(text_spinbox_consumption_rate)
        except Exception as error:
            print("Error:", error)

    def set_smart_plug(
        self,
        bool_checkbutton_switched_on: BooleanVar,
        text_spinbox_consumption_rate: StringVar,
    ):
        self.set_smart_device_switched_on(bool_checkbutton_switched_on)
        self.set_smart_plug_consumption_rate(text_spinbox_consumption_rate)


class SmartAirFryerGui(SmartDeviceGui):
    def __init__(self, smart_air_fryer: SmartAirFryer):
        super().__init__(smart_air_fryer)
        self.smart_device = smart_air_fryer

    def get_smart_device(self):
        return self.smart_device

    def set_smart_air_fryer_cooking_mode(
        self,
        text_option_menu_cooking_mode: StringVar,
    ):
        text_cooking_mode = text_option_menu_cooking_mode.get()
        self.smart_device.set_cooking_mode(text_cooking_mode)

    def set_smart_air_fryer(
        self,
        bool_checkbutton_switched_on: BooleanVar,
        text_option_menu_cooking_mode: StringVar,
    ):
        self.set_smart_device_switched_on(bool_checkbutton_switched_on)
        self.set_smart_air_fryer_cooking_mode(text_option_menu_cooking_mode)


class SmartDevicesStateManager:
    def __init__(self, home):
        self.home = home
        self.smart_devices_gui = []

        for smart_device in self.home.get_devices():
            if isinstance(smart_device, SmartPlug):
                smart_plug_gui = SmartPlugGui(smart_device)
                self.smart_devices_gui.append(smart_plug_gui)
            elif isinstance(smart_device, SmartAirFryer):
                smart_air_fryer_gui = SmartAirFryerGui(smart_device)
                self.smart_devices_gui.append(smart_air_fryer_gui)

    def get_smart_devices_gui(self):
        return self.smart_devices_gui

    def add_smart_device(self, smart_device_gui: SmartDeviceGui):
        smart_device = smart_device_gui.get_smart_device()
        self.home.add_device(smart_device)
        self.smart_devices_gui.append(smart_device_gui)

    def delete_smart_device(self, smart_device_gui: SmartDeviceGui):
        smart_device = smart_device_gui.get_smart_device()
        smart_device_index = self.home.get_devices().index(smart_device)
        self.home.remove_device_at(smart_device_index)

        self.smart_devices_gui.remove(smart_device_gui)
        smart_device_gui.delete_widgets()

    def toggle_all_smart_devices(
        self,
        button_toggle_all: Button,
        image_off: PhotoImage,
        image_on: PhotoImage,
    ):
        self.home.toggle_switch_all()
        self.update_all_smart_devices_gui()

        if self.home.get_switch_all_state() is False:
            button_toggle_all.config(image=image_off)
        elif self.home.get_switch_all_state() is True:
            button_toggle_all.config(image=image_on)

    def update_all_smart_devices_gui(self):
        for smart_device_gui in self.smart_devices_gui:
            smart_device_gui.update_smart_device()


class Theme:
    def __init__(
        self, foreground: str, background: str, activebackground: str
    ):
        self.foreground = foreground
        self.background = background
        self.activebackground = activebackground

    def get_foreground(self):
        return self.foreground

    def get_background(self):
        return self.background

    def get_activebackground(self):
        return self.activebackground


class CreateWidgets:
    # General create widget methods
    @staticmethod
    def create_checkbox_smart_device_switched_on(
        frame: Frame,
        smart_device_gui: SmartDeviceGui,
        current_theme: Theme,
    ):
        smart_device = smart_device_gui.get_smart_device()

        bool_checkbutton_switched_on = BooleanVar(
            frame, smart_device.get_switched_on()
        )
        checkbutton_switched_on = Checkbutton(
            frame,
            variable=bool_checkbutton_switched_on,
            onvalue=True,
            offvalue=False,
            # Always keep fg as black as the checkbutton bg
            # doesn't fully change
            fg="black",
            bg=current_theme.get_background(),
            activeforeground=current_theme.get_foreground(),
            activebackground=current_theme.get_activebackground(),
            command=lambda: smart_device_gui.set_smart_device_switched_on(
                bool_checkbutton_switched_on
            ),
        )

        return bool_checkbutton_switched_on, checkbutton_switched_on

    @staticmethod
    def create_spinbox_smart_plug_consumption_rate(
        frame: Frame,
        smart_plug_gui: SmartPlugGui,
        current_theme: Theme,
    ):
        smart_plug = smart_plug_gui.get_smart_device()
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
            fg=current_theme.get_foreground(),
            bg=current_theme.get_background(),
            command=lambda: smart_plug_gui.set_smart_plug_consumption_rate(
                text_spinbox_consumption_rate
            ),
        )
        spinbox_consumption_rate.bind(
            "<Return>",
            lambda _: smart_plug_gui.set_smart_plug_consumption_rate_validate(
                text_spinbox_consumption_rate
            ),
        )

        return text_spinbox_consumption_rate, spinbox_consumption_rate

    @staticmethod
    def create_option_menu_smart_air_fryer_cooking_mode(
        frame: Frame,
        smart_air_fryer_gui: SmartAirFryerGui,
        current_theme: Theme,
    ):
        smart_air_fryer = smart_air_fryer_gui.get_smart_device()

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
            command=lambda _: smart_air_fryer_gui.set_smart_air_fryer_cooking_mode(  # noqa: E501
                text_option_menu_cooking_mode
            ),
        )
        option_menu_cooking_mode.configure(
            fg=current_theme.get_foreground(),
            bg=current_theme.get_background(),
            activeforeground=current_theme.get_foreground(),
            activebackground=current_theme.get_background(),
        )
        option_menu_cooking_mode["menu"].configure(
            fg=current_theme.get_foreground(),
            bg=current_theme.get_background(),
            activeforeground=current_theme.get_foreground(),
            activebackground=current_theme.get_activebackground(),
        )

        return text_option_menu_cooking_mode, option_menu_cooking_mode

    # Add & edit create widgets methods
    @staticmethod
    def add_edit_create_widgets_smart_device(
        frame: Frame,
        smart_device_gui: SmartDeviceGui,
        font_size: int,
        current_theme: Theme,
    ) -> tuple[BooleanVar, list[Frame | Label | Checkbutton]]:
        frame_switched_on = Frame(frame)

        label_switched_on = Label(
            frame_switched_on,
            text="Switched on: ",
            font=("sans-serif", font_size),
            fg=current_theme.get_foreground(),
            bg=current_theme.get_background(),
        )

        (
            bool_checkbutton_switched_on,
            checkbutton_switched_on,
        ) = CreateWidgets.create_checkbox_smart_device_switched_on(
            frame_switched_on, smart_device_gui, current_theme
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
        frame: Frame,
        smart_plug_gui: SmartPlugGui,
        font_size: int,
        current_theme: Theme,
    ) -> tuple[StringVar, list[Frame | Label | Spinbox]]:
        frame_consumption_rate = Frame(frame)

        label_consumption_rate = Label(
            frame_consumption_rate,
            text="Consumption rate: ",
            fg=current_theme.get_foreground(),
            bg=current_theme.get_background(),
            font=("sans-serif", font_size),
        )

        (
            text_spinbox_consumption_rate,
            spinbox_consumption_rate,
        ) = CreateWidgets.create_spinbox_smart_plug_consumption_rate(
            frame_consumption_rate, smart_plug_gui, current_theme
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
        frame: Frame,
        smart_air_fryer_gui: SmartAirFryerGui,
        font_size: int,
        current_theme: Theme,
    ) -> tuple[StringVar, list[Frame | Label | OptionMenu]]:
        frame_cooking_mode = Frame(frame)

        label_cooking_modes = Label(
            frame_cooking_mode,
            text="Cooking modes: ",
            font=("sans-serif", font_size),
            fg=current_theme.get_foreground(),
            bg=current_theme.get_background(),
        )

        (
            text_option_menu_cooking_mode,
            option_menu_cooking_mode,
        ) = CreateWidgets.create_option_menu_smart_air_fryer_cooking_mode(
            frame_cooking_mode, smart_air_fryer_gui, current_theme
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

        self.button_top_frame = Frame(self.main_frame)

        self.smart_device_frames = Frame(self.main_frame)

        self.smart_devices_state_manager = SmartDevicesStateManager(home)

        self.font_sizes = {
            "title": 12,
            "body": 10,
        }

        self.themes = {
            "light": Theme("#000", "#fff", "#EDEDED"),
            "dark": Theme("#fff", "#1a1a1a", "#2C2C2C"),
        }
        self.current_theme = self.themes["light"]

        self.win.configure(bg=self.current_theme.get_background())
        self.main_frame.configure(bg=self.current_theme.get_background())
        self.smart_device_frames.configure(
            bg=self.current_theme.get_background()
        )
        self.button_top_frame.configure(bg=self.current_theme.get_background())

        self.images = {
            "smart_plug_image": PhotoImage(file="./assets/plug.png"),
            "smart_air_fryer_image": PhotoImage(file="./assets/pot.png"),
            "toggle_button_image": PhotoImage(file="./assets/toggle.png"),
            "edit_button_image": PhotoImage(file="./assets/edit.png"),
            "delete_button_image": PhotoImage(file="./assets/delete.png"),
            "add_button_image": PhotoImage(file="./assets/add.png"),
            "accessibility_button_image": PhotoImage(
                file="./assets/settings.png"
            ),
            "submit_button_image": PhotoImage(file="./assets/check.png"),
            "toggle_all_button_off": PhotoImage(
                file="./assets/toggle-off.png"
            ),
            "toggle_all_button_on": PhotoImage(file="./assets/toggle-on.png"),
        }

        for image in self.images:
            self.images[image] = self.images[image].subsample(8, 8)

    def run(self):
        self.create_widgets()
        self.win.mainloop()

    # Set methods
    def set_font_size(self, font_size):
        self.font_sizes["title"] = font_size + 2
        self.font_sizes["body"] = font_size

    def set_theme(self, theme):
        if theme == "Light":
            self.current_theme = self.themes["light"]
        elif theme == "Dark":
            self.current_theme = self.themes["dark"]
        self.set_theme_widgets()

    def set_theme_widgets(self):
        self.win.configure(bg=self.current_theme.get_background())
        self.main_frame.configure(bg=self.current_theme.get_background())
        self.smart_device_frames.configure(
            bg=self.current_theme.get_background()
        )
        self.button_top_frame.configure(bg=self.current_theme.get_background())

        def configure_widget_theme_all(widget):
            widget.configure(
                fg=self.current_theme.get_foreground(),
                bg=self.current_theme.get_background(),
                activeforeground=self.current_theme.get_foreground(),
                activebackground=self.current_theme.get_activebackground(),
            )

        for device in self.smart_devices_state_manager.get_smart_devices_gui():
            for widget in device.get_widgets():
                if isinstance(widget, Frame):
                    widget.configure(
                        bg=self.current_theme.get_background(),
                    )
                elif isinstance(widget, Checkbutton):
                    configure_widget_theme_all(widget)
                    widget.configure(
                        # Always keep fg as black as the checkbutton bg
                        # doesn't fully change
                        fg="black",
                    )
                elif isinstance(widget, Button):
                    configure_widget_theme_all(widget)
                elif isinstance(widget, OptionMenu):
                    configure_widget_theme_all(widget)
                    configure_widget_theme_all(widget["menu"])
                else:
                    widget.configure(
                        fg=self.current_theme.get_foreground(),
                        bg=self.current_theme.get_background(),
                    )

    # Widget submit methods
    def button_toggle(self, smart_device_gui: SmartDeviceGui):
        smart_device_gui.toggle_smart_device()

    def button_delete(self, smart_device_gui: SmartDeviceGui):
        self.smart_devices_state_manager.delete_smart_device(smart_device_gui)

    def button_toggle_all(self, button_toggle_all):
        image_off = self.images["toggle_all_button_off"]
        image_on = self.images["toggle_all_button_on"]
        self.smart_devices_state_manager.toggle_all_smart_devices(
            button_toggle_all, image_off, image_on
        )

    def button_edit(self, smart_device_gui: SmartDeviceGui):
        smart_home_system_edit = SmartHomeSystemEdit(
            self.win, self.font_sizes, self.current_theme, self.images
        )
        smart_home_system_edit.edit_create_widgets(smart_device_gui)

    def button_add(self):
        smart_home_system_add = SmartHomeSystemAdd(
            self.win,
            self.smart_device_frames,
            self.smart_devices_state_manager,
            self.font_sizes,
            self.current_theme,
            self.images,
        )
        smart_home_system_add.add_create_widgets()

    def button_accessibility(self):
        smart_home_system_accessibility = SmartHomeSystemAccessibility(
            self.win,
            self.main_frame,
            self.smart_device_frames,
            self.button_top_frame,
            self.smart_devices_state_manager,
            self.font_sizes,
            self.current_theme,
            self.themes,
            self.images,
        )
        smart_home_system_accessibility.accessibility_create_widgets()

    # Create widgets methods
    def create_widgets_buttons_smart_device(
        self, frame: Frame, smart_device_gui: SmartDeviceGui
    ):
        button_toggle_smart_device = Button(
            frame,
            image=self.images["toggle_button_image"],
            bg=self.current_theme.get_background(),
            command=lambda: self.button_toggle(smart_device_gui),
        )
        button_edit_smart_device = Button(
            frame,
            image=self.images["edit_button_image"],
            bg=self.current_theme.get_background(),
            command=lambda: self.button_edit(smart_device_gui),
        )
        button_delete_smart_device = Button(
            frame,
            image=self.images["delete_button_image"],
            bg=self.current_theme.get_background(),
            command=lambda: self.button_delete(smart_device_gui),
        )

        button_delete_smart_device.pack(side=RIGHT, anchor=E, padx=(5, 0))
        button_edit_smart_device.pack(side=RIGHT, anchor=E)
        button_toggle_smart_device.pack(side=RIGHT, anchor=E, padx=(5, 0))

        return (
            button_toggle_smart_device,
            button_edit_smart_device,
            button_delete_smart_device,
        )

    def create_widgets_smart_device(
        self,
        smart_device_gui: SmartDeviceGui,
        smart_device_image: PhotoImage,
        smart_device_text_title: str,
    ):
        smart_device_frame = Frame(self.smart_device_frames)
        smart_device_frame.configure(
            background=self.current_theme.get_background()
        )

        label_smart_device_image = Label(
            smart_device_frame,
            image=smart_device_image,
            bg=self.current_theme.get_background(),
        )
        label_smart_device_title = Label(
            smart_device_frame,
            text=smart_device_text_title,
            font=(
                "sans-serif",
                self.font_sizes["title"],
                "bold",
            ),
            fg=self.current_theme.get_foreground(),
            bg=self.current_theme.get_background(),
        )

        label_smart_device_switched_on = Label(
            smart_device_frame,
            text="Switched on:",
            font=("sans-serif", self.font_sizes["body"]),
            fg=self.current_theme.get_foreground(),
            bg=self.current_theme.get_background(),
        )
        (
            bool_checkbutton_switched_on,
            checkbutton_switched_on,
        ) = CreateWidgets.create_checkbox_smart_device_switched_on(
            smart_device_frame, smart_device_gui, self.current_theme
        )
        smart_device_gui.set_bool_var(bool_checkbutton_switched_on)

        label_smart_device_image.pack(side=LEFT, anchor=W)
        label_smart_device_title.pack(side=LEFT, anchor=W)

        if isinstance(smart_device_gui, SmartPlugGui):
            label_smart_device_switched_on.pack(
                side=LEFT, anchor=W, padx=(40, 0)
            )
            checkbutton_switched_on.pack(side=LEFT, anchor=W)

            label_smart_plug_consumption_rate = Label(
                smart_device_frame,
                text="Consumption rate:",
                font=("sans-serif", self.font_sizes["body"]),
                fg=self.current_theme.get_foreground(),
                bg=self.current_theme.get_background(),
            )
            (
                text_spinbox_consumption_rate,
                spinbox_consumption_rate,
            ) = CreateWidgets.create_spinbox_smart_plug_consumption_rate(
                smart_device_frame, smart_device_gui, self.current_theme
            )
            smart_device_gui.set_string_var(text_spinbox_consumption_rate)
            label_smart_plug_consumption_rate.pack(side=LEFT, anchor=W)
            spinbox_consumption_rate.pack(side=LEFT, anchor=W)
            smart_device_gui.add_widgets(
                [label_smart_plug_consumption_rate, spinbox_consumption_rate]
            )
        elif isinstance(smart_device_gui, SmartAirFryerGui):
            label_smart_device_switched_on.pack(side=LEFT, anchor=W)
            checkbutton_switched_on.pack(side=LEFT, anchor=W)

            label_smart_air_fryer_cooking_mode = Label(
                smart_device_frame,
                text="Cooking mode:",
                font=("sans-serif", self.font_sizes["body"]),
                fg=self.current_theme.get_foreground(),
                bg=self.current_theme.get_background(),
            )
            (
                text_option_menu_cooking_mode,
                option_menu_cooking_mode,
            ) = CreateWidgets.create_option_menu_smart_air_fryer_cooking_mode(
                smart_device_frame, smart_device_gui, self.current_theme
            )
            smart_device_gui.set_string_var(text_option_menu_cooking_mode)
            label_smart_air_fryer_cooking_mode.pack(
                side=LEFT, anchor=W, padx=(0, 20)
            )
            option_menu_cooking_mode.pack(side=LEFT, anchor=W)
            smart_device_gui.add_widgets(
                [label_smart_air_fryer_cooking_mode, option_menu_cooking_mode]
            )

        (
            button_toggle_smart_device,
            button_edit_smart_device,
            button_delete_smart_device,
        ) = self.create_widgets_buttons_smart_device(
            smart_device_frame, smart_device_gui
        )

        smart_device_frame.pack(fill="both")

        smart_device_gui.add_widgets(
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

    def create_widgets_smart_plug(self, smart_plug_gui: SmartPlugGui):
        smart_device_image = self.images["smart_plug_image"]
        smart_device_text_title = SmartDeviceTitles.SMART_PLUG.value
        self.create_widgets_smart_device(
            smart_plug_gui, smart_device_image, smart_device_text_title
        )

    def create_widgets_smart_air_fryer(
        self, smart_air_fryer_gui: SmartAirFryerGui
    ):
        smart_device_image = self.images["smart_air_fryer_image"]
        smart_device_text_title = SmartDeviceTitles.SMART_AIR_FRYER.value
        self.create_widgets_smart_device(
            smart_air_fryer_gui, smart_device_image, smart_device_text_title
        )

    def create_widgets(self):
        button_toggle_all = Button(
            self.button_top_frame,
            image=self.images["toggle_all_button_off"],
            bg=self.current_theme.get_background(),
            command=lambda: self.button_toggle_all(button_toggle_all),
        )

        button_accessibility = Button(
            self.button_top_frame,
            image=self.images["accessibility_button_image"],
            bg=self.current_theme.get_background(),
            command=lambda: self.button_accessibility(),
        )

        button_add = Button(
            self.main_frame,
            image=self.images["add_button_image"],
            bg=self.current_theme.get_background(),
            command=self.button_add,
        )

        button_toggle_all.pack(side=LEFT)
        button_accessibility.pack(side=RIGHT)
        self.button_top_frame.pack(fill="both")

        for (
            smart_device_gui
        ) in self.smart_devices_state_manager.get_smart_devices_gui():
            if isinstance(smart_device_gui, SmartPlugGui):
                self.create_widgets_smart_plug(smart_device_gui)
            elif isinstance(smart_device_gui, SmartAirFryerGui):
                self.create_widgets_smart_air_fryer(smart_device_gui)

        self.smart_device_frames.pack()
        button_add.pack(side=LEFT)


class SmartHomeSystemEdit(SmartHomeSystem):
    def __init__(
        self,
        win: Tk,
        font_sizes: dict[str, int],
        current_theme: Theme,
        images: dict[str, PhotoImage],
    ):
        self.edit_window = Toplevel(win)
        self.edit_window.title("Edit")
        self.edit_window.resizable(False, False)

        self.edit_window_frame = Frame(self.edit_window)
        self.edit_window_frame.pack(padx=10, pady=10, fill="both")

        self.font_sizes = font_sizes
        self.current_theme = current_theme
        self.images = images

    # Edit widget submit methods
    def edit_button_submit_smart_plug(
        self,
        smart_plug_gui: SmartPlugGui,
        bool_checkbutton_switched_on: BooleanVar,
        text_spinbox_consumption_rate: StringVar,
    ):
        try:
            smart_plug_gui.set_smart_plug(
                bool_checkbutton_switched_on,
                text_spinbox_consumption_rate,
            )
            smart_plug_gui.update_smart_device()
        except Exception as error:
            print("Error:", error)

    def edit_button_submit_smart_air_fryer(
        self,
        smart_air_fryer_gui: SmartAirFryerGui,
        bool_checkbutton_switched_on: BooleanVar,
        text_option_menu_cooking_mode: StringVar,
    ):
        smart_air_fryer_gui.set_smart_air_fryer(
            bool_checkbutton_switched_on,
            text_option_menu_cooking_mode,
        )
        smart_air_fryer_gui.update_smart_device()

    # Edit create widgets methods
    def edit_create_widgets_smart_plug(
        self,
        smart_plug_gui: SmartPlugGui,
        bool_checkbutton_switched_on: BooleanVar,
    ):
        text_spinbox_consumption_rate = (
            CreateWidgets.add_edit_create_widgets_smart_plug(
                self.edit_window_frame,
                smart_plug_gui,
                self.font_sizes["body"],
                self.current_theme,
            )[0]
        )
        edit_button_submit = Button(
            self.edit_window_frame,
            image=self.images["submit_button_image"],
            bg=self.current_theme.get_background(),
            command=lambda: self.edit_button_submit_smart_plug(
                smart_plug_gui,
                bool_checkbutton_switched_on,
                text_spinbox_consumption_rate,
            ),
        )
        edit_button_submit.pack(side=LEFT, anchor=W)

    def edit_create_widgets_smart_air_fryer(
        self,
        smart_air_fryer_gui: SmartAirFryerGui,
        bool_checkbutton_switched_on: BooleanVar,
    ):
        text_option_menu_cooking_mode = (
            CreateWidgets.add_edit_create_widgets_smart_air_fryer(
                self.edit_window_frame,
                smart_air_fryer_gui,
                self.font_sizes["body"],
                self.current_theme,
            )
        )[0]
        edit_button_submit = Button(
            self.edit_window_frame,
            image=self.images["submit_button_image"],
            bg=self.current_theme.get_background(),
            command=lambda: self.edit_button_submit_smart_air_fryer(
                smart_air_fryer_gui,
                bool_checkbutton_switched_on,
                text_option_menu_cooking_mode,
            ),
        )
        edit_button_submit.pack(side=LEFT, anchor=W)

    def edit_create_widgets(self, smart_device_gui: SmartDeviceGui):
        bool_checkbutton_switched_on = (
            CreateWidgets.add_edit_create_widgets_smart_device(
                self.edit_window_frame,
                smart_device_gui,
                self.font_sizes["body"],
                self.current_theme,
            )[0]
        )

        if isinstance(smart_device_gui, SmartPlugGui):
            self.edit_create_widgets_smart_plug(
                smart_device_gui, bool_checkbutton_switched_on
            )
        elif isinstance(smart_device_gui, SmartAirFryerGui):
            self.edit_create_widgets_smart_air_fryer(
                smart_device_gui, bool_checkbutton_switched_on
            )


class SmartHomeSystemAdd(SmartHomeSystem):
    def __init__(
        self,
        win: Tk,
        smart_device_frames: Frame,
        smart_devices_state_manager: SmartDevicesStateManager,
        font_sizes: Dict[str, int],
        current_theme: Theme,
        images: Dict[str, PhotoImage],
    ):
        self.win = win
        self.smart_device_frames = smart_device_frames
        self.smart_devices_state_manager = smart_devices_state_manager
        self.font_sizes = font_sizes
        self.current_theme = current_theme
        self.images = images

        self.add_window = Toplevel(win)
        self.add_window.title("Add")
        self.add_window.resizable(False, False)
        self.add_window.configure(bg=self.current_theme.get_background())

        self.add_window_frame = Frame(self.add_window)
        self.add_window_frame.pack(padx=10, pady=10, fill="both")
        self.add_window_frame.configure(bg=self.current_theme.get_background())

        self.smart_device_states = {
            "smart_device": "Smart Plug",
            "smart_plug_switched_on": False,
            "smart_plug_consumption_rate": 150,
            "smart_air_fryer_switched_on": False,
            "smart_air_fryer_cooking_mode": CookingModes.HEALTHY.value,
        }

        self.widgets = []

    def add_widgets(self, widgets):
        for widget in widgets:
            self.widgets.append(widget)

    def delete_widgets(self):
        if len(self.widgets) > 0:
            for widget in self.widgets:
                widget.destroy()

    # Set methods for the last selected device state
    def set_selected_smart_plug(
        self, bool_checkbutton_switched_on, text_spinbox_consumption_rate
    ):
        self.smart_device_states["smart_device"] = "Smart Plug"
        self.smart_device_states["smart_plug_switched_on"] = (
            bool_checkbutton_switched_on.get()
        )
        self.smart_device_states["smart_plug_consumption_rate"] = int(
            text_spinbox_consumption_rate.get()
        )

    def set_selected_smart_air_fryer(
        self, bool_checkbutton_switched_on, text_option_menu_cooking_mode
    ):
        self.smart_device_states["smart_device"] = "Smart Air Fryer"
        self.smart_device_states["smart_air_fryer_switched_on"] = (
            bool_checkbutton_switched_on.get()
        )
        self.smart_device_states["smart_air_fryer_cooking_mode"] = (
            text_option_menu_cooking_mode.get()
        )

    # Add widget submit methods
    def add_option_menu_submit(self, selected_smart_device: StringVar | str):
        # Delete existing objects if there are any (switch device)
        self.delete_widgets()

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
                smart_plug_gui = SmartPlugGui(SmartPlug(150))
                self.add_create_widgets_smart_plug(smart_plug_gui)
            case "Smart Air Fryer":
                smart_air_fryer_gui = SmartAirFryerGui(SmartAirFryer())
                self.add_create_widgets_smart_air_fryer(smart_air_fryer_gui)

    def add_button_submit_smart_plug(
        self,
        smart_plug_gui: SmartPlugGui,
        bool_checkbutton_switched_on: BooleanVar,
        text_spinbox_consumption_rate: StringVar,
    ):
        try:
            smart_plug_gui.set_smart_plug(
                bool_checkbutton_switched_on,
                text_spinbox_consumption_rate,
            )
            self.smart_devices_state_manager.add_smart_device(smart_plug_gui)
            self.create_widgets_smart_plug(smart_plug_gui)

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
        smart_air_fryer_gui: SmartAirFryerGui,
        bool_checkbutton_switched_on: BooleanVar,
        text_option_menu_cooking_mode: StringVar,
    ):
        smart_air_fryer_gui.set_smart_air_fryer(
            bool_checkbutton_switched_on,
            text_option_menu_cooking_mode,
        )
        self.smart_devices_state_manager.add_smart_device(smart_air_fryer_gui)
        self.create_widgets_smart_air_fryer(smart_air_fryer_gui)
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

    # Add create widgets methods
    def add_create_widgets_smart_plug(self, smart_plug_gui: SmartPlugGui):
        # Set the options of the last selected smart device
        try:
            smart_plug_gui.set_smart_plug(
                BooleanVar(
                    self.add_window_frame,
                    self.smart_device_states["smart_plug_switched_on"],
                ),
                StringVar(
                    self.add_window_frame,
                    str(
                        self.smart_device_states["smart_plug_consumption_rate"]
                    ),
                ),
            )
        except Exception as error:
            print("Error:", error)

        (
            text_option_menu_switched_on,
            gui_objects_smart_device,
        ) = CreateWidgets.add_edit_create_widgets_smart_device(
            self.add_window_frame,
            smart_plug_gui,
            self.font_sizes["body"],
            self.current_theme,
        )
        (
            text_spinbox_consumption_rate,
            gui_objects_smart_plug,
        ) = CreateWidgets.add_edit_create_widgets_smart_plug(
            self.add_window_frame,
            smart_plug_gui,
            self.font_sizes["body"],
            self.current_theme,
        )

        button_add_submit_smart_plug = Button(
            self.add_window_frame,
            image=self.images["submit_button_image"],
            bg=self.current_theme.get_background(),
            command=lambda: self.add_button_submit_smart_plug(
                smart_plug_gui,
                text_option_menu_switched_on,
                text_spinbox_consumption_rate,
            ),
        )
        button_add_submit_smart_plug.pack(side=LEFT, anchor=W, pady=5)

        self.add_widgets(
            [
                *gui_objects_smart_device,
                *gui_objects_smart_plug,
                button_add_submit_smart_plug,
            ]
        )

    def add_create_widgets_smart_air_fryer(self, smart_air_fryer_gui):
        # Set the options of the last selected smart device
        smart_air_fryer_gui.set_smart_air_fryer(
            BooleanVar(
                self.add_window_frame,
                self.smart_device_states["smart_air_fryer_switched_on"],
            ),
            StringVar(
                self.add_window_frame,
                self.smart_device_states["smart_air_fryer_cooking_mode"],
            ),
        )

        (
            text_option_menu_switched_on,
            gui_objects_smart_device,
        ) = CreateWidgets.add_edit_create_widgets_smart_device(
            self.add_window_frame,
            smart_air_fryer_gui,
            self.font_sizes["body"],
            self.current_theme,
        )

        (
            text_option_menu_cooking_mode,
            gui_objects_smart_air_fryer,
        ) = CreateWidgets.add_edit_create_widgets_smart_air_fryer(
            self.add_window_frame,
            smart_air_fryer_gui,
            self.font_sizes["body"],
            self.current_theme,
        )

        button_add_submit_smart_air_fryer = Button(
            self.add_window_frame,
            image=self.images["submit_button_image"],
            bg=self.current_theme.get_background(),
            command=lambda: self.add_button_submit_smart_air_fryer(
                smart_air_fryer_gui,
                text_option_menu_switched_on,
                text_option_menu_cooking_mode,
            ),
        )
        button_add_submit_smart_air_fryer.pack(side=LEFT, anchor=W, pady=5)

        self.add_widgets(
            [
                *gui_objects_smart_device,
                *gui_objects_smart_air_fryer,
                button_add_submit_smart_air_fryer,
            ]
        )

    def add_create_widgets(self):
        frame_pick_smart_device = Frame(self.add_window_frame)
        frame_pick_smart_device.configure(
            bg=self.current_theme.get_background()
        )

        label_pick_smart_device = Label(
            frame_pick_smart_device,
            text="Pick device: ",
            font=("sans-serif", self.font_sizes["body"]),
            fg=self.current_theme.get_foreground(),
            bg=self.current_theme.get_background(),
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


class SmartHomeSystemAccessibility(SmartHomeSystem):
    # Change between light and dark (toggle button)
    # Custom colour scheme (background and text colour) (tkColor)
    def __init__(
        self,
        win: Tk,
        main_frame: Frame,
        smart_device_frames: Frame,
        button_top_frame: Frame,
        smart_devices_state_manager: SmartDevicesStateManager,
        font_sizes: dict[str, int],
        current_theme: Theme,
        themes: dict[str, Theme],
        images: dict[str, PhotoImage],
    ):
        self.win = win
        self.main_frame = main_frame
        self.smart_device_frames = smart_device_frames
        self.button_top_frame = button_top_frame
        self.smart_devices_state_manager = smart_devices_state_manager
        self.font_sizes = font_sizes
        self.current_theme = current_theme
        self.themes = themes
        self.images = images

        self.accessibility_window = Toplevel(win)
        self.accessibility_window.title("Accessibility")
        self.accessibility_window.resizable(False, False)

        self.accessibility_window_frame = Frame(self.accessibility_window)
        self.accessibility_window_frame.pack(padx=10, pady=10, fill="both")

        self.maximum_font_size = 32
        self.minimum_font_size = 10

    def set_widgets_font_size(self, font_size):
        if (
            font_size >= self.minimum_font_size
            and font_size <= self.maximum_font_size
        ):
            smart_device_titles = [
                smart_device_title.value
                for smart_device_title in SmartDeviceTitles
            ]
            for (
                device
            ) in self.smart_devices_state_manager.get_smart_devices_gui():
                for widget in device.get_widgets():
                    if isinstance(widget, Label):
                        if widget.cget("text") in smart_device_titles:
                            widget.config(
                                font=("sans-serif", font_size + 2, "bold")
                            )
                        else:
                            widget.config(font=("sans-serif", font_size))
        else:
            print(
                f"Error: font size must be >= {self.minimum_font_size} \
and <= {self.maximum_font_size}"
            )

    def option_menu_theme_submit(self, theme):
        theme_value = theme.get()
        self.set_theme(theme_value)

    def spinbox_font_size_submit(self, font_size):
        try:
            font_size_value = int(font_size.get())
            self.set_font_size(font_size_value)
            self.set_widgets_font_size(font_size_value)
        except Exception as error:
            print("Error:", error)

    def accessibility_create_widgets_font_size(self):
        frame_font_size = Frame(self.accessibility_window)

        label_font_size = Label(
            frame_font_size,
            text="Font size: ",
            font=("sans-serif", self.font_sizes["body"]),
            fg=self.current_theme.get_foreground(),
            bg=self.current_theme.get_background(),
        )

        text_spinbox_font_size = StringVar(
            frame_font_size, str(self.font_sizes["body"])
        )

        spinbox_font_size = Spinbox(
            frame_font_size,
            textvariable=text_spinbox_font_size,
            from_=self.minimum_font_size,
            to=self.maximum_font_size,
            width=9,
            fg=self.current_theme.get_foreground(),
            bg=self.current_theme.get_background(),
            command=lambda: self.spinbox_font_size_submit(
                text_spinbox_font_size
            ),
        )
        spinbox_font_size.bind(
            "<Return>",
            lambda _: self.spinbox_font_size_submit(text_spinbox_font_size),
        )

        label_font_size.pack(side=LEFT)
        spinbox_font_size.pack(side=RIGHT)
        frame_font_size.pack(fill="both")

    def accessibility_create_widgets_theme(self):
        frame_theme = Frame(self.accessibility_window)

        theme_options = ["Light", "Dark"]

        text_option_menu_theme = StringVar(
            frame_theme,
            f"{theme_options[0]}",
        )

        label_theme = Label(
            frame_theme,
            text="Theme: ",
            font=("sans-serif", self.font_sizes["body"]),
            fg=self.current_theme.get_foreground(),
            bg=self.current_theme.get_background(),
        )

        option_menu_theme = OptionMenu(
            frame_theme,
            text_option_menu_theme,
            *theme_options,
            command=lambda _: self.option_menu_theme_submit(
                text_option_menu_theme
            ),
        )

        label_theme.pack(side=LEFT)
        option_menu_theme.pack(side=RIGHT)
        frame_theme.pack(fill="both")

    def accessibility_create_widgets(self):
        self.accessibility_create_widgets_font_size()
        self.accessibility_create_widgets_theme()


def main():
    home = set_up_home()
    smart_home_system = SmartHomeSystem(home)
    smart_home_system.run()


main()
