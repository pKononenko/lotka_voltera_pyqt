import numpy as np


def voltera_isolines(a, b, c, d, x_data, y_data):
    #isocont = lambda u, v: np.divide(np.exp(d*u + b*v), np.power(u, c) * np.power(v, a))
    isocont = lambda u, v: d*u - c * np.log(u) + b * v - a * np.log(v)

    point_cnt = 100
    x = np.linspace(np.min(x_data), np.max(x_data), point_cnt)
    y = np.linspace(np.min(y_data), np.max(y_data), point_cnt)
    X2, Y2 = np.meshgrid(x, y)
    Z2 = isocont(X2, Y2)

    return X2, Y2, Z2
