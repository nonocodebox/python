class Customer:

    def __init__(self, customer_id, start_floor, destination_floor):
        self.customer_id = customer_id
        self.start_floor = start_floor
        self.destination_floor = destination_floor
        self.current_floor = start_floor

    def get_start_floor(self):
        return self.start_floor

    def get_destination_floor(self):
        return self.destination_floor

    def set_current_floor(self, floor):
        self.current_floor = floor

    def get_current_floor(self):
        return self.current_floor

    def get_id(self):
        return self.customer_id

    def __hash__(self):
        return hash(self.get_id())


class Elevator:

    def __init__(self):
        self.current_floor = 1
        self.current_customers = set()
        # Start climbing up
        self.direction = 1

    def get_current_floor(self):
        return self.current_floor

    def move(self):
        self.current_floor += self.direction
        for customer in self.current_customers:
            customer.set_current_floor(self.current_floor)

    def add_customer(self, customer):
        self.current_customers.add(customer)

    def add_customers(self, customers):
        self.current_customers = self.current_customers.union(customers)

    def remove_customer(self, customer):
        #Remove element elem from the set if it is present.
        self.current_customers.discard(customer)

    def get_customers(self):
        return self.current_customers

    def remove_customers(self, removed_customers):
        self.current_customers.difference_update(removed_customers)

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction


class Building:

    def __init__(self, number_of_floors, customers):
        self.number_of_floors = number_of_floors
        self.served_customers = set()
        self.customers = customers
        self.elevator = Elevator()

    def get_number_of_floors(self):
        return self.number_of_floors

    def get_customers(self):
        return self.customers

    def get_customers_at(self, floor):
        by_floor_customers = set()
        for customer in self.customers:
            if customer.get_current_floor() == floor:
                by_floor_customers.add(customer)
        return by_floor_customers

    def get_customers_by_start(self, floor):
        by_floor_customers = set()
        for customer in self.customers:
            if customer.get_start_floor() == floor:
                by_floor_customers.add(customer)
        return by_floor_customers

    def get_customers_by_destination(self, floor):
        by_floor_customers = set()
        for customer in self.customers:
            if customer.get_destination_floor() == floor:
                by_floor_customers.add(customer)
        return by_floor_customers

    def get_customers_in_elevator(self):
        return self.elevator.get_customers()

    def get_served_customers(self):
        return self.served_customers

    def get_elevator_floor(self):
        return self.elevator.get_current_floor()

    def get_minimal_start_floor(self):
        minimal_floor = self.number_of_floors
        for customer in self.customers:
            if customer.get_start_floor() < minimal_floor:
                minimal_floor = customer.get_start_floor()
        return minimal_floor

    def get_minimal_destination_floor(self):
        minimal_floor = self.number_of_floors
        for customer in self.customers:
            if customer.get_destination_floor() < minimal_floor:
                minimal_floor = customer.get_destination_floor()
        return minimal_floor

    def get_maximal_destination_floor(self):
        maximal_floor = 1
        for customer in self.customers:
            if customer.get_destination_floor() > maximal_floor:
                maximal_floor = customer.get_destination_floor()
        return maximal_floor

    def get_maximal_start_floor(self):
        maximal_floor = 1
        for customer in self.customers:
            if customer.get_start_floor() > maximal_floor:
                maximal_floor = customer.get_start_floor()
        return maximal_floor

    def simple_algorithm_step(self):
        if self.is_finished():
            return

        if self.elevator.get_current_floor() == self.get_number_of_floors():
            self.elevator.set_direction(-1)

        added_customers = set()
        exit_customers = set()

        # Changes the current floor according to direction
        self.elevator.move()
        current_floor = self.elevator.get_current_floor()
        # Add all customers in current floor that haven't been served
        added_customers = self.get_customers_at(current_floor) \
            .difference(self.served_customers)

        self.elevator.add_customers(added_customers)
        # Delete all customers the current floor in their destination
        exit_customers = self.get_customers_by_destination(current_floor) \
            .intersection(self.elevator.get_customers())

        self.elevator.remove_customers(exit_customers)
        # Update served customers
        self.served_customers = self.served_customers.union(exit_customers)

    def improved_algorithm_step(self):
        if self.is_finished():
            return

        minimal = min([
            self.get_minimal_destination_floor(),
            self.get_minimal_start_floor()])
        maximal = max([
            self.get_maximal_destination_floor(),
            self.get_maximal_start_floor()])
        current_floor = self.elevator.get_current_floor()

        if current_floor == maximal:
            self.elevator.set_direction(-1)

        added_customers = set()
        exit_customers = set()

        # Changes the current floor according to direction
        self.elevator.move()

        current_floor = self.elevator.get_current_floor()

        # No passengers are coming down - so we can skip these floors
        if current_floor >= minimal:
            # Add all customers in current floor that haven't been served
            added_customers = self.get_customers_at(current_floor) \
                .difference(self.served_customers)
            self.elevator.add_customers(added_customers)
            # Delete all customers the current floor in their destination
            exit_customers = self.get_customers_by_destination(current_floor) \
                .intersection(self.elevator.get_customers())
            self.elevator.remove_customers(exit_customers)
            # Update served customers
            self.served_customers = self.served_customers.union(exit_customers)

    def is_finished(self):
        # in s1 or in s2 but not in both
        return not bool(
            self.served_customers.symmetric_difference(self.customers))
