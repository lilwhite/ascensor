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

## 4. Flujo de trabajo detallado

A continuación se describe paso a paso con ejemplos cómo empezar:

1. **Configurar el entorno de desarrollo**
   - Crear un entorno virtual en la raíz del proyecto:
     ```bash
     python -m venv venv
     source venv/bin/activate  # Linux/Mac
     venv\Scripts\activate     # Windows
     ```
   - Crear el archivo `requirements.txt` con las dependencias mínimas:
     ```txt
     pytest
     ```
   - Instalar dependencias:
     ```bash
     pip install -r requirements.txt
     ```

2. **Definir las clases en `src/models/`**
   - Crear `elevator.py`, `request.py` y `floor.py`.
   - Ejemplo en `elevator.py`:
     ```python
     class Elevator:
         def __init__(self, min_floor=1, max_floor=10):
             self.current_floor = 1
             self.doors_open = False
     ```
   - Añadir métodos básicos y documentar con docstrings.

3. **Implementar el controlador (`src/controller/`)**
   - Crear `controller.py` con funciones:
     ```python
     def move_to_floor(elevator, target_floor):
         # lógica sencilla: actualizar current_floor
         elevator.current_floor = target_floor
     ```
   - Agregar acciones de abrir/cerrar puertas:
     ```python
     def open_doors(elevator):
         elevator.doors_open = True
     ```

4. **Desarrollar el planificador FCFS (First-Come, First-Served) (`src/scheduler/`)**
   - En `scheduler.py`, mantener una cola de peticiones:
     ```python
     from collections import deque

     request_queue = deque()

     def add_request(request):
         request_queue.append(request)

     def get_next_request():
         return request_queue.popleft() if request_queue else None
     ```

5. **Crear la CLI con `argparse` (`src/cli.py`)**
   - Estructura básica:
     ```python
     import argparse
     from models.elevator import Elevator

     def main():
         parser = argparse.ArgumentParser()
         subparsers = parser.add_subparsers(dest='command')

         call = subparsers.add_parser('call')
         call.add_argument('floor', type=int)

         # añadir más subcomandos...

         args = parser.parse_args()
         # lógica para cada comando

     if __name__ == '__main__':
         main()
     ```

6. **Escribir y ejecutar pruebas (`tests/`)**
   - Crear archivos de prueba `test_elevator.py`, `test_scheduler.py`, etc.
   - Ejecutar:
     ```bash
     pytest --maxfail=1 --disable-warnings -q
     ```


