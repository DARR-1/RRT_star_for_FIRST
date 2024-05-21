import math
# Clase para representar un nodo en el árbol RRT*
class Node:
    #funcion para calcular la distancia
    def distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = (x, y)
        self.reference_point = None
        self.parent = None  # El nodo padre en el árbol
        self.update()
        
        
    
    def update(self):
        #print(self.parent)
        if self.parent == None:
            self.cost = 0
        else:
            self.cost = self.parent.cost + self.distance(self.position, self.parent.position)