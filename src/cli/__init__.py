#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
# 脚本执行器模块
检测脚本并根据参数加载并执行脚本。
"""

from importlib.metadata import EntryPoint, entry_points
import sys

import typer
from rich.console import Console


cli = typer.Typer(help="Nekoript: 脚本库")
CONSOLE = Console()
ECONSOLE = Console(stderr=True)


def get_plugin_map() -> dict[str, EntryPoint]:
    """检测脚本并获取元数据"""
    return {ep.name: ep for ep in entry_points(group="nekoript.plugins")}


PLUGIN_MAP = get_plugin_map()


def setup_plugins():
    """注册脚本"""
    plugins = PLUGIN_MAP
    potential_cmd = None
    for arg in sys.argv[1:]:
        if not arg.startswith("-"):
            potential_cmd = arg
            break

    if potential_cmd in plugins:
        ep = plugins[potential_cmd]
        try:
            plugin_app = ep.load()
            cli.add_typer(plugin_app, name=ep.name)
        except Exception as e:
            ECONSOLE.print(
                f"[bold red]脚本 {potential_cmd} 加载失败: [/bold red][red]{e}[/red]"
            )


@cli.callback(invoke_without_command=True)
def main_options(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="显示版本号"),
):
    """未包含子命令参数时的回调"""
    if ctx.invoked_subcommand is None:
        plugins = PLUGIN_MAP
        CONSOLE.print(ctx.get_help())
        if plugins:
            CONSOLE.print(
                f"可用脚本:\n{'\n'.join([ep.name for ep in plugins.values()])}\n"
            )
        else:
            CONSOLE.print("[yellow]暂无可用脚本[/yellow]\n")


def cli_run():
    """CLI 入口函数"""
    setup_plugins()
    cli()


if __name__ == "__main__":
    cli_run()
