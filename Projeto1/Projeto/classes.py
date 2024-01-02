import tkinter as tk

class BlocoTraducao(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.config(bg="#2C3E50", width=100, height=100)
        self.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        # Crie um widget para exibir a tradução binária
        self.traducao_texto = tk.Text(self, bg="#2C3E50", fg="#ECF0F1", font=("monaco", 14), state=tk.DISABLED)
        self.traducao_texto.pack(fill=tk.BOTH, expand=False)
        
    def limpar_traducao(self):
        self.traducao_texto.config(state=tk.NORMAL)
        self.traducao_texto.delete(1.0, tk.END)
        self.traducao_texto.config(state=tk.DISABLED)
        
    def write(self, text):
        self.traducao_texto.config(state=tk.NORMAL)
        self.traducao_texto.insert(tk.END, text+'\n')
        self.traducao_texto.config(state=tk.DISABLED)

class MemoriaWidget(tk.Frame):
    def __init__(self, master=None, tamanho_em_bytes=4096):
        super().__init__(master)
        self.tamanho_em_bytes = tamanho_em_bytes
        self.memoria = bytearray(tamanho_em_bytes)
        # Adiciona um Text Widget para exibir dados da memória
        self.text_area = tk.Text(self, wrap=tk.NONE, bg="#2C3E50", fg="#ECF0F1", font=("monaco", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH)

        self.atualizar_memoria_na_gui()

    def atualizar_memoria_na_gui(self):
        self.text_area.delete("1.0", tk.END)
        for i in range(len(self.memoria) + 4):
            linha = self.memoria[i:i+4]
            hex_string = ' '.join(f'{byte:04X}' for byte in linha)
            endereco = i
            texto = f'{endereco:03X}: {hex_string}\n'
            self.text_area.insert(tk.END, texto)

    def read_word(self, endereco, offset):
        # Lê uma palavra (4 bytes) da memória no endereço fornecido com um offset
        endereco_final = endereco + offset
        tam = len(self.memoria)
        print(tam)
        if 0 <= endereco_final < len(self.memoria):
            palavra_bytes = self.memoria[endereco_final:endereco + 4]
            # Converte os 4 bytes para um número inteiro (assumindo endianness little-endian)
            palavra = int.from_bytes(palavra_bytes, byteorder='little')
            return palavra
        else:
            # Levanta uma exceção em vez de imprimir
            raise ValueError(f"Endereço inválido - {endereco_final}")

    def write_word(self, endereco, valor, offset):
        # Escreve uma palavra (4 bytes) na memória no endereço fornecido com um offset
        endereco_final = endereco + offset
        if 0 <= endereco_final < len(self.memoria):
            # Converte o valor para bytes (assumindo endianness little-endian)
            valor_bytes = valor.to_bytes(4, byteorder='little')
            # Escreve os bytes na memória
            self.memoria[endereco_final:endereco + 4] = valor_bytes
            self.atualizar_memoria_na_gui()  # Atualiza a GUI após escrever na memória
        else:
            # Levanta uma exceção em vez de imprimir
            raise ValueError(f"Endereço inválido - {endereco_final}")

    def zerar_memoria(self):
        self.memoria = bytearray(self.tamanho_em_bytes)
        self.atualizar_memoria_na_gui()
        
class ConsoleWidget(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.config(bg="black")
        self.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)
        self.text_widget = tk.Text(self, bg="#000000", fg="#27AE60", font=("monaco", 14), state=tk.DISABLED)
        self.text_widget.pack(fill=tk.BOTH, expand=True)

    def clear(self):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.config(state=tk.DISABLED)

    def write(self, text):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, text+'\n')
        self.text_widget.config(state=tk.DISABLED)

class RegistradoresWidget(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.config(bg="#34495E", width=200, height=200)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.registradores = {
            "PC": 0, "zero": 0, "at": 0, "v0": 0, 
            "v1": 0, "a0": 0, "a1": 0, "a2": 0,
            "a3": 0, "t0": 0, "t1": 0, "t2": 0,
            "t3": 0, "t4": 0, "t5": 0, "t6": 0,
            "t7": 0, "s0": 0, "s1": 0, "s2": 0,
            "s3": 0, "s4": 0, "s5": 0, "s6": 0,
            "s7": 0, "t8": 0, "t9": 0, "k0": 0,
            "k1": 0, "gp": 0, "sp": 0, "s8": 0,
            "ra": 0
        }
        self.endereco_label = {}
        
        self.labels_registradores = {}
        for registrador, valor in self.registradores.items():
            lbl = tk.Label(self, text=f"{registrador} = {valor}", bg="#34495E", fg="#ECF0F1", padx=1, pady=1)
            lbl.pack(fill=tk.X)
            self.labels_registradores[registrador] = lbl

    def atualizar_registradores_na_gui(self):
        for nome_registrador, label in self.labels_registradores.items():
            valor = self.registradores[nome_registrador]
            if self.registradores["zero"] != 0:
                self.registradores["zero"] = 0
            label.config(text=f"{nome_registrador} = {valor}")

    def zerar_registradores(self):
        for nome_registrador in self.registradores:
            self.registradores[nome_registrador] = 0
            if nome_registrador == "sp":
                self.registradores["sp"] = 0
        self.atualizar_registradores_na_gui()