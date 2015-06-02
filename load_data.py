import os,sys,random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def load_4_layers(dataset="wan",aggregated=False):
    path = "data\\wan.csv"
    if dataset == "bms":
        path = "data\\bms.csv"
    node_mapping = {}
    count = 0
    graphs = [nx.DiGraph(),nx.DiGraph(),nx.DiGraph(),nx.DiGraph(),nx.DiGraph(),nx.DiGraph(),nx.DiGraph()]
    descr = ["strong real","weak real","strong facebook","weak facebook","real","facebook","aggregated"]
    with open(path,"r") as f:
        for line in f:
            s_line = line.split(",")
            from_node = int(s_line[0])
            to_node = int(s_line[2])
            layer = int(s_line[1])
            count = _addNode(from_node,node_mapping,count,graphs)
            count = _addNode(to_node,node_mapping,count,graphs)
            graphs[layer-1].add_edge(node_mapping[from_node],node_mapping[to_node])
            if layer < 3:
                graphs[4].add_edge(node_mapping[from_node],node_mapping[to_node])
            else:
                graphs[5].add_edge(node_mapping[from_node],node_mapping[to_node])
            graphs[6].add_edge(node_mapping[from_node],node_mapping[to_node])
    for i in range(len(graphs)):
        graphs[i].graph["title"] = dataset+" "+descr[i]
    res = graphs
    graphs = [res[0],res[1],res[4],res[2],res[3],res[5],res[6]]
    return (graphs,node_mapping)
    
def _addNode(node,node_mapping,count,graphs):
    if not node in node_mapping:
        node_mapping[node] = count
        for graph in graphs:
            graph.add_node(count)
        count += 1
    return count
    
def getTestGraph1():
    g = nx.DiGraph()
    for i in range(14):
        g.add_node(i)
    edges = [(0,1),(0,2),(2,1),(3,4),(4,5),(5,3),(6,7),(7,8),(6,8),(6,9),(9,8),(10,11),(11,10),(10,12),(12,11),(3,13),(13,5)]
    for i,j in edges:
        g.add_edge(i,j)
    return g
    
def getTestGraph2():
    g = nx.DiGraph()
    for i in range(8):
        g.add_node(i)
    edges = [(0,1),(0,2),(0,3),(1,3),(3,1),(2,1),(2,3),(3,2),(4,5),(4,6),(4,7),(7,6)]
    for i,j in edges:
        g.add_edge(i,j)
    return g
       
def main():
    graphs,node_mapping = load_4_layers()
    drawGraphs(graphs)
    
if __name__ == "__main__":
    main()
    