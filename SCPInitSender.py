from paramiko import SSHClient
from scp import SCPClient
import os


def sendFile(pin,username,host):
    ssh = SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(host, username=username)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(pin+".jpeg", '/home/'+username+'/staging/'+pin+".jpeg")# second parameter is what the name of the sent file is


sendFile("PLACEHOLDER",'USERNAME','pi.cs.oswego.edu')