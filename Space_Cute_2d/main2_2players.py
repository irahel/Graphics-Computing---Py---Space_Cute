########### IMPORTS ##################
import time
from builtins import isinstance
from random import randint, randrange
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
from PyQt5.QtWidgets import QShortcut
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

########### CONSTANTS ##################
########### TIME BEHIND THE SHOOTS ##################
from explosion import EXPLOSION_FRAMES
from propellant import PROPELLANT_FRAMES

SHOOT_TIME = 20000000000
SHOOT_TIME_ENEMY = 70000000000
########### INTERVAL BEHIND THE SPANWS ##################
SPANW_TIME = 80000000000
SPANW_TIME_ENEMY = 110000000000
SPANW_TIME_FLOWER = 500000000000
SPANW_TIME_PLANET = 920000000000
SPANW_TIME_STARS = 5000000000

class main(QtWidgets.QOpenGLWidget):
    ########### INITIALIZE AND CREATE VAR ##################
    def __init__(self, parent):
        QtWidgets.QOpenGLWidget.__init__(self, parent)
        self.started = False
        self.imageID_back = None
        self.in_scene = []
        self.ornaments = []
        self.moveSettings()
        self.player_x = 0
        self.player2_x = 20

        self.elapsed_time_shoot = 0
        self.elapsed_time_asteroide = 0
        self.elapsed_time_inimigo = 0
        self.elapsed_time_flower = 500000000000/2
        self.elapsed_time_planet = 920000000000/3
        self.elapsed_time_stars = 0
        self.hack = False
        ########## SOUNDS ##################
        self.sound_laser = QSound("sound/laser.wav", self)
        self.sound_laser_enemy = QSound("sound/laserenemy.wav", self)
        self.sound_explosion = QSound("sound/explos.wav", self)
        self.sound_1000pts = QSound("sound/1000pts.wav", self)
        self.sound_inGame = QSound("sound/startScene.wav", self)
        self.sound_death = QSound("sound/nooo.wav", self)
        ########### LISTS OBJECTS ##################
        self.enemy_queue = Queue_rotative()
        self.asteroid_queue = Queue_rotative()
        self.bullets_queue = Queue_rotative()
        self.flowers_queue = Queue_rotative()
        self.planets_queue = Queue_rotative()
        # self.stars_queue = Queue_rotative()
        self.explosion_queue = Queue_rotative()
        self.propellant_queue = Queue_rotative()


        self.animation_explosion = [None for _ in range (EXPLOSION_FRAMES)]
        self.animation_propellant_enemy = [None for _ in range (PROPELLANT_FRAMES)]
        self.img_nave_azul = None
        self.img_nave_amarela = None
        self.img_nave_preta = None
        self.img_tiro_azul = None
        self.img_tiro_preto = None
        self.img_tiro_amarelo = None
        self.img_tiro = None
        self.logo_init = None
        self.logo_end = None

        self.myLogo_i = Logo()
        self.myLogo_e = Logo()


        self.myNave = None
        self.myNave2 = None

    def init_queue(self):

        for _ in range (10):
            new = Enemy()
            self.enemy_queue.push(new)

        for _ in range (10):
            new = Asteroide()
            self.asteroid_queue.push(new)

        for _ in range(50):
            new = Shoot()
            self.bullets_queue.push(new)

        for _ in range(3):
            new = Flor()
            self.flowers_queue.push(new)

        for _ in range(5):
            new = Planeta()
            self.planets_queue.push(new)

        for _ in range(21):
            new = Explode()
            self.explosion_queue.push(new)

        for _ in range(11):
            new = Propellant()
            self.propellant_queue.push(new)


    ########### KEYBOARD PLAYER FUNC ##################
    def moveSettings(self):
        self.shortcut_left = QShortcut(QtCore.Qt.Key_A, self)
        self.shortcut_left.activated.connect(self.move_left)

        self.shortcut_right = QShortcut(QtCore.Qt.Key_D, self)
        self.shortcut_right.activated.connect(self.move_right)

        self.shortcut_left_shoot = QShortcut(QtCore.Qt.Key_Q , self)
        self.shortcut_left_shoot.activated.connect(self.move_left_and_shoot)

        self.shortcut_right_shoot = QShortcut(QtCore.Qt.Key_E , self)
        self.shortcut_right_shoot.activated.connect(self.move_right_and_shoot)

        self.shortcut_up = QShortcut(QtCore.Qt.Key_W, self)
        self.shortcut_up.activated.connect(self.player_shoot)

        self.shortcut_hack = QShortcut(QtCore.Qt.Key_T, self)
        self.shortcut_hack.activated.connect(self.active_hack)



        self.shortcut_left = QShortcut(QtCore.Qt.Key_J, self)
        self.shortcut_left.activated.connect(self.move2_left)

        self.shortcut_right = QShortcut(QtCore.Qt.Key_L, self)
        self.shortcut_right.activated.connect(self.move2_right)

        self.shortcut_up = QShortcut(QtCore.Qt.Key_I, self)
        self.shortcut_up.activated.connect(self.player2_shoot)

    ########### PREPARING THE SCENE ##################
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

        self.myNave = Nave(self.animation_propellant_enemy, self.player_x)
        self.in_scene.append(self.myNave)

        self.myNave2 = Nave(self.animation_propellant_enemy, self.player2_x)
        self.in_scene.append(self.myNave2)

        self.imageID_back = self.loadImage("img/Background.png")

        for i in range (EXPLOSION_FRAMES):
            self.animation_explosion[i] = self.loadImage(f"img/explosion/Comp{str(i)}.png")

        for i in range(PROPELLANT_FRAMES):
            self.animation_propellant_enemy[i] = self.loadImage(
                f"img/fire/Comp{str(i)}.png"
            )


        self.img_nave_amarela = self.loadImage("img/nave4.png")
        self.img_nave_azul = self.loadImage("img/nave1.png")
        self.img_nave_preta = self.loadImage("img/nave3.png")
        self.img_tiro_amarelo = self.loadImage("img/nave4_pow.png")
        self.img_tiro_preto = self.loadImage("img/nave3_pow.png")
        self.img_tiro_azul = self.loadImage("img/nave1_pow.png")
        self.img_tiro = self.loadImage("img/nave2_pow.png")
        self.logo_init = self.loadImage("img/SpaceCute.png")
        self.logo_end = self.loadImage("img/YouDied.png")

        self.myLogo_i.load("inicio", self.logo_init, self.logo_end)
        self.ornaments.append(self.myLogo_i)
        self.myLogo_i.inited = True

        self.myLogo_e.load("fim", self.logo_init, self.logo_end)

        self.init_queue()


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

    ########### PAINT FUNC ##################
    def paintGL(self):
        self.check_end_backm()
        self.update()
        if self.myNave.dead:
            self.started = False

        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        ########### DRAW BACKGROUND ##################
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

        self.update_time()
        self.spawn_flowers()
        self.spawn_planets()
        self.spawn_stars()

        ########### DRAW ORNAMENTS ##################
        for obj in self.ornaments:
            if obj is not None:
                if obj.dead:
                    if isinstance(obj, Flor):
                        self.flowers_queue.push(obj)
                        self.ornaments.remove(obj)
                    elif isinstance(obj, Planeta):
                        self.planets_queue.push(obj)
                        self.ornaments.remove(obj)
                    elif isinstance(obj, Star):
                        self.ornaments.remove(obj)
                obj.draw()
                obj.act()
                obj.check_dead()


        # print(self.bullets_queue.tam())
        ########### VERIFY IF THE GAME HAS STARTED ##################
        if (not self.started):
            return

        ########### DRAW SCENE ##################
        for obj in self.in_scene:
            if obj is not None:
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
                obj.draw()
                obj.act()
                obj.check_dead()

        ########### COLLISION CHECK ##################
        for obj_A in self.in_scene:
            if isinstance(obj_A, Asteroide):
                for obj_B in self.in_scene:
                    if obj_A != obj_B:
                        if isinstance(obj_B, Nave) and self.collide(obj_B, obj_A):
                            # obj_B.dead = True
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
                    if obj_A != obj_B:
                        if isinstance(obj_B, Nave) and self.collide(obj_B, obj_A):
                            # obj_B.dead = True
                            ui.down_life()
                            obj_A.dead = True
                        elif isinstance(obj_B, Shoot) and self.collide(obj_B, obj_A):
                            if not obj_B.is_enemy:
                                obj_A.dead = True
                                obj_B.dead = not self.hack
                                self.sound_explosion.play()
                                ui.up_point(10)
                                if ui.score % 1000 == 0:
                                    self.sound_1000pts.play()
            elif isinstance(obj_A, Shoot):
                if obj_A.is_enemy:
                    for obj_B in self.in_scene:
                        if (
                            obj_A != obj_B
                            and isinstance(obj_B, Nave)
                            and self.collide(obj_B, obj_A)
                        ):
                            # obj_B.dead = True
                            ui.down_life()
                            obj_A.dead = True

        self.spawn_asteroide()
        self.spawn_inimigos()

        self.update()

    def check_end_backm(self):
        if self.sound_inGame.isFinished():
            self.sound_inGame.play()

    def update_time(self):
        self.elapsed_time_shoot += time()
        self.elapsed_time_asteroide += time()
        self.elapsed_time_inimigo += time()
        self.elapsed_time_flower += time()
        self.elapsed_time_planet += time()
        self.elapsed_time_stars += time()

    def spawn_stars(self):
        if self.elapsed_time_stars >= SPANW_TIME_STARS:
            position = randint(-49,49)
            scale = self.rand_tam_star()
            new_star = Star(position, scale)
            self.ornaments.append(new_star)
            self.elapsed_time_stars = 0

    def spawn_planets(self):
        if self.elapsed_time_planet >= SPANW_TIME_PLANET:
            position = randint(-50,50)
            scale = self.rand_tam()
            new_planet = self.planets_queue.pop()
            new_planet.load(position, scale)
            self.ornaments.append(new_planet)
            self.elapsed_time_planet = 0

    def rand_tam(self):
        return float(f"{str(randint(0, 2))}.{str(randint(1, 5))}")

    def rand_tam_star(self):
        return float(f"0.{str(randint(1, 3))}")

    def spawn_flowers(self):
        if self.elapsed_time_flower >= SPANW_TIME_FLOWER:
            position = randint(-50,50)

            new_flower = self.flowers_queue.pop()
            new_flower.load(position)
            self.ornaments.append(new_flower)
            self.elapsed_time_flower = 0

    ########### SPAWNING ASTEROIDE FUNCS #################
    def spawn_asteroide(self):
        if self.elapsed_time_asteroide >= SPANW_TIME:
            new_aste = self.asteroid_queue.pop()
            new_aste.load(randint(-49,43))
            self.in_scene.append(new_aste)
            self.elapsed_time_asteroide = 0

    ########### SPAWNING ASTEROIDE FUNCS #################
    def spawn_inimigos(self):
        if self.elapsed_time_inimigo >= SPANW_TIME_ENEMY:
            self.create_inimigos(

            )

    def create_inimigos(self):
        new_inimigo = self.enemy_queue.pop()
        new_inimigo.load(randint(-49,43), self.animation_propellant_enemy, self.img_nave_azul, self.img_nave_amarela, self.img_nave_preta)
        self.in_scene.append(new_inimigo)
        self.elapsed_time_inimigo = 0

    ########### MOVING PLAYER FUNCS #################
    def move_left(self):
        if self.myNave.move_x + self.myNave.position_x >= -43:
            self.myNave.move_left()
            self.player_x -= 3

    def move_left_and_shoot(self):
        if self.myNave.move_x + self.myNave.position_x >= -43:
            self.myNave.move_left()
            self.player_x -= 3
            self.create_shoot(self.player_x)

    def move_right(self):
        if self.myNave.move_x + self.myNave.position_x <= 43:
            self.myNave.move_right()
            self.player_x += 3

    def move_right_and_shoot(self):
        if self.myNave.move_x + self.myNave.position_x <= 43:
            self.myNave.move_right()
            self.player_x += 3
            self.create_shoot(self.player_x)


    #############NEWS##############################

    def move2_left(self):
        if self.myNave2.move_x + self.myNave2.position_x >= -43:
            self.myNave2.move_left()
            self.player2_x -= 3

    def move2_right(self):
        if self.myNave2.move_x + self.myNave2.position_x <= 43:
            self.myNave2.move_right()
            self.player2_x += 3


    ########### SHOOT PLAYER FUNC ##################
    ########### CREATE THE BULLET ##################
    def player_shoot(self):
        self.create_shoot(self.player_x)

    def player2_shoot(self):
        self.create_shoot(self.player2_x)

    def create_shoot(self,position , position_y = None, position_y_2 = None,is_enemy = False, type = "player", qtd = None, tiro_respectivo = None):
        if is_enemy:
            if qtd == 1:
                new_shoot = self.bullets_queue.pop()
                new_shoot.load( tiro_respectivo, position,position_y, position_y_2, True , type)
                self.in_scene.append(new_shoot)
            elif qtd == 2:
                new_shoot = self.bullets_queue.pop()
                new_shoot.load( tiro_respectivo , position -2.5, position_y, position_y_2, True, type)
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
            else:
                new_shoot = self.bullets_queue.pop()
                new_shoot.load(self.img_tiro, position,-46.0, -40.0 , False,1)
                self.in_scene.append(new_shoot)
            self.elapsed_time_shoot =  0
            self.sound_laser.play()

    ########### COLISION CHECK FUNC ##################
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

    def reestart(self):
        self.reloc()
        self.started = False
        self.in_scene = []
        self.player_x = 0
        self.player2_x = 20
        self.myNave = Nave(self.animation_propellant_enemy, self.player_x)
        self.myNave2 = Nave(self.animation_propellant_enemy, self.player_x + 20)
        self.elapsed_time_shoot = 0
        self.elapsed_time_asteroide = 0
        self.elapsed_time_inimigo = 0
        self.hack = False
        self.in_scene.append(self.myNave)
        self.in_scene.append(self.myNave2)
        self.sound_inGame.stop()
        self.sound_inGame = QSound("sound/inGame.wav", self)
        self.sound_inGame.play()
        if self.myLogo_i.inited:
            self.ornaments.remove(self.myLogo_i)
            self.myLogo_i.inited = False
        if self.myLogo_e.inited:
            self.ornaments.remove(self.myLogo_e)
            self.myLogo_e.inited = False

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

        for obj in self.ornaments:
            if isinstance(obj, Flor):
                self.flowers_queue.push(obj)
                self.ornaments.remove(obj)
            elif isinstance(obj, Planeta):
                self.planets_queue.push(obj)
                self.ornaments.remove(obj)


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

    def dead(self):
        self.myNave.dead = True
        self.sound_inGame.stop()
        self.sound_inGame = QSound("sound/gameOver.wav", self)
        self.sound_death.play()
        if self.sound_death.isFinished():
            self.sound_inGame.play()
        self.ornaments.append(self.myLogo_e)
        self.myLogo_e.inited = True

########### MAIN FUNC ##################
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, main)

    MainWindow.show()
    sys.exit(app.exec_())
