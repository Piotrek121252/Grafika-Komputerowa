import pygame
import math

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


N = 2.0 / math.sqrt(3.0) # czynnik skalujący

def draw_axes():
    glBegin(GL_LINES)

    # X-axis in red
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)

    # Y-axis in green
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)

    # Z-axis in blue
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 1.0)

    glEnd()


def draw_tetrahedron(v1, v2, v3, v4):
    draw_triangle(v1, v2, v3)
    draw_triangle(v1, v3, v4)
    draw_triangle(v2, v3, v4)
    draw_triangle(v1, v2, v4)


def draw_triangle(point_a, point_b, point_c):
    glBegin(GL_TRIANGLES)

    glColor3f(1, 1, 1)
    glVertex3f(*point_a)

    glColor3f(0.75, 0.75, 0.75)
    glVertex3f(*point_b)

    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(*point_c)

    glEnd()


def draw_pyramid(v1, v2, v3, v4, level):
    if level == 0:
        draw_tetrahedron(v1, v2, v3, v4)
        return
    else:
        v12 = [
            (v1[0] + v2[0]) / 2,
            (v1[1] + v2[1]) / 2,
            (v1[2] + v2[2]) / 2
        ]

        v23 = [
            (v2[0] + v3[0]) / 2,
            (v2[1] + v3[1]) / 2,
            (v2[2] + v3[2]) / 2
        ]

        v31 = [
            (v1[0] + v3[0]) / 2,
            (v1[1] + v3[1]) / 2,
            (v1[2] + v3[2]) / 2
        ]

        v14 = [
            (v1[0] + v4[0]) / 2,
            (v1[1] + v4[1]) / 2,
            (v1[2] + v4[2]) / 2
        ]

        v24 = [
            (v2[0] + v4[0]) / 2,
            (v2[1] + v4[1]) / 2,
            (v2[2] + v4[2]) / 2
        ]

        v34 = [
            (v3[0] + v4[0]) / 2,
            (v3[1] + v4[1]) / 2,
            (v3[2] + v4[2]) / 2
        ]

        draw_pyramid(v1, v12, v31, v14, level - 1)
        draw_pyramid(v12, v2, v23, v24, level - 1)
        draw_pyramid(v31, v23, v3, v34, level - 1)
        draw_pyramid(v14, v24, v34, v4, level - 1)

points = [
            # [-1, -1, 1],
            # [1, -1, 1],
            # [0, 1, 1],
            # [0, 0.02, -1]
              [N, 0.0, -N / math.sqrt(2)],
              [-N, 0.0, -N / math.sqrt(2)],
              [0.0, 0.0, N / math.sqrt(2)],
              [0.0, math.sqrt(2.0 / 3.0) * N, 0.0]
        ]

def light():
    glLight(GL_LIGHT0, GL_POSITION,  (5, 5, 5, 0)) # źródło światła left, top, front

    # Ustawienie koloru światła otoczenia
    glLightfv(GL_LIGHT0, GL_AMBIENT, (1.0, 0.0, 0.0, 1.0))

    # Ustawienie koloru światła rozproszonego
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.0, 0.0, 1.0, 1.0))

    # Ustawienie koloru światła wypukłego
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.0, 1.0, 0.0, 1.0))
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE )


def main():
    num_of_levels = int(input("Podaj ilość poziomów Piramidy Sierpińskiego: "))

    if num_of_levels < 0:
        num_of_levels = 3
        print("Podana wartość nie spełnia wymagań, przyjmujemy poziom piramidy jako: 3.")

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    active = True

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_DEPTH_TEST)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    glTranslate(0.0, -0.2, 0)
                if event.key == pygame.K_DOWN:
                    glTranslate(0.0, 0.2, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslate(-0.2, 0, 0)
                if event.key == pygame.K_LEFT:
                    glTranslate(0.2, 0, 0)
                if event.key == pygame.K_w:
                    glTranslate(0, 0, 0.2)
                if event.key == pygame.K_s:
                    glTranslate(0, 0, -0.2)
                if event.key == pygame.K_SPACE:
                    #glRotatef(-90, 0, 0, -1)
                    active = not active

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_pyramid(points[0], points[1], points[2], points[3], num_of_levels)
        draw_axes()
        light()

        if active:
            glRotatef(0.5, 0, 1, 0)

        pygame.display.flip()
        pygame.time.wait(10)


main()