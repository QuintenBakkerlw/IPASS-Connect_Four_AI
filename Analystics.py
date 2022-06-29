from callable_AI import Connect_Four
import json
import matplotlib.pyplot as plt
import math



# usable disctionary to be impoted to json file
dictionary_Depth = {
    "winner" : 0,
    "turns" : 0,
    "depth_player_1": 0,
    "depth_player_2": 0,
    "total_time": 0,
    "row_size" : 6,
    "col_size" : 7,
}

dictionary_Size = {
    "winner": 0,
    "turns": 0,
    "total_time": 0,
    "row_size": 0,
    "col_size": 0,
}

# function to import data to json file
def import_data(inputFile, dict):
    with open(inputFile, "r") as file:
        data = json.load(file)
    data.append(dict)
    with open(inputFile, "w") as file:
        json.dump(data, file)

# function to get data to import json file(depth info)
def Connect_four_depth():
    for D1 in range(1,7):
        for D2 in range(1,7):
            output_1 = Connect_Four(D1, D2, 6, 7)
            dictionary_Depth["winner"] = output_1[0]
            dictionary_Depth["turns"] = output_1[1]
            dictionary_Depth["total_time"] = output_1[2]
            dictionary_Depth["depth_player_1"] = D1
            dictionary_Depth["depth_player_2"] = D2
            import_data("Depth_Depth_Data.json",dictionary_Depth)

# function to get data to import json file(size info)
def Connect_four_size():
    for i in range(0,5):
        for length in range(6,9):
            output_2  = Connect_Four( 5, 3, length, length+1 )
            dictionary_Size["winner"] = output_2[0]
            dictionary_Size["turns"] = output_2[1]
            dictionary_Size["total_time"] = output_2[2]
            dictionary_Size["row_size"] = length
            dictionary_Size["col_size"] = length+1
            import_data("Json_files/Size_Data.json",dictionary_Size)


# read json files
with open("Json_files/Depth_Data.json", "r") as file:
    data_depth = json.load(file)

with open("Json_files/Depth_Depth_Data.json", "r") as file:
    data_depth_2 = json.load(file)

with open("Json_files/Size_Data.json", "r") as file:
    data_size = json.load(file)

# function to get Depth * time played
def Depth_time_Played():
    time= []
    depth = []
    for i in data_depth:
       depth.append(i["depth_player_2"])
       time.append(i["total_time"])
    return time, depth

# function to get info of size and time,turns and winners
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
def calculate_average(time_or_turn):
    average = []
    six = 0
    seven = 0
    eight = 0
    for i in range(0,30):
        size = connect_four_size()[0]
        if time_or_turn == 0:
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
    plt.plot([2,3,4,5,6], two[1:] , label = "depth 2" , marker='o')
    plt.plot([3,4,5,6], three[2:] , label = "depth 3", marker='o')
    plt.plot([4,5,6], four[3:] , label = "depth 4", marker='o')
    plt.plot([5,6], five[4:] , label = "depth 5", marker='o')
    plt.plot([6], six[5:] , label = "depth 6", marker='o')
    plt.legend()
    plt.xlabel("Depth count of opponent")
    plt.ylabel("Amount of turns to finish")
    plt.title("Depth * Detph * Turns")
    plt.show()
