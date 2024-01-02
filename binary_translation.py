instrucoes_r = {
    'add': '000000 rs rt rd 00000 100000',
    'sub': '000000 rs rt rd 00000 100010',
    'mul': '000000 rs rt rd 00000 011000',
    'div': '000000 rs rt rd 00000 011010',
    'and': '000000 rs rt rd 00000 100100', 
    'or':  '000000 rs rt rd 00000 100101',
    'xor': '000000 rs rt rd 00000 100110', 
    'nor': '000000 rs rt rd 00000 100111', 
    'sll': '000000 00000 rt rd shamt 000000', 
    'sra': '000000 00000 rt rd shamt 000011', 
    'slt': '000000 rs rt rd shamt 101010', 
    'move':'000000 rs rt rd 00000 100000' 
}

instrucoes_i = {
    'addi': '001000 rs rt immediate',
    'subi': '001001 rs rt immediate',
    'li': '001001 rs rt immediate',
    'lw': '100011 base rt offset',
    'sw': '101011 base rt offset',
}

instrucoes_j = {
    'j': '000010 address',
    'jal': '000011 address',
}

instrucoes_especiais = {
    'jr': '000000 rs 00000 00000 00000 001000',
}
instrucoes_branch = {
    'beq': '000100 rs rt address',
    'bne': '000101 rs rt address',
    'blt': '000110 rs rt address',
    'bgt': '000111 rs rt address',
    'bge': '000101 rs rt address',

}

def traduzir_instrucao_jr(*operandos, mapeamento_registradores):
    # Verifica se o número correto de operandos foi fornecido
    if len(operandos) == 1:
        registrador_rs = operandos[0]
        
        # Verifica se o registrador rs é válido
        if registrador_rs in mapeamento_registradores:
            # Obtém o formato da instrução JR
            formato = '000000 rs 00000 00000 00000 001000'
            
            # Preenche os campos do formato com os valores fornecidos
            binario = formato.replace('rs', mapeamento_registradores.get(registrador_rs, '00000'))
            binario = binario.replace(" ", "")
            return binario
        else:
            raise ValueError(f"Registrador não reconhecido: {registrador_rs}")
    else:
        raise ValueError("A instrução 'jr' requer um operando: registrador_rs")

def traduzir_instrucao_branch(instrucao, *operandos, mapeamento_registradores, registradores_widget):
    formato = instrucoes_branch.get(instrucao, None)
    if formato:
        # Certifique-se de que há três operandos (registrador_rs, registrador_rt e endereço)
        if len(operandos) == 3:
            registrador_rs, registrador_rt, label = operandos
            endereco_label = registradores_widget.endereco_label.get(label, None)
            
            if endereco_label is not None:
                # Verifica se o valor associado à label é um dicionário ou um valor direto
                if isinstance(endereco_label, dict):
                    endereco = endereco_label.get('linha', None)
                else:
                    endereco = endereco_label

                binario = formato.replace('rs', mapeamento_registradores.get(registrador_rs, '00000'))
                binario = binario.replace('rt', mapeamento_registradores.get(registrador_rt, '00000'))
                binario = binario.replace('address', format(endereco, '016b'))
                binario = binario.replace(" ", "")
                print(binario)
                return binario
            else:
                raise ValueError(f"Label não encontrada: {label}")
        else:
            raise ValueError(f"Instrução branch requer três operandos: registrador_rs, registrador_rt e endereço")
    else:
        raise ValueError(f"Instrução branch não reconhecida: {instrucao}")

def traduzir_instrucao_i(instrucao, *operandos, mapeamento_registradores):

    if instrucao == 'li':
        # Instrução 'li' é tratada de forma diferente
        if len(operandos) == 2:  # Verifica se há dois operandos (registrador_rd e imediate)
            registrador_rd, imediate = operandos
            binario = instrucoes_i['li'].replace('rs', '00000')
            binario = binario.replace('rt', mapeamento_registradores.get(registrador_rd, '00000'))
            binario = binario.replace('immediate', format(int(imediate), '016b'))
            binario = binario.replace(" ", "")
            return binario
        else:
            raise ValueError("Instrução 'li' requer dois operandos: registrador_rd e imediate")

    if instrucao in ['lw', 'sw']:
        # Instruções lw e sw
        registrador_rt, offset, endereco_base = operandos
        binario = instrucoes_i[instrucao].replace('base', mapeamento_registradores.get(endereco_base, '00000'))
        binario = binario.replace('rt', mapeamento_registradores.get(registrador_rt, '00000'))
        binario = binario.replace('offset', format(int(offset), '016b'))
        binario = binario.replace(" ", "")
        return binario
    
    if instrucao in ['addi', 'subi']:
        registrador_rt, registrador_rd, imediate = operandos
        binario = instrucoes_i[instrucao].replace('rt', mapeamento_registradores.get(registrador_rt))
        binario = binario.replace('rs', mapeamento_registradores.get(registrador_rd))
        binario = binario.replace('immediate', format(int(imediate), '016b'))
        binario = binario.replace(" ", "")
        return binario
    else:
        raise ValueError(f"Instrução I não reconhecida: {instrucao}")

def traduzir_instrucao_j(instrucao, address, registradores_widget):
    # Obtém o formato da instrução J correspondente
    formato = instrucoes_j.get(instrucao, None)
    address = registradores_widget.endereco_label[address].get('linha', None)
    if formato:
        # Preenche os campos do formato com os valores fornecidos
        binario = formato.replace('address', format(address, '026b'))
        binario = binario.replace(" ", "")
        return binario
    else:
        raise ValueError(f"Instrução J não reconhecida: {instrucao}")

def traduzir_instrucao_r(instrucao, *operandos, mapeamento_registradores):
    # Obtém o formato da instrução R correspondente
    formato = instrucoes_r.get(instrucao, None)

    if instrucao == 'move':
        # Instrução 'move' é tratada como uma cópia direta do registrador rs para o registrador rd
        formato_move = instrucoes_r.get(instrucao, None)
        if formato_move:
            binario = formato_move.replace('rs', mapeamento_registradores.get(operandos[0], '00000'))
            binario = binario.replace('rd', mapeamento_registradores.get(operandos[1], '00000'))
            binario = binario.replace('rt', '00000')  # Registrador rt é ignorado na pseudoinstrução 'move'
            binario = binario.replace(" ", "")
            return binario

    # Tenta converter o registrador_rt em um valor inteiro (somente se a instrução exigir shamt)
    shamt = 0
    if formato:
        # Preenche os campos do formato com os valores fornecidos
        binario = formato.replace('rs', mapeamento_registradores.get(operandos[0], '00000'))
        binario = binario.replace('rt', mapeamento_registradores.get(operandos[2], '00000'))
        binario = binario.replace('rd', mapeamento_registradores.get(operandos[1], '00000'))
        binario = binario.replace(" ", "")
        # Adiciona a lógica para distinguir e preencher os campos específicos
        if instrucao in {'sll', 'sra'}:
            if formato and 'shamt' in formato:
                shamt = int(operandos[2])
            binario = binario.replace('shamt', format(int(shamt), '05b'))
            binario = binario.replace('funct', '000000' if instrucao == 'sll' else '000011')
            binario = binario.replace(" ", "")
        if instrucao == 'slt':
            binario = binario.replace('shamt', '00000')
            binario = binario.replace('funct', '101010')
            binario = binario.replace(" ", "")
        else:
            pass  # Adicione lógica para outros tipos de instruções R, se necessário
        return binario
    else:
        raise ValueError(f"Instrução R não reconhecida: {instrucao}")

def traduzir_instrucao(linha_atual, registradores_widget):
    mapeamento_registradores = {
    'zero':'00000', 'at':'00001',
    'v0': '00010', 'v1': '00011',
    'a0': '00100', 'a1': '00101', 
    'a2': '00110', 'a3': '00111',
    't0': '01000', 't1': '01001', 
    't2': '01010', 't3': '01011',
    't4': '01100', 't5': '01101', 
    't6': '01110', 't7': '01111',
    's0': '10000', 's1': '10001', 
    's2': '10010', 's3': '10011',
    's4': '10100', 's5': '10101', 
    's6': '10110', 's7': '10111',
    't8': '11000', 't9': '11001',
    'k0': '11010', 'k1': '11011',
    'gp': '11100', 'sp': '11101', 
    'fp': '11110', 'ra': '11111'
}
    linha_atual = [t[0] for t in linha_atual if t[0] and t[1] not in ['COMMA', 'COMMENT', 'SPACE', 'LPAREN', 'RPAREN']]
    linha_atual = list(filter(lambda x: ' ' not in x[0], linha_atual))
    linha_atual = [t.replace('$', '') if t.startswith('$') else t for t in linha_atual]
    instrucao, *operandos = linha_atual

    if instrucao in instrucoes_r:
        return traduzir_instrucao_r(instrucao, *operandos, mapeamento_registradores=mapeamento_registradores)
    
    elif instrucao in instrucoes_i:        
        return traduzir_instrucao_i(instrucao, *operandos, mapeamento_registradores=mapeamento_registradores)

    elif instrucao in instrucoes_j:
        return traduzir_instrucao_j(instrucao, *operandos, registradores_widget=registradores_widget)
    
    elif instrucao in instrucoes_branch:
        return traduzir_instrucao_branch(instrucao, *operandos, mapeamento_registradores=mapeamento_registradores, registradores_widget=registradores_widget)
   
    elif instrucao in instrucoes_especiais:
        return traduzir_instrucao_jr(*operandos, mapeamento_registradores=mapeamento_registradores)
    
    elif instrucao == 'la':
       return '00000000000000000000000000000000'