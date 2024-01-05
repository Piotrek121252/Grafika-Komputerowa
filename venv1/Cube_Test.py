import pygame

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (1, -1, -1),
    (1, -1, 1),
    (-1, -1, 1),
    (-1, -1, -1),

    (1, 1, -1),
    (1, 1, 1),
    (-1, 1, 1),
    (-1, 1, -1),
)

edges = (
    (0, 1),
    (0, 4),
    (0, 3),

    (2, 1),
    (2, 6),
    (2, 3),

    (6, 7),
    (6, 5),

    (4, 7),
    (4, 5),

    (7, 3),
    (5, 1),
)

surfaces = (
    (0,1,2,3),
    (0,1,5,4),
    (0,3,7,4),

    (4,5,6,7),
    (3,2,6,7),
    (1,2,6,5),
)

color = (

    (0.5, 0.5, 0.25),
    (0.25, 0.75, 0.5),
    #(1, 0, 0),
    (1, 1, 1),
    (1, 1, 0),
    #(0, 0, 1),
)


def cube(): 
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()    

    glBegin(GL_QUADS)
    for surface in surfaces:
        for i, vertex in enumerate(surface):
            glColor3fv(color[i]) 
            glVertex3fv(vertices[vertex])
    glEnd()           

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
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)


    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_DEPTH_TEST)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    glTranslate(0.0, -1.0, 0)
                if event.key == pygame.K_DOWN:
                    glTranslate(0.0, 1.0, 0)  
                if event.key == pygame.K_RIGHT:
                    glTranslate(-1.0, 0, 0)  
                if event.key == pygame.K_LEFT:
                    glTranslate(1.0, 0, 0)   
                if event.key == pygame.K_w:
                    glTranslate(0, 0, 1.0)  
                if event.key == pygame.K_s:
                    glTranslate(0, 0, -1.0)         
                if event.key == pygame.K_SPACE:
                    glRotatef(-90, 0, 0, -1)                        

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        cube()
        light()
        
        glRotatef(1, 0, 1, 0)

        
        pygame.display.flip()
        pygame.time.wait(10)        


main()                