import os, shutil, sys, logging
from datetime import datetime

from src.utils.common import utils
from src.utils.common import selenium_common

FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
DEFAULT_CONFIG = {
    "log_level" : 1, # 1 - DEBUG, 2 - INFO, 3 - WARN, 4- ERROR
    
    "print_log_to_output" : True,
    "write_log_to_file" : True,
    
    "clear_logs_init" : False,
    
    "appends_stack_call_to_log" : True,
}

class Log:

    def __init__(self, directory:str, name:str="cdc-helper", config:dict=DEFAULT_CONFIG):
        log = logging.getLogger(name)

        self.logger = log  
        self.name = name
        self.directory = directory 
        self.config = utils.init_config_with_default(config, DEFAULT_CONFIG)

        if self.config["clear_logs_init"]:
            utils.clear_directory(directory=self.directory, log=self.logger)
        
        if self.config["print_log_to_output"]:
            terminal_output = logging.StreamHandler(sys.stdout)
            terminal_output.setFormatter(FORMATTER)
            log.addHandler(terminal_output)
        
        if self.config["write_log_to_file"]:        
            file_output = logging.FileHandler('{dir}/tracker_{date}.log'.format(dir=directory, date=datetime.today().strftime("%Y-%m-%d_%H-%M")))
            file_output.setFormatter(FORMATTER)
            log.addHandler(file_output)

        log.setLevel(int(self.config["log_level"]) * 10)
        
    def append_stack_if(self, log_type, *output):
        msg = utils.concat_tuple(output)
        if self.config["appends_stack_call_to_log"]:
            log_type("=======================================================================================")
            log_type(*output, stack_info=True)
            log_type("\n=======================================================================================\n")
        else:
            log_type(msg)
        
    def info(self, *output):
        self.append_stack_if(self.logger.info, *output)
            
    def debug(self, *output):
        self.append_stack_if(self.logger.debug, *output)
            
    def error(self, *output):
        self.append_stack_if(self.logger.error, *output)
        
    def warning(self, *output):
        self.append_stack_if(self.logger.warning, *output)
        
        
    
    def info_if(self, condition:bool, *output):
        if condition:
            self.info(*output)
            
    def debug_if(self, condition:bool, *output):
        if condition:
            self.debug(*output)

    def error_if(self, condition:bool, *output):
        if condition:
            self.error(*output)
        
    def warning_if(self, condition:bool, *output):
        if condition:
            self.warning(*output)
    