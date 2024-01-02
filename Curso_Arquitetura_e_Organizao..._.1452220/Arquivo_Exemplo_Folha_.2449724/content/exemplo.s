
#void main(){

  #int f = folha(1,2,3,4);

  #printf("O resultado de folha é %i \n\n", f);

#}
#int folha(int g, int h, int I, int j){
#   int f;
#   f = (g + h) - (I + j);
#return f;
#}

.data 

 M1: .asciiz "O resultado de folha é "
 M2: .asciiz "\n\n"

.text


main:

	li $a0, 1
	li $a1, 2
	li $a2, 3
	li $a3, 4

	jal folha

	move $t0, $v0
	
	li $v0,4
	la $a0, M1
	syscall
	
	li $v0,1
	move $a0, $t0
	syscall
	
	li $v0,4
	la $a0, M2
	syscall
	
	li $v0,10
	syscall

folha:
	addi $sp, $sp, -12
	sw $s0, 12($sp)
	sw $s1, 8($sp)
	sw $ra, 4($sp)

	add $s0, $a0, $a1
	add $s1, $a2, $a3
	sub $v0,$s0, $s1	

	lw $s0, 12($sp)
	lw $s1, 8($sp)
	lw $ra, 4($sp)
	addi $sp, $sp,12

	jr $ra  
	








