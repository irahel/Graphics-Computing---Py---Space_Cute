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


#Classe
class Flor():
    # Inicia os parametros
    # self.move_y = Indica a movimentacao no eixo y
    # self.dead = Indica se o objeto deve ser desenhado
    # self.start_position_x = Posicao inical do objeto no eixo x
    # self.start_position_y = Posicao inicial do objeto no eixo y (y1)
    # self.start_position_y_2 = Posicao inicial do objeto no eixo y (y2)
    # self.skin = randint(0, 2) = Define a textura da "flor"
    # self.imageID = Textura carregada
    def __init__(self, position_x_nave = None):
        self.move_y = 0
        self.dead = False
        self.start_position_x = position_x_nave
        self.start_position_y = 50
        self.start_position_y_2 = 90
        self.skin = randint(0,2)
        self.imageID = self.loadImage()

    # Carrega a textura
    def loadImage(self):
        if self.skin == 0:
            im = Image.open("img/Flores1.png")
        elif self.skin == 1:
            im = Image.open("img/Flores2.png")
        elif self.skin == 2:
            im = Image.open("img/Flores3.png")

        ix, iy, image = im.size[0], im.size[1], im.tobytes()

        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, image
        )
        return ID

    # Define como o objeto deve ser desenhado
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
        glVertex3f(self.start_position_x -40,
                   self.move_y + self.start_position_y, 0)
        glTexCoord2f(1, 1)
        glVertex3f(self.start_position_x +40,
                   self.move_y + self.start_position_y , 0)
        glTexCoord2f(1, 0)

        glVertex3f(self.start_position_x + 40,
                   self.move_y + self.start_position_y_2, 0)
        glTexCoord2f(0, 0)
        glVertex3f(self.start_position_x -40,
                   self.move_y + self.start_position_y_2, 0)
        glEnd()

        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    # Move o objeto para baixo
    def move_down(self):
        self.move_y -= 0.5

    # Checa se o objeto esta fora da tela
    def check_range(self):
        if self.move_y + self.start_position_y_2 < -50:
            self.dead = True

    # Checa se o objeto morreu
    def check_dead(self):
        self.check_range()

    # Define o que sera feito pelo objeto
    def act(self):
        self.move_down()

    def get_x(self):
        pass

    def get_y(self):
        pass

    # Carrega as variaveis
    def load(self,position_x_nave):
        self.move_y = 0
        self.dead = False
        self.start_position_x = position_x_nave
        self.start_position_y = 50
        self.start_position_y_2 = 90
        self.skin = randint(0,2)
