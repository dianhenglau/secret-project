from datetime import date
import json

#FSD Ass Print Main Menu

def main_menu_prompt():
    print("""
FERRY TICKETING SYSTEM
P - to Purchase Ticket
V - to View Seating Arrangement
Q - to Quit the system
""")

#FSD Ass Print Route Choice

def route_choice_prompt():

    print("""
ROUTE CHOSSING MODULE
P - From Penang to Langkawi
L - From Langkawi to Penang
M - to return to Main Menu
""")
#FSD Ass Print Time Choice

def time_choice_prompt():

    print("""
DEPART TIME CHOOSING MODULE
1 - 10.00AM
2 - 11.00AM
3 - 12.00PM
4 - 1.00PM
5 - 2.00PM
6 - 3.00PM
7 - 4.00PM
8 - 5.00PM
""")
#FSD Ass Print Ticket Class Choice

def class_choice_prompt():

    print("""
PURCHASE MODULE
B - to purchase ticket for Business class
E - to purchase ticket for Economy class
M - to return to Main Menu
""")
#FSD Auto Assign Seat function

#return info
#return 0 = both business and economy are full
#return -1 = main menu
#return -2 = invalid input

def auto_assign_seat(class_choice, time_choice, ferryID_Route, data):
    if class_choice not in ['B', 'E', 'M']:
        print("Invalid input")
        return -2

    if class_choice == 'M':
        return -1

    if (class_choice == "B"):
        current_class = 'Business'
        next_class = 'Economy'
    else:
        current_class = 'Economy'
        next_class = 'Business'
        
    info = check_empty_seat(class_choice, time_choice, ferryID_Route,data)

    if (info[1] == -1): #info = [ferryID, seatnum]
        while(True):
            print(current_class, 'Class is full!\nDo you wish to be placed in', next_class,'class?\nY-Yes\nN-No\n')
            choice = input("Choose an option: ")

            if choice not in ['Y', 'N']:
                print("Invalid Input. Please enter a valid input.")
                continue

            if (choice == "Y"):
                class_choice = next_class[0]
                info = check_empty_seat(class_choice, time_choice, ferryID_Route, data)
                
                if (info[1] == -1):
                    print('Sorry.', next_class, 'class is full too!\nPlease choose another time.\n')
                    return 0

                else:
                    return info
                
            else:
                print("Next trip leaves in 1 hour. Return to Time.")
                return 0
            
    else:
        return info
#FSD Ass Print Time Choice

def ferryID_prompt():

    print("""
FERRY ID CHOOSING MODULE
1 - 001
2 - 002
3 - 003
4 - 004
5 - 005
6 - 006
7 - 007
8 - 008
""")
#FSD Print seating arrangement

def print_seating_arrangement(ferryID_choice, time_choice, data):
    seats = data[time_choice][ferryID_choice]

    n = 51
    print('*' * n)
    print('*    Ferry ID: {: <13} Date: {: <8}    *'.format(str(ferryID_choice + 1).rjust(3, '0'), date.today().strftime('%d %b %Y')))
    print('*' * n)
    print('*    {: <45}*'.format('BUSINESS CLASS'))
    print('*' * n)
    for i in range(2):
        for j in range(5):
            print('*    ' + str(seats[i * 5 + j]) + '    ', end="")
        print('*')
        print('*' * n)
    print('*    {: <45}*'.format('ECONOMY CLASS'))
    print('*' * n)
    for i in range(8):
        for j in range(5):
            print('*    ' + str(seats[10 + i * 5 + j]) + '    ', end="")
        print('*')
        print('*' * n)

def read_from_file():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [[[
            0 for i in range(50)]
            for j in range(8)]
            for k in range(8)]

def write_to_file(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

#FSD Check Empty Seat function

def check_empty_seat(class_choice, time_choice, ferryID_Route, data):
    seatnum = -1
    if (class_choice == "B"):
        for ferryID in ferryID_Route:
            try:
                index = data[time_choice][ferryID][0:10].index(0)
                data[time_choice][ferryID][index] = 1
                seatnum = index
                
                #print("Seatnum: ", seatnum)
                #print("FerryID: ", ferryID)
            except:
                pass
            if (seatnum != -1):
                #print("Seatnum: ", seatnum)
                #print("FerryID: ", ferryID)
                break

    else:
        for ferryID in ferryID_Route:
            try:
                index = data[time_choice][ferryID][10:50].index(0)
                data[time_choice][ferryID][index+10] = 1
                seatnum = index + 10
            except:
                pass
            if (seatnum != -1):
                break

    info = [ferryID, seatnum]

    return info

# Check whether all tickets are sold out

def full(ferryID_Route, data):
    for ferries in data:
        for ferryID in ferryID_Route:
            for seat in ferries[ferryID]:
                if seat == 0:
                    return False

    return True

