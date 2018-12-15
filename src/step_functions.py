from helpers import get_choice_from_user
from time import time
from datetime import date, timedelta, datetime

def main_menu(context, steps):
    del steps[1:]

    choice = get_choice_from_user(
        [
            'Purchase Ticket',
            'View Seating Arrangement',
            'Search Passenger Info',
            'Quit System'
        ],
        'choice',
        include_back_option=False,
        include_main_menu_option=False
    )

    context['main_menu_choice'] = choice

    if choice == 'P':
        steps += [
            select_route,
            select_date,
            select_time,
            select_method,
            select_seats,
            input_seat_names,
            confirm_details, # update data
            print_tickets
        ]

    elif choice == 'V':
        steps += [
            select_date,
            select_time,
            select_ferry,
            select_seat_no
        ]

    elif choice == 'S':
        steps += [
            select_route,
            select_date,
            select_time,
            search_name,
            select_search_result,
            process_result_selection,
            print_tickets
        ]

    else: # Q
        choice = 'B'

    return choice

main_menu.title = 'Main Menu'

def select_route(context, steps):
    context['route_choice'] = get_choice_from_user(
        SETTINGS['routes'],
        'route',
        include_back_option=False
    )

    return context['route_choice']

select_route.title = 'Route'

def select_date(context, steps):
    context['date_choice'] = get_choice_from_user(
        SETTINGS['dates'],
        'date',
        is_numeric_option=True
    )

    return context['date_choice']

select_date.title = 'Date'

def select_time(context, steps):
    context['time_choice'] = get_choice_from_user(
        SETTINGS['times'], 
        'time', 
        is_numeric_option=True
    )

    return context['time_choice']

select_time.title = 'Time'

def select_method(context, steps):
    context['method_choice'] = get_choice_from_user(
        ['Select seats manually', 'Auto-assign seats for me'],
        'choice'
    )

    return context['method_choice']

select_method.title = 'Method Selection'

def select_seats(context, steps):
    select_seats_method = auto_assign_seats
    if context['method_choice'] == 'S':
        select_seats_method = select_seats_manually

    context['seats'] = select_seats_method(
        context['route_choice'],
        context['date_choice'],
        context['time_choice']
    )

    return seats

select_seats.title = 'Seats'

def input_seat_names(context, steps):
    for s in context['seats']:
        name = input('{} {}: '.format(idx_to_ferry(s[1]), idx_to_seat(s[2])))
        if name == 'back' or name == 'return':
            return name
        s[3] = name

    return context['seats']

input_seat_names.title = 'Names'

def confirm_details(context, steps):
    print('Route: {}  Date: {}  Time: {}'.format(
        choice_to_route(context['route_choice']),
        choice_to_date(context['date_choice']),
        choice_to_time(context['time_choice'])
    ))

    for s in context['seats']:
        print('Ferry {} seat {} name {}'.format(
            idx_to_ferry(s[0], s[1]),
            idx_to_seat(s[2]),
            s[3]
        ))

    choice = input('Confirm (Y-Yes, B-Back, R-Return to main menu)? ')

    if choice == 'Y':
        for s in seats:
            s[4] = int(time.time())

        data_update(choice_to_date(context['date_choice']), context['seats'])

    return choice

confirm_details.title = 'Confirmation'

def print_tickets(context, steps):
    for time_idx, ferry_idx, seat_idx, passenger_name, purchase_time in context['seats']:
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

    return 'R'

print_tickets.title = 'Print Ticket'

def select_ferry(context, steps):
    context['ferry_choice'] = get_choice_from_user(
        SETTINGS['ferries'],
        'choice',
        is_numeric_option=True
    )

    return context['ferry_choice']

select_ferry.title = 'Ferry'

def select_seat_no(context, steps):
    date_idx = int(context['date_choice'])
    time_idx = int(context['time_choice'])
    ferry_idx = int(context['ferry_choice'])

    if time_idx % 2:
        ferry_idx = (ferry_idx + 4) % 8

    day = date.today() + timedelta(days=date_idx)
    data = data_query(day)
    seats = data[time_idx][ferry_idx]

    print_seating_arrangement(day, idx_to_time(time_idx), seats)

    while True:
        seat_no = get_seat_no_from_user()
        if seat_no == 'back' or seat_no == 'return':
            break
        print_seat_details(seats[seat_to_idx(seat_no)])

    return seat_no

select_seat_no.title = 'Seat Number'

def search_name(context, steps):
    context['search_str'] = input('Search name: ')

    return context['search_str']

search_name.title = 'Search'

def select_search_result(context, steps):
    search_str = context['search_str']

    route_idx = int(context['route_choice'])
    date_idx = int(context['date_choice'])
    time_idx = int(context['time_choice'])

    day = date.today() + timedelta(days=date_idx)
    data = data_query(day)
    
    ferry_candidates = data[time_idx][:4]
    if route_idx == 1:
        ferry_candidates = data[time_idx][4:]

    results = []
    for ferry_idx, ferry in enumerate(ferry_candidates):
        for seat_idx, seat in enumerate(ferry):
            if seat and seat[0] == search_str:
                results.push([time_idx, ferry_idx, seat_idx, seat[0], seat[1]])
    
    context['search_results'] = results
    context['result_choice'] = get_choice_from_user(
        results,
        'result',
        is_numeric_option=True
    )

    return context['result_choice']

select_search_result.title = 'Select Result'

def process_result_selection(context, steps):
    result_idx = int(context['result_choice'])
    context['seats'] = [context['search_results'][result_idx]]

    return 'continue'

process_result_selection.title = '' # Hidden step
