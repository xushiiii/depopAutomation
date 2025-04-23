def focus_next_widget(textbox_dict, event, current_textbox):
    """ Move focus to the next textbox when Tab is pressed. """
    textboxes = list(textbox_dict.values())  
    try:
        index = textboxes.index(current_textbox) 
        next_textbox = textboxes[index + 1]  
        next_textbox.focus_set()  
    except IndexError:
        pass 

    return "break"  