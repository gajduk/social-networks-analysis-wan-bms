import os,sys,random
import networkx as nx
import numpy as np
from compute_metrics import *
from load_data import *

save_fig_size = (15, 10)
save_fig_dpi = 150

def scatterPlotForMetrics(g1,g2,attribute):
    x = g1.graph[attribute]
    y = g2.graph[attribute]
    plt.scatter(x,y)
    plt.plot([min(x+y),max(x+y)],[min(x+y),max(x+y)],'k-',lw=2)
    plt.xlabel(g1.graph["title"])
    plt.ylabel(g2.graph["title"])
    plt.xlim(min(x+y),max(x+y))
    plt.ylim(min(x+y),max(x+y))
    plt.title(attribute)

def visualizeMetrics(dataset="wan",metrics="all",save_to_file=False):
    if metrics == "all":
        metrics = []
        for key in metrics_dict:
            metrics.append(key)
    graphs,node_mapping = load_4_layers(dataset)
    graphs = addMetricsAsAttributes(graphs,metrics)
    i = 1
    if save_to_file: 
        plt.figure(num=None, figsize=save_fig_size, dpi=save_fig_dpi)
    else:
        plt.figure()
    for metric in metrics:
        plt.subplot(3,3,i)
        scatterPlotForMetrics(graphs[2],graphs[5],metric)
        i += 1
    if save_to_file:
        plt.savefig(dataset+'.png')
    else:
        plt.show()
    for key in metrics:
        plt.figure()
        drawGraphs(graphs,key,False,save_to_file)
        
def drawGraphs(graphs,color_attribute=None,aggregated=False,save_to_file=False,min_size=10,max_size=100):
    if save_to_file:
        plt.figure(num=None, figsize=save_fig_size, dpi=save_fig_dpi)
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
        
        plt.title(graph.graph["title"])
        i += 1
        if not aggregated and i > 6:
            break
    if save_to_file:
        plt.savefig('{0}_{1}_{2}.png'.format(graphs[0].graph['title'][:3],color_attribute,str(aggregated)))
    else:
        plt.show()

        