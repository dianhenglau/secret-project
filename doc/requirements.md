# Requirements

Build a ferry ticketing system. This system is used by ticket counter. The user is a person working at ticket counter.

## General Info

- There are 8 ferries. Each ferry had an unique ID:

    - 001
    - 002
    - 003
    - 004
    - 005
    - 006
    - 007
    - 008

- Each ferry has 50 seats. 10 seats for business class, 40 seats for economy class.

- There are two routes:

    - Penang to Langkawi
    - Langkawi to Penang

- Ferries depart at following 8 times:

    - 10am
    - 11am
    - 12pm
    - 1pm
    - 2pm
    - 3pm
    - 4pm
    - 5pm

| Times | Ferry 001 to 004     | Ferry 005 to 008     |
| ----- | -------------------- | -------------------- |
| 10am  | Penang   to Langkawi | Langkawi to Penang   |
| 11am  | Langkawi to Penang   | Penang   to Langkawi |
| 12pm  | Penang   to Langkawi | Langkawi to Penang   |
|  1pm  | Langkawi to Penang   | Penang   to Langkawi |
|  2pm  | Penang   to Langkawi | Langkawi to Penang   |
|  3pm  | Langkawi to Penang   | Penang   to Langkawi |
|  4pm  | Penang   to Langkawi | Langkawi to Penang   |
|  5pm  | Langkawi to Penang   | Penang   to Langkawi |

## Required Functions

- User can sell ferry ticket to customer.

- Customer can choose seats, or can let computer auto-assign seats.

- User can sell tickets for one week time.

- User can print ticket for customer.

- User can view seating arrangement of ferry.

- User can view passenger info, given seat number, or customer name.

- Data should be stored in file.

- There is a limit of trial for invalid input. Return to main menu if that limit is reached.

## Additional Functions

- User can set ticket price.

- User can see transaction list.

- User can see sales summary.

- User can see seats summary (how many seats left in each ferry).

