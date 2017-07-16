# Imports
from OpenGL.GL import glRotate
from OpenGL.GL.exceptional import glTexParameter, glBegin, glEnd
from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f, glDisable, glEnable, glTexEnvi, glPushMatrix, \
    glTexCoord2f, glVertex3f, glPopMatrix
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_QUADS, glBindTexture, GL_TEXTURE_2D, \
    GL_LIGHTING, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE, GL_LINEAR, GL_TEXTURE_MIN_FILTER, \
    GL_TEXTURE_MAG_FILTER

#Classe
class Logo:
    # Inicia os parametros
    # self.inited = Indica se esse objeto esta visivel
    # self.dead = Indica se esse objeto nao esta sendo desenhado
    # self.start_position_x = Define a posicao inicial no eixo x
    # self.start_position_y = Define a posicao inicial no eixo y
    # self.type = Define o tipo (inicio ou fim)
    # self.logo_inicio = Textura do inicio
    # self.logo_fim = Textura do fim
    def __init__(self, Type = None, Init = None, End = None):
        self.inited = False
        self.dead = False
        self.start_position_x = 0
        self.start_position_y = 0
        self.type = Type
        self.logo_inicio = Init
        self.logo_fim = End

    # Define como o objeto deve ser desenhado
    def draw(self):

        glColor3f(1.0, 1.0, 1.0)
        # glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        if self.type == "inicio":
            glBindTexture(GL_TEXTURE_2D, self.logo_inicio)
        elif self.type == "fim":
            glBindTexture(GL_TEXTURE_2D, self.logo_fim)

        glPushMatrix()
        glRotate (90, 1, 0 ,0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex3f(self.start_position_x -35,
                   self.start_position_y - 25, -70)
        glTexCoord2f(1, 1)
        glVertex3f(self.start_position_x +35,
                   self.start_position_y - 25, -70)
        glTexCoord2f(1, 0)

        glVertex3f(self.start_position_x + 35,
                   self.start_position_y + 25, -70)
        glTexCoord2f(0, 0)
        glVertex3f(self.start_position_x - 35,
                   self.start_position_y + 25, -70)
        glEnd()

        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    def check_range(self):
        pass

    def check_dead(self):
        pass

    def act(self):
        pass

    def get_x(self):
        pass

    def get_y(self):
        pass

    # Carrega as variaveis
    def load(self,Type, Init, End):
        self.inited = False
        self.dead = False
        self.start_position_x = 0
        self.start_position_y = 0
        self.type = Type
        self.logo_inicio = Init
        self.logo_fim = End