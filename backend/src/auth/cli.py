"""CLI commands for RBAC data management."""

import asyncio

import click

from src.database.connection import AsyncSessionLocal

from .data_management import export_roles_permissions, import_roles_permissions


@click.group()
def rbac():
    """RBAC data management commands."""
    pass


@rbac.command()
@click.option(
    "--output",
    "-o",
    default="rbac_data.json",
    help="Output file path",
    type=click.Path(),
)
def export(output: str):
    """Export roles and permissions to JSON file."""

    async def _export():
        async with AsyncSessionLocal() as session:
            await export_roles_permissions(session, output)

    asyncio.run(_export())
    click.echo(f"✅ Exported to {output}")


@rbac.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--clear",
    is_flag=True,
    help="Clear existing roles/permissions before import",
)
def import_data(input_file: str, clear: bool):
    """Import roles and permissions from JSON file."""

    async def _import():
        async with AsyncSessionLocal() as session:
            await import_roles_permissions(session, input_file, clear_existing=clear)

    asyncio.run(_import())
    click.echo(f"✅ Imported from {input_file}")


if __name__ == "__main__":
    rbac()
