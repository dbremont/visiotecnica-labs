# Name of the output binary
TARGET = main

# Source files
SRCS = main.c

# Compiler and pkg-config flags
CC = gcc
CFLAGS = `pkg-config --cflags gtk+-3.0`
LIBS = `pkg-config --libs gtk+-3.0`

# Default target
all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

# Clean target
clean:
	rm -f $(TARGET)
