# Imports
from OpenGL.GL.exceptional import glGenTextures, glTexParameter, glBegin, glEnd
from OpenGL.GL.images import glTexImage2D
from OpenGL.raw.GL.VERSION.GL_1_0 import glPixelStorei, glColor3f, glDisable, glEnable, glTexEnvi, glPushMatrix, \
    glTexCoord2f, glVertex3f, glPopMatrix
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_QUADS, glBindTexture, GL_TEXTURE_2D, GL_UNPACK_ALIGNMENT, GL_RGBA, \
    GL_LIGHTING, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE, GL_LINEAR, GL_TEXTURE_MIN_FILTER, \
    GL_TEXTURE_MAG_FILTER
from OpenGL.raw.GL._types import GL_UNSIGNED_BYTE
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

    # Carrega a textura
    def loadImage(self):

        im = Image.open("img/asteroide.png")

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
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, self.imageID)

        glPushMatrix()

        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex3f(self.move_x + self.position_x -4.0,
                   self.move_y, 0)
        glTexCoord2f(1, 1)
        glVertex3f(self.move_x + self.position_x +4.0,
                   self.move_y, 0)
        glTexCoord2f(1, 0)

        glVertex3f(self.move_x + self.position_x + 4.0,
                   self.move_y + 10, 0)
        glTexCoord2f(0, 0)
        glVertex3f(self.move_x + self.position_x -4.0,
                   self.move_y + 10, 0)
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

    #  Define a ação a ser feita
    def act(self):
        self.move_down()

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
        return (self.move_y, self.move_y + 10)

    # Carrega os valores do objeto
    def load(self, initial_position_x):
        self.dead = False
        self.move_x = 0
        self.move_y = 50
        self.position_x = initial_position_x