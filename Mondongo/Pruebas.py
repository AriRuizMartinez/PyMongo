from mongoengine import *
from pprint import *
from pymongo import *

client = MongoClient("mongodb+srv://jfunesa:1234@patatas.guqeerw.mongodb.net/")

db = client.project
#db = client["Pokes"]

collection = db.pokemon
collectionTeam = db.team

input = input()
array = str(input).split(" ")
document = ""
if (len(array) == 3):
    if (array[0] == "Search"):
        try:
            num = int(array[1])
            if (len(array[1]) == 1):
                num = "00" + str(num)
            elif (len(array[1]) == 2):
                num = "0" + str(num)
            document = collection.find_one({"num": num}, {"_id": 0, "name": 1, str(array[2]): 1})
        except:
            string = array[1]
            document = collection.find_one({"name": string}, {"_id": 0, "name": 1, str(array[2]): 1})
        pprint(document)
    elif (array[0] == "Release"):
        try:
            num = int(array[1])
            if (len(array[1]) == 1):
                num = "00" + str(num)
            elif (len(array[1]) == 2):
                num = "0" + str(num)

            document = collection.find({"num": num})
            if document is None:
                print("No tens aquest Pokémon")
            else:
                numpok = len(document)
                document = collectionTeam.delete_one({"num": num}, {"_id": 0, "name": 1})
                print(document + "alliberat.Nombre dePokémon: " + numpok - 1)



        except:
            string = array[1]
            document = collection.find({"num": num})
            if document is None:
                print("No tens aquest Pokémon")
            else:
                numpok = len(document)
                document = collectionTeam.delete_one({"name": string})
                print(string + "alliberat.Nombre dePokémon: " + numpok - 1)
    elif (array[0] == "Candy"):
        string = array[1]
        document = collection.find_one({"name": string})
        document["current_candy"]