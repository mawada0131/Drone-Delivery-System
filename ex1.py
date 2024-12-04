import itertools

import search
import random
import math


ids = ["111111111", "111111111"]

problems = {
            "map": [['P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'P'], ],
            "drones": {'drone 1': (3, 3)},
            "packages": {'package 1': (0, 2),
                         'package 2': (2, 0)},
            "clients": {'Yossi': {"path": [(0, 1), (1, 1), (1, 0), (0, 0)],
                                  "packages": ('package 1', 'package 2')}}
        }

class DroneProblem(search.Problem):

    """This class implements a medical problem according to problem description file"""

    def __init__(self, initial):
        """Don't forget to implement the goal test
        You should change the initial to your own representation.
        search.Problem.__init__(self, initial) creates the root node"""
        self.map = initial["map"]
        self.drone_locstions = []
        self.drones_name = []
        for i in initial["drones"] :
            self.drones_name.append(i)
            self.drone_locstions.append(initial["drones"].get(i))
        self.package_locstions = []
        package_holding = []
        for i in initial["packages"]:
            self.package_locstions.append(initial["packages"].get(i))
            package_holding.append(False)
        self.clients_paths = []
        for i in initial["clients"]:
            self.clients_paths.append(initial["clients"].get(i)["path"])
        self.clients_packages = []
        packages_deliver = []
        self.clients = []
        clients_location = []
        self.clients_list = []
        for i in initial["clients"] :
            self.clients_list.append(i)
        for i in range(len(initial["clients"])):
            n = self.clients_list[i]
            self.clients.append(i)
            clients_location.append(0)
            self.clients_packages.append(initial["clients"].get(n)["packages"])
        self.packages = []
        for c in range(len(self.clients)):
            for i in range(len(self.clients_packages[c])):
                self.packages.append(i)
                packages_deliver.append(False)

        state0 = []
        state0.append(tuple(self.drone_locstions))
        state0.append(tuple(package_holding))
        state0.append(tuple(packages_deliver))
        state0.append(tuple(clients_location))
        self.state = tuple(state0)
        search.Problem.__init__(self, self.state)
        
    def actions(self, state):
        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""
        my_map = self.map
        drones = self.drone_locstions
        row_lenght = len(my_map)
        column_lenght = len(my_map[0])
        possible_acts = []
        for i in range(len(drones)):
            possible_act = []
            drone_loc_r = drones[i][0]
            drone_loc_c = drones[i][1]
            if (drone_loc_c + 1 < column_lenght):
                if my_map[drone_loc_r][drone_loc_c + 1] == 'P':
                    possible_act.append(tuple(('move' , self.drones_name[i] , (drone_loc_r, drone_loc_c + 1))))
            if (drone_loc_c - 1 > 0):
                if my_map[drone_loc_r][drone_loc_c - 1] == 'P':
                    possible_act.append(tuple(('move' , self.drones_name[i], (drone_loc_r, drone_loc_c - 1))))
            if (drone_loc_r - 1 > 0):
                if my_map[drone_loc_r - 1][drone_loc_c] == 'P':
                    possible_act.append(tuple(('move',  self.drones_name[i], (drone_loc_r - 1, drone_loc_c))))
            if (drone_loc_r + 1 < row_lenght):
                if my_map[drone_loc_r + 1][drone_loc_c] == 'P':
                    possible_act.append(tuple(('move ',  self.drones_name[i], (drone_loc_r + 1, drone_loc_c))))
            for n in range(len(self.package_locstions)):
                if my_map[drone_loc_r][drone_loc_c] == self.package_locstions[i] and (state[1][i]) == False and (state[2][i]) == False:
                    possible_act.append(tuple(('pick up',  self.drones_name[i], 'package' + ' ' +str(n+1) )))
            for c in range(len(self.clients)):
                if my_map[drone_loc_r][drone_loc_c] == self.clients_paths[c][state[3][c]]:
                    for package in self.packages:
                        if package in self.clients_packages[c]:
                            if state[2][0] == False:
                                possible_act.append(tuple(('deliver',  self.drones_name[i] ,self.clients_list[c] , 'package' + ' ' +str(n+1))))
            possible_act.append(tuple(('wait', self.drones_name[i])))
            possible_acts.append(tuple(possible_act))

        return possible_acts

    def update_loc_client(self , state):
        print('------------------------')
        y = state[3]
        for c in range(len(self.clients_list)):
            print(self.clients_list)
            lenght = len(self.clients_list)
            print(lenght)
            print(y[0])
            if y[c] == lenght :
                print("hi")
                y[c] = 0
            else:
                y[c] +=1

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        possible_acts = self.actions(state)
        if action in possible_acts:
            if action[0] == 'move':
                state[0][self.drones_name.index(action[1])] = action[2]
            if action[0] == 'pick up':
                state["holding"][self.packages.index(action[2])] = True
            if action[0] == 'deliver':
                state["packagedelivered"][self.packages.index(action[3])] = True
            if action[0] == 'wait':
                pass
        self.update_loc_client(state)


    def goal_test(self, state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""
        for package in range(len(self.packages)):
            if state[2][package] != True :
                return False
        return True

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state,
        state can be accessed via node.state)
        and returns a goal distance estimate"""
        return 0

    """Feel free to add your own functions
    (-2, -2, None) means there was a timeout"""


def create_drone_problem(game):
    return DroneProblem(game)

