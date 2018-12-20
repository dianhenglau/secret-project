from datetime import date, timedelta, datetime
from os import mkdir
from os.path import isdir, join
import json

SETTINGS = {
    'routes': ['Penang to Langkawi', 'Langkawi to Penang'],
    'dates': [str(date.today() + timedelta(days=x)) for x in range(8)],
    'times': ['10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm'],
    'ferries': ['{:03}'.format(i) for i in range(1, 9)]
}

def get_choice_from_user(
    options,
    choice_name,
    is_numeric_option=False,
    include_back_option=True,
    include_main_menu_option=True
):

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

def auto_assign_seats(route_choice, date_choice, time_choice):
    route = choice_to_route[route_choice]
    date_idx = int(date_choice)
    time_idx = int(time_choice)

    day = date.today() + timedelta(days=date_idx)
    data = data_query(day)
    ferries = data[time_idx]

    ferry_indexes = range(0, 4)
    if route == SETTINGS['routes'][1]:
        ferry_indexes = range(4, 8)

    business_left = sum([ferries[i][:10].count(None) for i in ferry_indexes])
    economy_left = sum([ferries[i][10:].count(None) for i in ferry_indexes])

    msg, business_tickets, economy_tickets = 
        _get_number_of_tickets(business_left, economy_left)
    if msg != 'success':
        return msg

    seats = []
    for ferry_idx in ferry_indexes:
        for seat_idx, seat in enumerate(ferries[ferry_idx]):
            if seat is None:
                seats.push([time_idx, ferry_idx, seat_idx, None, None])
                found_empty_seat = True
                break

    return seats

def select_seats_manually(route_choice, date_choice, time_choice):
    pass

# TODO: honjun
def idx_to_ferry(time_idx, ferry_idx):
    pass

# TODO: honjun
#                1   2   3   4   5
#             +--------------------+
# Business  A |  0   1   2   3   4 |
#           B |  5   6   7   8   9 |
#             +--------------------+
# Economy   C | 10  11  12  13  14 |
#           D | 15  16  17  18  19 |
#           E | 20  21  22  23  24 |
#           F | 25  26  27  28  29 |
#           G | 30  31  32  33  34 |
#           H | 35  36  37  38  39 |
#           I | 40  41  42  43  44 |
#           J | 45  46  47  48  49 |
#             +--------------------+
def idx_to_seat(i):
    pass

# TODO: honjun
# 0, 1, 2, 3 -> "Penang to Langkawi"
# 4, 5, 6, 7 -> "Langkawi to Penang"
def ferry_idx_to_route(i):
    pass

# TODO: honjun
def idx_to_time(i):
    pass

# TODO: honjun
# P -> "Penang to Langkawi"
# L -> "Langkawi to Penang"
def choice_to_route(c):
    pass

def choice_to_date(c):
    pass

# TODO: honjun
# '7' -> '5pm'
# '4' -> '2pm'
# '1' -> '11am'
def choice_to_time(c):
    pass

# TODO: honjun
def seat_to_idx(seat_num):
    pass

def data_update(_date, seats):
    pass

def data_query(_date):
    pass

def print_seating_arrangement(_date, time, seats):
    pass

def get_seat_num_from_user():
    pass

def print_seat_details(seat_info):
    pass

# Private Functions
# =================

def _get_number_of_tickets():
    print('How many tickets do you want to buy?')

    while True:
        b = input('Business class: ')

        if b in ['back', 'return']:
            return b, None

        if b == '':
            b = '0'

        if not b.isdigit():
            print('Invalid input. Please enter a number.')
            continue

        b = 



    while not b.isdigit() and b != '':
        b = input('Invalid input. Enter a number: ')

    e = input('Economy class: ')
    while not e.isdigit() and e != '':
        e = input('Invalid input. Enter a number: ')

    if int(b) + int(e) == 0:
        print('Please enter 
