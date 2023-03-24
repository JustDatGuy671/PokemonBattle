import random
import time
import sys
import pickle

def delay_print(s):
    # print one character at a time
    # https://stackoverflow.com/questions/9246076/how-to-print-one-character-at-a-time-on-one-line
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)

class battles:

    #Main Menu
    def mainmenu():
        print("\n\tMenu\n-------------")
        for i, x in enumerate(menu):
            print(f"{i + 1}.", x)
        option = int(input("Enter option: "))
        if option == 1:
            battles.profileselection()
        elif option == 2:
            battles.newtrainer()
        elif option == 3:
            print("Thanks for playing!")
            quit()
        else:
            print("Enter a valid option")
            battles.mainmenu()
    #New profile Creation
    def newtrainer():
        print("New Trainer Profile\n-------------")
        user = input("Enter user: ")
        for i, x in enumerate(pokedex):
            print(f"{i+1}.", x)
        index = int(input("Enter Pokemon: "))
        starter = pokedex[index-1]
        lvl = 5
        print("Profile Created\n-------------")
        #Shows user what their profile is
        print(f"Pokemon Trainer: {user}\nStarter: {starter}\nLvl: {lvl}")
        #Creates profile in text to remember for later(Database)
        userdex.update({user : tuple([starter, lvl])})
        with open("profiles.txt",'ab') as profiles:
            pickle.dump(userdex, profiles)
        battles.mainmenu()

    #Battle Mode
    def profileselection():
        global user
        global starter
        global lvl
        with open("profiles.txt",'rb') as profiles:
            while 1:
                try:
                    userdex.update(pickle.load(profiles))
                except EOFError:
                    break

        print("Battle Realm\n-------------")
        if userdex:
            print("Choose Your Profile: ")
            for i, x in enumerate(userdex):
                print(f"{i+1}.", x)
            username = input("\nEnter name: ")
            if username in userdex:
                print("\nIs this your profile?")
                option = input("Enter Yes or No: ")
                if option.lower() == "yes":
                    #Makes Global Variables for the User
                    user = username
                    starter = userdex[username][0]
                    lvl = userdex[username][1]
                    battles.battle()
                elif option.lower() == "no":
                    battles.profileselection()
            else:
                print("Not a valid user")
                battles.profileselection()
        else:
            print("No profiles found")
            battles.mainmenu()
#Generating Wild Encounter
    def battle():
        global WildEncounter
        global WildLvl
        WildEncounter = random.choice(pokedex)
        WildLvl = random.randint(1,lvl+5)
        delay_print("Walking through tall grass")
        delay_print("\n-----Wild Encounter Found-----")
        delay_print(f"\nTrainer: {user}")
        delay_print(f"\nPokemon: {starter}")
        delay_print(f"\nLvl: {lvl}")
        delay_print("\n\nvs\n")
        delay_print("\nWild Encounter")
        delay_print(f"\n{WildEncounter}")
        delay_print(f"\nLvl: {WildLvl}")
        battles.battlePhase()
#Battle Phase
    def battlePhase():
        if WildEncounter in pokedexInfo:
            WildHealth = pokedexInfo[WildEncounter][0]
        if starter in pokedexInfo:
            pokeHealth = pokedexInfo[starter][0]

        while (pokeHealth > 0) and (WildHealth > 0):
            print("\n\tPokemon Battle")
            print("\n---------------------")
            print(f"\n{WildEncounter}")
            print("Lvl:", WildLvl)
            print(f"HP: {WildHealth}")
            print(f"\n\t\t\t{starter}")
            print("\t\t\t Lvl: ", lvl)
            print(f"\t\t\t  HP: {pokeHealth}")
            #Pulls move list dictionary
            print("Move List")
            for i, x in enumerate(pokedexInfo[starter][1:5]):
                print(f"{i + 1}.", x)
            option = input("Enter option: ")
            if option.isnumeric():
                delay_print(f"\n{starter} used {pokedexInfo[starter][int(option)]}!")
                WildHealth -= movedex[pokedexInfo[starter][int(option)]]
                time.sleep(1)
                #Checks if pokemon is fainted
                if pokeHealth <= 0:
                    delay_print(f"\n{starter} fainted.")
                    delay_print(f"\n{user} ran back to the Pokemon Center")
                    break
                elif WildHealth <= 0:
                    delay_print(f"\nWild {WildEncounter} fainted")
                    delay_print(f"\n{user} defeated the wild pokemon")
                    break
                #Wild Pokemon Move
                WildMove = random.randint(1,4)
                delay_print(f"\nWild {WildEncounter} used {pokedexInfo[WildEncounter][WildMove]}!")
                pokeHealth -= movedex[pokedexInfo[WildEncounter][WildMove]]
                time.sleep(1)
            else:
                print("Entered value isn't numeric.")
            #Checks if any pokemon has fainted after both have went
            if pokeHealth <= 0:
                delay_print(f"\n{starter} fainted.")
                delay_print(f"\n{user} ran back to the Pokemon Center")
                break
            elif WildHealth <= 0:
                delay_print(f"\nWild {WildEncounter} fainted")
                delay_print(f"\n{user} defeated the wild pokemon")
                break
        delay_print("\nWould you like to continue battling?\n")
        continueOption = input("Enter yes or no: ")
        if continueOption.lower() == "yes":
            battles.battle()
        elif continueOption.lower() == "no":
            battles.mainmenu()
        else:
            print("Enter yes or no please")

if __name__ == '__main__':
    pokedexInfo = {
        "Pikachu" : tuple([20, "Tackle", "Quick Attack", "Spark", "Charge"]),
        "Squirtle" : tuple([20, "Tackle", "Water Gun", "Bubble", "Rapid Spin"]),
        "Charmander" : tuple([20, "Scratch", "Ember", "Smokescreen", "Dragon Rage"]),
        "Bulbasaur" : tuple([20, "Tackle", "Razor Leaf", "Vine Whip", "Leech Seed"]),
    }
    movedex = {
        "Tackle" : 2,
        "Quick Attack" : 2,
        "Spark" : 3,
        "Charge" : 2,
        "Water Gun": 3,
        "Bubble" : 2,
        "Rapid Spin" : 2,
        "Scratch" : 2,
        "Ember" : 3,
        "Smokescreen" : 2,
        "Dragon Rage" : 10,
        "Razor Leaf" : 4,
        "Vine Whip" : 3,
        "Leech Seed": 2
    }

    pokedex = ["Pikachu","Squirtle","Charmander","Bulbasaur"]
    userdex = {
    }
    menu = ["Battle", "New Trainer", "Quit"]
    battles.mainmenu()
