from app.crud import crud_clients, crud_users
from app.utils.auth import has_permission
from app.models.users import Department
from .filters_menu import menu_client_filters
from app.utils.validators import validate_phone, format_phone_number, validate_integer


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

        # Liste des clients
        if choice == "1":
            clients = crud_clients.get_all_clients(db)
            display_clients(clients)

        # Ajouter des clients.
        elif choice == "2":
            # Seuls les commerciaux (et éventuellement management) peuvent créer des clients
            if not has_permission(user, "manage_clients"):
                print("❌ Vous n'avez pas la permission d'ajouter des clients.")
                continue

            print("\n➕ Ajouter un client:")

            full_name = input("Nom complet: ")

            email = input("Email: ")

            phone = input("Téléphone: ")
            if not validate_phone(phone):
                print("❌ Téléphone invalide (format FR attendu)")
                continue
            phone = format_phone_number(phone)

            company = input("Entreprise: ")

            try:
                # Pour un commercial : le client est automatiquement associé à lui-même
                if user.department == Department.SALES:
                    commercial_id = user.id
                else:
                    # Management peut choisir un commercial
                    commercials = crud_users.get_sales_users(db)
                    print("Commerciaux disponibles:")
                    for c in commercials:
                        print(f"  {c.id}: {c.full_name}")
                    print()
                    commercial_id_str = input("ID commercial: ")
                    if not validate_integer(commercial_id_str):
                        print("❌ ID commercial invalide. Veuillez saisir un entier.")
                        continue
                    commercial_id = int(commercial_id_str)

                new_client = crud_clients.create_client(
                    db, full_name, email, phone, company, commercial_id
                )
                print(f"✅ Client créé: {new_client.full_name}")

            except Exception as e:
                db.rollback()
                print(f"❌ Erreur lors de la création du client. Vérifiez les valeurs saisies: {e}")

        # Voir un client
        elif choice == "3":
            client_id = input("\n👁️ ID du client: ")
            if not validate_integer(client_id):
                print("❌ ID invalide. Veuillez saisir un entier.")
                continue
            try:
                client = crud_clients.get_client_by_id(db, int(client_id))
                if client:
                    print("\n👤 Détails client:")
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
            except Exception:
                print("❌ Erreur lors de la lecture du client.")

        # modifier des clients.
        elif choice == "4":
            if not has_permission(user, "manage_clients"):
                print("❌ Vous n'avez pas la permission de modifier des clients.")
                continue

            client_id = input("\n✏️ ID du client à modifier: ")
            if not validate_integer(client_id):
                print("❌ ID invalide. Veuillez saisir un entier.")
                continue

            try:
                existing = crud_clients.get_client_by_id(db, int(client_id))
                if not existing:
                    print("❌ Client non trouvé")
                    continue

                # Un commercial ne peut modifier que ses propres clients
                if user.department == Department.SALES and existing.commercial_id != user.id:
                    print("❌ Vous ne pouvez modifier que vos propres clients.")
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
                    if not validate_phone(new_phone):
                        print("❌ Téléphone invalide (format FR attendu)")
                        continue
                    updates['phone'] = format_phone_number(new_phone)

                new_company = input(f"Entreprise [{existing.company_name}]: ")
                if new_company:
                    updates['company_name'] = new_company

                if updates:
                    crud_clients.update_client(db, existing.id, **updates)
                    print("✅ Client mis à jour")
                else:
                    print("⚠️  Aucune modification")

            except Exception as e:
                print(f"❌ Erreur lors de la mise à jour du client: {e}")
                db.rollback()

        # supprimer des clients
        elif choice == "5":
            if not has_permission(user, "manage_clients"):
                print("❌ Vous n'avez pas la permission de supprimer des clients.")
                continue

            client_id = input("\n🗑️ ID du client à supprimer: ")
            if not validate_integer(client_id):
                print("❌ ID invalide. Veuillez saisir un entier.")
                continue

            try:
                existing = crud_clients.get_client_by_id(db, int(client_id))
                if not existing:
                    print("❌ Client non trouvé")
                    continue

                # Un commercial ne peut supprimer que ses propres clients
                if user.department == Department.SALES or Department.SALES:
                    print("❌ Vous ne pouvez pas supprimer les clients.")
                    continue

                confirm = input(f"Confirmer la suppression de {existing.full_name}? (o/n): ")
                if confirm.lower() == 'o':
                    deleted = crud_clients.delete_client(db, existing.id)
                    if deleted:
                        print("✅ Client supprimé")
                    else:
                        print("❌ Impossible de supprimer ce client.")
                else:
                    print("❌ Annulé")

            except Exception as e:
                db.rollback()
                print(f"❌ Erreur lors de la suppression du client: {e}")

        # Filtres et recherche
        elif choice == "6":
            menu_client_filters(db, user)

        elif choice == "0":
            break

        else:
            print("❌ Option invalide")
