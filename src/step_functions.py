from helpers import *
import time as tm

def main_menu(context, steps):
    del steps[1:]

    choice = get_choice_from_user(
        [
            {'key': 'P', 'value': 'Purchase Ticket'},
            {'key': 'V', 'value': 'View Seating Arrangement'},
            {'key': 'S', 'value': 'Search Passenger'},
            {'key': 'Q', 'value': 'Quit System'}
        ],
        include_back_option=False,
        include_main_menu_option=False
    )

    context['main_menu_choice'] = choice

    if choice == 'P':
        steps += [
            'Purchase Ticket',
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
            'View Seating Arrangement',
            select_date,
            select_time,
            select_ferry,
            select_seat_num
        ]

    elif choice == 'S':
        steps += [
            'Search Passenger',
            select_date,
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
        [{'key': x[0], 'value': x} for x in SETTINGS['routes']],
        choice_name='route',
        include_back_option=False
    )

    return context['route_choice']

select_route.title = 'Route'

def select_date(context, steps):
    context['date_choice'] = get_choice_from_user([
        {'key': str(i), 'value': str(x)}
        for i, x in enumerate(SETTINGS['dates'])
    ], choice_name='date')

    return context['date_choice']

select_date.title = 'Date'

def select_time(context, steps):
    context['time_choice'] = get_choice_from_user([
        {'key': str(i), 'value': x} for i, x in enumerate(SETTINGS['times'])
    ], choice_name='time')

    return context['time_choice']

select_time.title = 'Time'

def select_method(context, steps):
    context['method_choice'] = get_choice_from_user([
        {'key': 'S', 'value': 'Select seats manually'}, 
        {'key': 'A', 'value': 'Auto-assign seats for me'}
    ], choice_name='method')

    return context['method_choice']

select_method.title = 'Method Selection'

def select_seats(context, steps):
    select_seats_method = auto_assign_seats
    if context['method_choice'] == 'S':
        select_seats_method = select_seats_manually

    # seats is a list of selected_seat, where selected_seat is a list containing:
    # - index for time
    # - index for ferry ID
    # - index for seat number
    # - passenger's name
    # - purchased date and time (timestamp, integer)

    context['seats'] = select_seats_method(
        context['route_choice'],
        context['date_choice'],
        context['time_choice']
    )

    return context['seats']

select_seats.title = 'Seats'

def input_seat_names(context, steps):
    print('''\
Enter passengers' name.
To go back to previous step, enter "back".
To return to main menu, enter "return".

Ferry ID  Seat Number  Passenger Name
--------  -----------  --------------\
''')

    for s in context['seats']:
        ferry_id = idx_to_ferry_id(s[0], s[1])
        seat_num = idx_to_seat(s[2])
        name = processed_input('{: <8}  {: <11}  '.format(ferry_id, seat_num))

        if name == 'back' or name == 'return':
            return name

        s[3] = name

    return context['seats']

input_seat_names.title = 'Names'

def confirm_details(context, steps):
    print('''\
Route : {}  
Date  : {}  
Time  : {}

Ferry ID  Seat Number  Passenger Name
--------  -----------  --------------\
'''.format(
    choice_to_route(context['route_choice']),
    choice_to_date(context['date_choice']),
    choice_to_time(context['time_choice'])
))

    for time_idx, ferry_idx, seat_idx, passenger_name, _ in context['seats']:
        print('{: <8}  {: <11}  {}'.format(
            idx_to_ferry_id(time_idx, ferry_idx),
            idx_to_seat(seat_idx),
            passenger_name
        ))
    print()

    choice = processed_input('Confirm? (Y-Yes, B-Back, R-Return to main menu): ')

    if choice == 'Y':
        for s in context['seats']:
            s[4] = int(tm.time())

        data_update(choice_to_date(context['date_choice']), context['seats'])

    return choice

confirm_details.title = 'Confirmation'

def print_tickets(context, steps):
    for time_idx, ferry_idx, seat_idx, passenger_name, purchased_on in context['seats']:
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
    ferry_idx_to_route(ferry_idx),
    date_to_str(choice_to_date(context['date_choice'])),
    idx_to_time(time_idx),
    idx_to_ferry_id(time_idx, ferry_idx),
    idx_to_seat(seat_idx),
    passenger_name,
    timestamp_to_str(purchased_on)
))

    return 'R'

print_tickets.title = 'Print Ticket'

def select_ferry(context, steps):
    context['ferry_choice'] = get_choice_from_user([
        {'key': str(i), 'value': x} for i, x in enumerate(SETTINGS['ferries'])
    ], choice_name='ferry')

    return context['ferry_choice']

select_ferry.title = 'Ferry'

def select_seat_num(context, steps):
    time_idx = int(context['time_choice'])
    ferry_idx = int(context['ferry_choice'])

    if time_idx%2:
        ferry_idx = (ferry_idx + 4)%8

    data = data_query(choice_to_date(context['date_choice']))
    seats = data[time_idx][ferry_idx]

    print_seating_arrangement(
        date_to_str(choice_to_date(context['date_choice'])),
        idx_to_time(time_idx), 
        idx_to_ferry_id(time_idx, ferry_idx), 
        seats
    )

    print('''\
To go back to previous step, enter "back".
To return to main menu, enter "return".
''')

    while True:
        seat_num = get_seat_num_from_user()

        if seat_num == 'back' or seat_num == 'return':
            break

        print_seat_details(seats[seat_to_idx(seat_num)])

    return seat_num

select_seat_num.title = 'Seat Number'

def search_name(context, steps):
    print('''\
To go back to previous step, enter "back".
To return to main menu, enter "return".
''')

    context['search_str'] = processed_input('Search name: ')

    return context['search_str']

search_name.title = 'Search'

def select_search_result(context, steps):
    date = choice_to_date(context['date_choice'])
    data = data_query(date)

    results = []
    for time_idx, time in enumerate(data):
        for ferry_idx, ferry in enumerate(time):
            for seat_idx, seat in enumerate(ferry):
                if seat and seat[0] == context['search_str']:
                    results.append([time_idx, ferry_idx, seat_idx, seat[0], seat[1]])
    
    context['search_results'] = results

    options = ['''\
\tName          : {}
\tRoute         : {}
\tDate and Time : {} {}
\tFerry ID      : {}
\tSeat Number   : {}
\tPurchased On  : {}
'''.format(
    passenger_name, 
    ferry_idx_to_route(ferry_idx),
    date_to_str(date),
    idx_to_time(time_idx),
    idx_to_ferry_id(time_idx, ferry_idx), 
    idx_to_seat(seat_idx),
    timestamp_to_str(purchased_on)
) for time_idx, ferry_idx, seat_idx, passenger_name, purchased_on in results]

    context['result_choice'] = get_choice_from_user([
        {'key': str(i), 'value': x} for i, x in enumerate(options)
    ], choice_name='result')

    return context['result_choice']

select_search_result.title = 'Select Result'

def process_result_selection(context, steps):
    result_idx = int(context['result_choice'])
    context['seats'] = [context['search_results'][result_idx]]

    return 'continue'

process_result_selection.title = '' # Hidden step
