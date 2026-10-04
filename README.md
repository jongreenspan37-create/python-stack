# Python Stack

> **This is a learning project.** It runs on Python's built-in `http.server`,
> which is not a production server, and it is not suitable for deployment as a
> live web application.

It shows how to build a web app from first principles, without a framework:

- **Front end:** HTML, CSS, Tailwind CSS and plain JavaScript
- **Back end:** plain Python, standard library only, plus `psycopg2` for the
  database
- **Database:** PostgreSQL 16
- **API:** endpoints that receive and return **JSON in the HTTP body**, called
  from the browser with `fetch()`

It has a sister project, [php-stack](https://github.com/jongreenspan37-create/php-stack),
which builds the same app with PHP and MySQL. **Many of the front-end files are
identical in the two projects on purpose.** The browser code doesn't know or
care which language is behind the API, as long as the JSON responses match.

## Running it

Everything runs in Docker, so Python packages and PostgreSQL don't need to be
installed locally.

```bash
cp .env.example .env        # then change the password in .env
docker compose up -d --build
```

Open <http://localhost> (port 80). On the **Database Interaction** page, click
**Create Tables** once to create the `roles` and `users` tables. On the
**Formula 1** page, click **Create F1 Tables** to load the F1 data from the CSV
files.

Edits to HTML, CSS and JS files take effect on the next page load. **Edits to
`.py` files need a restart** (`docker restart python-app`), because the server
loads the Python code once, at startup.

## How it works

```
browser ──fetch()──► /api/run/<file>/<function> ──► app.py ──► router.py ──► scripts/<file>.py
        ◄── JSON ─────────────────────────────────────────────── returns a dict or list
```

- `app/www/app.py` is the web server, built on `http.server`. Requests that
  don't start with `/api/run/` are served as static files, with a path
  traversal check.
- `router.py` maps each API name to a function in an explicit `ROUTES` dict.
  Only functions listed there can be reached.
- `app.py` decodes the JSON request body, calls the function and sends its
  return value back with `json.dumps`. Errors become JSON error responses.
- Database access uses psycopg2 with `%s` placeholders, so user input never
  becomes part of the SQL.

## Pages

| Page | Shows |
|---|---|
| `index.html` | Numbers, strings, string functions and date arithmetic through the API |
| `list-manipulation.html` | Reading a CSV and displaying it as a list and a table; counting and transforming items |
| `database-interaction.html` | Full CRUD for roles and users (a foreign key and a JOIN) |
| `formula1.html` | F1 driver tables built in the browser from JSON, using both `async/await` and `.then()` |
| `f1tables.html` | Pick a practice SQL query from a dropdown and see its results as a table |

## Layout

```
app/
  Dockerfile
  requirements.txt
  www/
    app.py            web server (static files + /api/run/)
    router.py         API route table
    connection.py     PostgreSQL connection, settings read from .env
    scripts/          API functions, CSV data, F1 schema and queries,
                      plus standalone Python practice scripts
    *.html, script.js, style.css
frontend/             an unused Vite + React starter, kept for later
docker-compose.yml    the Python app and PostgreSQL containers
```
