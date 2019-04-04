// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// if (KBD=0){
	// SCREEN=0;
// }
// else{
	// SCREEN=-1;
// }

	// if KBD = 0 goto WHITE
	@KBD
	D=M
	@WHITE
	D;JEQ
	// if KBD != 0 goto BLACK
	@BLACK
	D;JNE
(WHITE)
	// i = 8k - 1
	@8191
	D=A
	@i
	M=D
(LOOP_WHITE)
	// set register SCREEN + i white
	@i
	D=M
	@SCREEN
	A=A+D
	M=0
	// if i=0, goto END_WHITE
	@i
	D=M
	@END_WHITE
	D;JEQ
	// i--
	@1
	D=A
	@i
	M=M-D
	// goto LOOP_WHITE
	@LOOP_WHITE
	0;JMP
(END_WHITE)
	// if KBD != 0 goto BLACK
	@KBD
	D=M
	@BLACK
	D;JNE
	// else goto END_WHITE
	@END_WHITE
	0;JMP

(BLACK)
	// i = 8k - 1
	@8191
	D=A
	@i
	M=D
(LOOP_BLACK)
	// set register SCREEN + i black
	@i
	D=M
	@SCREEN
	A=A+D
	M=-1
	// if i=0, goto END_BLACK
	@i
	D=M
	@END_BLACK
	D;JEQ
	// i--
	@1
	D=A
	@i
	M=M-D
	// goto LOOP_BLACK
	@LOOP_BLACK
	0;JMP
(END_BLACK)
	// if KBD = 0 goto WHITE
	@KBD
	D=M
	@WHITE
	D;JEQ
	// else goto END_BLACK
	@END_BLACK
	0;JMP
