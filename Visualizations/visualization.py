import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def simulate_trial(n_steps):
    # Simulate outcomes (True for correct, False for incorrect)
    outcomes = np.random.choice([True, False], size=n_steps)
    
    # Calculate cumulative accuracy: proportion of Trues up to each step
    cumulative_accuracies = np.cumsum(outcomes) / (np.arange(n_steps) + 1)
    
    return outcomes, cumulative_accuracies

# Number of steps for each trial
n_steps = 100

# Simulate three trials
trial_data = [simulate_trial(n_steps) for _ in range(3)]

# Set up the figure and subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 15))

# Setting up lines for each trial on its subplot, we'll animate these lines
lines = [ax.plot([], [], label=f'Trial {i+1}')[0] for i, ax in enumerate(axs)]

for ax in axs:
    ax.set_xlim(0, n_steps)
    ax.set_ylim(0, 1)
    ax.legend()
    ax.set_xlabel('Steps')
    ax.set_ylabel('Cumulative Accuracy')

# Initialization function: plot the background of each frame
def init():
    for line in lines:
        line.set_data([], [])
    return lines

# Animation function: this is called sequentially
def animate(i):
    for line, data in zip(lines, trial_data):
        x = np.arange(1, i+2)
        y = data[1][:i+1]  # Cumulative accuracies
        line.set_data(x, y)
    return lines

# Call the animator
anim = FuncAnimation(fig, animate, init_func=init, frames=n_steps, interval=100, blit=True)

plt.show()