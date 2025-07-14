import json
import uuid

DB_FILE = 'dados_pacientes.json'

def carregar_pacientes():
    """Carrega a lista de pacientes do arquivo JSON."""
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existe ou está vazio/corrompido, retorna uma lista vazia.
        return []

def salvar_pacientes(pacientes):
    """Salva a lista de pacientes no arquivo JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(pacientes, f, indent=2, ensure_ascii=False)

def cadastrar_paciente():
    """Cadastra um novo paciente e o salva."""
    pacientes = carregar_pacientes()
    
    print("\n--- Cadastro de Novo Paciente ---")
    nome = input("Nome completo do paciente: ")
    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
    telefone = input("Telefone: ")
    
    # Gera um ID único para o paciente
    novo_paciente = {
        'id': str(uuid.uuid4())[:8], # Pega os 8 primeiros caracteres do UUID
        'nome': nome,
        'data_nascimento': data_nascimento,
        'telefone': telefone
    }
    
    pacientes.append(novo_paciente)
    salvar_pacientes(pacientes)
    
    print(f"\n✅ Paciente '{nome}' cadastrado com sucesso! ID: {novo_paciente['id']}")
    input("Pressione Enter para continuar...")

def listar_pacientes():
    """Lista todos os pacientes cadastrados."""
    pacientes = carregar_pacientes()
    
    print("\n--- Lista de Pacientes Cadastrados ---")
    if not pacientes:
        print("Nenhum paciente cadastrado.")
    else:
        for p in pacientes:
            print(f"ID: {p['id']} | Nome: {p['nome']} | Nascimento: {p['data_nascimento']} | Telefone: {p['telefone']}")
    
    print("-" * 35)
    input("Pressione Enter para continuar...")

def buscar_paciente(paciente_id):
    """Busca um paciente pelo seu ID."""
    pacientes = carregar_pacientes()
    for p in pacientes:
        if p['id'] == paciente_id:
            return p
    return None
