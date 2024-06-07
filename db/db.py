import os
import psycopg2
import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        db_url = current_app.config["DATABASE"]
        g.db = psycopg2.connect(db_url)
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    schema_file = os.path.join(current_app.root_path, "../db/schema.sql")
    with current_app.open_resource(schema_file) as f:
        schema = f.read().decode("utf8")
    with db.cursor() as cursor:
        cursor.execute(schema)
    db.commit()


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
