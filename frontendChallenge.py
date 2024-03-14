import csv
from tkinter import Button, Checkbutton, OptionMenu, PhotoImage
from typing import List, Self

from backend import SmartAirFryer, SmartDevice, SmartPlug


class Theme:
    def __init__(
        self: Self, foreground: str, background: str, activebackground: str
    ) -> None:
        self.foreground = foreground
        self.background = background
        self.activebackground = activebackground

    def get_foreground(self: Self) -> str:
        return self.foreground

    def get_background(self: Self) -> str:
        return self.background

    def get_activebackground(self: Self) -> str:
        return self.activebackground

    def configure_widget_theme(
        self: Self, widget: Checkbutton | Button
    ) -> None:
        widget.configure(
            fg=self.foreground,
            bg=self.background,
            activeforeground=self.foreground,
            activebackground=self.activebackground,
        )

    def configure_options_menu_theme(
        self: Self, option_menu: OptionMenu
    ) -> None:
        option_menu.configure(
            fg=self.foreground,
            bg=self.background,
            activeforeground=self.foreground,
            activebackground=self.activebackground,
        )
        option_menu["menu"].configure(
            fg=self.foreground,
            bg=self.background,
            activeforeground=self.foreground,
            activebackground=self.activebackground,
        )


class Themes:
    def __init__(self: Self) -> None:
        self.themes = {
            "light": Theme("#000", "#fff", "#f4f4f4"),
            "dark": Theme("#fff", "#3a3a3a", "#4a4a4a"),
            "custom": Theme("#000", "#fff", "#f4f4f4"),
        }
        self.current = self.themes["light"]

    def get_current_name(self: Self) -> str:
        if self.current == self.themes["light"]:
            return "Light"
        elif self.current == self.themes["dark"]:
            return "Dark"
        elif self.current == self.themes["custom"]:
            return "Custom"
        else:
            return "Light"

    def get_current(self: Self) -> Theme:
        return self.current

    def set_current(self: Self, theme_name: str) -> None:
        theme = theme_name.lower()
        if theme == "light" or theme == "dark" or theme == "custom":
            self.current = self.themes[theme]

    def get_custom_theme(self: Self) -> Theme:
        return self.themes["custom"]

    def set_custom_theme(
        self: Self, foreground: str, background: str, activebackground: str
    ) -> None:
        self.themes["custom"] = Theme(foreground, background, activebackground)


class Images:
    def __init__(self: Self) -> None:
        theme_dir = "./images/"
        self.images = {
            "smart_plug_image": PhotoImage(file=f"{theme_dir}plug.png"),
            "smart_air_fryer_image": PhotoImage(file=f"{theme_dir}pot.png"),
            "toggle_button_image": PhotoImage(file=f"{theme_dir}toggle.png"),
            "edit_button_image": PhotoImage(file=f"{theme_dir}edit.png"),
            "delete_button_image": PhotoImage(file=f"{theme_dir}delete.png"),
            "add_button_image": PhotoImage(file=f"{theme_dir}add.png"),
            "accessibility_button_image": PhotoImage(
                file=f"{theme_dir}settings.png"
            ),
            "submit_button_image": PhotoImage(file=f"{theme_dir}check.png"),
            "toggle_all_button_off": PhotoImage(
                file=f"{theme_dir}toggle-off.png"
            ),
            "toggle_all_button_on": PhotoImage(
                file=f"{theme_dir}toggle-on.png"
            ),
            "download_button_image": PhotoImage(
                file=f"{theme_dir}download.png"
            ),
            "upload_button_image": PhotoImage(file=f"{theme_dir}upload.png"),
        }

        for image in self.images:
            self.images[image] = self.images[image].subsample(8, 8)

    def get_smart_plug_image(self: Self) -> PhotoImage:
        return self.images["smart_plug_image"]

    def get_smart_air_fryer_image(self: Self) -> PhotoImage:
        return self.images["smart_air_fryer_image"]

    def get_toggle_button_image(self: Self) -> PhotoImage:
        return self.images["toggle_button_image"]

    def get_edit_button_image(self: Self) -> PhotoImage:
        return self.images["edit_button_image"]

    def get_delete_button_image(self: Self) -> PhotoImage:
        return self.images["delete_button_image"]

    def get_add_button_image(self: Self) -> PhotoImage:
        return self.images["add_button_image"]

    def get_accessibility_button_image(self: Self) -> PhotoImage:
        return self.images["accessibility_button_image"]

    def get_submit_button_image(self: Self) -> PhotoImage:
        return self.images["submit_button_image"]

    def get_toggle_all_button_off(self: Self) -> PhotoImage:
        return self.images["toggle_all_button_off"]

    def get_toggle_all_button_on(self: Self) -> PhotoImage:
        return self.images["toggle_all_button_on"]

    def get_download_button_image(self: Self) -> PhotoImage:
        return self.images["download_button_image"]

    def get_upload_button_image(self: Self) -> PhotoImage:
        return self.images["upload_button_image"]


class FontInfo:
    def __init__(self: Self) -> None:
        self.family = "sans-serif"
        self.size_title = 12
        self.size_body = 10

    def set_font_size(self: Self, font_size: int) -> None:
        self.size_title = font_size + 2
        self.size_body = font_size

    def get_size_title(self: Self) -> int:
        return self.size_title

    def get_size_body(self: Self) -> int:
        return self.size_body

    def get_family(self: Self) -> str:
        return self.family


class SmartDeviceFile:
    def __init__(self: Self, smart_devices: List[SmartDevice]) -> None:
        self.smart_devices: List[SmartDevice] = smart_devices

    def create_csv(self: Self) -> None:
        with open("storage.csv", mode="w") as smart_devices:
            smart_devices_writer = csv.writer(
                smart_devices,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )
            for smart_device in self.smart_devices:
                if isinstance(smart_device, SmartPlug):
                    smart_devices_writer.writerow(
                        [
                            "smart_plug",
                            f"{smart_device.get_switched_on()}",
                            f"{smart_device.get_consumption_rate()}",
                        ]
                    )
                elif isinstance(smart_device, SmartAirFryer):
                    smart_devices_writer.writerow(
                        [
                            "smart_air_fryer",
                            f"{smart_device.get_switched_on()}",
                            f"{smart_device.get_cooking_mode()}",
                        ]
                    )

    def read_csv(self: Self, file: str) -> list[str]:
        rows = []
        with open(file, mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                rows.append(row)
        return rows
