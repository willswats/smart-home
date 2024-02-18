# TODO

## Clean up

- [ ] Reduce repetition in `add_options_menu_submit`, `add_button_submit_smart_plug`, `add_button_submit_smart_air_fryer`

## Features

- [ ] Add error label for consumption rate entry
- [ ] Pass in `SmartPlug` or `SmartAirFryer` to `add_options_menu_submit` instead of deleting and recreating objects (to create a new instance each time)

## Fix

- [ ] Fix GUI resizing and not using all space

## Check

- [ ] If we are allowed to define more classes than the ones in the document
- [ ] If it's okay to things to the classes defined in the document, e.g. `error_message` is added to `SmartPlug`
