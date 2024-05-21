from RRT import RRT
import pandas as pd
from pygame import Rect

# Cada unidad en la aplicación equivale a medio centimetro en la vida real
MIN_NUM_OF_ITERATIONS = 5000
ROBOT_WIDTH = 80
ROBOT_LENGTH = 80
DELTA = 20            # Longitud máxima de paso para expandir el árbol
SOFT_TILES_WIDTH = 119.3333333333333333333333333333333333333333333333333333333333333333333
START = (2.5 * SOFT_TILES_WIDTH, -1.5 * SOFT_TILES_WIDTH)
GOAL = (.5 * SOFT_TILES_WIDTH, 1.5 * SOFT_TILES_WIDTH)
#The colliders are created by using the rect class of pygame. For example: pygame.Rect(200, 200, 100, 100)
COLLIDERS = [
    Rect(SOFT_TILES_WIDTH + 358, SOFT_TILES_WIDTH + 358, SOFT_TILES_WIDTH, 19.5272727272727),
    Rect(SOFT_TILES_WIDTH + 358, SOFT_TILES_WIDTH + 358, 19.5272727272727, SOFT_TILES_WIDTH),
    Rect(-SOFT_TILES_WIDTH + 358 -SOFT_TILES_WIDTH, SOFT_TILES_WIDTH + 358, SOFT_TILES_WIDTH, 19.5272727272727),
    Rect(-SOFT_TILES_WIDTH + 358 -19.5272727272727, SOFT_TILES_WIDTH + 358, 19.5272727272727, SOFT_TILES_WIDTH),
    Rect(SOFT_TILES_WIDTH * 2 + 358 , SOFT_TILES_WIDTH * 2 + 358, SOFT_TILES_WIDTH, SOFT_TILES_WIDTH),
    Rect(-SOFT_TILES_WIDTH * 2 + 358 - SOFT_TILES_WIDTH, SOFT_TILES_WIDTH * 2 + 358, SOFT_TILES_WIDTH, SOFT_TILES_WIDTH),
]


rrt = RRT(START, GOAL, COLLIDERS, ROBOT_WIDTH, ROBOT_LENGTH, DELTA)

rrt.GOAL_RADIUS = (SOFT_TILES_WIDTH - min(ROBOT_LENGTH, ROBOT_WIDTH)) / 2      # Radio alrededor del punto objetivo para considerarlo alcanzado
print(rrt.GOAL_RADIUS)
rrt.NUM_NODES_PER_CLICK = 500         # Número máximo de nodos en el árbol
rrt.NEIGHBORHOOD_RADIUS = 37           #tiene que ser mayor que DELTA y menos que la distancia entre start y goal
rrt.NODES_RADIUS = 5


rrt.main()
for i in range(MIN_NUM_OF_ITERATIONS):
    rrt.createNode()
    print(i)


rrt.main()

while rrt.shorter_rute == None:
    rrt.createNode()
    print(rrt.shorter_rute)

rrt.main(True)
#print(rrt.shorter_rute)

#save rute coords in a csv file
serie_data = []
rrt.shorter_rute.nodes.reverse()
for i in rrt.shorter_rute.nodes:
    serie_data.append(((i.x - rrt.WIDTH / 2) * 5, (i.y - rrt.HEIGHT / 2) * -5))

coords_serie = pd.Series(serie_data)
coords_serie.to_csv('CoordsList.csv')
print('se han guardado las coordenadas de la trayectoria')