import petutil as util, petaction as action
import os

def main():
    util.init()
    elapsed = util.calcElapsed()
    
    methods = {
        "delete": util.delete,
        "get": util.getValueUser,
        "details": util.details,
        "patpat": action.patpat,
        "feed": action.feed,
        "add": util.addUser,
        "edit": util.editUser,
        "reset": util.reset,
    }

    done = False
    while not done:
        if os.path.exists("petdata.txt"):
            methodToCall = raw_input("\nWhat method do you want to call? (return to quit) ").lower()
            if methodToCall in methods:
                methods[methodToCall]()
            elif not methodToCall == "":
                print("That method doesn't exist")
            else:
                done = True

if __name__ == "__main__":
    main()