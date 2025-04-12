import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import configparser
import subprocess
import threading
import datetime
import zipfile
import shutil
import time
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("minecraft_backup.log"),
        logging.StreamHandler()
    ]
)

class MinecraftBackupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Bedrock Server Backup")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variáveis para armazenar configurações
        self.server_path_var = tk.StringVar()
        self.backup_path_var = tk.StringVar()
        self.max_backups_var = tk.StringVar(value="5")
        self.backup_interval_var = tk.StringVar(value="24")
        self.world_name_var = tk.StringVar(value="Bedrock level")
        
        # Variável para controlar o agendamento
        self.schedule_running = False
        self.schedule_thread = None
        
        # Carregar configurações existentes
        self.config_path = "backup_config.ini"
        self.load_config()
        
        # Criar interface
        self.create_widgets()
        
    def load_config(self):
        """Carrega configurações do arquivo ou cria padrões se não existir"""
        config = configparser.ConfigParser()
        
        if os.path.exists(self.config_path):
            config.read(self.config_path)
            if 'Settings' in config:
                self.server_path_var.set(config['Settings'].get('ServerPath', ''))
                self.backup_path_var.set(config['Settings'].get('BackupPath', ''))
                self.max_backups_var.set(config['Settings'].get('MaxBackups', '5'))
                self.backup_interval_var.set(config['Settings'].get('BackupInterval', '24'))
                self.world_name_var.set(config['Settings'].get('WorldName', 'Bedrock level'))
    
    def save_config(self):
        """Salva configurações no arquivo"""
        config = configparser.ConfigParser()
        config['Settings'] = {
            'ServerPath': self.server_path_var.get(),
            'BackupPath': self.backup_path_var.get(),
            'MaxBackups': self.max_backups_var.get(),
            'BackupInterval': self.backup_interval_var.get(),
            'WorldName': self.world_name_var.get()
        }
        
        with open(self.config_path, 'w') as f:
            config.write(f)
        
        messagebox.showinfo("Configuração", "Configurações salvas com sucesso!")
    
    def create_widgets(self):
        """Cria os elementos da interface gráfica"""
        # Frame principal com padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Estilo para títulos
        title_style = ttk.Style()
        title_style.configure("Title.TLabel", font=("Arial", 14, "bold"))
        
        # Título
        title_label = ttk.Label(main_frame, text="Configuração de Backup - Minecraft Bedrock Server", style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Frame para configurações
        config_frame = ttk.LabelFrame(main_frame, text="Configurações", padding="10")
        config_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Grid para organizar os campos
        config_frame.columnconfigure(1, weight=1)
        
        # Caminho do servidor
        ttk.Label(config_frame, text="Pasta do Servidor:").grid(row=0, column=0, sticky=tk.W, pady=5)
        server_entry = ttk.Entry(config_frame, textvariable=self.server_path_var, width=50)
        server_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(config_frame, text="Procurar", command=self.browse_server_path).grid(row=0, column=2, padx=5, pady=5)
        
        # Caminho dos backups
        ttk.Label(config_frame, text="Pasta de Backups:").grid(row=1, column=0, sticky=tk.W, pady=5)
        backup_entry = ttk.Entry(config_frame, textvariable=self.backup_path_var, width=50)
        backup_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(config_frame, text="Procurar", command=self.browse_backup_path).grid(row=1, column=2, padx=5, pady=5)
        
        # Nome do mundo
        ttk.Label(config_frame, text="Nome do Mundo:").grid(row=2, column=0, sticky=tk.W, pady=5)
        world_entry = ttk.Entry(config_frame, textvariable=self.world_name_var)
        world_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Número máximo de backups
        ttk.Label(config_frame, text="Máximo de Backups:").grid(row=3, column=0, sticky=tk.W, pady=5)
        max_backups_spin = ttk.Spinbox(config_frame, from_=1, to=100, textvariable=self.max_backups_var, width=10)
        max_backups_spin.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Intervalo de backup
        ttk.Label(config_frame, text="Intervalo (horas):").grid(row=4, column=0, sticky=tk.W, pady=5)
        interval_spin = ttk.Spinbox(config_frame, from_=0.1, to=168, increment=0.5, textvariable=self.backup_interval_var, width=10)
        interval_spin.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Frame para botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Botões
        ttk.Button(button_frame, text="Salvar Configurações", command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Fazer Backup Agora", command=self.run_backup).pack(side=tk.LEFT, padx=5)
        
        self.schedule_button = ttk.Button(button_frame, text="Iniciar Agendamento", command=self.toggle_schedule)
        self.schedule_button.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Pronto")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Text widget para log
        self.log_text = tk.Text(log_frame, height=8, width=70, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar para o log
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Configurar handler para redirecionar logs para o widget de texto
        self.text_handler = TextHandler(self.log_text)
        logging.getLogger().addHandler(self.text_handler)
        
        # Adicionar log inicial
        logging.info("Aplicação iniciada. Configure os parâmetros e clique em 'Salvar Configurações'.")
    
    def browse_server_path(self):
        """Abre diálogo para selecionar pasta do servidor"""
        path = filedialog.askdirectory(title="Selecione a pasta do servidor Minecraft Bedrock")
        if path:
            self.server_path_var.set(path)
    
    def browse_backup_path(self):
        """Abre diálogo para selecionar pasta de backups"""
        path = filedialog.askdirectory(title="Selecione a pasta para salvar os backups")
        if path:
            self.backup_path_var.set(path)
    
    def run_backup(self):
        """Executa o backup manualmente"""
        if not self.validate_paths():
            return
        
        self.status_var.set("Fazendo backup...")
        self.root.update_idletasks()
        
        # Executar backup em uma thread separada para não congelar a interface
        threading.Thread(target=self._do_backup, daemon=True).start()
    
    def _do_backup(self):
        """Função que realiza o backup em uma thread separada"""
        try:
            success = self.create_backup()
            if success:
                self.cleanup_old_backups()
                self.status_var.set("Backup concluído com sucesso!")
            else:
                self.status_var.set("Erro ao fazer backup. Verifique o log.")
        except Exception as e:
            logging.error(f"Erro durante o backup: {str(e)}")
            self.status_var.set(f"Erro: {str(e)}")
    
    def toggle_schedule(self):
        """Inicia ou para o agendamento de backups"""
        if self.schedule_running:
            self.schedule_running = False
            self.schedule_button.configure(text="Iniciar Agendamento")
            self.status_var.set("Agendamento parado")
            logging.info("Agendamento de backups parado pelo usuário")
        else:
            if not self.validate_paths():
                return
            
            self.schedule_running = True
            self.schedule_button.configure(text="Parar Agendamento")
            self.status_var.set("Agendamento iniciado")
            
            # Iniciar thread de agendamento
            self.schedule_thread = threading.Thread(target=self.run_scheduled_backup, daemon=True)
            self.schedule_thread.start()
    
    def validate_paths(self):
        """Valida os caminhos configurados"""
        server_path = self.server_path_var.get()
        if not server_path or not os.path.exists(server_path):
            messagebox.showerror("Erro", "Caminho do servidor inválido ou não existe!")
            return False
        
        backup_path = self.backup_path_var.get()
        if not backup_path:
            messagebox.showerror("Erro", "Caminho de backup não definido!")
            return False
        
        # Criar pasta de backup se não existir
        os.makedirs(backup_path, exist_ok=True)
        
        return True
    
    def create_backup(self):
        """Cria um backup do mundo do servidor Minecraft Bedrock"""
        server_path = self.server_path_var.get()
        backup_path = self.backup_path_var.get()
        world_name = self.world_name_var.get()
        
        # Criar timestamp para nome do backup
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"minecraft_bedrock_backup_{timestamp}"
        backup_zip = os.path.join(backup_path, f"{backup_name}.zip")
        
        # Caminho para a pasta do mundo
        worlds_path = os.path.join(server_path, "worlds")
        world_path = os.path.join(worlds_path, world_name)
        
        if not os.path.exists(world_path):
            # Tentar encontrar a pasta do mundo se o nome não corresponder
            if os.path.exists(worlds_path):
                world_folders = [d for d in os.listdir(worlds_path) 
                                if os.path.isdir(os.path.join(worlds_path, d))]
                if world_folders:
                    world_path = os.path.join(worlds_path, world_folders[0])
                    logging.info(f"Usando pasta do mundo: {world_folders[0]}")
                else:
                    logging.error(f"Nenhuma pasta de mundo encontrada em {worlds_path}")
                    return False
            else:
                logging.error(f"Caminho do mundo não encontrado: {world_path}")
                return False
        
        logging.info(f"Criando backup do mundo: {world_path}")
        
        try:
            # Criar arquivo zip
            with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Percorrer todos os arquivos na pasta do mundo
                for root, _, files in os.walk(world_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Calcular caminho dentro do arquivo zip
                        arcname = os.path.relpath(file_path, os.path.dirname(world_path))
                        logging.debug(f"Adicionando {file_path} como {arcname}")
                        zipf.write(file_path, arcname)
            
            logging.info(f"Backup criado com sucesso: {backup_zip}")
            return True
        except Exception as e:
            logging.error(f"Erro ao criar backup: {str(e)}")
            return False
    
    def cleanup_old_backups(self):
        """Remove backups antigos para manter apenas o número especificado"""
        backup_path = self.backup_path_var.get()
        try:
            max_backups = int(self.max_backups_var.get())
        except ValueError:
            max_backups = 5
            logging.warning(f"Valor inválido para máximo de backups, usando padrão: {max_backups}")
        
        # Listar todos os arquivos de backup
        backup_files = [os.path.join(backup_path, f) for f in os.listdir(backup_path) 
                       if f.startswith("minecraft_bedrock_backup_") and f.endswith(".zip")]
        
        # Ordenar por data de modificação (mais recente primeiro)
        backup_files.sort(key=os.path.getmtime, reverse=True)
        
        # Remover backups excedentes
        if len(backup_files) > max_backups:
            for old_backup in backup_files[max_backups:]:
                try:
                    os.remove(old_backup)
                    logging.info(f"Backup antigo removido: {old_backup}")
                except Exception as e:
                    logging.error(f"Erro ao remover backup antigo {old_backup}: {str(e)}")
    
    def run_scheduled_backup(self):
        """Executa backups no intervalo especificado"""
        logging.info(f"Iniciando agendamento de backups")
        
        while self.schedule_running:
            try:
                interval_hours = float(self.backup_interval_var.get())
            except ValueError:
                interval_hours = 24
                logging.warning(f"Valor inválido para intervalo, usando padrão: {interval_hours} horas")
            
            interval_seconds = interval_hours * 3600
            
            # Fazer backup
            success = self.create_backup()
            if success:
                self.cleanup_old_backups()
            
            # Atualizar status
            next_backup = datetime.datetime.now() + datetime.timedelta(seconds=interval_seconds)
            next_backup_str = next_backup.strftime("%d/%m/%Y %H:%M:%S")
            self.status_var.set(f"Próximo backup em: {next_backup_str}")
            logging.info(f"Próximo backup agendado para: {next_backup_str}")
            
            # Esperar até o próximo backup
            for _ in range(int(interval_seconds)):
                if not self.schedule_running:
                    break
                time.sleep(1)


class TextHandler(logging.Handler):
    """Handler personalizado para redirecionar logs para o widget Text"""
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget
        
    def emit(self, record):
        msg = self.format(record)
        
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.see(tk.END)  # Rolar para o final
            self.text_widget.configure(state='disabled')
        
        # Executar na thread principal
        self.text_widget.after(0, append)


if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftBackupGUI(root)
    root.mainloop()