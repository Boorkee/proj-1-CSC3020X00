# Validation report

Students: Brooke Andrie

Request-level checks were run on October 2, 2026 using Flask's test client, an isolated SQLite database, and real CSRF tokens. All 25 checks passed. No automated test suite is required or included with the submission.

|Area|Checks|Result|
|---|---|---|
|Authentication|Protected routes, signup, mismatched passwords, duplicate IDs, incorrect password, successful login, signout|Passed|
|Schools|Create four schools, update type/status, missing ID returns 404, delete confirmation, remove related costs|Passed|
|Costs|Create and update directed costs, allow zero, reject negative cost and invalid destination|Passed|
|Routes|Cheaper indirect route, unreachable school, direction respected, closed intermediate school excluded|Passed|
|CSRF|Token required for POST forms|Passed|

Manual website testing and Docker build, run, and database persistence testing passed on October 3, 2026.
