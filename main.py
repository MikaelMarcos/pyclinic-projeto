# FILE: main.py (Versão Corrigida)

# Módulos do projeto
import pacientes
import medicos
import consultas

# Bibliotecas nativas e externas
import os
import time
from datetime import datetime

# A grande estrela da nova interface!
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align # <--- 1. IMPORTAÇÃO ADICIONADA AQUI

# Inicializa o console do Rich
console = Console()

def limpar_tela():
    """Limpa o terminal para uma melhor experiência de usuário."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_cabecalho(texto, cor_borda="cyan"):
    """Mostra um cabeçalho estilizado usando um painel do Rich."""
    # 2. CORREÇÃO APLICADA AQUI
    # O texto agora é envolvido em um objeto Align para ser centralizado
    texto_centralizado = Align.center(texto, style="bold")
    console.print(Panel(texto_centralizado, border_style=cor_borda))


def mostrar_dashboard():
    """Exibe um dashboard com estatísticas gerais da clínica."""
    
    # Carrega os dados usando as funções dos outros módulos
    lista_pacientes = pacientes.carregar_pacientes()
    lista_medicos = medicos.carregar_medicos()
    lista_consultas = consultas.carregar_consultas()
    
    # Calcula as estatísticas
    total_pacientes = len(lista_pacientes)
    total_medicos = len(lista_medicos)
    
    # Calcula as consultas agendadas para hoje
    hoje = datetime.now().date()
    consultas_hoje = 0
    for consulta in lista_consultas:
        if consulta['status'] == 'agendada':
            data_consulta = datetime.fromisoformat(consulta['data_hora']).date()
            if data_consulta == hoje:
                consultas_hoje += 1

    # Cria uma tabela para o dashboard
    tabela_dashboard = Table(show_header=False, box=None, padding=(0, 2))
    tabela_dashboard.add_column(style="magenta", justify="center")
    tabela_dashboard.add_column(style="bold green", justify="left")

    tabela_dashboard.add_row("👥", f"{total_pacientes} Pacientes Cadastrados")
    tabela_dashboard.add_row("⚕️", f"{total_medicos} Médicos Disponíveis")
    tabela_dashboard.add_row("📅", f"{consultas_hoje} Consultas Agendadas para Hoje")

    console.print(Panel(tabela_dashboard, title="[bold]Resumo da Clínica[/bold]", border_style="green", expand=False))

def menu_principal():
    """Exibe o menu principal e gerencia a navegação."""
    while True:
        limpar_tela()
        mostrar_cabecalho("🏥 PyClinic - Sistema de Gestão Médica 🏥")
        mostrar_dashboard()

        console.print("\n[bold cyan]Menu Principal[/bold cyan]")
        console.print("1. Gerenciar Pacientes")
        console.print("2. Gerenciar Médicos")
        console.print("3. Gerenciar Consultas")
        console.print("[bold red]0. Sair do Sistema[/bold red]")
        
        escolha = Prompt.ask("\nEscolha uma opção", choices=['1', '2', '3', '0'], default='0')
        
        if escolha == '1':
            menu_pacientes()
        elif escolha == '2':
            menu_medicos()
        elif escolha == '3':
            menu_consultas()
        elif escolha == '0':
            with console.status("[bold green]Saindo do sistema...[/bold green]", spinner="dots") as status:
                time.sleep(1.5)
            console.print("Até logo! 👋")
            break

def menu_pacientes():
    """Exibe o submenu para gerenciamento de pacientes."""
    while True:
        limpar_tela()
        mostrar_cabecalho("👥 Gerenciamento de Pacientes 👥", cor_borda="blue")
        
        console.print("\n1. Cadastrar Novo Paciente")
        console.print("2. Listar Todos os Pacientes")
        console.print("[bold red]9. Voltar ao Menu Principal[/bold red]")

        escolha = Prompt.ask("\nEscolha uma opção", choices=['1', '2', '9'], default='9')

        if escolha == '1':
            pacientes.cadastrar_paciente()
        elif escolha == '2':
            pacientes.listar_pacientes()
        elif escolha == '9':
            break

def menu_medicos():
    """Exibe o submenu para gerenciamento de médicos."""
    while True:
        limpar_tela()
        mostrar_cabecalho("⚕️ Gerenciamento de Médicos ⚕️", cor_borda="green")

        console.print("\n1. Cadastrar Novo Médico")
        console.print("2. Listar Todos os Médicos")
        console.print("[bold red]9. Voltar ao Menu Principal[/bold red]")

        escolha = Prompt.ask("\nEscolha uma opção", choices=['1', '2', '9'], default='9')

        if escolha == '1':
            medicos.cadastrar_medico()
        elif escolha == '2':
            medicos.listar_medicos()
        elif escolha == '9':
            break

def menu_consultas():
    """Exibe o submenu para gerenciamento de consultas."""
    while True:
        limpar_tela()
        mostrar_cabecalho("📅 Gerenciamento de Consultas 📅", cor_borda="magenta")
        
        console.print("\n1. Agendar Nova Consulta")
        console.print("2. Listar Todas as Consultas")
        console.print("3. Cancelar Consulta")
        console.print("[bold red]9. Voltar ao Menu Principal[/bold red]")
        
        escolha = Prompt.ask("\nEscolha uma opção", choices=['1', '2', '3', '9'], default='9')

        if escolha == '1':
            consultas.agendar_consulta()
        elif escolha == '2':
            consultas.listar_consultas()
        elif escolha == '3':
            consultas.cancelar_consulta()
        elif escolha == '9':
            break

# Ponto de entrada do programa
if __name__ == "__main__":
    menu_principal()
