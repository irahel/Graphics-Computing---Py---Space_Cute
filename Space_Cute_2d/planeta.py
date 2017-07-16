# Imports
from random import randint
from PIL import Image
from OpenGL.GL.exceptional import glGenTextures, glTexParameter, glBegin, glEnd
from OpenGL.GL.images import glTexImage2D
from OpenGL.raw.GL.VERSION.GL_1_0 import glPixelStorei, glColor3f, glDisable, glEnable, glTexEnvi, glPushMatrix, \
    glTexCoord2f, glVertex3f, glPopMatrix
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_QUADS, glBindTexture, GL_TEXTURE_2D, GL_UNPACK_ALIGNMENT, GL_RGBA, \
    GL_LIGHTING, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE, GL_LINEAR, GL_TEXTURE_MIN_FILTER, \
    GL_TEXTURE_MAG_FILTER
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

    # Define como o planeta deve ser desenhado
    def draw(self):

        glColor3f(1.0, 1.0, 1.0)
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, self.planets[self.skin])

        glPushMatrix()

        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex3f(self.start_position_x -(15 * self.my_scale),
                   self.move_y + self.start_position_y -(15 * self.my_scale), -1)
        glTexCoord2f(1, 1)
        glVertex3f(self.start_position_x +(15 * self.my_scale),
                   self.move_y + self.start_position_y -(15 * self.my_scale), -1)
        glTexCoord2f(1, 0)

        glVertex3f(self.start_position_x + (15 * self.my_scale),
                   self.move_y + self.start_position_y +(20 * self.my_scale), -1)
        glTexCoord2f(0, 0)
        glVertex3f(self.start_position_x -(15 * self.my_scale),
                   self.move_y + self.start_position_y + (20 * self.my_scale), -1)
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
