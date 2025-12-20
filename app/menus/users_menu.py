from app.crud import crud_users
from app.models.users import Department


def menu_users(db, user):
    """Menu gestion des utilisateurs"""
    if user.department != Department.MANAGEMENT:
        print("❌ Accès refusé - Réservé au management")
        return

    while True:
        print("\n" + "=" * 50)
        print("        GESTION DES UTILISATEURS")
        print("=" * 50)
        print("1. 📋  Liste des utilisateurs")
        print("2. ➕  Ajouter un utilisateur")
        print("3. 👁️  Voir un utilisateur")
        print("4. ✏️  Modifier un utilisateur")
        print("5. 🗑️  Supprimer un utilisateur")
        print("6. 📊  Statistiques")
        print("0. ↩️  Retour")
        print("-" * 50)

        choice = input("Choisissez une option: ")

        if choice == "1":
            users = crud_users.get_all_users(db)
            print(f"\n📋 Utilisateurs ({len(users)}):")
            for u in users:
                print(f"  {u.id}: {u.full_name} - {u.email} - {u.department.value}")

        elif choice == "2":
            print("\n➕ Ajouter un utilisateur:")
            full_name = input("Nom complet: ")
            email = input("Email: ")
            employee_id = input("ID employé: ")
            password = input("Mot de passe: ")

            print("Départements disponibles: SALES, SUPPORT, MANAGEMENT")
            department = input("Département: ").upper()

            try:
                new_user = crud_users.create_user(
                    db, full_name, email, employee_id, password, department
                )
                print(f"✅ Utilisateur créé: {new_user.full_name}")
            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "3":
            user_id = input("\n👁️ ID de l'utilisateur: ")
            try:
                user = crud_users.get_user_by_id(db, int(user_id))
                if user:
                    print(f"\n👤 Détails:")
                    print(f"  ID: {user.id}")
                    print(f"  Nom: {user.full_name}")
                    print(f"  Email: {user.email}")
                    print(f"  ID employé: {user.employee_id}")
                    print(f"  Département: {user.department.value}")
                    print(f"  Créé le: {user.created_at}")
                else:
                    print("❌ Utilisateur non trouvé")
            except:
                print("❌ ID invalide")

        elif choice == "4":
            user_id = input("\n✏️ ID de l'utilisateur à modifier: ")
            try:
                existing = crud_users.get_user_by_id(db, int(user_id))
                if not existing:
                    print("❌ Utilisateur non trouvé")
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

                new_dept = input(f"Département [{existing.department.value}]: ")
                if new_dept:
                    updates['department'] = Department(new_dept.upper())

                new_password = input("Nouveau mot de passe (laisser vide): ")
                if new_password:
                    updates['password'] = new_password

                if updates:
                    updated = crud_users.update_user(db, existing.id, **updates)
                    print(f"✅ Utilisateur mis à jour")
                else:
                    print("⚠️  Aucune modification")

            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "5":
            user_id = input("\n🗑️ ID de l'utilisateur à supprimer: ")
            try:
                existing = crud_users.get_user_by_id(db, int(user_id))
                if not existing:
                    print("❌ Utilisateur non trouvé")
                    continue

                confirm = input(f"Confirmer la suppression de {existing.full_name}? (o/n): ")
                if confirm.lower() == 'o':
                    deleted = crud_users.delete_user(db, existing.id)
                    print(f"✅ Utilisateur supprimé")
                else:
                    print("❌ Annulé")
            except:
                print("❌ ID invalide")

        elif choice == "6":
            try:
                summary = crud_users.get_users_summary(db)
                print(f"\n📊 Statistiques:")
                print(f"  Total: {summary['total']}")
                print(f"  Sales: {summary['sales']}")
                print(f"  Support: {summary['support']}")
                print(f"  Management: {summary['management']}")
            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "0":
            break

        else:
            print("❌ Option invalide")