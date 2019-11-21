import petutil as util
import random

def patpat():
    name = util.getValue("name")
    prePat = util.getValue("happiness")
    postPat = prePat + random.randint(3, 10)
    util.edit("happiness", postPat)
    print("{} says '{}'!".format(name, util.getValue("sound")))
    print("{}'s happiness increased from {} to {}!".format(name, prePat, postPat))

def feed():
    util.edit("hunger", util.getValue("hunger") + 10)
    print("{}'s hunger level is now {}".format(util.getValue("name"), util.getValue("hunger")))