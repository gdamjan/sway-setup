# My Sway setup

![sway screenshot](./sway.png)

[Sway](https://swaywm.org/) is a modern tilling wayland compositor, that emulates i3.
Based on wlroots, it's one of the most featureful wayland compositors.

Still, a lot of things wont work in Wayland.

# [sway systemd integration](https://github.com/swaywm/sway/wiki/Systemd-integration)

I'm running sway as a user systemd service, started by sddm (the login manager).

* `/usr/share/wayland-sessions/sway-service.desktop` is added for a custom wayland session
* when I choose that session in sddm `/usr/local/bin/sway-service.sh` is started, which:
  * loads the sddm/pam environment into the user systemd service manager
  * then starts the sway.service
  * systemd/user/sway.service loads additional environment variables from `~/.config/sway/env`
  * waits for the service to finish, which signals the end of the session
* next, sway initializes and starts running:
  * at the end sway calls `exec "systemctl --user import-environment ; systemctl --user start sway-session.target"`
    * which imports the additional sway env vars back into systemd
  * only then `sway-session.target` is getting started:
    * it has `Wants=graphical-session-pre.target` so any desktop non-gui services starts first
    * then it has `BindsTo=graphical-session.target wayland-session.target`, and any enabled
      gui/wayland and sway applets/services start from there
    * examples are `swayidle.service` which has `WantedBy=sway-session.target` (or `wayland-session.target`)
    * same with swaybar/waybar, mako, and similar.

## Where do environment variables go?

Read `man environment.d`, environment variables set there will be read by the
--user systemd, and since everything is started in its hierarchy variables will
properly propagate.

## Wayland tools
- https://github.com/gdamjan/swaylock (fork: implements a grace period before a password is required)
- https://gist.github.com/gdamjan/1415d93b83a38f64cffea0ff4c54fc4b (nm-applet with --indicator support)
- https://github.com/kennylevinsen/wldash (runner / dashboard)
- https://github.com/Hummer12007/brightnessctl/
- https://github.com/misterdanb/avizo (notification daemon for volume/backlight)
- https://github.com/cyclopsian/wdisplays (GUI display configurator for wlroots compositors)
- https://github.com/bugaevc/wl-clipboard (Command-line copy/paste utilities for Wayland)
- https://github.com/Alexays/Waybar/pull/85#issuecomment-525223382 (sway-layout script for waybar)

… and [more](https://github.com/topics/sway).

# An unordered list of wayland bugs and issues

- all firefox issues https://bugzilla.mozilla.org/show_bug.cgi?id=635134
- ~copy by select / paste with middle click in QT/KDE apps~
  (need to implement [gtk_primary_selection_device_manager](https://bugreports.qt.io/browse/QTBUG-66008)) (qt-5.14)
- ~ctrl-Ц/В doesn't copy/paste in QT/KDE~ https://bugreports.qt.io/browse/QTBUG-65503 (fixed qt-5.13)
- ~utf-8 paste~ https://bugreports.qt.io/browse/QTBUG-54786 (fixed qt-5.13)
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

# ps: `systemd-cgls -u user.slice`

```
Unit user.slice (/user.slice):
└─user-1000.slice 
  ├─user@1000.service 
  │ ├─dbus-broker.service 
  │ │ ├─1043 /usr/bin/dbus-broker-launch --scope user
  │ │ └─1044 dbus-broker --log 4 --controller 10 --machine-id dcf0d2b9b08f4fcf8…
  │ ├─run-r142215d057bf43d3bceb5cd0158dd792.service 
  │ │ ├─2290 /usr/bin/alacritty
  │ │ └─2310 /bin/bash
  │ ├─run-r93568e2d57e14e339b1b7f25e38b521c.service 
  │ │ ├─2131 /usr/bin/alacritty
  │ │ ├─2151 /bin/bash
  │ │ └─6512 systemd-cgls -u user.slice
  │ ├─swaykbdd.service 
  │ │ └─1115 /usr/bin/swaykbdd
  │ ├─run-r8d99f10d5f2e4bf58089b02b0a7791e8.service 
  │ │ ├─2184 /usr/bin/alacritty
  │ │ └─2204 /bin/bash
  │ ├─mako.service 
  │ │ └─1116 /usr/bin/mako
  │ ├─firefox.service 
  │ │ ├─1109 /opt/firefox/firefox
  │ │ ├─1329 /opt/firefox/firefox-bin -contentproc -parentBuildID 2020110616042…
  │ │ ├─1365 /opt/firefox/firefox-bin -contentproc -childID 1 -isForBrowser -pr…
  │ │ ├─1446 /opt/firefox/firefox-bin -contentproc -childID 2 -isForBrowser -pr…
  │ │ ├─1529 /opt/firefox/firefox-bin -contentproc -childID 3 -isForBrowser -pr…
  │ │ ├─1549 /opt/firefox/firefox-bin -contentproc -childID 5 -isForBrowser -pr…
  │ │ ├─1901 /opt/firefox/firefox-bin -contentproc -childID 6 -isForBrowser -pr…
  │ │ └─1980 /opt/firefox/firefox-bin -contentproc -childID 7 -isForBrowser -pr…
  │ ├─pulseaudio.service 
  │ │ ├─1004 /usr/bin/pulseaudio --daemonize=no --log-target=journal
  │ │ └─1039 /usr/lib/pulse/gsettings-helper
  │ ├─swayidle.service 
  │ │ └─1113 /usr/bin/swayidle -w -l
  │ ├─init.scope 
  │ │ ├─878 /usr/lib/systemd/systemd --user
  │ │ └─883 (sd-pam)
  │ ├─run-r68c60c3012ca412e81cc474fbc32b2ad.service 
  │ │ ├─2237 /usr/bin/alacritty
  │ │ └─2257 /bin/bash
  │ ├─sway.service 
  │ │ ├─1045 /usr/bin/sway
  │ │ ├─1098 swaybg -o * -i /usr/share/backgrounds/sway/Sway_Wallpaper_Blue_192…
  │ │ ├─1100 swaybar -b bar-0
  │ │ ├─1120 Xwayland :1 -rootless -terminate -listen 21 -listen 23 -wm 47
  │ │ └─1164 i3status-rs
  │ ├─org.kde.kdeconnect.service 
  │ │ ├─1112 /usr/lib/kdeconnectd
  │ │ ├─2493 kdeinit5: Running...
  │ │ ├─2494 /usr/lib/kf5/klauncher --fd=8
  │ │ └─2496 tags.so [kdeinit5] tags local:/run/user/1000/klauncherRBMkrF.1.sla…
  │ └─run-r652066f058184006ae1d462739e93b52.service 
  │   └─2062 /usr/bin/communi
  └─session-2.scope 
    ├─1012 /usr/lib/sddm/sddm-helper --socket /tmp/sddm-authe3be91ee-741e-41f8-…
    ├─1019 /usr/bin/kwalletd5 --pam-login 7 3
    └─1021 systemctl --wait --user start sway.service
```
