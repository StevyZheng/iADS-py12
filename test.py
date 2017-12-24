# coding = utf-8

import click


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()
    

def log_all_info(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    ctx.exit()


@click.command()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.option('--log_all_info', is_flag=True, callback=log_all_info,
              expose_value=False, is_eager=True)
@click.option('--name', default='Ethan', help='name')
def hello(name):
    click.echo('Hello %s!' % name)
if __name__ == '__main__':
    hello()
