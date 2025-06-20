import pytest
from elevator import Elevator

def test_request_floor_valid():
    e = Elevator(min_floor=1, max_floor=5)
    assert e.request_floor(3) is True
    assert 3 in e.requests

def test_request_floor_invalid():
    e = Elevator(min_floor=1, max_floor=3)
    assert e.request_floor(0) is False
    assert e.request_floor(4) is False

def test_request_floor_duplicates():
    e = Elevator()
    assert e.request_floor(2) is True
    before = list(e.requests)
    assert e.request_floor(2) is True  # válida pero no añade
    assert e.requests == before

def test_go_to_delegates_request_floor():
    e = Elevator()
    assert e.go_to(4) is True
    assert 4 in e.requests

def test_update_direction_no_requests():
    e = Elevator()
    e.requests = []
    e.current_floor = 2
    e.update_direction()
    assert e.direction is None

def test_update_direction_up():
    e = Elevator()
    e.requests = [5]
    e.current_floor = 2
    e.update_direction()
    assert e.direction == 'up'

def test_update_direction_down():
    e = Elevator()
    e.requests = [1]
    e.current_floor = 3
    e.update_direction()
    assert e.direction == 'down'

def test_load_weight_within_capacity():
    e = Elevator(weight_capacity=100)
    assert e.load_weight(50) is True
    assert e.current_weight == 50

def test_load_weight_exceeds_capacity(capsys):
    e = Elevator(weight_capacity=100)
    assert e.load_weight(150) is False
    out = capsys.readouterr().out
    assert "Capacidad excedida" in out

def test_unload_weight_not_negative():
    e = Elevator()
    e.current_weight = 30
    e.unload_weight(50)
    assert e.current_weight == 0

def test_open_and_close_door_manually(capsys):
    e = Elevator()
    e.is_moving = False
    e.door_open = False

    e.open_door()
    assert e.door_open is True
    out = capsys.readouterr().out
    assert f"Abriendo puertas en el piso {e.current_floor}" in out

    # As close_door solo comprueba door_open y load_weight (método), basta con llamarlo
    e.close_door()
    assert e.door_open is False
    out = capsys.readouterr().out
    assert f"Cerrando puertas en el piso {e.current_floor}" in out

def test_move_opens_door_at_destination():
    e = Elevator(min_floor=1, max_floor=5)
    e.go_to(3)
    # velocidad 1 m/s → 3 plantas ≈ 9 m → necesitamos ≥6 s para 2 plantas y algo más
    e.move(6.1)
    assert pytest.approx(e.current_floor, rel=1e-2) == 3.0
    assert e.door_open is True

def test_status_contains_all_fields():
    e = Elevator()
    s = e.status()
    assert "Piso:" in s
    assert "Peso:" in s
    assert "Puerta" in s
    assert "Moviendo" in s
    assert "Dirección" in s
    assert "Solicitudes" in s
