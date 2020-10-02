import random
import PokeVals as poke


class Pokemon:
    def __init__(self, name):
        self.name = name
        self.level = random.choice(range(12,31))
        self.type = poke.PokemonDict[name]
        self.max_health = 5 * self.level
        self.current_health = self.max_health
        self.knocked_out = False

    def lose_health(self, lossnum):
        if self.knocked_out == True:
            print("Can't use {}, they are knocked out.".format(self.name))
        else:
            self.current_health = self.current_health - lossnum
            if self.current_health > 0:
                print("{} is now at {} health.".format(self.name, self.current_health))
            else:
                self.current_health = 0
                self.knocked_out = True
                print("{} is now knocked out.".format(self.name))

    def gain_health(self, gainnum):
        if self.knocked_out == True:
            print("Can't use {}, they are knocked out.".format(self.name))
        else:
            self.current_health += gainnum
            if self.current_health > self.max_health:
                self.current_health = self.max_health
            print("{} is now at {} health.".format(self.name, self.current_health))

    def revive(self):
        if self.knocked_out == False:
            print("{} is not knocked out!".format(self.name))
        else:
            self.knocked_out = False
            self.current_health = self.max_health / 2
            print("{} has been revived with {} health.".format(self.name, self.current_health))

    def attack(self, victim):
        if self.knocked_out == False and victim.knocked_out == False:
            print("{} attacks {}".format(self.name, victim.name))
            if self.type == victim.type:
                victim.lose_health(self.level)
            elif self.type == 'Fire' and victim.type == 'Water':
                print("It's not very effective!")
                victim.lose_health(self.level / 2)
            elif self.type == 'Fire' and victim.type == 'Grass':
                print("It's super effective!")
                victim.lose_health(self.level * 2)
            elif self.type == 'Water' and victim.type == 'Grass':
                print("It's not very effective!")
                victim.lose_health(self.level / 2)
            elif self.type == 'Water' and victim.type == 'Fire':
                print("It's super effective!")
                victim.lose_health(self.level * 2)
            elif self.type == 'Grass' and victim.type == 'Fire':
                print("It's not very effective!")
                victim.lose_health(self.level / 2)
            elif self.type == 'Grass' and victim.type == 'Water':
                print("It's super effective!")
                victim.lose_health(self.level * 2)
        elif self.knocked_out == True:
            print("{} is knocked out!".format(self.name))
        elif victim.knocked_out == True:
            print("{} is knocked out!".format(self.name))

    def showstats(self):
        yesno = "No"
        if self.knocked_out == True:
            yesno = "Yes"
        print("Pokemon:{} | Lvl:{} | Type:{} | Max HP:{} | Current HP:{} | KO'd:{}".format(self.name, self.level, self.type, self.max_health, self.current_health, yesno))


class Trainer:
    def __init__(self, name):
        self.name = name
        self.sixpokemon = []
        def pokemonfunction():
            x = random.choice(poke.PokemonList)
            poke.PokemonList.pop(poke.PokemonList.index(x))
            return x
        while len(self.sixpokemon) < 6:
            self.sixpokemon.append(pokemonfunction())
        self.pokeclasses = [Pokemon(x) for x in self.sixpokemon]
        self.activepokemon = self.pokeclasses[0]
        self.activevispokemon = self.sixpokemon[0]
        self.numpots = random.choice(range(1,5))

    def __repr__(self):
        return "Trainer: " + self.name + "\nHealing Potions: " + str(self.numpots) + "\nActive Pokemon: " + self.activevispokemon + "\nParty:"

    def showallstats(self):
        return [x.showstats() for x in self.pokeclasses]

    def changeactive(self):
        print("What would you like to change your active pokemon to? 0:{} 1:{} 2:{} 3:{} 4:{} 5:{}.".format(self.sixpokemon[0], self.sixpokemon[1], self.sixpokemon[2], self.sixpokemon[3], self.sixpokemon[4], self.sixpokemon[5]))
        newnum = int(input())
        self.activepokemon = self.pokeclasses[newnum]
        self.activevispokemon = self.sixpokemon[newnum]
        return self.activepokemon.showstats()

    def currentactive(self):
        print("Current Active Pokemon is {}.".format(self.activevispokemon))

    def fight(self, player2):
        self.activepokemon.attack(player2.activepokemon)

    def heal(self):
        if self.numpots > 0:
            self.activepokemon.gain_health(self.activepokemon.max_health/2)
            self.numpots = self.numpots - 1
        else:
            print("No healing potions left!")

    def fromthedead(self):
        self.activepokemon.revive()

    def allkocheck(self):
        allko = 0
        for pokemon in self.pokeclasses:
            if pokemon.knocked_out == False:
                allko += 1
            else:
                continue
        return allko

print("Player 1 name?")
x = input().title()
print("Player 2 name?")
y = input().title()

player1 = Trainer(x)
player2 = Trainer(y)
print(player1)
player1.showallstats()
print(player2)
player2.showallstats()

def player1choices():
    if player1.activepokemon.knocked_out == True:
        player1.changeactive()
    print("Player one's turn! Choose an action: 1. View Party Stats. | 2. Change Active Pokemon | 3. Fight | 4. Heal | 5. Pass | Input a number to make a choice")
    choice = int(input())
    if choice == 1:
        player1.showallstats()
    if choice == 2:
        player1.changeactive()
    if choice == 3:
        player1.fight(player2)
    if choice == 4:
        player1.heal()
    if choice == 5:
        pass

def player2choices():
    if player2.activepokemon.knocked_out == True:
        player2.changeactive()
    print("Player two's turn! Choose an action: 1. View Party Stats. | 2. Change Active Pokemon | 3. Fight | 4. Heal | 5. Pass | Input a number to make a choice")
    choice = int(input())
    if choice == 1:
        player2.showallstats()
    if choice == 2:
        player2.changeactive()
    if choice == 3:
        player2.fight(player1)
    if choice == 4:
        player2.heal()
    if choice == 5:
        pass

while player1.allkocheck() != 0 and player2.allkocheck() != 0:
    player1choices()
    player2choices()


if player1.allkocheck() == 0:
    print("Game Over! {} wins!".format(y))

if player2.allkocheck() == 0:
    print("Game Over! {} wins!".format(x))



