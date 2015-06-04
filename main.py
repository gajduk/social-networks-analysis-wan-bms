from visualization import *
from compute_network_statistics import *


def main():
    with open("wan_stats.csv","w") as f:
        f.write(getStasForDataset(dataset="wan"))
        
    

if __name__ == "__main__"    :
    main()