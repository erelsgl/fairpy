# NOTE: to run this file, you need the optional module "plotting":
#    pip install experiments_csv[plotting]


from experiments_csv import single_plot_results, multi_plot_results
from matplotlib import pyplot as plt

multi_plot_results(
     "results/many_to_many_matchings.csv", save_to_file=True,
     filter={}, 
     x_field="item_capacity", y_field="runtime", z_field="algorithm", mean=True, 
     subplot_field = "agent_capacity", subplot_rows=2, subplot_cols=3, sharey=True, sharex=True,
     legend_properties={"size":6}, ylim=(0,30), xlim=(0,40))
