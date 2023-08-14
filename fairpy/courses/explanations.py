"""
A class for writing explanations to allocations.

Programmer: Erel Segal-Halevi.
Since: 2023-08
"""

from abc import ABC, abstractmethod
import logging


class ExplanationLogger:
    """
    The base explanation logger does nothing.
    """
    def info(self, message:str, *args, agents=None):
        pass


class SingleExplanationLogger(ExplanationLogger):
    """
    An explanation logger in which all messages are written to the same single base-logger.
    """
    def __init__(self, logger:logging.Logger):
        self.logger = logger

    def debug(self, message:str, *args, agents=None):
        if agents is None or not isinstance(agents,str):  # to all agents
            self.logger.debug(message, *args)
        else:                                          # to one agent
            self.logger.debug(agents+": "+message.strip(), *args)

    def info(self, message:str, *args, agents=None):
        if agents is None or not isinstance(agents,str):  # to all agents
            self.logger.info(message, *args)
        else:                                          # to one agent
            self.logger.info(agents+": "+message.strip(), *args)


class ConsoleExplanationLogger(SingleExplanationLogger):
    """
    A convenience class: an explanation logger in which all messages are written to the console. 
    """
    def __init__(self):
        logger = logging.getLogger("Explanations")
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())
        super().__init__(logger)


class ExplanationLoggerPerAgent(ExplanationLogger):
    """
    An explanation logger in which there is one logger per agent.
    """

    def __init__(self, map_agent_to_logger: dict[str,logging.Logger]):
        self.map_agent_to_logger = map_agent_to_logger


    def debug(self, message:str, *args, agents=None):
        if agents is None:
            for agent,logger in self.map_agent_to_logger.items():
                logger.debug(message, *args)
        elif isinstance(agents,str):
            self.map_agent_to_logger[agents].debug(message, *args)
        else:
            for agent in agents:
                self.map_agent_to_logger[agent].debug(message, *args)

    def info(self, message:str, *args, agents=None):
        if agents is None:
            for agent,logger in self.map_agent_to_logger.items():
                logger.info(message, *args)
        elif isinstance(agents,str):
            self.map_agent_to_logger[agents].info(message, *args)
        else:
            for agent in agents:
                self.map_agent_to_logger[agent].info(message, *args)



class FilesExplanationLogger(ExplanationLoggerPerAgent):
    """
    A convenience class: an explanation logger in which all messages for each agent are written to an agent-specific file. 
    """
    def __init__(self, map_agent_to_filename:dict, **kwargs):
        map_agent_to_logger ={}
        for agent,filename in map_agent_to_filename.items():
            logger = logging.getLogger(f"Explanations for agent {agent}")
            logger.setLevel(logging.DEBUG)
            logger.addHandler(logging.FileHandler(filename, **kwargs))
            map_agent_to_logger[agent] = logger
        super().__init__(map_agent_to_logger)


