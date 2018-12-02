from helpers import get_choice_from_user

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
            search_name, # input name, search it, print result
            select_search_result,
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
    if context['method_choice'] == 'S':
        seats = select_seats_manually(
            context['route_choice'],
            context['date_choice'],
            context['time_choice']
        )

    else:
        seats = auto_assign_seats(
            context['route_choice'],
            context['date_choice'],
            context['time_choice']
        )

    context['seats'] = seats

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

    choice = input('Confirm (Y: Yes, B: Back, R: Return to main menu)? ')

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
    pass

def select_seat_no(context, steps):
    pass

def search_name(context, steps):
    pass

def select_search_result(context, steps):
    pass

