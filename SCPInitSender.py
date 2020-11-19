from paramiko import SSHClient
from scp import SCPClient
import os

'''
SendFile uses SCP to send file over network to another host

varibles:
local_file- (str) that is the file location of the file you want to send on your local machine

username - (str) username of account on server. NOTE: must have RSA key between server and your local machine

server_local - (str) location on server you want the file NOTE: include the file you are sending

eg :  
server_local = "/home/myPC/video/file.mp3"
username = "user"
server_local = "/home/user/video/file.mp3"

'''
def sendFile(local_file,username,host,server_local):
    ssh = SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(host, username=username)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(local_file,server_local)





