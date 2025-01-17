import random

from mongoengine import *
from enum import Enum
from pprint import *
from pymongo import *
from datetime import datetime

client = MongoClient("Your Mongo URI")

clienteMongoEngine = connect(host="Your Mongo URI")

db = client.project
#db = client["Pokes"]

collection = db.pokemon
collectionTeam = db.team


class Types(Enum):
    BUG = "Bug"
    DARK = "Dark"
    DRAGON = "Dragon"
    ELECTRIC = "Electric"
    FAIRY = "Fairy"
    FIGHTING = "Fighting"
    FIRE = "Fire"
    FLYING = "Flying"
    GHOST = "Ghost"
    GRASS = "Grass"
    GROUND = "Ground"
    ICE = "Ice"
    NORMAL = "Normal"
    POISON = "Poison"
    PSYCHIC = "Psychic"
    ROCK = "Rock"
    STEEL = "Steel"
    WATER = "Water"

class Prev_evolution(EmbeddedDocument):
    num = IntField()
    name = StringField()

class Next_evolution(EmbeddedDocument):
    num = IntField()
    name = StringField()

class Pokemon(Document):
    num = IntField()
    name = StringField()
    img = StringField()
    type = ListField(EnumField(Types))
    height = StringField()
    weight = StringField()
    candy = StringField()
    candy_count = IntField()
    egg = StringField()
    spawn_chance = FloatField()
    avg_spawns = IntField()
    spawn_time = StringField()
    multipliers = ListField(FloatField())
    weaknesses = ListField(EnumField(Types))
    prev_evolution = ListField(EmbeddedDocumentField(Prev_evolution))
    next_evolution = ListField(EmbeddedDocumentField(Next_evolution))

class Moves(EmbeddedDocument):
    meta = {'allow_inheritance': True}
    name = StringField()
    pwr = FloatField(min_value=0, max_value=180)
    type = EnumField(Types)

class FastMove(Moves):
    movetype = StringField(default="Fast")
    energyGain = IntField(min_value=0, max_value=20)

class ChargedMove(Moves):
    movetype = StringField(default="Charged")
    energyCost = IntField(min_value=33, max_value=100)

class Team(Document):
    num = IntField()
    name = StringField()
    type = ListField(EnumField(Types))
    catch_date = DateField()
    CP = FloatField()
    HPmax = FloatField()
    HP = FloatField()
    atk = IntField()
    def_ = IntField(db_field="def")
    energy = IntField(min_value=0, max_value=100)
    moves = ListField(EmbeddedDocumentField(Moves))
    candy = StringField()
    candy_count = FloatField()
    current_candy = FloatField()
    weaknesses = ListField(EnumField(Types))


llamarada = ChargedMove(name="Llamarada", pwr=70, type=Types.FIRE, energyCost=50)
giroFuego = FastMove(name="Giro Fuego", pwr=14, type=Types.FIRE, energyGain=10)
ventisca = ChargedMove(name="Ventisca", pwr=130,type=Types.ICE, energyCost=100)
vahoGelido = FastMove(name="Vaho Gélido", pwr=10, type=Types.ICE, energyGain=8)

while(True):
    a = input()
    array = str(a).split(" ")
    document = ""
    if(array[0] == "Search"):
        try:
            num = int(array[1])
            if(len(array[1]) == 1):
                num = "00" + str(num)
            elif(len(array[1]) == 2):
                num = "0" + str(num)
            document = collection.find_one({"num": num}, {"_id": 0, "name": 1, str(array[2]): 1})
            document["name"]
            pprint(document)
        except:
            string = array[1]
            try:
                document = collection.find_one({"name": string}, {"_id": 0, "name": 1, str(array[2]): 1})
                pprint(document)
            except:
                print("No existeix aquest Pokémon")


    elif(array[0] == "Release"):
        try:
            num = int(array[1])
            try:
                document = collectionTeam.find_one({"num": num})
                collectionTeam.delete_one({"num": num})
                count = len(list(collectionTeam.find()))
                print(document["name"]+" alliberat. Nombre de Pokémon: " + str(count))
            except:
                print("No tens aquest Pokémon")

        except:
            string = array[1]
            try:
                document = collectionTeam.find_one({"name": string})
                collectionTeam.delete_one({"name": string})
                count = len(list(collectionTeam.find()))
                print(document["name"] + " alliberat. Nombre de Pokémon: " + str(count))
            except:
                print("No tens aquest Pokémon")

    elif(array[0] == "Catch"):
        string = array[1]
        try:
            document = Pokemon.objects(name = string)[0]
            pprint("S'ha capturat a " + document.name)
            HPMaxpok = random.randint(200, 1000)
            atkpok = random.randint(10, 50)
            defpok = random.randint(10, 50)
            CPpok = HPMaxpok + atkpok + defpok
            movespok = [llamarada, vahoGelido]
            newPokemon = Team(num=document.num, name=document.name, type=document.type, catch_date=datetime.now(),
                              CP=CPpok, HPmax=HPMaxpok, HP=HPMaxpok, atk=atkpok, def_=defpok, energy=0, moves=movespok,
                              candy=document.candy, candy_count=document.candy_count, current_candy=0,
                              weaknesses=document.weaknesses)
            newPokemon.save()
        except:
            print("No existeix aquest pokemon")

    elif(array[0] == "Candy"):
        string = array[1]
        try:
            document = Team.objects(name=string)[0]
            document.current_candy += 1
            pprint("Caramel donat a " + document.name + ". Caramels " + str(document.current_candy))
            document.save()
            try:
                if (document.current_candy >= document.candy_count):
                    document.current_candy = 0
                    document.CP += 100
                    mine = Pokemon.objects(name=document.name)[0]
                    evo = Pokemon.objects(name=mine.next_evolution[0].name)[0]
                    document.num = evo.num
                    document.name = evo.name
                    document.candy_count = evo.candy_count
                    document.save()
                    pprint(mine.name + " ha evolucionat a " + evo.name)
            except:
                print("Aquest pokemon no pot evolucionar")
        except:
            print("No tens aquest Pokémon")

    else:
        print("No he entès la comanda")


