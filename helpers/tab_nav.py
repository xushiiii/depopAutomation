def focus_next_widget(textbox_dict, event, current_textbox):
    """ Move focus to the next textbox when Tab is pressed. """
    textboxes = list(textbox_dict.values())  # ✅ Get all textboxes in order
    try:
        index = textboxes.index(current_textbox)  # ✅ Find current textbox
        next_textbox = textboxes[index + 1]  # ✅ Get next textbox
        next_textbox.focus_set()  # ✅ Move focus
    except IndexError:
        pass  # ✅ If it's the last textbox, do nothing

    return "break"  # ✅ Prevent default tab behavior inside `Text` widget