from app.menus.users_menu import menu_users
from app.menus.clients_menu import menu_clients
from app.menus.contracts_menu import menu_contracts
from app.menus.events_menu import menu_events
from app.models.users import Department
from app.utils.auth import get_user_permissions
from app.utils.session import clear_session  # importe la fonction qui supprime ~/.crm_token


def main_menu(db, user):
    """Menu principal"""
    try:
        while True:
            print("\n" + "=" * 50)
            print(f"    MENU PRINCIPAL - {user.full_name}")
            print("=" * 50)
            print("1. 👥  Gestion des clients")
            print("2. 📄  Gestion des contrats")
            print("3. 📅  Gestion des événements")

            if user.department == Department.MANAGEMENT:
                print("4. 👤  Gestion des utilisateurs")
            print("9. 🔧  Mon compte")
            print("11. 🏇 Quitter (rester connecté)")
            print("0. 🚪 Déconnexion complète")
            print("-" * 50)

            choice = input("Choisissez une option: ")

            if choice == "1":
                menu_clients(db, user)
            elif choice == "2":
                menu_contracts(db, user)
            elif choice == "3":
                menu_events(db, user)
            elif choice == "4" and user.department == Department.MANAGEMENT:
                menu_users(db, user)
            elif choice == "9":
                show_user_profile(user)
            elif choice == "11":
                print("\n👋 Au revoir !")
                break
            elif choice == "0":
                print("\n🔒 Déconnexion...")
                clear_session()
                break
            else:
                print("\n❌ Option invalide")
    finally:
        db.close()


def show_user_profile(user):
    """Afficher le profil de l'utilisateur"""
    print("\n" + "=" * 50)
    print(f"        MON PROFIL - {user.full_name}")
    print("=" * 50)
    print(f"👤 Nom complet: {user.full_name}")
    print(f"📧 Email: {user.email}")
    print(f"🆔 ID employé: {user.employee_id}")
    print(f"🏢 Département: {user.department.value}")
    print(f"📅 Créé le: {user.created_at}")
    print(f"🔄 Dernière mise à jour: {user.updated_at}")
    print("-" * 50)

    permissions = get_user_permissions(user)
    print("🔑 Permissions:")
    for perm in permissions:
        print(f"  • {perm}")
