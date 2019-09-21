#!/usr/bin/python
import i3ipc
import json


long_to_short = {
    'English (US)': 'en',
    'Macedonian': 'mk',
}

def print_status(keyboard):
    layout  = keyboard.xkb_active_layout_name
    short_code = long_to_short.get(layout, layout)
    output = {"text": short_code, "tooltip": layout, "class": short_code}
    print(json.dumps(output), flush=True)

def find_keyboard(sway):
    # *the* keyboard is the one with more than one layout
    for input_dev in sway.get_inputs():
        if input_dev.type == 'keyboard' and len(input_dev.xkb_layout_names) > 1:
            return input_dev

def on_input(sway, event):
    if event.change == "xkb_layout" and \
        event.input.identifier == sway.keyboard.identifier:
        print_status(event.input)

def main():
    sway = i3ipc.Connection()
    sway.keyboard = find_keyboard(sway)
    print_status(sway.keyboard)

    sway.on(i3ipc.Event.INPUT, on_input)
    sway.main()

main()
