import json
import uuid
from datetime import datetime
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
    
    print("\nPacientes disponíveis:")
    db_pacientes.listar_pacientes()
    paciente_id = input("Digite o ID do paciente: ")
    paciente = db_pacientes.buscar_paciente(paciente_id)
    if not paciente:
        print("❌ Erro: Paciente não encontrado.")
        input("Pressione Enter para continuar...")
        return

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

    for consulta in consultas:
        if consulta['medico_id'] == medico_id and consulta['data_hora'] == data_hora.isoformat() and consulta['status'] == 'agendada':
            print("❌ Erro: O médico já tem uma consulta agendada para este horário.")
            input("Pressione Enter para continuar...")
            return

    nova_consulta = {
        'id': str(uuid.uuid4())[:8],
        'paciente_id': paciente_id,
        'medico_id': medico_id,
        'data_hora': data_hora.isoformat(),
        'status': 'agendada',
        'valor': 150.00,  # 
        'status_pagamento': 'pendente' # 
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
            nome_paciente = paciente['nome'] if paciente else "N/A"
            nome_medico = medico['nome'] if medico else "N/A"
            data_hora_obj = datetime.fromisoformat(c['data_hora'])
            data_hora_formatada = data_hora_obj.strftime("%d/%m/%Y às %H:%M")
            
            pagamento_status = c.get('status_pagamento', 'N/A').upper()
            valor_consulta = c.get('valor', 0.0)
            
            print(f"ID: {c['id']} | Status: {c['status'].upper()} | Pagamento: {pagamento_status}")
            print(f"  Data: {data_hora_formatada} | Valor: R$ {valor_consulta:.2f}")
            print(f"  Paciente: {nome_paciente}")
            print(f"  Médico: {nome_medico}")
            print("-" * 20)
            
    print("-" * 35)
    input("Pressione Enter para continuar...")

def cancelar_consulta():
    """Cancela uma consulta agendada."""
    consultas = carregar_consultas()
    print("\n--- Cancelamento de Consulta ---")
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

def registrar_pagamento_consulta():
    """Registra o pagamento de uma consulta."""
    consultas = carregar_consultas()
    
    print("\n--- Registrar Pagamento de Consulta ---")
    
    consultas_pendentes = [c for c in consultas if c.get('status_pagamento') == 'pendente' and c['status'] == 'agendada']
    
    if not consultas_pendentes:
        print("Nenhuma consulta com pagamento pendente encontrada.")
        input("Pressione Enter para continuar...")
        return
        
    print("Consultas com pagamento pendente:")
    for c in consultas_pendentes:
        print(f"ID: {c['id']} | Data: {datetime.fromisoformat(c['data_hora']).strftime('%d/%m/%Y %H:%M')} | Valor: R$ {c['valor']:.2f}")

    consulta_id = input("\nDigite o ID da consulta para registrar o pagamento: ")
    
    consulta_encontrada = False
    for c in consultas:
        if c['id'] == consulta_id:
            c['status_pagamento'] = 'pago'
            consulta_encontrada = True
            break
            
    if consulta_encontrada:
        salvar_consultas(consultas)
        print("\n✅ Pagamento registrado com sucesso!")
    else:
        print("\n❌ Erro: Consulta não encontrada.")
        
    input("Pressione Enter para continuar...")
