/*##################################
EX2- CLIENT
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
#include <signal.h>

#define ERROR_EXIT -1
#define SUCCESS_EXIT 0

//Gets the file with the calculation result from the server --> and print the solution!
void signal_handler ( int sig )
{
    char solution_buff[10];
    int ans_fd;
    char ans_path[50];
    char solution_print[50];
    int ans_read;

    sprintf(ans_path, "to_client_%d.txt", (int)getpid());


    ans_fd= open(ans_path, O_RDONLY, 0666); //Open the file we get from server
    if( ans_fd < 0) //Check if Open syscall failed:
    {
        printf("Error- failed opening to_client file");
        //exit(ERROR_EXIT);
    }

    //Read the solution from the file we got from server:
    ans_read= read(ans_fd, solution_buff, 9); //Assume that the length of float number is 9 chars
    if(ans_read < 0)
    {
        printf("Error- failed reading to_client file");
        //exit(ERROR_EXIT);
    }
    
    solution_buff[9]= '\0'; //I Assume that the length of float number is 9 digits
    //Print answer to screen:
    sprintf(solution_print, "[Client with PID=%d]: The result of my calculation question is: %s\n",(int)getpid(), solution_buff);
    printf("%s", solution_print);

    remove(ans_path); //removing the "./to_client_XXXX" file after we finished using it
	close(ans_fd); //freeing our open fds
}


// ********************************* MAIN ********************************************
void main(int argc, char * argv[])
{
    if ( argc != 5)               //means that a server ID or 2 numbers and an operator were not given
    {
        printf("Error. please enter 4 arguments\n");
        //return (ERROR_EXIT);
    }

    //------------------------Initializations:---------------------------
    int to_srv_fd;
    int server_fd;
    int rand_num;
    int i;
    int j;
    char args_buffer[60];
    int fail_count=0;

    signal(1 , signal_handler); //Defines the handler for signal 1
    server_fd= atoi( argv[1]); //Get fd's server from commend line. so we could send a signal with "kill"

    //Creat an Input file of the inputs we want the server will calculate
    to_srv_fd= open("to_srv.txt", O_RDONLY|O_WRONLY|O_CREAT, 0666); //open to server file

    for (i=0; i<10; i++) //Check if the client was success to do open on 10 temps
    {
        if ( to_srv_fd == -1)
        {
            fail_count++;
            to_srv_fd= open("to_srv.txt", O_RDONLY|O_WRONLY|O_CREAT, 0666);
            if ( to_srv_fd == -1 )
            {
                rand_num= rand() % 10; //Random a number in range: 0-10
                sleep(rand_num);       // sleep for rand_num seconds
            }
            else //if success --> get out of for loop
            {
                break;
            }
        }
        if( fail_count == 10) // If there is not a success for 10 attempts--> the client can't get a service from the server
        {
            printf("Error- failed opening to_srv file too many times\n");
            //exit(ERROR_EXIT);
        }

    } //end for loop

    //-----------------------------Input integrity Check--------------------------------

    //Write the arguments into "to_srv.txt" file
    sprintf(args_buffer, "%d\n", (int)getpid()); //putting clieants id inside "args_buffer"
    if( write(to_srv_fd, args_buffer, strlen(args_buffer)) == -1) //Write Client PID to "to_server.txt" file
    {
        printf("Error- failed writing to_srv file\n");
        close(to_srv_fd);
        //exit(ERROR_EXIT);
    }


    //Copy the arguments from command line to "to_srv.txt" file
    for( j=2; j<5; j++)
    {
        sprintf( args_buffer, "%s\n", argv[j]); //Copy to arg_buffer the arg from command line
        if( write(to_srv_fd, args_buffer, strlen(args_buffer)) == -1)
        {
            printf("Error- failed writing to_server file");
            close(to_srv_fd);
            //exit(ERROR_EXIT);  
        }
    }

    close(to_srv_fd); //close the file

    //Send the signal to server:
    int kill_ret_val= kill(server_fd, 2);
    if( kill_ret_val < 0)
    {
        printf("Error- sending the signal to server failed");
        //exit(ERROR_EXIT); 
    }

        pause(); //waiting for signal from child of server
    
} //End of Main 