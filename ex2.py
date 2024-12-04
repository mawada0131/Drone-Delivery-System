import math
import random
import utils
from utils import mode

ids = ["212467575", "314813940"]


class DroneAgent:
    def __init__(self, initial):
       self.clients_len_p = len(initial["packages"])
    def act(self, state):

        my_map = state["map"]
        row_lenght = len(my_map)
        column_lenght = len(my_map[0])
        possible_acts = []
        for drone in state["drones"].keys():
            dron_n_of_pack = 0
            for pack in state["packages"]:
                if state["packages"][pack] == drone :
                    dron_n_of_pack+=1
            possible_act = []
            dron_loc = state["drones"][drone]
            if (0 <= dron_loc[1] + 1 < column_lenght):
                if my_map[dron_loc[0]][dron_loc[1] + 1] == 'P':
                    possible_act.append(tuple(('move', drone , ( dron_loc[0], dron_loc[1]+1))))
            if (0 <=dron_loc[1] - 1 < column_lenght):
                if my_map[dron_loc[0]][dron_loc[1] - 1] == 'P':
                    possible_act.append(tuple(('move', drone , ( dron_loc[0], dron_loc[1]-1))))
            if (0 <= dron_loc[0] + 1 < row_lenght):
                if my_map[dron_loc[0]+1][dron_loc[1]] == 'P':
                    possible_act.append(tuple(('move', drone , ( dron_loc[0] + 1, dron_loc[1]))))
            if (0 <= dron_loc[0] - 1 < row_lenght):
                if my_map[dron_loc[0] - 1][dron_loc[1]] == 'P':
                    possible_act.append(tuple(('move', drone , ( dron_loc[0]-1, dron_loc[1]))))
            if  (0 <= dron_loc[0] + 1 < row_lenght) and (0 <= dron_loc[1] + 1 < column_lenght):
                if my_map[dron_loc[0]+1][dron_loc[1]+1] == "P":
                    possible_act.append(tuple(('move', drone, (dron_loc[0] +1 , dron_loc[1] + 1))))
            if (0 <= dron_loc[0] - 1 < row_lenght) and (0 <= dron_loc[1] - 1 < column_lenght):
                if my_map[dron_loc[0]-1][dron_loc[1]-1] == "P" :
                    possible_act.append(tuple(('move', drone, (dron_loc[0] - 1 , dron_loc[1] - 1))))
            if (0 <= dron_loc[0] - 1 < row_lenght) and (0 <= dron_loc[1] + 1 < column_lenght) :
                if my_map[dron_loc[0]-1][dron_loc[1]+1] == "P" :
                    possible_act.append(tuple(('move', drone, (dron_loc[0] - 1 , dron_loc[1] + 1))))
            if (0 <= dron_loc[0] + 1 < row_lenght) and (0 <= dron_loc[1] - 1 < column_lenght) :
                if my_map[dron_loc[0]+1][dron_loc[1]-1] == "P":
                    possible_act.append(tuple(('move', drone, (dron_loc[0] + 1 , dron_loc[1] - 1))))
            for package in state["packages"].keys():
                if state["packages"][package] == dron_loc :
                    if dron_n_of_pack < 2 :
                       possible_act.append(tuple(('pick up', drone ,package)))
            for client in state["clients"].keys():
                if state["clients"][client]["location"] == dron_loc:
                    for package in state["clients"][client]["packages"]:
                        if package in state["packages"]:
                            if state["packages"][package] == drone :
                                possible_act.append(tuple(('deliver', drone, client, package)))

            possible_act.append(tuple(('wait', drone)))
            possible_acts.append(tuple(possible_act))
        new_coordinates_list = {}
        probs = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
        for client, properties in state["clients"].items():
            for _ in range(10000):
                movement = random.choices(probs, weights=properties["probabilities"])[0]
                new_coordinates = (properties["location"][0] + movement[0], properties["location"][1] + movement[1])
                if new_coordinates[0] < 0 or new_coordinates[1] < 0 or new_coordinates[0] >= len(
                        state["map"]) or new_coordinates[1] >= len(state["map"][0]):
                    continue
                break
            else:
                new_coordinates = (properties["location"][0], properties["location"][1])
            new_coordinates_list.update({client:new_coordinates})
        best = []
        for t in possible_acts:
            count0 = 10000
            best_action = None
            for action in t:
                count = 0
                if action[0] == 'deliver':
                    count = -1
                if action[0] == 'wait':
                    count = (len(state["map"])**2 + (len(state["map"][0])**2))**(1/2)
                if action[0] == 'pick up':
                    count = -3
                if action[0] == 'move':
                    pdis = 25
                    for package in state["packages"]:
                        if type(state["packages"][package]) == tuple:
                            cdis = utils.distance_squared(state["packages"][package], action[2])**(1/2)
                            if cdis < pdis:
                                pdis = cdis

                    client_min_dis = 100
                    for package in state["packages"]:
                        if type(state["packages"][package]) == str:
                            for client in state["clients"]:
                                if package in state["clients"][client]["packages"]:
                                    client_dis = utils.distance_squared(new_coordinates_list.get(client), action[2])**(1/2)

                                    if client_dis < client_min_dis:
                                        client_min_dis = client_dis

                    if client_min_dis < pdis :
                        count = client_min_dis
                    elif client_min_dis > pdis:
                        count = pdis
                if count < count0:
                    best_action = action
                    count0 = count
            best.append(best_action)
        if self.clients_len_p == 1 and len(state["packages"]) == 0:
            return "terminate"
        if not state["packages"]:
            return "reset"
        return best
