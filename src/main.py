from helpers import \
    main_menu, \
    purchase_ticket, \
    print_tickets, \
    view_seating, \
    search_passenger_info

print('''
======================
Ferry Ticketing System
======================
''')

while True:
    success, choice = main_menu()

    if not success:
        continue

    if choice == 'P':
        back_to_main, date, seats = purchase_ticket()

        if back_to_main:
            continue

        data_update(date, seats)
        print_tickets(seats)

    elif choice == 'V':
        view_seating()

    elif choice == 'S':
        search_passenger_info()

    else: # Q
        break

print('System quit')
