from collections import deque


class Storage(deque):
    """First-in First-out storage of goods"""
    def is_empty(self):
        return not bool(len(self))


class Element:
    def get_type(self):
        return 'no type'


class GroundType(Element):
    def get_type(self):
        return 'ground'


class WaterType(Element):
    def get_type(self):
        return 'water'


class GroundWaterType(Element):
    def get_type(self):
        return 'water', 'ground'


class Point:
    """Building.

    Attributes:
        coordinate: Map coordinate of a building.
    """
    def __init__(self, coordinate):
        self.coordinate = coordinate

    def get_position(self):
        """Returns current positions """
        return self.coordinate


class StoragePoint(Point, Storage):
    """A building that can save goods for further delivering."""
    def __init__(self, coordinate: int = 0, cargoes=None):
        Point.__init__(self, coordinate)
        Storage.__init__(self, cargoes)


class WaterPoint(Point, WaterType):
    """On water building."""
    pass


class GroundPoint(Point, GroundType):
    """On ground building."""
    pass


class GroundWaterStorage(StoragePoint, GroundWaterType):
    """A storage between ground and water of goods."""
    pass


class GroundStorage(StoragePoint, GroundType):
    """Ground storage of goods."""
    pass


class Cargo:
    """A goods that must be delivered.

    Attributes:
         destination: A destination point of the good.
    """
    def __init__(self, destination: str):
        self.destination = {'A': WaterPoint(5), 'B': GroundPoint(5)}[destination]


class Transport:
    """Transport carrying goods.

    Attributes:
        position: Current position on map.
        steps_til_point: Number of steps to point.
        destination_point: Where transport is going to
        loaded_cargo: Type of goods loaded on transport
    """
    def __init__(self, start_position: int):
        self.position = start_position
        self.steps_til_point = 0
        self.destination_point = None
        self.loaded_cargo = None

    def drive(self, destination: Point, cargo: Cargo = None):
        """Move transport to the destination point"""
        self.loaded_cargo = cargo
        self.destination_point = destination

        self.steps_til_point = abs(self.position - self.destination_point.get_position())
        self.position = self.destination_point.get_position()

    def make_step(self):
        """Make on step into the time, if transport arrive to point - unload"""
        if self.steps_til_point:
            self.steps_til_point -= 1
        if self.loaded_cargo and not self.steps_til_point:
            self.unload()

            self.loaded_cargo = None

    def unload(self):
        """Load cargo to new point"""
        if self.loaded_cargo.destination != self.destination_point:
            self.destination_point.append(self.loaded_cargo)

    def busy(self):
        """Сhecks if the transport is in transit"""
        return bool(self.steps_til_point) or bool(self.loaded_cargo)


class Trucks(Transport, GroundType):
    """Ground transportation"""
    pass


class Ships(Transport, WaterType):
    """Water transportation"""
    pass


def delivery(main_point: StoragePoint, transport):
    if main_point.is_empty() or transport.busy():
        return
    if transport.position != main_point.get_position():
        transport.drive(main_point)
        return
    cargo = main_point.popleft()
    point = cargo.destination
    if transport.get_type() not in cargo.destination.get_type():
        point = port
    transport.drive(point, cargo)


if __name__ == '__main__':
    factory, port = GroundStorage(0, map(Cargo, input())), GroundWaterStorage(1, [])
    # warehouse_a, warehouse_b = WaterPoint(5), GroundPoint(5)
    truck_1, truck_2 = Trucks(factory.get_position()), Trucks(factory.get_position())
    ship = Ships(port.get_position())
    count_steps = 0
    while any((truck_1.busy(), truck_2.busy(), ship.busy(), not factory.is_empty(), not port.is_empty())):
        delivery(factory, truck_1)
        delivery(factory, truck_2)
        delivery(port, ship)
        for transport in (truck_1, truck_2, ship):
            transport.make_step()
        count_steps += 1
    print(count_steps)
