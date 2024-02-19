# TODO

## Challenge Features

- [ ] Advanced Tkinter Widgets — Tkinter provides other widgets such as CheckButton or SpinBox which we have not covered in the classes. Currently, the user can only toggle each device straight from the main window. Modify your GUI to allow the user to modify other attributes of the devices directly from the main window using the widgets of your choice. You may also want to use similar widgets in the secondary windows of your app. [4 marks]
- [ ] Custom Device Visualisation — Enhance the GUI to represent each plug/device visually based on its type. For example, display a graphic or icon that represents your plugs/devices. This visual representation should provide an intuitive way for users to identify and interact with plugs/devices. Hint: look at the Photoimage widget. [3 marks]
- [ ] Interface & Accessibility setting — Improve the accessibility of your app by providing an “Accessibility settings” button. This needs to open a new window offering similar functionality to Moodle’s “Interface & Accessibility settings” menu. The user should be able to alter text size, change between light and dark mode, and also define a custom colour scheme (consisting of a background and text colour). Hint: Visit the tkColorChooser module. [4 marks]
- [ ] Permanent Data Storage — Currently, the user needs to create the devices one by one in the shell and the smart home system does not have permanent storage (i.e., upon closing the smart home system, all data will be lost). Investigate the tkFileDialog module of Tkinter which allows the user to upload a file (e.g., a text or a CSV file) where each row represents a device. Your app should also allow the user to save the state of a smart home to a file. [4 marks]
- [ ] Device Scheduler — Add a clock with hour values 0-23 which increment every 3 seconds to simulate the passing of time; “minutes” do not need to be implemented or displayed. Include a scheduling feature for devices using this clock feature, allowing users to set specific times for devices to turn on or off automatically. The main GUI window should show the clock and users should be able to see the devices turn on and off at the set times. [4 marks]

## Check

- [ ] If we are allowed to define more classes than the ones in the document
- [ ] If it's okay to things to the classes defined in the document, e.g. `error_message` is added to `SmartPlug`
