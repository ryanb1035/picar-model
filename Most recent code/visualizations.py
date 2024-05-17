import matplotlib.pyplot as plt
import os

# Global list to store previous datasets
previous_data = []

def plot_data(current_data):
    # Add the current data to the list of previous datasets
    previous_data.append(current_data)
    
    # Set up the plot
    plt.figure(figsize=(10, 6))
    
    # Plot each dataset with a different color
    for i, data in enumerate(previous_data):
        # Unpack the stimulus and response values
        stimuli, responses = (zip(*data))
        plt.scatter(stimuli, responses, color='black', label=f'Set {i+1}')

    # Adding labels and title
    plt.xlabel('Stimulus Strength')
    plt.ylabel('Neuron Response')
    plt.title('Neuron Response to Stimulus')
    plt.legend()

    # Save the figure as an image file
    plt.savefig(os.getcwd()+'\\Most recent code\\images\\plot.png')
    plt.close()  # Close the plotting window to free up resources