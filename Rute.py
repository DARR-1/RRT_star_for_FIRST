import math

class Rute:

    #funcion para calcular la distancia
    def calculate_distance(point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def __init__(self, nodes):
        self.nodes = nodes
        self.lenght = 0