#!/bin/bash

original_window=$(kdotool getactivewindow)

# left pane
xfce4-terminal --window --default-working-directory=/home/adam --tab --working-directory=/home/adam/Downloads --title=Downloads --tab --working-directory=/home/adam/Techsquare/clients/engaging/docs --title=Clients --tab --working-directory=/home/adam/notes --title=Notes --tab
sleep 1
qdbus-qt6 org.kde.kglobalaccel /component/kwin invokeShortcut "Window Quick Tile Left"
#xdotool keydown ctrl+alt key comma keyup ctrl+alt
#wtype -M ctrl alt comma -m ctrl alt

# right pane
xfce4-terminal --window --default-working-directory=/home/adam --tab --tab --tab --tab --working-directory=/home/adam/Backups --title=Backups
sleep 1
qdbus-qt6 org.kde.kglobalaccel /component/kwin invokeShortcut "Window Quick Tile Right"
#xdotool keydown ctrl+alt key period keyup ctrl+alt

# focus on original window
kdotool windowactivate "${original_window}"

# tab over to clients window
#xdotool keydown alt key Tab keyup alt

# start up key agent wrapper
#shopt -s expand_aliases
#source ~/.bash_aliases
#atka
