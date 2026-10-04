# Validation report

Students: Brooke Andrie; add teammates before submission.

Request-level checks were run on October 4, 2026 using Flask's test client, an isolated SQLite database, and real CSRF tokens. All 25 checks passed. No automated test suite is required or included with the submission.

|Area|Checks|Result|
|---|---|---|
|Authentication|Protected routes, signup, mismatched passwords, duplicate IDs, incorrect password, successful login, signout|Passed|
|Schools|Create four schools, update type/status, missing ID returns 404, delete confirmation, remove related costs|Passed|
|Costs|Create and update directed costs, allow zero, reject negative cost and invalid destination|Passed|
|Routes|Cheaper indirect route, unreachable school, direction respected, closed intermediate school excluded|Passed|
|CSRF|Token required for POST forms|Passed|

These are programmatic request checks, not a claim of completed manual browser testing. Manual testing remains listed in README.md. Docker build/run was not tested because Docker was unavailable. Branch protection, the instructor checkpoint, remote pushes, and team evaluations remain the team's responsibility.
