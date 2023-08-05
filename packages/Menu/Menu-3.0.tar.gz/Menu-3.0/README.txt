====
Menu
====

Easily create command-line menus.


Create a Menu
-------------

The Menu constructor arguments are all optional. The arguments are options, title, message, and refresh. Options is a list of tuples consisting of a name and a handler. Refresh is a handler called before showing the menu.

	Menu() # empty menu, will close upon opening
	Menu(options = [("Option Name", optionHandler)]) # customize the options
	Menu(title = "Menu title") # customize the title
	Menu(message = "Message text") # customize the message, disabled by default
	Menu(prompt = ">") # customize the user input prompt

Open the menu

    Menu().open()

Close the menu from the instance

    Menu().close()

or before defining it

    Menu(options = [("Close", Menu.CLOSE)])

Change the menu after creation

    menu = Menu()
    menu.set_options([("new option name", newOptionHandler)])
    menu.set_title("new title")
    menu.set_message("new message")
    menu.set_prompt("new prompt")

Easily create a submenu

	main = Menu(title = "Main Menu")
    sub = Menu(title = "Submenu")
    main.set_options([
        ("Open submenu", sub.open),
        ("Close main menu", main.close)
    ])
    sub.set_options([
        ("Return to main menu", sub.close)
    ])
    main.open()
