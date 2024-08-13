# Operating System Timer Simulation

This project simulates an operating system timer and calculates the turnaround time for various scheduling algorithms. It reads input data from a file, executes processes using different timing protocols, and computes the average turnaround time for each protocol.

## Supported Scheduling Algorithms

- **First-Come, First-Served (FCFS):** Processes are executed in the order they arrive.
- **Last-Come, First-Served Non-preemptive (LCFS-NP):** The most recently arrived process is executed next, without preemption.
- **Last-Come, First-Served Preemptive (LCFS-P):** The most recently arrived process can preempt the currently running process.
- **Shortest Job First Preemptive (SJF-P):** The process with the shortest remaining time is executed next and can preempt the current process.
- **Round Robin (RR):** Processes are executed in a cyclic order, each given a fixed time slice.

## How to Use

1. **Prepare Input Data:**
   - Ensure your input data file is formatted correctly. This file should contain the details of the processes you want to simulate.

2. **Run the Simulation:**
   - Execute the Python script from the command line, specifying the path to your input data file.
   - Example command:
     ```bash
     python simulate_timer.py input_data.txt
     ```

3. **View Results:**
   - The script will simulate process execution according to the specified algorithms and display the mean turnaround time for each scheduling protocol.

## Requirements

- **Python:** Make sure you have Python installed.
- **Libraries:**
  - `numpy` for numerical calculations
  - `tqdm` for progress bar visualization

  You can install the required libraries using pip:
  ```bash
  pip install numpy tqdm
