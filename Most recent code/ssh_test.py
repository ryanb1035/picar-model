import time
import paramiko as ssh
import stimuli
import visualizations
from time import sleep
import os

# Define essential parameters for SSHing into picar
host = "192.168.0.5"
username = "smlab-picar-dev"
password = "2mysore1lab"

# SSH into picar using paramiko library
client = ssh.client.SSHClient()
client.set_missing_host_key_policy(ssh.AutoAddPolicy())
client.connect(host, username=username, password=password)

# Method that runs a command on the picar and prints the output
def run_and_print(command):
    _stdin, _stdout, _stderr = client.exec_command(command)
    print(_stdout.read().decode())
    print(_stderr.read().decode())

# Method that takes the output of the picar's categorization, downloads it to the local computer, and returns its contents
def read_txt():
    # This block opens the client and downloads the output text of new_categorization to the local folder
    ftp_client = client.open_sftp()
    
    ### FIX REMOTE DIRECTORY
    ftp_client.get('Desktop//picar-dev//output.txt','output.txt')
    
    ftp_client.close()

    # This block opens output.txt on this computer and reads its lines
    # This just ends up being one line with two numbers representing both neuron outputs
    with open(os.getcwd()+'\\Most recent code\\output.txt', 'r') as file:
        # Read the single line
        line = file.readline().strip()

    # Split the line into two parts and convert them to floats from strings
    # This leads to a list of the two neuron output values
    numbers = [float(num) for num in line.split()]
    
    return numbers

# Current values represents the neuron output values at any point in time
# Since categorization hasn't been run yet these values are currently zero
current_values = [0,0]

for i in range(10):
    # This method call moves into the directory with the categorization program and runs it through SSH
    run_and_print("cd Desktop//picar-dev//new_categorization//; python new_categorization.py")

    # This method call creates and updates the stimulus program on the laptop
    stimuli.display_stimulus()

    #This method call creates and updates the vizualization program on the laptop
    stimuli.create_image_canvas()

    # The loop will run as long as the neuron values haven't changed, which means that the categorization program hasn't fully run yet
    while current_values.equal(read_txt()):
        # The GUI is updated so it remains visible during the loop
        stimuli.stimulus.update()
        stimuli.visualization.update()
    # When the loop ends, it means that the categorization program was fully ran
    # The new neuron values are recorded here
    current_values = read_txt()
    # Using these new values, and the values from the circles used in the stimulus progra, the values are all graphed
    visualizations.plot_data((stimuli.left_circle, current_values[0]),(stimuli.right_circle, current_values[1]))

client.close()