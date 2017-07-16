# Imports
import math
from OpenGL.GL import glRotate
from OpenGL.GL.exceptional import glTexParameter, glBegin, glEnd
from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f, glDisable, glEnable, glTexEnvi, glPushMatrix, \
    glTexCoord2f, glVertex3f, glPopMatrix
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_QUADS, glBindTexture, GL_TEXTURE_2D, \
    GL_LIGHTING, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE, GL_LINEAR, GL_TEXTURE_MIN_FILTER, \
    GL_TEXTURE_MAG_FILTER


# Classe
class Shoot:
    # Inicia os parametros
    # self.move = Controla o movimento no eixo y
    # self.dead = Indica se o objeto deve ser desenhado
    # self.start_position_x = Indica a posicao inicial no eixo x
    # self.start_position_y = Indica a posicao inicial no eixo y, y1
    # self.start_position_y_2 = Indica a posicao inicial no eixo y, y2
    # self.is_enemy = Indica se o tiro e do inimigo ou do player
    # self.type = Indica o tipo de inimigo, para selecao de textura
    # self.imageID = Textura do tiro
    def __init__(self, image=None,  position_x_nave=None, position_y_1_nave=None , position_y_2_nave=None, type=None, type_enemy=None, initial_z = None, this_angle = None):
        self.move = 0
        self.dead = False
        self.start_position_x = position_x_nave
        self.start_position_y = position_y_1_nave
        self.start_position_y_2 = position_y_2_nave
        self.is_enemy = type
        self.type = type_enemy
        self.z = initial_z
        self.imageID = image
        self.angle = this_angle

    # Define como o objeto deve ser desenhado
    def draw(self):

        glColor3f(1.0, 1.0, 1.0)
        # glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, self.imageID)

        glPushMatrix()
        # if self.is_enemy:
        #     glRotate(self.angle, 0, 0, 1)
        #

        glBegin(GL_QUADS)

        # glColor3f(0.0, 0.0, 1.0)
        glTexCoord2f(0, 1)
        glVertex3f(self.start_position_x + 1.0, self.move + self.start_position_y_2, -1.0)
        glTexCoord2f(1, 1)
        glVertex3f(self.start_position_x - 1.0, self.move + self.start_position_y_2, -1.0)
        glTexCoord2f(1, 0)
        glVertex3f(self.start_position_x - 1.0, self.move + self.start_position_y_2, 1.0)
        glTexCoord2f(0, 0)
        glVertex3f(self.start_position_x + 1.0, self.move + self.start_position_y_2, 1.0)

        # glColor3f(0.0, 1.0, 1.0)
        glTexCoord2f(0, 1)
        glVertex3f(self.start_position_x + 1.0, self.move + self.start_position_y, 1.0)
        glTexCoord2f(1, 1)
        glVertex3f(self.start_position_x + -1.0, self.move + self.start_position_y, 1.0)
        glTexCoord2f(1, 0)
        glVertex3f(self.start_position_x + -1.0, self.move + self.start_position_y, -1.0)
        glTexCoord2f(0, 0)
        glVertex3f(self.start_position_x + 1.0, self.move + self.start_position_y, -1.0)

        # glColor3f(1.0, 0.0, 0.0)
        glTexCoord2f(0, 1)
        glVertex3f(self.start_position_x + 1.0, self.move + self.start_position_y_2, 1.0)
        glTexCoord2f(1, 1)
        glVertex3f(self.start_position_x + -1.0, self.move + self.start_position_y_2, 1.0)
        glTexCoord2f(1, 0)
        glVertex3f(self.start_position_x + -1.0, self.move + self.start_position_y, 1.0)
        glTexCoord2f(0, 0)
        glVertex3f(self.start_position_x + 1.0, self.move + self.start_position_y, 1.0)

        # glColor3f(0.0, 1.0, 0.0)
        glTexCoord2f(0, 1)
        glVertex3f(self.start_position_x + 1.0, self.move + self.start_position_y, -1.0)
        glTexCoord2f(1, 1)
        glVertex3f(self.start_position_x + -1.0, self.move + self.start_position_y, -1.0)
        glTexCoord2f(1, 0)
        glVertex3f(self.start_position_x + -1.0, self.move + self.start_position_y_2, -1.0)
        glTexCoord2f(0, 0)
        glVertex3f(self.start_position_x + 1.0, self.move + self.start_position_y_2, -1.0)

        # glColor3f(1.0, 1.0, 0.0)
        glTexCoord2f(0, 1)
        glVertex3f(self.start_position_x + -1.0, self.move + self.start_position_y_2, 1.0)
        glTexCoord2f(1, 1)
        glVertex3f(self.start_position_x + -1.0, self.move + self.start_position_y_2, -1.0)
        glTexCoord2f(1, 0)
        glVertex3f(self.start_position_x + -1.0, self.move + self.start_position_y, -1.0)
        glTexCoord2f(0, 0)
        glVertex3f(self.start_position_x + -1.0, self.move + self.start_position_y, 1.0)

        # glColor3f(1.0, 0.0, 1.0)
        glTexCoord2f(0, 1)
        glVertex3f(self.start_position_x+ 1.0, self.move + self.start_position_y_2, -1.0)
        glTexCoord2f(1, 1)
        glVertex3f(self.start_position_x + 1.0, self.move + self.start_position_y_2, 1.0)
        glTexCoord2f(1, 0)
        glVertex3f(self.start_position_x + 1.0, self.move + self.start_position_y, 1.0)
        glTexCoord2f(0, 0)
        glVertex3f(self.start_position_x + 1.0, self.move + self.start_position_y, -1.0)

        glEnd()

        glPopMatrix()

        glDisable(GL_TEXTURE_2D)

    # Faz a movimentacao para cima
    def move_up(self):
        self.move += 3

    # Faz a movimentacao para baixo
    def move_down(self):
        self.move -= 3

    # Checa se o tiro esta fora da tela
    def check_range(self):
        if self.is_enemy == True:
            if self.move + self.start_position_y < -50 :
                self.dead = True
        elif self.is_enemy == False:
            if self.move + self.start_position_y_2 > 50:
                self.dead = True

    # Checa se o tiro esta morto
    def check_dead(self):
        self.check_range()

    # Define a acao que deve ser feita
    def act(self):
        if self.is_enemy == True:
            self.move_down()
        else:
            self.move_up()

    # Retorna uma tupla do tipo (x1 , x2)
    def get_x(self):
        return (self.start_position_x -1, self.start_position_x +1)

    # Retorna uma tupla do tipo (y1 , y2)
    def get_y(self):
        return ( self.move + self.start_position_y, self.move + self.start_position_y_2 + 9)

    # Retorna uma tupla do tipo (z1 , z2)
    def get_z(self):
        return -1, 1

    # Carrega as variaveis
    def load(self,image, position_x_nave , position_y_1_nave, position_y_2_nave, type, type_enemy, initial_z, this_angle):
        self.move = 0
        self.dead = False
        self.start_position_x = position_x_nave
        self.start_position_y = position_y_1_nave
        self.start_position_y_2 = position_y_2_nave
        self.is_enemy = type
        self.type = type_enemy
        self.z = initial_z
        self.imageID = image
        self.angle = this_angle
