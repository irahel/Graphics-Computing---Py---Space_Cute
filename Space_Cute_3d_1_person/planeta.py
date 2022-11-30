# Imports
from math import pi, sin, cos
from random import randint
from OpenGL.GL import glRotate
from PIL import Image
from OpenGL.GL.exceptional import glGenTextures, glTexParameter, glBegin, glEnd
from OpenGL.GL.images import glTexImage2D
from OpenGL.raw.GL.VERSION.GL_1_0 import glPixelStorei, glColor3f, glDisable, glEnable, glTexEnvi, glPushMatrix, \
    glTexCoord2f, glVertex3f, glPopMatrix, glNormal3f
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_QUADS, glBindTexture, GL_TEXTURE_2D, GL_UNPACK_ALIGNMENT, GL_RGBA, \
    GL_LIGHTING, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE, GL_LINEAR, GL_TEXTURE_MIN_FILTER, \
    GL_TEXTURE_MAG_FILTER, GL_QUAD_STRIP
from OpenGL.raw.GL._types import GL_UNSIGNED_BYTE


# Classe
class Planeta:
    # Inicia os parametros
    # self.move_y = Controla o movimento no eixo y
    # self.dead = Indica se o objeto deve ser desenhado
    # self.start_position_x = Define a posicao inicial no eixo x
    # self.start_position_y = Define a posicao inicial no eixo y
    # self.my_scale = Define a escala do planeta
    # self.skin = Indica a textura que sera usada
    # self.imageID = Textura usada
    def __init__(self, position_x = None, scale = None, images = None):
        self.move_y = 0
        self.dead = False
        self.start_position_x = position_x
        self.start_position_y = 120
        self.my_scale = scale
        self.skin = randint(0,9)
        self.planets = images
        self.lats = 10
        self.longs = 10
        self.angle = 0
        self.z = randint(1,2)
        self.z = 40 if self.z == 1 else -40
        self.scene_angle = 0

    # Define como o planeta deve ser desenhado
    def draw(self):

        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, self.planets[self.skin])

        glPushMatrix()
        glRotate(self.scene_angle , 0, 1, 0)
        glRotate(self.angle, 0, 1, 0)
        for i in range(self.lats + 1):
            lat0 = pi * (-0.5 + float(float(i - 1) / float(self.lats)))
            z0 = sin(lat0)
            zr0 = cos(lat0)

            lat1 = pi * (-0.5 + float(float(i) / float(self.lats)))
            z1 = sin(lat1)
            zr1 = cos(lat1)

            # Use Quad strips to draw the sphere
            glBegin(GL_QUAD_STRIP)

            for j in range(self.longs + 1):
                lng = 2 * pi * float(float(j - 1) / float(self.longs))
                x = cos(lng)
                y = sin(lng)
                glTexCoord2f(0, 1)
                glNormal3f(self.start_position_x +(15 * self.my_scale) + x * (zr0 * 15),
                           self.move_y + self.start_position_y + (20 * self.my_scale) + y * (zr0 * 15), self.z + z0 * -15)
                glTexCoord2f(1, 1)
                glVertex3f(self.start_position_x +(15 * self.my_scale) + x * (zr0 * 15),
                           self.move_y + self.start_position_y + (20 * self.my_scale)+ y * (zr0 * 15), self.z +z0 * -15)
                glTexCoord2f(1, 0)
                glNormal3f(self.start_position_x +(15 * self.my_scale) + x * (zr1 * 15),
                           self.move_y + self.start_position_y + (20 * self.my_scale) + y * (zr1 * 15), self.z +z1 * -15)
                glTexCoord2f(0, 0)
                glVertex3f(self.start_position_x +(15 * self.my_scale) + x * (zr1 * 15),
                           self.move_y + self.start_position_y + (20 * self.my_scale) + y * (zr1 * 15), self.z +z1 * -15)

            glEnd()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    # Faz o movimento para baixo
    def move_down(self):
        self.move_y -= 0.2

    # Checa se o planeta saiu da tela
    def check_range(self):
        if self.move_y + self.start_position_y + (15 * self.my_scale) < -50:
            self.dead = True

    # Checa se o planeta esta morto
    def check_dead(self):
        self.check_range()

    # Define a acao a ser feita
    def act(self):
        self.move_down()
        self.angle += 0.1

    def get_x(self):
        pass

    def get_y(self):
        pass

    # Carrega as variaveis
    def load(self, position_x , scale, images):
        self.move_y = 0
        self.dead = False
        self.start_position_x = position_x
        self.start_position_y = 120
        self.my_scale = scale
        self.skin = randint(0,9)
        self.planets = images
        self.angle = 0
        self.z = randint(1,2)
        self.z = 40 if self.z == 1 else -40
        self.scene_angle = 0
