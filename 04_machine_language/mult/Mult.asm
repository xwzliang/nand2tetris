// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// n = RAM[1];
// while (n>0){
	// RAM[2] += RAM[0];
	// n--;
// }

// Multiplies R0 and R1
	// n = RAM[1]
	@R1
	D=M
	@n
	M=D
	// RAM[2] = 0
	@R2
	M=0

(LOOP)
	// if n = 0 goto END
	@n
	D=M
	@END
	D;JEQ
	// RAM[2] += RAM[0]
	@R0
	D=M
	@R2
	M=D+M
	// n -= 1
	@1
	D=A
	@n
	M=M-D
	// goto LOOP
	@LOOP
	0;JMP
(END)
	// Infinite end loop
	@END
	0;JMP
