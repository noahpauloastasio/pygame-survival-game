import pygame
from settings import *

class Menu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont("agencyfb", 50)
        self.title_font = pygame.font.SysFont("agencyfb", 70)


        self.buttons = {
            "play": pygame.Rect(540, 350, button_width, button_height),
            "guide": pygame.Rect(540, 450, button_width, button_height),
            "settings": pygame.Rect(540, 550, button_width, button_height)
        }

        self.back_button = pygame.Rect(20, 20, 40, 40)
        self.background = pygame.transform.scale(pygame.image.load("../graphics/city-ruin-backgrounds/background 1/orig.png").convert(), (1280, 720))

        self.diff_rect = pygame.Rect(0, 0, 0, 0)

        self.fullscreen = False
        self.fullscreen_rect = pygame.Rect(0, 0, 0, 0)

    def draw(self):
        # background colour for the menu
        self.screen.blit(self.background, (0, 0))
        # game title
        text = self.title_font.render("One More Day", True, GREY)
        self.screen.blit(text, (485,30))

        # draw each button
        for button in self.buttons:
            rect = self.buttons[button]

            pygame.draw.rect(self.screen, UI_BG_COLOUR, rect)
            pygame.draw.rect(self.screen, BORDER_COLOUR, rect, 4)

            # text for the button
            text = self.font.render(button.capitalize(), True, WHITE)

            # position text inside the button
            text_x = rect.x + 30
            text_y = rect.y - 3

            self.screen.blit(text, (text_x, text_y))


    def draw_settings(self):
        self.screen.blit(self.background, (0, 0))

        # back arrow (triangle)
        pygame.draw.polygon(self.screen, GREY, [(40, 20), (20, 40), (40, 60)])

        text = self.font.render("Settings", True, BLACK)
        self.screen.blit(text, (100, 100))
        # difficulty
        current_diff = self.game.difficulties[self.game.diff_index]
        difficulty_text = self.font.render(f"Difficulty: {current_diff}", True, BLACK)
        self.diff_rect = difficulty_text.get_rect(topleft=(100, 200))
        self.screen.blit(difficulty_text, self.diff_rect)
        # fullscreen
        fullscreen_text = self.font.render(f"Fullscreen: {'On' if self.fullscreen else 'Off'}", True, BLACK)
        self.fullscreen_rect = fullscreen_text.get_rect(topleft=(100, 300))
        self.screen.blit(fullscreen_text, self.fullscreen_rect)



    def draw_guide(self):
        self.screen.blit(self.background, (0, 0))
        pygame.draw.polygon(self.screen, GREY, [(40, 20), (20, 40), (40, 60)])

        text = self.font.render("Guide", True, GREY)
        self.screen.blit(text, (100, 40))
        tips = [
            "Use arrow keys to move around",
            "Defeat zombies to gain exp and advance to the next day",
            "Use consumables to replensih health",
            "Press ESC to pause game and open menu"
        ]

        y_offset = 200
        for tip in tips:
            text = self.font.render(f"- {tip}", True, BLACK)
            self.screen.blit(text, (80, y_offset))
            y_offset += 80


    def check_click(self, pos):
        # go through each button and see if the mouse is inside it
        for button in self.buttons:
            rect = self.buttons[button]
            if rect.collidepoint(pos):
                return button

        return None

    def change_difficulty(self):
        self.current_index = (self.current_index + 1) % len(self.difficulties)
        new_diff = self.difficulties[self.current_index]
        self.set_difficulty(new_diff)
    