# Imports
from math import pi, sin, cos
from OpenGL.GL import glRotate
from OpenGL.GL.exceptional import glGenTextures, glTexParameter, glBegin, glEnd
from OpenGL.GL.images import glTexImage2D
from OpenGL.raw.GL.VERSION.GL_1_0 import glPixelStorei, glColor3f, glDisable, glEnable, glTexEnvi, glPushMatrix, \
    glTexCoord2f, glVertex3f, glPopMatrix, glNormal3f
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_QUADS, glBindTexture, GL_TEXTURE_2D, GL_UNPACK_ALIGNMENT, GL_RGBA, \
    GL_LIGHTING, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE, GL_LINEAR, GL_TEXTURE_MIN_FILTER, \
    GL_TEXTURE_MAG_FILTER, GL_QUAD_STRIP, GL_TRIANGLE_FAN
from OpenGL.raw.GL._types import GL_UNSIGNED_BYTE
from OpenGL.raw.GLUT import glutWireSphere
from PIL import Image
from OpenGL.GL.exceptional import glBegin, glEnd


# Classe
class Asteroide():
    # Inicia os parametros
    # self.dead = define se o objeto deve ser desenhado
    # self.move_x = Controla o movimento no eixo x do objeto
    # self.move_y = Controla o movimento no eixo y do objeto
    # self.position_x = Indica a posição inicial do x do objeto
    # self.imageID = Textura do objeto
    def __init__(self, initial_position_x = None):
        self.dead = False
        self.move_x = 0
        self.move_y = 50
        self.position_x = initial_position_x
        self.imageID = self.loadImage()
        self.lats = 10
        self.longs = 10
        self.angle = 0

    # Carrega a textura
    def loadImage(self):

        im = Image.open("img/nave1.png")

        ix, iy, image = im.size[0], im.size[1], im.tobytes()

        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, image
        )
        return ID
    # Descreve como o objeto deve ser desenhado
    def draw(self):
        glColor3f(1.0, 1.0, 1.0)
        # glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, self.imageID)

        glPushMatrix()
        # glRotate(self.angle, 0, 0, 0)
        #
        # for i in range(0, self.lats + 1):
        #     lat0 = pi * (-0.5 + float(float(i - 1) / float(self.lats)))
        #     z0 = sin(lat0)
        #     zr0 = cos(lat0)
        #
        #     lat1 = pi * (-0.5 + float(float(i) / float(self.lats)))
        #     z1 = sin(lat1)
        #     zr1 = cos(lat1)
        #
        #     # Use Quad strips to draw the sphere
        #     glBegin(GL_QUAD_STRIP)
        #
        #     for j in range(0, self.longs + 1):
        #         lng = 2 * pi * float(float(j - 1) / float(self.longs))
        #         x = cos(lng)
        #         y = sin(lng)
        #         glTexCoord2f(0, 1)
        #         glNormal3f(self.move_x + self.position_x + x * (zr0 * 3),
        #                    self.move_y + 4 + y * (zr0 * 3), z0 * 3)
        #         glTexCoord2f(1, 1)
        #         glVertex3f(self.move_x + self.position_x + x * (zr0 * 3),
        #                    self.move_y + 4+ y * (zr0 * 3), z0 * 3)
        #         glTexCoord2f(1, 0)
        #         glNormal3f(self.move_x + self.position_x + x * (zr1 * 3),
        #                    self.move_y + 4 + y * (zr1 * 3), z1 * 3)
        #         glTexCoord2f(0, 0)
        #         glVertex3f(self.move_x + self.position_x + x * (zr1 * 3),
        #                    self.move_y + 4 + y * (zr1 * 3), z1 * 3)
        #
        #     glEnd()

        # glColor3f(0, 0, 1)
        glBegin(GL_TRIANGLE_FAN)
        glTexCoord2f(0, 1)
        glVertex3f(self.move_x + self.position_x +0.5, self.move_y + 1, -3)
        glVertex3f(self.move_x + self.position_x +0, self.move_y + -1.5, -2)
        glVertex3f(self.move_x + self.position_x +1, self.move_y + -2, -2)
        glTexCoord2f(1, 1)
        glVertex3f(self.move_x + self.position_x +2, self.move_y + -1, -2)
        glVertex3f(self.move_x + self.position_x +2, self.move_y + 0, -2)
        glVertex3f(self.move_x + self.position_x +1.5, self.move_y + 1, -2)
        glVertex3f(self.move_x + self.position_x +0.5, self.move_y + 3, -2)
        glTexCoord2f(1, 0)
        glVertex3f(self.move_x + self.position_x +-0.5, self.move_y + 3, -2)
        glVertex3f(self.move_x + self.position_x +-0.2, self.move_y + 2, -2)
        glVertex3f(self.move_x + self.position_x +-1, self.move_y + 1, -2)
        glVertex3f(self.move_x + self.position_x +-2.5, self.move_y + 0, -2)
        glTexCoord2f(0, 0)
        glVertex3f(self.move_x + self.position_x +-1.5, self.move_y + -1, -2)
        glVertex3f(self.move_x + self.position_x +-0.5, self.move_y + 2, -2)
        glVertex3f(self.move_x + self.position_x +0, self.move_y + -1.5, -2)
        glEnd()

        # glColor3f(1.0, 1.0, 0)

        glBegin(GL_QUAD_STRIP)
        glTexCoord2f(0, 1)
        glVertex3f(self.move_x + self.position_x +0, self.move_y + -4, 0)
        glVertex3f(self.move_x + self.position_x +0, self.move_y + -1.5, -2)
        glVertex3f(self.move_x + self.position_x +2.5, self.move_y + -3, 0)
        glVertex3f(self.move_x + self.position_x +1, self.move_y + -2, -2)
        glVertex3f(self.move_x + self.position_x +3, self.move_y + 0, 0)
        glVertex3f(self.move_x + self.position_x +2, self.move_y + -1, -2)
        glVertex3f(self.move_x + self.position_x +3, self.move_y + 2, 0)
        glTexCoord2f(1, 1)
        glVertex3f(self.move_x + self.position_x +2, self.move_y + 0, -2)
        glVertex3f(self.move_x + self.position_x +2, self.move_y + 4, 0)
        glVertex3f(self.move_x + self.position_x +1.5, self.move_y + 1, -2)
        glVertex3f(self.move_x + self.position_x +-1, self.move_y + 5, 0)
        glVertex3f(self.move_x + self.position_x +0.5, self.move_y + 3, -2)
        glVertex3f(self.move_x + self.position_x +-3, self.move_y + 4, 0)
        glVertex3f(self.move_x + self.position_x +-0.5, self.move_y + 3, -2)
        glVertex3f(self.move_x + self.position_x +-2.5, self.move_y + 2, 0)
        glVertex3f(self.move_x + self.position_x +-0.2, self.move_y + 2, -2)
        glTexCoord2f(1, 0)
        glVertex3f(self.move_x + self.position_x +-4, self.move_y + 0, 0)
        glVertex3f(self.move_x + self.position_x +-1, self.move_y + 1, -2)
        glVertex3f(self.move_x + self.position_x +-3.5, self.move_y + -1.5, 0)
        glVertex3f(self.move_x + self.position_x +-2.5, self.move_y + 0, -2)
        glVertex3f(self.move_x + self.position_x +-2, self.move_y + -2, 0)
        glVertex3f(self.move_x + self.position_x +-1.5, self.move_y + -1, -2)
        glTexCoord2f(0, 0)
        glVertex3f(self.move_x + self.position_x +-1, self.move_y + -4, 0)
        glVertex3f(self.move_x + self.position_x +-0.5, self.move_y + 2, -2)
        glVertex3f(self.move_x + self.position_x +0, self.move_y + -4, 0)
        glVertex3f(self.move_x + self.position_x +0, self.move_y + -1.5, -2)
        glEnd()

        # glColor3f(1.0, 0, 0)
        glBegin(GL_QUAD_STRIP)
        glTexCoord2f(0, 1)
        glVertex3f(self.move_x + self.position_x +0, self.move_y + -4, 0)
        glVertex3f(self.move_x + self.position_x +0, self.move_y + -1.5, 2)
        glVertex3f(self.move_x + self.position_x +2.5, self.move_y + -3, 0)
        glVertex3f(self.move_x + self.position_x +1, self.move_y + -2, 2)
        glVertex3f(self.move_x + self.position_x +3, self.move_y + 0, 0)
        glVertex3f(self.move_x + self.position_x +2, self.move_y + -1, 2)
        glVertex3f(self.move_x + self.position_x +3, self.move_y + 2, 0)
        glTexCoord2f(1, 1)
        glVertex3f(self.move_x + self.position_x +2, self.move_y + 0, 2)
        glVertex3f(self.move_x + self.position_x +2, self.move_y + 4, 0)
        glVertex3f(self.move_x + self.position_x +1.5, self.move_y + 1, 2)
        glVertex3f(self.move_x + self.position_x +-1, self.move_y + 5, 0)
        glVertex3f(self.move_x + self.position_x +0.5, self.move_y + 3, 2)
        glVertex3f(self.move_x + self.position_x +-3, self.move_y + 4, 0)
        glVertex3f(self.move_x + self.position_x +-0.5, self.move_y + 3, 2)
        glVertex3f(self.move_x + self.position_x +-2.5, self.move_y + 2, 0)
        glTexCoord2f(1, 0)
        glVertex3f(self.move_x + self.position_x +-0.2, self.move_y + 2, 2)
        glVertex3f(self.move_x + self.position_x +-4, self.move_y + 0, 0)
        glVertex3f(self.move_x + self.position_x +-1, self.move_y + 1, 2)
        glVertex3f(self.move_x + self.position_x +-3.5, self.move_y + -1.5, 0)
        glVertex3f(self.move_x + self.position_x +-2.5, self.move_y + 0, 2)
        glVertex3f(self.move_x + self.position_x +-2, self.move_y + -2, 0)
        glTexCoord2f(0, 0)
        glVertex3f(self.move_x + self.position_x +-1.5, self.move_y + -1, 2)
        glVertex3f(self.move_x + self.position_x +-1, self.move_y + -4, 0)
        glVertex3f(self.move_x + self.position_x +-0.5, self.move_y + 2, 2)
        glVertex3f(self.move_x + self.position_x +0, self.move_y + -4, 0)
        glVertex3f(self.move_x + self.position_x +0, self.move_y + -1.5, 2)
        glEnd()

        # glColor3f(0, 1.0, 0)
        glBegin(GL_TRIANGLE_FAN)
        glTexCoord2f(0, 1)
        glVertex3f(self.move_x + self.position_x +0.5, self.move_y + 1, 3)
        glVertex3f(self.move_x + self.position_x +0, self.move_y + -1.5, 2)
        glVertex3f(self.move_x + self.position_x +1, self.move_y + -2, 2)
        glVertex3f(self.move_x + self.position_x +2, self.move_y + -1, 2)
        glTexCoord2f(1, 1)
        glVertex3f(self.move_x + self.position_x +2, self.move_y + 0, 2)
        glVertex3f(self.move_x + self.position_x +1.5, self.move_y + 1, 2)
        glVertex3f(self.move_x + self.position_x +0.5, self.move_y + 3, 2)
        glVertex3f(self.move_x + self.position_x +-0.5, self.move_y + 3, 2)
        glTexCoord2f(1, 0)
        glVertex3f(self.move_x + self.position_x +-0.2, self.move_y + 2, 2)
        glVertex3f(self.move_x + self.position_x +-1, self.move_y + 1, 2)
        glVertex3f(self.move_x + self.position_x +-2.5, self.move_y + 0, 2)
        glTexCoord2f(0, 0)
        glVertex3f(self.move_x + self.position_x +-1.5, self.move_y + -1, 2)
        glVertex3f(self.move_x + self.position_x +-0.5, self.move_y + 2, 2)
        glVertex3f(self.move_x + self.position_x +0, self.move_y + -1.5, 2)
        glEnd()

        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    # Define como é feito o movimento para a direita do asteroide
    def move_right(self):
        self.move_x += 3

    # Define como é feito o movimento para a esquerda do asteroide
    def move_left(self):
        self.move_x -= 3

    # Define como é feito o movimento para baixo
    def move_down(self):
        self.move_y -= 1

    # Checa se o asteroide morreu / saiu da tela
    def check_dead(self):
        self.check_range()

    def spin(self):
        if self.angle >= 350:
            self.angle = 0
        self.angle += 10

    #  Define a ação a ser feita
    def act(self):
        self.move_down()
        self.spin()

    # Checa se o asteroide saiu da tela
    def check_range(self):
        if self.move_y <= -90:
            self.dead = True

    # Retorna uma tupla do tipo (x1 , x2)
    def get_x(self):
        return (self.move_x + self.position_x -4.0,
                self.move_x + self.position_x + 4.0)

    # Retorna uma tupla do tipo (y1 , y2)
    def get_y(self):
        return (self.move_y - 4, self.move_y + 4)

    # Retorna uma tupla do tipo (z1 , z2)
    def get_z(self):
        return -1, 1

    # Carrega os valores do objeto
    def load(self, initial_position_x):
        self.dead = False
        self.move_x = 0
        self.move_y = 50
        self.position_x = initial_position_x
        self.angle = 0