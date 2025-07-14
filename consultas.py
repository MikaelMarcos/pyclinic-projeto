import json
import uuid
from datetime import datetime
# Importando as funções dos outros módulos para usar aqui
import pacientes as db_pacientes
import medicos as db_medicos

DB_FILE = 'dados_consultas.json'

def carregar_consultas():
    """Carrega a lista de consultas do arquivo JSON."""
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_consultas(consultas):
    """Salva a lista de consultas no arquivo JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(consultas, f, indent=2, ensure_ascii=False)

def agendar_consulta():
    """Agenda uma nova consulta."""
    consultas = carregar_consultas()
    
    print("\n--- Agendamento de Nova Consulta ---")
    
    # Listar pacientes para seleção
    print("\nPacientes disponíveis:")
    db_pacientes.listar_pacientes()
    paciente_id = input("Digite o ID do paciente: ")
    paciente = db_pacientes.buscar_paciente(paciente_id)
    if not paciente:
        print("❌ Erro: Paciente não encontrado.")
        input("Pressione Enter para continuar...")
        return

    # Listar médicos para seleção
    print("\nMédicos disponíveis:")
    db_medicos.listar_medicos()
    medico_id = input("Digite o ID do médico: ")
    medico = db_medicos.buscar_medico(medico_id)
    if not medico:
        print("❌ Erro: Médico não encontrado.")
        input("Pressione Enter para continuar...")
        return

    data_hora_str = input("Digite a data e hora da consulta (DD/MM/AAAA HH:MM): ")
    
    try:
        data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
    except ValueError:
        print("❌ Erro: Formato de data/hora inválido. Use DD/MM/AAAA HH:MM.")
        input("Pressione Enter para continuar...")
        return

    # Verificar conflito de horário para o mesmo médico
    for consulta in consultas:
        if consulta['medico_id'] == medico_id and consulta['data_hora'] == data_hora.isoformat() and consulta['status'] == 'agendada':
            print("❌ Erro: O médico já tem uma consulta agendada para este horário.")
            input("Pressione Enter para continuar...")
            return

    nova_consulta = {
        'id': str(uuid.uuid4())[:8],
        'paciente_id': paciente_id,
        'medico_id': medico_id,
        'data_hora': data_hora.isoformat(), # Salva no formato ISO para consistência
        'status': 'agendada'
    }
    
    consultas.append(nova_consulta)
    salvar_consultas(consultas)
    
    print(f"\n✅ Consulta agendada com sucesso! ID da Consulta: {nova_consulta['id']}")
    input("Pressione Enter para continuar...")

def listar_consultas():
    """Lista todas as consultas agendadas."""
    consultas = carregar_consultas()
    
    print("\n--- Lista de Todas as Consultas ---")
    if not consultas:
        print("Nenhuma consulta registrada.")
    else:
        for c in consultas:
            paciente = db_pacientes.buscar_paciente(c['paciente_id'])
            medico = db_medicos.buscar_medico(c['medico_id'])
            nome_paciente = paciente['nome'] if paciente else "Paciente não encontrado"
            nome_medico = medico['nome'] if medico else "Médico não encontrado"
            
            # Formata a data para exibição
            data_hora_obj = datetime.fromisoformat(c['data_hora'])
            data_hora_formatada = data_hora_obj.strftime("%d/%m/%Y às %H:%M")
            
            print(f"ID: {c['id']} | Status: {c['status'].upper()}")
            print(f"  Data: {data_hora_formatada}")
            print(f"  Paciente: {nome_paciente} (ID: {c['paciente_id']})")
            print(f"  Médico: {nome_medico} (ID: {c['medico_id']})")
            print("-" * 20)
            
    print("-" * 35)
    input("Pressione Enter para continuar...")

def cancelar_consulta():
    """Cancela uma consulta agendada."""
    consultas = carregar_consultas()
    
    print("\n--- Cancelamento de Consulta ---")
    
    # Mostra apenas as consultas agendadas para facilitar
    consultas_agendadas = [c for c in consultas if c['status'] == 'agendada']
    if not consultas_agendadas:
        print("Nenhuma consulta agendada para cancelar.")
        input("Pressione Enter para continuar...")
        return
        
    print("Consultas agendadas:")
    for c in consultas_agendadas:
        print(f"ID: {c['id']} | Data: {datetime.fromisoformat(c['data_hora']).strftime('%d/%m/%Y %H:%M')}")

    consulta_id = input("\nDigite o ID da consulta que deseja cancelar: ")
    
    consulta_encontrada = False
    for c in consultas:
        if c['id'] == consulta_id and c['status'] == 'agendada':
            c['status'] = 'cancelada'
            consulta_encontrada = True
            break
            
    if consulta_encontrada:
        salvar_consultas(consultas)
        print("\n✅ Consulta cancelada com sucesso!")
    else:
        print("\n❌ Erro: Consulta não encontrada ou já está cancelada.")
        
    input("Pressione Enter para continuar...")