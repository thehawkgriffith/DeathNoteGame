import numpy as np
import random


class Player:

    def __init__(self, id, role):
        self.role = role
        self.id = id
        self.alive = True
        self.detained = False

    def vote(self):
        print("Only for the eyes of", self.role)
        print("ID: ", self.id)
        return int(input("Enter your vote to detain a player: "))

    def convict(self):
        print("Only for the eyes of", self.role)
        print("ID: ", self.id)
        return int(input("Enter your vote to convict a player: "))

    def convict_vote(self):
        print("Only for the eyes of", self.role)
        print("ID: ", self.id)
        return input("Enter your vote to perform conviction: y/n")


class L(Player):

    def __init__(self, id):
        super(L, self).__init__(id, "L")
        self.prime_sus = 0
        self.truth_table = {}
        for i in range(8):
            self.truth_table[i] = "Unknown"
            if i == id:
                self.truth_table[i] = "L"

    def investigate(self):
        print("Only for the eyes of", self.role)
        print("ID: ", self.id)
        print(self.truth_table)
        print(self.prime_sus)
        print("Choose a member to investigate:")
        choice = int(input())
        return choice

    def define_prime_sus(self):
        print("Only for the eyes of", self.role)
        print("ID: ", self.id)
        choice = int(input("Choose a prime suspect."))
        self.prime_sus = choice

    def update_truth_table(self, id, role):
        self.truth_table[id] = role
        print(self.truth_table)


class Kira(Player):

    def __init__(self, id):
        super(Kira, self).__init__(id, "Kira")
        self.list_size = 6

    def generate_list(self):
        print("Only for the eyes of", self.role)
        print("ID: ", self.id)
        print("Input the death list of size", self.list_size)
        lista = input()
        print("KIRA's DEATH LIST")
        print(lista)

    def find_L(self, l_id):
        print("Only for the eyes of", self.role)
        print("ID: ", self.id)
        choice = int(input("Enter your choice of L's id:"))
        if choice == l_id:
            return True
        return False


class Kira2(Player):

    def __init__(self, id):
        super(Kira2, self).__init__(id, "Kira2")

    def kill(self):
        print("Only for the eyes of", self.role)
        print("ID: ", self.id)
        choice = int(input("ID to kill"))
        return choice


class Agent(Player):

    def __init__(self, id):
        super(Agent, self).__init__(id, "Task Force Agent")


class Environment:

    def __init__(self):
        arr = np.arange(0, 8)
        random.shuffle(arr)
        self.players = dict()
        self.players['L'] = L(arr[0])
        self.players['Kira'] = Kira(arr[1])
        self.players['Kira2'] = Kira2(arr[2])
        self.players['Agent1'] = Agent(arr[3])
        self.players['Agent2'] = Agent(arr[4])
        self.players['Agent3'] = Agent(arr[5])
        self.players['Agent4'] = Agent(arr[6])
        self.players['Agent5'] = Agent(arr[7])
        self.alive_players = list(self.players.values())
        self.id_roll_dict = {}
        for k, v in self.players.items():
            self.id_roll_dict[v.id] = v.role
        self.dead_players = []

    def start(self):
        self.render()
        self.players['Kira'].generate_list()
        choice = self.players['Kira2'].kill()
        self.players['L'].define_prime_sus()
        self.kill_player(choice)
        while True:
            if not self.players['Kira'].alive:
                print("Kira is dead, killed by the second kira.")
                print("The agents win.")
                return
            if not self.players['L'].alive:
                print("L is dead.")
                if self.players['L'].prime_sus == self.players['Kira'].id:
                    print("L's prime suspect is found to actually be Kira.")
                    print("The agents win.")
                else:
                    print("L could not find Kira.")
                    self.kira_wins()
                return
            if list(self.id_roll_dict.values()).count("Task Force Agent") == 0:
                print("All the task force agents are dead.")
                self.kira_wins()
                return
            if self.conviction_votes():
                choice = self.convict()
                if self.players['Kira'].id == choice:
                    if not self.players['Kira'].find_L(self.players["L"].id):
                        self.agents_win()
                    else:
                        self.kira_wins()
                    return
            choice = self.vote()
            self.detain(choice)
            self.night()
            self.day()
            self.remove_detention()

    def render(self):
        print("ALIAS         DETAINED     ALIVE")
        for _, player in sorted(self.players.items()):
            print(player.id, "            ", player.detained, "     ", player.alive)

    def conviction_votes(self):
        majority = False
        vote_dict = {'y': 0, 'n': 0}
        while not majority:
            vote_dict = {'y': 0, 'n': 0}
            for player in self.alive_players:
                choice = player.convict_vote()
                vote_dict[choice] += 1
            majority = self.check_majority(vote_dict)
        if max(vote_dict, key=vote_dict.get) == 'y':
            return True
        return False

    def convict(self):
        majority = False
        vote_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        while not majority:
            vote_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
            for player in self.alive_players:
                choice = player.convict()
                vote_dict[choice] += 1
            majority = self.check_majority(vote_dict)
        return max(vote_dict, key=vote_dict.get)

    def agents_win(self):
        print("The agents win, justice prevails.")
        print("Kira and the second Kira are both arrested and face life sentence.")

    def kira_wins(self):
        print("Agents Lose!")
        print("Kira becomes the god of the new world.")

    def detain(self, id):
        for i in range(len(self.alive_players)):
            if self.alive_players[i].id == id:
                self.alive_players[i].detained = True
                break

    def remove_detention(self):
        for i in range(len(self.alive_players)):
            self.alive_players[i].detained = False

    def night(self):
        self.render()
        if not self.players['L'].detained:
            choice = self.players['L'].investigate()
            role = self.id_roll_dict[choice]
            self.players['L'].update_truth_table(choice, role)
            self.players['L'].define_prime_sus()
        if not self.players['Kira'].detained:
            self.players['Kira'].generate_list()

    def day(self):
        self.render()
        if not self.players['Kira2'].detained:
            choice = self.players['Kira2'].kill()
            self.kill_player(choice)

    def vote(self):
        majority = False
        vote_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        while not majority:
            vote_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
            for player in self.alive_players:
                choice = player.vote()
                vote_dict[choice] += 1
            majority = self.check_majority(vote_dict)
        return max(vote_dict, key=vote_dict.get)

    def check_majority(self, dict):
        max_votes = max(dict.values())
        num_occur = 0
        for k, v in dict.items():
            if v == max_votes:
                num_occur += 1
        if num_occur == 1:
            return True
        return False

    def kill_player(self, id):
        for i in range(len(self.alive_players)):
            if self.alive_players[i].id == id:
                print(self.alive_players[i].role, "was killed.")
                self.alive_players[i].alive = False
                temp = self.alive_players.pop(i)
                self.dead_players.append(temp)
                self.players['Kira'].list_size -= 1
                break
