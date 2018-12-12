# created by ilyas Aroui on 06/12/2018

import numpy as np
from gurobipy import *
import matplotlib.pyplot as plt


def isfloat(value):
    """ vérifier si l'entrée est un float
    :return:
    True: Si la value est de type float
    False: Sinon
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def read_data():
    with open('distances92.txt', 'r') as distance_file:
        distances92 = np.array([float(x) for l in distance_file for x in l.split() if isfloat(x)])
        distances92 = np.reshape(distances92, (36, 36))
    distance_file.close()

    with open('villes92.txt', 'r') as cities_file:
        cities92 = np.array([c for l in cities_file for c in l.split('\n') if c])
    cities_file.close()

    with open('populations92.txt', 'r') as population_file:
        population92 = np.array([int(x) for l in population_file for x in l.split(',') if isfloat(x)])
    population_file.close()

    with open('coordvilles92.txt', 'r') as coor_file:
        coordinates92 = np.array([int(x) for l in coor_file for x in l.split(',') if isfloat(x)])
        coordinates92 = np.reshape(coordinates92, (36, 2))
    coor_file.close()

    return distances92, cities92, population92, coordinates92


def draw_affectations(affectation, image, avg_val, max_row, max_column):
    img = plt.imread(image)
    fig, ax = plt.subplots()
    ax.imshow(img)
    for j in range(len(resource_index)):
        l1 = np.where(affectation[:, j] == 1)[0]
        for i in range(len(l1)):
            color = 'C' + str(j) #  une couleur pour chaque resource
            if j == max_column and l1[i] == max_row:  #  la couleur noir pour la distance maximale
                color = 'black'
            plt.plot([coordinates[l1[i], 0], coordinates[resource_index[j], 0]],
                     [coordinates[l1[i], 1], coordinates[resource_index[j], 1]],
                     color=color, linewidth=1)
    plt.title('k = '+str(len(resource_index))+'\nDistance moyenne: ' + str(avg_val/36)[:6] +
              '\nDistance max: '+str(D[max_row, max_column]))
    title = 'exo2'+'_'
    for i in range(len(resource_index)):
        title += str(resource_index[i]) + '_'
    plt.savefig(title)
    plt.show()


#  data manipulation
distances, cities, population, coordinates = read_data()
assert distances.shape == (36, 36)
assert cities.shape == (36, )
assert population.shape == (36,)
assert coordinates.shape == (36, 2)

#  initialisation des constantes
num_cities = cities.shape[0]
resource_index = [3, 7, 23, 13, 33]
k = len(resource_index)
alpha = 0.1
epsilon = 1.e-6
population_max = population.sum()*(1 + alpha)/k
D = distances[:, resource_index]


# model
m = Model('exo2')
m.setParam('OutputFlag', False)

# decision variables
x = {}
for i in range(num_cities):
    for j in range(k):
        x[(i, j)] = m.addVar(vtype=GRB.BINARY)
z = m.addVar(vtype=GRB.CONTINUOUS, lb=0, obj=1.0)
m.update()

# constraints

for i in range(num_cities):
    m.addConstr(quicksum(x[(i, j)] for j in range(k)) == 1)

for j in range(k):
    m.addConstr(quicksum(x[(i, j)]*population[i] for i in range(num_cities)) <= population_max)

for i in range(num_cities):
    for j in range(k):
        m.addConstr(z >= x[(i, j)]*D[i, j])

m.setObjective(z + epsilon*quicksum(quicksum(D[i, j]*x[(i, j)] for
                                             i in range(num_cities)) for j in range(k)), GRB.MINIMIZE)

# optimization
m.optimize()

#  récupération de la matrice Xij
result = np.zeros((num_cities, k))
for i in range(num_cities):
    for j in range(k):
        result[i, j] = x[(i, j)].X

# assertion constraints
assert((result.sum(1) == 1).all() == True)
assert((sum(np.multiply(result,  population.reshape((36, 1)))) <= population_max).all() == True)


row_max = np.argmax(np.max(np.multiply(result, D), axis=1))
column_max = np.argmax(np.max(np.multiply(result, D), axis=0))

print(np.sum(np.multiply(result, D))/36)
print(np.max(np.multiply(result, D)))
draw_affectations(result, '92.png', np.sum(np.multiply(result, D)), row_max, column_max)
