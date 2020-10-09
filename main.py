import random
import PokeVals as poke


def dynamicinput(inputrange, inputtype=int):
    userinput = input()
    while userinput not in list(map(str, range(inputrange[0], inputrange[1]+1))):
        print("Invalid choice! Please enter a valid choice.")
        userinput = input()
    return inputtype(userinput)

class Pokemon:
    def __init__(self, name):
        self.name = name
        self.level = random.choice(range(12,31))
        self.type = poke.PokemonDict[name]
        self.max_health = 5 * self.level
        self.current_health = self.max_health
        self.knocked_out = False

    def lose_health(self, lossnum):
        if self.knocked_out:
            print(f"Can't use {self.name}, they are knocked out.")
        else:
            self.current_health = self.current_health - lossnum
            if self.current_health > 0:
                print(f"{self.name} is now at {self.current_health} health.")
            else:
                self.current_health = 0
                self.knocked_out = True
                print(f"{self.name} is now knocked out.")

    def gain_health(self, gainnum):
        if self.knocked_out:
            print(f"Can't use {self.name}, they are knocked out.")
        else:
            self.current_health += gainnum
            if self.current_health > self.max_health:
                self.current_health = self.max_health
            print(f"{self.name} is now at {self.current_health} health.")

    def revive(self):
        if not self.knocked_out:
            print(f"{self.name} is not knocked out!")
        else:
            self.knocked_out = False
            self.current_health = self.max_health / 2
            print(f"{self.name} has been revived with {self.current_health} health.")

    def attack(self, victim):
        if not self.knocked_out and not victim.knocked_out:
            print(f"{self.name} attacks {victim.name}")
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
        elif self.knocked_out:
            print(f"{self.name} is knocked out!")
        elif victim.knocked_out:
            print(f"{victim.name} is knocked out!")

    def showstats(self):
        kostatus = "No"
        if self.knocked_out:
            kostatus = "Yes"
        return f"Pokemon:{self.name} | Lvl:{self.level} | Type:{self.type} | Max HP:{self.max_health} | Current HP:{self.current_health} | KO'd:{kostatus}"


class Trainer:
    def __init__(self, name):
        self.name = name
        self.pokeclasses = []
        def pokemonfunction():
            pokemon_name = random.choice(poke.PokemonList)
            poke.PokemonList.remove(pokemon_name)
            return pokemon_name
        while len(self.pokeclasses) < 6:
            self.pokeclasses.append(Pokemon(pokemonfunction()))
        self.activepokemon = self.pokeclasses[0]
        self.activevispokemon = self.activepokemon.name
        self.numpots = random.choice(range(1,5))

    def __repr__(self):
        return f"Trainer: {self.name}\nHealing Potions: {str(self.numpots)}\nActive Pokemon: {self.activevispokemon}\nParty:"

    def showallstats(self):
        for pokemon in self.pokeclasses:
            print(pokemon.showstats())

    def changeactive(self):
        if not self.allkocheck():
            print("What would you like to change your active pokemon to?")
            for choice, pokemon in enumerate(self.pokeclasses):
                print(f"{choice}:", pokemon.showstats())
            userinput = dynamicinput((0, 5))
            if self.pokeclasses[userinput].knocked_out:
                print(f"{self.pokeclasses[userinput].name} is already knocked out! Select a different pokemon.")
                self.changeactive()
            else:
                self.activepokemon = self.pokeclasses[userinput]
                print(self.activepokemon.showstats())
        else:
            pass

    def currentactive(self):
        print(f"Current Active Pokemon is {self.activevispokemon}.")

    def fight(self, player2):
        self.activepokemon.attack(player2.activepokemon)

    def heal(self):
        if self.numpots > 0:
            self.activepokemon.gain_health(self.activepokemon.max_health/2)
            self.numpots -= 1
            print(f"{self.name} has {self.numpots} healing potions remaining.")
            return True
        else:
            print("No healing potions left!")
            return False

    def fromthedead(self):
        self.activepokemon.revive()

    def allkocheck(self):
        for pokemon in self.pokeclasses:
            if pokemon.knocked_out:
                continue
            else:
                break
        else:
            return True
        return False

print("Player 1 name?")
user1 = input().title()
print("Player 2 name?")
user2 = input().title()

player1 = Trainer(user1)
player2 = Trainer(user2)
print(player1)
player1.showallstats()
print(player2)
player2.showallstats()

def player1choices():
    if not player1.allkocheck():
        if player1.activepokemon.knocked_out:
            player1.changeactive()
        print(f"Player one({player1.name})'s turn! Choose an action: 1. View Party Stats. | 2. Change Active Pokemon | 3. Fight | 4. Heal | 5. Pass | Input a number to make a choice")
        choice = dynamicinput((1, 5))
        if choice == 1:
            player1.showallstats()
        if choice == 2:
            player1.changeactive()
        if choice == 3:
            player1.fight(player2)
        if choice == 4:
            used_pot = player1.heal()
            if not used_pot:
                player1choices()
        if choice == 5:
            pass
    else:
        pass

def player2choices():
    if not player2.allkocheck():
        if player2.activepokemon.knocked_out:
            player2.changeactive()
        print(f"Player two({player2.name})'s turn! Choose an action: 1. View Party Stats. | 2. Change Active Pokemon | 3. Fight | 4. Heal | 5. Pass | Input a number to make a choice")
        choice = dynamicinput((1, 5))
        if choice == 1:
            player2.showallstats()
        if choice == 2:
            player2.changeactive()
        if choice == 3:
            player2.fight(player1)
        if choice == 4:
            used_pot = player2.heal()
            if not used_pot:
                player2choices()
        if choice == 5:
            pass
    else:
        pass

while not player1.allkocheck() and not player2.allkocheck():
    player1choices()
    player2choices()

if player1.allkocheck():
    print(f"Game Over! All of {player1.name}'s pokemons are knocked out! {player2.name} wins!")

if player2.allkocheck():
    print(f"Game Over! All of {player2.name}'s pokemons are knocked out! {player1.name} wins!")



