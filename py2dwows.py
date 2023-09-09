from typing import Optional
import arcade, math
from arcade import Texture

window_size = (1300, 800)
window_width = window_size[0]
window_height = window_size[1]
window_title = 'Py2dwows'


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
                 acceleration: float = 1):
        super().__init__(filename, scale, image_x, image_y, image_width,
                         image_height, center_x, center_y, repeat_count_x,
                         repeat_count_y, flipped_horizontally,
                         flipped_vertically, flipped_diagonally,
                         hit_box_algorithm, hit_box_detail, texture, angle)
        self.target_speed = 0
        self.current_speed = 0
        self.max_speed = max_speed
        self.acceleration = acceleration

    def update(self):
        if self.current_speed < self.target_speed:
            self.current_speed += self.acceleration
        elif self.current_speed > self.target_speed:
            self.current_speed -= self.acceleration
        self.center_x += self.current_speed * math.cos(math.radians(
            self.angle))
        self.center_y += self.current_speed * math.sin(math.radians(
            self.angle))
        self.angle += self.change_angle * self.target_speed / 10

        # fix wrong calculation made by python itself
        self.center_x = round(self.center_x, 3)
        self.center_y = round(self.center_y, 3)
        self.angle = round(self.angle, 3)

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
        self.player_ship = Ship(filename='resources/ship.jpg',
                                max_speed=5,
                                acceleration=0.1)
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
            self.player_ship.target_speed += self.player_ship.max_speed / 4
        elif key == arcade.key.S:
            self.player_ship.target_speed -= self.player_ship.max_speed / 4
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