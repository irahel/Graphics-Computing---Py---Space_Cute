# Imports
from OpenGL.GL import glRotate, glTranslate
from OpenGL.GL.exceptional import glGenTextures, glTexParameter, glBegin, glEnd
from OpenGL.GL.images import glTexImage2D
from OpenGL.raw.GL.VERSION.GL_1_0 import glPixelStorei, glColor3f, glDisable, glEnable, glTexEnvi, glPushMatrix, \
    glTexCoord2f, glVertex3f, glPopMatrix, glMatrixMode, glLoadIdentity
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_QUADS, glBindTexture, GL_TEXTURE_2D, GL_UNPACK_ALIGNMENT, GL_RGBA, \
    GL_LIGHTING, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE, GL_LINEAR, GL_TEXTURE_MIN_FILTER, \
    GL_TEXTURE_MAG_FILTER, GL_TRIANGLE_STRIP, GL_TRIANGLES, GL_LINES, GL_TRIANGLE_FAN, GL_QUAD_STRIP, GL_PROJECTION, \
    GL_MODELVIEW
from OpenGL.raw.GL._types import GL_UNSIGNED_BYTE
from OpenGL.raw.GLU import gluPerspective, gluLookAt
from PIL import Image

# Classe
# A posição x da nave do player é definida por
#         self.move_x + self.position_x
# A posição y da nave é fixa


class Nave:
    # Inicia os parametros
    # self.dead = indica se o objeto deve ser desenhado
    # self.move_x = controla o movimento executado pela nave
    # self.position_x = indica a posição x inicial da nave
    # self.imageID = variavel para a textura da nave

    def __init__(self, initial_position):
        self.dead = False
        self.move_x = 0
        self.move_y = 0
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.shooting = False
        self.speed = 0
        self.position_x = initial_position
        self.casco = self.loadImage("img/nave/casco.png")
        self.vidro = self.loadImage("img/nave/cook.png")
        self.metal = self.loadImage("img/nave/metal.png")
        self.xizi = 0
        self.yizi = 42
        self.angle = 0

    # Carrega a imagem da nave do player
    def loadImage(self, imageName):
        im = Image.open(imageName)
        ix, iy, image = im.size[0], im.size[1], im.tobytes()
        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0,GL_RGBA, GL_UNSIGNED_BYTE, image)
        return ID

    # Descreve como o objeto deve ser desenhado
    def draw(self):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(45, 1.65, 0.1, 500)
        gluLookAt(self.xizi, self.yizi-50, 3.9,
                  self.xizi, self.yizi, 0,
                  0, 1, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # glRotate(20, 0, 0, 1)
        glPushMatrix()
        # glBindTexture(GL_TEXTURE_2D, self.casco)
        #
        # #Base da nave
        # glBegin(GL_TRIANGLE_FAN)
        # glTexCoord2f(0, 1)
        # glVertex3f(self.move_x + 0, self.move_y + 0, 1)
        # glTexCoord2f(1, 1)
        # glVertex3f(self.move_x + 0, self.move_y + 6, 1)
        # glTexCoord2f(1, 0)
        # glVertex3f(self.move_x + 1.5, self.move_y + 3, 1)
        # glTexCoord2f(0, 0)
        # glVertex3f(self.move_x + 2, self.move_y + 0, 1)
        # glTexCoord2f(0, 1)
        # glVertex3f(self.move_x + 5, self.move_y - 6, 1)
        # glTexCoord2f(1, 1)
        # glVertex3f(self.move_x + 2, self.move_y - 7, 1)
        # glTexCoord2f(1, 0)
        # glVertex3f(self.move_x + 1, self.move_y - 7, 1)
        # glTexCoord2f(1, 1)
        # glVertex3f(self.move_x + 0, self.move_y - 8, 1)
        # glTexCoord2f(1, 0)
        # glVertex3f(self.move_x - 1, self.move_y - 7, 1)
        # glTexCoord2f(0, 0)
        # glVertex3f(self.move_x - 2, self.move_y - 7, 1)
        # glTexCoord2f(0, 1)
        # glVertex3f(self.move_x - 5, self.move_y - 6, 1)
        # glTexCoord2f(1, 1)
        # glVertex3f(self.move_x - 2, self.move_y + 0, 1)
        # glTexCoord2f(1, 0)
        # glVertex3f(self.move_x - 1.5, self.move_y + 3, 1)
        # glTexCoord2f(0, 0)
        # glVertex3f(self.move_x + 0, self.move_y + 6, 1)
        # glEnd()
        #
        # #Casco da nave (fora)
        # glBegin(GL_QUAD_STRIP)
        # glTexCoord2f(0, 1)
        # glVertex3f(self.move_x + 0, self.move_y + 6, 1)
        # glVertex3f(self.move_x + 0, self.move_y + 3, 2)
        # glVertex3f(self.move_x + 1.5, self.move_y + 3, 1)
        # glVertex3f(self.move_x + 0.5, self.move_y + 2, 2)
        # glVertex3f(self.move_x + 2, self.move_y + 0, 1)
        # glVertex3f(self.move_x + 1, self.move_y + 0, 2)
        # glVertex3f(self.move_x + 5, self.move_y - 6, 1)
        # glVertex3f(self.move_x + 2, self.move_y - 4, 2)
        # glTexCoord2f(1, 1)
        # glVertex3f(self.move_x + 2, self.move_y - 7, 1)
        # glVertex3f(self.move_x + 1, self.move_y - 6, 2)
        # glVertex3f(self.move_x + 1, self.move_y - 7, 1)
        # glVertex3f(self.move_x + 0.5, self.move_y - 6, 2)
        # glVertex3f(self.move_x + 0, self.move_y - 8, 1)
        # glVertex3f(self.move_x + 0, self.move_y - 7, 2)
        # glVertex3f(self.move_x - 1, self.move_y - 7, 1)
        # glTexCoord2f(1, 0)
        # glVertex3f(self.move_x - 0.5, self.move_y - 6, 2)
        # glVertex3f(self.move_x - 2, self.move_y - 7, 1)
        # glVertex3f(self.move_x - 1, self.move_y - 6, 2)
        # glVertex3f(self.move_x - 5, self.move_y - 6, 1)
        # glVertex3f(self.move_x - 2, self.move_y - 4, 2)
        # glVertex3f(self.move_x - 2, self.move_y + 0, 1)
        # glTexCoord2f(0, 0)
        # glVertex3f(self.move_x - 1, self.move_y + 0, 2)
        # glVertex3f(self.move_x - 1.5, self.move_y + 3, 1)
        # glVertex3f(self.move_x - 0.5, self.move_y + 2, 2)
        # glVertex3f(self.move_x + 0, self.move_y + 6, 1)
        # glVertex3f(self.move_x + 0, self.move_y + 3, 2)
        # glEnd()
        #
        # glDisable(GL_TEXTURE_2D)
        #
        # glColor3f(1.0, 1.0, 1.0)
        # glDisable(GL_LIGHTING)
        # glEnable(GL_TEXTURE_2D)
        #
        # glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        # glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        # glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        #
        # glBindTexture(GL_TEXTURE_2D, self.metal)
        #
        # #Parte verde
        # glBegin(GL_QUAD_STRIP)
        # glTexCoord2f(0, 1)
        # glVertex3f(self.move_x + 0, self.move_y + 3, 2)
        # glVertex3f(self.move_x + 0, self.move_y + 2, 2.5)
        # glVertex3f(self.move_x + 0.5, self.move_y + 2, 2)
        # glVertex3f(self.move_x + 0.5, self.move_y + 1, 2.5)
        # glVertex3f(self.move_x + 1, self.move_y + 0, 2)
        # glVertex3f(self.move_x + 0.5, self.move_y + 0, 2.5)
        # glVertex3f(self.move_x + 2, self.move_y - 4, 2)
        # glTexCoord2f(1, 1)
        # glVertex3f(self.move_x + 1, self.move_y - 4, 2.5)
        # glVertex3f(self.move_x + 1, self.move_y - 6, 2)
        # glVertex3f(self.move_x + 1, self.move_y - 5, 2.5)
        # glVertex3f(self.move_x + 0.5, self.move_y - 6, 2)
        # glVertex3f(self.move_x + 0.5, self.move_y - 5, 2.5)
        # glVertex3f(self.move_x + 0, self.move_y - 7, 2)
        # glVertex3f(self.move_x + 0, self.move_y - 5, 2.5)
        # glVertex3f(self.move_x - 0.5, self.move_y - 6, 2)
        # glTexCoord2f(1, 0)
        # glVertex3f(self.move_x - 0.5, self.move_y - 5, 2.5)
        # glVertex3f(self.move_x - 1, self.move_y - 6, 2)
        # glVertex3f(self.move_x - 1, self.move_y - 5, 2.5)
        # glVertex3f(self.move_x - 2, self.move_y - 4, 2)
        # glVertex3f(self.move_x - 1, self.move_y - 4, 2.5)
        # glVertex3f(self.move_x - 1, self.move_y + 0, 2)
        # glTexCoord2f(0, 0)
        # glVertex3f(self.move_x - 0.5, self.move_y + 0, 2.5)
        # glVertex3f(self.move_x - 0.5, self.move_y + 2, 2)
        # glVertex3f(self.move_x - 0.5, self.move_y + 1, 2.5)
        # glVertex3f(self.move_x + 0, self.move_y + 3, 2)
        # glVertex3f(self.move_x + 0, self.move_y + 2, 2.5)
        # glEnd()
        #
        # glDisable(GL_TEXTURE_2D)
        #
        # glColor3f(1.0, 1.0, 1.0)
        # glEnable(GL_TEXTURE_2D)
        #
        # glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        # glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        # glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # glBindTexture(GL_TEXTURE_2D, self.vidro)
        #
        # #Mira
        #
        # glDisable(GL_TEXTURE_2D)
        glColor3f(1, 0, 0)

        glBegin(GL_LINES)
        glVertex3f(self.move_x + 0, self.move_y + 70, 3)
        glVertex3f(self.move_x + 0, self.move_y + 70, -3)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(self.move_x + 3, self.move_y + 70, 0)
        glVertex3f(self.move_x + -3, self.move_y + 70, 0)
        glEnd()
        glPopMatrix()


        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, self.vidro)

        #Cookpit
        # glPushMatrix()
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(self.move_x+ -11, self.move_y +6.9, 9.5)
        glTexCoord2f(1, 0)
        glVertex3f(self.move_x+ 11, self.move_y +6.9, 9.5)
        glTexCoord2f(1, 1)
        glVertex3f(self.move_x+ 11, self.move_y +6.9, -4)
        glTexCoord2f(0, 1)
        glVertex3f(self.move_x+ -11, self.move_y +6.9, -4)
        # glTexCoord2f(0, 1)
        # glVertex3f(self.move_x+ -50, self.move_y +50, 50)
        # glTexCoord2f(1, 1)
        # glVertex3f(self.move_x+ 50, self.move_y +50, 50)
        # glTexCoord2f(1, 0)
        # glVertex3f(self.move_x+ 50, self.move_y +-50, -50)
        # glTexCoord2f(0, 0)
        # glVertex3f(self.move_x+ -50, self.move_y +-50, -50)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        # glPopMatrix

    # Define como é feito o movimento para a direita da nave
    # e verifica se o movimento pode ser feito
    def move_right(self):
        if self.move_x + self.position_x <= 43:
            self.move_x += 1.5 + self.speed
            self.xizi += 1.5 + self.speed
            self.angle = -20

    # Define como é feito o movimento para a esquerda da nave
    # e verifica se o movimento pode ser feito
    def move_left(self):
        if self.move_x + self.position_x >= -43:
            self.move_x -= 1.5 + self.speed
            self.xizi -= 1.5 + self.speed
            self.angle = 20

    # Define como é feito o movimento para a cima da nave
    # e verifica se o movimento pode ser feito
    def move_up(self):
        if self.move_y <= 39:
            self.move_y += 1.5 + self.speed
            self.yizi += 1.5 + self.speed

    # Define como é feito o movimento para a baixo da nave
    # e verifica se o movimento pode ser feito
    def move_down(self):
        if self.move_y >= -39:
            self.move_y -= 1.5 + self.speed
            self.yizi -= 1.5 + self.speed

    def check_dead(self):
        pass

    def act(self):
        if self.moving_left:
            self.move_left()
        if self.moving_right:
            self.move_right()
        if self.moving_up:
            self.move_up()
        if self.moving_down:
            self.move_down()
        if not self.moving_left and not self.moving_right:
            self.angle = 0

    # Retorna uma tupla do tipo (x1 , x2)
    def get_x(self):
        return self.move_x - 5.0, self.move_x + 5.0

    # Retorna uma tupla do tipo (y1 , y2)
    def get_y(self):
        return self.move_y + 8.0, self.move_y - 8.0

    # Retorna uma tupla do tipo (z1 , z2)
    def get_z(self):
        return -3, 3
