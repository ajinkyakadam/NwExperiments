### Author : Ajinkya Kadam
### Date : 24th August
'''
As paramiko doesn't help with telnet,
we will be using pexpect module available
in python for the router configuration.
We have two steps in router configuration
Step 1:
     Router Configuration
        login to router daemon process
        hostname
        login and privilged mode password
        interface adresss
        Add banner
Step 2:
     OSPF Configuration
        login to ospf daemon router process
        router ospf process
        network announcements
'''
try:
    import pexpect
except:
    ImportError, "Pexpect module is missing, please install the module"

import sys

try:
     child = pexpect.spawn('telnet localhost 2601')
except pexpect.ExceptionPexpect:
     raise exceptions.NetworkException("Unable to spawn telnet process")
else:
    clog_fileName = open('/tmp/router4log', 'w')
    child.logfile = log_fileName

    index1 = child.expect([r'.refused',r'Vty password is not set.','Password: '])
    print "index1 is ", index1
    if index1 == 0:
        print "Either quagga process is stoped , please run sudo /etc/init.d/quagga start"
    elif index1 == 1:
        print "Vty password not set. Please set vty password in file /etc/quagga/zebra.conf"
    elif index1 == 2:
        child.sendline('router4')
        child.expect('.+>')

        ### Check if privilege mode password is set or not
        ###  if not then  only set the password or else
        ###   provide the password
        child.sendline('enable')
        index2 = child.expect(['Password: ','.+#'])

        if index2 == 0:
            child.sendline('router4')
            child.expect('.+#')
            child.sendline('configure terminal')
        elif index2 == 1:
            child.sendline('configure terminal')
            child.expect('.+#')
            child.sendline('enable password router4')
            child.expect('.+#')

        child.sendline('service password-encryption')
        child.expect('.+#')
        child.sendline('hostname router4')
        child.expect('.+#')
        child.sendline('interface eth1')
        child.expect('.+#')
        child.sendline('description Interface connected to router2')
        child.expect('.+#')
        child.sendline('ip address 192.168.1.18/30')
        child.expect('.+#')
        child.sendline('interface eth2')
        child.expect('.+#')
        child.sendline('description Interface connected to router3')
        child.expect('.+#')
        child.sendline('ip address 192.168.1.13/30')
        child.expect('.+#')
        child.sendline('interface eth3')
        child.expect('.+#')
        child.sendline('description Interface connected to router1')
        child.expect('.+#')
        child.sendline('ip address 192.168.1.2/30')
        child.expect('[\w()-]#')
        child.sendline('exit')
        child.expect('.+#')
        child.sendline('exit')
        child.expect('.+#')
        child.sendline('copy running-config startup-config')
finally:
    child.close()
    log_fileName.close()
