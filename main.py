# Final Project for Data Structures and Algorithsm II - C950
# Created by: Elizabeth R. Yarrow
# Student ID: 001172177
import MenuControl

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    menu = MenuControl.MainMenu()
    print(menu.title)

    choice = 0
    while choice != 4:
        menu.printMainMenu()
        value = input("Please enter the number that corresponds with your selection \n Your Entry: ")
        choice = int(value)

        if choice == 1:
            menu.runSimulation()
        if choice == 2:
            print("Choose from the following time intervals: ")
            print("[1] Between 8:35 and 9:25")
            print("[2] Between 9:35 and 10:25")
            print("[3] Between 12:03 and 1:12")
            print("[4] Pick Another time")
            val = input("Your choice: ")
            response = int(val)
            if response == 1:
                menu.runSimulation('08:35')
            if response == 2:
                menu.runSimulation('09:35')
            if response == 3:
                menu.runSimulation('12:03')
            if response == 4:
                print("Please enter a time to pause the simulation. Military time should be used and leading zeroes \n"
                      "included. In other words, 09:00 is valid but 9:00 is not")
                time = input("Your choice: ")
                menu.runSimulation(time)
        if choice == 3:
            menu.showStats()
        if choice == 4:
            print("Goodbye!")




