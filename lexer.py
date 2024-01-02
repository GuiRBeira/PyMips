import re
from validator import validar_codigo

def processar_codigo(codigo, registradores_widget, console_widget, traducao_widget, memoria_widget,modo_debug):
    token_patterns = [
    (r'[a-zA-Z]\w*:', 'LABEL'),
    (r'^(addi|subi|sll|sra|add|sub|mul|div|and|or|xor|nor|slt|j|jal|jr|beq|bne|blt|li|lw|sw|la|move)\b', 'INSTRUCTION'),
    (r'-?\b\d+\b', 'IMMEDIATE'),
    (r'\$[a-z0-9]+', 'REGISTER'), 
    (r',', 'COMMA'),          
    (r'#.*', 'COMMENT'),
    (r'\s+', 'SPACE'),
    (r'\.data', 'DATA'),
    (r'\.text', 'TEXT'),
    (r'\.asciiz\s+"([^"]*)"', 'ASCIIZ'),
    (r'syscall', 'SYSCALL'),
    (r'\b[a-zA-Z]\w*\b', 'DESTLABEL'),
     (r'\(', 'LPAREN'), 
    (r'\)', 'RPAREN'),  
    ]

    tokens = []
    for i, line in enumerate(codigo.split('\n'), 1):
        line = line.strip()
        position = 0
        while position < len(line):
            matched = False
            for pattern, token_type in token_patterns:
                regex = re.compile(pattern)
                match = regex.match(line, position)
                if match:
                    value = match.group(0)
                    tokens.append((value, token_type, i))
                    position = match.end()
                    matched = True
                    break
            if not matched:
                console_widget.write(f"Erro na linha {i}: Caractere inesperado '{line[position:]}'")
    validar_codigo(tokens, registradores_widget, console_widget,traducao_widget, memoria_widget,modo_debug)