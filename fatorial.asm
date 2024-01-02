.data

    texto: .asciiz "O resultado do Fatorial de 5 é \n\n"

.text

main:

    la $a0, texto
    li $v0, 4
    syscall

        
    li $a0, 5   # a0 == n
    li $v0, 1   # fat 
    li $t5, 1
    li $t0, 1
    
    jal fact

        move $a0, $v0
    li $v0,1
    syscall
    
    
    li $v0,10
    syscall
    


fact:
    addi $sp, $sp, -12
    sw $a0, 12($sp)
    sw $s0, 8($sp)
    sw $ra, 4($sp)
    
    beq $a0, $t0, sair   # n == 1?
    slt $s0, $a0, $t5       # caso base n < ou == 1
    bne $s0, $zero, sair

    addi $a0, $a0, -1
    
    jal fact

    lw $a0, 12($sp)
    lw $s0, 8($sp)
    lw $ra, 4($sp)
    addi $sp, $sp, 12
    
    mul $v0, $v0, $a0
    

sair:

    jr $ra
