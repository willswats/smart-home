import csv
from tkinter import OptionMenu, PhotoImage

from backend import SmartAirFryer, SmartPlug


class Themes:
    def __init__(self):
        self.themes = {
            "light": Theme("#000", "#fff", "#f4f4f4"),
            "dark": Theme("#fff", "#3a3a3a", "#4a4a4a"),
            "custom": Theme("#000", "#fff", "#f4f4f4"),
        }
        self.current = self.themes["light"]

    def get_current_name(self) -> str:
        if self.current == self.themes["light"]:
            return "Light"
        elif self.current == self.themes["dark"]:
            return "Dark"
        elif self.current == self.themes["custom"]:
            return "Custom"
        else:
            return "Light"

    def get_current(self):
        return self.current

    def set_current(self, theme_name: str):
        theme = theme_name.lower()
        if theme == "light" or theme == "dark" or theme == "custom":
            self.current = self.themes[theme]

    def get_custom_theme(self):
        return self.themes["custom"]

    def set_custom_theme(
        self, foreground: str, background: str, activebackground: str
    ):
        self.themes["custom"] = Theme(foreground, background, activebackground)


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

    def configure_widget_theme(self, widget):
        widget.configure(
            fg=self.foreground,
            bg=self.background,
            activeforeground=self.foreground,
            activebackground=self.activebackground,
        )

    def configure_options_menu_theme(self, option_menu: OptionMenu):
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


class Images:
    def __init__(self):
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

    def get_smart_plug_image(self):
        return self.images["smart_plug_image"]

    def get_smart_air_fryer_image(self):
        return self.images["smart_air_fryer_image"]

    def get_toggle_button_image(self):
        return self.images["toggle_button_image"]

    def get_edit_button_image(self):
        return self.images["edit_button_image"]

    def get_delete_button_image(self):
        return self.images["delete_button_image"]

    def get_add_button_image(self):
        return self.images["add_button_image"]

    def get_accessibility_button_image(self):
        return self.images["accessibility_button_image"]

    def get_submit_button_image(self):
        return self.images["submit_button_image"]

    def get_toggle_all_button_off(self):
        return self.images["toggle_all_button_off"]

    def get_toggle_all_button_on(self):
        return self.images["toggle_all_button_on"]

    def get_download_button_image(self):
        return self.images["download_button_image"]

    def get_upload_button_image(self):
        return self.images["upload_button_image"]


class FontInfo:
    def __init__(self):
        self.family = "sans-serif"
        self.size_title = 12
        self.size_body = 10

    def set_font_size(self, font_size):
        self.size_title = font_size + 2
        self.size_body = font_size

    def get_size_title(self):
        return self.size_title

    def get_size_body(self):
        return self.size_body

    def get_family(self):
        return self.family


class SmartDeviceFile:
    def __init__(self, smart_devices):
        self.smart_devices = smart_devices

    def create_csv(self):
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

    def read_csv(self, file):
        rows = []
        with open(file, mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                rows.append(row)
        return rows
