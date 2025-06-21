from models.elevator import Elevator
from controller.cli import ElevatorCLI

if __name__ == "__main__":
    elev = Elevator()
    cli = ElevatorCLI(elev)
    cli.run()
