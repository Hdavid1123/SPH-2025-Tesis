import matplotlib.pyplot as plt
from fluid.geometry_const import construir_fluido

def graficar_fluido():
    puntos = construir_fluido()
    plt.scatter(puntos[:, 0], puntos[:, 1], s=4, color='blue')
    plt.gca().set_aspect('equal')
    plt.title("Fluido generado")
    plt.show()