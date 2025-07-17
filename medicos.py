import json
import uuid

DB_FILE = 'dados_medicos.json'

def carregar_medicos():
    """Carrega a lista de médicos do arquivo JSON."""
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_medicos(medicos):
    """Salva a lista de médicos no arquivo JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(medicos, f, indent=2, ensure_ascii=False)

def cadastrar_medico():
    """Cadastra um novo médico e o salva."""
    medicos = carregar_medicos()
    
    print("\n--- Cadastro de Novo Médico ---")
    nome = input("Nome completo do médico: ")
    especialidade = input("Especialidade: ")
    
    novo_medico = {
        'id': str(uuid.uuid4())[:8],
        'nome': nome,
        'especialidade': especialidade,
        'salario': 10000.00  # salário de 10k
    }
    
    medicos.append(novo_medico)
    salvar_medicos(medicos)
    
    print(f"\n✅ Médico(a) '{nome}' cadastrado com sucesso! ID: {novo_medico['id']}")
    input("Pressione Enter para continuar...")

def listar_medicos():
    """Lista todos os médicos cadastrados."""
    medicos = carregar_medicos()
    
    print("\n--- Lista de Médicos Cadastrados ---")
    if not medicos:
        print("Nenhum médico cadastrado.")
    else:
        for m in medicos:
            print(f"ID: {m['id']} | Nome: {m['nome']} | Especialidade: {m['especialidade']} | Salário: R$ {m['salario']:.2f}")
            
    print("-" * 35)
    input("Pressione Enter para continuar...")

def buscar_medico(medico_id):
    """Busca um médico pelo seu ID."""
    medicos = carregar_medicos()
    for m in medicos:
        if m['id'] == medico_id:
            return m
    return None