from ship import Ship
import arcade
from config import *


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
                                acceleration=0.01,
                                friction=-0.03,
                                scale=0.167)
        self.player_ship.center_x = 50
        self.player_ship.center_y = 50
        self.ship_list.append(self.player_ship)

    def on_draw(self):
        self.clear()
        self.ship_list.draw()
        arcade.draw_text(f'Gear: {self.player_ship.gear.name}',
                         10,
                         window_height - 22,
                         font_size=12,
                         align='left')
        arcade.draw_text(
            f'Gear speed: {round(self.player_ship.target_speed,round_digits)}',
            10,
            window_height - 22 * 2,
            font_size=12,
            align='left')
        arcade.draw_text(
            f'Current speed: {round(self.player_ship.current_speed,round_digits)}',
            10,
            window_height - 22 * 3,
            font_size=12,
            align='left')

    def on_update(self, delta_time):
        self.ship_list.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player_ship.forward()
        elif key == arcade.key.S:
            self.player_ship.backward()
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