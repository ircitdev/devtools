---
description: Создание новой CLI команды (Typer)
---

Создай новую CLI команду используя Typer.

Включи:
- Typer app и команда
- Arguments и Options с типами
- Help text и descriptions
- Default values
- Validation
- Rich для красивого вывода
- Progress bar для длительных операций
- Обработка ошибок
- Примеры использования

Пример структуры:
```python
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def my_command(
    name: str = typer.Argument(..., help="Name"),
    verbose: bool = typer.Option(False, "--verbose", "-v")
):
    \"\"\"Command description\"\"\"
    if verbose:
        console.print(f"Processing {name}...", style="bold green")
```
