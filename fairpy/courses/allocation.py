def sorted_allocation(map_agent_name_to_bundle:dict):
    for agent,bundle in map_agent_name_to_bundle.items():
        if isinstance(bundle,list):
            bundle.sort()
        else: 
            map_agent_name_to_bundle[agent] = sorted(bundle)
    return map_agent_name_to_bundle
