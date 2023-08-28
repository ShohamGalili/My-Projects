/*##################################
EX2- SERVER
NAME: Shoham Galili
ID: 208010785
DESCRIPTION: The code simulating and run Client Server System.
##################################*/

#include <sys/stat.h>          
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>   
#include <fcntl.h> 
#include <string.h>         
#include <stdlib.h>
#include <sys/wait.h>

#define ERROR_EXIT -1
#define SUCCESS_EXIT 0

float Calculation( float first_arg, int operand, float second_arg)
{
    if ( operand == 1 )
    {
        return (first_arg + second_arg);
    }
    if ( operand == 2 )
    {
        return (first_arg - second_arg);
    }
    if ( operand == 3 )
    {
        return (first_arg * second_arg);
    }
    if ( operand == 4 )
    {
        if ( second_arg == 0)
        {
            write(1,"ERROR- Divided by 0!\n", 22);
            exit(-1);
        }
        else
        {
        return (first_arg / second_arg);
        }
    }
}

//Open the file and calculates the requested calculate
void signal_handler()
{
    int to_srv_fd;
    char inputs_buffer[50] = {'\0'};
    int pid;
    char* client_pid;
    char* first_num;
    char* second_num;
    char* operand;
    int to_client_fd;
    int open_to_client_pid;
    float calculation;
    char calculation_string[50];
    int write_ret_val;
    int to_client_fd_int;

    //open "to_server.txt" file
    to_srv_fd = open("to_srv.txt", O_RDONLY, 0666); 
    if (to_srv_fd == -1)
    {
        printf("Error- failed opening 'to_srv.txt' file\n");
        exit(ERROR_EXIT);
    }
    //read the inputs that were sent from client to inputs_buffer
    if (read( to_srv_fd, inputs_buffer, 50) == -1) 
    {
        printf("Error- failed reading 'to_srv.txt' file\n");
        exit(ERROR_EXIT);
    } 

    
    pid= fork();
    if ( pid < 0) //Check if fork has an error
    {
        printf("Error with fork syscall\n");
        exit(ERROR_EXIT);
    }

    else if ( pid == 0) //SON
    {   
        execlp("rm", "rm", "to_srv.txt", NULL); //delete the file after extracting the relevant content--> so other clients could call server

    } //End of Son's if

    else //FATHER:
    {
        //signal( SIGCHLD, SIG_IGN); //causes it not to turn the child into a zombie -- when the child exits it is reaped immediately
        int status;
        waitpid(pid,&status, 0);
    }
    

        //Extract relevant content from "to_server" file:
        client_pid= strtok(inputs_buffer, "\n");
        first_num= strtok( NULL , "\n");
        operand= strtok(NULL, "\n");
        second_num= strtok(NULL, "\n");

        //Create the name of to_client_fd file:
        char to_client_file_name[50] = "to_client_";
        strncat(to_client_file_name , client_pid, strlen(client_pid));

        strncat(to_client_file_name, ".txt", 4);

        to_client_fd= open( to_client_file_name, O_RDONLY|O_WRONLY|O_CREAT, 0666); //Create the to_client file

        if ( to_client_fd == -1)
        {
            printf("Error- failed opening 'to_srv.txt' file\n");
            exit(ERROR_EXIT); 
        }

        calculation=  Calculation( atof(first_num), atoi(operand), atof(second_num)); //Calculate
        sprintf( calculation_string, "%f\n",calculation);
        write_ret_val= write( to_client_fd , calculation_string, strlen(calculation_string) ); //Write the answer to the file that will be sent to client
        if( write_ret_val < 0)
        {
			fprintf(stderr, "Error - failed writing into to_client_%d\n", atoi(client_pid));   
            close(to_client_fd_int);
            remove(to_client_file_name);
            exit(ERROR_EXIT);        
        } 

    kill( atoi(client_pid), 1); //Let the client know that the answer is ready
    close(to_client_fd_int);
    
} // End of Func

void main(int argc, char * argv[])
{

    signal(2, signal_handler);

    while (1)
    {
        pause();
    }   
    
}