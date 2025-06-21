# Sistema de comandos para ascensor

---

## 1. Visión general

- **Objetivo:** Facilitar la práctica de conceptos básicos de Python aplicados a un sistema de control.  
- **Alcance:** Recepción de llamadas, planificación simple (FCFS), control de posición y puertas, interfaz de línea de comandos.

---

## 2. Organización de carpetas

```yaml
ascensor/
├── docs/ # Guía de usuario y documentación básica
├── src/ # Código fuente
│ ├── models/ # Clases de dominio (Elevator, Request, Floor)
│ ├── controller/ # Estado y acciones del ascensor
│ ├── scheduler/ # Planificador sencillo (First-Come, First-Served)
│ ├── cli.py # Script principal de línea de comandos
│ └── utils.py # Funciones auxiliares (logging, validación)
├── tests/ # Pruebas unitarias con pytest
├── requirements.txt # Dependencias (p. ej. pytest)
├── README.md # Cómo instalar y ejecutar
└── .gitignore # Archivos a ignorar en Git
```

---

## 3. Módulos principales

### 3.1 models/

- `Elevator`: atributos como piso actual y estado de puertas.  
- `Request`: origen, destino y dirección.  
- `Floor`: número y botones de llamada.

### 3.2 controller/

- Gestiona el estado interno del ascensor.  
- Métodos: `move_to_floor()`, `open_doors()`, `close_doors()`.

### 3.3 scheduler/

- Implementa FCFS: atiende peticiones en orden de llegada.  
- Función: `get_next_request(request_queue)`.

### 3.4 cli.py

- Uso de `argparse` para comandos simples:  
  - `call <floor>`: llamar al ascensor.  
  - `go <floor>`: seleccionar un piso dentro.  
  - `status`: mostrar estado actual.

### 3.5 utils.py

- Funciones de ayuda: validación de piso, formateo de salidas, logging básico.

### 3.6 tests/

- Pruebas unitarias para cada módulo.  
- Ejemplo con pytest:
  ```python
  def test_move_elevator():
      e = Elevator()
      e.move_to_floor(3)
      assert e.current_floor == 3


## 4. 🧭 Flujo de trabajo detallado

1. **Inicialización del ascensor**  
   Se crea una instancia de la clase `Elevator`, que contiene la lógica principal: piso actual, capacidad de carga, dirección, puertas, etc.

2. **Ejecución del controlador CLI**  
   La clase `ElevatorCLI` gestiona la interacción con el usuario a través de la terminal. Utiliza la librería `rich` para mostrar el estado del ascensor de forma visual y estilizada.

3. **Entrada del usuario**  
   El usuario introduce el piso de destino por consola. También puede salir del programa escribiendo `q`.

4. **Validación de entrada**  
   El controlador comprueba si el piso introducido está dentro del rango permitido (`min_floor`, `max_floor`) y si es un número válido.

5. **Simulación de movimiento**  
   Si el piso es válido, el controlador anima el desplazamiento del ascensor:
   - Se muestra una flecha animada (`↑`, `⇡`, `⇧` o `↓`, `⇣`, `⇩`) según la dirección.
   - El número de piso se actualiza dinámicamente durante el trayecto.
   - Se imprime un mensaje al llegar al destino.

6. **Actualización del estado interno**  
   El piso actual (`current_floor`) se actualiza en la instancia del ascensor una vez completado el movimiento.

7. **Repetición del ciclo**  
   El programa vuelve a solicitar entrada al usuario, repitiendo el flujo hasta que se indique salir.


