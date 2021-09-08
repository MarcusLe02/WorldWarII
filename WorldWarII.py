### Python libraries ###
import time
import sys
import random
import os

### CONSTANT VARIABLES ###

### There are 6 chambers in a pistol, each number represents a different chamber ###
CHAMBER_LIST = ["1","2","3","4","5","6"]

### Items in the shop (key) and their corresponding costs (value) ###
SHOP = {'fold':3,
        'inspect':4,
        'extra':5,
        'double':5,
        'triple':8,
        'help':None,
        'exit':None}

CARD_INSTRUCTION = ("\nBuff cards:\n"
                    "Fold (3 coins): Allow player to skip a single turn.\n"
                    "Inspect (4 coins): Allow player to check the number of chamber which is on fire.\n"
                    "Debuff cards:\n"
                    "Extra (5 coins): Force the opponent to add an additional bullet to the chambers in the next turn.\n"
                    "Double (5 coins): Force the opponent shoots 2 times in the next turn.\n"
                    "Triple (8 coins): Force the opponent shoots 3 times in the next turn.\n")

BACKGROUND = ("It was 1942 - the peak World War II.\nGermany dominated Europe, America joined the fight.\n"
             "But the war had escalated that no single country could risk any more casualties.\n"
             "Troops were drained, leaders were desperated.\n"
             "And finally, an agreement was made.\n"
             "It all came down to 'the leap of faith'.\n"
             "----------------------------------------\n"
             "You - a leader from the Allies, are chosen for this responsibility,\n"
             "the future of the world, lies in your hand, in the game of death:\n"
             "RUSSIAN ROULETTE.")

### A list of strings appears before each match begins, provides context to the game ##
SCRIPT = ["Bienvenue en Vichy France, I'm Phillipe Petain - the Chief of State.\n"
                "Are you heading towards France to restore the power of the Allies?\n"
                "How could you be so naive?????\nThe Axis power is too dominant - and the ally you seek is gone.\n"
                "I will show you our prowess. Now, bring on the game!!!",

                "What leads you to the City of Rome, dares to challenge the death?\n"
                "..........\nWell, I supposed that you have marched your way through France, with high hopes\n"
                "With great courtesy from the Leader of Fascism and Founder of the Empire,\n"
                "This Benito Mussolini has to say that your hopes are going to be shattered.\n"
                "The Vichy government you proudly disbanded, was only a puppet regime.\n"
                "For the true Axis, to expand our supremacy. Against us, you could never stand a chance.\n",

                "Prime Minister: Hail to the Emperor! HIROHITO.\n"
                "Our great Emperor, The Attack on Pearl Harbor was a great success.\n"
                "It declared the dominance of Japan empire to the weakening Allies. Until...\n"
                "Emperor: Until?\nPrime Minister:.....................\n"
                "Until the Allies commander disbanded Vichy France and Italy, with the favored from 'the game of death'.\n"
                "Emperor: The West has lost to the game they created themselves....\n"
                "Mussolini was too arrogant to ignore the spirits' call....\n Though, your life will not slip through my hands.\n"
                "The odds are with me, favored by the priests, spirits, and the holy power of Kami.\n"
                "Being The Chosen One, I bet with my life, and accept the challenge.",

                "Welcome to Nazi Germany, I'm Adolf Hitler.\n"
                "After all these days, we finally met.\n"
                "I guess we no longer need to have a trivial talk, do you?\n"
                "Today is the last day of the Allies, and tomorrow is the resurgence of eternal Fascism.\n"
                "Bring on every single of your weapons to the ultimate game of Russian Roulette."]

### Variables used to input the restart/continue decisions by player ###
restart_command = ""
continue_command = ""

### Player and NPC status ###
class characters:
    alive = True
    firing_chamber = None
    bullet_chamber = []
    fold_status = False
    debuff_status = None

### Player attributes ###
class players(characters):
    buff_cards = []
    debuff_cards = []
    coin = 10
player = players()

### NPC attributes and methods ###
class npc(characters):
    def __init__(self,name,num_buff_cards,debuff_cards,rewards,script,chapter):
        """
            Function that sets up the atrributes of NPC characters in the game

            Parameter: name - a string represents the name of NPC character
                       num_buff_cards - changeable number of buff cards (fold cards) in hand of NPC character
                       debuff_cards - changable list of debuff cards in hand of NPC character
                       rewards - a number represents the number of coin in which player will receive if defeating the NPC
                       script - a string appears before the match begins, provides context to the game
                       chapter - a string represents the order of chapters (matches) in the game

        """
        self.name = name
        self.num_fold_cards = num_buff_cards
        self.debuff_cards = debuff_cards
        self.rewards = rewards
        self.script = script
        self.chapter = chapter

    def npc_prepare(self):
        """
            Function that executes the automatic preparation phase of NPC before shooting.

            Print the debuff played by player towards the NPC,
            allow NPC to choose chamber(s) to insert the bullet(s) (return randomized choice),
            and spin the gun (randomize the firing chamber)

        """
        time.sleep(2)
        print("\nIt's "+self.name+"'s turn.")
        time.sleep(2)
        if npc.debuff_status == "double":
            print(self.name + " receives double debuff. "+self.name+" has to shoot himself 2 times.")
        elif npc.debuff_status == "triple":
            print(self.name + " receives triple debuff. "+self.name+" has to shoot himself 3 times.")
        npc.bullet_chamber = random.choice(CHAMBER_LIST)
        if npc.debuff_status == "extra":
            print(self.name+" receives extra debuff. "+self.name+" has to put 2 bullets in the chambers.")
            npc.bullet_chamber = random.sample(CHAMBER_LIST, 2)
        time.sleep(1)
        print(self.name+" is choosing the chamber(s) and spin the gun.")
        npc.firing_chamber = random.choice(CHAMBER_LIST)
        time.sleep(2)
        print("The gun is spinned. "+str(self.name).capitalize()+" is deciding on his action.")
        time.sleep(2)
    def npc_use_buff(self):
        """
            Function that allows NPC to make final decisions whether to use
            buff cards before starting to shoot themselves.

            If the buff card will prevent the death, it will be played.
            Return the positive effects for NPC (activate fold status).

        """
        if set(npc.firing_chamber) <= set(npc.bullet_chamber) and self.num_fold_cards > 0:
            print(self.name+" uses fold card. "+self.name+" is allowed to fold on the next shot.")
            npc.fold_status = True
            self.num_fold_cards -= 1
            print(self.name+" has "+str(self.num_fold_cards)+" fold card left.")
        else:
            print(self.name + " does not use any card.")
    def npc_shoot(self):
        """
            Function that makes NPC shoot themselves (with all buff and debuff effects applied)

            If the firing chamber is within the bullet chamber(s),
            the gun fires and the NPC character is dead. Else, NPC ends his shooting turn.

        """
        if npc.fold_status == True:
            if npc.debuff_status == "double":
                print("Since "+self.name+" is allowed to fold, he only needs to take 1 shot.")
                if set(npc.firing_chamber) <= set(npc.bullet_chamber):
                    printIt("---")
                    time.sleep(1)
                    print("BOOM! "+self.name+" died!")
                    time.sleep(1)
                    npc.alive = False
                else:
                    printIt("---")
                    time.sleep(1)
                    print("There is nothing happened. "+self.name+" luckily survived!")
            elif npc.debuff_status == "triple":
                print("Since "+self.name+" is allowed to fold, he only needs to take 2 shots.")
                if set(npc.firing_chamber) <= set(npc.bullet_chamber):
                    printIt("---")
                    time.sleep(1)
                    print("BOOM! "+self.name+" died!")
                    time.sleep(1)
                    npc.alive = False
                else:
                    printIt("---")
                    time.sleep(1)
                    print("There is nothing happened. "+self.name+" luckily survived!")
                    time.sleep(1)
                    print(self.name+" got 1 shot left. "+self.name+" respins and prepares to shoot.")
                    npc.firing_chamber = random.choice(CHAMBER_LIST)
                    time.sleep(1)
                    if set(npc.firing_chamber) <= set(npc.bullet_chamber):
                        printIt("---")
                        time.sleep(1)
                        print("BOOM! " + self.name + " died!")
                        time.sleep(1)
                        npc.alive = False
                    else:
                        printIt("---")
                        time.sleep(1)
                        print("There is nothing happened. " + self.name + " luckily survived!")
            else:
                print("Since "+self.name+" is allowed to fold, he does not need to take any shot.")
        elif npc.fold_status == False:
            print(self.name+" is preparing to shoot.")
            if npc.debuff_status == "double":
                if set(npc.firing_chamber) <= set(npc.bullet_chamber):
                    printIt("---")
                    time.sleep(1)
                    print("BOOM! "+self.name+" died!")
                    time.sleep(1)
                    npc.alive = False
                else:
                    printIt("---")
                    time.sleep(1)
                    print("There is nothing happened. "+self.name+" luckily survived!")
                    time.sleep(1)
                    print(self.name+" got 1 shot left. "+self.name+" re-spins and prepares to shoot.")
                    npc.firing_chamber = random.choice(CHAMBER_LIST)
                    time.sleep(1)
                    if set(npc.firing_chamber) <= set(npc.bullet_chamber):
                        printIt("---")
                        time.sleep(1)
                        print("BOOM! " + self.name + " died!")
                        time.sleep(1)
                        npc.alive = False
                    else:
                        printIt("---")
                        time.sleep(1)
                        print("There is nothing happened. " + self.name + " luckily survived!")
            elif npc.debuff_status == "triple":
                if set(npc.firing_chamber) <= set(npc.bullet_chamber):
                    printIt("---")
                    time.sleep(1)
                    print("BOOM! "+self.name+" died!")
                    time.sleep(1)
                    npc.alive = False
                else:
                    printIt("---")
                    time.sleep(1)
                    print("There is nothing happened. "+self.name+" luckily survived!")
                    time.sleep(1)
                    print(self.name+" got 2 shots left. "+self.name+" re-spins and prepares to shoot.")
                    npc.firing_chamber = random.choice(CHAMBER_LIST)
                    time.sleep(1)
                    if set(npc.firing_chamber) <= set(npc.bullet_chamber):
                        printIt("---")
                        time.sleep(1)
                        print("BOOM! " + self.name + " died!")
                        time.sleep(1)
                        npc.alive = False
                    else:
                        printIt("---")
                        time.sleep(1)
                        print("There is nothing happened. " + self.name + " luckily survived!")
                        time.sleep(1)
                        print(self.name + " got 1 shot left. " + self.name + " re-spins and prepares to shoot.")
                        npc.firing_chamber = random.choice(CHAMBER_LIST)
                        time.sleep(1)
                        if set(npc.firing_chamber) <= set(npc.bullet_chamber):
                            printIt("---")
                            time.sleep(1)
                            print("BOOM! " + self.name + " died!")
                            time.sleep(1)
                            npc.alive = False
                        else:
                            printIt("---")
                            time.sleep(1)
                            print("There is nothing happened. " + self.name + " luckily survived!")
            else:
                if set(npc.firing_chamber) <= set(npc.bullet_chamber):
                    printIt("---")
                    time.sleep(1)
                    print("BOOM! " + self.name + " died!")
                    time.sleep(1)
                    npc.alive = False
                else:
                    printIt("---")
                    time.sleep(1)
                    print("There is nothing happened. " + self.name + " luckily survived!")
    def npc_use_debuff(self):
        """
            Function that happens after the shooting turn of NPC is done.
            Print the victorious messages if NPC are no longer alive.
            Allow NPC to use a random debuff cards against the player if NPC are alive.

            Reset all pre-applied effects on NPC and print either victorious messages
            or debuff cards used by NPC.

        """
        npc.firing_chamber = None
        npc.bullet_chamber = []
        npc.fold_status = False
        npc.debuff_status = None
        time.sleep(2)
        if npc.alive == False:
            print("Congratulations! You defeated "+self.name+".")
            time.sleep(1)
            print("You receives "+str(self.rewards)+" coins for defeating "+self.name+".")
            player.coin += self.rewards
            time.sleep(1)
            while True:
                continue_command = input("Do you want to continue your journey (yes/no)?")
                if continue_command.lower() == "no":
                    print("Thanks for playing the game.")
                    os.system('cls')
                    sys.exit()
                elif continue_command.lower() == "yes":
                    printIt("---")
                    break
                elif continue_command.lower() not in ["no", "yes"]:
                    print("Invalid command. Please input 'yes' or 'no'.")
        else:
            if len(self.debuff_cards) == 0:
                print(self.name+ " does not have any debuff cards left.")
            else:
                print(self.name+" is deciding on his debuff action.")
                printIt("---")
                npc_debuff_use = random.choice(self.debuff_cards)
                print(self.name+" use "+npc_debuff_use+" debuff against you.")
                time.sleep(1)
                player.debuff_status = npc_debuff_use
                self.debuff_cards.remove(npc_debuff_use)
petain = npc("Petain",0,["double"],5,SCRIPT[0],"Chapter 1: Vichy France")
mussolini = npc("Mussolini",1,["extra","triple"],10,SCRIPT[1],"Chapter 2: Italy")
hirohito = npc("Hirohito",1,["extra","double","triple","triple"],15,SCRIPT[2],"Chapter 3: Japan")
hitler = npc("Hitler",2,["extra","extra","double","double","triple"],100,SCRIPT[3],"Chapter 4: Germany")

def printIt(text):
    """
        Print the text gradually, resembling typing effect.
    """
    for character in text + '\n':
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(1)

def printIt2(text):
    """
        Print the text gradually, resembling typing effect.
    """
    for character in text + '\n':
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(1/30)

def beginning():
    """
        Function that prints the credit for the author and choices of the Choice Menu.

        Return: 
            choice(): Function that execute user's choices
    """
    print('################################')
    print('# Fulbright University Vietnam #')
    print('################################')
    print('#         World War II         #')
    print('#              By              #')
    print('#          Le Nam Dong         #')
    print('################################')
    print('#          -- Play --          #')
    print('#          -- Quit --          #')
    print('################################\n')
    choice()

def choice():
    """
        Function that prompt the user to input their choice in the opening menu of the game.

        Input: a string that represents user's choice

        Return:
            main_game_loop() : function that starts the main game adventure.

            quit : stop playing immediately and close the console window.

    """
    while True:
        choice = input('>> ')
        if choice.lower() == 'play':
            printIt2(BACKGROUND)
            main_game_loop()
            break
        elif choice.lower() == 'quit':
            os.system('cls')
            sys.exit()
        else:
            print("Error: Invalid command, please enter either 'play' or 'quit'.")

def main_game_loop():
    """
        Function that maintains the process of the game with 4 chapters
        until the player quits or finishes the game by executing the match loops.

    """
    match_loop(petain)
    match_loop(mussolini)
    match_loop(hirohito)
    match_loop(hitler)

def match_loop(npc_boss):
    """
        Function that maintains the loop of battle in each match until
        either player or npc is no longer alive, which breaks the loop immediately.

        Parameter: npc_boss - an object of class 'npc', represents the NPC characters

        Executes a sequence of functions that happens during a single match corresponding
        to the parameter.

    """
    """
        This is a description of the functions executed in a loop of each match looks like:
            shop(): Player decides whether to purchase the cards (items) in the shop
            prepare(): Player chooses the chamber to insert the bullet and spin the gun
            use_buff(): Player decides whether to use buff cards to remove negative effects
            shoot(): Player shoots themselves
            use_debuff(): If the player is alive, they decide whether to use debuff cards
                to add negative effects on NPC's turn
                If the player is dead, they decide whether to restart the game & break the loop
            npc_boss.npc_prepare(): Similar to player, automatically performed by NPC
            npc_boss.npc_use_buff(): Similar to player, automatically performed by NPC
            npc_boss.npc_shoot(): Similar to player, automatically performed by NPC
            npc_boss.npc_use_debuff(): If the NPC is alive, it automatically decide to use debuff cards against player 
                If the NPC is dead, print the victorious message & break the loop
                
    """
    print("\n")
    printIt2(npc_boss.chapter)
    time.sleep(2)
    printIt2(npc_boss.script)
    time.sleep(2)
    while True:
        shop()
        prepare()
        use_buff()
        shoot()
        use_debuff()
        npc_boss.npc_prepare()
        npc_boss.npc_use_buff()
        npc_boss.npc_shoot()
        npc_boss.npc_use_debuff()
        if npc.alive == False:
            printIt2("You completed "+str(npc_boss.chapter[:9]))
            time.sleep(1)
            break
        if hitler.alive == False:
            printIt2("The war is over. The Axis has surrendered.\n"
                     "The world has restored to the previous balance.")
            printIt("Until...")
            time.sleep(2)
            printIt2("A really 'cold' war is coming.")
            time.sleep(5)
            input("Thank you for playing the game. Press Enter to end your journey.")
            os.system('cls')
            sys.exit()

def shop():
    """
        Function that allows player to access the shop to purchase items (buffs and debuffs)
        before preparing to shoot.

        Add purchased items to player's cards and subtract corresponding costs (coins).
    """
    print("\nYou have " + str(player.coin) + " coins.")
    while True:
        print("Acceptable items or commands:")
        for key,value in SHOP.items():
            print(key+",",end=" ")
        print("\n")
        item = input("Do you want to purchase any items before starting the battle?\n"
                     "Enter the card's name to purchase.\n"
                     "Enter 'help' for prices and item instructions or 'exit' to leave the shop.")
        if item in SHOP.keys() and item not in ('exit','help'):
            if player.coin >= SHOP.get(item):
                if item in ('fold','inspect'):
                    player.buff_cards.append(item)
                else:
                    player.debuff_cards.append(item)
                player.coin = player.coin - SHOP.get(item)
                print("You purchase the "+item+" card. You have "+str(player.coin)+" coins left.\n")
            else:
                print("You do not have enough coin.")
                pass
        elif item == 'help':
            print(CARD_INSTRUCTION)
        elif item == 'exit':
            print("Your current cards:")
            print("Buff cards:"+str(player.buff_cards))
            print("Debuff cards:"+str(player.debuff_cards))
            break
        else:
            print("Invalid item or command.\n")

def prepare():
    """
        Function that executes preparation phase for player before shooting.

        Input: Number(s) for player to insert the bullet(s)

        Print the debuff played by the opponent,
        chamber(s) to insert the bullet(s) (input the bullet chamber(s))
        and spin the gun (randomize the firing chamber)

    """
    time.sleep(1)
    print("\nIt's your turn.")
    time.sleep(1)
    if player.debuff_status == "extra":
        print("You receive extra debuff. You have to put 2 bullets in the chambers.")
        while True:
            player.bullet_chamber.append(input("Choose the first chamber to put the bullet in:"))
            player.bullet_chamber.append(input("Choose the second chamber to put the bullet in:"))
            if player.bullet_chamber[0] == player.bullet_chamber[1]:
                print("You can not enter the same chamber.")
                player.bullet_chamber.clear()
            elif set(player.bullet_chamber) <= set(CHAMBER_LIST):
                input("Press Enter to spin the gun.")
                time.sleep(1)
                player.firing_chamber = random.choice(CHAMBER_LIST)
                print("The gun is spinned.")
                break
            else:
                print("Invalid chambers. Please input chambers from 1 to 6.")
                player.bullet_chamber.clear()
    elif player.debuff_status == None:
        while True:
            player.bullet_chamber.append(input("Choose a chamber to put the bullet in:"))
            if set(player.bullet_chamber) <= set(CHAMBER_LIST):
                input("Press Enter to spin the gun.")
                time.sleep(1)
                player.firing_chamber = random.choice(CHAMBER_LIST)
                print("The gun is spinned.")
                break
            else:
                print("Invalid chamber. Please input a chamber from 1 to 6.")
                player.bullet_chamber.clear()
    elif player.debuff_status == "double":
        print("You receive double debuff. You have to shoot yourself 2 times.")
        while True:
            player.bullet_chamber.append(input("Choose a chamber to put the bullet in:"))
            if set(player.bullet_chamber) <= set(CHAMBER_LIST):
                input("Press Enter to spin the gun.")
                time.sleep(1)
                player.firing_chamber = random.choice(CHAMBER_LIST)
                print("The gun is spinned.")
                break
            else:
                print("Invalid chamber. Please input a chamber from 1 to 6.")
                player.bullet_chamber.clear()
    elif player.debuff_status == "triple":
        print("You receive triple debuff. You have to shoot yourself 3 times.")
        while True:
            player.bullet_chamber.append(input("Choose a chamber to put the bullet in:"))
            if set(player.bullet_chamber) <= set(CHAMBER_LIST):
                input("Press Enter to spin the gun.")
                time.sleep(1)
                player.firing_chamber = random.choice(CHAMBER_LIST)
                print("The gun is spinned.")
                break
            else:
                print("Invalid chamber. Please input a chamber from 1 to 6.")
                player.bullet_chamber.clear()

def use_buff():
    """
        Function that allows player to make final decisions whether to use
        buff cards before starting to shoot themselves.

        Input: A string represents the name of the buff card that is already owned.

        Return: Positive effects for player (print the firing chamber or activate fold status).
    """
    print("Your buff cards:\n" + str(player.buff_cards))
    print("Do you want to use any buff before shooting?")
    while True:
        buff_use = input("Press the buff name to use the buff or press 'skip' to skip using.")
        if buff_use in player.buff_cards:
            if buff_use.lower() == "inspect":
                print("Checking the chamber which is on firing mode.")
                time.sleep(1)
                print("The gun will fire on chamber "+player.firing_chamber+".")
                player.buff_cards.remove(buff_use)
                print("Your remaining buff cards:\n" + str(player.buff_cards))
            elif buff_use.lower() == "fold":
                print("You are allowed to fold in the next shot.\n")
                player.fold_status = True
                player.buff_cards.remove(buff_use)
                print("Your remaining buff cards:\n" + str(player.buff_cards))
        elif buff_use.lower() == "skip":
            print("You complete your buff decision.")
            break
        else:
            print("Invalid command. You do not have this buff or enter an invalid command.")

def shoot():
    """
        Function that makes player shoot themselves (with all buff and debuff effects applied)

        If the firing chamber is within the bullet chamber(s), the gun fires and the player is dead.
        Else, the player ends their shooting turn and receive a coin.

    """
    if player.debuff_status == "double":
        if player.fold_status == True:
            print("Since you are allowed to fold, you only need to take 1 shot.")
            input("Press Enter to shoot to your head.")
            if set(player.firing_chamber) <= set(player.bullet_chamber):
                printIt("---")
                time.sleep(1)
                print("BOOM! You died!")
                time.sleep(1)
                player.alive = False
            else:
                printIt("---")
                time.sleep(1)
                print("There is nothing happened. You luckily survived!")
                player.coin += 2
                print("You got 2 extra coins.")
        elif player.fold_status == False:
            input("Press Enter to shoot to your head.")
            if set(player.firing_chamber) <= set(player.bullet_chamber):
                printIt("---")
                time.sleep(1)
                print("BOOM! You died!")
                time.sleep(1)
                player.alive = False
            else:
                printIt("---")
                time.sleep(1)
                print("There is nothing happened. You luckily survived!")
                player.coin += 2
                print("You got 2 extra coins.")
                time.sleep(1)
                input("You got 1 shot left. Press Enter to re-spin.")
                player.firing_chamber = random.choice(CHAMBER_LIST)
                time.sleep(1)
                input("The gun is spinned. Press Enter to shoot to your head.")
                if set(player.firing_chamber) <= set(player.bullet_chamber):
                    printIt("---")
                    time.sleep(1)
                    print("BOOM! You died!")
                    time.sleep(1)
                    player.alive = False
                else:
                    printIt("---")
                    time.sleep(1)
                    print("There is nothing happened. You luckily survived!")
                    player.coin += 2
                    print("You got 2 extra coins.")
    elif player.debuff_status == "triple":
        if player.fold_status == True:
            print("Since you are allowed to fold, you only need to take 2 shots.")
            input("Press Enter to shoot to your head.")
            if set(player.firing_chamber) <= set(player.bullet_chamber):
                printIt("---")
                time.sleep(1)
                print("BOOM! You died!")
                time.sleep(1)
                player.alive = False
            else:
                printIt("---")
                time.sleep(1)
                print("There is nothing happened. You luckily survived!")
                player.coin += 2
                print("You got 2 extra coins.")
                time.sleep(1)
                input("You got 1 shot left. Press Enter to re-spin.")
                player.firing_chamber = random.choice(CHAMBER_LIST)
                time.sleep(1)
                input("The gun is spinned. Press Enter to shoot to your head.")
                if set(player.firing_chamber) <= set(player.bullet_chamber):
                    printIt("---")
                    time.sleep(1)
                    print("BOOM! You died!")
                    time.sleep(1)
                    player.alive = False
                else:
                    printIt("---")
                    time.sleep(1)
                    print("There is nothing happened. You luckily survived!")
                    player.coin += 2
                    print("You got 2 extra coins.")
        elif player.fold_status == False:
            input("Press Enter to shoot to your head.")
            if set(player.firing_chamber) <= set(player.bullet_chamber):
                printIt("---")
                time.sleep(1)
                print("BOOM! You died!")
                time.sleep(1)
                player.alive = False
            else:
                printIt("---")
                time.sleep(1)
                print("There is nothing happened. You luckily survived!")
                player.coin += 2
                print("You got 2 extra coins.")
                time.sleep(1)
                input("You got 2 shots left. Press Enter to re-spin.")
                player.firing_chamber = random.choice(CHAMBER_LIST)
                time.sleep(1)
                input("The gun is spinned. Press Enter to shoot to your head.")
                if set(player.firing_chamber) <= set(player.bullet_chamber):
                    printIt("---")
                    time.sleep(1)
                    print("BOOM! You died!")
                    time.sleep(1)
                    player.alive = False
                else:
                    printIt("---")
                    time.sleep(1)
                    print("There is nothing happened. You luckily survived!")
                    player.coin += 2
                    print("You got 2 extra coins.")
                    time.sleep(1)
                    input("You got 1 shot left. Press Enter to re-spin.")
                    player.firing_chamber = random.choice(CHAMBER_LIST)
                    time.sleep(1)
                    input("The gun is spinned. Press Enter to shoot to your head.")
                    if set(player.firing_chamber) <= set(player.bullet_chamber):
                        printIt("---")
                        time.sleep(1)
                        print("BOOM! You died!")
                        time.sleep(1)
                        player.alive = False
                    else:
                        printIt("---")
                        time.sleep(1)
                        print("There is nothing happened. You luckily survived!")
                        player.coin += 2
                        print("You got 2 extra coins.")
    else:
        if player.fold_status == True:
            print("Since you are allowed to fold, you do not need to take any shot.")
        elif player.fold_status == False:
            input("Press Enter to shoot to your head.")
            if set(player.firing_chamber) <= set(player.bullet_chamber):
                printIt("---")
                time.sleep(1)
                print("BOOM! You died!")
                time.sleep(1)
                player.alive = False
            else:
                printIt("---")
                time.sleep(1)
                print("There is nothing happened. You luckily survived!")
                player.coin += 2
                print("You got 2 extra coins.")

def use_debuff():
    """
        Function that happens after the shooting turn is done.
        Allow the player to decide whether to restart the game if they are not alive.
        Allow the player to use debuff cards against the opponent if they are alive.

        Reset all pre-applied effects on player and NPC.
        Quit/Restart game or putting negative effects on NPC.

    """
    player.firing_chamber = None
    player.bullet_chamber = []
    player.fold_status = False
    player.debuff_status = None
    if player.alive == False:
        while True:
            restart_command = input("GAME OVER! Restart the game (yes/no)?")
            if restart_command.lower() == "no":
                print("Thanks for playing the game.")
                os.system('cls')
                sys.exit()
            elif restart_command.lower() == "yes":
                print("Restart the game.")
                player.coin = 10
                player.alive = True
                player.buff_cards = []
                player.debuff_cards = []
                main_game_loop()
                break
            elif restart_command.lower() not in ["no", "yes"]:
                print("Invalid command. Please input 'yes' or 'no'.")
    else:
        print("Your debuff cards:\n" + str(player.debuff_cards))
        time.sleep(1)
        print("Do you want to use any debuff against the opponent?")
        while True:
            debuff_use = input("Press the debuff name to use or press 'skip' to skip using.")
            if debuff_use in player.debuff_cards:
                npc.debuff_status = debuff_use
                print("You use "+debuff_use+" against the opponent.")
                player.debuff_cards.remove(debuff_use)
                break
            elif debuff_use.lower() == "skip":
                print("You do not use any buff.")
                break
            else:
                print("Invalid command. You do not have this buff or enter an invalid command.")

beginning()
