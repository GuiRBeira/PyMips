.data
string:     .asciiz "Hello, MIPS!"

.text
main:
    la $a0, string
    read_loop:
        # Carrega o caractere da string
        lb $t0, 0($a0)

        # Verifica se chegou ao final da string (caractere nulo)
        beq $t0, $zero, end_loop

        # Faça o que quiser com o caractere (exemplo: imprimir)
        # Neste exemplo, imprimimos o caractere
        li $v0, 11        # Código do serviço de impressão de caractere
        move $a0, $t0     # Carrega o caractere para imprimir em $a0
        syscall

        # Incrementa o endereço para apontar para o próximo caractere
        addi $a0, $a0, 1

        # Continua o loop
        j read_loop
    end_loop:
    li $v0, 11
    li $a0, 10
    syscall
    li $v0, 10  
    syscall
