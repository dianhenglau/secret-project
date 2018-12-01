def main_menu():
    '''\
Print main menu. Ask input from user. Print error when necessary.

Return success, choice.

success can be:
- True, if input is valid
- False, otherwise

choice can be:
- 'P'
- 'V'
- 'S'
- 'Q'
'''

    return True, input('Enter a choice: ')

def purchase_ticket():
    '''\
Let user select route, date, time, seat selection method, seat/s, and input name/s. Let user confirm the details.

Return back_to_main, date, seats.

back_to_main can be:
- True, if user want to return to main menu
- False, otherwise

date has the format 'YYYYMMDD'

seats is a list of selected_seat, where selected_seat is a tuple containing:
- index for time
- index for ferry ID
- index for seat number
- passenger's name
- purchased date and time (integer)
'''

    return False, '20181201', [(0, 0, 0, 'Grace', 100)]

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
