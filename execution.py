import instructions as it
import binary_translation as bt

def executa_linha_linha(linhas_do_codigo, registradores_widget, console_widget, traducao_widget, memoria_widget,modo_debug):
    tipos_logicoaritmeticas = {'add', 'addi', 'sub', 'subi', 'mul', 'div', 'and', 'or', 'xor', 'nor', 'sra', 'sll', 'slt'}
    tipos_controle = {'beq', 'blt', 'bgt', 'bge','bne', 'j', 'jal', 'jr'} 
    tipos_acesso = {'li', 'sw', 'lw', 'move', 'la'}
    linha_atual_index = 0
    main_encontrada = False
    secao_data_encontrada = False
    secao_text_encontrada = False
    
    while linha_atual_index < len(linhas_do_codigo):
        linha_atual = linhas_do_codigo[linha_atual_index]
        #console_widget.write(str(linha_atual))
        linha_atual_index += 1
        referencia, *outros_tokens = linha_atual

        if referencia[1] == 'LABEL':
            linha_sem_espacos = list(filter(lambda token: token[1] != 'SPACE', linha_atual))
            nome_label = linha_sem_espacos[0][0].replace(':', '')
            
            # Inicializa o valor da LABEL como None
            valor = None
            
            # Verifica se a LABEL é seguida por uma instrução ASCIIZ
            if len(linha_sem_espacos) > 1 and linha_sem_espacos[1][1] == 'ASCIIZ' and secao_data_encontrada:
                # Obtém o valor da string (supondo que seja o segundo token na linha)
                valor = linha_sem_espacos[1][0]
                valor = valor.replace(".asciiz", "")
                valor = valor.replace('"','')
                valor = valor.replace("\\n", "")
            
            # Adiciona a LABEL ao dicionário de registradores, usando o rótulo como chave
            registradores_widget.endereco_label[nome_label] = {'valor': valor, 'linha': linha_atual_index}
            if referencia[0] == 'main:':
                main_encontrada = True

        elif referencia[1] == 'TEXT':
            pass
        
        elif referencia[1] == 'INSTRUCTION' and secao_text_encontrada and main_encontrada:
            registradores_widget.registradores["PC"]+=1
            if referencia[0] in tipos_logicoaritmeticas:    
                it.instrucao_logicoaritmetica(linha_atual, registradores_widget, console_widget)

            elif referencia[0] in tipos_controle:
                linha_atual_index = it.instrucao_desvio(linha_atual, registradores_widget, linha_atual_index)

            elif referencia[0] in tipos_acesso:
                it.instrucao_acesso(linha_atual, registradores_widget, memoria_widget, console_widget)
                
            binario = bt.traduzir_instrucao(linha_atual, registradores_widget)
            traducao_widget.write(binario)
            
        elif referencia[1] == 'SYSCALL' and main_encontrada:
            if it.syscall(registradores_widget, console_widget):
                break
        if modo_debug:
            input("DEBUG: Pressione Enter para continuar...")
        
        registradores_widget.atualizar_registradores_na_gui()
        memoria_widget.atualizar_memoria_na_gui()
