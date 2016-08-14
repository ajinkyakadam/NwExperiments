### Implementing a Learning Switch and Adding a Flow Entry if destination MAC is known using POX

In order to start with the basics, I am using this 
[tutorial](https://github.com/mininet/openflow-tutorial/wiki/Create-a-Learning-Switch) as it is a great starting point. 
Basic hub like functionality is provided in `pox/misc/of_tutorial.py` file where the switch forwards any packet it receives 
to all the ports except on which it received the packet. To build on it we need to create a learning switch which learns the
port number from the source mac address, so if for future reference there is packet containting the source mac address 
which is previously learnt and added to the mac-table then we just forward the packet to the corresponding output port. 
