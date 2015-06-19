import networkx as nx
from load_data import *
from compute_metrics_multiplex import *

def numNodes(g):
    return g.number_of_nodes()
    
def numEdges(g):
    return g.number_of_edges()
    
def avgDeg(g):
    return g.number_of_edges()*1.0/g.number_of_nodes()
    
def getGiantComponent(g):
    return g.subgraph(max([key for key in nx.strongly_connected_components(g)],key=len))
    
def diameter(g):
    return nx.diameter(getGiantComponent(g))
    
def avgPathLen(g):
    return nx.average_shortest_path_length(getGiantComponent(g))
    
def nodesInGiantComponent(g):
    return getGiantComponent(g).number_of_nodes()
    
def edgesInGiantComponent(g):
    return getGiantComponent(g).number_of_edges()

def assortativity(g):
    return nx.degree_assortativity_coefficient(g,x="in",y="in")
    
stats = { "# nodes":numNodes, "# edges":numEdges, "Avg. degree":avgDeg , "Diameter":diameter,\
          "Avg. path length":avgPathLen, "# Nodes in GC":nodesInGiantComponent,"# Edges in GC":edgesInGiantComponent,\
          "Assortativity":assortativity}

def getHeader():
    res = "\t"
    for stat in stats:
        res += ","+stat
    return res
    
    
def getStatsForGraph(g):
    res = g.graph["title"][4:]
    for stat in stats:
        res += ","+str(stats[stat](g))
    return res

def getGlobalStatsFromAttribute(graphs,graph_combinations=[],metrics=[]):
    res = graphs[0].graph["title"][:3]
    for metric in metrics:
        res += ","+metric
            
    for i,k in graph_combinations:
        gi,gk = graphs[i],graphs[k]
        if i == k:
            res += "\n"+gi.graph["title"][4:]
        else:
            res += "\n"+gi.graph["title"][4:]+"->"+gk.graph["title"][4:]
        for metric in metrics:
            attribute_name = "Global "+getMetricString(metric,gi,gk)
            res += ",{0:.3f}".format(gi.graph[attribute_name])            
    return res
    
def getStasForDataset(dataset="wan"):
    graphs,node_mapping = load_4_layers(dataset)
    metrics = metrics_dict_multiplex.copy()
    del metrics["Overlapping Index"]
    temp = [(i,i) for i in range(len(graphs))]
    addMetricsAsAttributesMultiplex(graphs,temp,metrics)
    res = getGlobalStatsFromAttribute(graphs,temp,metrics)
    res += "\n"
    res += "\n"
    res += "Multiplex"
    res += "\n"
    res += "\n"
    metrics = metrics_dict_multiplex.copy()
    temp = graph_combinations+[(k,i) for i,k in graph_combinations]
    addMetricsAsAttributesMultiplex(graphs,temp,metrics)
    res += getGlobalStatsFromAttribute(graphs,temp,metrics)
    
    return res 

def main():
    with open("wan_graph_stats.csv","w") as pout:
        graphs,node_mapping = load_4_layers("wan")
        pout.write(getHeader())
        for g in graphs:
            pout.write("\n"+getStatsForGraph(g))
            
    with open("bms_graph_stats.csv","w") as pout:
        graphs,node_mapping = load_4_layers("bms")
        pout.write(getHeader())
        for g in graphs:
            pout.write("\n"+getStatsForGraph(g))
    
if __name__ == "__main__":
    main()

