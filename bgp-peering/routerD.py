### Author : Ajinkya Kadam
### Date : 2nd September
'''
Step 1:
     Router Configuration
        login to router daemon process
        hostname
        login and privilged mode password
        interface adresss
'''
try:
    import pexpect
except:
    ImportError, "Pexpect module is missing, please install the module"

try:
    import re
    import os
except ImportError:
    raise ImportError, "Exception occured when importing re and os module"

try:
    child = pexpect.spawn('telnet localhost 2601')
except pexpect.ExceptionPexpect:
    raise exceptions.NetworkException("Unable to spawn telnet process")
else:
    log_fileName = open('/tmp/routerDlog', 'w')
    child.logfile = log_fileName

    index1 = child.expect([r'.refused',r'Vty password is not set.','Password: '])
    print "index1 is ", index1
    if index1 == 0:
        print "Either quagga process is stoped , please run sudo /etc/init.d/quagga start"
    elif index1 == 1:
        print "Vty password not set. Please set vty password in file /etc/quagga/zebra.conf"
    elif index1 == 2:
        child.sendline('routerD')
        child.expect('.+>')

        ### Check if privilege mode password is set or not
        ###  if not then  only set the password or else
        ###   provide the password
        child.sendline('enable')
        index2 = child.expect(['Password: ','.+#'])

        if index2 == 0:
            child.sendline('routerD')
            child.expect('.+#')
            child.sendline('configure terminal')
        elif index2 == 1:
            child.sendline('configure terminal')
            child.expect('.+#')
            child.sendline('enable password routerD')
            child.expect('.+#')

        child.sendline('service password-encryption')
        child.expect('.+#')
        child.sendline('hostname routerD')
        child.expect('.+#')

        ## get interface name
        iface1 = re.search(r'e\w+\d',os.popen('ip addr | grep "10.1.4.2"').read()).group()
        iface2 = re.search(r'e\w+\d',os.popen('ip addr | grep "10.1.5.2"').read()).group()
        child.sendline('interface '+iface1)
        child.expect('.+#')
        child.sendline('description Interface connected to router C which is iBGP peer')
        child.expect('.+#')
        child.sendline('ip address 10.1.4.2/30')
        child.expect('.+#')
        child.sendline('interface '+iface2)
        child.expect('.+#')
        child.sendline('description Interface connected to host 2 ')
        child.expect('.+#')
        child.sendline('ip address 10.1.5.2/30')
        child.expect('[\w()-]#')
        child.sendline('exit')
        child.expect('.+#')
        child.sendline('exit')
        child.expect('.+#')
        child.sendline('copy running-config startup-config')
finally:
    child.close()
    log_fileName.close()
