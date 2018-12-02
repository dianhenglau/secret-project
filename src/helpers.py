from datetime import date, timedelta, datetime
from os import mkdir
from os.path import isdir, join
import json


# Data Functions
# ==============

SETTINGS = {
    'routes': ['Penang to Langkawi', 'Langkawi to Penang'],
    'dates': [str(date.today() + timedelta(days=x)) for x in range(8)],
    'times': ['10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm'],
    'ferries': ['{:03}'.format(i) for i in range(1, 9)]
}

def idx_to_route(ferry_idx):
    if ferry_idx >= 4:
        return 'Langkawi to Penang'
    else:
        return 'Penang to Langkawi'

def idx_to_time(time_idx):
    return SETTINGS['times'][time_idx]

def idx_to_ferry(time_idx, ferry_idx):
    if time_idx % 2:
        ferry_idx = (ferry_idx + 4) % 8

    return SETTINGS['ferries'][ferry_idx]

def idx_to_seat(seat_idx):
    return chr(ord('A') + seat_idx // 5) + str(seat_idx % 5 + 1)

def data_query(date):
    '''\
Get data from date.

Return data. See doc/data_description.md for data format.
'''

    try:
        with open(join('data', 'data_' + str(date) + '.json'), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [[[
            None for i in range(50)]
            for j in range(8)]
            for k in range(8)]

def data_update(date, seats):
    '''\
Update given seats to data according to date.

Refer seats and date format at purchase_ticket().

Return nothing.
'''

    data = data_query(date)

    for time_idx, ferry_idx, seat_idx, passenger_name, purchase_time in seats:
        data[time_idx][ferry_idx][seat_idx] = [passenger_name, purchase_time]
    
    if not isdir('data'):
        mkdir('data', 0o755)

    with open(join('date', 'data_' + str(date) + '.json'), 'w') as f:
        json.dump(data, f)


# Common Functions
# ================

def get_choice_from_user(
    breadcrumbs,
    options, 
    choice_name, 
    is_numeric_option=False, 
    include_back_option=True,
    include_main_menu_option=True
):
    '''\
'''

    print(' > '.join(breadcrumbs))

    choices = map(str, range(len(options)))

    if not is_numeric_option:
        choices = [x[0] for x in options]

    if include_back_option:
        choices.append('B')
        options.append('Back')

    if include_main_menu_option:
        choices.append('R')
        options.append('Return to Main Menu')

    for choice, option in zip(choices, options):
        print(choice + ': ' + option)

    while True:
        choice = input('Select a ' + choice_name + ': ')

        if choice not in choices:
            print('Invalid input')
            continue

        break

    return choice

def print_tickets(date, seats):
    '''\
Print ticket/s according to date and seats.

Refer seats and date format at purchase_ticket().

Return nothing.
'''

    for time_idx, ferry_idx, seat_idx, passenger_name, purchase_time in seats:
        print('''\
    +----------------+--------------------------+
    |          Route | {: <24} |
    |           Date | {: <24} |
    |           Time | {: <24} |
    |       Ferry ID | {: <24} |
    |        Seat No | {: <24} |
    | Passenger Name | {: <24} |
    |   Purchased At | {: <24} |
    +----------------+--------------------------+

'''.format(
    idx_to_route(ferry_idx),
    str(date),
    idx_to_time(time_idx),
    idx_to_ferry(time_idx, ferry_idx)
    idx_to_seat(seat_idx),
    passenger_name,
    datetime.utcfromtimestamp(purchase_time).strftime('%Y-%m-%d %H:%M:%S')
))


# Flow Functions
# ==============

def main_menu():
    '''\
Print main menu. Ask input from user. Print error when necessary.

Return choice.

choice can be:
- 'P'
- 'V'
- 'S'
- 'Q'
'''

    breadcrumbs = ['Main Menu']

    return get_choice_from_user(breadcrumbs, [
        'Purchase Ticket',
        'View Seating Arrangement',
        'Search Passenger Info',
        'Quit System'
    ], 'choice', include_back_option=False, include_main_menu_option=False)

def get_seat_selection_from_user(
    breadcrumbs, 
    route_choice,
    date_choice, 
    time_choice, 
    method_choice
):
    '''\
'''

    pass

def purchase_ticket():
    '''\
Let user select route, date, time, seat selection method, seat/s, and input name/s. Let user confirm the details.

Return back_to_main, date, seats.

back_to_main can be:
- True, if user want to return to main menu
- False, otherwise

date has type datetime.date

seats is a list of selected_seat, where selected_seat is a tuple containing:
- index for time
- index for ferry ID
- index for seat number
- passenger's name
- purchased date and time (timestamp, integer)
'''

    breadcrumbs = ['Main Menu', 'Purchase Ticket', 'Route']

    while True:
        route_choice = get_choice_from_user(
            breadcrumbs,
            SETTINGS['routes'],
            'route',
            include_back_option=False
        )

        if route_choice == 'R':
            breadcrumbs.pop()
            return True, None, None

        breadcrumbs.push('Date')

        while True:
            date_choice = get_choice_from_user(
                breadcrumbs,
                SETTINGS['dates'],
                'date',
                is_numeric_option=True
            )
            
            if date_choice == 'B':
                breadcrumbs.pop()
                break

            elif date_choice == 'R':
                return True, None, None

            # TODO: Check if tickets of the day sold out

            breadcrumbs.push('Time')

            while True:
                time_choice = get_choice_from_user(
                    breadcrumbs,
                    SETTINGS['times'], 
                    'time', 
                    is_numeric_option=True
                )

                if time_choice == 'B':
                    breadcrumbs.pop()
                    break

                elif time_choice == 'R':
                    return True, None, None

                breadcrumbs.push('Selection Method')

                while True:
                    method_choice = get_choice_from_user(
                        breadcrumbs,
                        ['Select seat manually', 'Auto-assign seat for me'],
                        'choice'
                    )

                    if method_choice == 'B':
                        breadcrumbs.pop()
                        break

                    elif method_choice == 'R':
                        return True, None, None

                    breadcrumbs.push('Seat Selection')

                    while True:
                        seats = get_seat_selection_from_user(
                            breadcrumbs, 
                            route_choice,
                            date_choice, 
                            time_choice, 
                            method_choice
                        )

                        if seats == 'back':
                            breadcrumbs.pop()
                            break

                        elif seats == 'return':
                            return True, None, None

                        return False, date.today() + timedelta(days=date_choice), seats

def print_seating_arrangement(date_choice, time_choice, ferry_choice):
    pass

def view_seating():
    '''\
Let user select date, time, ferry ID. Show seating arrangement. User can input seat number to check passenger's information, or "end" to return to main menu, or "back" to previous page.

Return nothing.
'''

    breadcrumbs = ['Main Menu', 'View Seating', 'Date']

    while True:
        date_choice = get_choice_from_user(
            breadcrumbs,
            SETTINGS['dates'],
            'date',
            is_numeric_option=True
        )
        
        if date_choice == 'B':
            breadcrumbs.pop()
            break

        elif date_choice == 'R':
            return

        breadcrumbs.push('Time')

        while True:
            time_choice = get_choice_from_user(
                breadcrumbs,
                SETTINGS['times'], 
                'time', 
                is_numeric_option=True
            )

            if time_choice == 'B':
                breadcrumbs.pop()
                break

            elif time_choice == 'R':
                return

            breadcrumbs.push('Ferry')
            
            while True:
                ferry_choice = get_choice_from_user(
                    breadcrumbs,
                    SETTINGS['ferries'], 
                    'ferry', 
                    is_numeric_option=True
                )

                if ferry_choice == 'B':
                    breadcrumbs.pop()
                    break

                elif ferry_choice == 'R':
                    return

                date_idx = int(date_choice)
                time_idx = int(time_choice)
                ferry_idx = int(ferry_choice)

                if time_idx % 2:
                    ferry_idx = (ferry_idx + 4) % 8

                breadcrumbs.push('Seat Plan')
            
                day = date.today() + timedelta(days=date_idx)
                data = data_query(day)
                seats = data[time_idx][ferry_idx]

                print_seating_arrangement(
                    day,
                    idx_to_time(time_idx),
                    seats
                )

                while True:
                    seat_no = input('Enter seat number to check details: ')

                    if seat_no == 'back':
                        breadcrumbs.pop()
                        break

                    elif seat_no == 'return':
                        return

                    seat_idx = 

def search_passenger_info():
    '''\
Let user select route, date, time, and input name. While entering name, user can enter "end" to return to main menu, or "back" to previous page. Show search result/s. Let user select the correct result to print ticket.
'''

    print('search_passenger_info')
