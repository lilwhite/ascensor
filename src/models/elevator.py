class Elevator:
    def __init__(self, min_floor=1, max_floor=10, weight_capacity=1600):
        # __Atributos del ascensor__
        self.min_floor = min_floor                  # Piso mínimo del ascensor
        self.max_floor = max_floor                  # Piso máximo del ascensor
        self.current_floor = min_floor              # Piso actual del ascensor
        self.current_weight = 0                     # Peso actual en el ascensor
        self.weight_capacity = weight_capacity      # Capacidad máxima de peso del ascensor
        self.direction = None                       # 'up', 'down', or None
        self.requests = []                          # Lista de pisos solicitados
        self.is_moving = False                      # Indica si el ascensor está en movimiento
        self.door_open = False                      # Indica si la puerta está abierta
        self.door_open_time = 0                     # Contador de tiempo para la puerta abierta
        self.door_close_time = 0                    # Contador de tiempo para la puerta cerrada
        self.door_open_duration = 5                 # Duración de la apertura de la puerta
        self.door_close_duration = 3                # Duración del cierre de la puerta
        self.velocity = 1.0                         # Velocidad del ascensor (m/s)

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
    
    def go_to(self, floor: bool):
        """
        Añade una petición interna de ir a `floor`.
        Delegamos en request_floor para validación y encolado.
        """
        return self.request_floor(floor)

    def update_direction(self):
        """
        Decide el valor de self.direction en función de self.requests:
          - 'up' si el siguiente destino > current_floor
          - 'down' si el siguiente destino < current_floor
          - None si no hay peticiones (o ya estamos en la planta solicitada)
        """
        if not self.requests:
            # Sin peticiones → reposo
            self.direction = None
            return

        target = self.requests[0]
        if target > self.current_floor:
            self.direction = 'up'
        elif target < self.current_floor:
            self.direction = 'down'
        else:
            # target == current_floor → ya llegamos
            self.direction = None

    def open_door(self):
        """
        Abre la puerta del ascensor.
        """
        if not self.door_open and not self.is_moving:
            self.door_open = True
            self.door_open_duration
            print(f"Abriendo puertas en el piso {self.current_floor}.")

    def close_door(self):
        """
        Cierra la puerta del ascensor.
        """
        if self.door_open and self.load_weight:
            self.door_open = False
            self.door_close_duration
            print(f"Cerrando puertas en el piso {self.current_floor}.")

    def load_weight(self, weight: float) -> bool:
        """
        Carga un peso en el ascensor; devuelve True si se pudo cargar, False si se excede la capacidad.
        """
        if self.current_weight + weight <= self.weight_capacity:
            self.current_weight += weight
            print(f"Peso cargado: {weight} kg. Peso actual: {self.current_weight} kg.")
            return True
        else:
            print("Capacidad excedida")
            return False
        
    def unload_weight(self, weight: float) -> bool:
        """
        Descarga un peso del ascensor; devuelve True si se pudo descargar, False si el peso es mayor al actual.
        """
        self.current_weight = max(0, self.current_weight - weight)

    def move(self, delta_time: float):
        """
        Avanza la simulación delta_time segundos.
        Gestiona puertas y movimiento.
        """
        # 1) Si las puertas están abiertas, contabiliza tiempo de apertura
        if self.door_open:
            self.door_open_time += delta_time
            if self.door_open_time >= self.door_open_duration:
                self.close_doors()
            return

        # 2) Si las puertas se están cerrando
        if not self.door_open and self.door_close_time < self.door_close_duration:
            self.door_close_time += delta_time
            if self.door_close_time >= self.door_close_duration:
                self.is_moving = True
            return

        # 3) Si no se está moviendo y hay peticiones, calculamos dirección
        if not self.is_moving:
            self.update_direction()
            if self.direction:
                self.is_moving = True

        # 4) Movimiento real
        if self.is_moving:
            distance = self.velocity * delta_time    # metros recorridos
            floors_moved = distance / 3.0             # asumiendo 3 m/piso

            if self.direction == 'up':
                self.current_floor += floors_moved
            elif self.direction == 'down':
                self.current_floor -= floors_moved

            # comprobar si hemos llegado o pasado el siguiente piso solicitado
            if self.requests:
                target = self.requests[0]
                arrived = (
                    (self.direction == 'up' and self.current_floor >= target) or
                    (self.direction == 'down' and self.current_floor <= target)
                )
                if arrived:
                    self.current_floor = target
                    self.is_moving = False
                    self.requests.pop(0)
                    self.open_doors()

    def update(self, delta_time: float = 1.0):
        """
        Llamar cada delta_time segundos para simular.
        """
        self.move(delta_time)

    def status(self) -> str:
        return (f"Piso: {self.current_floor:.1f}, Peso: {self.current_weight}kg, "
                f"Puerta {'abierta' if self.door_open else 'cerrada'}, "
                f"Moviendo: {self.is_moving}, Dirección: {self.direction}, "
                f"Solicitudes: {self.requests}")
