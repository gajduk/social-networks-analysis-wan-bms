import os,sys,random
import networkx as nx
import pylab as plt
import math

graph_combinations = [(0,3),(0,4),(1,3),(1,4),(2,5),(0,5),(1,5),(2,3),(2,4)]
#graph_combinations = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)]

def getMetricString(metric,g1,g2):
    return metric+"\n"+str(g1.graph['title'][4:])+"->"+str(g2.graph['title'][4:])

def outDeg(g,i):
    return len(g.out_edges(i))
    
def inDeg(g,i):
    return len(g.in_edges(i))
    
def maxOut(g):
    return max([outDeg(g,i) for i in range(g.number_of_nodes())])
    
def maxIn(g):
    return max([inDeg(g,i) for i in range(g.number_of_nodes())])
  
  
"""
return {j: i f j} where f is in_edges or out_edges functions for a graph

example
_n(0,g.out_edges)
"""
def _n(i,f):
    if "in" in f.__name__:
        return [j for j,_ in f(i)]   
    return [j for _,j in f(i)]
    
"""
return the set W_i = {h: i f1 j and j f2 h, where f1 and f2 are in_edges or out_edges functions for a graph

example
Wi(0,g.out_edges,g.out_edges)

"""
def Wi(i,f1,f2):
    res = set()
    temp1 = _n(i,f1)
    for j in temp1:
        res |= set(_n(j,f2))
    return res-set([i])
    
"""
Return the set W_i^n (g) =
n = 1
{h: i -> j and j -> h} (out,out)
n = 2
{h: i -> j and h -> j} (out,in)
n = 3
{h: j -> i and j -> h} (in,out)
n = 4
{h: j -> i and h -> j} (in,in)
"""
def nWi(i,g,n):
    if n == 1:
        return Wi(i,g.out_edges,g.out_edges)
    elif n == 2:
        return Wi(i,g.out_edges,g.in_edges)
    elif n == 3:
        return Wi(i,g.in_edges,g.out_edges)
    elif n == 4:
        return Wi(i,g.in_edges,g.in_edges)        
 
    
"""
Returns the Jaccard similarity between two sets or lists
Jaccard similarity for sets A and B is defined as

           | A /\ B |
JS =    ----------------
           | A U B |
            
"""    
def JS(s1,s2):
    temp1 = set(s1)
    temp2 = set(s2)
    if len(temp1|temp2) == 0:
        return 1.0
    return len(temp1&temp2)*1.0/len(temp1|temp2)
    
"""
returns (i->j g1) * (i->j g2)
"""         
def overlapIndex(g1,g2,i):
    return JS(_n(i,g1.out_edges),_n(i,g2.out_edges))
 
"""
returns (i->j g1) * (j->i g2)
"""     
def reciprocity(g1,g2,i):
    return JS(_n(i,g1.out_edges),_n(i,g2.in_edges))    
    
"""
returns (i->j g1) * (j->h g1) * (i->h g2)
"""    
def transTrip(g1,g2,i):
    return JS(Wi(i,g1.out_edges,g1.out_edges),_n(i,g2.out_edges))
    
"""
returns (i->j g1) * (j->h g1) * (h->i g2)
"""    
def threeCycles(g1,g2,i):
    return JS(Wi(i,g1.out_edges,g1.out_edges),_n(i,g2.in_edges))

"""
returns the balance : The extent to which two actors make the same choices can be expressed simply as the number of friends (outgoing choices) that they have in common:
"""    
def balance(g1,g2,i):
    res = 0.0
    for k in range(g1.number_of_nodes()):
        if g1.has_edge(i,k):
            #print _n(i,g1.out_edges)
            #print [e for e in _n(k,g2.out_edges) if e != i]
            #print JS(_n(i,g1.out_edges),[e for e in _n(k,g2.out_edges) if e != i])
            #print ""
            res += JS(_n(i,g1.out_edges),[e for e in _n(k,g2.out_edges) if e != i])
    if (len(_n(i,g1.out_edges))) == 0 :
        return 1.0
    return res*1.0/(len(_n(i,g1.out_edges)))       
        
    
"""
For each node in nodes calculates the multiplex metrics metric for graphs g1 and g2
Returns a dictionary with keys = nodes and values equal to the multiplex metric for the respective node
set nodes == "all" to calculate the metric for all nodes
"""    
def _getMetricForNodesMultiplex(g1,g2,metric=overlapIndex,nodes="all"):
    if nodes == "all":
        nodes = [i for i in range(g1.number_of_nodes())]
    res = {}
    for i in nodes:
        res[i] = metric(g1,g2,i)
    return res

    
metrics_dict_multiplex = {"Overlapping Index":overlapIndex,"Reciprocity":reciprocity,\
    "Transitivity Triplets":transTrip,"Three Cycles":threeCycles,"Balance":balance}

global_metrics_dict = {}

"""
Returns a dictionary with keys = nodes and values = metric for the respective nodes on graphs g1 and g2
"""
def getMetricMultiplex(g1,g2,metric="Overlapping index"):
    if metric in metrics_dict_multiplex:
        return _getMetricForNodesMultiplex(g1,g2,metrics_dict_multiplex[metric])
    else:
        print "ERROR metric:"+metric+" not implemented"
        return None

"""
Adds the metric as attribute to g1
The metric is calculated for all nodes in g1, using g1 and g2
"""
def addMetricAsAttributeMultiplex(g1,g2,metric):
    for_node = getMetricMultiplex(g1,g2,metric)
    l = [for_node[key] for key in range(g1.number_of_nodes())]
    s = getMetricString(metric,g1,g2)
    g1.graph[s] = l
    global_value = reduce(lambda x, y: x + y, l) / len(l)
    g1.graph["Global "+s] = global_value
        
"""
Adds a list of metrics as attributes to the nodes in the corresponding graphs
Each calculated on a pair of graphs (g1,g2) and is added as an attribute to graph1
if metrics == "all" then calculate all metrics for multiplex graphs
returns the set of graphs with added attributes
"""
def addMetricsAsAttributesMultiplex(graphs,graph_pairs,metrics="all"):
    if metrics == "all":
        metrics = [key for key in metrics_dict_multiplex]
    for metric in metrics:
        if metric in metrics_dict_multiplex:
            for g1,g2 in graph_pairs:
                addMetricAsAttributeMultiplex(graphs[g1],graphs[g2],metric)
    return graphs
    
def test():
    g1 = nx.DiGraph()
    g1.add_nodes_from(range(9))
    g1.add_edges_from([(0,1),(1,2),(1,3),(1,5),(4,5),(4,6),(0,7),(8,0),(1,7),(0,4)])
    g2 = nx.DiGraph()
    g2.add_nodes_from(range(9))
    g2.add_edges_from([(0,2),(0,5),(3,0),(0,4),(7,0)])
    for metric in metrics_dict_multiplex:
        print metric,getMetricMultiplex(g1,g2,metric)
        
    plt.subplot(1,2,1)
    nx.draw(g1,with_labels=True)
    plt.subplot(1,2,2)
    nx.draw(g2,with_labels=True)
    plt.show()
    
    
if __name__ == "__main__":
    test()