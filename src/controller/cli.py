# controller/cli.py
import time
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.live import Live
from rich import box

class ElevatorCLI:
    def __init__(self, elevator):
        self.elevator = elevator
        self.console = Console()

    def render_panel(self, floor, symbol):
        title = Text()
        title.append(f"{symbol}\n", style="bold gold1")
        title.append(f"{floor}\n", style="bold gold1 underline")
        title.append(f"{self.elevator.weight_capacity} Kg MAX", style="bold")

        return Panel(
            Align.center(title, vertical="middle"),
            title="Ascensor",
            title_align="left",
            width=30,
            border_style="gold3",
            box=box.DOUBLE,
        )

    def animate_movement(self, target):
        current = self.elevator.current_floor
        step = 1 if target > current else -1
        anim = ["↑", "⇡", "⇧", "↑"] if step == 1 else ["↓", "⇣", "⇩", "↓"]

        with Live(self.render_panel(current, anim[0]), refresh_per_second=4) as live:
            for floor in range(current + step, target + step, step):
                for symbol in anim:
                    live.update(self.render_panel(floor - step, symbol))
                    time.sleep(0.1)
                self.elevator.current_floor = floor  # actualiza estado
                live.update(self.render_panel(floor, anim[0]))
                time.sleep(0.2)

    def run(self):
        while True:
            self.console.print("\n[bold green]¿A qué piso quieres ir? (q para salir):[/]")
            user_input = input("> ").strip()
            if user_input.lower() == "q":
                break
            if not user_input.isdigit():
                self.console.print("[red]Entrada no válida.[/]")
                continue

            target = int(user_input)
            if not self.elevator.min_floor <= target <= self.elevator.max_floor:
                self.console.print("[red]Piso fuera de rango.[/]")
                continue

            self.animate_movement(target)
            self.console.print(f"[bold cyan]Llegamos al piso {target}[/]")