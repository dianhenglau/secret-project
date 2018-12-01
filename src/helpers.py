from datetime import date, timedelta

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
- purchased date and time (integer)
'''

    breadcrumbs = ['Main Menu', 'Purchase Ticket', 'Route']

    while True:
        route_choice = get_choice_from_user(breadcrumbs, [
            'Penang to Langkawi',
            'Langkawi to Penang',
        ], 'route', include_back_option=False)

        if route_choice == 'R':
            breadcrumbs.pop()
            return True, None, None

        breadcrumbs.push('Date')

        while True:
            today = date.today()
            date_choice = get_choice_from_user(breadcrumbs, [
                str(today + timedelta(days=x)) for x in range(8)
            ], 'date', is_numeric_option=True)
            
            if date_choice == 'B':
                breadcrumbs.pop()
                break

            elif date_choice == 'R':
                return True, None, None

            breadcrumbs.push('Time')

            while True:
                time_choice = get_choice_from_user(breadcrumbs, [
                    '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm'
                ], 'time', is_numeric_option=True)

                if time_choice == 'B':
                    breadcrumbs.pop()
                    break

                elif time_choice == 'R':
                    return True, None, None

                breadcrumbs.push('Selection Method')

                while True:
                    method_choice = get_choice_from_user(breadcrumbs, [
                        'Select seat manually', 'Auto-assign seat for me'
                    ], 'choice')

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

                        return False, today + timedelta(days=date_choice), seats

def data_update(date, seats):
    '''\
Update given seats to data according to date.

Refer seats and date format at purchase_ticket().

Return nothing.
'''

    print('data_update')

def print_tickets(date, seats):
    '''\
Print ticket/s according to date and seats.

Refer seats and date format at purchase_ticket().

Return nothing.
'''

    print('print_tickets')

def view_seating():
    '''\
Let user select date, time, ferry ID. Show seating arrangement. User can input seat number to check passenger's information, or "end" to return to main menu, or "back" to previous page.

Return nothing.
'''

    print('view_seating')

def search_passenger_info():
    '''\
Let user select route, date, time, and input name. While entering name, user can enter "end" to return to main menu, or "back" to previous page. Show search result/s. Let user select the correct result to print ticket.
'''

    print('search_passenger_info')
