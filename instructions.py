import tkinter.simpledialog

#FUNCOES AUXILIARES PARA O MAPEAMENTO DAS LABELS E ACESSO

def obter_elemento_por_nome_label(registradores_widget, nome_label):
    if nome_label in registradores_widget.endereco_label:
        return registradores_widget.endereco_label[nome_label]
    else:
        return None

def obter_elemento_por_linha(registradores_widget, linha_atual_index):
    for nome_label, elemento in registradores_widget.endereco_label.items():
        if isinstance(elemento, dict) and 'linha' in elemento and elemento['linha'] == linha_atual_index:
            return elemento
    return None

###########################################################################################################################################
###########################################################################################################################################

def instrucao_logicoaritmetica(tokens_da_linha, registradores_widget, console_widget):
    tokens_da_linha = [t[0] for t in tokens_da_linha if t[0] and t[1] not in ['COMMA', 'COMMENT', 'SPACE']]
    tokens_da_linha = list(filter(lambda x: ' ' not in x[0], tokens_da_linha))
    tokens_da_linha = [t.replace('$', '') if t.startswith('$') else t for t in tokens_da_linha]
    #desta forma vai ter somente instrucao e registradores nas linhas
    instrucao, registrador_destino, registrador_operando1, registrador_operando2 = tokens_da_linha
    try:
        imediato = int(registrador_operando2)
        if instrucao == "addi":
            registradores_widget.registradores[registrador_destino] = registradores_widget.registradores[registrador_operando1] + imediato
        if instrucao == "subi":
            registradores_widget.registradores[registrador_destino] = registradores_widget.registradores[registrador_operando1] - imediato
        if instrucao == "sll":
            registradores_widget.registradores[registrador_destino] = registradores_widget.registradores[registrador_operando1] << imediato
        if instrucao == "sra":
            registradores_widget.registradores[registrador_destino] = registradores_widget.registradores[registrador_operando1] >> imediato
    except:
        if instrucao == "add":
            registradores_widget.registradores[registrador_destino] = int(registradores_widget.registradores[registrador_operando1]) + int(registradores_widget.registradores[registrador_operando2])
        if instrucao == "sub":
            registradores_widget.registradores[registrador_destino] = int(registradores_widget.registradores[registrador_operando1]) - int(registradores_widget.registradores[registrador_operando2])
        if instrucao == "mul":
            registradores_widget.registradores[registrador_destino] = int(registradores_widget.registradores[registrador_operando1]) * int(registradores_widget.registradores[registrador_operando2])  
        if instrucao == "div":
            try:
                registradores_widget.registradores[registrador_destino] = registradores_widget.registradores[registrador_operando1] / registradores_widget.registradores[registrador_operando2]
                registradores_widget.registradores[registrador_destino] = int(registradores_widget.registradores[registrador_destino])
            except:
                console_widget.write("Divisao por zero")
        if instrucao == "and":
            registradores_widget.registradores[registrador_destino] = registradores_widget.registradores[registrador_operando1] & registradores_widget.registradores[registrador_operando2]
        if instrucao == "or":
            registradores_widget.registradores[registrador_destino] = registradores_widget.registradores[registrador_operando1] | registradores_widget.registradores[registrador_operando2]
        if instrucao == "xor":
            registradores_widget.registradores[registrador_destino] = registradores_widget.registradores[registrador_operando1] ^ registradores_widget.registradores[registrador_operando2]
        if instrucao == "nor":
            registradores_widget.registradores[registrador_destino] = ~(registradores_widget.registradores[registrador_operando1] | registradores_widget.registradores[registrador_operando2])
        if instrucao == "slt":
            registradores_widget.registradores[registrador_destino] = 1 if registradores_widget.registradores[registrador_operando1] < registradores_widget.registradores[registrador_operando2] else 0
    
###########################################################################################################################################
###########################################################################################################################################

def instrucao_desvio(tokens_da_linha, registradores_widget, linha_atual_index):
    tokens_da_linha = [t[0] for t in tokens_da_linha if t[0] and t[1] not in ['COMMA', 'COMMENT', 'SPACE']]
    tokens_da_linha = list(filter(lambda x: ' ' not in x[0], tokens_da_linha))
    tokens_da_linha = [t.replace('$', '') if t.startswith('$') else t for t in tokens_da_linha]
    tipo, *outros_tokens, destino_label = tokens_da_linha
    
    if tipo == "j":
        try:
            return registradores_widget.endereco_label[destino_label].get('lista')
        except:
            return registradores_widget.endereco_label[destino_label]
    elif tipo == "jal":
        registradores_widget.registradores['ra'] = linha_atual_index + 1
        try:
            return registradores_widget.endereco_label[destino_label].get('lista')
        except:
            return registradores_widget.endereco_label[destino_label]
    
    elif tipo == "jr":
        registrador_destino = destino_label
        return registradores_widget.registradores[registrador_destino]
        

    elif tipo in {"beq", "bne", "bgt", "bge", "blt"}:
        registrador1 = registradores_widget.registradores[outros_tokens[0]]
        registrador2 = registradores_widget.registradores[outros_tokens[1]]
        # Lógica para instruções de salto condicional
        if tipo == "beq" and registrador1 == registrador2:
            try:
                return registradores_widget.endereco_label[destino_label].get('lista')
            except:
                return registradores_widget.endereco_label[destino_label]
            
        if tipo == "bne" and registrador1 != registrador2:
            try:
                return registradores_widget.endereco_label[destino_label].get('lista')
            except:
                return registradores_widget.endereco_label[destino_label]
            
        if tipo == "bgt" and registrador1 > registrador2:
            try:
                return registradores_widget.endereco_label[destino_label].get('lista')
            except:
                return registradores_widget.endereco_label[destino_label]
            
        if tipo == "bge" and registrador1 >= registrador2:
            try:
                return registradores_widget.endereco_label[destino_label].get('lista')
            except:
                return registradores_widget.endereco_label[destino_label]
            
        if tipo == "blt" and registrador1 < registrador2:
            try:
                return registradores_widget.endereco_label[destino_label].get('lista')
            except:
                return registradores_widget.endereco_label[destino_label]

    return linha_atual_index

###########################################################################################################################################
###########################################################################################################################################
    
def instrucao_acesso(tokens_da_linha, registradores_widget, memoria_widget, console_widget):
    tokens_da_linha = [t[0] for t in tokens_da_linha if t[0] and t[1] not in ['COMMA', 'COMMENT', 'SPACE', 'LPAREN', 'RPAREN']]
    tokens_da_linha = list(filter(lambda x: ' ' not in x[0], tokens_da_linha))
    tokens_da_linha = [t.replace('$', '') if t.startswith('$') else t for t in tokens_da_linha]
    instrucao = tokens_da_linha[0]
    
    if instrucao == "li":
        _, registrador_destino, imediato = tokens_da_linha
        registradores_widget.registradores[registrador_destino] = int(imediato)

    if instrucao == "lw":
        _, registrador_destino, offset, registrador_base = tokens_da_linha
        offset = int(offset)
        offset /= 4
        offset = int(offset)
        if registrador_base != 'sp':
            registradores_widget.registradores[registrador_destino] = registradores_widget.registradores[registrador_base] + offset
        else:
            registradores_widget.registradores[registrador_destino] = memoria_widget.read_word(registradores_widget.registradores['sp'], offset)

    if instrucao == "sw":
        _, registrador_origem, offset, registrador_base = tokens_da_linha
        offset = int(offset)
        offset /= 4
        offset = int(offset)
        if registrador_base != 'sp':
            memoria_widget.write_word(registradores_widget.registradores[registrador_base] + offset, registradores_widget.registradores[registrador_origem])
        else:
            memoria_widget.write_word(registradores_widget.registradores['sp'], registradores_widget.registradores[registrador_origem], offset)
            
    if instrucao == "la":
        _, registrador_base, label = tokens_da_linha
        registradores_widget.registradores[registrador_base] = registradores_widget.endereco_label[label].get('linha', None)
    if instrucao == "move":
        _, registrador_destino, registrador_base = tokens_da_linha
        # A instrução 'move' copia o valor de um registrador para outro
        registradores_widget.registradores[registrador_destino] = registradores_widget.registradores[registrador_base]

def syscall(registradores_widget, console_widget):
    if registradores_widget.registradores['v0'] == 1:
        console_widget.write(str(registradores_widget.registradores["a0"]) + '\n')
        
    if registradores_widget.registradores['v0'] == 4:  # imprime string
        endereco = registradores_widget.registradores["a0"]
        dicionario = obter_elemento_por_linha(registradores_widget, endereco)

        if dicionario is not None and 'valor' in dicionario:
            string = dicionario['valor']
            console_widget.write(str(string))
        else:
            console_widget.write("Erro: String não encontrada.\n")
    
    if registradores_widget.registradores['v0'] == 5:  # lê int
        console_widget.write("Executando syscall para ler inteiro, clique na tela caso a janela para digitar o valor nao aparecer")
        # Use o simpledialog para obter um inteiro do usuário
        try:
            input_int = tkinter.simpledialog.askinteger("Input", "Digite o inteiro:")
            registradores_widget.registradores['v0'] = input_int
            
        except ValueError:
            console_widget.write("DEBUG: Entrada inválida para inteiro")
    if registradores_widget.registradores['v0'] == 10:  # encerra o programa
        console_widget.write("Programa encerrado")
        return True
    return False