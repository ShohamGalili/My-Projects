A client-server system based on signal communication and data transfer via files.

I implemented a calculator of the 4 basic operations (addition, subtraction, multiplication and division) based on server software that receives from a client software,
a pair of numbers and the requested operation and the server must return the result of the calculation as an answer to the client.

The client software will receive 4 parameters in the command line to run and will look like this:
ex2_client.out P1 P2 P3 P4
where the Pi are the parameters and are defined as follows:
i. P1 – is the server's PID (server process ID number).
ii. P2 - is the first numerical value on which the calculation operation must be performed.
iii. P3 – is the code of the calculation operation itself: 1-addition, 2-subtraction, 3-multiplication 4-division.
iv. P4 - is the second numerical value with which the calculation operation must be performed.

Note: The server software must be run in the background (the server software will wait for requests from client programs that will try to connect to the server).
