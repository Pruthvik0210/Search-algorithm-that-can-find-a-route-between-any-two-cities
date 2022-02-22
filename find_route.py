"""
Net_Id : 1001861545
Name : Pruthvik Kakadiya
Assignment 1
"""

import sys


def map_build(input_file):
    for i in input_file:
        if i.lower().find('end of input') != -1:
            break
        else:
            inputs = i.strip().split(' ')
            temporary_source = inputs[0]    #to store temporary source
            temporary_destination = inputs[1]   #to store temporary destination
            if temporary_source in cities_list:
                pass
            else:
                cities_list.append(temporary_source)

            if temporary_destination in cities_list:
                pass
            else:
                cities_list.append(temporary_destination)

    cities_list.sort()
    for x in range(len(cities_list)):
        distance_cities.append([])
        for y in range(len(cities_list)):
            distance_cities[x].append(-1)
        distance_cities[x][x] = 0

    for i in input_file:
        if i.lower().find('end of input') != -1:
            break
        else:
            temporary = i.strip().split(" ")
            source1 = temporary[0]
            destination1 = temporary[1]
            distance = temporary[2]
            try:
                distance_cities[cities_list.index(source1)][cities_list.index(destination1)] = float(distance)
                distance_cities[cities_list.index(destination1)][cities_list.index(source1)] = float(distance)
            except ValueError as e:
                print("error", e, "online", i)
    return


def route_finder(route, visited):
    path = []

    def back(destination, visited):
        if destination is None:
            return
        else:
            for node in visited:
                if node["node"] == destination:
                    path.append(destination)
                    back(node["parent"], visited)

    if route:
        print('distance : ' + str(route['cost']) + ' km')
        print('route :')
        back(route['current'], visited)
        path.reverse()
        for i in range(0, len(path) - 1):
            print(cities_list[path[i]] + ' to ' + cities_list[path[i + 1]] + ' : ' + str(
                distance_cities[path[i]][path[i + 1]]) + 'km')

    else:
        print('distance : infinity')
        print('route : not found')
    return


def fringe_sort(fringe, temporary):
    if len(fringe) > 1:
        for i in range(0, len(fringe) - 1):
            min = i
            for j in range(i + 1, len(fringe)):
                a = fringe[min]['cost']  # dictionary
                b = fringe[j]['cost']  # dictionary
                if temporary:
                    a += fringe[min]['heu']
                    b += fringe[j]['heu']
                if a > b:
                    min = j

            temp = fringe[min]  # swapping the values
            fringe[min] = fringe[i]
            fringe[i] = temp
        return fringe
    else:
        return fringe


def visited_nodes(current, visited):
    for node in visited:
        if current == node['node']:
            return True

    return False


def uniform_cost_search(source, destination):  # for uninformed search
    expanded_node = 0  # expanded node counter
    generated_node = 1  # generated node counter
    destination = cities_list.index(destination)   #destination city
    fringe = []  # fringe dictionary
    visited = []  # visited nodes dictionary
    route = False  # dictionary of rute
    fringe.append({'current': cities_list.index(source), 'cost': 0, 'parent_node': None})
    while len(fringe) > 0:
        expanded_node += 1
        if fringe[0]['current'] == destination:
            visited.append({'node': fringe[0]['current'], 'parent': fringe[0]['parent_node']})
            route = fringe[0]
            break
        elif visited_nodes(fringe[0]['current'], visited):
            del fringe[0]
            continue
        else:
            visited.append({'node': fringe[0]['current'], 'parent': fringe[0]['parent_node']})
            for i in range(len(distance_cities[fringe[0]['current']])):
                if distance_cities[fringe[0]['current']][i] > 0:
                    fringe.append({'current': i, 'cost': fringe[0]['cost'] + distance_cities[fringe[0]['current']][i],
                                   'parent_node': fringe[0]['current']})
                    generated_node += 1
            del fringe[0]
            fringe = fringe_sort(fringe, False)

    print('nodes expanded: ' + str(expanded_node))
    print('nodes generated: ' + str(generated_node))

    route_finder(route, visited)
    return


def informed_search_astar(source, destination):
    expanded_node = 0  # expanded node counter
    generated_node = 1  # generated node counter
    destination = cities_list.index(destination) #destination city
    fringe = []  # fringe dictionary
    visited = []  # visited nodes dictionary
    route = False  # dictionary of rute
    fringe.append({'current': cities_list.index(source), 'cost': 0, 'heu': heuristics[cities_list.index(source)], 'parent_node': None})
    while len(fringe) > 0:
        expanded_node +=1
        if fringe[0]['current'] == destination:
            visited.append({'node':fringe[0]['current'],'parent':fringe[0]['parent_node']})
            route = fringe[0]
            break
        elif visited_nodes(fringe[0]['current'], visited):
            del fringe[0]
            continue
        else:
            visited.append({'node': fringe[0]['current'], 'parent': fringe[0]['parent_node']})
            for i in range(len(distance_cities[fringe[0]['current']])):
                if distance_cities[fringe[0]['current']][i] > 0:
                    fringe.append({'current': i, 'cost': fringe[0]['cost'] + distance_cities[fringe[0]['current']][i], 'heu': heuristics[i],
                                   'parent_node': fringe[0]['current']})
                    generated_node += 1
            del fringe[0]
            fringe = fringe_sort(fringe, True)

    print('nodes expanded: ' + str(expanded_node))
    print('nodes generated: ' + str(generated_node))

    route_finder(route, visited)
    return



def heuristics_values(h_file):
    for i in h_file:
        if i.lower().find("end of input") != -1:
            break
        else:
            heu = i.split(" ")
            heuristics[cities_list.index(heu[0])] = float(heu[1])
        return




if len(sys.argv) >= 4:

    input_file = sys.argv[1]  # the input file having cost between cities
    cities_list = []  # dictionary of all cities
    distance_cities = []  # dictionary of distance between cities
    map_build(open(sys.argv[1],"r").read().split("\n"))
    source = sys.argv[2]  # source/start city
    destination = sys.argv[3]  # destination/goal city
    if len(sys.argv) == 4:  # for uninformed search
        uniform_cost_search(source, destination)

    elif len(sys.argv) == 5:  # for informed search
        heuristics = [0] * len(cities_list)
        h_file = sys.argv[4]    # heuristic value file for informed search
        heuristics_values(open(h_file, 'r').read().split("\n"))
        informed_search_astar(source, destination)

    else:
        print('Input Error')

else:
    print('Input Error')




"""
References:
AI Stuart Russell and Peter Norvig 3rd Edition
GeeksForGeeks
Stackoverflow
Github
W3 school for python
"""
