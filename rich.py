from _pyrepl import console

from sqlalchemy import Table


def afficher_clients_rich(clients):
    table = Table(title="Liste des clients")

    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Nom complet", style="bold")
    table.add_column("Email", style="magenta")
    table.add_column("Téléphone", style="green")
    table.add_column("Entreprise", style="yellow")

    for c in clients:
        table.add_row(
            str(c.id),
            c.full_name,
            c.email,
            c.phone or "",
            c.company_name or "",
        )

    console.print(table)
