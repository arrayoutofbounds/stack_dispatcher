# A1 for COMPSCI340/SOFTENG370 2015
# Prepared by Robert Sheehan
# Modified by ...

# You are not allowed to use any extra sleep calls.

import threading
import _thread
from random import randint
from time import sleep
from enum import Enum

Type = Enum("Type", "background interactive")
State = Enum("State", "runnable waiting killed")

class Process(threading.Thread):
    """A process."""

    next_id = 1

    def __init__(self, iosys, dispatcher, type):
        """Construct a process.
        iosys - the io subsystem so the process can do IO
        dispatcher - so that the process can notify the dispatcher when it has finished
        """
        threading.Thread.__init__(self)
        #assign pid..incremented
        self.id = Process.next_id
        Process.next_id += 1

        # this prints the stars to the screen
        self.iosys = iosys

        #assigns a dispatcher...that ensures loading/unloading of processes depending on state
        self.dispatcher = dispatcher

        #defines what state that the process is in
        self.type = type



        self.panel = None
        self.daemon = True

        # You will need a process state variable - self.state
        # which should only be modified by the dispatcher and io system.
        # the state can be used to determine which list - runnable or waiting the process
        # appears in.
        # ...

        self.state = State.runnable

        # have a threading event added to the process to control this process object from outside
        self.event = threading.Event()


    def run(self):

        # need to add checks for state
        # set runnable to 0 , waiting to 1 etc

        #if (self.state == State.runnable):
        #    pass
        #elif( self.state == Start.waiting):
        #    pass
        #else:
        #    pass       



        """Start the process running."""
        if self.type == Type.background:
            # runs the background method from this class itself.
            self.run_background()
        elif self.type == Type.interactive:
            # runs the interactive thread method from this class itself.
            self.run_interactive()
        self.dispatcher.proc_finished(self)

    def run_interactive(self):
        """Run as an interactive process."""
        # Something like the following but you will have to think about
        # pausing and resuming the process.

        # me : after the user input comes back you have to move the window to the next in runnable process
        # and even set the state of the process to running

        # LOOPS WILL NOT RUN IF 0 or LESS

        loops = self.ask_user()
        while loops > 0:
            for i in range(loops):
                self.main_process_body()
            self.iosys.write(self, "\n") # writes the data to the process window
            loops = self.ask_user() # asks the user again for input.

    def run_background(self):
        # gets random number from 10 to 160 and then runs the loop that many times.
        # each time the loop runs it prints a asterix (*).

        """Run as a background process."""
        loops = randint(10, 160)
        for i in range(loops):
            self.main_process_body()

        # call this when process is finished     

    def ask_user(self):

        # this method is used inthe run_interactive method above. It 
        # asks the user for a number to run the loop
        # if the input is -1 then the process is quit. If above -1 then it runs and 
        # asks the user again for an input

        """Ask the user for number of loops."""
        self.iosys.write(self, "How many loops? ")

        input = None

        while input is None:
            self.event.wait()
            input = self.iosys.read(self)

        if self.state == State.killed:
            _thread.exit()
        return int(input)

    def main_process_body(self):
        # Something like the following but you will have to think about
        # pausing and resuming the process.


        # check to see if supposed to terminate
        if self.state == State.killed:
            _thread.exit()
        
        self.event.wait()

        self.iosys.write(self, "*")
        sleep(0.1)
