class Storage:
    """First-in First-out storage of goods.

    Attributes:
        storage: Stock of goods.
    """

    def __init__(self, iterable, *args, **kwargs):
        self.storage = list(iterable)
        super(Storage, self).__init__(*args, **kwargs)

    def is_empty(self):
        """Checks if stocks are empty"""
        return not bool(len(self.storage))

    def cargo_in(self, cargo):
        """Puts the goods in stock

        Args:
            cargo: Goods must be stocked.
        """
        self.storage.append(cargo)

    def cargo_out(self):
        """Issues an item from stocks"""
        return self.storage.pop(0)


class Point:
    """Building.

    Attributes:
        coordinate: Map coordinate of a building.
    """

    def __init__(self, coordinate, *args, **kwargs):
        self.coordinate = coordinate
        super(Point, self).__init__(*args, **kwargs)

    def get_position(self):
        """Returns current positions """
        return self.coordinate


class StoragePoint(Point, Storage):
    """A building that can save goods for further delivering."""

    def __init__(self, coordinate: int = 0, cargoes=None):
        super(StoragePoint, self).__init__(coordinate, cargoes)


class Warehouse(Point):
    """Simple building."""

    def __init__(self, name, *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"Warehouse{self.name}"


class Port(StoragePoint):
    """A storage between ground and water of goods."""

    def __str__(self):
        return f"Port"


class Factory(StoragePoint):
    """Ground storage of goods."""

    def __str__(self):
        return f"Factory"


class Cargo:
    """A goods that must be delivered.

    Attributes:
         destination: A destination point of the good.
    """

    def __init__(self, destination: Point):
        self.destination = destination


class Route:
    """Transport routes"""

    def __init__(self, road_to_a: Point, road_to_b: Point = None):
        self.route = {'A': road_to_a, 'B': road_to_b}

    def __add_new_road(self, name: str, point: Point):
        """Adds new road to routes"""
        self.route[name] = point


class Transport:
    """Transport carrying goods.

    Attributes:
        position: Current position on map.
        steps_til_point: Number of steps to point.
        destination_point: Where transport is going to
        loaded_cargo: Type of goods loaded on transport
        global_main_storage: 1st cargo input at the map
        local_storage:  Storage point where transport  pick ups cargoes
    """

    def __init__(self, start_position: StoragePoint, route: Route, global_main_storage: StoragePoint = None, ):
        if global_main_storage is None:
            global_main_storage = start_position
        self.route = route
        self.global_main_storage = global_main_storage
        self.local_storage = start_position

        self.position = start_position
        self.steps_til_point = 0
        self.destination_point = None
        self.loaded_cargo = None

    def drive(self, destination: Point, cargo: Cargo = None):
        """Move transport to the destination point.

        Args:
            destination: A point where need to drive to.
            cargo: Deliverable cargo.
        """
        self.loaded_cargo = cargo
        self.destination_point = destination

        self.steps_til_point = abs(self.position.get_position() - self.destination_point.get_position())
        self.position = self.destination_point

    def make_step(self):
        """Make on step into the time, if transport arrive to point - unload"""
        if self.steps_til_point:
            self.steps_til_point -= 1
        if self.loaded_cargo and not self.steps_til_point:
            self.unload()

    def unload(self):
        """Load cargo to new point."""

        if self.loaded_cargo.destination != self.destination_point:
            self.destination_point.cargo_in(self.loaded_cargo)
        self.loaded_cargo = None

    def busy(self):
        """Checks if the transport is in transit."""
        return bool(self.steps_til_point) or bool(self.loaded_cargo)

    def delivery(self):
        """The function sends the transport to the point

        The function checks stock balances and transport bossiness.
        After checking the current position, if the transport is not in
        the storage point send him to storage point back. Else transport pick up
        goods and  goes to the point  destination of the goods.
        """
        if (self.local_storage.is_empty() and self.global_main_storage.is_empty()) or self.busy():
            return
        if self.position.get_position() != self.local_storage.get_position():
            self.drive(self.local_storage)
            return
        if self.local_storage.is_empty():
            return
        cargo = self.local_storage.cargo_out()
        point = self.route.route[cargo.destination.name]
        self.drive(point, cargo)


class LoggingTransport(Transport):
    """Special class for logging the transport actions.

    Attributes:
        number: Each type of transport get his unique number.
    """

    def __init__(self, number, *args, **kwargs):
        self.number = number
        super().__init__(*args, **kwargs)

    def drive(self, destination: Point, cargo: Cargo = None):
        """Logger for transport drive to point."""
        if cargo:
            print(f'{self} took cargo in the {self.position}')
        else:
            print(f'{self} turned around to the {destination}')
        super().drive(destination, cargo)

    def make_step(self):
        """Logger for driving to point."""
        if self.steps_til_point:
            print(f'{self} went to the {self.destination_point}')
        super().make_step()

    def unload(self):
        """Logger for unload goods into point."""
        print(f'{self} unloaded  in the {self.destination_point}')
        super().unload()

    def __str__(self):
        return f"{self.__class__.__name__}{self.number}"


class Truck(LoggingTransport):
    """Ground transportation."""


class Ship(LoggingTransport):
    """Water transportation."""


def get_destination_point(destination: str) -> Point:
    """Function gives a house point for map symbol"""
    return {'A': warehouse_a, 'B': warehouse_b}[destination]


if __name__ == '__main__':
    warehouse_a, warehouse_b = Warehouse('A', 5), Warehouse('B', 5)

    factory, port = Factory(0, map(Cargo, map(get_destination_point, input()))), Port(1, [])
    track_route = Route(port, warehouse_b)
    ship_route = Route(warehouse_a)
    truck_1, truck_2 = Truck(1, factory, track_route), Truck(2, factory, track_route)

    ship1 = Ship(1, port, ship_route, factory)

    count_steps = 0
    while any((truck_1.busy(), truck_2.busy(), ship1.busy(), not factory.is_empty(), not port.is_empty())):
        print(f"Turn number {count_steps}\n")
        for transport in (truck_1, truck_2, ship1):
            transport.delivery()
        for transport in (truck_1, truck_2, ship1):
            transport.make_step()
        count_steps += 1
        print()

    print(f"Total time: {count_steps}")
