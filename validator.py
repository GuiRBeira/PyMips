from execution import executa_linha_linha

def agrupar_tokens_por_linha(tokens):
    tokens_por_linha = {}

    for token in tokens:
        linha = token[2]
        if linha not in tokens_por_linha:
            tokens_por_linha[linha] = []
        tokens_por_linha[linha].append(token)
    return list(tokens_por_linha.values())

def validar_codigo(tokens, registradores_widget, console_widget,traducao_widget, memoria_widget,modo_debug):
    tipos_logicoaritmeticas = {'add', 'addi', 'sub', 'subi', 'mul', 'div', 'and', 'or', 'xor', 'nor', 'sra', 'sll', 'slt'}
    tipos_controle = {'beq', 'blt', 'bgt', 'bge','bne', 'j', 'jal', 'jr'}
    tipos_acesso = {'li', 'sw','lw', 'move', 'la'}
    diretive_data = False
    diretive_text = False
    tokens_por_linha = agrupar_tokens_por_linha(tokens)
    linhas_do_codigo = []
    for tokens_da_linha in tokens_por_linha:
        for token in tokens_da_linha:
            if token[1] == 'REGISTER':
                if token[0][1:] in registradores_widget.registradores:
                    pass
                else:
                    console_widget.write(f"Registrador inválido {token[0]} na linha: {token[2]}")
                    
            if token[1] == 'DATA':
                diretive_data = True
                
            if token[1] == 'TEXT':
                diretive_text = True
                
            if token[1] == 'INSTRUCTION':
                instrucao = token[0]
                
                if instrucao in tipos_logicoaritmeticas or instrucao in tipos_controle or instrucao in tipos_acesso:
                    pass
                else:
                    console_widget.write(f"Instrução inválida na linha {token[2]}: {instrucao}\n")
                    
            if token[1] == 'LABEL':
                nome_label = token[0].replace(":", "")
                registradores_widget.endereco_label[nome_label] = token[2]
            
                    
        linhas_do_codigo.append(tokens_da_linha)
        
    if not diretive_data:
        console_widget.write("Elemento '.data' faltando !!\n")
        
    if not diretive_text:
        console_widget.write("Elemento '.text' faltando !!\n")
        
    executa_linha_linha(linhas_do_codigo, registradores_widget, console_widget, traducao_widget, memoria_widget,modo_debug)