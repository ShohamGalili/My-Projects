This code simulates an operating system timer and calculates the turnaround time for different timing protocols. It reads input data from a file, simulates the execution of processes using various scheduling algorithms, and calculates the mean turnaround time for each algorithm.

Supports the following timing protocols:
  - First-Come, First-Served (FCFS)
  - Last-Come, First-Served Non-preemptive (LCFS-NP)
  - Last-Come, First-Served Preemptive (LCFS-P)
  - Shortest Job First Preemptive (SJF-P)
  - Round Robin (RR)

Input data is read from a file specified in the command line.

The code is implemented in Python and uses the following libraries:
  - `numpy` for numerical calculations
  - `tqdm` for progress bar visualization
