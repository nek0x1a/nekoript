"""
# 示例脚本
这是一个示例脚本。
"""

import typer
from rich.console import Console

CONSOLE = Console()
ECONSOLE = Console(stderr=True)

# 子脚本自己的 Typer 实例
app = typer.Typer(help="这是一个示例脚本")


# 使用子命令
# @app.command()
# def run(name: str = typer.Option("", "--name", "-n", help="输入名称")):
#     """特定子命令的入口函数"""
#     CONSOLE.print(f"Hello! [green]{name}[/green], from plugin!")


# 没有子命令
@app.callback(invoke_without_command=True)
def main(name: str = typer.Option("", "--name", "-n", help="输入名称")):
    """未包含子命令参数时的回调"""
    CONSOLE.print(f"Hello! [green]{name}[/green], from plugin!")
