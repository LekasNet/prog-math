import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from mpl_toolkits.mplot3d import Axes3D


def task_1():
    print("Тестовые данные: Спираль Архимеда")
    theta = np.linspace(0, 4 * np.pi, 1000)
    a, b = 0.1, 0.1
    r = a + b * theta
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    plt.figure(figsize=(6, 6))
    plt.plot(x, y)
    plt.title("Архимедова спираль")
    plt.axis('equal')
    plt.show()


def task_2():
    print("Тестовые данные: [10, 20, 30, 40]")
    data = [10, 20, 30, 40]
    labels = ['Категория 1', 'Категория 2', 'Категория 3', 'Категория 4']
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("Круговая диаграмма")
    plt.show()


def task_3():
    print("Тестовые данные: Мозаика 12x12, 6 цветов")
    rows, cols = 12, 12
    colors = np.random.randint(0, 6, (rows, cols))
    plt.imshow(colors, cmap='tab10', extent=(0, cols, 0, rows))
    plt.title("Мозаичное изображение")
    plt.show()


def task_4():
    print("Тестовые данные: Разрешение 600x600")
    res = 600
    x = np.linspace(-2, 1, res)
    y = np.linspace(-1.5, 1.5, res)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    C = Z.copy()
    mandelbrot = np.zeros_like(X, dtype=int)
    for i in range(100):
        Z = Z ** 2 + C
        Z[np.abs(Z) > 2] = 2  # Ограничиваем значения, чтобы избежать переполнения
        mask = (np.abs(Z) < 2) & (mandelbrot == 0)
        mandelbrot[mask] = i

    plt.imshow(mandelbrot, cmap='hot', extent=(-2, 1, -1.5, 1.5))
    plt.title("Фрактал Мандельброта")
    plt.colorbar()
    plt.show()


particles = 15
positions = np.zeros((particles, 2))
velocities = np.random.uniform(-1, 1, (particles, 2))


def task_5():
    print("Тестовые данные: 15 частиц, скорости уменьшаются с удалением")
    global positions
    global velocities
    global particles
    fig, ax = plt.subplots()
    scat = ax.scatter(positions[:, 0], positions[:, 1])
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    def update(frame):
        global positions
        global velocities
        positions += velocities
        scat.set_offsets(positions)

    ani = animation.FuncAnimation(fig, update, frames=100, interval=50)
    plt.show()


def task_6():
    print("Тестовые данные: 4 планеты, с разными массами")
    num_planets = 4
    radii = np.linspace(1, 4, num_planets)
    angles = np.linspace(0, 2 * np.pi, 500)
    plt.figure(figsize=(6, 6))
    for r in radii:
        x = r * np.cos(angles)
        y = r * np.sin(angles)
        plt.plot(x, y)
    plt.scatter(0, 0, color='yellow', s=300, label='Звезда')
    plt.title("Планетарная система")
    plt.axis('equal')
    plt.legend()
    plt.show()


def task_7():
    print("Тестовые данные: z = exp(-x^2 - y^2), x,y [-3, 3]")
    x = np.linspace(-3, 3, 50)
    y = np.linspace(-3, 3, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-X ** 2 - Y ** 2)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')
    plt.title("3D график")
    plt.show()


def task_8():
    print("Тестовые данные: Регион 20x20, температурный диапазон [-20, 30]")
    data = np.random.uniform(-20, 30, (20, 20))
    plt.imshow(data, cmap='coolwarm', interpolation='nearest')
    plt.colorbar(label='Температура')
    plt.title("Тепловая карта")
    plt.show()


def task_9():
    print("Тестовые данные: Социальная сеть, 10 узлов")
    G = nx.Graph()
    nodes = range(10)
    edges = [(i, (i + 1) % 10) for i in nodes]
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    nx.draw_circular(G, with_labels=True, node_color='skyblue')
    plt.title("Сетевой граф")
    plt.show()


def task_10():
    print("Тестовые данные: 3D волна, фронт распространяется спирально")
    x = np.linspace(0, 4 * np.pi, 500)
    y = np.sin(x)
    fig, ax = plt.subplots()
    line, = ax.plot(x, y)

    def update(frame):
        line.set_ydata(np.sin(x + frame / 10.0))

    ani = animation.FuncAnimation(fig, update, frames=100, interval=50)
    plt.title("Волновой фронт")
    plt.show()


def main():
    while True:
        tasks = {
            '1': task_1,
            '2': task_2,
            '3': task_3,
            '4': task_4,
            '5': task_5,
            '6': task_6,
            '7': task_7,
            '8': task_8,
            '9': task_9,
            '10': task_10
        }

        print("Выберите номер задачи (1-10):")

        choice = input("Введите номер задачи: ").strip()

        if choice in tasks:
            tasks[choice]()
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
