# AI Factory Swarm — pilot target

Public pilot for [AI Factory Swarm](https://github.com/martins-vds/ai-factory-swarm): a high-fidelity
rewrite of [Eclipse Cargo Tracker](https://github.com/eclipse-ee4j/cargotracker) (Java EE 7, branch
`javaee7`, MIT) into Python/Django on PostgreSQL, driven by the harness's role agents.

Migration state lives in `.migration/`; decisions in `docs/adr/` and on the decision-map issue.

## Django target

The empty target project is in `src/cargotracker`, with `manage.py` at the repository root. It
targets Python 3.13 and PostgreSQL 17. Install the pinned application and development dependencies
with `python -m pip install -r requirements-dev.txt`.

Configure PostgreSQL with `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, and
`POSTGRES_PORT`; defaults are `cargotracker`, `cargotracker`, an empty password, `localhost`, and
`5432`. Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` for the deployment
environment.

Tailwind uses the standalone CLI and does not require Node.js: run `make tailwind-install`, then
`make tailwind-build` (or `make tailwind-watch` during development). The base template includes
htmx, and `django-htmx` middleware exposes htmx request metadata to Django.
