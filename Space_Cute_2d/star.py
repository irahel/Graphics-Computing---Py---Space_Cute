# Imports
from random import randint
from OpenGL.GL.exceptional import glBegin, glEnd
from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f, glPushMatrix, \
    glVertex3f, glPopMatrix
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_TRIANGLE_FAN

# Classe
class Star:
    # Inicia os parametros
    # self.dead = define se o objeto deve ser desenhado
    # self.move_x = Posição x inicial
    # self.scale = Controla o tamanho da estrela
    # self.move_y = Controla o movimento no eixo y do objeto
    # self.speed = Indica a velocidade de queda
    def __init__(self ,position, scale):
        self.move_x = position
        self.scale = scale
        self.move_y = 55
        self.speed = self.rand_speed()
        self.dead = False

    # Descreve como o objeto deve ser desenhado
    def draw(self):
        glColor3f(1.0, 1.0, 1.0)

        glPushMatrix()

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(self.move_x + 0 * self.scale ,self.move_y + 0 * self.scale ,0)
        glVertex3f(self.move_x + 0 * self.scale, self.move_y + 2 * self.scale,0)
        glVertex3f(self.move_x + 1.5 * self.scale, self.move_y + 1.5 * self.scale, 0)
        glVertex3f(self.move_x + 2 * self.scale, self.move_y + 0 * self.scale, 0)
        glVertex3f(self.move_x + 1.5 * self.scale, self.move_y + -1.5 * self.scale, 0)
        glVertex3f(self.move_x + 0 * self.scale, self.move_y -2 * self.scale, 0)
        glVertex3f(self.move_x -1.5 * self.scale, self.move_y-1.5 * self.scale, 0)
        glVertex3f(self.move_x -2 * self.scale, self.move_y + 0 * self.scale, 0)
        glVertex3f(self.move_x -1.5 * self.scale, self.move_y + 1.5 * self.scale, 0)
        glVertex3f(self.move_x + 0 * self.scale, self.move_y + 2 * self.scale, 0)
        glEnd()

        glPopMatrix()

    # Define como é feito o movimento para baixo
    def move_down(self):
        self.move_y -= self.speed

    # Checa se a estrela saiu da tela
    def check_range(self):
        if self.move_y + 2 * self.scale < -50:
            self.dead = True

    # Checa se a estrela morreu
    def check_dead(self):
        self.check_range()

    #  Define a ação a ser feita
    def act(self):
        self.move_down()

    # Retorna uma tupla do tipo (x1 , x2)
    def get_x(self):
        pass

    # Retorna uma tupla do tipo (y1 , y2)
    def get_y(self):
        pass

    # Retorna um numero randomico para velocidade da estrela
    def rand_speed(self):
        return float(str(randint(0, 1)) +"."+ str(randint(3, 9)))