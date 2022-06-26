import json
import matplotlib.pyplot as plt
import math


with open("Depth_Data.json", "r") as file:
    data_depth = json.load(file)

with open("Data.json", "r") as file:
    data_depth_2 = json.load(file)

with open("Size_Data.json", "r") as file:
    data_size = json.load(file)


def win_percent(number):
    win = 0
    lost = 0
    tie = 0
    for i in data_depth_2:
        if i["depth_player_1"] == number:
            if i["winner"] == 1:
                win += 1
            elif i["winner"] == 2:
                lost += 1
            else:
                tie += 1
        elif i["depth_player_2"] == number:
            if i["winner"] == 2:
                win += 1
            elif i["winner"] == 1:
                lost += 1
            else:
                tie += 1
    total = win+lost+tie
    winP = win/total * 100
    return winP, number

def Depth_time_Played():
    time= []
    depth = []
    for i in data_depth:
       depth.append(i["depth_player_2"])
       time.append(i["total_time"])
    print(time)
    return time, depth


def connect_four_size():
    size = []
    time = []
    turns = []
    winner = []
    for i in data_size:
        size.append(i["row_size"])
        time.append(i["total_time"])
        turns.append(i["turns"])
        winner.append(i["winner"])
    return size, time, turns, winner

# gets average of a lst from Size_Data.json
def calculate_average(time_turn):
    average = []
    six = 0
    seven = 0
    eight = 0
    for i in range(0,30):
        size = connect_four_size()[0]
        if time_turn == 0:
            chosen = connect_four_size()[1]
        else:
            chosen = connect_four_size()[2]
        if size[i] == 6:
            six = six + chosen[i]
        elif size[i] == 7:
            seven += chosen[i]
        elif size[i] == 8:
            eight += chosen[i]
    six = six/10
    seven = seven/10
    eight = eight/10
    average.append(six)
    average.append(seven)
    average.append(eight)


# formule for size * turns
def size_turns():
    x_axis = []
    y_axis = []
    for x in range(6, 16):
        x_axis.append(x)
        tot = pow(x,2)
        turns = 14*tot -178 * x + 591
        y_axis.append(turns)

    plt.xlabel("Size of board")
    plt.ylabel("Amount of turns to finish")
    plt.title("Size * Turns")
    plt.plot(x_axis,y_axis, marker = 'o')
    plt.show()




# y = 82,666x^2 - 987,31x + 2976,2
# formule for size * time
def size_time():
    x_axis = []
    y_axis = []
    for x in range(6,16):
        y_axis.append(x)
        tot = pow(x,2)
        time = 82.666 * tot - 987.31 * x + 2976.2
        x_axis.append(time)

    plt.xlabel("Size of board")
    plt.ylabel("Amount of time to finish")
    plt.title("Size * Time")
    plt.plot(y_axis,x_axis, marker = 'o')
    plt.show()

# formule for time * depth
# y = 0,0022e 1,8826x
# 0,0022 x 10^ 1,8826 * x
# start on depth 5 max end_depth diff for readable graph is 3-4
def time_depth(end_depth):
    x_axis = []
    y_axis = []
    for x in range(5,end_depth):
        time = 0.0022 * math.exp(1.8826*x)
        x_axis.append(x)
        y_axis.append(time)

    plt.xlabel("Depth of tree")
    plt.ylabel("Amount of time to finish")
    plt.title("Depth * time")
    plt.plot(x_axis, y_axis, marker='o')
    plt.show()



def depth_depth_turns():
    one = []
    two = []
    three = []
    four = []
    five = []
    six = []
    for i in data_depth_2:
        if i["depth_player_1"] == 1:
            one.append(i["turns"])
        elif i["depth_player_1"] == 2:
            two.append(i["turns"])
        elif i["depth_player_1"] == 3:
            three.append(i["turns"])
        elif i["depth_player_1"] == 4:
            four.append(i["turns"])
        elif i["depth_player_1"] == 5:
            five.append(i["turns"])
        elif i["depth_player_1"] == 6:
            six.append(i["turns"])

    plt.plot([1,2,3,4,5,6], one , label = "depth 1", marker='o')
    plt.plot([1,2,3,4,5,6], two , label = "depth 2" , marker='o')
    plt.plot([1,2,3,4,5,6], three , label = "depth 3", marker='o')
    plt.plot([1,2,3,4,5,6], four , label = "depth 4", marker='o')
    plt.plot([1,2,3,4,5,6], five , label = "depth 5", marker='o')
    plt.plot([1,2,3,4,5,6], six , label = "depth 6", marker='o')
    plt.legend()
    plt.xlabel("Depth count of opponent")
    plt.ylabel("Amount of turns to finish")
    plt.title("Depth * Detph * Turns")
    plt.show()
