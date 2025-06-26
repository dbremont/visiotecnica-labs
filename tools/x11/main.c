#include <X11/Xlib.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    Display *display;
    Window window;
    int screen;
    GC gc;
    XEvent event;

    // Open connection to X server
    display = XOpenDisplay(NULL);
    if (display == NULL) {
        fprintf(stderr, "Unable to open X display\n");
        exit(1);
    }

    screen = DefaultScreen(display);

    // Create a simple window
    window = XCreateSimpleWindow(display, RootWindow(display, screen),
                                 100, 100, 400, 200, 1,
                                 BlackPixel(display, screen),
                                 WhitePixel(display, screen));

    // Select input events (for handling expose and close)
    XSelectInput(display, window, ExposureMask | KeyPressMask);

    // Set window title
    XStoreName(display, window, "X11 Hello World");

    // Create graphics context
    gc = XCreateGC(display, window, 0, NULL);
    XSetForeground(display, gc, BlackPixel(display, screen));

    // Show the window
    XMapWindow(display, window);

    // Event loop
    while (1) {
        XNextEvent(display, &event);

        if (event.type == Expose) {
            // Draw text
            XDrawString(display, window, gc, 50, 100, "Hello, X11 World!", 17);
        }

        if (event.type == KeyPress) {
            break;
        }
    }

    // Cleanup
    XFreeGC(display, gc);
    XDestroyWindow(display, window);
    XCloseDisplay(display);
    return 0;
}
