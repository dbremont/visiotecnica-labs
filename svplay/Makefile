# Makefile for GTK3 + FFmpeg Video Player

CC = gcc
CFLAGS = -Wall -g
PKG_CONFIG_LIBS = libavcodec libavformat libavutil libswscale sdl2
LIBS = `pkg-config --cflags --libs $(PKG_CONFIG_LIBS)`
SRC = svplay.c
OUT = svplay

all: $(OUT)

$(OUT): $(SRC)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

clean:
	rm -f $(OUT)
