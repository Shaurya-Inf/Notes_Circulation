import networkx as nx
import itertools
import sys
import pandas as pd

x = pd.read_csv('data_orig.csv', header=None, skiprows=1)

G = nx.DiGraph()

for index, row in x.iterrows():
    source_node = str(row[0])
    attached_nodes=[]
    for i in range(1, len(row)):
        if str(row[i]) != 'nan' and str(row[i]) != str(row[0]):
           attached_nodes.append(str(row[i]))

    for i in attached_nodes:
        G.add_edge(source_node, i)

def calculate_path_length(shortest_path_lengths, path):
    length = 0
    for i in range(len(path) - 1):
        length += shortest_path_lengths[path[i]][path[i+1]]
    return length

def path_of_length(start, end, length, current_length=0, path=[]):
        if current_length == length:
            if start == end:
                return path 
            else:
                return None

        for neighbor in G.successors(start):
            if neighbor not in path:
                new_path =path_of_length(neighbor, end, length, current_length + 1, path + [start])
                if new_path:
                    return new_path

        return None

def travelling_salesman(graph, source_node, selected_nodes):
    shortest_path = []
    shortest_length = float('inf')
    nodes = list(graph.nodes())
    selected_nodes.append(source_node)
    shortest_path_lengths = dict(nx.all_pairs_dijkstra_path_length(graph))  
    for i in selected_nodes:
        a=len(list(G.successors(i)))
        if a==0:
            print(i, " doesn't point to any other node. Hence, it is not possible to make a cycle passing through it.")
            sys.exit()

    for i in itertools.permutations(selected_nodes):
        path = list(i) + [source_node]
        if path[0] == source_node:
            length = calculate_path_length(shortest_path_lengths, path)
            if length < shortest_length:
                shortest_length = length
                shortest_path = path

    l_nodes=[]            
    for i in range(len(shortest_path)-1):
        a=shortest_path[i]
        b=shortest_path[i+1]
        lgt=shortest_path_lengths[a][b]
        l_nodes.append(path_of_length(a,b,lgt))
    l_nodes_final=[]
    for i in l_nodes:
        l_nodes_final.extend(i)
    l_nodes_final.append(source_node)    
    return  shortest_length, l_nodes_final

selected_nodes = []
print("Enter only those nodes which are present in the graph")
source_node =input("Enter the source node: ")
k = int(input("Enter the number of nodes to visit (excluding the source node): "))
for i in range(k):
    selected_nodes.append(input("Enter the node: "))

shortest_length,l_nodes = travelling_salesman(G, source_node, selected_nodes)
print("Shortest Length:", shortest_length)
print("Path followed:",l_nodes)