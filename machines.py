import math

import numpy as np
import matplotlib.pyplot as plt
# from scipy.optimize import minimize_scalar


class Trebuchet:
    def __init__(self, arm_ratio, frame_height, arm_length):
        self.arm_ratio = arm_ratio          # Доля рычага, относящаяся к весу
        self.frame_height = frame_height    # Высота вала
        self.arm_length = arm_length        # Длина рычага
        self.missile_arm_length = arm_length * (1 - arm_ratio)
        self.weight_arm_length = arm_length * arm_ratio
        self.g = 9.80665
        self.missile_coordinates = None

    def launch_parameters(self, distance, rad_angle):
        self.missile_x = -np.cos(rad_angle) * self.missile_arm_length
        self.missile_y = -np.sin(rad_angle) * self.missile_arm_length + self.frame_height

        self.weight_x = np.cos(rad_angle) * self.weight_arm_length
        self.weight_y = np.sin(rad_angle) * self.weight_arm_length + self.frame_height

        print(f"Missile start point: ({self.missile_x}; {self.missile_y})")
        print(f"Weight start point: ({self.weight_x}; {self.weight_y})")

        x_move = -self.missile_x + distance
        numerator = self.g * (x_move ** 2)
        denomenator = 2 * (np.cos(rad_angle) ** 2) * (self.missile_y + x_move * np.tan(rad_angle))
        v0 = math.sqrt(numerator / denomenator)

        print(f"Launching missile with angle: {np.degrees(rad_angle):.2f} degrees and v0: {v0:.2f} m/s")
        return v0

    def trajectory(self, v0, angle):
        v_y = v0 * np.sin(angle)
        v_x = v0 * np.cos(angle)
        print(f"Vx: {v_x}, Vy: {v_y}")

        first_path_time = v_y / self.g                      # Время до достижения наивысшей точки
        max_y = self.missile_y + v_y * first_path_time - 0.5 * self.g * (first_path_time ** 2)

        second_path_time = math.sqrt((2 * max_y) / self.g)    # Время от высшей точки до падения
        total_time = first_path_time + second_path_time     # Общее время полета

        print(f"Flight time: {total_time} s, x_move: {v_x * total_time} m, y_move: {self.missile_y + v_y * total_time - 0.5 * self.g * (total_time)**2} m")

        t = np.linspace(0, total_time, num=1000)            # Временные точки
        x = self.missile_x + v_x * t                        # Положение по x
        y = self.missile_y + v_y * t - 0.5 * self.g * t**2  # Положение по y

        return t, x, y

    def visualize(self, distance, angle=None):
        rad_angle = np.radians(angle % 90)
        v0 = self.launch_parameters(distance, rad_angle)
        t, x, y = self.trajectory(v0, rad_angle)

        plt.figure(figsize=(10, 5))
        plt.plot([0, 0], [0, self.frame_height], label='Станина', color="black")
        plt.plot([self.missile_x, 0], [self.missile_y, self.frame_height], label='Метательный рычаг', color='red')
        plt.plot([0, self.weight_x], [self.frame_height, self.weight_y], label='Рычаг противовеса', color='green')

        plt.plot(self.missile_x, self.missile_y, marker='o', color='red')
        plt.plot(0, self.frame_height, marker='o', color='black')
        plt.plot(self.weight_x, self.weight_y, marker='o', color='green')

        plt.plot(x, y, label='Траектория', color='blue')
        plt.xlabel('Дистанция (м)')
        plt.ylabel('Высота (м)')
        plt.title('Траектория полета снаряда требушета')

        plt.grid(True)
        plt.axis('equal')
        plt.legend()
        # plt.xticks(np.arange(0, plt.xlim()[1], 0.1))
        plt.show()