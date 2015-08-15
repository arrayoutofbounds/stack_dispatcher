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

        # set the process flag to true so that it runs
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
        # set the event to set

        if (len(self.runnable_processes) == 0):
            pass
        elif (len(self.runnable_processes) == 1):
            self.runnable_processes[len(self.runnable_processes) - 1].event.set()
        else:
            self.runnable_processes[len(self.runnable_processes) - 2].event.set()
  


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

        #step 1 : deallocate the window 
        self.io_sys.remove_window_from_process(process)

        #remove from list of runnable processes
        #self.runnable_processes.remove(process)
        length = len(self.runnable_processes)
        
        if(self.runnable_processes[length-1].id == process.id):
            
            position = length -1
            self.moving(position)
            
            del self.runnable_processes[length-1]
        else:
            position = length -2

            self.moving(position)
            del self.runnable_processes[length-2]

        #decrement top of stack
        self.top_of_stack -= self.top_of_stack

        #start the next process
        self.dispatch_next_process()


        #step 2: remove from list of runnable

    def proc_waiting(self, process):
        """Receive notification that process is waiting for input."""
        # ...

    def process_with_id(self, id):
        """Return the process with the id."""
        # ...
        return None

    def moving(self,position):

        for i in range(position,len(self.runnable_processes)):

            if(i == len(self.runnable_processes) -1 ):
                break
            else:
                self.io_sys.move_process(self.runnable_processes[i+1],position)

                position += 1



