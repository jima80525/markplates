#!/usr/bin/env python

def flying_pig_menu():
    components = ["SPAM", "BAKED BEANS"]
    menu_item = [component[0] for component in range(0, 6)]
    menu_item.append(components[1])

    menu_string = ",".join(menu_item) + f"+{component[1]}"
    return menu_string


print("Hello world")
print("Vikings love:", viking_menu)
