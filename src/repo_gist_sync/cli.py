import pathlib
import typing as t

import click
from . import GistSync


@click.command()
@click.option("-C", "--create", is_flag=True, help="Flag: Create GIST")
@click.option("-U", "--update", is_flag=True, help="Flag: Update GIST")
@click.option("-D", "--delete", is_flag=True, help="Flag: Delete GIST")
@click.option("-t", "--auth-token", help="GIST REST API token")
@click.option("-f", "--file-name", help="Absolute or relative file name path")
@click.option("-id", "--gist-id", default=None, help="GIST ID")
def run(
    create: bool, update: bool, delete: bool, auth_token: str, file_name: str, gist_id: str
) -> None:
    gist_api = GistSync(auth_token=auth_token)

    if create:
        response_data = gist_api.create_gist(file_name=file_name)

    elif update:
        if not gist_id:
            response_data = gist_api.update_gist(file_name=file_name)
        else:
            response_data = gist_api.update_gist(file_name=file_name, gist_id=gist_id)

    elif delete:
        if not gist_id:
            response_data = gist_api.delete_gist(file_name=file_name)
        else:
            response_data = gist_api.delete_gist(gist_id=gist_id)

    click.echo(str(response_data))

@click.command()
@click.option("-t", "--auth-token", help="GIST REST API token")
@click.option("-d", "--directory", help="Directory that contains Python scripts")
def dir_run(auth_token: str, directory: t.Union[pathlib.Path, str]) -> None:
    gist_api = GistSync(auth_token=auth_token)
    dir_path = pathlib.Path(directory)
    gists = gist_api.get_gists()

    gist_files_dictfiles = [list(gist_item["files"].keys()) for gist_item in gists]
    gist_files = [x for x in gist_files_dictfiles for x in x]

    for python_filepath in dir_path.rglob("*.py"):
        click.echo(python_filepath)
        python_filename = python_filepath.name
        if python_filename in gist_files:
            click.echo("UPDATE")
            _ = gist_api.update_gist(file_name=python_filepath)
        else:
            click.echo("CREATE")
            _ = gist_api.create_gist(file_name=python_filepath)

    click.echo("DONE")
