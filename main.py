import click
from readsettings import ReadSettings
from cli.helper import login_required, safe_load_texts
from cli.config import CONFIG_FILEPATH
from cli.core import get_node_info, test_host, get_node_about, show_host
from cli.wallet import get_wallet_info
from cli.node import create_node
from cli.user import register_user, login_user, logout_user

config = ReadSettings(CONFIG_FILEPATH)
TEXTS = safe_load_texts()


@click.group()
def cli():
    pass


@cli.command('setHost', help="Set SKALE node endpoint")
@click.argument('host')
@click.option('--skip-check', is_flag=True)
def set_host(host, skip_check):
    if test_host(host) or skip_check:
        config['host'] = host
        print(f'SKALE host: {host}')
    else:
        print(TEXTS['service']['node_host_not_valid'])


@cli.command('host', help="Get SKALE node endpoint")
def host():
    show_host(config)


@cli.group('node', help="SKALE node commands")
def node():
    pass


@cli.group('user', help="SKALE node user commands")
def user():
    pass


@user.command('register', help="Create new user for SKALE node")
@click.option(
    '--username', '-u',
    prompt="Enter username",
    help='SKALE node username'
)
@click.option(
    '--password', '-p',
    prompt="Enter password",
    help='SKALE node password',
    hide_input=True
)
@click.option(
    '--token', '-t',
    prompt="Enter one-time token",
    help='One-time token',
    hide_input=True
)
def register(username, password, token):
    register_user(config, username, password, token)


@user.command('login', help="Login user in a SKALE node")
@click.option(
    '--username', '-u',
    prompt="Enter username",
    help='SKALE node username'
)
@click.option(
    '--password', '-p',
    prompt="Enter password",
    help='SKALE node password',
    hide_input=True
)
def login(username, password):
    login_user(config, username, password)

@user.command('logout', help="Logout from SKALE node")
def logout():
    logout_user(config)


@node.command('info', help="Get info about SKALE node")
@click.option('--format', '-f', type=click.Choice(['json', 'text']))
@login_required
def node_info(format):
    get_node_info(config, format)


@node.command('about', help="Get service info about SKALE node")
@click.option('--format', '-f', type=click.Choice(['json', 'text']))
@login_required
def node_about(format):
    get_node_about(config, format)


@node.command('register', help="Register current node in the SKALE Manager")
@click.option(
    '--name', '-n',
    prompt="Enter node name",
    help='SKALE node name'
)
@click.option(
    '--p2p-ip',
    prompt="Enter node p2p IP",
    help='p2p IP for communication between nodes'
)
@click.option(
    '--public-ip',
    prompt="Enter node public IP",
    help='Public IP for RPC connections'
)
@click.option(
    '--port', '-p',
    prompt="Enter node base port",
    help='Base port for node sChains'
)
@login_required
def register_node(name, p2p_ip, public_ip, port):
    create_node(config, name, p2p_ip, public_ip, port)


@cli.group('wallet', help="Node wallet commands")
def wallet():
    pass


@wallet.command('info', help="Get info about SKALE node wallet")
@click.option('--format', '-f', type=click.Choice(['json', 'text']))
@login_required
def wallet_info(format):
    get_wallet_info(config, format)


if __name__ == '__main__':
    cli()
