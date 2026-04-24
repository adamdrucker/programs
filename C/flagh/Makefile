CC      ?= gcc
CFLAGS  ?= -O2 -Wall -Wextra
PREFIX  ?= /usr/local
BINDIR  ?= $(PREFIX)/bin

TARGET  = flagh
SRC     = flagh.c

.PHONY: all clean install uninstall

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

install: $(TARGET)
	install -d $(BINDIR)
	install -m 755 $(TARGET) $(BINDIR)/$(TARGET)

uninstall:
	rm -f $(BINDIR)/$(TARGET)
