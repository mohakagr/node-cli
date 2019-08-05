import click
from core.helper import login_required, get, download_log_file
from core.print_formatters import print_logs

from configs.cli_logger import LOG_FILEPATH, DEBUG_LOG_FILEPATH

@click.group()
def logs_cli():
    pass


@logs_cli.group(help="Logs commands")
def logs():
    pass


@logs.command(help="List of log files on connected node")
@login_required
def ls():
    logs = get('logs')
    if not logs:
        return
    print_logs(logs)


@logs.command(help="Download log file from connected node")
@click.argument('name')
@click.option('--schain', '-s', help='sChain log type')
@login_required
def download(name, schain):
    type = 'schain' if schain else 'base'
    res = download_log_file(name, type, schain)
    if res:
        print(f'File {res} downloaded')
    else:
        print('Something went wrong, couldn\'t download log file')


@logs.command(help="Fetch the logs of the node-cli")
@click.option('--debug', is_flag=True)
@login_required
def cli(debug):
    filepath = DEBUG_LOG_FILEPATH if debug else LOG_FILEPATH
    with open(filepath, 'r') as fin:
        print(fin.read())
