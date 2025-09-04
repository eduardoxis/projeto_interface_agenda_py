import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar
import json
import os

class AgendaAcademica:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Agenda Acadêmica")
        self.janela.geometry("900x600")
        self.janela.configure(bg="#f6f2f2")
        self.janela.resizable(True,True )
        
        # Dados
        self.data_atual = datetime.now()
        self.eventos = self.carregar_eventos()
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Criar interface
        self.criar_widgets()
        self.atualizar_calendario()
        
    def criar_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar pesos
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Cabeçalho com navegação
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        ttk.Button(header_frame, text="<", width=3, command=self.mes_anterior).pack(side=tk.LEFT)
        self.label_mes = ttk.Label(header_frame, text="", font=('Arial', 14, 'bold'))
        self.label_mes.pack(side=tk.LEFT, padx=10)
        ttk.Button(header_frame, text=">", width=3, command=self.proximo_mes).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text="Hoje", command=self.hoje).pack(side=tk.LEFT, padx=10)
        ttk.Button(header_frame, text="+ Novo Evento", command=self.novo_evento).pack(side=tk.RIGHT)
        
        # Calendário
        self.frame_calendario = ttk.Frame(main_frame)
        self.frame_calendario.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Lista de eventos do dia selecionado
        eventos_frame = ttk.LabelFrame(main_frame, text="Eventos do Dia", padding="10")
        eventos_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        eventos_frame.columnconfigure(0, weight=1)
        eventos_frame.rowconfigure(1, weight=1)
        
        self.label_data_selecionada = ttk.Label(eventos_frame, text="Selecione uma data", font=('Arial', 12, 'bold'))
        self.label_data_selecionada.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Lista de eventos
        self.lista_eventos = tk.Listbox(eventos_frame, height=15, font=('Arial', 10))
        self.lista_eventos.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Frame de botões para eventos
        botoes_frame = ttk.Frame(eventos_frame)
        botoes_frame.grid(row=2, column=0, sticky=tk.E)
        
        ttk.Button(botoes_frame, text="Ver Detalhes", command=self.ver_detalhes_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text="Editar", command=self.editar_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text="Excluir", command=self.excluir_evento).pack(side=tk.LEFT, padx=5)
        
        # Rodapé
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        self.label_status = ttk.Label(footer_frame, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.label_status.pack(fill=tk.X)
        
        # Bind para seleção de data
        self.data_selecionada = None
        
    def atualizar_calendario(self):
        # Limpar calendário anterior
        for widget in self.frame_calendario.winfo_children():
            widget.destroy()
            
        # Atualizar label do mês/ano
        self.label_mes.config(text=self.data_atual.strftime("%B %Y").title())
        
        # Obter informações do mês
        cal = calendar.monthcalendar(self.data_atual.year, self.data_atual.month)
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        
        # Adicionar cabeçalho dos dias da semana
        for i, dia in enumerate(dias_semana):
            label = ttk.Label(self.frame_calendario, text=dia, font=('Arial', 10, 'bold'))
            label.grid(row=0, column=i, padx=2, pady=2)
            
        # Adicionar dias do mês
        for row, semana in enumerate(cal, start=1):
            for col, dia in enumerate(semana):
                if dia == 0:
                    continue
                    
                frame_dia = ttk.Frame(self.frame_calendario, relief=tk.RAISED, borderwidth=1)
                frame_dia.grid(row=row, column=col, padx=2, pady=2, sticky=(tk.W, tk.E, tk.N, tk.S))
                frame_dia.columnconfigure(0, weight=1)
                
                # Verificar se é hoje
                hoje = datetime.now()
                estilo = 'TLabel'
                if dia == hoje.day and self.data_atual.month == hoje.month and self.data_atual.year == hoje.year:
                    frame_dia.configure(style='Accent.TFrame')
                    estilo = 'Accent.TLabel'
                
                # Label do dia
                label_dia = ttk.Label(frame_dia, text=str(dia), style=estilo)
                label_dia.grid(row=0, column=0, sticky=tk.W)
                
                # Verificar se há eventos neste dia
                data_str = f"{self.data_atual.year}-{self.data_atual.month:02d}-{dia:02d}"
                if data_str in self.eventos:
                    # Mostrar quantos eventos existem
                    num_eventos = len(self.eventos[data_str])
                    label_eventos = ttk.Label(frame_dia, text=f"{num_eventos} evento(s)", style=estilo, font=('Arial', 7))
                    label_eventos.grid(row=1, column=0, sticky=tk.W)
                
                # Bind de clique
                frame_dia.bind("<Button-1>", lambda e, d=dia: self.selecionar_dia(d))
                label_dia.bind("<Button-1>", lambda e, d=dia: self.selecionar_dia(d))
                
        # Configurar tamanho das colunas
        for col in range(7):
            self.frame_calendario.columnconfigure(col, weight=1)
            
    def selecionar_dia(self, dia):
        self.data_selecionada = f"{self.data_atual.year}-{self.data_atual.month:02d}-{dia:02d}"
        self.mostrar_eventos_dia()
        
    def mostrar_eventos_dia(self):
        if not self.data_selecionada:
            return
            
        data_obj = datetime.strptime(self.data_selecionada, "%Y-%m-%d")
        self.label_data_selecionada.config(text=data_obj.strftime("%d/%m/%Y"))
        
        # Limpar lista
        self.lista_eventos.delete(0, tk.END)
        
        # Adicionar eventos
        if self.data_selecionada in self.eventos:
            for evento in self.eventos[self.data_selecionada]:
                self.lista_eventos.insert(tk.END, f"{evento['hora']}p - {evento['titulo']} ({evento['tipo']})")
        
        self.label_status.config(text=f"Mostrando Eventos de {data_obj.strftime('%d/%m/%Y')}")
        
    def novo_evento(self):
        if not self.data_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma data primeiro!")
            return
            
        self.janela_evento("Adicionar Evento")
        
    def ver_detalhes_evento(self):
        selecionado = self.lista_eventos.curselection()
        if not selecionado or not self.data_selecionada:
            messagebox.showwarning("Aviso", "Selecione um evento primeiro!")
            return
            
        index = selecionado[0]
        evento = self.eventos[self.data_selecionada][index]
        
        detalhes = f"""
Título: {evento['titulo']}
Tipo: {evento['tipo']}
Data: {self.data_selecionada}
Hora: {evento['hora']}
Descrição: {evento['descricao']}
Disciplina: {evento['disciplina']}
"""
        messagebox.showinfo("Detalhes do Evento", detalhes)
        
    def editar_evento(self):
        selecionado = self.lista_eventos.curselection()
        if not selecionado or not self.data_selecionada:
            messagebox.showwarning("Aviso", "Selecione um evento primeiro!")
            return
            
        index = selecionado[0]
        self.evento_edicao = self.eventos[self.data_selecionada][index]
        self.index_edicao = index
        self.janela_evento("Editar Evento", edicao=True)
        
    def excluir_evento(self):
        selecionado = self.lista_eventos.curselection()
        if not selecionado or not self.data_selecionada:
            messagebox.showwarning("Aviso", "Selecione um evento primeiro!")
            return
            
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este evento?"):
            index = selecionado[0]
            del self.eventos[self.data_selecionada][index]
            
            # Se não há mais eventos nesta data, remover a data
            if not self.eventos[self.data_selecionada]:
                del self.eventos[self.data_selecionada]
                
            self.salvar_eventos()
            self.mostrar_eventos_dia()
            self.atualizar_calendario()
        
    def janela_evento(self, titulo, edicao=False):
        janela = tk.Toplevel(self.janela)
        janela.title(titulo)
        janela.geometry("400x500")
        janela.transient(self.janela)
        janela.grab_set()
        
        # Frame principal
        frame = ttk.Frame(janela, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos do formulário
        ttk.Label(frame, text="Título:*").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        entry_titulo = ttk.Entry(frame, width=30)
        entry_titulo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(5, 0))
        
        ttk.Label(frame, text="Tipo:*").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        combo_tipo = ttk.Combobox(frame, values=["Prova", "Trabalho", "Entrega", "Apresentação", "Reunião", "Outro"])
        combo_tipo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(5, 0))
        
        ttk.Label(frame, text="Disciplina:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        entry_disciplina = ttk.Entry(frame, width=30)
        entry_disciplina.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(5, 0))
        
        ttk.Label(frame, text="Data:*").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        entry_data = ttk.Entry(frame, width=30)
        entry_data.insert(0, self.data_selecionada)
        entry_data.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(5, 0))
        
        ttk.Label(frame, text="Hora:*").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        entry_hora = ttk.Entry(frame, width=30)
        entry_hora.insert(0, "08:00")
        entry_hora.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(5, 0))
        
        ttk.Label(frame, text="Descrição:").grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        text_descricao = tk.Text(frame, width=30, height=5)
        text_descricao.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(5, 0))
        
        # Preencher campos se for edição
        if edicao:
            entry_titulo.insert(0, self.evento_edicao['titulo'])
            combo_tipo.set(self.evento_edicao['tipo'])
            entry_disciplina.insert(0, self.evento_edicao['disciplina'])
            entry_data.delete(0, tk.END)
            entry_data.insert(0, self.data_selecionada)
            entry_hora.delete(0, tk.END)
            entry_hora.insert(0, self.evento_edicao['hora'])
            text_descricao.insert("1.0", self.evento_edicao['descricao'])
        
        # Botões
        botoes_frame = ttk.Frame(frame)
        botoes_frame.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        def salvar():
            # Validar campos obrigatórios
            if not entry_titulo.get() or not combo_tipo.get() or not entry_data.get() or not entry_hora.get():
                messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios (*)!")
                return
                
            evento = {
                'titulo': entry_titulo.get(),
                'tipo': combo_tipo.get(),
                'disciplina': entry_disciplina.get(),
                'hora': entry_hora.get(),
                'descricao': text_descricao.get("1.0", tk.END).strip()
            }
            
            data_evento = entry_data.get()
            
            if edicao:
                # Remover evento antigo
                del self.eventos[self.data_selecionada][self.index_edicao]
                
                # Se não há mais eventos na data antiga, remover a data
                if not self.eventos[self.data_selecionada]:
                    del self.eventos[self.data_selecionada]
            
            # Adicionar evento à data
            if data_evento not in self.eventos:
                self.eventos[data_evento] = []
                
            self.eventos[data_evento].append(evento)
            self.salvar_eventos()
            
            # Atualizar interface
            if data_evento == self.data_selecionada:
                self.mostrar_eventos_dia()
            self.atualizar_calendario()
            
            janela.destroy()
            messagebox.showinfo("Sucesso", "Evento salvo com sucesso!")
        
        ttk.Button(botoes_frame, text="Salvar", command=salvar).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text="Cancelar", command=janela.destroy).pack(side=tk.LEFT, padx=5)
        
        # Configurar pesos
        frame.columnconfigure(1, weight=1)
        janela.columnconfigure(0, weight=1)
        janela.rowconfigure(0, weight=1)
        
    def mes_anterior(self):
        self.data_atual = self.data_atual.replace(day=1) - timedelta(days=1)
        self.atualizar_calendario()
        
    def proximo_mes(self):
        if self.data_atual.month == 12:
            self.data_atual = self.data_atual.replace(year=self.data_atual.year+1, month=1, day=1)
        else:
            self.data_atual = self.data_atual.replace(month=self.data_atual.month+1, day=1)
        self.atualizar_calendario()
        
    def hoje(self):
        self.data_atual = datetime.now()
        self.selecionar_dia(self.data_atual.day)
        self.atualizar_calendario()
        
    def carregar_eventos(self):
        if os.path.exists("eventos.json"):
            try:
                with open("eventos.json", "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}
        
    def salvar_eventos(self):
        with open("eventos.json", "w") as f:
            json.dump(self.eventos, f)

            
            
    def executar(self):
        # Centralizar a janela
        self.janela.eval('tk::PlaceWindow . center')
        self.janela.mainloop()

# Executar a aplicação
if __name__ == "__main__":
    app = AgendaAcademica()
    app.executar()
    