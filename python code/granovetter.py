import networkx as nx
from load_data import *
from compute_metrics_multiplex import *
from compute_network_statistics import *

def getGranovetterForDataset(dataset="wan"):
    graphs,node_mapping = load_4_layers(dataset)
    strong = graphs[6]
    weak = graphs[7]
    all = graphs[8]
    c_total_s_wedges = 0.0
    c_s_wedges_by_s = 0.0
    c_s_wedges_by_w = 0.0
    c_total_w_wedges = 0.0
    c_w_wedges_by_s = 0.0
    c_w_wedges_by_w = 0.0
    for i in range(strong.number_of_nodes()):
        for j in range(strong.number_of_nodes()):
            for k in range(strong.number_of_nodes()):
                if strong.has_edge(i,j) and strong.has_edge(j,k):
                    c_total_s_wedges += 1.0
                    if strong.has_edge(i,k) or strong.has_edge(k,i):
                        c_s_wedges_by_s += 1.0
                    if weak.has_edge(i,k) or weak.has_edge(k,i):
                        c_s_wedges_by_w += 1.0
                       
                if weak.has_edge(i,j) and weak.has_edge(j,k):
                    c_total_w_wedges += 1.0
                    if strong.has_edge(i,k) or strong.has_edge(k,i):
                        c_w_wedges_by_s += 1.0
                    if weak.has_edge(i,k) or weak.has_edge(k,i):
                        c_w_wedges_by_w += 1.0
                        

    c_s_wedges_by_a = c_s_wedges_by_s+c_s_wedges_by_w
    c_w_wedges_by_a = c_w_wedges_by_s+c_w_wedges_by_w
    return ("There are a total of {:.0f} strong wedges out of which:\n"+\
           "\t{:.3f} percent are closed by another strong link\n"+\
           "\t{:.3f} are closed by a weak link\n"+\
           "\t{:.3f} are closed by any link\n").format(c_total_s_wedges,c_s_wedges_by_s*100/c_total_s_wedges,c_s_wedges_by_w*100/c_total_s_wedges,c_s_wedges_by_a*100/c_total_s_wedges)+\
           ("\n\nThere are a total of {:.0f} weak wedges out of which:\n"+\
           "\t{:.3f} percent are closed by a strong link\n"+\
           "\t{:.3f} are closed by another weak link\n"+\
           "\t{:.3f} are closed by any link\n").format(c_total_w_wedges,c_w_wedges_by_s*100/c_total_w_wedges,c_w_wedges_by_w*100/c_total_w_wedges,c_w_wedges_by_a*100/c_total_w_wedges)
           

def main():
    path = """..\\results\\novi rezultati\\"""
    txt_file = """granovveter.txt"""
    
    with open(path+"wan_"+txt_file,"w") as pout:
        pout.write(getGranovetterForDataset("wan"))
    with open(path+"bms_"+txt_file,"w") as pout:
        pout.write(getGranovetterForDataset("bms"))
           
        
if __name__ == "__main__":
    main()