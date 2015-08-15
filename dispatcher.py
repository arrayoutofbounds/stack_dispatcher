# A1 for COMPSCI340/SOFTENG370 2015
# Prepared by Robert Sheehan
# Modified by Anmol Desai 

# You are not allowed to use any sleep calls.

from threading import Lock, Event
from process import State

class Dispatcher():
    """The dispatcher."""

    MAX_PROCESSES = 8
    
   
    def __init__(self):
        """Construct the dispatcher."""
        # create a list to simulate a stack

        self.top_of_stack = 0;

         # list of runnable processes
        self.runnable_processes = []

        # list of waiting for input procceses
        self.waiting_proccesses = []


    def set_io_sys(self, io_sys):
        """Set the io subsystem."""
        self.io_sys = io_sys

    def add_process(self, process):
        """Add and start the process."""
        # ...

        # put it on top of stack
        self.runnable_processes.append(process)


        #assign it to a window
        self.io_sys.allocate_window_to_process(process,self.top_of_stack)

        

        # increment the top of stack
        self.top_of_stack += 1

        process.event.set()
        # run the process
        process.start()

        # check if the top of stack is more than 0, then there is atleast 1 other process. If it is....iterate through and make rest of them wait. 
        # then the code below starts the new process
        if(self.top_of_stack > 2):
            for p in range( 0, len(self.runnable_processes) - 2):
                self.runnable_processes[p].event.clear()

    def dispatch_next_process(self):
        """Dispatch the process at the top of the stack."""
        # ...



    def to_top(self, process):
        """Move the process to the top of the stack."""
        # ...


    def pause_system(self):
        """Pause the currently running process.
        As long as the dispatcher doesn't dispatch another process this
        effectively pauses the system.
        """
        # ...

    def resume_system(self):
        """Resume running the system."""
        # ...

    def wait_until_finished(self):
        """Hang around until all runnable processes are finished."""
        # ...

    def proc_finished(self, process):
        """Receive notification that "proc" has finished.
        Only called from running processes.
        """
        # ...

    def proc_waiting(self, process):
        """Receive notification that process is waiting for input."""
        # ...

    def process_with_id(self, id):
        """Return the process with the id."""
        # ...
        return None
