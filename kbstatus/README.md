### kbstatus

**kbstatus** is a small i3status add-on written in Python,
that let's you to display the status of your keyboard
(numlock, capslock, current layouti) in the far-left position.



## Installation

Copy kbstatus to any directory of your PATH i.e. ~/.local/bin.


Change the permission to 755 i.e. chmod 755 ~/.local/bin/kbstatus.

In ~/.i3/config replace the line in the 'bar' section:

```i3config
status_command i3status
```

to:

```i3config
status_command i3status | kbstatus
```

## Dependencies

You need have Python 3.6 or higher installed. oh
