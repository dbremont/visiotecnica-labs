#include <GL/glut.h>
#include <math.h>

float angle = 0.0f;

void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    glLoadIdentity();

    // Rotate and draw triangle
    glRotatef(angle, 0.0f, 0.0f, 1.0f);

    // glBegin(GL_TRIANGLES);
    //     glColor3f(1.0, 0.0, 0.0); glVertex2f(-0.5, -0.5);
    //     glColor3f(0.0, 1.0, 0.0); glVertex2f( 0.5, -0.5);
    //     glColor3f(0.0, 0.0, 1.0); glVertex2f( 0.0,  0.5);
    // glEnd();

    // glBegin(GL_POLYGON); // Deprecated, but works in immediate mode
    //     glVertex2f(-0.5, -0.5);
    //     glVertex2f(0.0, -0.7);
    //     glVertex2f(0.3, -0.4);
    //     glVertex2f(0.2, 0.3);
    //     glVertex2f(-0.3, 0.5);
    // glEnd();

    // glBegin(GL_LINE_LOOP);`
    //     for (int i = 0; i < 100; i++) {
    //         float angle = i * 2.0f * M_PI / 100;
    //         glVertex2f(cos(angle), sin(angle));
    //     }
    // glEnd();


    // GLfloat vertices[] = {
    //     0.0f, 0.0f, 0.0f,
    //     1.0f, 0.0f, 0.0f,
    //     1.0f, 1.0f, 0.0f,
    //     0.0f, 1.0f, 0.0f
    // };

    // glBegin(GL_LINE_LOOP); // draws connected lines between vertices and closes the loop
    // for (int i = 0; i < 4; i++) {
    //     glVertex3f(vertices[3*i], vertices[3*i+1], vertices[3*i+2]);
    // }
    // glEnd();

    //   glClear(GL_COLOR_BUFFER_BIT);

        // Draw a white grid "floor" for the tetrahedron to sit on.
        glColor3f(1.0, 1.0, 1.0);
        glBegin(GL_LINES);
        for (GLfloat i = -2.5; i <= 2.5; i += 0.25) {
            glVertex3f(i, 0, 2.5); glVertex3f(i, 0, -2.5);
            glVertex3f(2.5, 0, i); glVertex3f(-2.5, 0, i);
        }
        glEnd();

        // Draw the tetrahedron.  It is a four sided figure, so when defining it
        // with a triangle strip we have to repeat the last two vertices.
        glBegin(GL_TRIANGLE_STRIP);
            glColor3f(1, 1, 1); glVertex3f(0, 2, 0);
            glColor3f(1, 0, 0); glVertex3f(-1, 0, 1);
            glColor3f(0, 1, 0); glVertex3f(1, 0, 1);
            glColor3f(0, 0, 1); glVertex3f(0, 0, -1.4);
            glColor3f(1, 1, 1); glVertex3f(0, 2, 0);
            glColor3f(1, 0, 0); glVertex3f(-1, 0, 1);
        glEnd();

        glFlush();

    glutSwapBuffers();
}

void timer(int value) {
    angle += 1.0f;
    if (angle > 360) angle -= 360;

    glutPostRedisplay();
    glutTimerFunc(16, timer, 0);  // ~60 FPS
}

void init() {
    glClearColor(0.1, 0.1, 0.1, 1.0);
}

int main(int argc, char **argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(500, 500);
    glutCreateWindow("Rotating Triangle");

    init();
    glutDisplayFunc(display);
    glutTimerFunc(0, timer, 0);
    glutMainLoop();
    return 0;
}
