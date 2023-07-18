"""
To run this file, you need to
    pip install experiments_csv[plotting]
"""


from experiments_csv import single_plot_results, multi_plot_results
from matplotlib import pyplot as plt
from pathlib import Path

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_utilitarian.png",
     filter={"num_of_items": 20}, 
     x_field="value_noise_ratio", y_field="utilitarian_value", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_egalitarian.png",
     filter={"num_of_items": 20}, 
     x_field="value_noise_ratio", y_field="egalitarian_value", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_maxenvy.png",
     filter={"num_of_items": 20}, 
     x_field="value_noise_ratio", y_field="max_envy", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_meanenvy.png",
     filter={"num_of_items": 20}, 
     x_field="value_noise_ratio", y_field="mean_envy", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

# multi_plot_results(
#      "results/many_to_many_matchings.csv", save_to_file=True,
#      filter={}, 
#      x_field="item_capacity", y_field="runtime", z_field="algorithm", subplot_field = "agent_capacity", 
#      mean=True, subplot_rows=2, subplot_cols=3, sharey=True, sharex=True,
#      legend_properties={"size":6}, ylim=(0,30), xlim=(0,40))
