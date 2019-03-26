import pygame
pygame.init()
import json
from os import system
from random import choice
import sys
import time


lambo = pygame.mixer.Sound("./lambo.wav")
damn = pygame.mixer.Sound("./damn.wav")
senioraaa = pygame.mixer.Sound("./banana.wav")
portaa = pygame.mixer.Sound("./door.wav")
hammero = pygame.mixer.Sound("./hammer.wav")
newspapera = pygame.mixer.Sound("./newspaper.wav")
lanciafiiiamme = pygame.mixer.Sound("./flame.wav")
topolinello = pygame.mixer.Sound("./topolino.wav")
fiammiferino = pygame.mixer.Sound("fiammifero.wav")
lucchetto = pygame.mixer.Sound("./lucchetto.wav")

WRONG_INTERACTION_RESPONSES = [
    "non succede nulla",
    "non funziona",
    "niente da fare",
    "non credo sia la cosa giusta da fare",
    "non credo proprio",
    "non e'il caso"
]
IS_WINDOWS = sys.platform.lower() == "win32"

class Fg:
    rs="\033[00m"
    black='\033[30m'
    red='\033[31m'
    green='\033[32m'
    orange='\033[33m'
    blue='\033[34m'
    purple='\033[35m'
    cyan='\033[36m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'
    lightred='\033[91m'
    lightgreen='\033[92m'
    yellow='\033[93m'
    lightblue='\033[94m'
    pink='\033[95m'
    lightcyan='\033[96m'

class Bg:
    rs="\033[00m"
    black='\033[40m'
    red='\033[41m'
    pink='\033[95m'
    orange='\033[33m'
    green='\033[42m'
    yellow='\033[43m'
    blue='\033[44m'
    magenta='\033[45m'
    purple='\033[35m'
    lightgrey='\033[37m'
    lightcyan='\033[96m'
    cyan='\033[46m'
    white='\033[47m'

class Directions:
    N = 0
    S = 1
    W = 2
    E = 3


class Entity:
    def __init__(self, room, x, y, graphic=None, color=None, name=None, description=None, interactions=None):
        self.room = room
        self.x = x
        self.y = y
        self.graphic = graphic
        self.color = color
        self.name = name
        self.description = description
        self.interactions = interactions
        self.game = self.room.game

    def set(self, graphic, definition):
        self.graphic = graphic
        self.color = getattr(Bg, definition["color"])
        self.name = definition["name"]
        self.description = definition["description"]
        self.interactions = definition.get("interactions")

    def interact(self, item=None):
        if self.interactions:
            action = None

            if item is not None and item.graphic in self.interactions:
                action = self.interactions[item.graphic]
            elif item is None and "no-item" in self.interactions:
                action = self.interactions["no-item"]

            if action is not None:
                player = self.game.player

                if "message" in action:
                    print(action["message"])
                if action["message"] == "bravoovovovog":
                    senioraaa.play()

                elif action["message"] == "si apre" or action["message"] == "si è aperta":
                    portaa.play()

                elif action["message"] == "Non farti problemi ehh! Spacca pure con il martello ⚒ " or action["message"] == "Sembra funzionare! Stai spaccando tutto come non mai 🦄 !":
                    hammero.play()

                elif action["message"] == "Non se lo sarebbe mai aspettato. Convinto da decenni che nessuno lo avrebbe più scoperto, Raymond Charles Rowe, famoso dj della Pennsylvania noto come DJ Freez, mandava avanti brillantemente la sua carriera esibendosi davanti a un pubblico ignaro di avere davanti a sé un assassino, l'uomo che quattro giorni prima del Natale 1992 aveva ucciso brutalmente Christy Mirack, un'insegnante di scuola media di 25 anni, strangolandola nella sua casa di Lancaster, in Pennsylvania, dopo averla stu****a." or action["message"] == "Non poteva sapere che la polizia non aveva mai chiuso quel caso e, sconvolta dalla ferocia di quell'omicidio, se l'era legato al dito senza mai smettere di indagare. Così come non poteva immaginare che a tradirlo sarebbe stata, involontariamente, la sorellastra che, iscrivendosi a un sito genealogico dotato di un imponente database di dna, ha permesso agli investigatori di risalire a lui." or action["message"] == "Scomparso il giudice Reynlods che condannò all'ergastolo il killer DJ!":
                    newspapera.play()

                elif action["message"] == "Hai fuso la serratura... ora si potrà aprire con la 🔑 K" or action["message"] == "Hai sciolto il quadro!":
                    lanciafiiiamme.play()

                elif action["message"] == "Ciao, sono Topolino! Per ottenere la chiave devi darmi il tuo lanciafiamme... sei pericoloso 🧐 ":
                    topolinello.play()

                elif action["message"] == "Hai acceso la 🕯 !":
                    fiammiferino.play()

                elif action["message"] == "È la 🔑 giusta!":
                    lucchetto.play()

                elif action["message"] == "Ora hai un lanciafiamme 🔥 simile a quello di Elon Musk! 😃 ":
                    damn.play()

                elif action["message"] == "Grazie a questa molletta hai fatto partire la macchina ... è ora di fuggire!" or action["message"] == "Grazie alle chiavi hai fatto partire la macchina ... è ora di fuggire!":
                    lambo.play()
                if "transform" in action:
                    transform = action["transform"]
                    if transform == " ":
                        self.room.entities.remove(self)
                    else:
                        self.set(transform, Game.config["entities"][transform])

                if "pickup" in action:
                    player.inventory[self.graphic] = self

                if item is not None and action.get("remove_from_inventory", False) == True :
                    del player.inventory[item.graphic]

                if "move_to_room" in action:
                    player.change_room(self.game.rooms[action["move_to_room"]])

                if "game_over" in action:
                    self.game.game_over(action["game_over"])

                if "win" in action:
                    self.game.win(action["win"])
                return

        print(choice(WRONG_INTERACTION_RESPONSES))

    def __str__(self):
        return self.color + " " + self.graphic + " " + Fg.rs + Bg.rs


class Mobile(Entity):
    def __init__(self, room, x, y, graphic, color):
        Entity.__init__(self, room, x, y, graphic, color)

    def change_room(self, room):
        from_room_number = self.room.number
        self.room = room
        for entity in self.room.entities:
            if entity.graphic == str(from_room_number):
                self.x = entity.x
                self.y = entity.y
                break
        else:
            raise Exception("this room has no {} door".format(from_room_number))

    def move(self, direction):
        if direction == Directions.N and self.y > 0 and self.room.get_entity_at_coords(self.x, self.y - 1) is None:
            self.y -= 1
        elif direction == Directions.S and self.y < self.room.h - 1 and self.room.get_entity_at_coords(self.x, self.y + 1) is None:
            self.y += 1
        elif direction == Directions.W and self.x > 0 and self.room.get_entity_at_coords(self.x - 1, self.y) is None:
            self.x -= 1
        elif direction == Directions.E and self.x < self.room.w - 1 and self.room.get_entity_at_coords(self.x + 1, self.y) is None:
            self.x += 1


class Player(Mobile):
    def __init__(self, room, x, y):
        Mobile.__init__(self, room, x, y, "G", Bg.orange)
        self.inventory = {}

    def draw_inventory(self):
        print("Inventario:")
        if len(self.inventory) == 0:
            print("\t- vuoto")
        else:
            for entity in self.inventory.values():
                print("\t- {} {}: {}".format(entity, entity.name, entity.description))

    def change_player_room(self, room):
        # self.room.number
        self.room = room
        # todo set player coords based on previous room

    def get_nearby_entities(self):
        nearby_entities = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                if not x == y == 0:
                    entity = self.room.get_entity_at_coords(self.x + x, self.y + y)
                    if entity and type(entity) is not Wall:
                        nearby_entities.append(entity)

        return nearby_entities


class Wall(Entity):
    def __init__(self, room, x, y):
        Entity.__init__(self, room, x, y, " ", Bg.black)


class Game:
    config = {}
    for key in ("entities", "rooms", "game"):
        file = open("./config/{}.json".format(key))
        config[key] = json.load(file)
        file.close()

    def __init__(self):
        self.rooms = []
        for i in range(len(Game.config["rooms"])):
            room_data = Game.config["rooms"][str(i)]
            self.rooms.append(Room(self, i, room_data["color"], room_data["name"], room_data["description"]))

        self.player = Player(self.rooms[Game.config["game"]["start_room"]], *Game.config["game"]["start_coords"])

        for room in self.rooms:
            room.entities.insert(0, self.player)

    def get_current_room(self):
        return self.player.room

    def win(self, message):
        print(message)
        print(Fg.green + "HAI VINTO!" + Fg.rs)
        input()
        exit()

    def game_over(self, message):
        print(message)
        print(Fg.red + "HAI PERSO!" + Fg.rs)
        input()
        exit()

    def update(self):
        if IS_WINDOWS:
            system("cls")
        else:
            system("clear")

        print()
        self.get_current_room().draw()
        print()
        self.player.draw_inventory()
        print()
        print("Azioni:")
        print("\t- muovi con W A S D")
        nearby_entities = self.player.get_nearby_entities()
        for entity in nearby_entities:
            print("\t- {}: {}; interagisci con {}".format(entity.name, entity.description, entity))
            for inventory_entity in self.player.inventory.values():
                print("\t- usa {} con {} con {}{}".format(inventory_entity.name, entity.name, inventory_entity, entity))

        print("\t- QUIT per uscire")

        action = input().upper()
        if action == "W":
            self.player.move(Directions.N)
        elif action == "S":
            self.player.move(Directions.S)
        elif action == "A":
            self.player.move(Directions.W)
        elif action == "D":
            self.player.move(Directions.E)
        elif action == "QUIT" or action == "Q!":
            quit()
        else:
            item = None
            if len(action) > 1:
                action = action.replace(" ", "")
                item = self.player.inventory.get(action[0])
                action = action[1]

            for entity in nearby_entities:
                if action == entity.graphic:
                    entity.interact(item)
                    input("premi un tasto per continuare...")
                    break


class Room:
    def __init__(self, game, number, color, name, description):
        self.game = game
        self.number = number
        self.color = getattr(Bg, color)
        self.name = name
        self.description = description

        file = open("./config/{}.room".format(number))
        rows = file.readlines()
        file.close()
        self.h = len(rows)
        self.w = len(rows[0]) - 1
        self.entities = []

        for y in range(self.h):
            for x in range(self.w):
                char = rows[y][x].upper()
                if char == "#":
                    self.entities.append(Wall(self, x, y))
                elif char in Game.config["entities"]:
                    e = Entity(self, x, y)
                    e.set(char, Game.config["entities"][char])
                    self.entities.append(e)

    def get_entity_at_coords(self, x, y):
        for e in self.entities:
            if e.x == x and e.y == y:
                return e

    def draw(self):
        print(self.name)
        print(self.description)
        for y in range(self.h):
            for x in range(self.w):
                e = self.get_entity_at_coords(x, y)
                if e:
                    print(e, end="")
                else:
                    print(self.color + "   " + Bg.rs, end="")
            print()


g = Game()

while True:
    g.update()
