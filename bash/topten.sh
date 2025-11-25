# find top ten largest files for the given directory

sudo du -ah $1 | sort -rh | head -10
