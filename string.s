.data
string:     .asciiz "Hello, MIPS!"

.text
main:
    # Carrega o endereço base da string em $a0
    la $a0, string

    # Loop para percorrer a string e imprimir os caracteres
    read_loop:
        # Carrega o caractere da string
        lb $t0, 0($a0)

        # Verifica se chegou ao final da string (caractere nulo)
        beq $t0, $zero, end_loop

        # Imprime o caractere
        li $v0, 11        # Código do serviço de impressão de caractere
        move $a0, $t0     # Carrega o caractere para imprimir em $a0
        syscall

        # Incrementa o endereço para apontar para o próximo caractere
        addi $a0, $a0, 1

        # Continua o loop
        j read_loop

    end_loop:
    # Imprime uma nova linha no final
    li $v0, 11
    li $a0, 10
    syscall

    # Fim do programa
    li $v0, 10          # Código do serviço de término do programa
    syscall
