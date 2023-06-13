<!-- prettier-ignore -->
### kbstatus

kbstatus is a small addon to the i3status, which allows you
to display the status of your keyboard. (numlock, capslock,
current layout, etc.)

## Installation

Copy kbstatus to any directory of your PATH i.e. ~/.local/bin.
Change the permission to 755 i.e. chmod 755 ~/.local/bin/kbstatus.
In ~/.i3/config replace the line:

<!-- prettier-ignore -->
```i3config
status_command i3status | kbstatus

```
