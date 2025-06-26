# Name of the executable
TARGET = main

# Compiler and flags
CC = gcc
CFLAGS = -Wall -O2

# X11 library
LIBS = -lX11

# Source file
SRC = main.c

# Default target
all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LIBS)

# Clean target
clean:
	rm -f $(TARGET)
