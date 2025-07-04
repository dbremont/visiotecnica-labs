# Makefile for OpenGL + GLUT example

CC = gcc
CFLAGS = -Wall -O2
LIBS = -lGL -lGLU -lglut -lm

TARGET = main
SRC = main.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LIBS)

clean:
	rm -f $(TARGET)
