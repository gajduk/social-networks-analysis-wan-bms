import networkx as nx
from load_data import *

def numNodes(g):
    return g.number_of_nodes()
    
def numEdges(g):
    return g.number_of_edges()
    
def avgDeg(g):
    return g.number_of_edges()*1.0/g.number_of_nodes()
    
def reciprocity(g):
    count = 0
    for from_node,to_node in g.edges():
        if g.has_edge(to_node,from_node):
            count += 1
    return count*1.0/len(g.edges())
    
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
    
stats = { "# nodes":numNodes, "# edges":numEdges, "Avg. degree":avgDeg , "Reciprocity":reciprocity, "Diameter":diameter,\
          "Avg. path length":avgPathLen, "# Nodes in GC":nodesInGiantComponent,"# Edges in GC":edgesInGiantComponent,\
          "Assortativity":assortativity}

def getHeader():
    res = "\t"
    for stat in stats:
        res += ","+stat
    return res
    
def getStatsForGraph(g):
    res = g.graph["title"]
    for stat in stats:
        res += ","+str(stats[stat](g))
    return res
    
def getStasForDataset(dataset="wan"):
    graphs,node_mapping = load_4_layers(dataset)
    res = getHeader()
    for g in graphs:
        res += "\n"+getStatsForGraph(g)
    return res   

