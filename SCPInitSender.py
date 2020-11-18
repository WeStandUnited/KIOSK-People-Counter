from paramiko import SSHClient
from scp import SCPClient
import os


def sendPhoto(pin,username,host):
    ssh = SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(host, username=username)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(pin+".jpeg", '/home/'+username+'/csc380/'+pin+".jpeg")# second parameter is what the name of the sent file is


def sendVideo(videoname,username,host,directory):
    ssh = SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(host, username=username)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(directory+videoname+".avi")




sendPhoto("test4.jpeg",'cchiass2','pi.cs.oswego.edu')