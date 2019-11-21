from datetime import datetime
import os, re

def init():
    if not os.path.exists("config.txt"):
        initDefaultConfig()
    if not os.path.exists("petdata.txt"):
        initialize()
    stripFile("config.txt")
    stripFile("petdata.txt")



def getValueUser():
    attribute = raw_input("What attribute would you like? ").lower()
    if containsAttribute(attribute):
        print(getValue(attribute))
    else:
        print("That attribute does not exist")

def getValue(attribute):
    with open("petdata.txt", "r") as f:
        line = f.readline()
        attr = line[:line.index(": ")].lower()
        while line and attr != attribute:
            line = f.readline()
            attr = line[:line.index(": ")].lower()
        if not line:
            return "That attribute does not exist"
        else:
            value = line[line.index(":") + len(":"):].strip()
            if re.search('^[0-9\.\ ]*$', value):
                #int(re.search(r'\d+', value).group()) # regex if string contains non-numbers
                return int(value)
            else:
                return value



def editUser():
    attribute = raw_input("What attribute would you like to change? ").lower()
    if containsAttribute(attribute):
        value = raw_input("What is the new value? ")
        edit(attribute, value)
    else:
        print("That attribute does not exist")

def edit(attribute, value):
    with open("petdata.txt", "r") as f:
        line = f.readline()
        with open("petdatatemp.txt", "a+") as t:
            while line:
                attr = line[:line.index(": ")].lower()
                if attr == attribute:
                    t.write("{}: {}\n".format(attribute.lower(), value))
                else:
                    t.write(line)
                line = f.readline()
    os.remove("petdata.txt")
    os.rename("petdatatemp.txt", "petdata.txt")



def addUser():
    attribute = raw_input("What attribute would you like to add? ").lower()
    if containsAttribute(attribute):
        print("That attribute already exists")
    else:
        value = raw_input("What is the value? ")
        add(attribute, value)

def add(attribute, value):
    with open("petdata.txt", "a") as f:
        f.write("{}: {}".format(attribute, value))
    with open("config.txt", "a") as c:
        c.write(attribute)



def removeUser():
    attribute = raw_input("What attribute would you like to remove? ").lower()
    if not containsAttribute(attribute):
        print("That attribute does not exist")
    else:
        remove(attribute)

def remove(attribute):
    with open("petdata.txt", "r") as f:
        line = f.readline()
        with open("petdatatemp.txt", "a+") as t:
            while line:
                attr = line[:line.index(": ")].lower()
                if not attr == attribute:
                    t.write(line)
                line = f.readline()
    os.remove("petdata.txt")
    os.rename("petdatatemp.txt", "petdata.txt")



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
        while line:
            print(line),
            line = f.readline()



def containsAttribute(attribute):
    with open("petdata.txt", "r") as f:
        line = f.readline()
        while line:
            attr = line[:line.index(": ")].lower()
            if attribute == attr:
                return True
            line = f.readline()
        return False



def initDefaultConfig():
    with open("config.txt", "a+") as c:
        c.write("last interaction\n")
        c.write("name\n")
        c.write("species\n")
        c.write("sound\n")
        c.write("happiness\n")
        c.write("hunger\n")

def initialize():
    print("\nInitializing file\n")
    with open("petdata.txt", "a+") as f:
        with open("config.txt", "r") as c:
            attribute = c.readline().lower().strip()
            while attribute:
                if attribute == "last interaction":
                    f.write("{}: {}\n".format(attribute, datetime.now()))
                else:
                    value = raw_input("{}? ".format(attribute.capitalize()))
                    f.write("{}: {}\n".format(attribute, value))
                attribute = c.readline().lower().strip()

def reset():
    answer = raw_input("Are you sure? (y/n) ")
    if answer.lower().startswith("y"):
        os.remove("config.txt")
        os.remove("petdata.txt")
        initDefaultConfig()
        initialize()
    elif answer.lower().startswith("n"):
        print("Operation canceled")
    else:
        print("Didn't understand so nothing happened")



def stripFile(file):
    with open(file, "r") as f:
        line = f.readline()
        with open("temp" + file, "a+") as t:
            while line:
                if not line.strip() == "":
                    if not "\n" in line:
                        t.write(line + "\n")
                    else:
                        t.write(line)
                line = f.readline()
    os.remove(file)
    os.rename("temp" + file, file)



def calcElapsed():
    old = datetime.strptime(getValue("last interaction"), '%Y-%m-%d %H:%M:%S.%f')
    edit("last interaction", datetime.now())
    curr = datetime.strptime(getValue("last interaction"), '%Y-%m-%d %H:%M:%S.%f')
    elapsed = (curr - old).total_seconds()

    oldHunger = getValue("hunger")
    newHunger = oldHunger - int(elapsed * 50 / 86400) # -50 per day
    if newHunger <= 0:
        newHunger = 0
    edit("hunger", newHunger)
    print("It's been {} hours since your last interaction and {}'s hunger level is now {}".format(
        elapsed / 3600, getValue("name"), getValue("hunger")))
    return elapsed