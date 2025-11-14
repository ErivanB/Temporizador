import tkinter as tk
from datetime import datetime, timedelta

class Cronometro:
    def __init__(self, root):
        self.root = root
        self.root.title("Cronômetro")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        # Variáveis de controle
        self.executando = False
        self.tempo_inicial = None
        self.tempo_decorrido = timedelta(0)

        # Interface
        self.criar_interface()

    def criar_interface(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')

        # Display do tempo
        self.label_tempo = tk.Label(
            main_frame,
            text="00:00:00.000",
            font=("Arial", 24, "bold"),
            fg="#2E8B57",
            bg="#F0F0F0",
            relief="sunken",
            bd=2,
            padx=10,
            pady=10
        )
        self.label_tempo.pack(pady=20)

        # Frame dos botões
        frame_botoes = tk.Frame(main_frame)
        frame_botoes.pack(pady=10)

        # Botão Iniciar
        self.btn_iniciar = tk.Button(
            frame_botoes,
            text="Iniciar",
            command=self.iniciar,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            width=8,
            height=2
        )
        self.btn_iniciar.pack(side="left", padx=5)

        # Botão Pausar
        self.btn_pausar = tk.Button(
            frame_botoes,
            text="Pausar",
            command=self.pausar,
            bg="#FF9800",
            fg="white",
            font=("Arial", 12, "bold"),
            width=8,
            height=2,
            state="disabled"
        )
        self.btn_pausar.pack(side="left", padx=5)

        # Botão Reiniciar
        self.btn_reiniciar = tk.Button(
            frame_botoes,
            text="Reiniciar",
            command=self.reiniciar,
            bg="#F44336",
            fg="white",
            font=("Arial", 12, "bold"),
            width=8,
            height=2
        )
        self.btn_reiniciar.pack(side="left", padx=5)

        # Frame dos tempos parciais
        frame_parciais = tk.Frame(main_frame)
        frame_parciais.pack(pady=10, fill='x')

        # Botão Tempo Parcial
        self.btn_parcial = tk.Button(
            frame_parciais,
            text="Tempo Parcial",
            command=self.marcar_parcial,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            state="disabled"
        )
        self.btn_parcial.pack(side="left", padx=5)

        # Lista de tempos parciais
        self.lista_parciais = tk.Listbox(
            frame_parciais,
            height=4,
            width=15,
            font=("Arial", 8)
        )
        self.lista_parciais.pack(side="right", padx=5, fill='x', expand=True)

    def formatar_tempo(self, tempo_delta):
        """Formata o timedelta para o formato HH:MM:SS.mmm"""
        total_segundos = int(tempo_delta.total_seconds())
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60
        milissegundos = tempo_delta.microseconds // 1000

        return f"{horas:02d}:{minutos:02d}:{segundos:02d}.{milissegundos:03d}"

    def atualizar_tempo(self):
        """Atualiza o display do tempo"""
        if self.executando:
            tempo_atual = datetime.now() - self.tempo_inicial + self.tempo_decorrido
            self.label_tempo.config(text=self.formatar_tempo(tempo_atual))
            self.root.after(10, self.atualizar_tempo)  # Atualiza a cada 10ms

    def iniciar(self):
        """Inicia o cronômetro"""
        if not self.executando:
            self.executando = True
            self.tempo_inicial = datetime.now()
            self.atualizar_tempo()

            # Atualiza estados dos botões
            self.btn_iniciar.config(state="disabled")
            self.btn_pausar.config(state="normal")
            self.btn_parcial.config(state="normal")

    def pausar(self):
        """Pausa o cronômetro"""
        if self.executando:
            self.executando = False
            self.tempo_decorrido += datetime.now() - self.tempo_inicial

            # Atualiza estados dos botões
            self.btn_iniciar.config(state="normal")
            self.btn_pausar.config(state="disabled")

    def reiniciar(self):
        """Reinicia o cronômetro"""
        self.executando = False
        self.tempo_inicial = None
        self.tempo_decorrido = timedelta(0)
        self.label_tempo.config(text="00:00:00.000")
        self.lista_parciais.delete(0, tk.END)

        # Atualiza estados dos botões
        self.btn_iniciar.config(state="normal")
        self.btn_pausar.config(state="disabled")
        self.btn_parcial.config(state="disabled")

    def marcar_parcial(self):
        """Marca um tempo parcial"""
        if self.executando:
            tempo_atual = datetime.now() - self.tempo_inicial + self.tempo_decorrido
            tempo_formatado = self.formatar_tempo(tempo_atual)

            # Adiciona à lista de tempos parciais
            numero_parcial = self.lista_parciais.size() + 1
            self.lista_parciais.insert(tk.END, f"Parcial {numero_parcial}: {tempo_formatado}")

            # Rola para o final da lista
            self.lista_parciais.see(tk.END)

def main():
    root = tk.Tk()
    app = Cronometro(root)
    root.mainloop()

if __name__ == "__main__":
    main()