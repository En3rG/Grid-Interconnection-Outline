import datetime
import logging
import functools

def initLogs(loglevel):
    print("...Initializing logs/read settings.xml")

    ## START TIME
    start_time = datetime.datetime.now()

    ## GET THE TIME YYYY-MM-DD_HR_MIN_SEC_XXXXXX FORMAT
    times = str(start_time)
    times = times.replace(":", "_")
    times = times.replace(".", "_")
    logfile = "../logs/" + times + ".log"

    ## DEBUG prints: 	debug, info, warning, error
    ## INFO prints: 	info, warning, error
    ## WARNING prints: 	warning, error

    levels = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR}

    ## EX: levels['debug'] = loggging.DEBUG
    level = levels[str(loglevel)]

    logging.basicConfig(filename=logfile,
                        format='%(asctime)s %(levelname)7s %(filename)s %(lineno)5s %(funcName)20s: %(message)s ',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=level)
    logging.basicConfig()
    logging.debug('<- will be printed')
    logging.info('<- will be printed')
    logging.warning('<- will be printed')
    logging.error("<- will be printed")
    logging.info("**************************************************************************************")

## DECORATOR FOR JUST A REGULAR FUNCTION OR __INIT__ FUNCTION?
def catch_wrapper(func):
    @functools.wraps(func)
    def func_wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            logging.error("From: %s", func.__name__)
            logging.error(str(e))
            print("From: ", func.__name__)
            print("Error:", str(e))
    return func_wrapper

## DECORATOR FOR A FUNCTION IN A CLASS (NOT WORKING ALL THE TIME THOUGH)
## ALSO TAKES INTO ACCOUNT OBJ WHO CALLED THE WRAPPER (SELF)
def catch_wrapper_classfunc(func):
    #@functools.wraps(func)
    def func_wrapper(calling_obj,*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            logging.error("Calling_obj: %s", calling_obj)
            logging.error("From: %s", func.__name__)
            logging.error(str(e))
            print("Calling_obj", calling_obj)
            print("From: ", func.__name__)
            print("Error:", str(e))
    return func_wrapper