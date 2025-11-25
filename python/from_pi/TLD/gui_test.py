from guizero import App, Text, TextBox, PushButton, Slider, Picture


''' Func takes the value from "my_name", which is a text box
    accepting input, and updates the "welcome_message" variable,
    which is what's displayed in the window '''

def say_my_name():
    welcome_message.value = first_name.value, last_name.value
    # Update the button message
    update_text.text = "You made a change!"


''' Func takes a value passed to it and then adjusts the message size
    based on that value '''

def change_text_size(slider_value):
    welcome_message.size = slider_value


# Creates the GUI app, with title
app = App("Hello, World!")

# Displays message in body of app window
welcome_message = Text(app, text="Welcome to my app!", size=30, font="Sans serif", color="blue")

# Displays text box in body
first_name = TextBox(app, width=20)
last_name = TextBox(app, width=20)

# Displays a button in the body
# The "command" argument allows for a function to be called on button push
update_text = PushButton(app, command=say_my_name, text="Display my name")

# Text size for slider
text_size = Slider(app, command=change_text_size, start=30, end=70)




app.display()
