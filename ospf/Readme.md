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

#### Install Quagga 

I am using the guidelines given [here](https://wiki.ubuntu.com/JonathanFerguson/Quagga) to install Quagga, however I will be making some changes to the configuration as per our experiment. On the machines we will be only running Zebra and Ospfd daemon. All other protocol daemons will be disabled. 

Please follow the below instructions 

    sudo apt-get install quagga 

Now lets enable IPv4 forwarding as we need IPV4 support only for OSPFv2 

    echo "net.ipv4.conf.all.forwarding=1" | sudo tee -a /etc/sysctl.conf 
    echo "net.ipv4.conf.default.forwarding=1" | sudo tee -a /etc/sysctl.conf

Then do, 

    sudo sysctl -p 

Lets create the configuration files. You may use a different editor to create those files like vim, gedit.  

    sudo nano /etc/quagga/ospfd.conf 
    sudo nano /etc/quagga/vtysh.conf 
    sudo nano /etc/quagga/zebra.conf 
    
Now lets change the permission of those configuration files 
    
    sudo chown quagga:quaggavty /etc/quagga/vtysh.conf && sudo chmod 660 /etc/quagga/vtysh.conf 
    sudo chown quagga:quagga /etc/quagga/zebra.conf && sudo chmod 640 /etc/quagga/zebra.conf 
    sudo chown quagga:quagga /etc/quagga/ospfd.conf && sudo chmod 640 /etc/quagga/ospfd.conf

By default all routing protocols are disabled in the file /etc/quagga/daemons, so we will need to enable those daemons that we need for this experiment. 

    sudo vim /etc/quagga/daemons

and then replace 

    zebra=no
    ospfd=no
with 

    zebra=yes
    ospfd=yes

Now we will restart the daemon, by running

    sudo /etc/init.d/quagga restart 

You will get the following output at your terminal 

    Stopping Quagga daemons (prio:0): (ospfd) (zebra) (bgpd) (ripd) (ripngd) (ospf6d) (isisd).
    Removing all routes made by zebra.
    Loading capability module if not yet done.
    Starting Quagga daemons (prio:10): zebra ospfd.

From the above output you may confirm that we have started the zebra daemon and ospfd daemon successfully. 


#### Configure Router 1
In order to configure router 1 via the virtual terminal interface we first need to set the virtual terminal password in the zebra daemon. So please add the following lines in the file `/etc/quagga/zebra.conf`
```
hostname Router1
password router1
enable password router1
service password-encryption
log stdout
```

after adding the above lines please **save** the file and then run. 

    sudo /etc/init.d/quagga restart 

Now if you do 

    telnet localhost 2601

you will see the virtual terminal interface, as follows and it will prompt for the password. Provide the passsword you set above after which we will configure the router1. 

If you run `show run` in priviledged mode, you can see the current configuration as 
```
username@router1:~$ telnet localhost 2601
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.

Hello, this is Quagga (version 0.99.20.1).
Copyright 1996-2005 Kunihiro Ishiguro, et al.


User Access Verification

Password: 
Router1> enable
Password: 
Router1# show run

Current configuration:
!
hostname Router1
password 8 nkf3Ra2uYS0YY
enable password 8 3kGy.r3/e2OCA
log stdout
service password-encryption
!
```

Its easy to see that our passwords are encrypted because of `service password-encryption` command. Similarly you can configure remaining 3 routers and verify if your configuration has been added.  
