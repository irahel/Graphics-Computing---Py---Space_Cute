# Imports
from time import time
from OpenGL.GL.exceptional import glTexParameter
from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f, glDisable, glEnable, glTexEnvi, glPushMatrix, \
    glTexCoord2f, glVertex3f, glPopMatrix
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_QUADS, glBindTexture, GL_TEXTURE_2D, \
    GL_LIGHTING, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE, GL_LINEAR, GL_TEXTURE_MIN_FILTER, \
    GL_TEXTURE_MAG_FILTER
from OpenGL.GL.exceptional import glBegin, glEnd

# Constantes
# EXPLOSION_FRAME = Duracao de cada frame
# EXPLOSION_FRAMES = Quantidade de frames da explosao
EXPLOSION_FRAME = 0.045
EXPLOSION_FRAMES = 27


#Classe
class Explode:
    # Inicia os parametros
    # self.start = Tempo em que foi iniciado
    # self.quadro = Quadro atual
    # self.type = Tipo (Player ou inimigo (Muda a orientacao) )
    # self.x = Posicao no eixo x
    # self.y = Posicao no eixo y
    # self.dead = Indica se o objeto deve ser desenhado
    # self.imgs = Vetor com texturas
    def __init__(self, images = None, x = None, y = None, Type = "player"):
        self.start = time()
        self.quadro = 0
        self.type = Type
        self.x = x
        self.y = y
        self.dead = False
        self.imgs = images

    # Define como a exlposao deve ser desenhada
    def draw(self):
        img = self.imgs[self.quadro]

        w = 30
        h = 43

        glColor3f(1.0, 1.0, 1.0)
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, self.imgs[self.quadro])

        glPushMatrix()

        glBegin(GL_QUADS)

        glTexCoord2f(0, 1)
        glVertex3f(self.x - w / 2, self.y - h / 2, 1)
        glTexCoord2f(1, 1)
        glVertex3f(self.x + w / 2, self.y - h / 2, 1)
        glTexCoord2f(1, 0)
        glVertex3f(self.x + w / 2, self.y + h / 2, 1)
        glTexCoord2f(0, 0)
        glVertex3f(self.x - w / 2, self.y + h / 2, 1)

        glEnd()

        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

        if time() - self.start >= EXPLOSION_FRAME:
            if not self.type == "player":
                self.quadro += 1
                self.start = time()

                if self.quadro >= EXPLOSION_FRAMES:
                    self.quadro = 0
                    self.dead = True
            else:
                self.quadro += 1
                self.start = time()

                if self.quadro >= EXPLOSION_FRAMES:
                    self.quadro = 0
                    self.dead = True

    # Move o objeto
    def move_me(self, x, y):
        self.x += x
        self.y += y

    def act(self):
        pass

    def check_dead(self):
        pass

    # Carrega as variaveis do objeto
    def load(self,images, x, y, Type):
        self.start = time()
        self.quadro = 0
        self.type = Type
        self.x = x
        self.y = y
        self.dead = False
        self.imgs = images
