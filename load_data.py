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
       
    
def drawGraphs(graphs,color_attribute=None,aggregated=False,save_to_file=False,min_size=10,max_size=100):
    if save_to_file:
        plt.figure(num=None, figsize=(15, 10), dpi=150)
    if not color_attribute is None:
        plt.suptitle(color_attribute)
    pos = nx.spring_layout(graphs[6],iterations=7,k=.3)
    i = 1
    for graph in graphs:
        if aggregated:
            plt.subplot(3,3,i)
        else:
            plt.subplot(2,3,i)            
        if color_attribute == None:
            nx.draw(graph,pos,node_size=10,edgelist=[])
        else:
            node_weights = np.array(graph.graph[color_attribute])
            max_weight = max(node_weights)*1.0
            min_weight = min(node_weights)*1.0
            node_sizes = min_size+(node_weights-min_weight)/(max_weight-min_weight)*(max_size-min_size)
            nx.draw(graph,pos,node_size=node_sizes,edgelist=[],node_color=graph.graph[color_attribute])
        nx.draw_networkx_edges(graph,pos,alpha=0.1,arrows=False,edge_color =[[.6,.6,.6]]*graph.number_of_edges())
        #nx.draw_networkx_labels(graph,pos,{i:str(i) for i in range(graph.number_of_nodes())},font_size=16)
        plt.title(graph.graph["title"])
        i += 1
        if not aggregated and i > 6:
            break
    if save_to_file:
        plt.savefig('{0}_{1}_{2}.png'.format(graphs[0].graph['title'][:3],color_attribute,str(aggregated)))
    else:
        plt.show()


def main():
    graphs,node_mapping = load_4_layers()
    drawGraphs(graphs)
    
if __name__ == "__main__":
    main()
    