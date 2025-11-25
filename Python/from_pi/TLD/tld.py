from guizero import App, Combo, Text, PushButton, Picture

def button_do():
    if class_choice.value == "Warrior":
        class_stats.value = "STR\t40\nDEX\t25\nVIT\t30\nAGI\t15\nINT\t10\nMND\t10\n\nABILITY:\tProvoke\nDraw enemy attacks"
        class_image.value = "warrior.png"
    elif class_choice.value == "Monk":
        class_stats.value = "STR\t30\nDEX\t25\nVIT\t40\nAGI\t15\nINT\t10\nMND\t10\n\nABILITY:\tFocus\nDouble attack power"
        class_image.value = "monk.png"
    elif class_choice.value == "White Mage":
        class_stats.value = "STR\t10\nDEX\t15\nVIT\t25\nAGI\t10\nINT\t30\nMND\t40\n\nABILITY:\tCure\nHeal an ally"
        class_image.value = "white_mage.png"
    elif class_choice.value == "Black Mage":
        class_stats.value = "STR\t10\nDEX\t15\nVIT\t10\nAGI\t25\nINT\t40\nMND\t30\n\nABILITY:\tFireball\nCast Fire on an enemy"
        class_image.value = "black_mage.png"
    elif class_choice.value == "Thief":
        class_stats.value = "STR\t25\nDEX\t40\nVIT\t10\nAGI\t30\nINT\t15\nMND\t10\n\nABILITY:\tSteal\nSteal an item from an enemy"
        class_image.value = "thief.png"

# Create the GUI
app = App(title="The Last Dream", width=450, height=300, layout="grid")

# Message
message = Text(app, text="Create a character", size=25, grid=[0,1], font="Sans serif", color="black")

# Creates drop-down list
class_choice = Combo(app, options=["Warrior", "Monk", "White Mage", "Black Mage", "Thief"], grid=[0,4], align="left")

# Class choice
class_desc = Text(app, text="Choose your class: ", grid=[0,3], align="left")

# Button
class_select = PushButton(app, command=button_do, text="Select", grid=[0,8], align="left")
# Make a function that displays an image for the class selected

# Display class stats
class_stats = Text(app, text="STR\t40\nDEX\t25\nVIT\t30\nAGI\t15\nINT\t10\nMND\t10\n\nABILITY:\tProvoke\nDraw enemy attacks", grid=[0,6], align="right")

# Class image
class_image = Picture(app, image="warrior.png", grid=[1,6], align="right", width=100, height=100)

# Special ability
#class_ability = Text(app, text="ABILITY: Provoke\nDraw enemy attacks", grid=[0,8], align="right")


app.display()
