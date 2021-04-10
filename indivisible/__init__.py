#!python3

class SequentialAllocation:
	"""
	A class that handles the process of sequentially allocating bundles to agents, e.g., 
	  in a bag-filling procedure.
	"""

	def __init__(self, agents:list, objects:list, logger):
		self.remaining_agents = list(agents)
		self.remaining_objects = list(objects)
		self.bundles = len(agents)*[None]
		self.logger = logger

	def let_agent_get_objects(self, i_agent, allocated_objects):
		self.bundles[i_agent] = allocated_objects
		self.remaining_agents.remove(i_agent)
		for o in allocated_objects: 
			self.remaining_objects.remove(o)
		self.logger.info("Agent %d takes the bag with objects %s. Remaining agents: %s. Remaining objects: %s.", 
			i_agent, allocated_objects, self.remaining_agents, self.remaining_objects)


