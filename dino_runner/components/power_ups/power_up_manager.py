import pygame
import random
from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.dinosaur import Dinosaur

from dino_runner.utils.constants import SHIELD_TYPE, HAMMER_TYPE, DEFAULT_TYPE





class PowerUpManager:


    def __init__(self):
        self.power_ups = []
        self.hammer = []
        self.duration = random.randint(3, 5)
        self.when_appears = random.randint(50, 70)
        self.drop_hammer = False

    def update(self, game):
        if len(self.power_ups) == 0 and self.when_appears == game.score:
           self.generate_power_up()
        
        if len(self.hammer) == 1:
            self.hammer[0].drop_update(game.game_speed, self.power_ups)
            
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
        
            if game.player.dino_rect.colliderect(power_up.rect): 
                power_up.start_time = pygame.time.get_ticks()
                game.player.has_power_up = True
                
                if self.power_up_type == 0:
                    game.player.type = SHIELD_TYPE
                elif self.power_up_type == 1:
                    game.player.type = HAMMER_TYPE
                    self.hammer.append(Hammer())
                game.player.power_up_time = power_up.start_time + (self.duration * 1000)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)
        
        if len(self.hammer) == 1:
            if self.drop_hammer == True:
                self.hammer[0].draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.hammer = []
        self.when_appears = random.randint(50, 70)

    def generate_power_up(self):
        self.power_up_type = random.randint(0, 1)
        self.when_appears += random.randint(200, 300)
        if self.power_up_type == 0:
            power_up = Shield()
            self.power_ups.append(power_up)
        elif self.power_up_type == 1:
            power_up = Hammer()
            self.power_ups.append(power_up)

    def dropped_hammer(self, game, user_input):
        if game.player.type == HAMMER_TYPE and user_input [pygame.K_SPACE]:
                game.player.type = DEFAULT_TYPE
                self.drop_hammer = True
                game.player.has_power_up = False
                self.hammer[0].rect.x = game.player.X_POS
                self.hammer[0].rect.y = game.player.dino_rect.y


