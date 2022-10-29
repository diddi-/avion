import click

from avion.api.app import setup_wsgi_app


@click.group()
def cli():
    pass


@cli.command()
def run():
    app = setup_wsgi_app()
    app.run_develop()


@cli.command()
def routes():
    app = setup_wsgi_app()
    for route in app.get_routes():
        click.echo(route)
