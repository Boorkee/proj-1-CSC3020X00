# Project 1: School District Management

Student: Brooke Andrie  
Course: CSC3020 – Software Engineering Fundamentals  
Instructor: Thyago Mota  
Repository: https://github.com/Boorkee/proj-1-CSC3020X00

## Overview

This project is a Flask web application for managing schools in a small district. Users can create an account, log in, add and edit schools, delete schools, and save transportation costs between them. The app also finds the cheapest way to transfer resources between open schools.

The project follows the waterfall phases: communication, planning, modeling, construction, testing, and deployment. I am completing the project individually.

## Communication Phase

### Requirements and scope

The application implements the following features:

- User signup, login, and signout.
- A list of schools with their names, addresses, types, and operational statuses.
- Creating, updating, and deleting school records.
- Adding and updating transportation costs between schools.
- Calculating cheapest transfer routes, including routes through intermediate schools.

Resource inventory and resource availability updates are marked as planned in the assignment and are not implemented in this version. Route planning minimizes transportation costs; it does not allocate quantities of resources.

### Constraints and risks

The assignment allows three weeks and a team of up to three members. This implementation uses Python, Flask, and SQLAlchemy, and I am handling the project alone. The main risks are limited time for development and testing, and local setup problems. During Docker testing, the C: drive ran out of space. Moving Docker's storage to D: and refreshing the build cache resolved the build issues.

## Planning Phase

### Estimated schedule

This is a proposed three-week schedule, not an actual work log. Implementation and the tests documented below were completed ahead of these estimated dates.

|Phase|Task|Start|End|Duration|Deliverable|
|---|---|---|---|---|---|
|Modeling|Requirements analysis|10/04/26|10/06/26|3 days|Use case diagram|
|Modeling|Data model|10/07/26|10/08/26|2 days|Class diagram|
|Construction|Coding|10/09/26|10/17/26|9 days|Application source code|
|Construction|Testing|10/18/26|10/22/26|5 days|Test report|
|Deployment|Delivery|10/23/26|10/24/26|2 days|Final commit, push, and repository bundle|

### Team roles

|Name|Role(s)|
|---|---|
|Brooke Andrie|Manager, developer, tester, documenter|

There are no teammates, so teammate evaluations do not apply.

## Modeling Phase

### Use case diagram

The use case diagram is in [uml/use_case.wsd](uml/use_case.wsd). It shows signup, login, signout, listing schools, creating and updating schools, deleting schools, managing transfer costs, and finding cheapest routes. School management and transfer planning require authentication.

### Class diagram

The class diagram is in [uml/class.wsd](uml/class.wsd), based on [src/app/models.py](src/app/models.py).

|Class|Fields|Purpose|
|---|---|---|
|User|id, name, about, passwd|Stores account information and a hashed password|
|School|id, name, address, _type, status|Stores school information|
|TransportationCost|from_school_id, to_school_id, cost|Stores the cost of a directed transfer between two schools|

Each transportation cost has one source school and one destination school. Each school can have zero or more outgoing and incoming transportation costs. The pair of school IDs is the transportation cost's composite primary key.

School types are stored as 0 for elementary, 1 for middle, and 2 for high school. Status is stored as 0 for open and 1 for closed. The website displays the corresponding labels.

Open the `.wsd` files using a PlantUML viewer to render the diagrams.

## Implementation Phase

The app uses Flask for routes and templates, SQLAlchemy with SQLite for persistent data, Flask-Login for authentication, Flask-WTF for forms and CSRF protection, and bcrypt for password hashing.

Transportation costs are directed. Saving a cost from School A to School B does not automatically create the reverse cost. Saving an existing school pair updates its cost. Zero costs are accepted, while negative costs, transfers to the same school, and nonexistent destinations are rejected.

The supplied Dijkstra implementation in [src/app/sp.py](src/app/sp.py) calculates cheapest routes. Only open schools are included in the graph. Unreachable destinations are shown as unreachable. Deleting a school removes its incoming and outgoing transportation costs. Opening the deletion page does not delete a school; the user must submit the confirmation form.

### Project files

|Location|Contents|
|---|---|
|src/app/|Application initialization, models, forms, routes, and shortest-path code|
|templates/|HTML pages|
|static/style.css|Website styling|
|uml/|PlantUML use case and class diagrams|
|pics/|Original assignment interface examples|
|requirements.txt|Python dependencies|
|Dockerfile|Container build and startup instructions|
|SETUP.md|Additional setup and submission instructions|
|VALIDATION.md|Initial request-level verification report|

The `.gitignore` excludes the virtual environment, generated Python files, local database, environment file, and submission bundles. The `.dockerignore` excludes local development files from the image.

### Branch workflow

The supplied repository history includes the implementation branch `feature/complete-app`, its merge into `dev`, and the merge from `dev` into `main`. A separate private GitHub repository has been created, and the local repository's remote points to it. Final documentation updates are being prepared on `feature/final-updates` before merging and pushing.

### Instructor checkpoint

The mandatory instructor checkpoint has not yet been confirmed complete. The assignment requires presenting the use case and class diagrams, working baseline, protected main branch, proposed schedule, and role assignments. It specifies that the checkpoint should occur before implementation; the checkpoint still needs to be discussed with the instructor.

## Testing Phase

Manual website testing and Docker testing passed on October 4, 2026. The times below are the approximate Mountain times when results were confirmed, rather than exact test start times.

|Functionality Tested|Date|Time (Mountain)|Result|
|---|---|---|---|
|Signup and login|10/04/26|3:02 PM|passed|
|Create and list four schools; update School A's address|10/04/26|3:02 PM|passed|
|Save directed transportation costs|10/04/26|3:04 PM|passed|
|Choose cheaper indirect route and show unreachable school|10/04/26|3:04 PM|passed|
|Update existing cost and accept a zero cost|10/04/26|3:06 PM|passed|
|Recalculate routes after changing a cost|10/04/26|3:06 PM|passed|
|Reject negative costs and nonexistent destination IDs|10/04/26|3:06 PM|passed|
|Exclude closed school and restore routes when reopened|10/04/26|3:07 PM|passed|
|Require confirmation before deleting school|10/04/26|3:08 PM|passed|
|Delete school and related costs; recalculate routes|10/04/26|3:08 PM|passed|
|Signout and redirect protected page to login|10/04/26|3:10 PM|passed|
|Reject incorrect password and accept correct password|10/04/26|3:10 PM|passed|
|Reject duplicate account ID and mismatched signup passwords|10/04/26|3:10 PM|passed|
|Build Docker image successfully|10/04/26|3:58 PM|passed|
|Run Docker container and preserve account and schools after restart|10/04/26|4:03 PM|passed|

### Route test example

Schools A, B, C, and D had IDs 1, 2, 3, and 4. Costs were A to B = 4, B to C = 3, and A to C = 20. The app selected A → B → C at total cost 7, while D was unreachable. Updating A to B to zero changed the total to C to 3. Closing or deleting B changed the route to A → C at cost 20. Reopening B before deletion restored the indirect route.

## Deployment Phase

### Run locally in Windows PowerShell

From the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
$env:SECRET_KEY = "school-project-local-testing-key"
.\.venv\Scripts\python.exe -m flask --app app run
```

Open http://127.0.0.1:5000. SQLite creates the local database automatically. The key above is for local testing; use a private random key for a deployed application.

### Build and run with Docker

With Docker Desktop running, execute from the project folder:

```powershell
docker build -t district-schools .
docker volume create schools-data
docker run --rm --name district-schools-test -p 5001:5000 -e SECRET_KEY="school-project-local-testing-key" -v schools-data:/app/instance district-schools
```

Open http://localhost:5001. The image serves the application using Gunicorn. The named volume preserves the database when the container is stopped and recreated. Both the Docker build and persistence after restart were tested successfully.

### Remaining delivery requirements

- Complete the self-evaluation below.
- Confirm completion of the mandatory instructor checkpoint.
- Configure and verify main-branch protection on the private repository. This has not yet been confirmed; protection availability depends on the GitHub account plan.
- Merge final updates through `dev` into `main`, commit with the message `final submission`, and push the branches.
- Generate and verify a fresh repository bundle after the final edits.

## Self-Evaluation

Your Name: Andrie_Brooke

This project is being completed individually. No teammate evaluations are included. Complete the self-evaluation ratings honestly using the assignment's scale:

- 1: strongly disagree
- 2: disagree
- 3: neutral
- 4: agree
- 5: strongly agree

```text
[  ] I made meaningful contributions to the project.
[  ] My contributions were valuable to the team's success.
[  ] I supported collaboration within the team.
[  ] I took initiative and responsibility for my work.
[  ] I communicated effectively and was dependable.
[  ] I was present and available to the team as expected.
[  ] I fostered trust by being reliable, transparent, and respectful in all interactions.
[  ] I helped resolve disagreements constructively, promoting understanding and collaboration.
[  ] I contributed to or led decision-making processes with clarity, fairness, and consideration of team input.
```

## Submission

Submit the final `.bundle` repository file to the course dropbox. Create it from the final committed repository:

```powershell
git bundle create project-1.bundle --all
git bundle verify project-1.bundle
```

Regenerate the bundle after any additional edits or commits. Source files should identify Brooke Andrie as the sole student author. The optional graph visualization bonus is not included.
