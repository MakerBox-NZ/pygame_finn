import random
lorax = random.randint (1,6)#variable
onceler = random.randint (1,6)#variable

def dice():

    print("The guardian of the trees got ", lorax)
    print("The onceler got ", onceler)

    if lorax > onceler:
        print("You leaned the right way!")
    elif lorax == onceler:
        print("We are now harvesting the tufts")
    else:
        print("How bad can this possibly be? Who cares if a few trees are dying?")


    while true:
        print("Set the stage agian")
        roll = input()
        dice()
