# gui/button_utils.py

import tkinter as tk

def create_styled_button(parent, text, command, state=tk.NORMAL, width=20, **kwargs):
    """
    Creates a Tkinter Button with predefined styles.

    :param parent: Parent Tkinter widget.
    :param text: The text to display on the button.
    :param command: The function to call when the button is clicked.
    :param state: The initial state of the button (e.g., tk.NORMAL, tk.DISABLED).
    :param width: The width of the button.
    :param kwargs: Additional styling options.
    :return: A Tkinter Button widget.
    """
    default_style = {

        'width': width,
        'padx': 10,
        'pady': 5
    }
    # Update default_style with any additional kwargs
    default_style.update(kwargs)
    return tk.Button(
        parent,
        text=text,
        command=command,
        state=state,
        **default_style
    )
