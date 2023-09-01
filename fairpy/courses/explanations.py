"""
A class for writing explanations to allocations.

Programmer: Erel Segal-Halevi.
Since: 2023-08
"""

from abc import ABC, abstractmethod
import logging

import numpy as np
from fairpy.courses.instance import Instance

class ExplanationLogger:
    """
    The base explanation logger does nothing.
    """
    def info(self, message:str, *args, agents=None):
        pass

    def debug(self, message:str, *args, agents=None):
        pass

    def explain_valuations(self, instance:Instance):
        for agent in instance.agents:
            self.info("Your valuations:", agents=agent)
            for item in sorted(instance.items, key=lambda item: instance.agent_item_value(agent,item), reverse=True):
                self.info(" * %s: %g", item, instance.agent_item_value(agent,item), agents=agent)
            self.info("You need %d courses, so your maximum possible value is %g.", instance.agent_capacity(agent), instance.agent_maximum_value(agent), agents=agent)

    def explain_allocation(self, allocation:dict, instance:Instance, map_course_to_name:dict={}):
        for agent,bundle in allocation.items():
            self.info("Your bundle is:", agents=agent)
            ranking = instance.agent_ranking(agent, bundle)
            for item in sorted(bundle, key=ranking.__getitem__):
                self.info(f" * Course {map_course_to_name.get(item,item)} (number {ranking[item]} in your ranking), with value {instance.agent_item_value(agent,item)}", agents=agent)
            absolute_value = instance.agent_bundle_value(agent,bundle)
            maximum_value  = instance.agent_maximum_value(agent)
            relative_value = absolute_value/maximum_value*100
            self.info(f"The maximum possible value you could get for {instance.agent_capacity(agent)} courses is {maximum_value}.", agents=agent)
            self.info(f"The total value of this bundle is {absolute_value}, which is {np.round(relative_value)}% of the maximum.", agents=agent)

    def explain_fractional_allocation(self, fractional_allocation:dict, instance:Instance, map_course_to_name:dict={}):
        for agent,bundle in fractional_allocation.items():
            self.info("Your fractional bundle is:", agents=agent)
            ranking = instance.agent_ranking(agent)
            for item,fraction in sorted(bundle.items(), key=lambda pair: ranking[pair[0]]):
                if fraction>0:
                    self.info(f" * Course {map_course_to_name.get(item,item)}: {np.round(100*fraction)}%.", agents=agent)
            absolute_value = instance.agent_fractionalbundle_value(agent,bundle)
            maximum_value  = instance.agent_maximum_value(agent)
            relative_value = absolute_value/maximum_value*100
            self.info(f"The maximum possible value you could get for {instance.agent_capacity(agent)} courses is {maximum_value}.", agents=agent)
            self.info(f"The total value of this fractional bundle is {absolute_value}, which is {np.round(relative_value)}% of the maximum.", agents=agent)



class SingleExplanationLogger(ExplanationLogger):
    """
    An explanation logger in which all messages are written to the same single base-logger.
    """
    def __init__(self, logger:logging.Logger):
        self.logger = logger

    def debug(self, message:str, *args, agents=None):
        if agents is None or not is_individual_agent(agents):  # to all agents
            self.logger.debug(message, *args)
        else:                                          # to one agent
            self.logger.debug(agents+": "+message.strip(), *args)

    def info(self, message:str, *args, agents=None):
        if agents is None or not is_individual_agent(agents):  # to all agents
            self.logger.info(message, *args)
        else:                                          # to one agent
            self.logger.info(agents+": "+message.strip(), *args)


class ConsoleExplanationLogger(SingleExplanationLogger):
    """
    A convenience class: an explanation logger in which all messages are written to the console. 
    """
    def __init__(self, level=logging.DEBUG):
        logger = logging.getLogger("Explanation console")
        logger.setLevel(level)
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
        elif is_individual_agent(agents):
            self.map_agent_to_logger[agents].debug(message, *args)
        else:
            for agent in agents:
                self.map_agent_to_logger[agent].debug(message, *args)

    def info(self, message:str, *args, agents=None):
        if agents is None:
            for agent,logger in self.map_agent_to_logger.items():
                logger.info(message, *args)
        elif is_individual_agent(agents):
            self.map_agent_to_logger[agents].info(message, *args)
        else:
            for agent in agents:
                self.map_agent_to_logger[agent].info(message, *args)



class FilesExplanationLogger(ExplanationLoggerPerAgent):
    """
    A convenience class: an explanation logger in which all messages for each agent are written to an agent-specific file. 
    """
    def __init__(self, map_agent_to_filename:dict, level=logging.DEBUG, **kwargs):
        map_agent_to_logger ={}
        for agent,filename in map_agent_to_filename.items():
            logger = logging.getLogger(f"Explanation file for agent {agent}")
            logger.setLevel(level)
            logger.addHandler(logging.FileHandler(filename, **kwargs))
            map_agent_to_logger[agent] = logger
        super().__init__(map_agent_to_logger)



class LogStream(object):
    def __init__(self):
        self.text = ''
    def write(self, str):
        self.text += str
    def flush(self):
        pass
    def __str__(self):
        return self.text


# from io import StringIO
class StringsExplanationLogger(ExplanationLoggerPerAgent):
    """
    A convenience class: an explanation logger in which all messages for each agent are written to an agent-specific string. 
    """
    def __init__(self, agents:list, level=logging.DEBUG, **kwargs):
        map_agent_to_logger = {}
        self.map_agent_to_stream = {}
        for agent in agents:
            self.map_agent_to_stream[agent] = LogStream()
            logger = logging.getLogger(f"Explanation string for agent {agent}")
            logger.setLevel(level)
            logger.addHandler(logging.StreamHandler(self.map_agent_to_stream[agent]))
            map_agent_to_logger[agent] = logger
        super().__init__(map_agent_to_logger)

    def agent_string(self, agent):
        return str(self.map_agent_to_stream[agent])

    def map_agent_to_explanation(self):
        return {
            agent: str(self.map_agent_to_stream[agent])
            for agent in self.map_agent_to_stream.keys()
        }

def is_individual_agent(agents):
    return isinstance(agents,int) or isinstance(agents,str)


