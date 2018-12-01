from helpers import *

data = read_from_file()

while(True):
    main_menu_prompt()
    mm_choice = input("Choose an option: ")

    if mm_choice not in ['P', 'V', 'Q']:
        print('Invalid input')
        continue

    if (mm_choice == "P"):
        while True:
            route_choice_prompt()
            route_choice = input("Choose an option: ")

            if route_choice not in ['P', 'L', 'M']:
                print('Invalid input')
                continue

            if (route_choice == "P" or route_choice == "L"):
                if route_choice == "P":
                    ferryID_Route = list(range(0,4))
                else:
                    ferryID_Route = list(range(4,8))

                if full(ferryID_Route, data):
                    print('Sorry, all tickets are sold out. Please come back tomorrow.')
                    break

                while (True):
                    time_choice_prompt()
                    time_choice = input('Choose an option: ')

                    try:
                        time_choice = int(time_choice) - 1
                    except:
                        print('Invalid input')
                        continue

                    if time_choice not in range(8):
                        print('Invalid input')
                        continue

                    while True:
                        class_choice_prompt()
                        class_choice = input("Choose an option: ")

                        n = auto_assign_seat(class_choice, time_choice, ferryID_Route, data)
                        write_to_file(data)
                        if (n == -1): # Go to main menu
                            break # Break class selection loop
                        elif (n == 0): # Ferries are full, or user choose no when asked about whether user want to change class
                            break # Break class selection loop
                        elif (n == -2): 
                            continue
                        
                        if time_choice % 2:
                            ferryID = (n[0] + 4) % 8
                        else:
                            ferryID = n[0]

                        seatnum = n[1]
                        print("FerryID is: 00" + str(ferryID + 1))
                        print("Seat number is:", seatnum + 1)
                        # TODO: Insert passenger's name and print ticket
                        break # Break class selection loop

                    if n == 0:
                        continue
                    else:
                        break # Break time selection loop

            break # Break route selection loop
        
    elif (mm_choice == "V"):
        while True:
            ferryID_prompt()
            ferryID_choice = input("Choose an option: ")

            try:
                ferryID_choice = int(ferryID_choice) - 1
            except:
                print("Invalid Input")
                continue

            if ferryID_choice < 0 or ferryID_choice > 7:
                print("Invalid Input")
                continue
            
            while True:
                time_choice_prompt()
                time_choice = input("Choose an option: ")

                try:
                    time_choice = int(time_choice) - 1
                except:
                    print("Invalid Input")
                    continue

                if time_choice < 0 or time_choice > 7:
                    print("Invalid Input")
                    continue

                break
            break

        print_seating_arrangement(ferryID_choice, time_choice, data)
        
    else:
        print("Quit")
        break
