import datetime
from multiprocessing import Process, Pool, freeze_support, Queue, Lock
import time
import ctypes


########################################################################################################################
##
########################################################################################################################
class Process_handler:
    ## WHEN INITIALIZED
    def __init__(self):
        self.jobslist = []
        self.process_number = []
        self.process_started = 0
        self.verbose = None

	## GATHER ALL PROCESS TO BE DONE
	## EACH PROCESS WILL HAVE FUNCTION, q, AND ARGS (ARGS IS A LIST)
    def gather(self, func_,args_):
        arg_dict = {}
        arg_dict['function'] = func_
        arg_dict['q'] = Queue()
        arg_dict['args'] = args_
        self.jobslist.append(arg_dict)

    def get_len_joblist(self):
        return len(self.jobslist)

    def get_num_cores(self):
        return self.number_of_cores

    def run_all(self, number_of_cores = 2, verbose = True):
        if number_of_cores == 1:
            ctypes.windll.user32.MessageBoxW(None, "2 or more core for multiprocess", "Error", 0)

        self.verbose = verbose

        self.number_of_cores = number_of_cores
        for x in range(0, self.number_of_cores):
            p = Process()
            p.start()
            p.terminate()
            self.process_number.append(p)

		## ADDED DELAY TO WAIT TO STOP
        time.sleep(.001)
        if self.verbose == True:
            print("Jobs: ", len(self.jobslist))
        
		## RUN UNTIL job_number REACHES LEN OF JOBLIST
        while (self.process_started < len(self.jobslist)):
            if self.verbose == True:
                print("Process starting... ", self.process_started)
			## CHECK WHICH HAS NO PROCESS RUNNING (LOOPS UP TO THE number_of_cores)
            for x in range(0,self.number_of_cores):
                if self.process_number[x].is_alive() == False:
                    arguments = []
                    arguments.append(self.jobslist[self.process_started]['q'])
                    for i in range(0,len(self.jobslist[self.process_started]['args'])):
                        arguments.append(self.jobslist[self.process_started]['args'][i])

                    self.process_number[x] = Process(target=self.jobslist[self.process_started]['function'], args=arguments)
                    self.process_number[x].start()
                    if self.verbose == True:
                        print("Started process for job: ", self.process_started)
                    self.process_started = self.process_started + 1

					## IF ITS THE LAST JOB, BREAK OUT
                    if self.process_started == len(self.jobslist):
                        break
            time.sleep(.25)




