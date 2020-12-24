import numpy as np
import matplotlib.pyplot as plt
import time


def runge_calc(a, b, c, d, x, y, t1, t2, h):
    t_list = np.arange(t1, t2, h)
    if t_list[-1] != t2:
        t_list = np.append(t_list, t2)
    x_data = np.zeros(len(t_list))
    y_data = np.zeros(len(t_list))

    f1 = lambda x, y: -c * y + d * x * y
    f2 = lambda x, y: a * x - b * x * y
    x_data[0] = x
    y_data[0] = y

    for i in range(1, len(t_list)):
        k1 = h * f1(x, y)
        q1 = h * f2(x, y)
        k2 = h * f1(x + q1/2, y + k1/2)
        q2 = h * f2(x + q1/2, y + k1/2)
        k3 = h * f1(x + q2/2, y + k2/2)
        q3 = h * f2(x + q2/2, y + k2/2)
        k4 = h * f1(x + q3, y + k3)
        q4 = h * f2(x + q3, y + k3)

        x += (q1 + 2 * q2 + 2 * q3 + q4) / 6
        y += (k1 + 2 * k2 + 2 * k3 + k4) / 6

        x_data[i] = x
        y_data[i] = y

    return t_list, y_data, x_data


def voltera_time(a, b, c, d, x0, y0, t1, t2, eps = 0.001):
    # Визначимо h
    h = np.sqrt(np.sqrt(eps))
    R = 1
    t_list, yh, xh = runge_calc(a, b, c, d, x0, y0, t1, t2, h)

    while R > eps:
        #t_list, yh, xh = runge_calc(a, b, c, d, x0, y0, t1, t2, h)
        t_list2, yh2, xh2 = runge_calc(a, b, c, d, x0, y0, t1, t2, h / 2)

        R1 = abs(xh[-1] - xh2[-1]) / 15
        R2 = abs(yh[-1] - yh2[-1]) / 15
        R = max(R1, R2)
        h = h / 2
        t_list, yh, xh = t_list2, yh2, xh2

    return t_list2, xh2, yh2

'''if __name__ == "__main__":
    time1 = time.time()
    t_list, x_data, y_data = voltera_time(1.58, 1.94, 1.19, 0.63, 2.85, 1.85, 9, 39.5, 0.001)
    print(time.time() - time1)
    plt.plot(t_list, x_data, 'r', label = 'prey', linewidth = 2)
    plt.plot(t_list, y_data, label = 'predator', linewidth = 2)
    plt.legend()
    plt.show()'''
