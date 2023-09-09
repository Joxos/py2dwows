from typing import Literal
import arcade, math
from arcade import Texture
from config import *
from enum import Enum

window_size = (1300, 800)
window_width = window_size[0]
window_height = window_size[1]
window_title = 'Py2dwows'
view_scale = 1  # 1: 1 nmile


class GEAR(Enum):
    REVERSE = -1
    NEUTRAL = 0
    SLOW = 1
    HALF = 2
    FAST = 3
    FULL = 4


class Ship(arcade.Sprite):

    def __init__(self,
                 filename: str = None,
                 scale: float = 1,
                 image_x: float = 0,
                 image_y: float = 0,
                 image_width: float = 0,
                 image_height: float = 0,
                 center_x: float = 0,
                 center_y: float = 0,
                 repeat_count_x: int = 1,
                 repeat_count_y: int = 1,
                 flipped_horizontally: bool = False,
                 flipped_vertically: bool = False,
                 flipped_diagonally: bool = False,
                 hit_box_algorithm: str | None = "Simple",
                 hit_box_detail: float = 4.5,
                 texture: Texture = None,
                 angle: float = 0,
                 max_speed: float = 10,
                 acceleration: float = 1,
                 friction: float = 1):
        super().__init__(filename, scale, image_x, image_y, image_width,
                         image_height, center_x, center_y, repeat_count_x,
                         repeat_count_y, flipped_horizontally,
                         flipped_vertically, flipped_diagonally,
                         hit_box_algorithm, hit_box_detail, texture, angle)
        self.gear: GEAR = GEAR.NEUTRAL
        self.target_speed = 0
        self.current_speed = 0
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.friction = friction

    def forward(self):
        if self.gear < 4:
            self.gear += 1
        if self.gear == GEAR.NEUTRAL:
            # exclude division by zero
            self.target_speed = 0
        else:
            self.target_speed = self.max_speed / self.gear
        print(f'Now in {self.gear.name}')

    def backward(self):
        if self.gear > -1:
            self.gear -= 1
        if self.gear == GEAR.NEUTRAL:
            # exclude division by zero
            self.target_speed = 0
        else:
            self.target_speed = self.max_speed / self.gear
        print(f'Now in {self.gear.name}')

    def update(self):
        if self.current_speed < self.target_speed:
            loss = self.target_speed - self.current_speed
            if loss >= self.acceleration:
                self.current_speed += self.acceleration
            else:
                self.current_speed = self.target_speed
        elif self.current_speed > self.target_speed:
            loss = self.current_speed - self.target_speed
            if loss >= self.friction:
                self.current_speed -= self.friction
            else:
                self.current_speed = self.target_speed
        self.center_x += self.current_speed * math.cos(math.radians(
            self.angle))
        self.center_y += self.current_speed * math.sin(math.radians(
            self.angle))
        self.angle += self.change_angle * self.current_speed / 10

        # fix wrong calculation made by python itself
        self.center_x = round(self.center_x, round_digits)
        self.center_y = round(self.center_y, round_digits)
        self.angle = round(self.angle, round_digits)

        # boarder
        if self.left < 0:
            self.left = 0
        elif self.right > window_width - 1:
            self.right = window_width - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > window_height - 1:
            self.top = window_height - 1


class Py2dwows(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.ship_list = []
        self.player_ship = None

        arcade.set_background_color(arcade.color.AZURE)

    def setup(self):
        self.ship_list = arcade.SpriteList()
        self.player_ship = Ship(filename='resources/myoko.jpg',
                                max_speed=9,
                                acceleration=0.1,
                                friction=0.085,
                                scale=0.167)
        self.player_ship.center_x = 50
        self.player_ship.center_y = 50
        self.ship_list.append(self.player_ship)

    def on_draw(self):
        self.clear()
        self.ship_list.draw()

    def on_update(self, delta_time):
        self.ship_list.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player_ship.target_speed += round(
                self.player_ship.max_speed / 4, round_digits)
        elif key == arcade.key.S:
            self.player_ship.target_speed -= round(
                self.player_ship.max_speed / 4, round_digits)
        elif key == arcade.key.Q:
            self.player_ship.change_angle += 1
        elif key == arcade.key.E:
            self.player_ship.change_angle += -1


def main():
    window = Py2dwows(window_width, window_height, window_title)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()