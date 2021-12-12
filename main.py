import pygame
import sys
from pygame.locals import *
import moviepy.editor as py
import random

volume = 0.1
scale_w = 1
scale_h = 1
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Glamorous NKWDman')
icon = pygame.image.load("icons_i_bg/nkwdicon.png")
pygame.display.set_icon(icon)
font = pygame.font.SysFont("Times New Roman®", 28)
Button_not_active_image = pygame.image.load("icons_i_bg/Main_button_icon_1.png")
Button_active_image = pygame.image.load("icons_i_bg/Main_button_icon_2.png")
konvert_im1 = pygame.image.load("icons_i_bg/pismo.png")
konvert_im2 = pygame.image.load("icons_i_bg/otkritoe_pismo.png")
option_bg = pygame.image.load("icons_i_bg/options_blyad_pizdec.png")


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


def draw_image(image, x, y):
    width = image.get_width()
    height = image.get_height()
    image = pygame.transform.scale(image, (int(width * scale_w), int(height * scale_h)))
    rect = image.get_rect()
    rect.center = (x * scale_w, y * scale_h)
    screen.blit(image, (x * scale_w, y * scale_h))


def play_video(video):
    clip = py.VideoFileClip(video)
    clip_resized = clip.resize(newsize=(int(1280 * scale_w), int(720 * scale_h)))
    clip_resized.preview()
    global screen
    screen = pygame.display.set_mode((int(1280 * scale_w), int(720 * scale_h)), pygame.RESIZABLE)


class Background:
    def __init__(self, image):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale_w), int(height * scale_h)))


class Static_background(Background):
    def __init__(self, x, y, image):
        super().__init__(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Animated_background(Background):
    def __init__(self, image, dif):
        super().__init__(image)
        self.rect = self.image.get_rect()
        self.dif = dif

    def animation(self, y, image, var=1, x=0):
        super().__init__(image)
        var += int(self.dif * scale_w)
        self.rect.topleft = (x + self.rect.x, y)
        self.rect.x += var
        screen.blit(self.image, (self.rect.x - 1280 * scale_w, self.rect.y * scale_h))
        screen.blit(self.image, (self.rect.x, self.rect.y * scale_h))
        if self.rect.x >= 1280 * scale_w:
            self.rect.x = 0
        self.rect.topleft = (x + self.rect.x, y)


class Text:
    def __init__(self, text, color, x, y, for_button):
        if scale_h < scale_w:
            self.font_size = int(35 * scale_h)
        else:
            self.font_size = int(35 * scale_w)
        self.font_type = pygame.font.SysFont("Times New Roman®", self.font_size)
        self.text = text
        self.textobj = self.font_type.render(text, True, color, )
        self.textrect = self.textobj.get_rect()
        if for_button:
            self.textrect.center = (x, y)
        if not for_button:
            self.textrect.topleft = (x, y)


class Static_text(Text):
    def __init__(self, surface, text, color, x, y, for_button):
        super().__init__(text, color, x, y, for_button)
        surface.blit(self.textobj, self.textrect)


class Animated_text(Static_text, Static_background):
    def __init__(self):
        pass

    def draw(self, text, x, y, image, border=23, count=0, current_row=0):
        rows = [""]
        y_pos = [y]
        for letter in text:
            button_skip = Button_with_text(1050, 500, Button_not_active_image,
                                           Button_active_image, "Skip", 0.75)
            Static_background.__init__(self, 0, 0, image)
            if button_skip.update_button_with_text("sounds/button_sound.wav"):
                break
            rows[current_row] += letter
            for smth in range(current_row + 1):
                Static_text.__init__(self, screen, rows[smth], "black", x * scale_w, y_pos[smth] * scale_h,
                                     False)
            if letter != " ":
                play_sound("sounds/Machine_effect_1.wav")
            count += 1
            if count >= border and letter == " ":
                play_sound("sounds/typewriter-line-break-1.wav")
                current_row += 1
                count = 0
                rows.insert(current_row, "")
                y_pos.insert(current_row, y)
                y_pos[current_row] += (40 * current_row) * scale_h
            for event in pygame.event.get():
                Default_event_check(event)
            pygame.display.update()
            mainClock.tick(random.randrange(6, 12, 1))
        return True


class Static_text_after_animation_xd(Static_text, Static_background):
    def __init__(self):
        pass

    def draw_text(self, text, x, y, image, border=23):
        rows = [""]
        y_pos = [y]
        current_row = 0
        count = 0
        for letter in text:
            Static_background.__init__(self, 0, 0, image)
            rows[current_row] += letter
            for smth in range(current_row + 1):
                Static_text.__init__(self, screen, rows[smth], "black", x * scale_w, y_pos[smth] * scale_h,
                                     False)
            count += 1
            if count >= border and letter == " ":
                current_row += 1
                count = 0
                rows.insert(current_row, "")
                y_pos.insert(current_row, y)
                y_pos[current_row] += (40 * current_row) * scale_h

    def draw(self, text, x, y, image, name_left, name_right, arg1, arg2, video_ex, video):
        self.draw_text(text, x, y, image)
        while True:
            for event in pygame.event.get():
                if Default_event_check(event):
                    self.draw_text(text, x, y, image)
            left_button = Button_with_text(200, 630, Button_not_active_image,
                                           Button_active_image, name_left, 1)
            right_button = Button_with_text(1080, 630, Button_not_active_image,
                                            Button_active_image, name_right, 1)
            konvert = Button_without_text(1080, 450, konvert_im1,
                                          konvert_im2, 1)
            if left_button.update_button_with_text("sounds/button_sound.wav"):
                return arg1
            if right_button.update_button_with_text("sounds/button_sound.wav"):
                return arg2
            if video_ex and konvert.update_button("sounds/button_sound.wav"):
                play_video(video)
                self.draw_text(text, x, y, image)
            pygame.display.update()
            mainClock.tick(60)


class Buttons:
    def __init__(self, image, image2, button_scale):
        self.click = False
        self.button_scale = button_scale
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,
                                            (int(width * scale_w * self.button_scale),
                                             int(height * scale_h * self.button_scale)))
        self.rect = self.image.get_rect()
        width = image2.get_width()
        height = image2.get_height()
        self.image2 = pygame.transform.scale(image2, (
            int(width * scale_w * self.button_scale), int(height * scale_h * self.button_scale)))
        self.rect2 = self.image2.get_rect()


class Button_without_text(Buttons):
    def __init__(self, x, y, image, image2, button_scale):
        super().__init__(image, image2, button_scale)
        self.x = x * scale_w
        self.y = y * scale_h
        self.rect.center = (self.x, self.y)
        self.rect2.center = (self.x, self.y)

    def update_button(self, sound):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 0:
                screen.blit(self.image2, (self.rect2.x, self.rect2.y))
            if pygame.mouse.get_pressed()[0] == 1:
                screen.blit(self.image, (self.rect.x, self.rect.y))
                self.click = True
        if not self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 0 or pygame.mouse.get_pressed()[0] == 1:
                screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.click:
            play_sound(sound)
        return self.click


class Button_with_text(Buttons, Static_text):
    def __init__(self, x, y, image, image2, text, button_scale):
        Buttons.__init__(self, image, image2, button_scale)
        self.x = x * scale_w
        self.y = y * scale_h
        self.rect.center = (self.x, self.y)
        self.rect2.center = (self.x, self.y)
        self.text = text

    def update_button_with_text(self, sound):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 0:
                screen.blit(self.image2, (self.rect2.x, self.rect2.y))
            if pygame.mouse.get_pressed()[0] == 1 and not self.click:
                screen.blit(self.image, (self.rect.x, self.rect.y))
                self.click = True
        if not self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 0 or pygame.mouse.get_pressed()[0] == 1:
                screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.click:
            play_sound(sound)
        Static_text.__init__(self, screen, self.text, (0, 0, 0), self.x, self.y, True)
        return self.click


# "sounds/button_sound.wav"


class Slider:
    def __init__(self):
        plus = pygame.image.load("icons_i_bg/plus.png")
        self.plus_im = plus
        minus = pygame.image.load("icons_i_bg/minus.png")
        self.minus_im = minus
        plus_act = pygame.image.load("icons_i_bg/plus_act.png")
        self.plus_act_im = plus_act
        minus_act = pygame.image.load("icons_i_bg/minus_act.png")
        self.minus_act_im = minus_act
        kwadrat = pygame.image.load("icons_i_bg/kwadrat.png")
        self.kwadrat_im = kwadrat

    def draw(self):
        global volume
        button_minus = Button_without_text(165, 537, self.minus_im,
                                           self.minus_act_im, 1)
        button_plus = Button_without_text(515, 537, self.plus_im,
                                          self.plus_act_im, 1)
        dif = 233 + (200 * volume * 5)
        draw_image(self.kwadrat_im, dif, 524)
        if button_minus.update_button("sounds/button-33a.wav"):
            if volume > 0:
                volume -= 0.002
        if button_plus.update_button("sounds/button-33a.wav"):
            if volume < 0.2:
                volume += 0.002


class Player:
    def __init__(self, image):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale_w), int(height * scale_h)))
        self.rect = self.image.get_rect()

    def draw(self, x, y):
        self.rect.topleft = (x, y)

    def animation(self, x_dir, y_dir):
        blit_pos_x = self.rect.x + x_dir
        blit_pos_y = self.rect.y + y_dir
        screen.blit(self.image, (blit_pos_x, blit_pos_y))

    def player_input_update(self, x_move, y_move, start_x, start_y, exist=True):
        # self.__init__(self.image)
        if exist:
            self.draw(start_x, start_y)
            exist = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.animation(0, y_move)
        if keys[pygame.K_s]:
            self.animation(0, -y_move)
        if keys[pygame.K_a]:
            self.animation(-x_move, 0)
        if keys[pygame.K_d]:
            self.animation(x_move, 0)
        else:
            self.animation(0, 0)


# _____________________________________________________________________ #
def main_menu():
    Main_menu_bg_im = pygame.image.load("icons_i_bg/Main_menu_image.png")
    Main_menu_bg = Static_background(0, 0, Main_menu_bg_im)
    while True:
        button_game = Button_with_text(500, 55, Button_not_active_image, Button_active_image,
                                       "Game", 1)
        button_options_and_saves = Button_with_text(800, 55, Button_not_active_image,
                                                    Button_active_image, "Options/Saves", 1)
        button_game_history = Button_with_text(1100, 55, Button_not_active_image,
                                               Button_active_image, "History", 1)
        Main_menu_bg.__init__(0, 0, Main_menu_bg_im)
        if button_game.update_button_with_text("sounds/button_sound.wav"):
            game_menu()
        if button_options_and_saves.update_button_with_text("sounds/button_sound.wav"):
            options()
        if button_game_history.update_button_with_text("sounds/button_sound.wav"):
            game_text()
        for event in pygame.event.get():
            Default_event_check(event)
        pygame.display.update()
        mainClock.tick(24)


def game_text(page=1):
    Text_menu_bg_im = pygame.image.load("icons_i_bg/Text_big_brother.png")
    text_bg = Static_background(0, 0, Text_menu_bg_im)
    text_bg.__init__(0, 0, Text_menu_bg_im)
    text = ["Welcome in our game comrade. We are glad to see you!", "Do you know something about WW2 history?"
        , "Are you stupid? Did you even open the History book?                        Okay, it doesn't matter anyway, "
          "only lies are written in them. Now we will tell you the truth.", "Excellent comrade!!! But I have to upset "
                                                                            "you, all you know is a lie. But don't be "
                                                                            "upset! Now we will tell you the truth. "
        ,
            "As we all know, at the beginning of the war, Germany was invincible. The allies fell one by one.         "
            "Meanwhile in France:"]
    text_animation = Animated_text()
    text_static = Static_text_after_animation_xd()
    while True:
        if page == 0:
            main_menu()
        if page == 1:
            if text_animation.draw(text[0], 420, 60, Text_menu_bg_im):
                page = text_static.draw(text[0], 420, 60, Text_menu_bg_im, "Menu", "Next", 0, 2, False, None)
        if page == 2:
            if text_animation.draw(text[1], 420, 60, Text_menu_bg_im):
                page = text_static.draw(text[1], 420, 60, Text_menu_bg_im, "No", "Yes", 3, 4, False, None)
        if page == 3:  # No
            if text_animation.draw(text[2], 420, 60, Text_menu_bg_im):
                page = text_static.draw(text[2], 420, 60, Text_menu_bg_im, "Previous", "Next", 2, 5, False, None)
        if page == 4:  # Yes
            if text_animation.draw(text[3], 420, 60, Text_menu_bg_im):
                page = text_static.draw(text[3], 420, 60, Text_menu_bg_im, "Previous", "Next", 2, 5, False, None)
        if page == 5:
            if text_animation.draw(text[4], 420, 60, Text_menu_bg_im):
                page = text_static.draw(text[4], 420, 60, Text_menu_bg_im, "Choose", "Game", 2, 6, True, "videos/france"
                                                                                                         ".mp4")
        if page == 6:
            game_menu()
            main_menu()
            '''if text_animation.draw(text[0], 420, 60, Text_menu_bg_im):
                page = text_static.draw(text[0], 420, 60, Text_menu_bg_im, "Menu", "Next", 0, 2)
        if page == 7:
            if text_animation.draw(text[0], 420, 60, Text_menu_bg_im):
                page = text_static.draw(text[0], 420, 60, Text_menu_bg_im, "Menu", "Next", 0, 2)
        if page == 8:
            if text_animation.draw(text[0], 420, 60, Text_menu_bg_im):
                page = text_static.draw(text[0], 420, 60, Text_menu_bg_im, "Menu", "Next", 0, 2)
        if page == 9:
            if text_animation.draw(text[0], 420, 60, Text_menu_bg_im):
                page = text_static.draw(text[0], 420, 60, Text_menu_bg_im, "Menu", "Next", 0, 2)
        if page == 10:
            if text_animation.draw(text[0], 420, 60, Text_menu_bg_im):
                page = text_static.draw(text[0], 420, 60, Text_menu_bg_im, "Menu", "Next", 0, 2)'''
        for event in pygame.event.get():
            Default_event_check(event)
        pygame.display.update()
        mainClock.tick(60)


def game_menu():
    button_level_1_image_not_active = pygame.image.load("icons_i_bg/Bismarck_button_not_active.png")
    button_level_1_image_active = pygame.image.load("icons_i_bg/Bismarck_button_active.png")
    map_game_menu = pygame.image.load("icons_i_bg/Game_menu_background_map.png").convert()
    map_game_menu_bg = Static_background(0, 0, map_game_menu)
    while True:
        button_level_1 = Button_without_text(100, 100, button_level_1_image_not_active, button_level_1_image_active, 1)
        map_game_menu_bg.__init__(0, 0, map_game_menu)
        if button_level_1.update_button("sounds/button_sound.wav"):
            level_1()
        for event in pygame.event.get():
            Default_event_check(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
        pygame.display.update()
        mainClock.tick(60)


def level_1():
    sky = pygame.image.load("icons_i_bg/sky.png").convert()
    # Bismarck = pygame.image.load("icons_i_bg/Bismarck_test.png").convert()
    sea = pygame.image.load("icons_i_bg/sea.png").convert()
    player = pygame.image.load("icons_i_bg/player.png").convert()
    sea_back = Animated_background(sea, 1)
    sky_back = Animated_background(sky, 1)
    player_1 = Player(player)
    while True:
        """screen.blit(Bismarck, (x_pos_b, y_pos_b))
        x_pos_b += 0.3"""
        sky_back.animation(0, sky)
        sea_back.animation(500, sea)
        player_1.player_input_update(100, 100, 450, 450)
        for event in pygame.event.get():
            Default_event_check(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False

        pygame.display.update()
        mainClock.tick(120)


def options():
    bg = Static_background(0, 0, option_bg)
    while True:
        bg.__init__(0, 0, option_bg)
        button_save_1 = Button_with_text(1170, 273, Button_not_active_image, Button_active_image,
                                         "Save 1", 0.7)
        button_save_2 = Button_with_text(1170, 338, Button_not_active_image,
                                         Button_active_image, "Save 2", 0.7)
        button_save_3 = Button_with_text(1170, 403, Button_not_active_image,
                                         Button_active_image, "Save 3", 0.7)
        button_save_4 = Button_with_text(1170, 468, Button_not_active_image,
                                         Button_active_image, "Save 4", 0.7)
        button_save_5 = Button_with_text(1170, 533, Button_not_active_image,
                                         Button_active_image, "Save 5", 0.7)
        slider = Slider()
        slider.draw()
        button_save_1.update_button_with_text("sounds/button_sound.wav")
        button_save_2.update_button_with_text("sounds/button_sound.wav")
        button_save_3.update_button_with_text("sounds/button_sound.wav")
        button_save_4.update_button_with_text("sounds/button_sound.wav")
        button_save_5.update_button_with_text("sounds/button_sound.wav")
        for event in pygame.event.get():
            Default_event_check(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
        pygame.display.update()
        mainClock.tick(60)


main_menu()
pygame.guit()
