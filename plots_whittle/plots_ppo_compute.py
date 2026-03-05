import numpy as np
import matplotlib.pyplot as plt
plt.figure(figsize=(6, 4))
# Step 1: Read data from a text file
file_path = '5ue_policy_time.txt'  # Change this to the path of your text file
with open(file_path, 'r') as file:
    data = file.readlines()
    data = [float(line.strip()) for line in data]  # Convert each line into a float

# Step 2: Calculate the CDF
data_sorted = np.sort(data)
cdf = np.arange(1, len(data_sorted)+1) / len(data_sorted)
plt.plot(data_sorted, cdf)
# Step 3: Plot the CDF

# Step 1: Read data from a text file
file_path = '10ue_policy_time.txt'  # Change this to the path of your text file
with open(file_path, 'r') as file:
    data = file.readlines() 
    data = [float(line.strip()) for line in data] + [25]  # Convert each line into a float

# Step 2: Calculate the CDF
data_sorted = np.sort(data)
cdf = np.arange(1, len(data_sorted)+1) / len(data_sorted)
plt.plot(data_sorted, cdf)

# Step 1: Read data from a text file
file_path = '20ue_policy_time.txt'  # Change this to the path of your text file
with open(file_path, 'r') as file:
    data = file.readlines()
    data = [float(line.strip()) for line in data] + [75] # Convert each line into a float

# Step 2: Calculate the CDF
data_sorted = np.sort(data)
cdf = np.arange(1, len(data_sorted)+1) / len(data_sorted)
plt.plot(data_sorted, cdf)

plt.xlim(0,800)
plt.legend(["5UEs", "10UEs", "20UEs"], fontsize = 16)

#plt.xlabel('Data Values')
#plt.ylabel('CDF')
#plt.title('Cumulative Distribution Function (CDF)')
plt.grid(True)
plt.savefig("ppo_compute.pdf")
plt.show()
