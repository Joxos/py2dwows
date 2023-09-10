import math

import arcade
from config import *
from gear import GEAR, forward_gear, backward_gear


def accelerate(current_speed, acceleration, friction, target_speed):
    if current_speed < 0:
        acceleration, friction = -friction, -acceleration
    loss = target_speed - current_speed
    if loss > 0:
        # increase speed
        if loss >= acceleration:
            return current_speed + acceleration
        else:
            # less than acceleration
            return target_speed
    elif loss < 0:
        # decrease speed
        loss = target_speed - current_speed
        if loss <= friction:
            return current_speed + friction
        else:
            # less than friction
            return target_speed


class Ship(arcade.Sprite):

    def __init__(
            self,
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
            texture: arcade.Texture = None,
            # set default angle to 90 degree
            angle: float = 90,
            # new parameters
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
        self.gear = forward_gear(self.gear)
        self.target_speed = self.max_speed * self.gear.value / 4

    def backward(self):
        self.gear = backward_gear(self.gear)
        self.target_speed = self.max_speed * self.gear.value / 4

    def update(self):
        if self.current_speed < self.target_speed:
            self.current_speed = accelerate(self.current_speed,
                                            self.acceleration, self.friction,
                                            self.target_speed)
        elif self.current_speed > self.target_speed:
            self.current_speed = accelerate(self.current_speed,
                                            self.acceleration, self.friction,
                                            self.target_speed)
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
        if self.center_x < 0:
            self.center_x = 0
        elif self.center_x > window_width - 1:
            self.center_x = window_width - 1

        if self.center_y < 0:
            self.center_y = 0
        elif self.center_y > window_height - 1:
            self.center_y = window_height - 1