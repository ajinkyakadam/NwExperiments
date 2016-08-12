### Author : Ajinkya Kadam
### Date : 12th August


try:
    import networkx as nx
except:
    print "Unabale to import networkx module, please install networkx module"

try:
   import matplotlib.pyplot as plt
except:
   print "Unable to import matlplotlib module, please install matplotlib module"


## Create Graph 

g = nx.Graph()

## Add 4 nodes to graph 
for i in range(1,5):
    g.add_node(i)


## Add Edges
edge_list = [(1,4),(1,2),(2,4),(4,3),(2,3)]

g.add_edges_from(edge_list)


## Add labels to each node 
node_label = {}

node_label[1]='Router 1'

node_label[2]='Router 2'

node_label[3]='Router 3'

node_label[4]='Router 4'


## Draw Graph 

nx.draw(g,labels=node_label,with_labels=True,node_size=3500,node_color='w')
plt.show()
plt.savefig("ospftopology.png")




