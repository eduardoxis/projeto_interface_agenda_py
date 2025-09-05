import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import calendar
import json
import os
import hashlib

def centralizar_janela(janela):
    """Centraliza uma janela na tela"""
    janela.update_idletasks()
    largura = janela.winfo_width()
    altura = janela.winfo_height()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f'{largura}x{altura}+{x}+{y}')

class LoginWindow:
    def __init__(self):
        """Inicializa a janela de login"""
        self.janela = tk.Tk()
        self.janela.title("Login - Agenda Acadêmica")
        self.janela.geometry("300x200")
        self.janela.resizable(False, False)
        self.janela.configure(bg="#f0f0f0")
        self.janela.attributes("-alpha", 0.9)  # Transparência leve
        
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Agenda Acadêmica", font=('Arial', 14, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos de entrada
        ttk.Label(main_frame, text="Usuário:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_usuario = ttk.Entry(main_frame, width=20)
        self.entry_usuario.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Label(main_frame, text="Senha:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_senha = ttk.Entry(main_frame, width=20, show="*")
        self.entry_senha.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Frame para botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Login", command=self.fazer_login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Registrar", command=self.abrir_registro).pack(side=tk.LEFT, padx=5)
        
        # Configurar pesos para responsividade
        main_frame.columnconfigure(1, weight=1)
        
        # Centralizar a janela
        centralizar_janela(self.janela)
        
        self.usuario = None
        
    def fazer_login(self):
        """Verifica as credenciais do usuário e faz login se forem válidas"""
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        
        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
            
        if self.verificar_credenciais(usuario, senha):
            self.usuario = usuario
            self.janela.destroy()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
            
    def abrir_registro(self):
        """Abre a janela de registro"""
        RegistroWindow(self.janela)
            
    def hash_senha(self, senha):
        """Gera um hash SHA-256 para a senha"""
        return hashlib.sha256(senha.encode()).hexdigest()
            
    def verificar_credenciais(self, usuario, senha):
        """Verifica se o usuário e senha correspondem aos armazenados"""
        if not os.path.exists("usuarios.json"):
            return False
            
        try:
            with open("usuarios.json", "r") as f:
                usuarios = json.load(f)
                if usuario in usuarios and usuarios[usuario]['senha_hash'] == self.hash_senha(senha):
                    return True
            return False
        except:
            return False
        
    def executar(self):
        """Executa la janela de login e retorna o usuário autenticado"""
        self.janela.mainloop()
        return self.usuario

class RegistroWindow:
    def __init__(self, parent):
        """Inicializa a janela de registro"""
        self.janela = tk.Toplevel(parent)
        self.janela.title("Registro - Agenda Acadêmica")
        self.janela.geometry("600x700")
        self.janela.resizable(False, False)
        self.janela.configure(bg="#f0f0f0")
        self.janela.transient(parent)
        self.janela.grab_set()
        
        # Frame principal com scrollbar
        main_frame = ttk.Frame(self.janela, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas e scrollbar para formulário longo
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        titulo = ttk.Label(scrollable_frame, text="Registro de Novo Usuário", font=('Arial', 14, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos de entrada
        campos = [
            ("Nome Completo:", "entry_nome"),
            ("Matrícula:", "entry_matricula"),
            ("Email:", "entry_email"),
            ("Usuário:*", "entry_usuario"),
            ("Senha:*", "entry_senha"),
            ("Confirmar Senha:*", "entry_confirmar_senha")
        ]
        
        self.widgets = {}
        for i, (label_text, widget_name) in enumerate(campos, start=1):
            ttk.Label(scrollable_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=5)
            if "senha" in widget_name:
                widget = ttk.Entry(scrollable_frame, width=30, show="*")
            else:
                widget = ttk.Entry(scrollable_frame, width=30)
            widget.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
            self.widgets[widget_name] = widget
        
        # Curso
        ttk.Label(scrollable_frame, text="Curso:*").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.combo_curso = ttk.Combobox(scrollable_frame, values=[
            "Enfermagem", 
            "Sistema de Informação", 
            "Análise e Desenvolvimento de Sistemas",
            "Direito", 
            "Medicina Veterinária"
        ], width=27)
        self.combo_curso.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Turno
        ttk.Label(scrollable_frame, text="Turno:*").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.combo_turno = ttk.Combobox(scrollable_frame, values=[
            "Matutino", 
            "Noturno"
        ], width=27)
        self.combo_turno.grid(row=8, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Termos de Uso
        ttk.Label(scrollable_frame, text="Termos de Uso:*", font=('Arial', 10, 'bold')).grid(row=9, column=0, sticky=tk.W, pady=(15, 5))
        
        # Área de texto para os termos
        termos_frame = ttk.Frame(scrollable_frame)
        termos_frame.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        termos_texto = scrolledtext.ScrolledText(termos_frame, width=60, height=8, font=('Arial', 9))
        termos_texto.pack(fill=tk.BOTH, expand=True)
        
        # Inserir o texto dos termos
        termos = """# Termo de Uso - Agenda Acadêmica

## Dados Pessoais *

- Nome Completo
- Matrícula
- E-mail
- Usuário
- Senha
- Curso
- Turno

## De acordo - Instruções referente ao uso do sistema: *

- O sistema de agenda acadêmica é de uso exclusivo para alunos da instituição
- Os dados cadastrais serão utilizados apenas para fins acadêmicos
- O usuário é responsável por manter a confidencialidade de sua senha
- A instituição se reserva o direito de suspender contas em caso de uso inadequado
- O sistema armazenará seus eventos e compromissos acadêmicos de forma segura

Ao marcar a caixa abaixo, você declara estar ciente e de acordo com os termos acima."""
        
        termos_texto.insert(tk.END, termos)
        termos_texto.config(state=tk.DISABLED)
        
        # Checkbox de aceitação de termos
        self.var_aceito = tk.BooleanVar()
        checkbox = ttk.Checkbutton(
            scrollable_frame, 
            text="Aceito os termos de uso e política de privacidade", 
            variable=self.var_aceito
        )
        checkbox.grid(row=11, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        # Botões
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.grid(row=12, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Registrar", command=self.registrar_usuario).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.janela.destroy).pack(side=tk.LEFT, padx=5)
        
        # Configurar pesos para responsividade
        scrollable_frame.columnconfigure(1, weight=1)
        termos_frame.columnconfigure(0, weight=1)
        
        # Centralizar a janela
        self.janela.after(100, lambda: centralizar_janela(self.janela))
        
    def hash_senha(self, senha):
        """Gera um hash SHA-256 para a senha"""
        return hashlib.sha256(senha.encode()).hexdigest()
        
    def registrar_usuario(self):
        """Processa o registro do novo usuário"""
        # Obter valores dos campos
        nome = self.widgets['entry_nome'].get().strip()
        matricula = self.widgets['entry_matricula'].get().strip()
        email = self.widgets['entry_email'].get().strip()
        usuario = self.widgets['entry_usuario'].get().strip()
        senha = self.widgets['entry_senha'].get()
        confirmar_senha = self.widgets['entry_confirmar_senha'].get()
        curso = self.combo_curso.get().strip()
        turno = self.combo_turno.get().strip()
        aceito = self.var_aceito.get()
        
        # Validar campos obrigatórios
        if not all([usuario, senha, confirmar_senha, curso, turno, email]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios (*)!")
            return
            
        # Validar comprimento do usuário and senha
        if len(usuario) < 3:
            messagebox.showwarning("Aviso", "O usuário deve ter pelo menos 3 caracteres!")
            return
            
        if len(senha) < 6:
            messagebox.showwarning("Aviso", "A senha deve ter pelo menos 6 caracteres!")
            return
            
        # Validar se as senhas coincidem
        if senha != confirmar_senha:
            messagebox.showwarning("Aviso", "As senhas não coincidem!")
            return
            
        # Validar aceitação dos termos
        if not aceito:
            messagebox.showwarning("Aviso", "Você deve aceitar os termos de uso!")
            return
            
        # Carregar usuários existentes ou criar um dicionário vazio
        if os.path.exists("usuarios.json"):
            try:
                with open("usuarios.json", "r") as f:
                    usuarios = json.load(f)
            except:
                usuarios = {}
        else:
            usuarios = {}
            
        # Verificar se o usuário já existe
        if usuario in usuarios:
            messagebox.showerror("Erro", "Usuário já existe!")
            return
            
        # Verificar se o email já está em uso
        for user_data in usuarios.values():
            # CORREÇÃO: Verificar se user_data é um dicionário antes de usar .get()
            if isinstance(user_data, dict) and user_data.get('email') == email:
                messagebox.showerror("Erro", "Email já está em uso!")
                return
            
        # Adicionar novo usuário
        usuarios[usuario] = {
            'senha_hash': self.hash_senha(senha),
            'nome': nome,
            'matricula': matricula,
            'email': email,
            'curso': curso,
            'turno': turno,
            'data_registro': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Salvar usuários no arquivo
        with open("usuarios.json", "w") as f:
            json.dump(usuarios, f, indent=4)
            
        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
        self.janela.destroy()

class AgendaAcademica:
    def __init__(self, usuario):
        """Inicializa a agenda acadêmica para o usuário especificado"""
        self.janela = tk.Tk()
        self.janela.title(f"Agenda Acadêmica - {usuario}")
        self.janela.geometry("900x600")
        self.janela.configure(bg="#f6f2f2")
        self.janela.resizable(True, True)
        
        # Dados da aplicação
        self.usuario = usuario
        self.data_atual = datetime.now()
        self.eventos = self.carregar_eventos()
        self.info_usuario = self.carregar_info_usuario()
        
        # Configurar estilo visual
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Criar interface gráfica
        self.criar_widgets()
        self.atualizar_calendario()
        
    def carregar_info_usuario(self):
        """Carrega as informações do usuário a partir do arquivo"""
        if os.path.exists("usuarios.json"):
            try:
                with open("usuarios.json", "r") as f:
                    usuarios = json.load(f)
                    return usuarios.get(self.usuario, {})
            except:
                return {}
        return {}
        
    def criar_widgets(self):
        """Cria todos os elementos da interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar pesos para responsividade
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Cabeçalho com navegação e informações do usuário
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Botões de navegação do calendário
        ttk.Button(header_frame, text="<", width=3, command=self.mes_anterior).pack(side=tk.LEFT)
        self.label_mes = ttk.Label(header_frame, text="", font=('Arial', 14, 'bold'))
        self.label_mes.pack(side=tk.LEFT, padx=10)
        ttk.Button(header_frame, text=">", width=3, command=self.proximo_mes).pack(side=tk.LEFT)
        
        # Botão para ir para a data atual
        ttk.Button(header_frame, text="Hoje", command=self.hoje).pack(side=tk.LEFT, padx=10)
        
        # Área do usuário (nome e botão de sair)
        user_frame = ttk.Frame(header_frame)
        user_frame.pack(side=tk.RIGHT)
        
        # Exibir informações do usuário se disponíveis
        user_info = f"{self.usuario}"
        if 'curso' in self.info_usuario:
            user_info += f" | {self.info_usuario['curso']}"
        if 'turno' in self.info_usuario:
            user_info += f" | {self.info_usuario['turno']}"
            
        ttk.Label(user_frame, text=user_info, font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        ttk.Button(user_frame, text="Sair", command=self.sair).pack(side=tk.LEFT, padx=5)
        
        # Botão para adicionar novo evento
        ttk.Button(header_frame, text="+ Novo Evento", command=self.novo_evento).pack(side=tk.RIGHT, padx=(0, 10))
        
        # Frame do calendário
        self.frame_calendario = ttk.Frame(main_frame)
        self.frame_calendario.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Frame da lista de eventos do dia selecionado
        eventos_frame = ttk.LabelFrame(main_frame, text="Eventos do Dia", padding="10")
        eventos_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        eventos_frame.columnconfigure(0, weight=1)
        eventos_frame.rowconfigure(1, weight=1)
        
        # Label para mostrar a data selecionada
        self.label_data_selecionada = ttk.Label(eventos_frame, text="Selecione uma data", font=('Arial', 12, 'bold'))
        self.label_data_selecionada.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Lista de eventos
        self.lista_eventos = tk.Listbox(eventos_frame, height=15, font=('Arial', 10))
        self.lista_eventos.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Frame de botões para gerenciar eventos
        botoes_frame = ttk.Frame(eventos_frame)
        botoes_frame.grid(row=2, column=0, sticky=tk.E)
        
        ttk.Button(botoes_frame, text="Ver Detalhes", command=self.ver_detalhes_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text="Editar", command=self.editar_evento).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text="Excluir", command=self.excluir_evento).pack(side=tk.LEFT, padx=5)
        
        # Rodapé com status
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        self.label_status = ttk.Label(footer_frame, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.label_status.pack(fill=tk.X)
        
        # Variável para armazenar la data selecionada
        self.data_selecionada = None
        
    def sair(self):
        """Fecha a aplicação"""
        self.janela.destroy()
        
    def atualizar_calendario(self):
        """Atualiza a exibição do calendário com o mês/ano atual"""
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
                if dia == 0:  # Dias que não pertencem ao mês atual
                    continue
                    
                # Criar frame para cada dia
                frame_dia = ttk.Frame(self.frame_calendario, relief=tk.RAISED, borderwidth=1)
                frame_dia.grid(row=row, column=col, padx=2, pady=2, sticky=(tk.W, tk.E, tk.N, tk.S))
                frame_dia.columnconfigure(0, weight=1)
                
                # Verificar se é hoje para destacar
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
                
                # Bind de clique para selecionar o dia
                frame_dia.bind("<Button-1>", lambda e, d=dia: self.selecionar_dia(d))
                label_dia.bind("<Button-1>", lambda e, d=dia: self.selecionar_dia(d))
                
        # Configurar tamanho das colunas
        for col in range(7):
            self.frame_calendario.columnconfigure(col, weight=1)
            
    def selecionar_dia(self, dia):
        """Seleciona um dia no calendário e mostra seus eventos"""
        self.data_selecionada = f"{self.data_atual.year}-{self.data_atual.month:02d}-{dia:02d}"
        self.mostrar_eventos_dia()
        
    def mostrar_eventos_dia(self):
        """Mostra os eventos do dia selecionado na lista"""
        if not self.data_selecionada:
            return
            
        # Converter data para formato legível
        data_obj = datetime.strptime(self.data_selecionada, "%Y-%m-%d")
        self.label_data_selecionada.config(text=data_obj.strftime("%d/%m/%Y"))
        
        # Limpar lista de eventos
        self.lista_eventos.delete(0, tk.END)
        
        # Adicionar eventos à lista
        if self.data_selecionada in self.eventos:
            for evento in self.eventos[self.data_selecionada]:
                self.lista_eventos.insert(tk.END, f"{evento['hora']} - {evento['titulo']} ({evento['tipo']})")
        
        # Atualizar status
        self.label_status.config(text=f"Mostrando eventos de {data_obj.strftime('%d/%m/%Y')}")
        
    def novo_evento(self):
        """Abre janela para adicionar um novo evento"""
        if not self.data_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma data primeiro!")
            return
            
        self.janela_evento("Adicionar Evento")
        
    def ver_detalhes_evento(self):
        """Mostra os detalhes do evento selecionado"""
        selecionado = self.lista_eventos.curselection()
        if not selecionado or not self.data_selecionada:
            messagebox.showwarning("Aviso", "Selecione um evento primeiro!")
            return
            
        # Obter evento selecionado
        index = selecionado[0]
        evento = self.eventos[self.data_selecionada][index]
        
        # Montar string com detalhes
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
        """Abre janela para editar evento selecionado"""
        selecionado = self.lista_eventos.curselection()
        if not selecionado or not self.data_selecionada:
            messagebox.showwarning("Aviso", "Selecione um evento primeiro!")
            return
            
        # Armazenar evento selecionado para edição
        index = selecionado[0]
        self.evento_edicao = self.eventos[self.data_selecionada][index]
        self.index_edicao = index
        self.janela_evento("Editar Evento", edicao=True)
        
    def excluir_evento(self):
        """Exclui evento selecionado após confirmação"""
        selecionado = self.lista_eventos.curselection()
        if not selecionado or not self.data_selecionada:
            messagebox.showwarning("Aviso", "Selecione um evento primeiro!")
            return
            
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este evento?"):
            index = selecionado[0]
            # Remover evento
            del self.eventos[self.data_selecionada][index]
            
            # Se não há mais eventos nesta data, remover a data
            if not self.eventos[self.data_selecionada]:
                del self.eventos[self.data_selecionada]
                
            # Salvar e atualizar interface
            self.salvar_eventos()
            self.mostrar_eventos_dia()
            self.atualizar_calendario()
        
    def janela_evento(self, titulo, edicao=False):
        """Cria janela para adicionar/editar eventos"""
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
            """Salva o evento no arquivo"""
            # Validar campos obrigatórios
            if not entry_titulo.get() or not combo_tipo.get() or not entry_data.get() or not entry_hora.get():
                messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios (*)!")
                return
                
            # Criar dicionário com dados do evento
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
        
        # Configurar pesos para responsividade
        frame.columnconfigure(1, weight=1)
        janela.columnconfigure(0, weight=1)
        janela.rowconfigure(0, weight=1)
        
        # Centralizar a janela de evento
        janela.after(100, lambda: centralizar_janela(janela))
        
    def mes_anterior(self):
        """Navega para o mês anterior no calendário"""
        self.data_atual = self.data_atual.replace(day=1) - timedelta(days=1)
        self.atualizar_calendario()
        
    def proximo_mes(self):
        """Navega para o próximo mês no calendário"""
        if self.data_atual.month == 12:
            self.data_atual = self.data_atual.replace(year=self.data_atual.year+1, month=1, day=1)
        else:
            self.data_atual = self.data_atual.replace(month=self.data_atual.month+1, day=1)
        self.atualizar_calendario()
        
    def hoje(self):
        """Volta para a data atual no calendário"""
        self.data_atual = datetime.now()
        self.selecionar_dia(self.data_atual.day)
        self.atualizar_calendario()
        
    def carregar_eventos(self):
        """Carrega os eventos do arquivo do usuário atual"""
        filename = f"eventos_{self.usuario}.json"
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}
        
    def salvar_eventos(self):
        """Salva os eventos no arquivo do usuário atual"""
        filename = f"eventos_{self.usuario}.json"
        with open(filename, "w") as f:
            json.dump(self.eventos, f, indent=4)

    def executar(self):
        """Executa a aplicação principal"""
        # Centralizar a janela
        centralizar_janela(self.janela)
        self.janela.mainloop()

# Ponto de entrada da aplicação
if __name__ == "__main__":
    # Primeiro, exibir a janela de login
    login = LoginWindow()
    usuario = login.executar()
    
    # Se o login foi bem-sucedido, iniciar a agenda acadêmica
    if usuario:
        app = AgendaAcademica(usuario)
        app.executar()