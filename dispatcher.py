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
        self.top_of_stack = 0

        # list to show where to place next waiting process
        self.next_in_waiting = 0

         # list of runnable processes
        self.runnable_processes = []

        # list of waiting for input procceses
        self.waiting_processes = []


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
        self.io_sys.move_process(process,self.top_of_stack)

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

        if(len(self.runnable_processes) > 0):
            self.runnable_processes[len(self.runnable_processes) - 1].event.clear()

        if(len(self.runnable_processes) > 1):
            self.runnable_processes[len(self.runnable_processes) - 2].event.clear()
        

    def resume_system(self):
        """Resume running the system."""
        # ...

        if(len(self.runnable_processes) > 0):
            self.runnable_processes[len(self.runnable_processes) - 1].event.set()

        if(len(self.runnable_processes) > 1):
            self.runnable_processes[len(self.runnable_processes) - 2].event.set()


        
        

    def wait_until_finished(self):
        """Hang around until all runnable processes are finished."""
        # ...

        while (len(self.runnable_processes) >0):
            pass

            

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
        self.top_of_stack -= 1

        #start the next process
        self.dispatch_next_process()


        #step 2: remove from list of runnable

    def proc_waiting(self, process):
        """Receive notification that process is waiting for input."""
        # ...

        # this method tells the dispatcher that the process given input is waiting
        # so set the state to waiting and remove it from the list of runnable processes
        # and give it the first empty position in the set of waiting processes
        if (process.state == State.runnable):
            # set the state to waiting
            process.state = State.waiting

            # STOP THE PROCESS....
            process.event.clear()

            # get the index of the process to move to waiting
            indexOfProcess = self.runnable_processes.index(process)

            # delete the process from the runnable list
            del self.runnable_processes[indexOfProcess]

            self.top_of_stack -= 1

            # append the process to the list of waiting processes
            self.waiting_processes.append(process)

            # move the process to the waiting panel
            self.io_sys.move_process(process,self.next_in_waiting)

            #incrememnt the next space for waiting
            self.next_in_waiting += 1

            #shuffle things on left to appropriate places
            self.moving2()

            self.dispatch_next_process()
            
        else:
            self.done_waiting(process)    


    def done_waiting(self, process):

        if(self.top_of_stack >= 2):
            # for p in range( 0, len(self.runnable_processes) - 2):
            self.runnable_processes[self.top_of_stack - 2].event.clear()

        # set it to runnable
        process.state = State.runnable

        #set it to run
        process.event.set()

        # get the index of the process to move from waiting
        indexOfProcess = self.waiting_processes.index(process)

        # delete the process from the runnable list
        del self.waiting_processes[indexOfProcess]

        self.next_in_waiting -= 1

        # append it to runnable list
        self.runnable_processes.append(process)

        # send it to runnable side - visually
        self.io_sys.move_process(process,self.top_of_stack)

        self.top_of_stack += 1

        self.moving3()

        self.dispatch_next_process()


    def process_with_id(self, id):
        """Return the process with the id."""
        # ...

        # need to check if the process is in runnable or waiting list
        # and carry the code out accordingly

        processToMove = None

        # wrong because there will be time when it does not match....and it keeps printing not found that time
        for p in self.runnable_processes:

            if(p.id == id):
                processToMove = p
                break
        
        for p in self.waiting_processes:

            if(p.id == id):
                processToMove = p
                break

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

    def moving3(self):

        # this goes throught he updated list and just movies it to the
        # same position as the index it is in
        for i in range(0,len(self.waiting_processes)):

            self.io_sys.move_process(self.waiting_processes[i],i)        


    def killing_process(self,process):

        #remove from the lists if the process is there
        if process in self.runnable_processes:

            # need to de allocate that process from the windows
            self.io_sys.remove_window_from_process(process)

            # get the index of the process to remove
            index = self.runnable_processes.index(process)
            
            # delete that process from the stack
            del self.runnable_processes[index]

            #decrement top of stack as one item just got deleted permanently from the stack
            self.top_of_stack -= 1

            # re map the processes left to the window panel
            self.moving2()
            
        elif (process in self.waiting_processes):

            # remove the process from a window
            self.io_sys.remove_window_from_process(process)

            # need to find the index of the process in the waiting list
            index1 = self.waiting_processes.index(process)

            # delete the process from the waiting list
            del self.waiting_processes[index1]

            # decrement as the list for waiting got smaller. So next value is put at a lower value
            self.next_in_waiting -= 1

            # call this method to rearrange the list.
            self.moving3()
        else:
            pass      

        # set the state of process to kill. This has to be set after the code above as this code will end the thread
        # refer to process.main body method, where each time the thread is run, it is checked to see if it is to be killed or not
        # depening on its state
        process.state = State.killed    
        
        # call dispatch method to ensure that the last and the second process in the current representation are run
        self.dispatch_next_process()











