# Data Description

Each file stores data for a day. E.g. `data_2018-12-01.json`.

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

| Index | Ferry ID, if time index is even | Ferry ID, if time index is odd |
| ----- | ------------------------------- | ------------------------------ |
| 0     | 001                             | 005                            |
| 1     | 002                             | 006                            |
| 2     | 003                             | 007                            |
| 3     | 004                             | 008                            |
| 4     | 005                             | 001                            |
| 5     | 006                             | 002                            |
| 6     | 007                             | 003                            |
| 7     | 008                             | 004                            |

Ferry index 0 to 3 always go from Penang to Langkawi. Ferry index 4 to 7 always go from Langkawi to Penang.

Each ferry has 50 seats, indexes from 0 to 49.

Each seat can either be null or object contains:

- Name (string)
- Purchased date and time (timestamp, integer)

