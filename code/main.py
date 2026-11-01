import pygame, sys
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

from settings import *
from level import Level
from menu import Menu

class Game:
    def __init__(self):


        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('One More Day')
        self.clock = pygame.time.Clock()

        # difficulty
        self.difficulty = "Normal"
        self.difficulty_multiplier = 1.0
        self.difficulties = ["Easy", "Normal", "Hard"]
        self.diff_index =  1

        # create level instance
        self.level = Level(self.difficulty_multiplier)

        # background music
        pygame.mixer.music.load("../audio/no-im-not-human-theme-made-with-Voicemod.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1) # loops the audio

    def set_difficulty(self):
        self.diff_index = (self.diff_index + 1) % len(self.difficulties)
        self.difficulty = self.difficulties[self.diff_index]
        

        if self.difficulty == "Easy":
            self.difficulty_multiplier = 0.5
        elif self.difficulty == "Normal":
            self.difficulty_multiplier = 1.0
        elif self.difficulty == "Hard":
            self.difficulty_multiplier = 2.0


    def run(self):
        menu = Menu(self.screen, self)
        game_state = 'menu'
        while True:
            # handle quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if game_state =='menu':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clicked = menu.check_click(event.pos)
                        if clicked == 'play':
                            game_state = 'play'
                        elif clicked == 'guide':
                            game_state = 'guide'
                        elif clicked == 'settings':
                            game_state = 'settings'

                if game_state == 'guide' or game_state == 'settings':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if menu.back_button.collidepoint(event.pos):
                            game_state = 'menu'

                if game_state == 'settings':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if menu.diff_rect.collidepoint(event.pos):
                            self.set_difficulty()

                        if menu.fullscreen_rect.collidepoint(event.pos):
                            menu.fullscreen = not menu.fullscreen

                            if menu.fullscreen:
                                # set fullscreen
                                pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                            else:
                                # window
                                pygame.display.set_mode((WIDTH, HEIGHT))

            if game_state == 'menu':
                menu.draw()

            elif game_state == 'play':
                # update game visuals
                self.screen.fill((101,117,96))
                self.level.run()          # Level handles updating + drawing
                self.clock.tick(FPS)      # limit FPS

            elif game_state == 'guide':
                menu.draw_guide()

            elif game_state == 'settings':
                menu.draw_settings()

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
