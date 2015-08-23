import os,sys,random
import networkx as nx
import numpy as np
from compute_metrics_single_graph import *
from compute_metrics_multiplex import *
from load_data import *

save_fig_size = (25, 20)
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
        
prev_pos = None     

def histogramMetricSingle(dataset="wan",save_to_file=True):
    graphs,node_mapping = load_4_layers(dataset)
    graph_pairs = [(i,i) for i in range(len(graphs))]
    addMetricsAsAttributesMultiplex(graphs,graph_pairs)
    metrics = {"Reciprocity":reciprocity,"tp1":tp1,"tp2":tp2,"tc1":tc1,"tc2":tc2}
    addMetricsAsAttributesMultiplex(graphs,graph_pairs,metrics)
    
    for metric in metrics:
    
        if save_to_file: 
            plt.figure(num=None, figsize=save_fig_size, dpi=save_fig_dpi)
        else:
            plt.figure()
        i = 1
        plt.suptitle(dataset+" "+metric, fontsize=36)
        for g1,g2 in graph_pairs:
            graph = graphs[g1]
            title = graphs[g1].graph["title"][4:]
            values = np.array(graph.graph[getMetricString(metric,graphs[g1],graphs[g2])])
            weights = np.ones_like(values)/len(values)
            plt.subplot(3,3,i)
            # the histogram of the data
            n, bins, patches = plt.hist(values, 20, facecolor='g', alpha=0.75,weights=weights)
            plt.title(title, fontsize=26)
            plt.xlim([0.0,1.0])
            plt.ylim([0.0,max(n)*1.2])
            plt.grid(True)
            plt.xlabel(metric, fontsize=22)
            plt.ylabel('Fraction of nodes', fontsize=22)
            plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
            i += 1
        if save_to_file:
            plt.savefig(dataset+"_"+metric+'_hist.png')
        else:
            plt.show()
    
    
    
def histogramMetricMultiplex(dataset="wan",metric="Overlapping index",save_to_file=False):
    graphs,node_mapping = load_4_layers(dataset)
    graph_pairs = graph_combinations+[(g2,g1) for g1,g2 in graph_combinations]+[(i,i) for i in range(len(graphs))]
    addMetricsAsAttributesMultiplex(graphs,graph_pairs)
    if save_to_file: 
        plt.figure(num=None, figsize=save_fig_size, dpi=save_fig_dpi)
    else:
        plt.figure()
    plt.suptitle(dataset+" "+metric)
    
    i = 1
    for g1,g2 in graph_pairs:
        graph = graphs[g1]
        title = graphs[g1].graph["title"][4:]+"->"+graphs[g2].graph["title"][4:]
        values = np.array(graph.graph[getMetricString(metric,graphs[g1],graphs[g2])])
        weights = np.ones_like(values)/len(values)
        plt.subplot(5,6,i)
        # the histogram of the data
        n, bins, patches = plt.hist(values, 20, facecolor='g', alpha=0.75,weights=weights)
        plt.title(title)
        plt.xlim([0.0,1.0])
        plt.ylim([0.0,max(n)*1.2])
        plt.grid(True)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        i += 1
    if save_to_file:
        plt.savefig(dataset+"_"+metric+'_hist.png')
    else:
        plt.show()
        
def visualizeMetricMutliplex(dataset="wan",metric="Overlapping index",save_to_file=False,min_size=10,max_size=60):
    global prev_pos
    graphs,node_mapping = load_4_layers(dataset)
    graph_pairs = graph_combinations+[(g2,g1) for g1,g2 in graph_combinations]+[(i,i) for i in range(len(graphs))]
    addMetricsAsAttributesMultiplex(graphs,graph_pairs)
    if save_to_file: 
        plt.figure(num=None, figsize=save_fig_size, dpi=save_fig_dpi)
    else:
        plt.figure()
    plt.suptitle(dataset)
    if prev_pos is None:
        pos = nx.spring_layout(graphs[8],iterations=7,k=.25)
        prev_pos = pos
    else:
        pos = prev_pos
    max_weight = -100000
    min_weight = 100000
    
    for g1,g2 in graph_pairs:
        graph = graphs[g1]
        color_attribute = getMetricString(metric,graphs[g1],graphs[g2])
        
        node_weights = np.array(graph.graph[color_attribute])
        avg_weight = sum(node_weights)*1.0/node_weights.size
        node_weights[node_weights>avg_weight*2] = avg_weight*2
        max_weight = max(max_weight,max(node_weights)*1.0)
        min_weight = min(min_weight,min(node_weights)*1.0)
        
    i = 1    
    for g1,g2 in graph_pairs:
        graph = graphs[g1]
        color_attribute = getMetricString(metric,graphs[g1],graphs[g2])
        plt.subplot(5,6,i)
        node_weights = np.array(graph.graph[color_attribute])
        avg_weight = sum(node_weights)*1.0/node_weights.size
        node_weights[node_weights>avg_weight*2] = avg_weight*2
        
        node_sizes = min_size+(node_weights-min_weight)/(max_weight-min_weight)*(max_size-min_size)
        nx.draw(graph,pos,node_size=node_sizes,edgelist=[],node_color=graph.graph[color_attribute])
        nx.draw_networkx_edges(graph,pos,alpha=0.1,arrows=False,edge_color =[[.6,.6,.6]]*graph.number_of_edges())
        i += 1
        plt.title(color_attribute)
        
    if save_to_file:
        plt.savefig(dataset+"_"+metric+'.png')
    else:
        plt.show()

def getSubplotRowsAndCols(number_of_subplots):
    rows,cols = 1,2
    if number_of_subplots > 16:
        rows,cols = 5,4
    else:  
        if number_of_subplots > 12:
            rows,cols = 4,4
        else:
            if number_of_subplots > 8:
                rows,cols = 3,4
            else:
                if number_of_subplots > 6:
                    rows,cols = 2,4
                else:
                    if number_of_subplots > 4:
                        rows,cols = 2,3
                    else:
                        rows,cols = 2,2
    return rows,cols
        
def visualizeAllMetricsForGraphs(dataset="wan",network="real",metrics="all",save_to_file=False,min_size=10,max_size=100):
    if metrics == "all":
        metrics = []
        for key in metrics_dict:
            metrics.append(key)
    graphs,node_mapping = load_4_layers(dataset)
    graphs = addMetricsAsAttributes(graphs,metrics)
    
    if network == "both":
        rows,cols = getSubplotRowsAndCols(2*len(metrics))
    else:
        rows,cols = getSubplotRowsAndCols(len(metrics))
    
    i = 1
    if save_to_file: 
        plt.figure(num=None, figsize=save_fig_size, dpi=save_fig_dpi)
    else:
        plt.figure()
    plt.suptitle(dataset)
    pos = nx.spring_layout(graphs[6],iterations=7,k=.3)
    if network == "real":
        graph_idxs = [2]
    else:
        if network == "both":
            graph_idxs = [2,5]        
        else:
            graph_idxs = [5]
    for color_attribute in metrics:
        k = "real"
        for graph in [graphs[idx] for idx in graph_idxs]:
            plt.subplot(rows,cols,i)
            node_weights = np.array(graph.graph[color_attribute])
            avg_weight = sum(node_weights)*1.0/node_weights.size
            node_weights[node_weights>avg_weight*2] = avg_weight*2
            max_weight = max(node_weights)*1.0
            min_weight = min(node_weights)*1.0
            
            print avg_weight,max_weight,min_weight
            node_sizes = min_size+(node_weights-min_weight)/(max_weight-min_weight)*(max_size-min_size)
            nx.draw(graph,pos,node_size=node_sizes,edgelist=[],node_color=graph.graph[color_attribute])
            nx.draw_networkx_edges(graph,pos,alpha=0.1,arrows=False,edge_color =[[.6,.6,.6]]*graph.number_of_edges())
            i += 1
            if not network == "both":
                k = network
            plt.title(color_attribute+" "+k)
            k = "facebook"
    if save_to_file:
        plt.savefig(dataset+"_"+network+'.png')
    else:
        plt.show()
        
        
def drawGraphs(graphs,color_attribute=None,aggregated=False,save_to_file=False,min_size=10,max_size=100):
    if save_to_file:
        plt.figure(num=None, figsize=save_fig_size, dpi=save_fig_dpi)
    if not color_attribute is None:
        plt.suptitle(color_attribute)
    pos = nx.spring_layout(graphs[6],iterations=7,k=.3)
    i = 1
    for graph in graphs:
        plt.subplot(3,3,i)           
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
        if not aggregated and i > 7:
            break
    if save_to_file:
        plt.savefig('{0}_{1}_{2}.png'.format(graphs[0].graph['title'][:3],color_attribute,str(aggregated)))
    else:
        plt.show()

histogramMetricSingle("bms")
        