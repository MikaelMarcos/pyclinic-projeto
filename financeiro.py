import medicos as db_medicos
import consultas as db_consultas
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

def mostrar_balanco_financeiro():
    """Calcula e exibe o balanço financeiro da clínica."""
    console = Console()
    
    # Calcular Faturamento
    consultas = db_consultas.carregar_consultas()
    faturamento = 0.0
    for c in consultas:
        if c.get('status_pagamento') == 'pago':
            faturamento += c.get('valor', 0.0)
            
    # Calcular Despesas
    medicos = db_medicos.carregar_medicos()
    despesas = 0.0
    for m in medicos:
        despesas += m.get('salario', 0.0)
        
    # Calcular Lucro/Prejuízo
    balanco = faturamento - despesas
    
    # Exibir com Rich
    print("\n")
    balanco_texto = f"R$ {balanco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    cor_balanco = "green" if balanco >= 0 else "red"
    
    tabela = Table(show_header=False, box=None)
    tabela.add_row("[bold green]Faturamento Total (Consultas Pagas):[/]", f"R$ {faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    tabela.add_row("[bold red]Despesas Totais (Salários):[/]", f"R$ {despesas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    console.print(Panel(tabela, title="[bold cyan]Balanço Financeiro[/bold cyan]", border_style="cyan"))
    
    console.print(Panel(Text(f"Lucro / Prejuízo: {balanco_texto}", justify="center"), style=f"bold {cor_balanco}", border_style=cor_balanco))

    input("\nPressione Enter para continuar...")