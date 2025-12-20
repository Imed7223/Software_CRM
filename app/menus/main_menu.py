from app.database.database import SessionLocal
from app.utils.auth import authenticate_user
from app.menus.users_menu import menu_users
from app.menus.clients_menu import menu_clients
from app.menus.contracts_menu import menu_contracts
from app.menus.events_menu import menu_events
from app.models.users import Department


def login():
    """Menu de connexion"""
    db = SessionLocal()

    print("\n" + "=" * 50)
    print("        CONNEXION - EPICEVENTS CRM")
    print("=" * 50)

    email = input("Email: ")
    password = input("Mot de passe: ")

    user = authenticate_user(db, email, password)

    if user:
        print(f"\n✅ Bienvenue {user.full_name} ({user.department.value})")
        return db, user
    else:
        print("\n❌ Identifiants incorrects")
        db.close()
        return None, None


def main_menu():
    """Menu principal"""
    db, user = login()
    if not user:
        return

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

            print("0. 🚪  Déconnexion")
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
            elif choice == "0":
                print("\n👋 Au revoir !")
                break
            else:
                print("\n❌ Option invalide")

    finally:
        db.close()