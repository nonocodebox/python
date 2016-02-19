import sys
import Queue

ATM_COUNT = 4  # How many atms
ATM_AVAILABLE = -1  # indicates the atm is available
NOT_FOUND = -2


class Person:

    def __init__(self, person_id, arrival, service_time):
        self.person_id = person_id
        self.arrival = arrival
        self.service_time = service_time
        self.used_atm_index = -1

    def get_id(self):
        return self.person_id

    def get_arrival(self):
        return self.arrival

    def get_service_time(self):
        return self.service_time

    def get_atm_index(self):
        return self.used_atm_index

    def set_atm_index(self, index):
        self.used_atm_index = index


class Event:

    def __init__(self, person, event_type, time):
        self.person = person
        self.event_type = event_type
        self.time_event_happens = time

    def get_person(self):
        return self.person

    def get_type(self):
        return self.event_type

    def get_time(self):
        return self.time_event_happens

    def __cmp__(self, other):
        if self.time_event_happens < other.time_event_happens:
            return -1
        elif self.time_event_happens > other.time_event_happens:
            return 1

        if self.get_type() == 'A' and other.get_type() == 'D':
            return -1
        elif self.get_type() == 'D' and other.get_type() == 'A':
            return 1

        return self.get_person().get_id() - other.get_person().get_id()

    def __str__(self):
        res = "Time %d: person %d " % (self.get_time(),
                                       self.get_person().get_id())

        if self.get_type() == 'A':
            res += "arrived."

        else:
            res += "departed from ATM %d." % self.get_person().get_atm_index()

        return res


def read_file_events_and_update(file_name, event_queue):

    file = open(file_name, 'r')
    line = file.readline()
    # Read first line - mode
    mode = int(line.split()[1])
    # The total number of persons
    person_count = 0

    line = file.readline()
    while line:
        # Each line contains a person's data
        split_values = line.split()
        person = Person(int(split_values[0]), int(split_values[1]),
                        int(split_values[2]))
        # Create an arrival event of the current person
        event_queue.put(Event(person, 'A', person.get_arrival()))
        person_count += 1

        line = file.readline()
    return mode, person_count


def find_atm_available(atm_machines):
    # Loops over the atms and find available
    for i in xrange(0, len(atm_machines)):
        if atm_machines[i] == ATM_AVAILABLE:
            return i
    return NOT_FOUND


def find_minimal_line(line_queues):
    # Define a function to get the line size
    def get_line_size(index):
        return line_queues[index].qsize()

    # Return the index of the queue with the minimal size
    return min(range(0, len(line_queues)), key=get_line_size)


def leave_atm(atm_machines, person):
    # Find the person's ATM index
    atm_index = person.get_atm_index()

    # Free the ATM previously used by this person
    atm_machines[atm_index] = ATM_AVAILABLE
    return atm_index


def join_atm(event_queue, atm_machines, atm_index, person, join_time):
    # Set the ATM to be used by this person
    atm_machines[atm_index] = person.get_id()

    # Set the person's ATM index
    person.set_atm_index(atm_index)

    # Create a departure event for this person
    new_event_time = join_time + person.get_service_time()
    event_queue.put(Event(person, 'D', new_event_time))

def run_atm_simulation(event_queue, queue_count):
    # Initialize the line queue and ATM list
    atm_machines = []
    line_queues = []

    # Clear the waiting time
    total_wait = 0

    for i in xrange(0, ATM_COUNT):
        # No one is using any of the ATMs
        atm_machines.append(ATM_AVAILABLE)

    for i in xrange(0, queue_count):
        # Initialize this ATM's line queue
        line_queues.append(Queue.Queue())

    # Loop until there are no more events
    while not event_queue.empty():
        cur_event = event_queue.get()
        cur_person = cur_event.get_person()

        # Check the event type
        if cur_event.get_type() == 'A':   # Arrival event
            # Try to find an available ATM
            place_atm = find_atm_available(atm_machines)
            if place_atm != NOT_FOUND:
                # This person can use the available ATM
                join_atm(event_queue, atm_machines, place_atm, cur_person,
                         cur_event.get_time())
            else:
                # No ATMs available, put the person in the shortest line queue
                line_queues[find_minimal_line(line_queues)].put(cur_person)

        else:  # 'D' Departure event
            # This person will now depart the ATM
            place_atm = leave_atm(atm_machines, cur_person)

            # Make sure the index is smaller than queue_cout
            queue_index = place_atm % queue_count
            
            # Check if there are more persons in the current line
            # (index will never be greater than the number of lines)
            if not line_queues[queue_index].empty():
                # Get the next person
                next_person = line_queues[queue_index].get()

                # Next person in this line can now join this ATM
                join_atm(event_queue, atm_machines, place_atm, next_person,
                         cur_event.get_time())

            # Calculate the waiting time
            total_wait += cur_event.get_time() - cur_person.get_arrival()

        # Print this event
        print cur_event

    return total_wait

def main():
    # Create the event queue
    event_queue = Queue.PriorityQueue(0)

    # Read the mode and persons from the file
    mode, person_count = read_file_events_and_update(sys.argv[1], event_queue)

    # Run the simulation according to the mode
    if mode == 1 or mode == 4:
        total_wait = run_atm_simulation(event_queue, mode)
    else:
        print "ERROR: Parsing file."
        return 1

    # Calculate the average waiting time
    average = 0

    if person_count > 0:
        average = float(total_wait) / float(person_count)

    # Use this line to print the average. Do not modify it, except perhaps
    # to replacing the variable "average" to suit your code.

    print "Average waiting time: %.3f" % average
    return 0

if __name__ == "__main__":
    main()
