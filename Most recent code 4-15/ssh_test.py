import paramiko

host = "192.168.0.5"
username = "smlab-picar-dev"
password = "2mysore1lab"

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)

def run_and_print(command):
    _stdin, _stdout, _stderr = client.exec_command(command)
    print(_stdout.read().decode())
    print(_stderr.read().decode())

for i in range(1):
    run_and_print("cd Desktop//picar-dev//new_categorization//; python new_categorization.py")

client.close()