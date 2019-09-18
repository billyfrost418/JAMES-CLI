import click
import json
import requests as req
import sys


def print_json(obj):
    parsed = json.loads(obj.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))


@click.group()
@click.argument('Address', type=str)
@click.argument('Port', type=str)
@click.pass_context
def main(ctx, address, port):
    path = "http://" + address + ":" + port
    ctx.obj = {
        'path': path
    }


@main.command()
@click.pass_context
def get_all_domains(ctx):
    """List all domains"""
    res = req.get(ctx.obj['path'] + "/domains")
    print_json(res)


@main.command()
@click.pass_context
@click.argument('domain_name', type=str)
def add_domain(ctx, domain_name):
    """Add a domain to the domain list"""
    res = req.put(ctx.obj['path'] + "/domains/" + domain_name)

    if res.status_code == 204:
        print("%s has been added." % domain_name)
    elif res.status_code == 400:
        print("Invalid request for domain creation.")
    else:
        print("Internal server error!")


@main.command()
@click.pass_context
@click.argument('domain_name', type=str)
def delete_domain(ctx, domain_name):
    """Delete a domain from the domain list"""
    res = req.delete(ctx.obj['path'] + "/domains/" + domain_name)

    if res.status_code == 204:
        print("%s has been removed." % domain_name)
    elif res.status_code == 500:
        print("Internal server error!")


if __name__ == "__main__":
    main()
