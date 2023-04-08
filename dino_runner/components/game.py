import pygame
from dino_runner.components.menu import Menu
from dino_runner.components.obstacles.obstacle_manager import ObstableManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

from dino_runner.utils.constants import BG, DEFAULT_TYPE, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.dinosaur import Dinosaur

class Game:
    GAME_SPEED = 20
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = self.GAME_SPEED
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstableManager()
        self.menu = Menu(self.screen)
        self.running = False
        self.score = 0
        self.max_score = 0
        self.death_counts = 0
        self.power_up_manager = PowerUpManager()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.game_speed = self.GAME_SPEED
        self.reset_game()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.power_up_manager.dropped_hammer(self, user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self)


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_max_score()
        self.power_up_manager.draw(self.screen)
        self.draw_power_up()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self):
        self.menu.reset_screen_color(self.screen)
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2
        self.screen.blit(ICON, (half_screen_width - 50, half_screen_height - 140))
        if self.death_counts == 0:
            self.menu.draw(self.screen, "Press any key to start")
        else:
            self.menu.draw(self.screen, "GAME OVER! PRESS ANY KEY TO PLAY AGAIN")
            self.draw_score()
            self.draw_max_score()
            self.draw_death_count()
        self.menu.update(self)

    def update_score(self):
        self.score +=1 
        if self.score % 100 == 0 and self.game_speed < 500:
            self.game_speed += 1

    def draw_score(self):
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        text_rect = text.get_rect()
        if self.playing:
            text_rect.center = (700, 50)
        else:
            text_rect.center = (half_screen_width - 240, half_screen_height - 240)
        self.screen.blit(text,text_rect)
    
    def cal_max_score(self):
        if self.score > self.max_score:
            self.max_score = self.score
        return self.max_score    
    
    def draw_max_score(self):
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Max Score: {self.cal_max_score()}', True, (0, 0, 0))
        text_rect = text.get_rect()
        if self.playing:
            text_rect.center = (950, 50)
        else:
            text_rect.center = (half_screen_width + 240, half_screen_height - 240)
        self.screen.blit(text,text_rect)

    def draw_death_count(self):
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Death counts: {self.death_counts}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (half_screen_width, half_screen_height + 240)
        self.screen.blit(text,text_rect)

    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.game_speed = self.GAME_SPEED
        self.score = 0
        self.power_up_manager.reset_power_ups()
        self.player.reset()
        self.player.has_power_up = False

    def draw_power_up(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks())/1000, 2)
            if time_to_show >= 0:
                self.menu.draw(self.screen, f'{self.player.type.capitalize()} enable for {time_to_show} seconds', 500, 500) 
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE