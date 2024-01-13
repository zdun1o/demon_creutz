import numpy as np
import matplotlib.pyplot as plt
from random import randrange
import pandas as pd

def count_cost(tab, i, j, r, c):
    left = (j - 1)
    right = (j + 1) % c
    up = (i - 1)
    down = (i + 1) % r

    de1 = -(tab[i][j] * (tab[up][j] + tab[down][j] + tab[i][left] + tab[i][right]))
    de2 = -(-tab[i][j] * (tab[up][j] + tab[down][j] + tab[i][left] + tab[i][right]))

    return de1 - de2

def linear_reg(_x, _y):
    avg_xy = np.average(_x * _y)
    avg_x = np.average(_x)
    avg_y = np.average(_y)
    avg_x2 = np.average(_x * _x)
    avg_y2 = np.average(_y * _y)

    a = (avg_xy - avg_x * avg_y) / (avg_x2 - avg_x ** 2)
    b = avg_y - a * avg_x

    return a, b

def find_stabilization_point(tab):
    unique_element, counts = np.unique(tab, return_counts=True)
    index = np.argmax(counts)
    stabilization_point = np.where(tab == unique_element[index])[0]
    stabilization_point = stabilization_point.astype(int)

    return stabilization_point[0]


rows, cols, iter, num_dem, *start_demons = map(int, input().split())

# rows, cols = 46, 46
# iter = 40000
# start_demons = [rows*cols*2]

t, m_t = [], []
latex_data = []
latex_data.append(["T", "m(T)"])

for start_demon in start_demons:
    for dem in np.linspace(int(start_demon*7/10), int(start_demon/20), 30):
        lattice = np.ones((rows, cols))

        energy, demon = -2 * rows * cols, int(dem)
        demon_data, cost_data, energy_data, m_data = [], [], [], []

        hist_data = {}

        for i in range(0, iter):
            r_rand, c_rand = randrange(rows), randrange(cols)

            de = count_cost(lattice, r_rand, c_rand, rows, cols)

            if(demon + de >= 0):
                demon += de
                energy -= de
                lattice[r_rand][c_rand] *= -1

            demon_data.append(demon)
            cost_data.append(de)
            energy_data.append(energy)
            m_data.append(np.sum(lattice))

        demon_bef_stab = demon_data

        stabilization_point_of_demon = find_stabilization_point(demon_data)
        demon_data = demon_data[stabilization_point_of_demon:]

        for i in demon_data:
            if int(i) in hist_data:
                hist_data[int(i)] += 1
            else:
                hist_data[int(i)] = 1

        hist_data = {key: value for key, value in hist_data.items() if value > 10}
        hist_x = np.array(list(hist_data.keys()))
        hist_y = np.array(list(hist_data.values()))
        log_hist_y = np.log(hist_y)

        a, b = linear_reg(hist_x, log_hist_y)

        temp = -1 / a

        stabilization_point_of_mag = find_stabilization_point(m_data)
        avg_m = np.mean(m_data[stabilization_point_of_mag:])

        t.append(temp)
        m_t.append(avg_m/(rows*cols))

        # print("{}   {}".format(temp, avg_m/(rows*cols)))

        # if dem == int(start_demon*7/10):
        #     plt.scatter(range(iter), demon_bef_stab, color='red', marker='o', s=5)
        #     plt.axvline(stabilization_point_of_demon, color='blue', linestyle='--')
        #     plt.xlabel("czas")
        #     plt.ylabel("wartość demona")
        #     plt.show()
        #
        #     plt.scatter(range(iter), m_data, color='red', marker='o', s=5)
        #     plt.axvline(stabilization_point_of_mag, color='blue', linestyle='--')
        #     plt.xlabel("czas")
        #     plt.ylabel("wartość magnetyzacji")
        #     plt.show()
        #
        #     plt.scatter(hist_x, hist_y, color='red', marker='o', s=5)
        #     plt.xlabel("wartośc energii demona")
        #     plt.ylabel("ilosc wystąpień")
        #     plt.show()
        #
        #     plt.scatter(hist_x, log_hist_y, color='red', marker='o', s=5)
        #     plt.xlabel("wartośc energii demona")
        #     plt.ylabel("logarytm ilości wystąpień")
        #     plt.show()
        #
        #     lin_x = np.linspace(min(hist_x), max(hist_x), 100)
        #     lin_y = a * lin_x + b
        #     plt.plot(lin_x, lin_y)
        #     plt.scatter(hist_x, log_hist_y, color='red', marker='o', s=5)
        #     plt.xlabel("wartośc energii demona")
        #     plt.ylabel("logarytm ilości wystąpień")
        #     plt.show()

        latex_data.append([temp, avg_m/(rows*cols)])

    # toLatex = pd.DataFrame(data=latex_data[1:],
    #                    columns=latex_data[0])
    # with open('mytable_46x46.tex', 'w') as lf:
    #     lf.write(toLatex.to_latex())

    plt.scatter(t, m_t, color='blue', marker='o', s=5)
    plt.axhline(y=0, color='red', linestyle='--')
    plt.xlabel("T")
    plt.ylabel("m(T)")
    plt.show()