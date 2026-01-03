from app.crud import crud_contracts, crud_clients
from .filters_menu import menu_contract_filters
from app.utils.validators import validate_integer, validate_amount
from app.models.users import Department
from app.utils.auth import has_permission


def display_contracts(contracts):
    """Afficher la liste des contrats"""
    if not contracts:
        print("Aucun contrat trouvé")
        return

    print(f"\n📄 Contrats ({len(contracts)}):")
    for contract in contracts:
        status = "✓" if contract.is_signed else "✗"
        print(
            f"  {contract.id}: {contract.total_amount}€ - "
            f"Reste: {contract.remaining_amount}€ - "
            f"Signé: {status} - Client: {contract.client_id}"
        )


def menu_contracts(db, user):
    while True:
        print("\n" + "=" * 50)
        print("        GESTION DES CONTRATS")
        print("=" * 50)
        print("1. 📋  Liste des contrats")
        print("2. ➕  Ajouter un contrat")
        print("3. 👁️  Voir un contrat")
        print("4. ✏️  Modifier un contrat")
        print("5. ✍️  Signer un contrat")
        print("6. 💰  Ajouter un paiement")
        print("7. 🗑️  Supprimer un contrat")
        print("8. 🔍  Filtres et recherche")
        print("9. 📊  Statistiques")
        print("0. ↩️  Retour")
        print("-" * 50)

        choice = input("Choisissez une option: ")

        # 1. Liste
        if choice == "1":
            contracts = crud_contracts.get_all_contracts(db)
            display_contracts(contracts)

        # 2. Ajouter un contrat
        elif choice == "2":
            # Le support ne doit pas créer de contrats
            if (
                    user.department == Department.SUPPORT
                    or not (
                    has_permission(user, "create_contracts")
                    or has_permission(user, "manage_contracts")
                            )
                    ):
                print("❌ Vous n'avez pas la permission de créer des contrats.")
                continue

            print("\n➕ Ajouter un contrat:")

            # Afficher les clients
            clients = crud_clients.get_all_clients(db)
            print("Clients disponibles:")
            for c in clients:
                print(f"  {c.id}: {c.full_name} - {c.company_name}")
            print()

            try:
                total_str = input("Montant total: ")
                if not validate_amount(total_str):
                    print("❌ Montant total invalide. Veuillez saisir un nombre positif.")
                    continue
                total = float(total_str)

                remaining_str = input("Montant restant: ")
                if not validate_amount(remaining_str):
                    print("❌ Montant restant invalide. Veuillez saisir un nombre positif.")
                    continue
                remaining = float(remaining_str)

                client_id_str = input("ID client: ")
                if not validate_integer(client_id_str):
                    print("❌ ID client invalide. Veuillez saisir un nombre entier.")
                    continue
                client_id = int(client_id_str)

                # Vérifier que le client existe
                client = crud_clients.get_client_by_id(db, client_id)
                if not client:
                    print("❌ Client introuvable. Veuillez choisir un ID dans la liste.")
                    continue

                commercial_id = user.id

                signed_input = input("Contrat signé? (o/n): ")
                is_signed = signed_input.lower() == 'o'

                new_contract = crud_contracts.create_contract(
                    db, total, remaining, is_signed, client_id, commercial_id
                    )
                print(f"✅ Contrat créé: {new_contract.id}")
            except Exception:
                db.rollback()
                print("❌ Erreur lors de la création du contrat. Vérifiez les valeurs saisies.")

        # 3. Voir un contrat (lecture autorisée pour tous)
        elif choice == "3":
            contract_id = input("\n👁️ ID du contrat: ")
            if not validate_integer(contract_id):
                print("❌ ID invalide. Veuillez saisir un nombre entier.")
                continue
            try:
                contract = crud_contracts.get_contract_by_id(db, int(contract_id))
                if contract:
                    print("\n📄 Détails contrat:")
                    print(f"  ID: {contract.id}")
                    print(f"  Montant total: {contract.total_amount}€")
                    print(f"  Montant restant: {contract.remaining_amount}€")
                    print(f"  Signé: {'Oui' if contract.is_signed else 'Non'}")
                    print(f"  Client ID: {contract.client_id}")
                    print(f"  Commercial ID: {contract.commercial_id}")
                    print(f"  Créé le: {contract.creation_date}")
                else:
                    print("❌ Contrat non trouvé")
            except Exception as e:
                print("❌ Erreur lors de la lecture du contrat.", e)

        # 4. Modifier un contrat
        elif choice == "4":
            # Vérif permission globale
            if not has_permission(user, "manage_contracts") and not has_permission(user, "update_own_contracts"):
                print("❌ Vous n'avez pas la permission de modifier des contrats.")
                continue

            contract_id = input("\n✏️ ID du contrat à modifier: ")
            if not validate_integer(contract_id):
                print("❌ ID invalide. Veuillez saisir un nombre entier.")
                continue

            try:
                contract_id_int = int(contract_id)
                existing = crud_contracts.get_contract_by_id(db, contract_id_int)
                if not existing:
                    print("❌ Contrat non trouvé")
                    continue

                # SALES : ne peut modifier que ses propres contrats
                if user.department == Department.SALES:
                    if not has_permission(user, "update_own_contracts"):
                        print("❌ Vous n'avez pas la permission de modifier des contrats.")
                        continue
                    if existing.commercial_id != user.id:
                        print("❌ Vous ne pouvez modifier que vos propres contrats.")
                        continue

                # SUPPORT : n'a aucune des permissions → bloqué au début
                # MANAGEMENT : a manage_contracts → peut tout modifier

                print(f"Modification du contrat {existing.id}")
                print("Laissez vide pour ne pas modifier")

                updates = {}

                new_total = input(f"Montant total [{existing.total_amount}]: ")
                if new_total:
                    if not validate_amount(new_total):
                        print("❌ Montant total invalide.")
                        continue
                    updates["total_amount"] = float(new_total)

                new_remaining = input(f"Montant restant [{existing.remaining_amount}]: ")
                if new_remaining:
                    if not validate_amount(new_remaining):
                        print("❌ Montant restant invalide.")
                        continue
                    updates["remaining_amount"] = float(new_remaining)

                signed_input = input(f"Signé? (o/n) [{'o' if existing.is_signed else 'n'}]: ")
                if signed_input:
                    updates["is_signed"] = signed_input.lower() == "o"

                if updates:
                    crud_contracts.update_contract(db, existing.id, **updates)
                    print("✅ Contrat mis à jour")
                else:
                    print("⚠️  Aucune modification")

            except Exception as e:
                db.rollback()
                print(f"❌ Erreur lors de la mise à jour du contrat: {e}")

        # 5. Signer un contrat
        elif choice == "5":
            # Personne sans permission ne peut signer
            if not has_permission(user, "sign_own_contracts"):
                print("❌ Vous n'avez pas la permission de signer des contrats.")
                continue

            contract_id = input("\n✍️ ID du contrat à signer: ")
            if not validate_integer(contract_id):
                print("❌ ID invalide. Veuillez saisir un nombre entier.")
                continue

            try:
                contract_id_int = int(contract_id)
                existing = crud_contracts.get_contract_by_id(db, contract_id_int)
                if not existing:
                    print("❌ Contrat non trouvé")
                    continue

                # SALES : ne peut signer que ses propres contrats
                if user.department == Department.SALES:
                    if existing.commercial_id != user.id:
                        print("❌ Vous ne pouvez signer que vos propres contrats.")
                        continue

                # SUPPORT n'a aucune des permissions → bloqué au début
                # MANAGEMENT (manage_contracts) → peut signer tous les contrats

                updated = crud_contracts.sign_contract(db, contract_id_int)
                if updated:
                    print("✅ Contrat signé")
                else:
                    print("❌ Contrat non trouvé")

            except Exception:
                db.rollback()
                print("❌ Erreur lors de la signature du contrat.")

        # 6. Ajouter un paiement
        elif choice == "6":
            # Le support ne doit pas ajouter de paiements
            if (
                    user.department == Department.SUPPORT
                    or not (
                    has_permission(user, "manage_contracts")
                    or has_permission(user, "update_own_contracts")
                            )
                    ):
                print("❌ Vous n'avez pas la permission d'ajouter des paiements.")
                continue

            contract_id = input("\n💰 ID du contrat: ")
            if not validate_integer(contract_id):
                print("❌ ID invalide. Veuillez saisir un nombre entier.")
                continue
            try:
                contract = crud_contracts.get_contract_by_id(db, int(contract_id))
                if not contract:
                    print("❌ Contrat non trouvé")
                    continue

                print(f"Montant restant: {contract.remaining_amount}€")
                amount_str = input("Montant du paiement: ")
                if not validate_amount(amount_str):
                    print("❌ Montant de paiement invalide.")
                    continue
                amount = float(amount_str)

                updated = crud_contracts.add_payment(db, contract.id, amount)
                if updated:
                    print(f"✅ Paiement ajouté. Nouveau reste: {updated.remaining_amount}€")
            except Exception:
                db.rollback()
                print("❌ Erreur lors de l'ajout du paiement.")

        # 7. Supprimer un contrat
        elif choice == "7":
            # Personne sans permission ne peut supprimer
            if not has_permission(user, "manage_contracts") and not has_permission(user, "manage_own_contracts"):
                print("❌ Vous n'avez pas la permission de supprimer des contrats.")
                continue

            contract_id = input("\n🗑️ ID du contrat à supprimer: ")
            if not validate_integer(contract_id):
                print("❌ ID invalide. Veuillez saisir un nombre entier.")
                continue

            try:
                contract_id_int = int(contract_id)
                existing = crud_contracts.get_contract_by_id(db, contract_id_int)
                if not existing:
                    print("❌ Contrat non trouvé")
                    continue

                # SALES : ne peut supprimer que ses propres contrats
                if user.department == Department.SALES:
                    if not has_permission(user, "manage_own_contracts"):
                        print("❌ Vous n'avez pas la permission de supprimer des contrats.")
                        continue
                    if existing.commercial_id != user.id:
                        print("❌ Vous ne pouvez supprimer que vos propres contrats.")
                        continue

                # SUPPORT n'a aucune des permissions → bloqué au début
                # MANAGEMENT à manage_contracts → peut tout supprimer

                confirm = input(f"Confirmer la suppression du contrat {existing.id}? (o/n): ")
                if confirm.lower() == "o":
                    deleted = crud_contracts.delete_contract(db, existing.id)
                    if deleted:
                        print("✅ Contrat supprimé")
                    else:
                        print("❌ Impossible de supprimer ce contrat.")
                else:
                    print("❌ Annulé")

            except Exception:
                db.rollback()
                print("❌ Erreur lors de la suppression du contrat.")

        # 8. Filtres et recherche (lecture, donc OK pour tous)
        elif choice == "8":
            menu_contract_filters(db, user)

        # 9. Statistiques (lecture, donc OK pour tous)
        elif choice == "9":
            try:
                summary = crud_contracts.get_contract_summary(db)
                print("\n📊 Statistiques des contrats:")
                print(f"  Total: {summary['total']}")
                print(f"  Signés: {summary['signed']}")
                print(f"  Non signés: {summary['unsigned']}")
                print(f"  Montant total: {summary['total_amount']}€")
                print(f"  Montant restant: {summary['remaining_amount']}€")
                print(f"  Montant payé: {summary['paid_amount']}€")

                if summary['total_amount'] > 0:
                    percent = (summary['paid_amount'] / summary['total_amount']) * 100
                    print(f"  Pourcentage payé: {percent:.1f}%")
            except Exception as e:
                db.rollback()
                print("❌ Erreur lors du calcul des statistiques.", e)

        elif choice == "0":
            break

        else:
            print("❌ Option invalide")
