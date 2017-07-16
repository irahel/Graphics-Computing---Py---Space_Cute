# Imports
from random import randint

from OpenGL.GL import glRotate
from OpenGL.GL.exceptional import glGenTextures, glTexParameter, glBegin, glEnd
from OpenGL.raw.GL.VERSION.GL_1_0 import glPixelStorei, glColor3f, glDisable, glEnable, glTexEnvi, glPushMatrix, \
    glTexCoord2f, glVertex3f, glPopMatrix
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_QUADS, glBindTexture, GL_TEXTURE_2D, GL_UNPACK_ALIGNMENT, GL_RGBA, \
    GL_LIGHTING, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE, GL_LINEAR, GL_TEXTURE_MIN_FILTER, \
    GL_TEXTURE_MAG_FILTER, GL_TRIANGLES
from propellant import Propellant

# Constantes
# Facilia a visualização
DIRECTION_RIGHT = True
DIRECTION_LEFT = False

# Classe
class Enemy():
    # Inicia os parametros
    # self.dead = define se o objeto deve ser desenhado
    # self.move_x = controla o movimento no eixo x
    # self.move_y = controla o movimento no eixo y, inicia fora da tela (70)
    # self.position_x = define a posição inical do inimigo
    # self.beahavior = define o comportamento sobre a movimentação do inimigo
    # self.skin_* = Texturas pre carregadas
    # self.ran_zigzag = define o alcance do movimento em zig zag
    # self.current_direction = indica a direção atual que ele está
    # self.elapsed_shoot_time = indica o tempo desde o ultimo tiro
    # self.nave_type = Textura da nave
    # self.shoot_type_rand = define a quantidade de tiros que o inimigo pode atirar
    # self.propellant = Objeto "propulsor" da nave
    def __init__(self, propelant_anim = None, initial_position_x = 0, nave_azul = None, nave_preta = None, nave_amarela = None):
        self.dead = False
        self.move_x = 0
        self.move_y = 70
        self.position_x = initial_position_x
        self.behavior = self.rand_behavior()
        self.skin_azul = nave_azul
        self.skin_amarela = nave_amarela
        self.skin_preta = nave_preta
        if self.behavior == "ZigZag":
            self.rand_zigzag_range = randint(8, 40)
            self.zig_x_1 = self.move_x + self.position_x - self.rand_zigzag_range
            self.zig_x_2 = self.move_x + self.position_x + self.rand_zigzag_range
        self.current_direction = DIRECTION_RIGHT
        self.elapsed_shoot_time = 0
        self.nave_type = randint(0, 2)

        self.shoot_type_rand = randint(1,10)
        if self.shoot_type_rand >= 1 and self.shoot_type_rand <=5:
            self.shoot_type = 1
        elif self.shoot_type_rand >= 6 and self.shoot_type_rand <=8:
            self.shoot_type = 2
        else:
            self.shoot_type = 3

        self.propellant = Propellant(propelant_anim, self.position_x, self.move_y + 12, "enemy")
        self.moving_right = False
        self.moving_left = False

    # Descreve como o objeto deve ser desenhado
    def draw(self):
        # self.propellant.draw()
        #
        glColor3f(1.0, 1.0, 1.0)
        # glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        if self.nave_type == 0:
            glBindTexture(GL_TEXTURE_2D, self.skin_azul)
        elif self.nave_type == 1:
            glBindTexture(GL_TEXTURE_2D, self.skin_amarela)
        elif self.nave_type == 2:
            glBindTexture(GL_TEXTURE_2D, self.skin_preta)

        glPushMatrix()

        # glBegin(GL_QUADS)
        # glTexCoord2f(0, 1)
        # glVertex3f(self.move_x + self.position_x -4.0,
        #            self.move_y, 0)
        # glTexCoord2f(1, 1)
        # glVertex3f(self.move_x + self.position_x +4.0,
        #            self.move_y, 0)
        # glTexCoord2f(1, 0)
        #
        # glVertex3f(self.move_x + self.position_x + 4.0,
        #            self.move_y + 12, 0)
        # glTexCoord2f(0, 0)
        # glVertex3f(self.move_x + self.position_x - 4.0,
        #            self.move_y + 12, 0)
        # glEnd()

        if self.moving_right:
            glRotate(10, 0.1, 0.7, 0.2)
        elif self.moving_left:
            glRotate(-10, 0.1, 0.7, 0.2)


        #Vermelho, baixo
        glBegin(GL_TRIANGLES)
        # glColor3f(1.0, 0.0, 0.0)
        glTexCoord2f(0, 1)
        glTexCoord2f(1, 1)
        glVertex3f(self.move_x + self.position_x + 5.0, self.move_y + 12, -2.0)
        glTexCoord2f(1, 0)
        glVertex3f(self.move_x + self.position_x + 0.0, self.move_y, 0.0)
        glTexCoord2f(0, 0)
        glVertex3f(self.move_x + self.position_x - 5.0, self.move_y + 12, -2.0)
        glEnd()
        # VERDE esq
        glBegin(GL_TRIANGLES)
        # glColor3f(0.0, 1.0, 0.0)
        glTexCoord2f(0, 1)
        glTexCoord2f(1, 1)
        glVertex3f(self.move_x + self.position_x - 5.0, self.move_y + 12, -2.0)
        glTexCoord2f(1, 0)
        glVertex3f(self.move_x + self.position_x + 0.0, self.move_y, 0.0)
        glTexCoord2f(0, 0)
        glVertex3f(self.move_x + self.position_x + 0.0, self.move_y + 12, 2.0)
        glEnd()
        #############3 Azul escuro dir
        glBegin(GL_TRIANGLES)
        # glColor3f(0.5, 0.5, 1.0)
        glTexCoord2f(0, 1)
        glTexCoord2f(1, 1)
        glVertex3f(self.move_x + self.position_x + 5.0, self.move_y + 12, -2.0)
        glTexCoord2f(1, 0)
        glVertex3f(self.move_x + self.position_x + 0.0, self.move_y, 0.0)
        glTexCoord2f(0, 0)
        glVertex3f(self.move_x + self.position_x + 0.0, self.move_y + 12, 2.0)
        glEnd()
        #####################Roxo FRENTE
        glBegin(GL_TRIANGLES)
        # glColor3f(0.0, 0.0, 1.0)
        glTexCoord2f(0, 1)
        glTexCoord2f(1, 1)
        glVertex3f(self.move_x + self.position_x + 0.0, self.move_y + 12, 2.0)
        glTexCoord2f(1, 0)
        glVertex3f(self.move_x + self.position_x + 5.0, self.move_y + 12, -2.0)
        glTexCoord2f(0, 0)
        glVertex3f(self.move_x + self.position_x - 5.0, self.move_y + 12, -2.0)
        glEnd()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    # Define como é feito o movimento para a direita da nave
    def move_right(self):
        self.move_x += 0.7
        self.propellant.move_me(0.7, 0)

    # Define como é feito o movimento para a esquerda da nave
    def move_left(self):
        self.move_x -= 0.7
        self.propellant.move_me(-0.7, 0)

    # Define como é feito o movimento para baixo da nave
    def move_down(self):
        self.move_y -= 0.5
        self.propellant.move_me(0, -0.5)

    # Checa se a nave morreu / saiu da tela
    def check_dead(self):
        self.check_range()

    # Define a forma que a nave se move
    def move_yourself(self):
        if self.behavior == "Vertical":
            self.move_down()
        elif self.behavior == "Diagonal":
            self.check_max(-49, 49)
            if self.current_direction == DIRECTION_RIGHT:
                self.moving_right = True
                self.moving_left = False
                self.move_right()
                self.move_down()
            elif self.current_direction == DIRECTION_LEFT:
                self.moving_right = False
                self.moving_left = True
                self.move_left()
                self.move_down()
        elif self.behavior == "ZigZag":
            self.check_max(self.zig_x_1, self.zig_x_2)
            if self.current_direction == DIRECTION_RIGHT:
                self.moving_right = True
                self.moving_left = False
                self.move_right()
                self.move_down()
            elif self.current_direction == DIRECTION_LEFT:
                self.moving_right = False
                self.moving_left = True
                self.move_left()
                self.move_down()

    #  Define a ação a ser feita
    def act(self):
        self.move_yourself()

    # Checa se a nave bateu no alcance minimo ou maximo
    def check_max(self, min_range, max_range):
        if self.move_x + self.position_x -4.0 <= min_range:
            self.current_direction = DIRECTION_RIGHT
        elif self.move_x + self.position_x + 4.0 >= max_range:
            self.current_direction = DIRECTION_LEFT

    # Checa se a nave está fora da tela
    def check_range(self):
        if self.move_y <= -90:
            self.dead = True
            self.propellant.im_dead()

    # Retorna uma tupla do tipo (x1 , x2)
    def get_x(self):
        return self.move_x + self.position_x - 5.0, \
            self.move_x + self.position_x + 5.0

    # Retorna uma tupla do tipo (y1 , y2)
    def get_y(self):
        return self.move_y, self.move_y + 12.0

    # Retorna uma tupla do tipo (z1 , z2)
    def get_z(self):
        return -2, 2

    # Retorna um comportamento randomico
    def rand_behavior(self):
        choice = randint(0,91)
        if choice <= 30:
            return "Diagonal"
        elif choice >= 31 and choice <= 60:
            return "Vertical"
        elif choice >= 61 and choice <= 90:
            return "ZigZag"
        else:
            return "Daniel"

    # Carrega os valores do objeto
    def load(self,initial_position_x , propellant_anim, nave_azul, nave_amarela, nave_preta):
        self.dead = False
        self.move_x = 0
        self.move_y = 70
        self.position_x = initial_position_x
        self.skin_azul = nave_azul
        self.skin_amarela = nave_amarela
        self.skin_preta = nave_preta
        self.behavior = self.rand_behavior()
        if self.behavior == "ZigZag":
            self.rand_zigzag_range = randint(8, 40)
            self.zig_x_1 = self.move_x + self.position_x - self.rand_zigzag_range
            self.zig_x_2 = self.move_x + self.position_x + self.rand_zigzag_range
        self.current_direction = DIRECTION_RIGHT
        self.elapsed_shoot_time = 0
        self.nave_type = randint(0, 2)

        self.shoot_type_rand = randint(1, 10)
        if 1 <= self.shoot_type_rand <= 5:
            self.shoot_type = 1
        elif 6 <= self.shoot_type_rand <= 8:
            self.shoot_type = 2
        else:
            self.shoot_type = 3

        self.propellant = Propellant(propellant_anim, self.position_x, self.move_y + 16.7, "enemy")
        self.moving_right = False
        self.moving_left = False
