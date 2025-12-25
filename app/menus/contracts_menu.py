from app.crud import crud_contracts, crud_clients
from .filters_menu import menu_contract_filters


def display_contracts(contracts):
    """Afficher la liste des contrats"""
    if not contracts:
        print("Aucun contrat trouvé")
        return

    print(f"\n📄 Contrats ({len(contracts)}):")
    for contract in contracts:
        status = "✓" if contract.is_signed else "✗"
        print(f"  {contract.id}: {contract.total_amount}€ - "
              f"Reste: {contract.remaining_amount}€ - "
              f"Signé: {status} - Client: {contract.client_id}")

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
        print("8. 🔍  Filtres et recherche")  # <-- NOUVELLE OPTION
        print("9. 📊  Statistiques")
        print("0. ↩️  Retour")
        print("-" * 50)

        choice = input("Choisissez une option: ")

        if choice == "1":
            contracts = crud_contracts.get_all_contracts(db)
            display_contracts(contracts)

        elif choice == "2":
            print("\n➕ Ajouter un contrat:")

            # Afficher les clients
            clients = crud_clients.get_all_clients(db)
            print("Clients disponibles:")
            for c in clients:
                print(f"  {c.id}: {c.full_name} - {c.company_name}")
            print()

            try:
                total = float(input("Montant total: "))
                remaining = float(input("Montant restant: "))
                client_id = int(input("ID client: "))
                commercial_id = user.id

                signed_input = input("Contrat signé? (o/n): ")
                is_signed = signed_input.lower() == 'o'

                new_contract = crud_contracts.create_contract(
                    db, total, remaining, is_signed, client_id, commercial_id
                )
                print(f"✅ Contrat créé: {new_contract.id}")
            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "3":
            contract_id = input("\n👁️ ID du contrat: ")
            try:
                contract = crud_contracts.get_contract_by_id(db, int(contract_id))
                if contract:
                    print(f"\n📄 Détails contrat:")
                    print(f"  ID: {contract.id}")
                    print(f"  Montant total: {contract.total_amount}€")
                    print(f"  Montant restant: {contract.remaining_amount}€")
                    print(f"  Signé: {'Oui' if contract.is_signed else 'Non'}")
                    print(f"  Client ID: {contract.client_id}")
                    print(f"  Commercial ID: {contract.commercial_id}")
                    print(f"  Créé le: {contract.creation_date}")
                else:
                    print("❌ Contrat non trouvé")
            except:
                print("❌ ID invalide")

        elif choice == "4":
            contract_id = input("\n✏️ ID du contrat à modifier: ")
            try:
                existing = crud_contracts.get_contract_by_id(db, int(contract_id))
                if not existing:
                    print("❌ Contrat non trouvé")
                    continue

                print(f"Modification du contrat {existing.id}")
                print("Laissez vide pour ne pas modifier")

                updates = {}
                new_total = input(f"Montant total [{existing.total_amount}]: ")
                if new_total:
                    updates['total_amount'] = float(new_total)

                new_remaining = input(f"Montant restant [{existing.remaining_amount}]: ")
                if new_remaining:
                    updates['remaining_amount'] = float(new_remaining)

                signed_input = input(f"Signé? (o/n) [{'o' if existing.is_signed else 'n'}]: ")
                if signed_input:
                    updates['is_signed'] = signed_input.lower() == 'o'

                if updates:
                    updated = crud_contracts.update_contract(db, existing.id, **updates)
                    print(f"✅ Contrat mis à jour")
                else:
                    print("⚠️  Aucune modification")

            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "5":
            contract_id = input("\n✍️ ID du contrat à signer: ")
            try:
                updated = crud_contracts.sign_contract(db, int(contract_id))
                if updated:
                    print(f"✅ Contrat signé")
                else:
                    print("❌ Contrat non trouvé")
            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "6":
            contract_id = input("\n💰 ID du contrat: ")
            try:
                contract = crud_contracts.get_contract_by_id(db, int(contract_id))
                if not contract:
                    print("❌ Contrat non trouvé")
                    continue

                print(f"Montant restant: {contract.remaining_amount}€")
                amount = float(input("Montant du paiement: "))

                updated = crud_contracts.add_payment(db, contract.id, amount)
                if updated:
                    print(f"✅ Paiement ajouté. Nouveau reste: {updated.remaining_amount}€")
            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "7":
            contract_id = input("\n🗑️ ID du contrat à supprimer: ")
            try:
                existing = crud_contracts.get_contract_by_id(db, int(contract_id))
                if not existing:
                    print("❌ Contrat non trouvé")
                    continue

                confirm = input(f"Confirmer la suppression du contrat {existing.id}? (o/n): ")
                if confirm.lower() == 'o':
                    deleted = crud_contracts.delete_contract(db, existing.id)
                    print(f"✅ Contrat supprimé")
                else:
                    print("❌ Annulé")
            except:
                print("❌ ID invalide")

        elif choice == "8":  # Nouvelle option

            menu_contract_filters(db, user)

        elif choice == "9":
            try:
                summary = crud_contracts.get_contract_summary(db)
                print(f"\n📊 Statistiques des contrats:")
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
                print(f"❌ Erreur: {e}")

        elif choice == "0":
            break

        else:
            print("❌ Option invalide")