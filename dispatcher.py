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

        # if the length is 0 then do nothing
        # else if the length is 1 then only run the lone process
        # else the length is >1 then run the last 2 processes

        if (len(self.runnable_processes) == 0):
            pass
        elif (len(self.runnable_processes) == 1):
            self.runnable_processes[len(self.runnable_processes) - 1].event.set()
        else:
            #set the last and the second last process to work
            self.runnable_processes[len(self.runnable_processes) - 1].event.set()
            self.runnable_processes[len(self.runnable_processes) - 2].event.set()
  


    def to_top(self, process):
        """Move the process to the top of the stack."""
        # ...

        # get index of process to move to top
        index = self.runnable_processes.index(process)

        # delete the process from the list 
        del self.runnable_processes[index]
        
        # append the same process to the end of the list (top of the stack)
        self.runnable_processes.append(process)

        # call the iosys move process method and move the process to the top of the stack -1. I.e just replacing the existing process at top
        self.io_sys.move_process(process,self.top_of_stack-1)

        # call the local moving method to make sure that the empty spaces are filled ( i.e list matches the visual....with no gaps)
        self.moving2()

        # make the third to last process wait ( it was the second to last process before we moved a process to the top)
        self.runnable_processes[len(self.runnable_processes) - 3].event.clear()

        # call dispatch method to ensure that the last and the second process in the current representation are run
        self.dispatch_next_process()



    def pause_system(self):
        """Pause the currently running process.
        As long as the dispatcher doesn't dispatch another process this
        effectively pauses the system.
        """
        # set the last 2 items in the list to clear

        self.runnable_processes[len(self.runnable_processes) - 1].event.clear()
        self.runnable_processes[len(self.runnable_processes) - 2].event.clear()

    def resume_system(self):
        """Resume running the system."""
        # ...
        self.runnable_processes[len(self.runnable_processes) - 1].event.set()
        self.runnable_processes[len(self.runnable_processes) - 2].event.set()

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

        # move before removing
        length = len(self.runnable_processes)
        
        if(self.runnable_processes[length-1].id == process.id):
            
            position = length -1
            #self.moving(position)

            del self.runnable_processes[length-1]

            self.moving2()
        else:
            position = length -2

            #self.moving(position)
            del self.runnable_processes[length-2]

            self.moving2()

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
        processToMove = None

        for p in self.runnable_processes:

            if(p.id == id):
                processToMove = p
                break
            else:
                print ("Process Number not found")
        
        return processToMove

    # move the process down the stack   
    # DO NOT USE THIS
    def moving(self,position):

        for i in range(position,len(self.runnable_processes)):

            if(i == len(self.runnable_processes) -1 ):
                break
            else:
                self.io_sys.move_process(self.runnable_processes[i+1],position)

                position += 1



    def moving2(self):

        # this goes throught he updated list and just movies it to the
        # same position as the index it is in
        for i in range(0,len(self.runnable_processes)):

            self.io_sys.move_process(self.runnable_processes[i],i)
