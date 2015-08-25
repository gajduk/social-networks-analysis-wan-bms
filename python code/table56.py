import networkx as nx
from load_data import *
from compute_metrics_multiplex import *
from compute_network_statistics import *

def get56TablesForDataset(dataset="wan"):
    graphs,node_mapping = load_4_layers(dataset)
    metrics = ["Reciprocity","tc2","tp2"]
    #sOff,sON | wOff,wON | sOff,wOFF | sOn,wON | s,w | Off,ON
    temp = [(0,3),(1,4),(0,1),(3,4),(6,7),(2,5)]
    temp = temp+[(k,i) for i,k in temp]
    addMetricsAsAttributesMultiplex(graphs,temp,metrics)
    res = getGlobalStatsFromAttribute(graphs,temp,metrics)
    return res

def main():
    path = """..\\results\\novi rezultati\\"""
    csv_file = """table_56.csv"""
    table_file = """table_56.txt"""
    
    with open(path+"wan_"+csv_file,"w") as pout:
        pout.write(get56TablesForDataset("wan"))
    
    table_from_csv(path+"wan_"+table_file,path+"wan_"+csv_file)
    
    with open(path+"bms_"+csv_file,"w") as pout:
        pout.write(get56TablesForDataset("bms"))
    
    table_from_csv(path+"bms_"+table_file,path+"bms_"+csv_file)
        
        
if __name__ == "__main__":
    main()