// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@IS_EQUAL_2
D;JEQ
@SP
A=M-1
M=0
@END_COMPARE_EQ_2
0;JMP
(IS_EQUAL_2)
@SP
A=M-1
M=-1
(END_COMPARE_EQ_2)
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@IS_EQUAL_5
D;JEQ
@SP
A=M-1
M=0
@END_COMPARE_EQ_5
0;JMP
(IS_EQUAL_5)
@SP
A=M-1
M=-1
(END_COMPARE_EQ_5)
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@IS_EQUAL_8
D;JEQ
@SP
A=M-1
M=0
@END_COMPARE_EQ_8
0;JMP
(IS_EQUAL_8)
@SP
A=M-1
M=-1
(END_COMPARE_EQ_8)
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@IS_LESS_11
D;JLT
@SP
A=M-1
M=0
@END_COMPARE_LT_11
0;JMP
(IS_LESS_11)
@SP
A=M-1
M=-1
(END_COMPARE_LT_11)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@IS_LESS_14
D;JLT
@SP
A=M-1
M=0
@END_COMPARE_LT_14
0;JMP
(IS_LESS_14)
@SP
A=M-1
M=-1
(END_COMPARE_LT_14)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@IS_LESS_17
D;JLT
@SP
A=M-1
M=0
@END_COMPARE_LT_17
0;JMP
(IS_LESS_17)
@SP
A=M-1
M=-1
(END_COMPARE_LT_17)
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@IS_GREATER_20
D;JGT
@SP
A=M-1
M=0
@END_COMPARE_GT_20
0;JMP
(IS_GREATER_20)
@SP
A=M-1
M=-1
(END_COMPARE_GT_20)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@IS_GREATER_23
D;JGT
@SP
A=M-1
M=0
@END_COMPARE_GT_23
0;JMP
(IS_GREATER_23)
@SP
A=M-1
M=-1
(END_COMPARE_GT_23)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@IS_GREATER_26
D;JGT
@SP
A=M-1
M=0
@END_COMPARE_GT_26
0;JMP
(IS_GREATER_26)
@SP
A=M-1
M=-1
(END_COMPARE_GT_26)
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// neg
@SP
A=M-1
M=-M
// and
@SP
AM=M-1
D=M
A=A-1
M=D&M
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
AM=M-1
D=M
A=A-1
M=D|M
// not
@SP
A=M-1
M=!M
