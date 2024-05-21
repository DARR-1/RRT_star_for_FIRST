import pygame
import random
import math
from Node import Node
from Rute import Rute

class RRT():

    def __init__(self, START = (0,0), GOAL = (100, 100), COLLIDERS = [pygame.Rect(200, 200, 100, 100)], ROBOT_WIDTH = 0, ROBOT_LENGTH = 0, DELTA = 20):
        self.START = START
        self.GOAL = GOAL

        # Definir colores
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.DARK_RED = (200, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)
        self.BLACK = (0 ,0 ,0)
        self.PURPLE = (255, 0, 255)
        self.ORANGE = (255, 165, 0)

        # Dimensiones de la ventana
        self.WIDTH = 716
        self.HEIGHT = 716

        
        # Parámetros del RRT*
        self.DELTA = DELTA            # Longitud máxima de paso para expandir el árbol
        self.GOAL_RADIUS = 20      # Radio alrededor del punto objetivo para considerarlo alcanzado
        self.NUM_NODES_PER_CLICK = 500         # Número máximo de nodos en el árbol
        self.NEIGHBORHOOD_RADIUS = 37
        self.ROBOT_WIDTH = ROBOT_WIDTH
        self.ROBOT_LENGTH = ROBOT_LENGTH
        self.NODES_RADIUS = 5

        #ajustar valores de coordenadas para que tengan el centro como punto de referencia
        self.START = (START[0] + self.WIDTH / 2, START[1] + self.HEIGHT / 2)
        self.GOAL = (GOAL[0] + self.WIDTH / 2, GOAL[1] + self.HEIGHT / 2)

        #colliders
        self.COLLIDERS = COLLIDERS

        #Variables
        self.internal_colliders = []
        self.nodes_list = [Node(self.START[0], self.START[1])]
        self.shorter_rute = None

    #calculate internal colliders
        for i in self.COLLIDERS:
            
            # Reduciendo la línea en líneas más cortas
            left = i.left - self.ROBOT_WIDTH / 2
            top = i.top - self.ROBOT_LENGTH / 2
            width = i.width + self.ROBOT_WIDTH
            height = i.height + self.ROBOT_LENGTH

            # Agregando el rectángulo con las nuevas líneas
            self.internal_colliders.append(pygame.Rect(left, top, width, height))
        


    #funcion para calcular la distancia
    def distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    #funcion para calcular el nodo más cercano a un punto
    def nearestNode(self, nodes, point):
        actual_min_distance = float('inf')
        closest_node = None
        for i in nodes:
            if self.distance(i.position, point) < actual_min_distance:
                closest_node = i
                actual_min_distance = self.distance(i.position, point)
        return closest_node

    #funcion para generar un punto aleatorio
    def randomPoint(self):
        x = random.randint(0, self.WIDTH)
        y = random.randint(0, self.HEIGHT)
        
        return x, y


    def getNeighbors(self, new_node, nodes):
        neighbor_nodes = []
        for i in nodes:
            if self.distance(i.position, new_node.position) < self.NEIGHBORHOOD_RADIUS:
                neighbor_nodes.append(i)
        
        neighbors_positions = []
        for j in neighbor_nodes:
            neighbors_positions.append(j.position)
        #print('neighbors: ', neighbors_positions)

        return neighbor_nodes
        
    def nearestParent(self, node, nodes):
        parent = self.nearestNode(nodes, node.reference_point)
        min_cost = float('inf')
        neighbors_list = self.getNeighbors(node, nodes)
        for i in neighbors_list:
            cost = i.cost + self.distance(i.position, node.position)
            if cost < min_cost:
                parent = i
                min_cost = cost

        return parent

    def reconectNeighbors(self, node, nodes):
        neighbors_list = self.getNeighbors(node, nodes)

        for i in neighbors_list:
            cost = node.cost + self.distance(node.position, i.position)

            if cost < i.cost and all(self.line_collides_with_rect(node.position, i.position, collider) == () for collider in self.internal_colliders):
                #print('neighbor reconection')
                i_index = nodes.index(i)
                nodes[i_index].parent = node
                nodes[i_index].update()
            #print(i.cost)
            #print(cost)


    def createNode(self, nodes = None, reference_point=(float('inf'), 0)):
        if nodes == None:
            nodes = self.nodes_list

        while True:
            if reference_point == (float('inf'), 0):
                point = self.randomPoint()
            else:
                point = reference_point
                
            nearest = self.nearestNode(nodes,point)
            angle = math.atan2(point[1] - nearest.y, point[0] - nearest.x)
            x = nearest.x + self.DELTA * math.cos(angle)
            y = nearest.y + self.DELTA * math.sin(angle)
            new_node = Node(x, y)
            new_node.reference_point = point
            new_node.parent = self.nearestParent(new_node, nodes)

            #for collider in self.internal_colliders:
            #    print(self.line_collides_with_rect(new_node.position, new_node.parent.position, collider))
            #    print('condition: ', self.line_collides_with_rect(new_node.position, new_node.parent.position, collider) == ())
                
            #print(all(self.line_collides_with_rect(new_node.position, new_node.parent.position, collider) == () for collider in self.internal_colliders))

            # Verifica si el punto está fuera de todos los rectángulos de colision
            if all(self.line_collides_with_rect(new_node.position, new_node.parent.position, collider) == () for collider in self.internal_colliders):
                #print('position: ', new_node.position)
                #new_node.reference_point = poin

                #print('post parent: ', new_node.parent.
                
                new_node.update()
                self.reconectNeighbors(new_node, nodes)
                self.shorter_rute = self.shorterRute(nodes)

                #if shorter_rute != None:
                    #(shorter_rute.nodes)
                #self.shorter_rute = 5
                self.nodes_list.append(new_node)

                #k = self.WIDTH * self.HEIGHT
                #n = len(nodes)
                #self.NEIGHBORHOOD_RADIUS = math.sqrt((k/n)) + self.DELTA

                return new_node

    def createRute(self, last_node):
        last_check_node = last_node
        check_nodes = []
        iterations = 0
        while True:
            if last_check_node.parent == None:
                new_rute = Rute(check_nodes)
                new_rute.lenght = new_rute.nodes[0].cost
                return new_rute
            
            if iterations == 0:
                check_nodes.append(last_check_node)
            else:
                check_nodes.append(last_check_node.parent)
                last_check_node = last_check_node.parent
            
            iterations += 1

    def shorterRute(self, nodes):
        #print('se inicio la funcion shorterRute()')
        global shorter_rute
        minimum_distance_rute = None

        for l in nodes:
            if self.distance(l.position, self.GOAL) < self.GOAL_RADIUS + self.NODES_RADIUS:
                #print('nodo dentro del goal')
                if self.shorter_rute != None and self.shorter_rute.nodes != []:
                    actual_shorter_rute_node = self.shorter_rute.nodes[0]
                    minimum_distance_rute = self.createRute(actual_shorter_rute_node)

                    if l.cost < actual_shorter_rute_node.cost:
                        print('se ha creado una nueva ruta')
                        self.createRute(l)
                    else:
                        self.createRute(actual_shorter_rute_node)
                else:
                    #print(self.shorter_rute)
                    minimum_distance_rute = self.createRute(l)
    

        #print(minimum_distance_rute)
        return minimum_distance_rute
        
    def line_collides_with_rect(self, start, end, rect):
        # Verifica si la línea entre start y end colisiona con rect
        return rect.clipline(start, end)

    def main(self, show_nodes = False):
        #atributos de pygame
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.BACKGROUND_IMAGE = pygame.image.load('background.png')
        self.BACKGROUND_IMAGE = pygame.transform.scale(self.BACKGROUND_IMAGE, (self.WIDTH, self.HEIGHT))
        pygame.init()
        pygame.display.set_caption("RRT*")

        clock = pygame.time.Clock()

        #nodes_list = [node(START[0], START[1])]

        pygame.font.init()
        font = pygame.font.Font(None, 30)

        running = True
        while running:
            #print(self.shorter_rute)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.nodes_list.append(self.createNode(self.nodes_list))
                    #nodes_list.append(createNode(nodes_list, GOAL))
                if event.type == pygame.KEYDOWN:
                    for i in range(0, self.NUM_NODES_PER_CLICK):
                        self.nodes_list.append(self.createNode(self.nodes_list))
                        #nodes_list.append(createNode(nodes_list, GOAL))
                        #print(i)
            #last_node = self.nodes_list[-1]
            
            if self.shorter_rute != None:
                text_surface = font.render(str(self.shorter_rute.lenght), True, self.BLACK)



            self.screen.fill(self.WHITE)
            self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

            if show_nodes:
                for i in self.nodes_list[1:]:
                    pygame.draw.line(self.screen, self.BLACK, i.parent.position, i.position)
                    pygame.draw.circle(self.screen, self.GREEN, i.position, self.NODES_RADIUS)
                    #print(i.parent.position, i.position)

            #Draw the start, goal and reference point

            #if self.nodes_list[1:] != []:
            #    pygame.draw.line(self.screen, self.BLACK, last_node.position, last_node.reference_point, 2)
            #    pygame.draw.circle(self.screen, self.PURPLE, last_node.reference_point, self.NODES_RADIUS)
            #pygame.draw.circle(self.screen, self.ORANGE, last_node.position, self.NODES_RADIUS)
            pygame.draw.circle(self.screen, self.RED, self.START, 10)
            pygame.draw.circle(self.screen, self.YELLOW, self.GOAL, self.GOAL_RADIUS)         

            #draw the shorter rute
            if self.shorter_rute is not None:
                for j in self.shorter_rute.nodes:
                    if j.parent != None:
                        pygame.draw.line(self.screen, self.RED, j.position, j.parent.position, 3)
                    pygame.draw.circle(self.screen, self.DARK_RED, j.position, self.NODES_RADIUS)
            #else:
            #    print('shorter_rute is None')

            #draw colliders
            #for c in self.internal_colliders:
            #    pygame.draw.rect(self.screen, self.BLACK, c)
            
            for k in self.COLLIDERS:
                pygame.draw.rect(self.screen, self.BLUE, k)

            if self.shorter_rute != None:
                self.screen.blit(text_surface, (self.WIDTH // 2 - text_surface.get_width() // 2, self.HEIGHT // 2 - text_surface.get_height() // 2))  # Dibujar el texto centrado

            pygame.display.flip()  # Actualizar la pantalla
            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    rrt = RRT()
    rrt.main()