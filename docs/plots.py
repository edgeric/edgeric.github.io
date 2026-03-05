import matplotlib.pyplot as plt

# Define the new X and Y axes values
percentages = ["40%", "50%", "60%", "70%", "80%", "90%"]
scenarios = ["Scenario1", "Scenario2", "Scenario3", "Scenario4", "Scenario5", "Scenario6"]

# Create a figure with four subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Subplot 1 - Normal plot (crosses diagonally, ticks elsewhere)
for i in range(len(scenarios)):
    for j in range(len(percentages)):
        if i == j:
            axs[0, 0].scatter(percentages[j], scenarios[i], marker='x', color='red')
        else:
            axs[0, 0].scatter(percentages[j], scenarios[i], marker='P', color='blue')
axs[0, 0].set_xlabel("% of High Action Throughput")
axs[0, 0].set_title("EMBB Capacity")

# Subplot 2 - Special plot (crosses in the first row, ticks elsewhere)
for i in range(len(scenarios)):
    for j in range(len(percentages)):
        if i == 0:
            axs[0, 1].scatter(percentages[j], scenarios[i], marker='x', color='red')
        else:
            axs[0, 1].scatter(percentages[j], scenarios[i], marker='P', color='blue')
axs[0, 1].set_xlabel("% of High Action Throughput")
axs[0, 1].set_title("XR Capacity")

# Subplots 3 and 4 - Repeat the normal plot configuration
for i in range(len(scenarios)):
    for j in range(len(percentages)):
        if i == j:
            axs[1, 0].scatter(percentages[j], scenarios[i], marker='x', color='red')
            axs[1, 1].scatter(percentages[j], scenarios[i], marker='x', color='red')
        else:
            axs[1, 0].scatter(percentages[j], scenarios[i], marker='P', color='blue')
            axs[1, 1].scatter(percentages[j], scenarios[i], marker='P', color='blue')
axs[1, 0].set_xlabel("% of High Action Throughput")
axs[1, 0].set_title("EMBB Capacity")
axs[1, 1].set_xlabel("% of High Action Throughput")
axs[1, 1].set_title("EMBB Capacity")

# Adjust layout
plt.tight_layout()

# Show the updated plot
plt.show()
fig.savefig("/Users/ushasighosh/Downloads/project_edgerix/docs/capacity.pdf")



