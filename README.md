# [sway systemd integration](https://github.com/swaywm/sway/wiki/Systemd-integration)

* sway will `exec systemctl --user start sway-session.target` in its config file
* `sway-session.target` has `BindsTo=graphical-session.target`
* and for example `swayidle.service` will have either `WantedBy=sway-session.target` or `graphical-session.target`
  * same with swaybar/waybar, mako, and similar.

## Timeline of events:
* user logins
* pam starts systemd --user
* in the meantime sddm starts the user sway.service and waits for it to stop (ie. when sway exits)
  * sway.service wants `graphical-session-pre.target`
* sway, once ready, starts the sway-session.target, which stars other **enabled** components of sway

### Where do environment variables go?

`~/.config/sway/env` variables set for the sway service, but also imported by the systemd --user manager.

## Wayland tools
- https://github.com/gdamjan/swaylock (implements a grace period before a password is required)
- https://gist.github.com/gdamjan/1415d93b83a38f64cffea0ff4c54fc4b (nm-applet with --indicator support)
- https://github.com/Alexays/Waybar/pull/85#issuecomment-525223382 (sway-layout script for waybar)
- https://github.com/kennylevinsen/wldash (runner / dashboard)
- https://github.com/misterdanb/avizo (notification daemon for volume/backlight)
- https://github.com/Hummer12007/brightnessctl/

## Also:
- `pip install --user i3ipc`


# An unordered list of wayland bugs and issues

- copy by select / paste with middle click in QT/KDE apps 
  (need to implement [gtk_primary_selection_device_manager](https://bugreports.qt.io/browse/QTBUG-66008)) (qt-5.14)
- ~ctrl-Ц/В doesn't copy/paste in QT/KDE~ https://bugreports.qt.io/browse/QTBUG-65503 (fixed qt-5.13)
- ~utf-8 paste~ https://bugreports.qt.io/browse/QTBUG-54786 (fixed qt-5.13)
- all firefox issues https://bugzilla.mozilla.org/show_bug.cgi?id=635134
- per window/app keyboard layout
  https://github.com/swaywm/sway/pull/3155 (see https://github.com/swaywm/sway/pull/4504/files)
- keyboard layout applet ([waybar](https://github.com/Alexays/Waybar/issues/66), [protocol](https://github.com/swaywm/wlr-protocols/pull/31))
  
- ~mpv doesn't inhibit screensaver~ (fix is: --gpu-context=wayland)
  should be automatic in mpv > 0.29.1
- ~mpv error: failed to resolve wl_drm_interface(): /usr/lib/libEGL_mesa.so.0: undefined symbol: wl_drm_interface
  libva-intel-driver > 2.3.0~ (fixed in arch packages)

- xmag/zoom - double check font antialiasing
- ~networkmanager applet~ (recompiled `nm-applet --indicator`)
- ~pulseaudio applet~ (waybar kind of)
- bluetooth applet
- kdeconnect applet (and functionality: clipboard, remote control)
- ~KDE/Qt apps style~ (works fine with XDG_CURRENT_DESKTOP=KDE)
- systemd --user support in sway https://github.com/swaywm/sway/pull/3486
- generic screen/window capture (chromecasting, webrtc screensharing, screencasting) - pipewire integration in firefox/chrome
