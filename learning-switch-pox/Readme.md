### Implementing a Learning Switch and Adding a Flow Entry if destination MAC is known using POX

In order to start with the basics, I am using this 
[tutorial](https://github.com/mininet/openflow-tutorial/wiki/Create-a-Learning-Switch) as it is a great starting point. 
Basic hub like functionality is provided in `pox/misc/of_tutorial.py` file where the switch forwards any packet it receives 
to all the ports except on which it received the packet. To build on it we need to create a learning switch which learns the
port number from the source mac address, so if for future reference there is packet containting the source mac address 
which is previously learnt and added to the mac-table then we just forward the packet to the corresponding output port. 


Here is the topology, which we create using mininet. 

<img src="learningSwitch.png" height="300">

To create above topology use 
```
 sudo mn --topo single,3 --mac --switch ovsk --controller remote
```
Now lets add the port learning behavior. We add the following code to the method `act_like_switch`

```
# Get the source and destination MAC, and also the input port 
# for a given packet
	
src_mac_addr = str(packet.src)
dst_mac_addr = str(packet.dst)
input_port = packet_in.in_port
       
## Add the source MAC to the correpsonding input port 

if src_mac_addr not in self.mac_to_port:
	 self.mac_to_port[src_mac_addr] = input_port
```
What the above code does is that it stores the input port to source mac address like a key value pair in a dictionary named `mac_to_port`. 
