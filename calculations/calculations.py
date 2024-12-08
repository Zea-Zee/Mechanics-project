import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

G = 9.81

def calculate_r(m1, m2, ma, h, l, a1, a2, is_shift=False, visualize=False):
    '''
    m1 - mass of projectile \n
    m2 - mass of counterweight \n
    ma - mass of lever \n
    h - height of mount \n
    l - length of lever \n
    a1 - start angle \n
    a2 - finish angle (Measured in the opposite direction from the starting point) \n
    shift - difference between middle of trebushet and position of throw \n
    visualise - visualise trajectory \n
    '''
    
    a1r = np.radians(a1)
    a2r = np.radians(a2)

#----------------------------------------------------------------------------------------------
    speed = np.sqrt((2*G*l*(np.cos(a1r) + np.cos(a2r))*(m2-m1))/(m1+m2))
#----------------------------------------------------------------------------------------------

    print('Скорость вылета:', speed)
    
    t1 = (2*speed*np.sin(a2r))/G
    x1 = t1*speed*np.cos(a2r)
    
    heigth_of_launch = h + l*np.cos(a2r)
    D = (2*speed*np.sin(a2r))**2 + 8*G*(heigth_of_launch)
    t2 = (-2*speed*np.sin(a2r) + np.sqrt(D))/(2*G)    
    x2 = speed*np.cos(a2r)*t2
    
    print('Время полёта:', t1+t2)
    
    length = x1+x2
    if is_shift:
        shift = l * np.sin(a2r)
        length -= shift
    else:
        shift = 0
    print(f'Дистанция (m1={m1}, m2={m2}) = {length*100:.1f}cm')

    if visualize:
        t1_arr = np.linspace(0, t1+t2, num=10000, endpoint=False)
        x1_arr = speed*np.cos(a2r)*t1_arr - shift
        y1_arr = speed*np.sin(a2r)*t1_arr - 1/2*G*(t1_arr**2) + heigth_of_launch
        plt.figure(figsize=(12,8))
        plt.plot(x1_arr, y1_arr, color='blue', label='Траектория полета')
        plt.scatter(x1_arr[np.where(y1_arr == np.max(y1_arr))][0], np.max(y1_arr), color='red', s=25, zorder=10, label=f'Максимальный Y={np.max(y1_arr):.3f} м (X={x1_arr[np.where(y1_arr == np.max(y1_arr))][0]:.3f})')
        plt.scatter(x1_arr[-1], 0, color='green', s=25, zorder=10, label=f'Максимальный X={x1_arr[-1]:.3f} м')

        plt.plot([0, 0], [0, h], label='Станина', color="black")

        plt.plot([-l*np.sin(a2r), 0], [h+l*np.cos(a2r), h], label='Метательный рычаг (момент вылета)', color='red')
        plt.plot([0, l*np.sin(a2r)], [h, h-l*np.cos(a2r)], label='Рычаг противовеса (момент вылета)', color='green')

        plt.plot([-l*np.sin(a1r), 0], [h-l*np.cos(a1r), h], label='Метательный рычаг (начальный момент)', color='red', linestyle='--', alpha=0.8)
        plt.plot([0, l*np.sin(a1r)], [h, h+l*np.cos(a1r)], label='Рычаг противовеса (начальный момент)', color='green', linestyle='--', alpha=0.8)

        plt.plot(0, h, marker='o', color='black')
        plt.plot(-l*np.sin(a2r), h+l*np.cos(a2r), marker='o', zorder=10, color='red')
        plt.plot(l*np.sin(a2r), h-l*np.cos(a2r), marker='o', zorder=10, color='green')
        plt.plot(-l*np.sin(a1r), h-l*np.cos(a1r), marker='o', zorder=10, color='red', alpha=0.8)
        plt.plot(l*np.sin(a1r), h+l*np.cos(a1r), marker='o', zorder=10, color='green', alpha=0.8)

        pre_release_t = np.linspace(np.radians(270-a1), np.radians(90+a2), num=1000)
        pre_release_x = np.cos(pre_release_t) * l
        pre_release_y = h + np.sin(pre_release_t) * l
        plt.plot(pre_release_x, pre_release_y, label='Траектория до вылета', color='blue', linestyle='--', alpha=0.8)

        plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
        plt.axvline(0, color='black', linestyle='--', linewidth=0.8)
        plt.xlabel('Дистанция (м)')
        plt.ylabel('Высота (м)')
        plt.legend(loc='upper right')
        plt.grid()
        plt.axis('equal')
        plt.show()

    return length

def main():
    ball = 0.0168
    jump_ball = 0.0111
    fixing = 0.009 + 0.0025 + 0.0025 * 2 #= 0.0165
    backet = [0.010, 0.027, 0.043, 0.060, 0.077]
    lever_mass = 0.019
    frame_mass = 0.066

    # Длины в метрах
    lever_length = 0.125
    frame_heigth = 0.151
    bruss_heigth = 0.015

    # Углы в градусах
    alpha = 33
    beta = 35

    parser = argparse.ArgumentParser()
    parser.add_argument("--m1", default=jump_ball,
                        help="Масса снаряда.", type=float)
    
    parser.add_argument("--m2", default=backet[3]+fixing,
                        help="Масса противовеса.", type=float)
    
    parser.add_argument("--ma", default=lever_mass,
                        help="Масса рычага.", type=float)
    
    parser.add_argument("--h", default=frame_heigth + bruss_heigth,
                        help="Высота оси вращения.", type=float)
    
    parser.add_argument("--l", default=lever_length,
                        help="Длина плеча (от оси до края рычага).", type=float)
    
    parser.add_argument("--alpha", default=alpha,
                        help="Начальный угол.", type=float)
    
    parser.add_argument("--beta", default=beta,
                        help="Угол вылета.", type=float)
    
    parser.add_argument("--is_shift", default=True,
                        help="Учитывать ли смещение точки вылета по X относительно оси вращения.", type=bool)
    
    parser.add_argument("--visualize", default=True,
                        help="Выводить ли визуализацию.", type=bool)
    
    m1 = parser.parse_args().m1
    m2 = parser.parse_args().m2
    ma = parser.parse_args().ma
    h = parser.parse_args().h
    l = parser.parse_args().l
    a1 = parser.parse_args().alpha
    a2 = parser.parse_args().beta
    is_shift = parser.parse_args().is_shift
    visualize = parser.parse_args().visualize
    
    calculate_r(m1, m2, ma, h, l, a1, a2, is_shift, visualize)

if __name__ == "__main__":
    main()