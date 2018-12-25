from step_functions import main_menu
from helpers import print_breadcrumb

print('''\
========================
 Ferry Ticketing System
========================\
''')

context = {}
steps = [main_menu]

i = 0
while i >= 0:
    if isinstance(steps[i], str) or steps[i].title:
        print_breadcrumb(steps[:i + 1])

    result = steps[i](context, steps)

    if result == 'B' or result == 'back':
        while True:
            i -= 1
            if callable(steps[i]):
                break
    elif result == 'R' or result == 'return':
        i = 0
    else:
        while True:
            i += 1
            if callable(steps[i]):
                break

print('\nSystem quit')
