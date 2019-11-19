import os, re, random
from datetime import datetime

attributes = {}

def main():
    if not os.path.exists("petdata.txt"):
        initialize()
    else:
        initDict()
    
    methods = {
        "delete": delete,
        "get": getValueUser,
        "details": details,
        "patpat": patpat,
        "add": addUser,
        "edit": editUser,
        "reset": reset,
        "save": save,
    }

    done = False
    while not done:
        methodToCall = raw_input("What method do you want to call? (return to quit) ").lower()
        if methodToCall in methods:
            methods[methodToCall]()
        elif not methodToCall == "":
            print("That method doesn't exist")
        else:
            answer = raw_input("Do you want to save changes? (y/n) ").lower()
            if answer.startswith("y"):
                save()
            elif not answer.startswith("n"):
                save()
                print("Didn't understand so changes were saved")
            done = True

# These are some cool methods

def delete():
    answer = raw_input("Are you sure? (y/n) ")
    if answer.lower().startswith("y"):
        os.remove("petdata.txt")
    elif answer.lower().startswith("n"):
        print("Operation canceled")
    else:
        print("Didn't understand so nothing happened")

def details():
    print("Pet details:")
    with open("petdata.txt", "r") as f:
        line = f.readline()
        line = f.readline() # skip "Pet Data" header
        while line:
            print(line),
            line = f.readline()

def rewrite(attribute, value):
    with open("petdata.txt", "r") as f:
        line = f.readline()
        with open("petdatatemp.txt", "a+") as t:
            while line:
                if line.lower().startswith(attribute.lower()):
                    t.write("{}: {}\n".format(attribute, value))
                else:
                    t.write(line)
                line = f.readline()
    
    os.remove("petdata.txt")
    os.rename("petdatatemp.txt", "petdata.txt")

def getValueUser():
    attribute = raw_input("What attribute would you like? ").lower()
    if attribute in attributes:
        print(getValue(attribute))
    else:
        print("That attribute does not exist")

def getValue(attribute):
    """with open("petdata.txt", "r") as f:
        line = f.readline()
        while line and not line.lower().startswith(attribute.lower()):
            line = f.readline()
        if not line:
            return "That attribute does not exist"
        else:
            value = line[line.index(":") + len(":"):].strip()
            if not re.search('[a-zA-Z]', value):
                #int(re.search(r'\d+', value).group()) # regex if string contains non-numbers
                return int(value)
            else:
                return value"""
    if attribute in attributes:
        return attributes[attribute]
    else:
        return "That attribute does not exist"

def patpat():
    name = getValue("Name")
    prePat = getValue("Happiness")
    postPat = prePat + random.randint(3, 10)
    rewrite("Happiness", postPat)
    print("{} says {}!".format(name, getValue("Sound")))
    print("{}'s happiness increased from {} to {}!".format(name, prePat, postPat))

def addUser():
    attribute = raw_input("What attribute would you like to add? ").lower()
    if attribute in attributes:
        print("That attribute already exists")
    else:
        value = raw_input("What is the value? ")
        add(attribute, value)

def add(attribute, value):
    attributes.update( {attribute : value} )

def editUser():
    attribute = raw_input("What attribute would you like to change? ").lower()
    if attribute in attributes:
        value = raw_input("What is the new value? ")
        edit(attribute, value)
    else:
        print("That attribute does not exist")

def edit(attribute, value):
    attributes[attribute] = value

def initialize():
    print("\nInitializing file\n")
    with open("petdata.txt", "a+") as f:
        name = raw_input("What is your pet's name? ")
        species = raw_input("What species is {}? ".format(name))
        sound = raw_input("What sound does {} make? ".format(name))
        gender = raw_input("What gender is {}? (optional and not restricted to binary genders) ".format(name))

        f.write("Pet Data\n")
        f.write("name: {}\n".format(name))
        f.write("species: {}\n".format(species))
        f.write("happiness: 20\n")
        f.write("sound: {}\n".format(sound))
        f.write("gender: {}\n".format(gender))
        f.write("last interaction: {}\n".format(datetime.now()))

        initDict()

def initDict():
    with open("petdata.txt", "r") as f:
        line = f.readline()
        while line:
            if ": " in line:
                splitted = line.split(": ")
                key = splitted[0].strip().lower()
                value = splitted[1].strip()
                attributes.update( {key : value} )
            line = f.readline()

def save():
    with open("petdata.txt", "r") as f:
        line = f.readline()
        with open("petdatatemp.txt", "a+") as t:
            alreadyUsed = []
            t.write(line) # write "Pet Data" header
            line = f.readline() # then skip to the next line
            while line:
                attr = line[:line.index(": ")].lower()
                if (attr in attributes):
                    alreadyUsed.append(attr)
                    t.write("{}: {}\n".format(attr, attributes[attr]))
                else:
                    t.write(line)
                line = f.readline()
                
            for a in attributes:
                if not a in alreadyUsed:
                    t.write("{}: {}\n".format(a, attributes[a]))
    
    os.remove("petdata.txt")
    os.rename("petdatatemp.txt", "petdata.txt")

def reset():
    answer = raw_input("Are you sure? (y/n) ")
    if answer.lower().startswith("y"):
        os.remove("petdata.txt")
        initialize()
    elif answer.lower().startswith("n"):
        print("Operation canceled")
    else:
        print("Didn't understand so nothing happened")

if __name__ == "__main__":
    main()