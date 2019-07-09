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
@IS_EQUAL_StackTest_2
D;JEQ
@SP
A=M-1
M=0
@END_COMPARE_EQ_StackTest_2
0;JMP
(IS_EQUAL_StackTest_2)
@SP
A=M-1
M=-1
(END_COMPARE_EQ_StackTest_2)
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
@IS_EQUAL_StackTest_5
D;JEQ
@SP
A=M-1
M=0
@END_COMPARE_EQ_StackTest_5
0;JMP
(IS_EQUAL_StackTest_5)
@SP
A=M-1
M=-1
(END_COMPARE_EQ_StackTest_5)
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
@IS_EQUAL_StackTest_8
D;JEQ
@SP
A=M-1
M=0
@END_COMPARE_EQ_StackTest_8
0;JMP
(IS_EQUAL_StackTest_8)
@SP
A=M-1
M=-1
(END_COMPARE_EQ_StackTest_8)
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
@IS_LESS_StackTest_11
D;JLT
@SP
A=M-1
M=0
@END_COMPARE_LT_StackTest_11
0;JMP
(IS_LESS_StackTest_11)
@SP
A=M-1
M=-1
(END_COMPARE_LT_StackTest_11)
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
@IS_LESS_StackTest_14
D;JLT
@SP
A=M-1
M=0
@END_COMPARE_LT_StackTest_14
0;JMP
(IS_LESS_StackTest_14)
@SP
A=M-1
M=-1
(END_COMPARE_LT_StackTest_14)
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
@IS_LESS_StackTest_17
D;JLT
@SP
A=M-1
M=0
@END_COMPARE_LT_StackTest_17
0;JMP
(IS_LESS_StackTest_17)
@SP
A=M-1
M=-1
(END_COMPARE_LT_StackTest_17)
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
@IS_GREATER_StackTest_20
D;JGT
@SP
A=M-1
M=0
@END_COMPARE_GT_StackTest_20
0;JMP
(IS_GREATER_StackTest_20)
@SP
A=M-1
M=-1
(END_COMPARE_GT_StackTest_20)
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
@IS_GREATER_StackTest_23
D;JGT
@SP
A=M-1
M=0
@END_COMPARE_GT_StackTest_23
0;JMP
(IS_GREATER_StackTest_23)
@SP
A=M-1
M=-1
(END_COMPARE_GT_StackTest_23)
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
@IS_GREATER_StackTest_26
D;JGT
@SP
A=M-1
M=0
@END_COMPARE_GT_StackTest_26
0;JMP
(IS_GREATER_StackTest_26)
@SP
A=M-1
M=-1
(END_COMPARE_GT_StackTest_26)
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
