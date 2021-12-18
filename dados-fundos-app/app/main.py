import click
from itertools import product
from app.dados_fundos import *

@click.group()
def cli():
    pass

@cli.command("import_daily")
@click.argument("year")
@click.argument("month")
def cmd_import_daily(year, month):
    download_diario_file(year, month)
    load_file_info_diario(year, month)


@cli.command("import_all")
def cmd_import_all():
    years = ["2021", "2020"]
    months = ["01", "02", "03", "04", "05", "06", "08", "09", "10", "11", "12"]
    for year, month in list(product(years, months)):
        download_diario_file(year, month)
        load_file_info_diario(year, month)

@cli.command("import_cadastro")
def cmd_import_cadastro():
    download_cadastro()

@cli.command("convert_db")
def cmd_convert_db():
    convert_files_to_structure_db()


if __name__ == "__main__":
    cli()
