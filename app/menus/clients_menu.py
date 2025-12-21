from app.crud import crud_clients, crud_users
from datetime import datetime


def display_clients(clients):
    """Afficher la liste des clients"""
    if not clients:
        print("Aucun client trouvé")
        return

    print(f"\n📋 Clients ({len(clients)}):")
    for client in clients:
        print(f"  {client.id}: {client.full_name} - {client.company_name} - {client.email}")


def menu_clients(db, user):
    """Menu gestion des clients"""
    while True:
        print("\n" + "=" * 50)
        print("        GESTION DES CLIENTS")
        print("=" * 50)
        print("1. 📋  Liste des clients")
        print("2. ➕  Ajouter un client")
        print("3. 👁️  Voir un client")
        print("4. ✏️  Modifier un client")
        print("5. 🗑️  Supprimer un client")
        print("6. 🔍  Filtres et recherche")
        print("0. ↩️  Retour")
        print("-" * 50)

        choice = input("Choisissez une option: ")

        if choice == "1":
            clients = crud_clients.get_all_clients(db)
            display_clients(clients)

        elif choice == "2":
            print("\n➕ Ajouter un client:")

            # Afficher les commerciaux disponibles
            commercials = crud_users.get_users_by_department(db, user.department)
            print("Commerciaux disponibles:")
            for c in commercials:
                print(f"  {c.id}: {c.full_name}")
            print()

            full_name = input("Nom complet: ")
            email = input("Email: ")
            phone = input("Téléphone: ")
            company = input("Entreprise: ")

            try:
                commercial_id = int(input("ID commercial: "))
                new_client = crud_clients.create_client(
                    db, full_name, email, phone, company, commercial_id
                )
                print(f"✅ Client créé: {new_client.full_name}")
            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "3":
            client_id = input("\n👁️ ID du client: ")
            try:
                client = crud_clients.get_client_by_id(db, int(client_id))
                if client:
                    print(f"\n👤 Détails client:")
                    print(f"  ID: {client.id}")
                    print(f"  Nom: {client.full_name}")
                    print(f"  Email: {client.email}")
                    print(f"  Téléphone: {client.phone}")
                    print(f"  Entreprise: {client.company_name}")
                    print(f"  Commercial ID: {client.commercial_id}")
                    print(f"  Créé le: {client.created_date}")
                    print(f"  Dernier contact: {client.last_contact}")
                else:
                    print("❌ Client non trouvé")
            except:
                print("❌ ID invalide")

        elif choice == "4":
            client_id = input("\n✏️ ID du client à modifier: ")
            try:
                existing = crud_clients.get_client_by_id(db, int(client_id))
                if not existing:
                    print("❌ Client non trouvé")
                    continue

                print(f"Modification de {existing.full_name}")
                print("Laissez vide pour ne pas modifier")

                updates = {}
                new_name = input(f"Nom [{existing.full_name}]: ")
                if new_name:
                    updates['full_name'] = new_name

                new_email = input(f"Email [{existing.email}]: ")
                if new_email:
                    updates['email'] = new_email

                new_phone = input(f"Téléphone [{existing.phone}]: ")
                if new_phone:
                    updates['phone'] = new_phone

                new_company = input(f"Entreprise [{existing.company_name}]: ")
                if new_company:
                    updates['company_name'] = new_company

                if updates:
                    updated = crud_clients.update_client(db, existing.id, **updates)
                    print(f"✅ Client mis à jour")
                else:
                    print("⚠️  Aucune modification")

            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "5":
            client_id = input("\n🗑️ ID du client à supprimer: ")
            try:
                existing = crud_clients.get_client_by_id(db, int(client_id))
                if not existing:
                    print("❌ Client non trouvé")
                    continue

                confirm = input(f"Confirmer la suppression de {existing.full_name}? (o/n): ")
                if confirm.lower() == 'o':
                    deleted = crud_clients.delete_client(db, existing.id)
                    print(f"✅ Client supprimé")
                else:
                    print("❌ Annulé")
            except:
                print("❌ ID invalide")

        elif choice == "6":
            from .filters_menu import menu_client_filters
            menu_client_filters(db, user)

        elif choice == "0":
            break

        else:
            print("❌ Option invalide")