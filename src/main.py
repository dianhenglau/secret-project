from step_functions import main_menu
from helpers import print_breadcrumb

print('''\

========================
 Ferry Ticketing System
========================

''')

context = {}
steps = [main_menu]

i = 0
while i >= 0:
    print_breadcrumb(steps[:i + 1])

    result = steps[i](context, steps)
    
    if result == 'B' or result == 'back':
        i -= 1
    elif result == 'R' or result == 'return':
        i = 0
    else:
        i += 1

print('System quit')
