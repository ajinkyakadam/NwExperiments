### Author : Ajinkya Kadam
### Date : 2nd September
'''
Step 2:
     Router BGP Configuration
        login to bgp daemon process
        login and privilged mode password
        hostname
        annonuce networks
        configure neighbor
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
    child = pexpect.spawn('telnet localhost 2604')
except pexpect.ExceptionPexpect:
    raise exceptions.NetworkException("Unable to spawn telnet process")
else:
    log_fileName = open('/tmp/routerBbgplog', 'w')
    child.logfile = log_fileName

    index1 = child.expect([r'.refused',r'Vty password is not set.','Password: '])
    print "index1 is ", index1
    if index1 == 0:
        print "Either quagga process is stoped , please run sudo /etc/init.d/quagga start"
    elif index1 == 1:
        print "Vty password not set. Please set vty password in file /etc/quagga/zebra.conf"
    elif index1 == 2:
        child.sendline('routerB')
        child.expect('.+>')

        ### Check if privilege mode password is set or not
        ###  if not then  only set the password or else
        ###   provide the password
        child.sendline('enable')
        index2 = child.expect(['Password: ','.+#'])

        if index2 == 0:
            child.sendline('routerB')
            child.expect('.+#')
            child.sendline('configure terminal')
        elif index2 == 1:
            child.sendline('configure terminal')
            child.expect('.+#')
            child.sendline('enable password routerB')
            child.expect('.+#')
        child.sendline('service password-encryption')
        child.expect('.+#')
        child.sendline('hostname routerB')
        child.expect('.+#')
        child.sendline('router bgp 65100')
        child.expect('.+#')
        child.sendline('network 10.1.3.0 mask 255.255.255.252')
        child.expect('.+#')
        child.sendline('neighbor 10.1.3.2 remote-as 65200')
        child.expect('.+#')
        child.sendline('neighbor 10.1.2.1 remote-as 65100')
        child.expect('.+#')
        child.sendline('neighbor 10.1.2.1 next-hop-self')
        child.expect('.+#')
        child.sendline('end')
        child.expect('.+#')
        child.sendline('clear ip bgp 10.1.4.2 soft out')
        child.expect('.+#')
        child.sendline('copy running-config startup-config')
        child.sendline('exit')
finally:
    child.close()
    log_fileName.close()
