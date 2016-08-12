#### Goal 
To implement OSPFv2 on a 4 node topology in which the nodes emulate a router using Quagga Protocol stack. 

####  Topology 
We use the following topology for our experiment 

<img src="ospftopology.png" height="250">


### OSPFv2 : Open Shortest Path First
We are going to configure the above routers to run OSPFv2 protocol, which is a link state routing protocol based on Dijkstras algorithm. As described [here](https://en.wikipedia.org/wiki/Open_Shortest_Path_First)
> OSPF is perhaps the most widely used interior gateway protocol (IGP) in large enterprise networks.

Dijkstras algorithm is used to find shortest path from a node to all other nodes in the graph. Hence this algorithm is used in OSPF routing protocol to find shortest path from any given router to all the routers in  a network. When we use OSPF each router in a network builds its routing table based on the shortest path it has computed using Dijkstra's algorithm. OPSF routers build a topological database using all the link state advertisements and hello protocol, and this "topological database" serves as an input to the Dijkstras algorithm which then computes the shortest path. 


In our experiment we are going to build a single area OSPF network and observe the exchange of link state updates using wireshark. We will also purposefully make one of the router go down and see how the routing tables get updated. This is going to be fun experiment and a very good starting point to do more complex experiments so stay tuned.  

