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
    colorchooser,
    filedialog,
)

from backend import (
    CookingModes,
    SmartAirFryer,
    SmartDevice,
    SmartHome,
    SmartPlug,
)
from frontendChallenge import FontInfo, Images, SmartDeviceFile, Themes


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

    def delete_all_smart_devices(self):
        for smart_device_gui in self.smart_devices_gui:
            smart_device_gui.delete_widgets()

        self.smart_devices_gui = []
        self.home.delete_all_devices()


class Utilities:
    # General create widget methods
    @staticmethod
    def create_checkbox_smart_device_switched_on(
        frame: Frame,
        smart_device_gui: SmartDeviceGui,
        themes: Themes,
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
            bg=themes.get_current().get_background(),
            activeforeground=themes.get_current().get_foreground(),
            activebackground=themes.get_current().get_activebackground(),
            command=lambda: smart_device_gui.set_smart_device_switched_on(
                bool_checkbutton_switched_on
            ),
        )

        return bool_checkbutton_switched_on, checkbutton_switched_on

    @staticmethod
    def create_spinbox_smart_plug_consumption_rate(
        frame: Frame,
        smart_plug_gui: SmartPlugGui,
        themes: Themes,
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
            fg=themes.get_current().get_foreground(),
            bg=themes.get_current().get_background(),
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
        themes: Themes,
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
        themes.get_current().configure_options_menu_theme(
            option_menu_cooking_mode
        )

        return text_option_menu_cooking_mode, option_menu_cooking_mode

    # Add & edit create widgets methods
    @staticmethod
    def add_edit_create_widgets_smart_device(
        frame: Frame,
        smart_device_gui: SmartDeviceGui,
        font_info: FontInfo,
        themes: Themes,
    ) -> tuple[BooleanVar, list[Frame | Label | Checkbutton]]:
        frame_switched_on = Frame(frame)
        frame_switched_on.configure(bg=themes.get_current().get_background())

        label_switched_on = Label(
            frame_switched_on,
            text="Switched on: ",
            font=(font_info.get_family(), font_info.get_size_body()),
            fg=themes.get_current().get_foreground(),
            bg=themes.get_current().get_background(),
        )

        (
            bool_checkbutton_switched_on,
            checkbutton_switched_on,
        ) = Utilities.create_checkbox_smart_device_switched_on(
            frame_switched_on, smart_device_gui, themes
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
        font_info: FontInfo,
        themes: Themes,
    ) -> tuple[StringVar, list[Frame | Label | Spinbox]]:
        frame_consumption_rate = Frame(frame)
        frame_consumption_rate.configure(
            bg=themes.get_current().get_background()
        )

        label_consumption_rate = Label(
            frame_consumption_rate,
            text="Consumption rate: ",
            fg=themes.get_current().get_foreground(),
            bg=themes.get_current().get_background(),
            font=(font_info.get_family(), font_info.get_size_body()),
        )

        (
            text_spinbox_consumption_rate,
            spinbox_consumption_rate,
        ) = Utilities.create_spinbox_smart_plug_consumption_rate(
            frame_consumption_rate, smart_plug_gui, themes
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
        font_info: FontInfo,
        themes: Themes,
    ) -> tuple[StringVar, list[Frame | Label | OptionMenu]]:
        frame_cooking_mode = Frame(frame)
        frame_cooking_mode.configure(bg=themes.get_current().get_background())

        label_cooking_modes = Label(
            frame_cooking_mode,
            text="Cooking modes: ",
            font=(font_info.get_family(), font_info.get_size_body()),
            fg=themes.get_current().get_foreground(),
            bg=themes.get_current().get_background(),
        )

        (
            text_option_menu_cooking_mode,
            option_menu_cooking_mode,
        ) = Utilities.create_option_menu_smart_air_fryer_cooking_mode(
            frame_cooking_mode, smart_air_fryer_gui, themes
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

        self.button_top_frame = Frame(self.main_frame)

        self.home = home

        # To access the widgets and set the theme for them
        self.non_smart_device_buttons = []

        self.smart_devices_state_manager = SmartDevicesStateManager(home)

        self.font_info = FontInfo()

        self.themes = Themes()

        self.win.configure(bg=self.themes.get_current().get_background())
        self.main_frame.configure(
            bg=self.themes.get_current().get_background()
        )
        self.smart_device_frames.configure(
            bg=self.themes.get_current().get_background()
        )
        self.button_top_frame.configure(
            bg=self.themes.get_current().get_background()
        )

        self.images = Images()

    def run(self):
        self.create_widgets()
        self.win.mainloop()

    # Set methods
    def set_theme(self, theme):
        self.themes.set_current(theme)
        self.set_theme_widgets()

    def set_theme_widgets(self):
        current_theme = self.themes.get_current()
        self.win.configure(bg=current_theme.get_background())
        self.main_frame.configure(bg=current_theme.get_background())
        self.smart_device_frames.configure(bg=current_theme.get_background())
        self.button_top_frame.configure(bg=current_theme.get_background())

        for button in self.non_smart_device_buttons:
            self.themes.get_current().configure_widget_theme(button)

        for device in self.smart_devices_state_manager.get_smart_devices_gui():
            for widget in device.get_widgets():
                if isinstance(widget, Frame):
                    widget.configure(
                        bg=current_theme.get_background(),
                    )
                elif isinstance(widget, Checkbutton):
                    current_theme.configure_widget_theme(widget)
                    widget.configure(
                        # Always keep fg as black as the checkbutton bg
                        # doesn't fully change
                        fg="black",
                    )
                elif isinstance(widget, Button):
                    current_theme.configure_widget_theme(widget)
                elif isinstance(widget, OptionMenu):
                    current_theme.configure_options_menu_theme(widget)
                else:
                    widget.configure(
                        fg=current_theme.get_foreground(),
                        bg=current_theme.get_background(),
                    )

    # Widget submit methods
    def button_toggle(self, smart_device_gui: SmartDeviceGui):
        smart_device_gui.toggle_smart_device()

    def button_delete(self, smart_device_gui: SmartDeviceGui):
        self.smart_devices_state_manager.delete_smart_device(smart_device_gui)

    def button_toggle_all(self, button_toggle_all):
        image_off = self.images.get_toggle_all_button_off()
        image_on = self.images.get_toggle_all_button_on()
        self.smart_devices_state_manager.toggle_all_smart_devices(
            button_toggle_all, image_off, image_on
        )

    def button_edit(self, smart_device_gui: SmartDeviceGui):
        smart_home_system_edit = SmartHomeSystemEdit(
            self.win, self.font_info, self.themes, self.images
        )
        smart_home_system_edit.edit_create_widgets(smart_device_gui)

    def button_add(self):
        smart_home_system_add = SmartHomeSystemAdd(
            self.win,
            self.smart_device_frames,
            self.smart_devices_state_manager,
            self.font_info,
            self.themes,
            self.images,
        )
        smart_home_system_add.add_create_widgets()

    def button_accessibility(self):
        smart_home_system_accessibility = SmartHomeSystemAccessibility(
            self.win,
            self.main_frame,
            self.smart_device_frames,
            self.button_top_frame,
            self.non_smart_device_buttons,
            self.smart_devices_state_manager,
            self.font_info,
            self.themes,
            self.images,
        )
        smart_home_system_accessibility.accessibility_create_widgets()

    def button_download(self):
        smart_device_file = SmartDeviceFile(self.home.get_devices())
        smart_device_file.create_csv()

    def button_upload(self):
        smart_device_file = SmartDeviceFile(self.home.get_devices())
        file = filedialog.askopenfile()
        if file is not None:
            self.smart_devices_state_manager.delete_all_smart_devices()
            smart_device_rows = smart_device_file.read_csv(file.name)

            for smart_device_row in smart_device_rows:
                device_type = smart_device_row[0]
                if device_type == "smart_plug":
                    switched_on = smart_device_row[1]
                    consumption_rate = int(smart_device_row[2])

                    smart_plug = SmartPlug(consumption_rate)
                    if switched_on is True:
                        smart_plug.toggle_switch()

                    smart_plug_gui = SmartPlugGui(smart_plug)

                    self.smart_devices_state_manager.add_smart_device(
                        smart_plug_gui
                    )
                elif device_type == "smart_air_fryer":
                    switched_on = smart_device_row[1]
                    cooking_mode = smart_device_row[2]

                    smart_air_fryer = SmartAirFryer()
                    if switched_on is True:
                        smart_air_fryer.toggle_switch()
                    smart_air_fryer.set_cooking_mode(cooking_mode)

                    smart_air_fryer_gui = SmartAirFryerGui(smart_air_fryer)

                    self.smart_devices_state_manager.add_smart_device(
                        smart_air_fryer_gui
                    )

        for (
            smart_device_gui
        ) in self.smart_devices_state_manager.get_smart_devices_gui():
            if isinstance(smart_device_gui, SmartPlugGui):
                self.create_widgets_smart_plug(smart_device_gui)
            elif isinstance(smart_device_gui, SmartAirFryerGui):
                self.create_widgets_smart_air_fryer(smart_device_gui)

    # Create widgets methods
    def create_widgets_buttons_smart_device(
        self, frame: Frame, smart_device_gui: SmartDeviceGui
    ):
        button_toggle_smart_device = Button(
            frame,
            image=self.images.get_toggle_button_image(),
            command=lambda: self.button_toggle(smart_device_gui),
        )
        button_edit_smart_device = Button(
            frame,
            image=self.images.get_edit_button_image(),
            command=lambda: self.button_edit(smart_device_gui),
        )
        button_delete_smart_device = Button(
            frame,
            image=self.images.get_delete_button_image(),
            command=lambda: self.button_delete(smart_device_gui),
        )

        self.themes.get_current().configure_widget_theme(
            button_toggle_smart_device
        )
        self.themes.get_current().configure_widget_theme(
            button_edit_smart_device
        )
        self.themes.get_current().configure_widget_theme(
            button_delete_smart_device
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
            background=self.themes.get_current().get_background()
        )

        label_smart_device_image = Label(
            smart_device_frame,
            image=smart_device_image,
            bg=self.themes.get_current().get_background(),
        )
        label_smart_device_title = Label(
            smart_device_frame,
            text=smart_device_text_title,
            font=(
                self.font_info.get_family(),
                self.font_info.get_size_title(),
                "bold",
            ),
            fg=self.themes.get_current().get_foreground(),
            bg=self.themes.get_current().get_background(),
        )

        label_smart_device_switched_on = Label(
            smart_device_frame,
            text="Switched on:",
            font=(self.font_info.get_family(), self.font_info.get_size_body()),
            fg=self.themes.get_current().get_foreground(),
            bg=self.themes.get_current().get_background(),
        )
        (
            bool_checkbutton_switched_on,
            checkbutton_switched_on,
        ) = Utilities.create_checkbox_smart_device_switched_on(
            smart_device_frame, smart_device_gui, self.themes
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
                font=(
                    self.font_info.get_family(),
                    self.font_info.get_size_body(),
                ),
                fg=self.themes.get_current().get_foreground(),
                bg=self.themes.get_current().get_background(),
            )
            (
                text_spinbox_consumption_rate,
                spinbox_consumption_rate,
            ) = Utilities.create_spinbox_smart_plug_consumption_rate(
                smart_device_frame, smart_device_gui, self.themes
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
                font=(
                    self.font_info.get_family(),
                    self.font_info.get_size_body(),
                ),
                fg=self.themes.get_current().get_foreground(),
                bg=self.themes.get_current().get_background(),
            )
            (
                text_option_menu_cooking_mode,
                option_menu_cooking_mode,
            ) = Utilities.create_option_menu_smart_air_fryer_cooking_mode(
                smart_device_frame, smart_device_gui, self.themes
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
        smart_device_image = self.images.get_smart_plug_image()
        smart_device_text_title = SmartDeviceTitles.SMART_PLUG.value
        self.create_widgets_smart_device(
            smart_plug_gui, smart_device_image, smart_device_text_title
        )

    def create_widgets_smart_air_fryer(
        self, smart_air_fryer_gui: SmartAirFryerGui
    ):
        smart_device_image = self.images.get_smart_air_fryer_image()
        smart_device_text_title = SmartDeviceTitles.SMART_AIR_FRYER.value
        self.create_widgets_smart_device(
            smart_air_fryer_gui, smart_device_image, smart_device_text_title
        )

    def create_widgets(self):
        button_toggle_all = Button(
            self.button_top_frame,
            image=self.images.get_toggle_all_button_off(),
            command=lambda: self.button_toggle_all(button_toggle_all),
        )

        button_accessibility = Button(
            self.button_top_frame,
            image=self.images.get_accessibility_button_image(),
            command=lambda: self.button_accessibility(),
        )

        button_add = Button(
            self.main_frame,
            image=self.images.get_add_button_image(),
            command=self.button_add,
        )

        button_download = Button(
            self.button_top_frame,
            image=self.images.get_download_button_image(),
            command=self.button_download,
        )

        button_upload = Button(
            self.button_top_frame,
            image=self.images.get_upload_button_image(),
            command=self.button_upload,
        )

        self.themes.get_current().configure_widget_theme(button_toggle_all)
        self.themes.get_current().configure_widget_theme(button_accessibility)
        self.themes.get_current().configure_widget_theme(button_add)
        self.themes.get_current().configure_widget_theme(button_download)
        self.themes.get_current().configure_widget_theme(button_upload)

        self.non_smart_device_buttons.append(button_toggle_all)
        self.non_smart_device_buttons.append(button_accessibility)
        self.non_smart_device_buttons.append(button_add)
        self.non_smart_device_buttons.append(button_download)
        self.non_smart_device_buttons.append(button_upload)

        button_toggle_all.pack(side=LEFT)

        button_accessibility.pack(side=RIGHT, padx=(5, 0))
        button_download.pack(side=RIGHT)
        button_upload.pack(side=RIGHT, padx=(5, 0))
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
        font_info: FontInfo,
        themes: Themes,
        images: Images,
    ):
        self.edit_window = Toplevel(win)
        self.edit_window.title("Edit")
        self.edit_window.resizable(False, False)

        self.edit_window_frame = Frame(self.edit_window)
        self.edit_window_frame.pack(padx=10, pady=10, fill="both")

        self.font_info = font_info
        self.themes = themes
        self.images = images

        self.edit_window.configure(
            bg=self.themes.get_current().get_background()
        )
        self.edit_window_frame.configure(
            bg=self.themes.get_current().get_background()
        )

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
        themes: Themes,
    ):
        text_spinbox_consumption_rate = (
            Utilities.add_edit_create_widgets_smart_plug(
                self.edit_window_frame,
                smart_plug_gui,
                self.font_info,
                self.themes,
            )[0]
        )
        edit_button_submit = Button(
            self.edit_window_frame,
            image=self.images.get_submit_button_image(),
            bg=self.themes.get_current().get_background(),
            command=lambda: self.edit_button_submit_smart_plug(
                smart_plug_gui,
                bool_checkbutton_switched_on,
                text_spinbox_consumption_rate,
            ),
        )
        themes.get_current().configure_widget_theme(edit_button_submit)
        edit_button_submit.pack(side=LEFT, anchor=W)

    def edit_create_widgets_smart_air_fryer(
        self,
        smart_air_fryer_gui: SmartAirFryerGui,
        bool_checkbutton_switched_on: BooleanVar,
        themes: Themes,
    ):
        text_option_menu_cooking_mode = (
            Utilities.add_edit_create_widgets_smart_air_fryer(
                self.edit_window_frame,
                smart_air_fryer_gui,
                self.font_info,
                self.themes,
            )
        )[0]
        edit_button_submit = Button(
            self.edit_window_frame,
            image=self.images.get_submit_button_image(),
            bg=self.themes.get_current().get_background(),
            command=lambda: self.edit_button_submit_smart_air_fryer(
                smart_air_fryer_gui,
                bool_checkbutton_switched_on,
                text_option_menu_cooking_mode,
            ),
        )
        themes.get_current().configure_widget_theme(edit_button_submit)

        edit_button_submit.pack(side=LEFT, anchor=W)

    def edit_create_widgets(self, smart_device_gui: SmartDeviceGui):
        bool_checkbutton_switched_on = (
            Utilities.add_edit_create_widgets_smart_device(
                self.edit_window_frame,
                smart_device_gui,
                self.font_info,
                self.themes,
            )[0]
        )

        if isinstance(smart_device_gui, SmartPlugGui):
            self.edit_create_widgets_smart_plug(
                smart_device_gui, bool_checkbutton_switched_on, self.themes
            )
        elif isinstance(smart_device_gui, SmartAirFryerGui):
            self.edit_create_widgets_smart_air_fryer(
                smart_device_gui, bool_checkbutton_switched_on, self.themes
            )


class SmartHomeSystemAdd(SmartHomeSystem):
    def __init__(
        self,
        win: Tk,
        smart_device_frames: Frame,
        smart_devices_state_manager: SmartDevicesStateManager,
        font_info: FontInfo,
        themes: Themes,
        images: Images,
    ):
        self.win = win
        self.smart_device_frames = smart_device_frames
        self.smart_devices_state_manager = smart_devices_state_manager
        self.font_info = font_info
        self.themes = themes
        self.images = images

        self.add_window = Toplevel(win)
        self.add_window.title("Add")
        self.add_window.resizable(False, False)
        self.add_window.configure(
            bg=self.themes.get_current().get_background()
        )

        self.add_window_frame = Frame(self.add_window)
        self.add_window_frame.pack(padx=10, pady=10, fill="both")
        self.add_window_frame.configure(
            bg=self.themes.get_current().get_background()
        )

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
        ) = Utilities.add_edit_create_widgets_smart_device(
            self.add_window_frame,
            smart_plug_gui,
            self.font_info,
            self.themes,
        )
        (
            text_spinbox_consumption_rate,
            gui_objects_smart_plug,
        ) = Utilities.add_edit_create_widgets_smart_plug(
            self.add_window_frame,
            smart_plug_gui,
            self.font_info,
            self.themes,
        )

        button_add_submit_smart_plug = Button(
            self.add_window_frame,
            image=self.images.get_submit_button_image(),
            command=lambda: self.add_button_submit_smart_plug(
                smart_plug_gui,
                text_option_menu_switched_on,
                text_spinbox_consumption_rate,
            ),
        )
        self.themes.get_current().configure_widget_theme(
            button_add_submit_smart_plug
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
        ) = Utilities.add_edit_create_widgets_smart_device(
            self.add_window_frame,
            smart_air_fryer_gui,
            self.font_info,
            self.themes,
        )

        (
            text_option_menu_cooking_mode,
            gui_objects_smart_air_fryer,
        ) = Utilities.add_edit_create_widgets_smart_air_fryer(
            self.add_window_frame,
            smart_air_fryer_gui,
            self.font_info,
            self.themes,
        )

        button_add_submit_smart_air_fryer = Button(
            self.add_window_frame,
            image=self.images.get_submit_button_image(),
            bg=self.themes.get_current().get_background(),
            command=lambda: self.add_button_submit_smart_air_fryer(
                smart_air_fryer_gui,
                text_option_menu_switched_on,
                text_option_menu_cooking_mode,
            ),
        )
        self.themes.get_current().configure_widget_theme(
            button_add_submit_smart_air_fryer
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
            bg=self.themes.get_current().get_background()
        )

        label_pick_smart_device = Label(
            frame_pick_smart_device,
            text="Pick device: ",
            font=(self.font_info.get_family(), self.font_info.get_size_body()),
            fg=self.themes.get_current().get_foreground(),
            bg=self.themes.get_current().get_background(),
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
        self.themes.get_current().configure_options_menu_theme(
            option_menu_pick_smart_device
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
        non_smart_device_buttons: list[Button],
        smart_devices_state_manager: SmartDevicesStateManager,
        font_info: FontInfo,
        themes: Themes,
        images: Images,
    ):
        self.win = win
        self.main_frame = main_frame
        self.smart_device_frames = smart_device_frames
        self.button_top_frame = button_top_frame
        self.non_smart_device_buttons = non_smart_device_buttons
        self.smart_devices_state_manager = smart_devices_state_manager
        self.font_info = font_info
        self.themes = themes
        self.images = images

        self.accessibility_window = Toplevel(win)
        self.accessibility_window.title("Accessibility")
        self.accessibility_window.resizable(False, False)

        self.accessibility_window_frame = Frame(self.accessibility_window)
        self.accessibility_window_frame.pack(padx=10, pady=10, fill="both")

        self.accessibility_window.configure(
            bg=self.themes.get_current().get_background()
        )
        self.accessibility_window_frame.configure(
            bg=self.themes.get_current().get_background()
        )

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
                                font=(
                                    self.font_info.get_family(),
                                    font_size + 2,
                                    "bold",
                                )
                            )
                        else:
                            widget.config(
                                font=(self.font_info.get_family(), font_size)
                            )
        else:
            print(
                f"Error: font size must be >= {self.minimum_font_size} \
and <= {self.maximum_font_size}"
            )

    def accessibility_create_widgets_font_size(self):
        frame_font_size = Frame(self.accessibility_window_frame)
        frame_font_size.configure(
            bg=self.themes.get_current().get_background()
        )

        label_font_size = Label(
            frame_font_size,
            text="Font size: ",
            font=(self.font_info.get_family(), self.font_info.get_size_body()),
            fg=self.themes.get_current().get_foreground(),
            bg=self.themes.get_current().get_background(),
        )

        text_spinbox_font_size = StringVar(
            frame_font_size, str(self.font_info.get_size_body())
        )

        spinbox_font_size = Spinbox(
            frame_font_size,
            textvariable=text_spinbox_font_size,
            from_=self.minimum_font_size,
            to=self.maximum_font_size,
            width=9,
            fg=self.themes.get_current().get_foreground(),
            bg=self.themes.get_current().get_background(),
        )

        label_font_size.pack(side=LEFT)
        spinbox_font_size.pack(side=RIGHT)
        frame_font_size.pack(fill="both")

        return text_spinbox_font_size

    def accessibility_create_widgets_theme(self):
        frame_theme = Frame(self.accessibility_window_frame)
        frame_theme.configure(bg=self.themes.get_current().get_background())

        theme_options = [self.themes.get_current_name()]
        theme_names = ["Light", "Dark", "Custom"]
        for theme_name in theme_names:
            if theme_name != self.themes.get_current_name():
                theme_options.append(theme_name)

        text_option_menu_theme = StringVar(
            frame_theme,
            f"{theme_options[0]}",
        )

        label_theme = Label(
            frame_theme,
            text="Theme: ",
            font=(self.font_info.get_family(), self.font_info.get_size_body()),
            fg=self.themes.get_current().get_foreground(),
            bg=self.themes.get_current().get_background(),
        )

        option_menu_theme = OptionMenu(
            frame_theme,
            text_option_menu_theme,
            *theme_options,
        )

        self.themes.get_current().configure_options_menu_theme(
            option_menu_theme
        )

        label_theme.pack(side=LEFT)
        option_menu_theme.pack(side=RIGHT)
        frame_theme.pack(fill="both")

        return text_option_menu_theme

    def accessibility_create_widgets_colorchooser(
        self, label_colorchooser_text, text_colorchooser_value
    ):
        frame_colorchooser = Frame(self.accessibility_window_frame)
        frame_colorchooser.configure(
            bg=self.themes.get_current().get_background()
        )

        text_colorchooser = StringVar(
            frame_colorchooser, text_colorchooser_value
        )

        label_colorchooser = Label(
            frame_colorchooser,
            text=f"{label_colorchooser_text}",
            font=(self.font_info.get_family(), self.font_info.get_size_body()),
            fg=self.themes.get_current().get_foreground(),
            bg=self.themes.get_current().get_background(),
        )

        button_colorchooser = Button(
            frame_colorchooser,
            textvariable=text_colorchooser,
            command=lambda: button_colorchooser_submit(),
        )

        self.themes.get_current().configure_widget_theme(button_colorchooser)

        def button_colorchooser_submit():
            color = colorchooser.askcolor()
            hexa = color[1]
            if hexa is not None:
                text_colorchooser.set(str(hexa))

        label_colorchooser.pack(side=LEFT)
        button_colorchooser.pack(side=RIGHT)
        frame_colorchooser.pack(fill="both")

        return text_colorchooser

    def accessibility_submit(
        self,
        text_spinbox_font_size,
        text_option_menu_theme,
        text_foreground,
        text_background,
        text_activeback,
    ):
        try:
            font_size_value = int(text_spinbox_font_size.get())
            self.font_info.set_font_size(font_size_value)
            self.set_widgets_font_size(font_size_value)
        except Exception as error:
            print("Error:", error)

        foreground = text_foreground.get()
        background = text_background.get()
        activebackground = text_activeback.get()
        self.themes.set_custom_theme(foreground, background, activebackground)

        theme = text_option_menu_theme.get()
        self.set_theme(theme)

    def accessibility_create_widgets(self):
        text_spinbox_font_size = self.accessibility_create_widgets_font_size()
        text_option_menu_theme = self.accessibility_create_widgets_theme()
        text_foreground = self.accessibility_create_widgets_colorchooser(
            "Custom foreground: ",
            self.themes.get_custom_theme().get_foreground(),
        )
        text_background = self.accessibility_create_widgets_colorchooser(
            "Custom background: ",
            self.themes.get_custom_theme().get_background(),
        )
        text_activeback = self.accessibility_create_widgets_colorchooser(
            "Custom active background: ",
            self.themes.get_custom_theme().get_activebackground(),
        )
        button_accessibility_submit = Button(
            self.accessibility_window_frame,
            image=self.images.get_submit_button_image(),
            command=lambda: self.accessibility_submit(
                text_spinbox_font_size,
                text_option_menu_theme,
                text_foreground,
                text_background,
                text_activeback,
            ),
        )
        self.themes.get_current().configure_widget_theme(
            button_accessibility_submit
        )
        button_accessibility_submit.pack(side=LEFT, anchor=W, pady=5)


def main():
    home = set_up_home()
    smart_home_system = SmartHomeSystem(home)
    smart_home_system.run()


main()
