from main import Connect_Four
import json
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
def import_data(inputFile, dict):
    with open(inputFile, "r") as file:
        data = json.load(file)
    data.append(dict)
    with open(inputFile, "w") as file:
        json.dump(data, file)

for D1 in range(1,7):
    for D2 in range(1,7):
        output_1 = Connect_Four(D1, D2, 6, 7)
        dictionary_Depth["winner"] = output_1[0]
        dictionary_Depth["turns"] = output_1[1]
        dictionary_Depth["total_time"] = output_1[2]
        dictionary_Depth["depth_player_1"] = D1
        dictionary_Depth["depth_player_2"] = D2
        import_data("Data.json",dictionary_Depth)


# for i in range(0,5):
#     for length in range(6,9):
#         output_2  = Connect_Four( 5, 3, length, length+1 )
#         dictionary_Size["winner"] = output_2[0]
#         dictionary_Size["turns"] = output_2[1]
#         dictionary_Size["total_time"] = output_2[2]
#         dictionary_Size["row_size"] = length
#         dictionary_Size["col_size"] = length+1
#         import_data("Size_Data.json",dictionary_Size)
