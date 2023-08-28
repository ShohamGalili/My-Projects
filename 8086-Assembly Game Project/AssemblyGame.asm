;Shoham Galili 208010785

.model small
.stack 100h
.data
		out_msg db 'Score: $'
		repeat3 dw 0
		LastKeyPress db 0
		Flag db 0
		FlagExit db 0

.code

;***********************************************************
;Black_Screen 
;Outputs: This function prints black background on screen
;***********************************************************

	Black_Screen PROC near uses es ax si
	
		mov ax, 0B800h
		mov es, ax        ;Set ax to Screen
		mov si, 0h
		mov ax,' '        ;Print ' ' to screen 
		mov cx, 1280h     ;Set cx to Screen Size
		
		ScreenLoop:	
			mov es:[si],ax
			sub cx, 2h
			add si, 2h
			cmp cx, 0 
		jnz ScreenLoop
		
		mov bl, 4Fh ;Set O to screen
	    mov bh, 04h ;Set Red color
		mov es:[2000d], bx
		
	ret
	Black_Screen ENDP
	
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

;***********************************************************
;Randomized_Point 
;Outputs: This function prints point on randomized location on screen
;***********************************************************

	Randomized_Point proc near uses ax dx es si
	
		mov al, 00h
		out 70h, al ;Sent request to port 70 to get seconds
		
		in al, 71h ;Read the Seconds from port 71
		mov ch, al
		
		mov al, 02h
		out 70h, al ;Sent request to port 70 to get minutes
		
		in al, 71h ;Read the minutes from port 71
		mov cl, al
		
		;~~~~~~~Senity Checks:~~~~~~~~~
		;Check if the address is out of screen range
		mov ax, cx 
		mov si, 2000d ;The size of screen
		div si ;do ax/si when: ax= (int) ax/si , dx= ax mod si 
		shl dx, 1 ;dx= dx*2
		mov cx, dx
		
		;Check if the new address is equal to prev address
		cmp cx, si 
		jnz ifNotEqual
		add cx, 2h ;Update tha address to cx+2h --> Insure that its not the same address as the prev

		ifNotEqual:
		mov si, cx
		mov ax, 0B800h
		mov es, ax  ;Set es to Screen
		mov dl, 58h ;Set X to screen
	    mov dh, 04h ;Set Red color
		mov es:[si], dx ;Set X on screen in address si
	
	ret	
	Randomized_Point ENDP
	
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

;***********************************************************
;Print_Score
;Outputs: This function prints the score to screen
;***********************************************************
	Print_Score proc near uses di dx cx ax
	
		mov ax, di
		mov dl, 10d
		div dl ;al= (int) ax/dl . ah= ax mod dl --> al= ten's digit ah= unit digit
		add al, 30h ;Convert to ASCII number
		add ah, 30h ;Convert to ASCII number
		mov cx, ax
		
		;mov dx, offset out_msg ;Print 'Score ' to screen
		;mov ax, 0B800h
		;mov es, ax
		;mov es:[340h], dx
		
	
		mov dx, offset out_msg
		mov ah, 9h
		int 21h
		
		mov dl, cl
		mov ah, 02h
		int 21h
		
		mov dl, ch
		mov ah, 02h
		int 21h
		
		mov dh, 1 ;Move to the next line
		mov dl, 0
		mov bh, 0
		mov ah, 2
		int 10h

		
	ret
	Print_Score endp 
	
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
;***********************************************************
;ISR_New_1C
;Outputs: This function change int 1C
;***********************************************************	

	ISR_New_1C proc far 
		
		cmp repeat3, 3h ;if has passed 0.165 sec
		jnz IncRepeat3 ;if repeat3 != 3
		
		mov repeat3, 0h ;if repeat3 == 3
		call Continue_Move ;if has passed 0.165 seconds make another move at the same direction
		;mov Flag, 1 ;Flag = 1 --> in the main call to Continue_Move
		jmp end1C
		
		IncRepeat3: ;if repeat3 != 3
		inc repeat3
		;mov Flag, 0 ;Flag = 0 --> Dont Move
		
		end1C:
		int 81h ;use the old interrupt

	iret
	ISR_New_1C ENDP

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;***********************************************************
;Continue_Move
;Outputs: This function check the key that was pressed, and continue move to the needed direction
;***********************************************************

	Continue_Move proc near uses ax es 
	
		;mov Flag, 0 ;Flag=0 --> on the next iteration we dont enter Continue_Move again
		in al,60h ;Read Scan Code from keyboard port
		and al, 7Fh ;Save the scan code pressing
		mov LastKeyPress, al 

	check_W_2: ;UP
		cmp LastKeyPress, 17d ;Check if W has pressed
		jnz check_A_2
		
		;Check if the symbol is on the first line
		cmp bx, 160d 
		jb end_continue_move ;if bx<160 --> dont move
		
		mov ax, 0B800h
		mov es, ax
		mov ax,' '
		mov es:[bx],ax ;Delete the prev O
		sub bx, 160d ;Updating to the previous line- move UP
		mov ax,044Fh ;'O' in red color
		mov es:[bx], ax
		
		;~~~~~~~~~~~~~~~~~~~~~~~~~~		
		check_A_2: ;LEFT
		cmp LastKeyPress, 30d ;Check if A has pressed
		jnz check_D_2
		
		
		;Check if the symbol is on the first column
		mov ax, bx ; ax= address
		push bx
		mov bh, 160d
		div bh ;al= (int) ax/bh . ah= ax mod bh
		pop bx
		cmp ah, 0 ;Check if the symbol is on the first column
		jz end_continue_move;Check if the symbol is on the first column --> Dont move
		
		mov ax, 0B800h
		mov es, ax
		mov ax,' '
		mov es:[bx],ax ;Delete the prev O
		sub bx, 2h ;move LEFT
		mov ax,044Fh ;'O' in red color
		mov es:[bx], ax
		
		;~~~~~~~~~~~~~~~~~~~~~~~~~~		
		check_D_2: ;RIGHT
		cmp LastKeyPress, 32d ;Check if D has pressed
		jnz check_S_2
		
		;Check if the symbol is on the last column
		mov ax, bx ; ax= address
		push bx
		mov bh, 160d
		div bh ;al= (int) ax/bh . ah= ax mod bh
		pop bx
		cmp ah, 158d ; Check if the symbol is on the last column
		jz end_continue_move ;Check if the symbol is on the last column --> Dont move
		
		mov ax, 0B800h
		mov es, ax
		mov ax,' '
		mov es:[bx],ax ;Delete the prev O
		add bx, 2h ;move RIGHT
		mov ax,044Fh ;'O' in red color
		mov es:[bx], ax
		
		;~~~~~~~~~~~~~~~~~~~~~~~~~~		
		check_S_2: ;DOWN
		cmp LastKeyPress, 31d ;Check if S has pressed
		jnz check_address_2
		
		;Check if the symbol is on the last line
		cmp bx, 3838d 
		ja end_continue_move ;if bx>=3840 --> dont move
		
		mov ax, 0B800h
		mov es, ax
		mov ax,' '
		mov es:[bx],ax ;Delete the prev O
		add bx, 160d ;Updating to the next line- move DOWN
		mov ax,044Fh ;'O' in red color
		mov es:[bx], ax

		
		;~~~~~~~~~~~~~~~~~~~~~~~~~~		
		check_address_2:
		cmp cx, bx ;cx= Point Address , bx= Symbol Address --> Check if O succeed collect X
		jnz end_continue_move ;if there is no succeed --> continue
		;if O succeed collect X:
		inc di ;Points Number ++
		call Randomized_Point ;Get another point on randomize address on screen
		
		end_continue_move:
	
	ret
	Continue_Move ENDP
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	.startup

	mov di, 0h ;Counter of Points that collected
	mov si, 0h
	
	call Black_Screen
	
	call Randomized_Point
	
	mov bx, 2000d ;Initial address of O
	
	mov ax,0h ; IVT is location is '0000' address of RAM
	mov es,ax
	
	
	;cli ; block interrupts
	cli
	;moving 1C into IVT[081h]
	mov ax,es:[1Ch*4] ;copying old ISR1C IP to free vector
	mov es:[81h*4],ax
	mov ax,es:[1Ch*4+2] ;copying old ISR1C CS to free vector
	mov es:[81h*4+2],ax
	
	;moving ISR_New_1C into IVT[1C]
	mov ax,offset ISR_New_1C ;copying IP of ISR_New to IVT[1C]
	mov es:[1Ch*4],ax
	mov ax,cs ;copying CS of our ISR_New into IVT[1C]
	mov es:[1Ch*4+2],ax
	
	sti ;enable interrupts
	
	cli
	;mask interrupts from keyboard
	in al, 21h
	or al, 02h
	out 21h, al
	sti
	
	L1: 
	if_key_was_pressed:
		in al,64h
		test al, 00000001b ;Check Lsb- if LSB ==1 --> Key was pressed if LSB ==0 --> Key wasn't pressed
		jz if_key_was_pressed
			
			in al,60h ;Read Scan Code from keyboard port
			Check_Q_2: ;EXIT
			cmp al, 90h ;Check if Q has pressed
			jnz call_Con_Move
			
			mov ax, 0B800h
			mov es, ax
			mov ax,' '
			mov es:[bx],ax ;Delete the prev O
			
			mov si, cx
			mov es:[si],ax ;Delete the prev X
			jmp  out_loop
			
			call_Con_Move:
			call Continue_Move
		
	
	end_L1:
	jmp L1
	
	out_loop:
	
	cli
	;unmask keyboard
	mov al,0
	out 21h,al
	sti
	
	printScore:
	call Print_Score

	;~~~~~~~~~~~back to the original IVT~~~~~~~~~~~~~
	mov ax, 0 ; IVT is location is '0000' address of RAM
	mov es, ax
	cli ; block interrupts
	
	;moving 1C into IVT[081h]
	mov ax,es:[81h*4] ;copying old ISR1C IP to ISR 1C
	mov es:[1Ch*4],ax
	mov ax,es:[81h*4+2] ;copying old ISR1C CS to ISR 1C
	mov es:[1Ch*4+2],ax
	
	sti ;enable interrupts
	
	
	.exit

end 