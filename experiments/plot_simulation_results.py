"""
To run this file, you need to
    pip install experiments_csv>=0.5.3
"""


from experiments_csv import single_plot_results, multi_plot_results
from matplotlib import pyplot as plt
from pathlib import Path

filter={"num_of_items": 20, 
        "algorithm": [
            "yekta_day", "almost_egalitarian_allocation", "iterated_maximum_matching",
            "round_robin", "bidirectional_round_robin"
          ]}

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_utilitarian.png",
     filter=filter, 
     x_field="value_noise_ratio", y_field="utilitarian_value", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_egalitarian.png",
     filter=filter, 
     x_field="value_noise_ratio", y_field="egalitarian_value", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_maxenvy.png",
     filter=filter, 
     x_field="value_noise_ratio", y_field="max_envy", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_meanenvy.png",
     filter=filter, 
     x_field="value_noise_ratio", y_field="mean_envy", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_meandeficit.png",
     filter=filter, 
     x_field="value_noise_ratio", y_field="mean_deficit", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_maxdeficit.png",
     filter=filter, 
     x_field="value_noise_ratio", y_field="max_deficit", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_top1.png",
     filter=filter, 
     x_field="value_noise_ratio", y_field="num_with_top_1", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_top2.png",
     filter=filter, 
     x_field="value_noise_ratio", y_field="num_with_top_2", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_top3.png",
     filter=filter, 
     x_field="value_noise_ratio", y_field="num_with_top_3", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )

multi_plot_results(
     "results/course_allocation_biased.csv", 
     save_to_file="results/course_allocation_biased_runtime.png",
     filter=filter, 
     x_field="value_noise_ratio", y_field="runtime", z_field="algorithm", mean=True, 
     subplot_field = "num_of_agents", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
     legend_properties={"size":6}, 
     )


######## OLD PLOTS

# multi_plot_results(
#      "results/many_to_many_matchings.csv", save_to_file=True,
#      filter={}, 
#      x_field="item_capacity", y_field="runtime", z_field="algorithm", subplot_field = "agent_capacity", 
#      mean=True, subplot_rows=2, subplot_cols=3, sharey=True, sharex=True,
#      legend_properties={"size":6}, ylim=(0,30), xlim=(0,40))


# multi_plot_results(
#      "results/fractional_course_allocation.csv", 
#      save_to_file=True,
#     #  filter={"num_of_items": [5,10,20,30]},  # ValueError: ('Lengths must match to compare', (760,), (4,))
#      filter={}, 
#      x_field="num_of_agents", y_field="runtime", z_field="algorithm", mean=True, 
#      subplot_field = "num_of_items", subplot_rows=2, subplot_cols=2, sharey=True, sharex=True,
#      legend_properties={"size":6}, 
#      )
