from visualization import *
from compute_network_statistics import *
from compute_metrics_multiplex import *

def main():
    for metric in metrics_dict_multiplex:
        visualizeMetricMutliplex(dataset="bms",metric=metric,save_to_file=True)
    
if __name__ == "__main__"    :
    main()