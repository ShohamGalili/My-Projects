import sys
from ProcessClass import ProcessClass

#GLOBAL VARIABLES:
clock= 0
Turnaround_schedulers= []

#Func that read from the file we get from the command line
def read_file (file):
    file= open(file, "r") #open the file from command line
    file_content= file.readlines() #read from file (string)
    for i in range(len(file_content)):
        file_content[i]= file_content[i].replace( "\n", "")
    
    #Extract the first arg of the number of processes
    num_of_processes= int(file_content[0])
    file_content.remove(file_content[0])

    #Go through the list--> for each node, split the content to new list without ","
    file_content= [list(map(int, s.split(","))) for s in file_content] 

    return num_of_processes, file_content


#The func create an Process-Object for each process from the big processes list:
def make_Processes(processes_list, num_of_processes):
    ProcessObjectsList= []
    for i in range(num_of_processes):
        ProcessObjectsList.append(ProcessClass(processes_list[i], i+1)) #Create a Process object for each node of the whole list, and add it tp the objects list
        #ProcessObjectsList[i].printProcess(i) #Print the Process's Parameters
    
    return ProcessObjectsList

################################### FCFS ##########################################
#The func calculate the mean Turnaround time of FCFS scheduler:
def FCFS_scheduler (processObjectsList, num_of_processes ):
    global Turnaround_schedulers 
    global clock

    processObjectsList.sort(key=lambda Process: (Process.arrivalTime, Process.subPriority)) #Sorting the Objects list by arrival Time

    for i in range(num_of_processes):
        if (processObjectsList[i].isTerminated == False):
            if(processObjectsList[i].arrivalTime > clock):
                clock= processObjectsList[i].arrivalTime #Add the arrival time of the process to the clock
            clock+= processObjectsList[i].computationTime #At the end of the complication --> Add the computation time of the process to the clock
        processObjectsList[i].Turnaround= clock - processObjectsList[i].arrivalTime #Calc of Turnaround= End Time - Start Time

    #Calculate the mean of Turnaround times:
    sum_of_Turnaround=0
    for i in range(num_of_processes):
        sum_of_Turnaround += processObjectsList[i].Turnaround

    FCFS_scheduler_Turnaround = sum_of_Turnaround / num_of_processes #the avarage Turnaround

    Turnaround_schedulers.append(FCFS_scheduler_Turnaround) #Add the FCFS Mean Turnaround to the General Turnaround list

################################### LCFS Not Preemptive ##########################################
def LCFS_Not_Preemptive_scheduler (processObjectsList, num_of_processes ):
    global Turnaround_schedulers 
    global clock
    clock= processObjectsList[0].arrivalTime
    max_process=0
    sum_LCFS_scheduler_Turnaround=0

    processObjectsList.sort(key=lambda Process: (Process.arrivalTime, Process.subPriority)) #Sorting the Objects list by arrival Time

    for i in range(num_of_processes):
        processObjectsList[i].isTerminated= False

    while not all ( processObjectsList[i].isTerminated for i in range(num_of_processes)): #While not all Processes are get Terminated...
        AliveList = []
        for i in range(num_of_processes):
            if (processObjectsList[i].isTerminated == False):
                if(processObjectsList[i].arrivalTime <= clock):
                    AliveList.append(i) #If the process isnt terminated && Still not run on CPU --> add him to the list
            max_process= max(AliveList, default=0)

        if (len(AliveList) == 0):
            clock +=1
        else:
            clock= clock+ processObjectsList[max_process].computationTime #Update global clock
            processObjectsList[max_process].isTerminated = True 
            AliveList.remove(max_process) #Delete the process from list
            processObjectsList[max_process].Turnaround= clock - processObjectsList[max_process].arrivalTime
            sum_LCFS_scheduler_Turnaround += processObjectsList[max_process].Turnaround #Update the turnaround time

    
    LCFS_scheduler_Turnaround = sum_LCFS_scheduler_Turnaround / num_of_processes #the avarage Turnaround
    Turnaround_schedulers.append(LCFS_scheduler_Turnaround) #Add the LCFS Mean Turnaround to the General Turnaround list

################################### LCFS Preemptive ##########################################
def LCFS_Preemptive_scheduler (processObjectsList, num_of_processes ):
    global Turnaround_schedulers 
    global clock
    clock= processObjectsList[0].arrivalTime
    max_process=0
    sum_LCFS_scheduler_Turnaround=0

    processObjectsList.sort(key=lambda Process: (Process.arrivalTime, Process.subPriority)) #Sorting the Objects list by arrival Time

    for i in range(num_of_processes):
        processObjectsList[i].isTerminated= False

    while not all ( processObjectsList[i].isTerminated for i in range(num_of_processes)): #While not all Processes are get Terminated...
        AliveList = []
        for i in range(num_of_processes):
            if (processObjectsList[i].isTerminated == False):
                if(processObjectsList[i].arrivalTime <= clock):
                    AliveList.append(i) #If the process isnt terminated && Still not run on CPU --> add him to the list
            max_process= max(AliveList, default=0)

        if (len(AliveList) == 0):
            clock +=1
            processObjectsList[max_process].computeLeftTime -= 1
        else:
            if( processObjectsList[max_process].computationTime == 0):
                processObjectsList[max_process].isTerminated = True 
                processObjectsList[max_process].Turnaround= clock - processObjectsList[max_process].arrivalTime
                sum_LCFS_scheduler_Turnaround += processObjectsList[max_process].Turnaround #Update the turnaround time

            else:
                clock +=1
                processObjectsList[max_process].computeLeftTime -= 1
                if (processObjectsList[max_process].computeLeftTime == 0):
                    processObjectsList[max_process].isTerminated = True 
                    AliveList.remove(max_process) #Delete the process from list
                    processObjectsList[max_process].Turnaround= clock - processObjectsList[max_process].arrivalTime
                    sum_LCFS_scheduler_Turnaround += processObjectsList[max_process].Turnaround #Update the turnaround time

    
    LCFS_scheduler_Turnaround = sum_LCFS_scheduler_Turnaround / num_of_processes #the avarage Turnaround
    Turnaround_schedulers.append(LCFS_scheduler_Turnaround) #Add the LCFS Mean Turnaround to the General Turnaround list


################################### RR Preemptive ##########################################
def RR_Preemptive_scheduler (processObjectsList, num_of_processes, quantum_Time ):
    global Turnaround_schedulers 
    global clock
    clock= processObjectsList[0].arrivalTime
    shortest_process= 0
    sum_RR_scheduler_Turnaround=0

    processObjectsList.sort(key=lambda Process: (Process.arrivalTime, Process.subPriority)) #Sorting the Objects list by arrival Time

    for i in range(num_of_processes): #initialize the param "isTerminated"
        processObjectsList[i].isTerminated= False

    for i in range(num_of_processes): #initialize the param "LeftComputeTime"
        processObjectsList[i].remainingTimeRestart()

    while not all ( processObjectsList[i].isTerminated for i in range(num_of_processes)): #While not all Processes are get Terminated...
        AliveList = []

        for i in range(num_of_processes):
            #if (processObjectsList[i].isTerminated == False):
                if(processObjectsList[i].arrivalTime <= clock):
                    AliveList.append(i) #If the process isnt terminated && Still not run on CPU --> add him to the list
                #shortest_process= min(AliveList, default=0) #choose the process with the min computation time
        if all(processObjectsList[i].isTerminated for i in range(len(AliveList))):
            clock +=1
            #processObjectsList[shortest_process].computeLeftTime -= 1
        else:
            for j in range(len(AliveList)): #Run the process that arrived and not terminated yet:
                if (processObjectsList[AliveList[j]].isTerminated == False): #Check if the process is terminated.
                    if (processObjectsList[AliveList[j]].computeLeftTime <= quantum_Time): #if the remaiming time is 1 or 0
                        clock += processObjectsList[AliveList[j]].computeLeftTime #updating the global clock
                        processObjectsList[AliveList[j]].computeLeftTime = 0 #Update the remaining time to 0 (Terminated)
                        processObjectsList[AliveList[j]].isTerminated = True #Update the process to be terminated
                        processObjectsList[AliveList[j]].Turnaround= clock - processObjectsList[AliveList[j]].arrivalTime #Calc the turnaround of the process that end 
                        sum_RR_scheduler_Turnaround += processObjectsList[j].Turnaround #Update the turnaround time

                    else:
                        clock += quantum_Time #Update the global clock 
                        processObjectsList[AliveList[j]].computeLeftTime -= quantum_Time #Sub the quantom time and continue to the next iteration

            
            for k in range(len(AliveList), num_of_processes): #Check for new Process that has arrived:
                if(processObjectsList[k].arrivalTime <= clock): #Check if the new process 
                    AliveList.append(k) #If there is new process --> add him to the list
                    if processObjectsList[AliveList[k]].computeLeftTime <= quantum_Time: # check if the time that left to the new process to run is less than the quantum time
                        clock += processObjectsList[AliveList[k]].computeLeftTime #Run the process
                        processObjectsList[AliveList[k]].computeLeftTime = 0 #Update the remaining time to 0 (Terminated)
                        processObjectsList[AliveList[k]].isTerminated = True #Update the process to be terminated
                        processObjectsList[AliveList[k]].Turnaround= clock - processObjectsList[AliveList[k]].arrivalTime #Calc the turnaround of the process that end 
                        sum_RR_scheduler_Turnaround += processObjectsList[k].Turnaround #Update the turnaround time
                    
                    else:
                        clock += quantum_Time #Update the global clock 
                        processObjectsList[AliveList[k]].computeLeftTime -= quantum_Time #Sub the quantom time and continue to the next iteration                
    
    RR_scheduler_Turnaround = sum_RR_scheduler_Turnaround / num_of_processes #the avarage Turnaround
    Turnaround_schedulers.append(RR_scheduler_Turnaround) #Add the LCFS Mean Turnaround to the General Turnaround list


################################### SJF Preemptive ##########################################
def SJF_Preemptive_scheduler (processObjectsList, num_of_processes ):
    global Turnaround_schedulers 
    global clock
    clock= processObjectsList[0].arrivalTime
    sum_SJF_scheduler_Turnaround=0
    computationTimeList= []
    ComputeMinTime=0
    IndexMinTime=0

    processObjectsList.sort(key=lambda Process: (Process.arrivalTime, Process.subPriority)) #Sorting the Objects list by arrival Time

    for i in range(num_of_processes): #Initialize the parameter of "isTerminated"
        processObjectsList[i].isTerminated= False
    
    for i in range(num_of_processes): #Initialize the parameter of "computeLeftTime"
        processObjectsList[i].remainingTimeRestart()

    #Check if all the processes are terminated:
    while not all ( processObjectsList[i].isTerminated for i in range(num_of_processes)): #While not all Processes are get Terminated...
        AliveList = []
        computationTimeList= []
        for i in range(num_of_processes):
            if (processObjectsList[i].isTerminated == False):
                if(processObjectsList[i].arrivalTime <= clock):
                    AliveList.append(i) #If the process isnt terminated && Still not run on CPU --> add him to the list
                    computationTimeList.append(processObjectsList[i].computationTime) #add the computation time of the process to the computation time list

        if (len(AliveList) == 0):
            clock +=1 #Updating the global clock
        else:
            ComputeMinTime= min(computationTimeList) #Save the min computation time
            for j in range(len(AliveList)): #Finding the index of the process with the min compute time
                if processObjectsList[AliveList[j]].computationTime == ComputeMinTime: #####
                    IndexMinTime= AliveList[j] 

            if (processObjectsList[IndexMinTime].computeLeftTime == 0): #Check if the computation time of the process is 0 (Terminated)
                processObjectsList[IndexMinTime].isTerminated = True 
                processObjectsList[IndexMinTime].Turnaround= clock - processObjectsList[IndexMinTime].arrivalTime
                sum_SJF_scheduler_Turnaround += processObjectsList[IndexMinTime].Turnaround #Update the turnaround time

            else:
                clock+=1 #Updating the global clock
                processObjectsList[IndexMinTime].computeLeftTime = processObjectsList[IndexMinTime].computeLeftTime -1
                if processObjectsList[IndexMinTime].computeLeftTime <= 0:
                    processObjectsList[IndexMinTime].isTerminated = True 
                    processObjectsList[IndexMinTime].Turnaround= clock - processObjectsList[IndexMinTime].arrivalTime
                    sum_SJF_scheduler_Turnaround += processObjectsList[IndexMinTime].Turnaround #Update the turnaround time

    
    SJF_scheduler_Turnaround = sum_SJF_scheduler_Turnaround / num_of_processes #the avarage Turnaround
    Turnaround_schedulers.append(SJF_scheduler_Turnaround) #Add the LCFS Mean Turnaround to the General Turnaround list
    


#MAIN PROGRAM
def main():
    name_of_file= sys.argv[1]
    num_of_processes, file_content= read_file(name_of_file)
    ProcessObjectsList= make_Processes(file_content, num_of_processes)
    FCFS_scheduler(ProcessObjectsList, num_of_processes)
    print("FCFS: mean Turnaround = ", round(Turnaround_schedulers[0],2))
    LCFS_Not_Preemptive_scheduler(ProcessObjectsList, num_of_processes)
    print("LCFS Non-Preemptive: mean Turnaround = ", round(Turnaround_schedulers[1],2))
    LCFS_Preemptive_scheduler(ProcessObjectsList, num_of_processes)
    print("LCF Preemptive: mean Turnaround = ", round(Turnaround_schedulers[2],2))
    RR_Preemptive_scheduler(ProcessObjectsList, num_of_processes, 2)
    print("RR Preemptive: mean Turnaround = ", round(Turnaround_schedulers[3],2))
    SJF_Preemptive_scheduler(ProcessObjectsList, num_of_processes)
    print("SJF Preemptive: mean Turnaround = ", round(Turnaround_schedulers[4],2))


main()






