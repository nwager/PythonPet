import os, re, random
from datetime import datetime

def main():
    methods = {
        "rename": rename,
        "delete": delete,
        "get": getValue,
        "details": details,
        "patpat": patpat,
        "reset": reset,
    }

    if not os.path.exists("petdata.txt"):
        initialize()
    rewrite("Last interaction", datetime.now())

    done = False
    while not done:
        methodToCall = raw_input("What method do you want to call? (return to quit) ")
        if methodToCall in methods:
            if methodToCall == "get":
                attribute = raw_input("What attribute would you like? ")
                value = getValue(attribute)
                print(value)
            else:
                methods[methodToCall.lower()]()
        elif not methodToCall == "":
            print("That method doesn't exist")
        else:
            done = True

# These are some cool methods

def rename():
    name = raw_input("What name would you like to use? ")
    rewrite("Name", name)

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

def getValue(attribute):
    with open("petdata.txt", "r") as f:
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
                return value

def patpat():
    name = getValue("Name")
    prePat = getValue("Happiness")
    postPat = prePat + random.randint(3, 10)
    rewrite("Happiness", postPat)
    print("{} says {}!".format(name, getValue("Sound")))
    print("{}'s happiness increased from {} to {}!".format(name, prePat, postPat))

def initialize():
    print("\nInitializing file\n")
    with open("petdata.txt", "a+") as f:
        name = raw_input("What is your pet's name? ")
        species = raw_input("What species is {}? ".format(name))
        sound = raw_input("What sound does {} make? ".format(name))
        gender = raw_input("What gender is {}? (optional and not restricted to binary genders) ".format(name))

        f.write("Pet Data\n")
        f.write("Name: {}\n".format(name))
        f.write("Species: {}\n".format(species))
        f.write("Happiness: 20\n")
        f.write("Sound: {}\n".format(sound))
        f.write("Gender: {}\n".format(gender))
        f.write("Last interaction: {}\n".format(datetime.now()))

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