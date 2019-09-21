#!/usr/bin/env python

# This script keeps track of active keyboard layouts per window.
#
# This script requires i3ipc-python package (install it from a system package
# manager or pip).
#
# https://github.com/swaywm/sway/pull/4504/files
import i3ipc

sway = i3ipc.Connection()
prev_focused = sway.get_tree().find_focused().id
windows = {}

def on_window_focus(ipc, event):
    global windows, prev_focused

    # Save current layouts
    layouts = {input.identifier: input.xkb_active_layout_index for input in sway.get_inputs()}
    windows[prev_focused] = layouts

    # Restore layout of the newly focused window
    if event.container.id in windows:
        for (input_id, layout_index) in windows[event.container.id].items():
            if layout_index != layouts[input_id]:
                sway.command(f'input "{input_id}" xkb_switch_layout {layout_index}')

    prev_focused = event.container.id

def on_window_close(ipc, event):
    global windows
    if event.container.id in windows:
        del(windows[event.container.id])

def on_window(ipc, event):
    if event.change == "focus":
        on_window_focus(ipc, event)
    elif event.change == "close":
        on_window_close(ipc, event)

sway.on("window", on_window)
sway.main()
