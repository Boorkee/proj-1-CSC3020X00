# Setup and submission

Students: Brooke Andrie; add teammates before submission.

## Run in Windows PowerShell

Open PowerShell in this project folder. Use Python 3.12 or newer.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
$env:SECRET_KEY = "replace-this-with-a-long-random-secret"
.\.venv\Scripts\python.exe -m flask --app app run
```

Open http://127.0.0.1:5000 and sign up. The SQLite database is created automatically in `instance/`. Keep `SECRET_KEY` consistent between restarts.

## Manual tests

1. Try opening `/schools` while logged out. It should send you to login.
2. Sign up; try mismatched passwords and a duplicate ID. Log in with a wrong password, then the correct one.
3. Create schools A, B, C, and D. Note their IDs. Update a school and check that type and status save.
4. Save A to B at cost 4, B to C at cost 3, and A to C at cost 20. A's routes should show A → B → C at cost 7. D should be unreachable.
5. Update A to B to cost 0. The route to C should now cost 3. Negative costs and nonexistent destination IDs should be rejected.
6. Close B. A to C should now use the direct route at cost 20. Closed schools should not appear as transfer destinations.
7. Open B again, then delete it. Confirm it is gone and its incoming/outgoing costs are removed. Opening the delete page alone should not delete it.
8. Sign out and check that protected pages require login again.
9. Enter the actual results, date, and time in README.md.

Costs are directed: A to B does not automatically create B to A. A route's cost is the sum of its saved edges.

## Docker

```powershell
docker build -t district-schools .
docker volume create schools-data
docker run --rm -p 5000:5000 -e SECRET_KEY="replace-with-a-long-random-secret" -v schools-data:/app/instance district-schools
```

Open http://localhost:5000. The volume keeps school data between container runs. The Dockerfile is included, but the image still needs to be built and tested on a computer with Docker.

## GitHub and submission

Use your own fork/repository, not the instructor's repository. This copy includes `main`, `dev`, and `feature/complete-app` branches with the implementation merged into main.

Protect `main` under your GitHub repository's Settings → Rules → Rulesets (or Branches, depending on the interface). Complete the instructor checkpoint and team evaluations. Add all teammate names to Python, HTML, CSS, Dockerfile, and UML source headers before your final submission.

After your final edits:

```powershell
git add .
git commit -m "final submission"
git push origin main dev
git bundle create project-1.bundle --all
git bundle verify project-1.bundle
```

The team representative submits the `.bundle`; other teammates submit their completed README.md as instructed. To open the included bundle in a new folder:

```powershell
git clone project-1.bundle project-1
```
