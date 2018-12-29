from os import mkdir
from os.path import isdir, join
import datetime as dt
import time as tm
import json

SETTINGS = {
    'routes': ['Penang to Langkawi', 'Langkawi to Penang'],
    'dates': [dt.date.today() + dt.timedelta(days=x) for x in range(8)],
    'times': ['10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm'],
    'ferries': ['{:03}'.format(i) for i in range(1, 9)]
}

def processed_input(prompt_str=''):
    return input(prompt_str).strip()

def get_choice_from_user(
    options,
    choice_name,
    is_numeric_option=False,
    include_back_option=True,
    include_main_menu_option=True
):

    choices = list(map(str, range(len(options))))
    options = options[:]

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
    print()

    while True:
        choice = processed_input('Select a {}: '.format(choice_name))

        if choice not in choices:
            print('Invalid input')
            continue

        return choice

def auto_assign_seats(route_choice, date_choice, time_choice):
    time_idx = int(time_choice)
    data = data_query(choice_to_date(date_choice))
    ferries = data[time_idx]

    ferry_indexes = range(0, 4)
    if choice_to_route(route_choice) == SETTINGS['routes'][1]:
        ferry_indexes = range(4, 8)

    business_left = sum([ferries[i][:10].count(None) for i in ferry_indexes])
    economy_left = sum([ferries[i][10:].count(None) for i in ferry_indexes])

    err_msg, num_of_business, num_of_economy = \
        _get_number_of_tickets(business_left, economy_left)

    if err_msg:
        return err_msg

    business_seats = []
    economy_seats = []

    for ferry_idx in ferry_indexes:
        ferry = ferries[ferry_idx]

        business_seats += [
            [time_idx, ferry_idx, i, None, None] 
            for i in range(10) if ferry[i] is None
        ][:num_of_business - len(business_seats)]

        economy_seats += [
            [time_idx, ferry_idx, i, None, None] 
            for i in range(10, 50) if ferry[i] is None
        ][:num_of_economy - len(economy_seats)]

    return business_seats + economy_seats

def select_seats_manually(route_choice, date_choice, time_choice):
    time_idx = int(time_choice)
    data = data_query(choice_to_date(date_choice))
    ferries = data[time_idx]

    ferry_indexes = range(0, 4)
    if choice_to_route(route_choice) == SETTINGS['routes'][1]:
        ferry_indexes = range(4, 8)

    seats = _get_seats_input(ferries, ferry_indexes, time_idx)

    return seats

def idx_to_ferry_id(time_idx, ferry_idx):
    if time_idx%2:
        ferry_idx = (ferry_idx + 4)%8

    return SETTINGS['ferries'][ferry_idx]

def idx_to_seat(i):
    return chr(65 + i//5) + str(i%5 + 1)

def ferry_idx_to_route(i):
    return SETTINGS['routes'][i//4]

def idx_to_time(i):
    return SETTINGS['times'][i]

def choice_to_route(c):
    return SETTINGS['routes'][0] if c == 'P' else SETTINGS['routes'][1]

def choice_to_date(c):
    return SETTINGS['dates'][int(c)]

def choice_to_time(c):
    return SETTINGS['times'][int(c)]

def seat_to_idx(seat_num):
    return (ord(seat_num[0]) - 65)*5 + int(seat_num[1]) - 1

def timestamp_to_str(timestamp):
    return tm.strftime('%Y-%m-%d %H:%M:%S', tm.localtime(timestamp))

def date_to_str(date):
    return date.strftime('%d %b %Y (%a)')

def ferry_id_to_idx(time_idx, ferry_id):
    ferry_idx = SETTINGS['ferries'].index(ferry_id)

    if time_idx%2:
        ferry_idx = (ferry_idx + 4)%8

    return ferry_idx

def data_update(date, seats):
    data = data_query(date)

    for time_idx, ferry_idx, seat_idx, passenger_name, purchase_time in seats:
        data[time_idx][ferry_idx][seat_idx] = [passenger_name, purchase_time]

    if not isdir('data'):
        mkdir('data', 0o755)

    with open(join('data', 'data-' + str(date) + '.json'), 'w') as f:
        json.dump(data, f)

def data_query(date):
    try:
        with open(join('data', 'data-' + str(date) + '.json'), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [[[
            None for i in range(50)]
            for j in range(8)]
            for k in range(8)]

def print_seating_arrangement(date, time, ferry_id, seats):
    stars = '   ' + '*'*51
    class_title_fmt = '   * {: <48}*'
    seat_row_fmt = '  ' + '*    {}    '*5 + '*'

    seats = [0 if x is None else 1 for x in seats]

    print(stars)
    print('   * Ferry {}   Date: {}   Time: {: <4} *'.format(ferry_id, date, time))
    print(stars)
    print((' ' + seat_row_fmt).format(*range(1, 6)))
    print(stars)
    print(class_title_fmt.format('BUSINESS'))
    print(stars)
    for i in range(2):
        print((chr(65 + i) + seat_row_fmt).format(*seats[i*5:(i + 1)*5]))
        print(stars)
    print(class_title_fmt.format('ECONOMY'))
    print(stars)
    for i in range(2, 10):
        print((chr(65 + i) + seat_row_fmt).format(*seats[i*5:(i + 1)*5]))
        print(stars)
    print()

def get_seat_num_from_user():
    while True:
        x = processed_input('Enter seat number to check detail (e.g. A3): ')

        if x in ['back', 'return']:
            return x

        if len(x) != 2:
            print('Invalid seat number "{}"'.format(x))
            continue

        if len(x) != 2 \
            or not ('A' <= x[0] <= 'J') \
            or not ('1' <= x[1] <= '5'):

            print('Invalid seat number "{}"'.format(x))
            continue

        return x

def print_seat_details(seat_info):
    if seat_info is None:
        print('Empty seat')
        return

    print('''
Passenger's Name: {}
Purchased On:     {}
'''.format(
    seat_info[0],
    tm.strftime('%Y-%m-%d %H:%M:%S', tm.localtime(seat_info[1]))
))

def print_breadcrumb(steps):
    titles = []
    for s in steps:
        if isinstance(s, str):
            titles.append(s)
        elif s.title:
            titles.append(s.title)

    print('\n' + ' > '.join(titles) + '\n')

# Private Functions
# =================

def _get_number_of_tickets(business_left, economy_left):
    print('''\
To go back to previous step, enter "back".
To return to main menu, enter "return".

How many tickets do you want to buy?\
''')

    class_ = ['Business', 'Economy']
    seats_left = [business_left, economy_left]
    num_of_seats = [0, 0]

    i = 0
    while i < 2:
        x = processed_input('{} class ({} seats available): '.format(
            class_[i], seats_left[i]
        ))

        if x in ['back', 'return']:
            if x == 'back' and i == 1:
                i -= 1
                continue
            return x, None, None

        if x == '':
            x = '0'

        if not x.isdigit():
            print('Invalid input. Please enter a number.')
            continue

        x = int(x)

        if x > seats_left[i]:
            print('Not enough ticket. Please enter not more than {} tickets.'.format(seats_left[i]))
            continue

        num_of_seats[i] = x

        if i == 1 and sum(num_of_seats) == 0:
            print('Please enter at least 1 ticket.')
            i = 0
            continue
            
        i += 1

    return '', num_of_seats[0], num_of_seats[1]

def _get_seats_input(ferries, ferry_indexes, time_idx):
    _print_available_seats(ferries, ferry_indexes, time_idx)

    print('''
Enter seats in the format: <ferry_id> <seat>... <ferry_id> <seat>...
For example: 001 A1 A2 G1 002 C1 D1 E1 F1 003 J5

To go back to previous step, enter "back".
To return to main menu, enter "return".
''')

    while True:
        x = processed_input('Enter seats: ')

        if x in ['back', 'return']:
            return x

        err_msg, pairs = _parse_seats_input(x)

        if err_msg:
            print(err_msg)
            continue

        failed = False
        seats = []

        for ferry_id, seat_num in pairs:
            ferry_idx = ferry_id_to_idx(time_idx, ferry_id)
            seat_idx = seat_to_idx(seat_num)

            if ferry_idx not in ferry_indexes:
                print('Ferry {} is not available.'.format(ferry_id))
                failed = True
                break

            if ferries[ferry_idx][seat_idx] is not None:
                print('Ferry {} seat {} is occupied.'.format(ferry_id, seat_num))
                failed = True
                break

            seats.append([time_idx, ferry_idx, seat_idx, None, None])

        if failed:
            continue

        return seats

def _print_available_seats(ferries, ferry_indexes, time_idx):
    ferry_ids = [idx_to_ferry_id(time_idx, i) for i in ferry_indexes]
    encoded_ferries = [[
        idx_to_seat(i) if seat is None else '__'
        for i, seat in enumerate(ferry)]
        for ferry in ferries]

    print(('    Ferry {}      '*4).format(*ferry_ids))
    print('+----------------+ '*4)
    for i in range(2):
        for j in ferry_indexes:
            print('| {} {} {} {} {} |'.format(*encoded_ferries[j][i*5:(i + 1)*5]), end=' ')
        print()
    print('+----------------+ '*4)
    for i in range(2, 10):
        for j in ferry_indexes:
            print('| {} {} {} {} {} |'.format(*encoded_ferries[j][i*5:(i + 1)*5]), end=' ')
        print()
    print('+----------------+ '*4)

def _parse_seats_input(x):
    tokens = x.split()

    current_ferry = ''
    pairs = []

    for token in tokens:
        if token in SETTINGS['ferries']:
            current_ferry = token
            continue

        if len(token) != 2 \
            or not ('A' <= token[0] <= 'J') \
            or not ('1' <= token[1] <= '5'):

            return 'Invalid seat number "{}"'.format(token), None

        if not current_ferry:
            return 'Please specify ferry ID', None

        pairs.append([current_ferry, token])

    if not pairs:
        return 'Please choose at least one seat', None

    return '', pairs

