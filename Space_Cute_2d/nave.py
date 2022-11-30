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
from propellant import Propellant

# Classe
# A posição x da nave do player é definida por
#         self.move_x + self.position_x
# A posição y da nave é fixa


class Nave():
    # Inicia os parametros
    # self.dead = indica se o objeto deve ser desenhado
    # self.move_x = controla o movimento executado pela nave
    # self.position_x = indica a posição x inicial da nave
    # self.imageID = variavel para a textura da nave
    # self.propellant = Objeto "propulsor" da nave

    def __init__(self, propellant_anim, initial_position):
        self.dead = False
        self.move_x = 0
        self.moving_left = False
        self.moving_right = False
        self.shooting = False
        self.speed = 0
        self.position_x = initial_position
        self.imageID = self.loadImage()
        self.propellant = Propellant(propellant_anim, self.position_x, -43.3, "player")

    # Carrega a imagem da nave do player
    def loadImage(self, imageName="img/nave2.png"):
        im = Image.open(imageName)
        ix, iy, image = im.size[0], im.size[1], im.tobytes()
        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0,GL_RGBA, GL_UNSIGNED_BYTE, image)
        return ID

    # Descreve como o objeto deve ser desenhado
    def draw(self):
        self.propellant.draw()

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
        glVertex3f(self.move_x + self.position_x - 4.0,
                   -40.0, 1)
        glTexCoord2f(1, 1)
        glVertex3f(self.move_x + self.position_x + 4.0,
                   -40.0, 1)
        glTexCoord2f(1, 0)

        glVertex3f(self.move_x + self.position_x + 4.0,
                   -28.0, 1)
        glTexCoord2f(0, 0)
        glVertex3f(self.move_x + self.position_x - 4.0,
                   -28.0, 1)
        glEnd()

        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    # Define como é feito o movimento para a direita da nave
    # e verifica se o movimento pode ser feito
    def move_right(self):
        if self.move_x + self.position_x <= 43:
            self.move_x += 1.5 + self.speed
            self.propellant.move_me(1.5 + self.speed, 0)

    # Define como é feito o movimento para a esquerda da nave
    # e verifica se o movimento pode ser feito
    def move_left(self):
        if self.move_x + self.position_x >= -43:
            self.move_x -= 1.5 + self.speed
            self.propellant.move_me(-(1.5 +self.speed) , 0)

    def check_dead(self):
        pass

    def act(self):
        if self.moving_left:
            self.move_left()
        if self.moving_right:
            self.move_right()

    # Retorna uma tupla do tipo (x1 , x2)
    def get_x(self):
        return (self.move_x + self.position_x -4.0, self.move_x + self.position_x + 4.0)

    # Retorna uma tupla do tipo (y1 , y2)
    def get_y(self):
        return (-46.0, -34.0)