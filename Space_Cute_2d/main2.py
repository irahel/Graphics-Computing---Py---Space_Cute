# Imports
import time
from builtins import isinstance
from random import randint
from time import time
from OpenGL.GL.exceptional import glGenTextures, glTexParameter, glBegin, glEnd
from OpenGL.GL.images import glTexImage2D
from OpenGL.raw.GL.VERSION.GL_1_0 import glPixelStorei, glColor3f, glDisable, glEnable, glTexEnvi, glPushMatrix, \
    glTexCoord2f, glVertex3f, glPopMatrix, glClearColor, glShadeModel, glBlendFunc, glAlphaFunc, glMatrixMode, \
    glLoadIdentity, glOrtho, glClear
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_QUADS, glBindTexture, GL_TEXTURE_2D, GL_UNPACK_ALIGNMENT, GL_RGBA, \
    GL_LIGHTING, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE, GL_LINEAR, GL_TEXTURE_MIN_FILTER, \
    GL_TEXTURE_MAG_FILTER, GL_SMOOTH, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ALPHA_TEST, GL_NOTEQUAL, \
    GL_PROJECTION, GL_MODELVIEW, GL_COLOR_BUFFER_BIT
from OpenGL.raw.GL._types import GL_UNSIGNED_BYTE
from PIL import Image
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtMultimedia import QSound
from asteroide import Asteroide
from enemy import Enemy
from mainwindow import Ui_MainWindow
from nave import Nave
from pow import Shoot
from flor import Flor
from planeta import Planeta
from star import Star
from explosion import Explode
from my_queue import Queue_rotative
from propellant import Propellant
from logo import Logo
from explosion import EXPLOSION_FRAMES
from propellant import PROPELLANT_FRAMES
from power_up import Power_up

# Constantes
# SHOOT_TIME = Tempo minimo para o player conseguir atirar
# SHOOT_TIME_ENEMY = Tempo minimo para os inimigos conseguirem atirar
# SPAWN_TIME = Tempo em que os asteroides aparecem
# SPAWN_TIME_ENEMY = Tempo em que os inimigos aparecem
# SPAWN_TIME_FLOWER = Tempo em que as "nebulosas" aparecem
# SPAWN_TIME_PLANET = Tempo em que os planetas aparecem
# SPAWN_TIME_STARS = Tempo em que as estrelas aparecem
SHOOT_TIME = 20000000000
SHOOT_TIME_ENEMY = 70000000000
SPAWN_TIME = 80000000000
SPAWN_TIME_ENEMY = 110000000000
SPAWN_TIME_FLOWER = 500000000000
SPAWN_TIME_PLANET = 920000000000
SPAWN_TIME_STARS = 5000000000
POWER_UP_TIME = 800000000000
POWER_UP_SHOOT = 500000000000
POWER_UP_SPEED = 500000000000

# Todo objeto do jogo deve implementar as funcoes
#	        draw()
#			act()
#			check_dead()
# E conter um atributo self.dead

# Todo objeto que necessita de teste de colisao deve implementar as funcoes
#			get_x()
#			get_y()

# Todo objeto que será pre carregado deve implementar a funcao
#			load()

class main(QtWidgets.QOpenGLWidget):
    # Cria as variaveis necessarias
    # self.started = Indica se o jogo foi iniciado ou nao
    # self.in_scene = Vetor para a cena (tudo que faz parte do jogo e sera desenhado)
    # self.ornaments = Vetor para a beleza da cena (tudo que sao apenas "flores")
    #
    # Temporizadores
    # self.elapsed_time_shoot = Tempo desde o ultimo tiro do player
    # self.elapsed_time_asteroide = Tempo desde o ultimo asteroide criado
    # self.elapsed_time_inimigo = Tempo desde o ultimo inimigo criado
    # self.elapsed_time_flower = Tempo desde a ultima flor criada
    # self.elapsed_time_planet = Tempo desde o ultimo planeta criado
    # self.elapsed_time_stars = = Tempo desde a ultima estrela criada
    #
    # Sons
    # self.sound_laser = Tiro do player
    # self.sound_laser_enemy = Tiro do inimigo
    # self.sound_explosion = Explosao
    # self.sound_1000pts = 1000 pontos alcancados
    # self.sound_inGame = Fundo do jogo
    # self.sound_death = Morte
    #
    # Filas para pre carregamento dos objetos
    # self.enemy_queue = Fila dos inimigos
    # self.asteroid_queue = Fila dos Asteroides
    # self.bullets_queue = Fila das balas
    # self.flowers_queue = Fila das flores
    # self.planets_queue = Fila dos planetas
    # self.explosion_queue = Fila das explosoes
    # self.propellant_queue = Fila dos propulsores
    #
    # Variaveis para pre carregamento das texturas
    # self.animation_explosion
    # self.animation_propellant_enemy
    # self.img_nave_azul
    # self.img_nave_amarela
    # self.img_nave_preta
    # self.img_tiro_azul
    # self.img_tiro_preto
    # self.img_tiro_amarelo
    # self.img_tiro
    # self.logo_init
    # self.logo_end
    # self.imageID_back
    # self.myLogo_i = Logo()
    # self.myLogo_e = Logo()
    #
    # self.myNave = Nave do jogador
    def __init__(self, parent):
        QtWidgets.QOpenGLWidget.__init__(self, parent)
        self.started = False
        self.imageID_back = None
        self.in_scene = []
        self.ornaments = []
        self.elapsed_time_shoot = 0
        self.elapsed_time_asteroide = 0
        self.elapsed_time_inimigo = 0
        self.elapsed_time_flower = 500000000000/2
        self.elapsed_time_planet = 920000000000/3
        self.elapsed_time_stars = 0
        self.elapsed_time_powers = 0
        self.elapsed_time_power_shoot = 0
        self.elapsed_time_power_speed = 0
        self.hack = False
        self.speed = False
        self.sound_laser = QSound("sound/laser.wav", self)
        self.sound_laser_enemy = QSound("sound/laserenemy.wav", self)
        self.sound_explosion = QSound("sound/explos.wav", self)
        self.sound_1000pts = QSound("sound/1000pts.wav", self)
        self.sound_inGame = QSound("sound/startScene.wav", self)
        self.sound_death = QSound("sound/nooo.wav", self)
        self.sound_power = QSound("sound/powerUp.wav",self)
        self.enemy_queue = Queue_rotative()
        self.asteroid_queue = Queue_rotative()
        self.bullets_queue = Queue_rotative()
        self.flowers_queue = Queue_rotative()
        self.planets_queue = Queue_rotative()
        self.explosion_queue = Queue_rotative()
        self.propellant_queue = Queue_rotative()
        self.power_queue = Queue_rotative()
        self.animation_explosion = [None for i in range (EXPLOSION_FRAMES)]
        self.animation_propellant_enemy = [None for i in range (PROPELLANT_FRAMES)]
        self.img_planets = [None for i in range (10)]
        self.img_nave_azul = None
        self.img_nave_amarela = None
        self.img_nave_preta = None
        self.img_tiro_azul = None
        self.img_tiro_preto = None
        self.img_tiro_amarelo = None
        self.img_tiro = None
        self.logo_init = None
        self.logo_end = None
        self.power_up_vida = None
        self.power_up_shoot = None
        self.power_up_speed = None
        self.myLogo_i = Logo()
        self.myLogo_e = Logo()
        self.myNave = None

    # Inicializa as filas de pre carregamentos
    def init_queue(self):

        for i in range (20):
            new = Enemy()
            self.enemy_queue.push(new)

        for i in range (50):
            new = Asteroide()
            self.asteroid_queue.push(new)

        for i in range(100):
            new = Shoot()
            self.bullets_queue.push(new)

        for i in range(10):
            new = Flor()
            self.flowers_queue.push(new)

        for i in range(10):
            new = Planeta()
            self.planets_queue.push(new)

        for i in range(50):
            new = Explode()
            self.explosion_queue.push(new)

        for i in range(30):
            new = Propellant()
            self.propellant_queue.push(new)

        for i in range(20):
            new = Power_up()
            self.power_queue.push(new)

    # Prepara a cena e carrega as texturas
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(GL_SMOOTH)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(GL_NOTEQUAL, 0.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-50.0, 50.0, -50.0, 50.0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.myNave = Nave(self.animation_propellant_enemy, 0)
        self.in_scene.append(self.myNave)

        self.imageID_back = self.loadImage("img/Background.png")

        for i in range(EXPLOSION_FRAMES):
            self.animation_explosion[i] = self.loadImage("img/explosion/Comp" + str(i) + ".png")

        for i in range(PROPELLANT_FRAMES):
            self.animation_propellant_enemy[i] = self.loadImage("img/fire/Comp" + str(i) + ".png")

        for i in range (10):
            self.img_planets[i] = self.loadImage("img/planets/planeta" +str(i) + ".png")

        self.img_nave_amarela = self.loadImage("img/nave4.png")
        self.img_nave_azul = self.loadImage("img/nave1.png")
        self.img_nave_preta = self.loadImage("img/nave3.png")
        self.img_tiro_amarelo = self.loadImage("img/nave4_pow.png")
        self.img_tiro_preto = self.loadImage("img/nave3_pow.png")
        self.img_tiro_azul = self.loadImage("img/nave1_pow.png")
        self.img_tiro = self.loadImage("img/nave2_pow.png")
        self.logo_init = self.loadImage("img/SpaceCute.png")
        self.logo_end = self.loadImage("img/YouDied.png")
        self.power_up_vida = self.loadImage("img/power_up_life.png")
        self.power_up_shoot = self.loadImage("img/power_up_shot.png")
        self.power_up_speed = self.loadImage("img/power_up_speed.png")

        self.myLogo_i.load("inicio", self.logo_init, self.logo_end)
        self.ornaments.append(self.myLogo_i)
        self.myLogo_i.inited = True

        self.myLogo_e.load("fim", self.logo_init, self.logo_end)

        self.init_queue()

        # Arrumando erros de frict
        fix_p = self.propellant_queue.pop()
        fix_p.load(self.animation_propellant_enemy, 70, 70, "fix")
        self.ornaments.append(fix_p)

        new_explosion = self.explosion_queue.pop()
        new_explosion.load(self.animation_explosion, 70, 70, "fix")
        self.ornaments.append(new_explosion)

    # Funcao para carregar imagens a partir de um caminho
    def loadImage(self, path):
        im = Image.open(path)

        ix, iy, image = im.size[0], im.size[1], im.tobytes()

        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, image
        )
        return ID

    # funcoes para acoes no teclado
    # A = move para esquerda
    # D = move para direita
    # W = atira
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.myNave.moving_left = True
        if event.key() == QtCore.Qt.Key_A:
            self.myNave.moving_left = True

        if event.key() == QtCore.Qt.Key_Right:
            self.myNave.moving_right = True
        if event.key() == QtCore.Qt.Key_D:
            self.myNave.moving_right = True

        if event.key() == QtCore.Qt.Key_Up:
            self.myNave.shooting = True
        if event.key() == QtCore.Qt.Key_W:
            self.myNave.shooting = True

        # if event.key() == QtCore.Qt.Key_T:
        #     self.hack = True

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.myNave.moving_left = False
        if event.key() == QtCore.Qt.Key_A:
            self.myNave.moving_left = False

        if event.key() == QtCore.Qt.Key_Right:
            self.myNave.moving_right = False
        if event.key() == QtCore.Qt.Key_D:
            self.myNave.moving_right = False

        if event.key() == QtCore.Qt.Key_Up:
            self.myNave.shooting = False
        if event.key() == QtCore.Qt.Key_W:
            self.myNave.shooting = False

        if event.key() == QtCore.Qt.Key_T:
            self.hack = False

    # Funcao de desenhar a cena
    def paintGL(self):

        # Checa se a musica de fundo acabou e reinicia
        self.check_end_backm()
        self.update()
        # Se o player morreu, entao o jogo acaba
        if self.myNave.dead:
            self.started = False

        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # Desenha o background
        ''''' Inicio do background '''''
        glColor3f(1.0, 1.0, 1.0)
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, self.imageID_back)

        glPushMatrix()

        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex3f(50,-50, 1)
        glTexCoord2f(1, 1)
        glVertex3f(-50, -50, 1)
        glTexCoord2f(1, 0)
        glVertex3f(-50, 50, 1)
        glTexCoord2f(0, 0)
        glVertex3f(50, 50, 1)
        glEnd()

        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
        ''''' Fim do background '''''

        self.update_time()
        self.spawn_flowers()
        self.spawn_planets()
        self.spawn_stars()

        # Desenha os ornamentos ( "Flores" )
        # e retira os objetos "mortos" retornando eles para a fila
        for obj in self.ornaments:
            if not obj == None:
                if obj.dead:
                    if isinstance(obj, Flor):
                        self.flowers_queue.push(obj)
                        self.ornaments.remove(obj)
                    elif isinstance(obj, Planeta):
                        self.planets_queue.push(obj)
                        self.ornaments.remove(obj)
                    elif isinstance(obj, Star):
                        self.ornaments.remove(obj)
                    elif isinstance(obj, Explode):
                        self.explosion_queue.push(obj)
                        self.ornaments.remove(obj)
                    elif isinstance(obj, Propellant):
                        self.propellant_queue.push(obj)
                        self.ornaments.remove(obj)
                obj.draw()
                obj.act()
                obj.check_dead()

        # print (self.enemy_queue.tam())
        # Verifica se o jogo foi iniciado
        if (not self.started):
            return

        # Desenha a cena
        # e retira os objetos mortos retornando ele para a fila
        # e instancia uma explosao no lugar
        for obj in self.in_scene:
            if not obj == None:
                if obj.dead:
                    if isinstance(obj, Enemy):
                        new_explosion = self.explosion_queue.pop()
                        new_explosion.load(self.animation_explosion, obj.move_x + obj.position_x ,obj.move_y + 6, "enemy")
                        self.in_scene.append(new_explosion)
                        self.enemy_queue.push(obj)
                        self.in_scene.remove(obj)
                    elif isinstance(obj, Asteroide):
                        new_explosion = self.explosion_queue.pop()
                        new_explosion.load(self.animation_explosion, obj.move_x + obj.position_x, obj.move_y + 5,"enemy")
                        self.in_scene.append(new_explosion)
                        self.asteroid_queue.push(obj)
                        self.in_scene.remove(obj)
                    elif isinstance(obj, Shoot):
                        self.bullets_queue.push(obj)
                        self.in_scene.remove(obj)
                    elif isinstance(obj, Explode):
                        obj.dead = False
                        self.explosion_queue.push(obj)
                        self.in_scene.remove(obj)
                    elif isinstance(obj, Power_up):
                        self.power_queue.push(obj)
                        self.in_scene.remove(obj)
                if isinstance(obj, Nave):
                    if obj.shooting:
                        self.create_shoot(obj.move_x + obj.position_x)
                obj.draw()
                obj.act()
                obj.check_dead()

        # Testa as colisoes e aplica os efeitos (ganhar pontos, ou perder vida)
        for obj_A in self.in_scene:
            if isinstance(obj_A, Asteroide):
                for obj_B in self.in_scene:
                    if not (obj_A == obj_B):
                        if isinstance(obj_B, Nave) and self.collide(obj_B, obj_A):
                            ui.down_life()
                            obj_A.dead = True
                        elif isinstance(obj_B, Shoot) and self.collide(obj_B, obj_A):
                            if not obj_B.is_enemy:
                                obj_A.dead = True
                                if not self.hack:
                                    obj_B.dead = True
                                self.sound_explosion.play()
                                ui.up_point(10)
                                if ui.score % 1000 == 0:
                                    self.sound_1000pts.play()
            elif isinstance(obj_A, Enemy):
                obj_A.elapsed_shoot_time += time()
                if obj_A.elapsed_shoot_time >= SHOOT_TIME_ENEMY:
                    if obj_A.nave_type == 0:
                        self.create_shoot(obj_A.move_x + obj_A.position_x,
                                          obj_A.move_y,
                                          obj_A.move_y + 6, True, obj_A.nave_type,
                                          obj_A.shoot_type, self.img_tiro_azul)
                    elif obj_A.nave_type ==1:
                        self.create_shoot(obj_A.move_x + obj_A.position_x,
                                          obj_A.move_y,
                                          obj_A.move_y + 6, True, obj_A.nave_type,
                                          obj_A.shoot_type, self.img_tiro_amarelo)
                    elif obj_A.nave_type == 2:
                        self.create_shoot(obj_A.move_x + obj_A.position_x,
                                          obj_A.move_y,
                                          obj_A.move_y + 6, True, obj_A.nave_type,
                                          obj_A.shoot_type, self.img_tiro_preto)

                    obj_A.elapsed_shoot_time = 0
                for obj_B in self.in_scene:
                    if not (obj_A == obj_B):
                        if isinstance(obj_B, Nave) and self.collide(obj_B, obj_A):
                            ui.down_life()
                            obj_A.dead = True
                        elif isinstance(obj_B, Shoot) and self.collide(obj_B, obj_A):
                            if not obj_B.is_enemy:
                                obj_A.dead = True
                                if self.hack:
                                    obj_B.dead = False
                                else:
                                    obj_B.dead = True
                                self.sound_explosion.play()
                                ui.up_point(10)
                                if ui.score % 1000 == 0:
                                    self.sound_1000pts.play()
            elif isinstance(obj_A, Shoot):
                if obj_A.is_enemy:
                    for obj_B in self.in_scene:
                        if not (obj_A == obj_B):
                            if isinstance(obj_B, Nave) and self.collide(obj_B, obj_A):
                                ui.down_life()
                                obj_A.dead = True
            elif isinstance(obj_A, Nave):
                if self.speed:
                    obj_A.speed = 3
                else:
                    obj_A.speed = 0
                for obj_B in self.in_scene:
                    if not (obj_A == obj_B):
                        if isinstance(obj_B, Power_up) and self.collide(obj_B, obj_A):
                            obj_B.dead = True
                            self.sound_power.play()
                            if obj_B.skin == 0:
                                ui.up_life()
                            elif obj_B.skin == 1:
                                self.hack = True
                                self.elapsed_time_power_shoot = 0
                            elif obj_B.skin == 2:
                                self.speed = True
                                self.elapsed_time_power_speed = 0

        self.spawn_asteroide()
        self.spawn_inimigos()
        self.spawn_powers()
        self.update()

    # Checa se a musica de fundo acabou e reinicia caso positivo
    def check_end_backm(self):
        if self.sound_inGame.isFinished():
            self.sound_inGame.play()

    # Atualiza o tempo dos temporizadores
    def update_time(self):
        self.elapsed_time_shoot += time()
        self.elapsed_time_asteroide += time()
        self.elapsed_time_inimigo += time()
        self.elapsed_time_flower += time()
        self.elapsed_time_planet += time()
        self.elapsed_time_stars += time()
        self.elapsed_time_powers += time()
        if self.hack:
            self.elapsed_time_power_shoot += time()
        if self.elapsed_time_power_shoot >= POWER_UP_SHOOT:
            self.hack = False
        if self.speed:
            self.elapsed_time_power_speed += time()
        if self.elapsed_time_power_speed >= POWER_UP_SPEED:
            self.speed = False

    # Faz a criacao das estrelas, com uma posicao e escala aleatoria
    def spawn_stars(self):
        if self.elapsed_time_stars >= SPAWN_TIME_STARS:
            position = randint(-49,49)
            scale = self.rand_tam_star()
            new_star = Star(position, scale)
            self.ornaments.append(new_star)
            self.elapsed_time_stars = 0

    # Faz a criacao dos planetas, com uma posicao e escala aleatoria
    def spawn_planets(self):
        if self.elapsed_time_planet >= SPAWN_TIME_PLANET:
            position = randint(-50,50)
            scale = self.rand_tam()
            new_planet = self.planets_queue.pop()
            new_planet.load(position, scale, self.img_planets)
            self.ornaments.append(new_planet)
            self.elapsed_time_planet = 0

    # Retorna um tamanho aleatorio para os planetas
    def rand_tam(self):
        return float(str(randint(0, 2)) +"."+ str(randint(1, 5)))

    # Retorna um tamanho aleatorio para as estrelas
    def rand_tam_star(self):
        return float("0."+ str(randint(1, 3)))

    # Faz a criacao das flores, com uma posicao aleatoria
    def spawn_flowers(self):
        if self.elapsed_time_flower >= SPAWN_TIME_FLOWER:
            position = randint(-50,50)
            new_flower = self.flowers_queue.pop()
            new_flower.load(position)
            self.ornaments.append(new_flower)
            self.elapsed_time_flower = 0

    # Faz a criacao dos asteroides, com uma posicao aleatioria
    def spawn_asteroide(self):
        if self.elapsed_time_asteroide >= SPAWN_TIME:
            new_aste = self.asteroid_queue.pop()
            new_aste.load(randint(-49,43))
            self.in_scene.append(new_aste)
            self.elapsed_time_asteroide = 0

    # Faz a criacao dos power ups, com uma posicao aleatioria
    def spawn_powers(self):
        if self.elapsed_time_powers >= POWER_UP_TIME:
            new_power = self.power_queue.pop()
            new_power.load(randint(-49, 43), 60, self.power_up_vida, self.power_up_shoot, self.power_up_speed)
            self.in_scene.append(new_power)
            self.elapsed_time_powers = 0

    # Faz a criacao dos inimigos, com uma posicao aleatoria
    def spawn_inimigos(self):
        if self.elapsed_time_inimigo >= SPAWN_TIME_ENEMY:
            new_inimigo = self.enemy_queue.pop()
            new_inimigo.load(randint(-49,43), self.animation_propellant_enemy, self.img_nave_azul, self.img_nave_amarela, self.img_nave_preta)
            self.in_scene.append(new_inimigo)
            self.elapsed_time_inimigo = 0

    # Funcao para criacao dos tiros, tanto dos inimigos quanto do player
    def create_shoot(self,position , position_y = None, position_y_2 = None,is_enemy = False, type = "player", qtd = None, tiro_respectivo = None):
        if is_enemy:
            if qtd == 1:
                new_shoot = self.bullets_queue.pop()
                new_shoot.load( tiro_respectivo, position,position_y, position_y_2, True , type)
                self.in_scene.append(new_shoot)
            elif qtd == 2:
                new_shoot = self.bullets_queue.pop()
                new_shoot.load( tiro_respectivo , position - 2.5, position_y, position_y_2, True, type)
                new_shoot2 = self.bullets_queue.pop()
                new_shoot2.load( tiro_respectivo, position + 2.5, position_y, position_y_2, True, type)
                self.in_scene.append(new_shoot)
                self.in_scene.append(new_shoot2)
            elif qtd == 3:
                new_shoot = self.bullets_queue.pop()
                new_shoot.load( tiro_respectivo , position -5, position_y, position_y_2, True, type)
                new_shoot2 = self.bullets_queue.pop()
                new_shoot2.load( tiro_respectivo, position , position_y, position_y_2, True, type)
                new_shoot3 = self.bullets_queue.pop()
                new_shoot3.load( tiro_respectivo , position + 5, position_y, position_y_2, True, type)
                self.in_scene.append(new_shoot)
                self.in_scene.append(new_shoot2)
                self.in_scene.append(new_shoot3)
            self.sound_laser_enemy.play()
            return
        if self.elapsed_time_shoot >= SHOOT_TIME:
            if self.hack:
                new_shoot = self.bullets_queue.pop()
                new_shoot.load(self.img_tiro, position + 5, -46.0, -40.0, False,1)
                new_shoot2 = self.bullets_queue.pop()
                new_shoot2.load(self.img_tiro, position - 5, -46.0, -40.0, False,1)
                new_shoot3 = self.bullets_queue.pop()
                new_shoot3.load(self.img_tiro, position, -46.0, -40.0, False,1)
                self.in_scene.append(new_shoot)
                self.in_scene.append(new_shoot2)
                self.in_scene.append(new_shoot3)
                self.sound_laser.play()
            else:
                new_shoot = self.bullets_queue.pop()
                new_shoot.load(self.img_tiro, position,-46.0, -40.0 , False,1)
                self.in_scene.append(new_shoot)
                self.sound_laser.play()
            self.elapsed_time_shoot = 0

    # Checagem de colisao
    def collide(self, A, B):
        A_colliding_B_in_x = (A.get_x()[1] >= B.get_x()[0] and A.get_x()[1] <= B.get_x()[1])
        #or
        B_colliding_A_in_x = (B.get_x()[1] >= A.get_x()[0] and B.get_x()[1] <= A.get_x()[1])

        A_colliding_B_in_y = (A.get_y()[1] >= B.get_y()[0] and A.get_y()[1] <= B.get_y()[1])
        #or
        B_colliding_A_in_y = (B.get_y()[1] >= A.get_y()[0] and B.get_y()[1] <= A.get_y()[1])

        return (A_colliding_B_in_x or B_colliding_A_in_x) and \
               (A_colliding_B_in_y or B_colliding_A_in_y)

    def active_hack(self):
        self.hack = not self.hack

    # Reinicia o jogo, seta todas as variaveis para o inicio
    def reestart(self):
        self.reloc()
        self.started = False
        self.player_move_left = False
        self.player_move_right = False
        self.myNave = Nave(self.animation_propellant_enemy, 0)
        self.elapsed_time_shoot = 0
        self.elapsed_time_asteroide = 0
        self.elapsed_time_inimigo = 0
        self.hack = False
        self.in_scene = []
        self.in_scene.append(self.myNave)
        self.sound_inGame.stop()
        self.sound_inGame = QSound("sound/inGame.wav", self)
        self.sound_inGame.play()
        if self.myLogo_i.inited:
            self.ornaments.remove(self.myLogo_i)
            self.myLogo_i.inited = False
        if self.myLogo_e.inited:
            self.ornaments.remove(self.myLogo_e)
            self.myLogo_e.inited = False

    # Realoca os objetos atualmente na cena para suas respectivas filas
    def reloc(self):
        for obj in self.in_scene:
            if isinstance(obj, Enemy):
                self.enemy_queue.push(obj)
                self.in_scene.remove(obj)
            elif isinstance(obj, Asteroide):
                self.asteroid_queue.push(obj)
                self.in_scene.remove(obj)
            elif isinstance(obj, Shoot):
                self.bullets_queue.push(obj)
                self.in_scene.remove(obj)
            elif isinstance(obj, Explode):
                self.explosion_queue.push(obj)
                self.in_scene.remove(obj)
            elif isinstance(obj, Power_up):
                self.power_queue.push(obj)
                self.in_scene.remove(obj)

        for obj in self.ornaments:
            if isinstance(obj, Flor):
                self.flowers_queue.push(obj)
                self.ornaments.remove(obj)
            elif isinstance(obj, Planeta):
                self.planets_queue.push(obj)
                self.ornaments.remove(obj)

    # Para o jogo
    def stop(self):
        self.reloc()
        self.started = False
        self.sound_inGame.stop()
        self.sound_inGame = QSound("sound/startScene.wav", self)
        self.sound_inGame.play()
        self.in_scene = []
        self.ornaments.append(self.myLogo_i)
        if self.myLogo_e.inited:
            self.ornaments.remove(self.myLogo_e)
            self.myLogo_e.inited = False
        self.myLogo_i.inited = True

    #  Quando o jogador morre
    def dead(self):
        self.reloc()
        self.myNave.dead = True
        self.sound_inGame.stop()
        self.sound_inGame = QSound("sound/gameOver.wav", self)
        self.sound_death.play()
        if self.sound_death.isFinished():
            self.sound_inGame.play()
        self.ornaments.append(self.myLogo_e)
        self.myLogo_e.inited = True

# Main
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, main)

    MainWindow.show()
    sys.exit(app.exec_())
