class Elevator:
    def __init__(self, min_floor=1, max_floor=10):
        # __Atributos del ascensor__
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.current_floor = min_floor
        self.direction = None                       # 'up', 'down', or None
        self.requests = []                          # Lista de pisos solicitados
        self.is_moving = False                      # Indica si el ascensor está en movimiento
        self.door_open = False                      # Indica si la puerta está abierta
        self.door_open_time = 0                     # Tiempo desde que la puerta está abierta
        self.door_close_time = 0                    # Tiempo desde que la puerta está cerrada
        self.door_open_duration = 5                 # Duración de la apertura de la puerta
        self.door_close_duration = 3                # Duración del cierre de la puerta
        self.velocity = 1                           # Velocidad del ascensor (pisos por segundo)

    def request_floor(self, floor: int):
        """
        Añade una petición de piso (desde fuera o dentro).
        """
        if self.min_floor <= floor <= self.max_floor: # Primero verifica que floor esté entre min_floor y max_floor (inclusive).
            if floor not in self.requests:            # Comprueba si ya teníamos esa misma planta en la lista self.requests. Si ya existe, no la vuelve a añadir, pero sí devuelve True (la petición es “válida”, solo que ya estaba).
                self.requests.append(floor)
                self.requests.sort()
            return True
        return False