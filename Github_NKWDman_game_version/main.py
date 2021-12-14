import pygame
import sys
from pygame.locals import *
import moviepy.editor as py
import random


def im_unbox(name):
    try:
        fullname = "image/" + name
        image = pygame.image.load(fullname).convert_alpha()
        return image
    except():
        print("error image")


volume = 0.1
scale_w = 1
scale_h = 1
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Glamorous NKWDman')
pygame.display.set_icon(im_unbox("nkwdicon.png"))
font = pygame.font.SysFont("Times New Roman®", 28)
Button_na = pygame.image.load("image/Main_button_icon_1.png")
Button_a = pygame.image.load("image/Main_button_icon_2.png")


def play_sound(music):
    sound = pygame.mixer.Sound(music)
    sound.set_volume(volume)
    sound.play()


def Default_event_check(event):
    global scale_w, scale_h, screen
    if event.type == VIDEORESIZE:
        screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        scale_w = event.w / 1280
        scale_h = event.h / 720
        return True
    if event.type == QUIT:
        sys.exit()


def image_render(image):
    width = image.get_width()
    height = image.get_height()
    image = pygame.transform.scale(image, (int(width * scale_w), int(height * scale_h)))
    return image


def draw_image(image, x, y):
    rect = image_render(image).get_rect()
    rect.center = (x * scale_w, y * scale_h)
    screen.blit(image_render(image), (x * scale_w, y * scale_h))


def play_video(video):
    clip = py.VideoFileClip(video)
    clip_resized = clip.resize(newsize=(int(1280 * scale_w), int(720 * scale_h)))
    clip_resized.preview()
    global screen
    screen = pygame.display.set_mode((int(1280 * scale_w), int(720 * scale_h)), pygame.RESIZABLE)


class Text:
    def __init__(self, text, x, y):
        self.x = x
        self.y = y
        if scale_h < scale_w:
            self.font_size = int(35 * scale_h)
        else:
            self.font_size = int(35 * scale_w)
        self.font_type = pygame.font.SysFont("Times New Roman®", self.font_size)
        self.text = text
        self.textobj = self.font_type.render(text, True, (0, 0, 0))
        self.textrect = self.textobj.get_rect()
        self.textrect.center = (self.x * scale_w, self.y * scale_h)


class Text_center(Text):
    def __init__(self, text, x, y):
        super().__init__(text, x, y)
        self.textrect.center = (self.x * scale_w, self.y * scale_h)

    def draw_tc(self):
        screen.blit(self.textobj, self.textrect)


class Text_topleft(Text):
    def __init__(self, text, x, y):
        super().__init__(text, x, y)
        self.textrect.topleft = (self.x * scale_w, self.y * scale_h)

    def draw_ttl(self):
        screen.blit(self.textobj, self.textrect)


class Animated_background:
    def __init__(self, image, speed, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.y = y

    def animation(self, speed_var=0):
        speed_var += int(self.speed * scale_w)
        if speed_var < 1:
            speed_var = 1
        self.rect.topleft = (self.rect.x, self.y)
        self.rect.x += speed_var
        screen.blit(image_render(self.image), (self.rect.x - 1280 * scale_w, self.rect.y * scale_h))
        screen.blit(image_render(self.image), (self.rect.x, self.rect.y * scale_h))
        if self.rect.x >= 1280 * scale_w:
            self.rect.x = 0
        self.rect.topleft = (self.rect.x, self.y)


class Text_pages:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    def draw_text(self, text, border=23):
        rows = [""]
        y_pos = [self.y]
        current_row = 0
        count = 0
        for letter in text:
            draw_image(self.image, 0, 0)
            rows[current_row] += letter
            for i in range(current_row + 1):
                clt = Text_topleft(rows[i], self.x, y_pos[i])
                clt.draw_ttl()
            count += 1
            if count >= border and letter == " ":
                current_row += 1
                count = 0
                rows.insert(current_row, "")
                y_pos.insert(current_row, self.y)
                y_pos[current_row] += (40 * current_row) * scale_h

    def draw_animation_text(self, text, border=23, count=0, current_row=0):
        rows = [""]
        y_pos = [self.y]
        button_skip = Button(1050, 500, Button_na, Button_a, 0.75, "sounds/button_sound.wav")
        for letter in text:
            draw_image(self.image, 0, 0)
            if button_skip.draw_button_with_text("Skip"):
                break
            rows[current_row] += letter
            for i in range(current_row + 1):
                clt = Text_topleft(rows[i], self.x, y_pos[i])
                clt.draw_ttl()
            if letter != " ":
                play_sound("sounds/Machine_effect_1.wav")
            count += 1
            if count >= border and letter == " ":
                play_sound("sounds/typewriter-line-break-1.wav")
                current_row += 1
                count = 0
                rows.insert(current_row, "")
                y_pos.insert(current_row, self.y)
                y_pos[current_row] += (40 * current_row) * scale_h
            for event in pygame.event.get():
                Default_event_check(event)
            pygame.display.update()
            mainClock.tick(random.randrange(6, 12, 1))
        return True

    def draw(self, text, name_left, name_right, arg1, arg2, video):
        self.draw_text(text)
        left_button = Button(200, 630, Button_na,
                             Button_a, 1, "sounds/button_sound.wav")
        right_button = Button(1080, 630, Button_na,
                              Button_a, 1, "sounds/button_sound.wav")
        konvert = Button(1080, 450, im_unbox("pismo.png"),
                         im_unbox("otkritoe_pismo.png"), 1, "sounds/button_sound.wav")
        while True:
            for event in pygame.event.get():
                if Default_event_check(event):
                    self.draw_text(text)
            if left_button.draw_button_with_text(name_left):
                return arg1
            if right_button.draw_button_with_text(name_right):
                return arg2
            if video is not None and konvert.draw_button():
                play_video(video)
                self.draw_text(text)
            pygame.display.update()
            mainClock.tick(60)


class Button:
    def __init__(self, x, y, image1, image2, button_scale, sound):
        self.click = False
        self.button_scale = button_scale
        self.x = x
        self.y = y
        self.image1 = image1
        self.image2 = image2
        self.sound = sound

    def update_image(self, image):
        width = image.get_width()
        height = image.get_height()
        image = pygame.transform.scale(image, (int(width * scale_w * self.button_scale),
                                               int(height * scale_h * self.button_scale)))
        self.rect = image.get_rect()
        self.rect.center = (self.x * scale_w, self.y * scale_h)
        return image

    def events(self):
        pos = pygame.mouse.get_pos()
        screen.blit(self.update_image(self.image1), (self.rect.x, self.rect.y))
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 0:
                screen.blit(self.update_image(self.image2), (self.rect.x, self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
            else:
                if self.click:
                    self.click = False
                    return True
        else:
            self.click = False

    def draw_button(self):
        if self.events():
            play_sound(self.sound)
            return True

    def draw_button_with_text(self, text):
        clt = Text_center(text, self.x, self.y)
        if self.events():
            play_sound(self.sound)
            return True
        clt.draw_tc()


class Player:
    def __init__(self, image, x, y, speed):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed

    def player_input_update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed * scale_h
        if keys[pygame.K_s]:
            self.y += self.speed * scale_h
        if keys[pygame.K_a]:
            self.x -= self.speed * scale_w
        if keys[pygame.K_d]:
            self.x += self.speed * scale_w

    def draw(self):
        self.player_input_update()
        draw_image(self.image, self.x, self.y)


# _____________________________________________________________________ #
def main_menu():
    button_game = Button(500, 55, Button_na, Button_a,
                         1, "sounds/button_sound.wav")
    button_options_and_saves = Button(800, 55, Button_na,
                                      Button_a, 1, "sounds/button_sound.wav")
    button_game_history = Button(1100, 55, Button_na,
                                 Button_a, 1, "sounds/button_sound.wav")
    while True:
        draw_image(im_unbox("Main_menu_image.png"), 0, 0)
        if button_game.draw_button_with_text("Game"):
            pass
            game_menu()
        if button_options_and_saves.draw_button_with_text("Options/Saves"):
            options()
        if button_game_history.draw_button_with_text("History"):
            game_text()
            pass
        for event in pygame.event.get():
            Default_event_check(event)
        pygame.display.update()
        mainClock.tick(24)


def game_text(page=1):
    draw_image(im_unbox("Text_big_brother.png"), 0, 0)
    text = ["Welcome in our game comrade. We are glad to see you!", "Do you know something about WW2 history?"
        , "Are you stupid? Did you even open the History book?                        Okay, it doesn't matter anyway, "
          "only lies are written in them. Now we will tell you the truth.", "Excellent comrade!!! But I have to upset "
                                                                            "you, all you know is a lie. But don't be "
                                                                            "upset! Now we will tell you the truth. "
        ,
            "As we all know, at the beginning of the war, Germany was invincible. The allies fell one by one.         "
            "Meanwhile in France:"]
    Pages = Text_pages(im_unbox("Text_big_brother.png"), 420, 60)
    while True:
        if page == 0:
            main_menu()
        if page == 1:
            if Pages.draw_animation_text(text[0]):
                page = Pages.draw(text[0], "Menu", "Next", 0, 2, None)
        if page == 2:
            if Pages.draw_animation_text(text[1]):
                page = Pages.draw(text[1], "No", "Yes", 3, 4, None)
        if page == 3:  # No
            if Pages.draw_animation_text(text[2]):
                page = Pages.draw(text[2], "Previous", "Next", 2, 5, None)
        if page == 4:  # Yes
            if Pages.draw_animation_text(text[3]):
                page = Pages.draw(text[3], "Previous", "Next", 2, 5, None)
        if page == 5:
            if Pages.draw_animation_text(text[4]):
                page = Pages.draw(text[4], "Choose", "Game", 2, 6, "videos/france.mp4")
        if page == 6:
            game_menu()
            main_menu()
        for event in pygame.event.get():
            Default_event_check(event)
        pygame.display.update()
        mainClock.tick(60)


def game_menu():
    button_level_1 = Button(100, 100, im_unbox("Bismarck_button_not_active.png"),
                            im_unbox("Bismarck_button_active.png"), 1, "sounds/button_sound.wav")
    while True:
        draw_image(im_unbox("Game_menu_background_map.png"), 0, 0)
        if button_level_1.draw_button():
            level_1()
        for event in pygame.event.get():
            Default_event_check(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
        pygame.display.update()
        mainClock.tick(60)


def level_1():
    # Bismarck = pygame.image.load("icons_i_bg/Bismarck_test.png").convert()
    sea_back = Animated_background(im_unbox("sea.png"), 3, 500)
    sky_back = Animated_background(im_unbox("sky.png"), 3, 0)
    player_1 = Player(im_unbox("player.png"), 800, 400, 10)
    while True:
        """screen.blit(Bismarck, (x_pos_b, y_pos_b))
        x_pos_b += 0.3"""
        sky_back.animation()
        sea_back.animation()
        player_1.draw()
        for event in pygame.event.get():
            Default_event_check(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False

        pygame.display.update()
        mainClock.tick(120)


def options():
    button_save_1 = Button(1170, 273, Button_na, Button_a, 0.7,
                           "sounds/button_sound.wav")
    button_save_2 = Button(1170, 338, Button_na, Button_a, 0.7,
                           "sounds/button_sound.wav")
    button_save_3 = Button(1170, 403, Button_na, Button_a, 0.7,
                           "sounds/button_sound.wav")
    button_save_4 = Button(1170, 468, Button_na, Button_a, 0.7,
                           "sounds/button_sound.wav")
    button_save_5 = Button(1170, 533, Button_na, Button_a, 0.7,
                           "sounds/button_sound.wav")
    button_minus = Button(165, 537, im_unbox("minus.png"),
                          im_unbox("minus_act.png"), 1, "sounds/button-30.wav")
    button_plus = Button(515, 537, im_unbox("plus.png"),
                         im_unbox("plus_act.png"), 1, "sounds/button-30.wav")
    while True:
        draw_image(im_unbox("options_bg.png"), 0, 0)
        global volume
        dif = 233 + (200 * volume * 5)
        draw_image(im_unbox("kwadrat.png"), dif, 524)
        if button_minus.draw_button() and volume > 0:
            volume -= 0.02
        if button_plus.draw_button() and volume < 0.2:
            volume += 0.02
        if button_save_1.draw_button_with_text("Save 1"):
            pass
        if button_save_2.draw_button_with_text("Save 2"):
            pass
        if button_save_3.draw_button_with_text("Save 3"):
            pass
        if button_save_4.draw_button_with_text("Save 4"):
            pass
        if button_save_5.draw_button_with_text("Save 5"):
            pass
        for event in pygame.event.get():
            Default_event_check(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
        pygame.display.update()
        mainClock.tick(60)


main_menu()
pygame.guit()
