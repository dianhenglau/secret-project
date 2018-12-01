# Data Description

Each file stores data for a day. E.g. `data_20181201.json`.

Each day has 8 times, with the following indexes:

- 0: 10am
- 1: 11am
- 2: 12pm
- 3: 1pm
- 4: 2pm
- 5: 3pm
- 6: 4pm
- 7: 5pm

Each time has 8 ferries, with the following indexes:

- 0: 001
- 1: 002
- 2: 003
- 3: 004
- 4: 005
- 5: 006
- 6: 007
- 7: 008

Each ferry has 50 seats, indexes from 0 to 49.

Each seat can either be null or object contains:

- Name (string)
- Purchased date and time (integer)

