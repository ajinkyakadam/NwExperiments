## Author : Ajinkya Kadam
## Script to setup quagga and install some required modules. 

sudo apt-get update
sudo apt-get install -y vim 
sudo apt-get install -y python-pip
sudo pip install pexpect
sudo apt-get install -y quagga 
echo "net.ipv4.conf.all.forwarding=1" | sudo tee -a /etc/sysctl.conf 
echo "net.ipv4.conf.default.forwarding=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p 
sudo touch /etc/quagga/bgpd.conf 
sudo touch /etc/quagga/vtysh.conf 
sudo touch /etc/quagga/zebra.conf 

sudo chown quagga:quaggavty /etc/quagga/vtysh.conf && sudo chmod 660 /etc/quagga/vtysh.conf 
sudo chown quagga:quagga /etc/quagga/zebra.conf && sudo chmod 640 /etc/quagga/zebra.conf 
sudo chown quagga:quagga /etc/quagga/bgpd.conf && sudo chmod 640 /etc/quagga/bgpd.conf



