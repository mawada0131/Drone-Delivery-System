import random
import json

ids = ["212467575","314813940"]

class DroneAgent:
    def __init__(self, n, m):
        self.mode = 'train'  # do not change this!
        # your code here
        self.q = {}
        self.m = m
        self.n = n
        self.epsilon = 0.01  # exploration constant
        self.alpha = 0.45  # learning constant
        self.gamma = 0.99  # discount constant
        self.actions = ['reset', 'wait', 'pick', 'move_up', 'move_down', 'move_left', 'move_right', 'deliver']

    def get_q(self, obs0, action):
        obs0['packages'] = tuple(obs0['packages'])
        return self.q.get((json.dumps(obs0), action), 0.0)

    def possible_action(self , obs0):
        actions = self.actions
        possible_act = []
        for action in actions :
            if action == 'deliver' :
                if obs0["drone_location"] == obs0["target_location"] :
                    for pack in obs0["packages"] :
                        if type(pack[1]) == str :
                            possible_act.append(action)
                            break
                break
            if action == 'pick' :
                count_pack = 0
                for pack in obs0["packages"]:
                    if type(pack[1]) == str:
                        count_pack +=1
                for pack in obs0["packages"]:
                    if obs0["drone_location"] == pack[1] and count_pack<2:
                        possible_act.append(action)
                        break
            if action == 'move_up' :
                if obs0["drone_location"][0] - 1 >= 0 :
                    possible_act.append(action)
            if action == 'move_down' :
                if obs0["drone_location"][0] + 1 < self.n :
                    possible_act.append(action)
            if action == 'move_right' :
                if obs0["drone_location"][1] + 1 < self.m:
                    possible_act.append(action)
            if action == 'move_left' :
                if obs0["drone_location"][1] - 1 >= 0 :
                    possible_act.append(action)
            if action == 'wait' :
                possible_act.append(action)
        return possible_act

    def select_action(self, obs0):
        actions = self.possible_action(obs0)
        if len(obs0["packages"]) == 0:
            action = 'reset'
        elif random.random() < self.epsilon and self.mode =='train':
            action = random.choice(actions)
        else:
            q = [self.get_q(obs0, a) for a in actions]
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)
            action = actions[i]
        return action

    def train(self):
        self.mode = 'train'  # do not change this!

    def eval(self):
        self.mode = 'eval'  # do not change this!

    def update(self, obs0, action, obs1, reward):
        actions = self.actions
        q_max = max([self.get_q(obs1, a) for a in actions])
        obs0['packages'] = tuple(obs0['packages'])
        q_old = self.q.get((json.dumps(obs0), action), None)
        if q_old is None:
            self.q[(json.dumps(obs0), action)] = reward
        else:
            self.q[(json.dumps(obs0), action)] = q_old + self.alpha * (reward + self.gamma * q_max - q_old)