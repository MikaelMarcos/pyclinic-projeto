# Importando os módulos com apelidos para clareza
import pacientes
import medicos
import consultas
import os

def limpar_tela():
    """Limpa o terminal para uma melhor experiência de usuário."""
    # 'nt' é para Windows, 'posix' é para Mac/Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    """Exibe o menu principal e gerencia a navegação."""
    while True:
        limpar_tela()
        print("--- Bem-vindo ao Sistema PyClinic ---")
        print("1. Gerenciar Pacientes")
        print("2. Gerenciar Médicos")
        print("3. Gerenciar Consultas")
        print("0. Sair do Sistema")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            menu_pacientes()
        elif escolha == '2':
            menu_medicos()
        elif escolha == '3':
            menu_consultas()
        elif escolha == '0':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar...")

def menu_pacientes():
    """Exibe o submenu para gerenciamento de pacientes."""
    while True:
        limpar_tela()
        print("--- Gerenciamento de Pacientes ---")
        print("1. Cadastrar Novo Paciente")
        print("2. Listar Todos os Pacientes")
        print("9. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            pacientes.cadastrar_paciente()
        elif escolha == '2':
            pacientes.listar_pacientes()
        elif escolha == '9':
            break
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")

def menu_medicos():
    """Exibe o submenu para gerenciamento de médicos."""
    while True:
        limpar_tela()
        print("--- Gerenciamento de Médicos ---")
        print("1. Cadastrar Novo Médico")
        print("2. Listar Todos os Médicos")
        print("9. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            medicos.cadastrar_medico()
        elif escolha == '2':
            medicos.listar_medicos()
        elif escolha == '9':
            break
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")

def menu_consultas():
    """Exibe o submenu para gerenciamento de consultas."""
    while True:
        limpar_tela()
        print("--- Gerenciamento de Consultas ---")
        print("1. Agendar Nova Consulta")
        print("2. Listar Todas as Consultas")
        print("3. Cancelar Consulta")
        print("9. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            consultas.agendar_consulta()
        elif escolha == '2':
            consultas.listar_consultas()
        elif escolha == '3':
            consultas.cancelar_consulta()
        elif escolha == '9':
            break
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")

# Ponto de entrada do programa
if __name__ == "__main__":
    menu_principal()

