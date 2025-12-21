"""
Menus de filtres avancés pour les différentes équipes
"""
from datetime import datetime, timedelta
from app.crud import (
    crud_clients, crud_contracts, crud_events, crud_users
)
from app.models.users import Department


def menu_contract_filters(db, user):
    """Menu de filtres pour les contrats (Commercial)"""
    while True:
        print("\n" + "=" * 50)
        print("        FILTRES CONTRATS - COMMERCIAL")
        print("=" * 50)
        print("1. 📄 Contrats non signés")
        print("2. 💰 Contrats non entièrement payés")
        print("3. 📊 Mes contrats")
        print("4. 🔍 Recherche avancée")
        print("0. ↩️ Retour")
        print("-" * 50)

        choice = input("Choisissez une option: ")

        if choice == "1":
            contracts = crud_contracts.get_unsigned_contracts(db)
            if user.department == Department.SALES:
                contracts = [c for c in contracts if c.commercial_id == user.id]

            if contracts:
                print(f"\n📄 Contrats non signés ({len(contracts)}):")
                for c in contracts:
                    client = crud_clients.get_client_by_id(db, c.client_id)
                    client_name = client.full_name if client else "N/A"
                    print(f"  {c.id}: {client_name} - {c.total_amount}€")
            else:
                print("✅ Tous les contrats sont signés")

        elif choice == "2":
            contracts = crud_contracts.get_unpaid_contracts(db)
            if user.department == Department.SALES:
                contracts = [c for c in contracts if c.commercial_id == user.id]

            if contracts:
                print(f"\n💰 Contrats avec solde ({len(contracts)}):")
                for c in contracts:
                    client = crud_clients.get_client_by_id(db, c.client_id)
                    client_name = client.full_name if client else "N/A"
                    print(f"  {c.id}: {client_name} - Reste: {c.remaining_amount}€ / {c.total_amount}€")
            else:
                print("✅ Tous les contrats sont payés")

        elif choice == "3":
            contracts = crud_contracts.get_contracts_by_commercial(db, user.id)
            if contracts:
                print(f"\n📊 Mes contrats ({len(contracts)}):")
                for c in contracts:
                    client = crud_clients.get_client_by_id(db, c.client_id)
                    client_name = client.full_name if client else "N/A"
                    status = "✓" if c.is_signed else "✗"
                    print(f"  {c.id}: {client_name} - {c.total_amount}€ - Signé: {status}")
            else:
                print("📭 Aucun contrat associé")

        elif choice == "4":
            print("\n🔍 Recherche avancée:")
            client_name = input("Nom client (vide pour tous): ")
            min_amount = input("Montant minimum (vide pour aucun): ")
            max_amount = input("Montant maximum (vide pour aucun): ")
            signed_input = input("Signé? (o/n/tous): ")

            try:
                filters = {}
                if client_name:
                    filters['client_name'] = client_name
                if min_amount:
                    filters['min_amount'] = float(min_amount)
                if max_amount:
                    filters['max_amount'] = float(max_amount)

                if signed_input.lower() == 'o':
                    filters['signed'] = True
                elif signed_input.lower() == 'n':
                    filters['signed'] = False

                contracts = crud_contracts.search_contracts(db, **filters)

                if user.department == Department.SALES:
                    contracts = [c for c in contracts if c.commercial_id == user.id]

                if contracts:
                    print(f"\n🔍 Résultats ({len(contracts)}):")
                    for c in contracts:
                        client = crud_clients.get_client_by_id(db, c.client_id)
                        client_name = client.full_name if client else "N/A"
                        status = "✓" if c.is_signed else "✗"
                        print(f"  {c.id}: {client_name} - {c.total_amount}€ - Signé: {status}")
                else:
                    print("🔍 Aucun résultat")

            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "0":
            break

        else:
            print("❌ Option invalide")


def menu_event_filters(db, user):
    """Menu de filtres pour les événements"""
    while True:
        print("\n" + "=" * 50)
        print("        FILTRES ÉVÉNEMENTS")
        print("=" * 50)

        if user.department == Department.SUPPORT:
            print("1. 👥 Mes événements assignés")
            print("2. ⚠️ Événements sans support")
            print("3. 📅 Événements à venir (7 jours)")
            print("4. 🔍 Recherche avancée")

        elif user.department == Department.MANAGEMENT:
            print("1. ⚠️ Événements sans support")
            print("2. 👥 Événements par support")
            print("3. 📅 Événements par période")
            print("4. 📍 Événements par lieu")
            print("5. 🔍 Recherche avancée")

        elif user.department == Department.SALES:
            print("1. 👥 Mes événements (mes clients)")
            print("2. 📅 Événements à venir")

        print("0. ↩️ Retour")
        print("-" * 50)

        choice = input("Choisissez une option: ")

        # Support team filters
        if user.department == Department.SUPPORT:
            if choice == "1":
                events = crud_events.get_events_by_support(db, user.id)
                if events:
                    print(f"\n👥 Mes événements ({len(events)}):")
                    for e in events:
                        print(f"  {e.id}: {e.name} - {e.start_date} - {e.location}")
                else:
                    print("📭 Aucun événement assigné")

            elif choice == "2":
                events = crud_events.get_events_without_support(db)
                if events:
                    print(f"\n⚠️ Événements sans support ({len(events)}):")
                    for e in events:
                        print(f"  {e.id}: {e.name} - {e.start_date} - {e.location}")
                else:
                    print("✅ Tous les événements ont un support")

            elif choice == "3":
                events = crud_events.get_upcoming_events(db, 7)
                user_events = [e for e in events if e.support_id == user.id]
                if user_events:
                    print(f"\n📅 Mes événements à venir ({len(user_events)}):")
                    for e in user_events:
                        print(f"  {e.id}: {e.name} - {e.start_date} - {e.location}")
                else:
                    print("📭 Aucun événement à venir")

            elif choice == "4":
                print("\n🔍 Recherche avancée:")
                name = input("Nom (vide pour tous): ")
                location = input("Lieu (vide pour tous): ")

                filters = {}
                if name:
                    filters['name'] = name
                if location:
                    filters['location'] = location
                filters['support_id'] = user.id  # Seulement ses événements

                events = crud_events.search_events(db, **filters)
                if events:
                    print(f"\n🔍 Mes événements ({len(events)}):")
                    for e in events:
                        print(f"  {e.id}: {e.name} - {e.start_date} - {e.location}")
                else:
                    print("🔍 Aucun résultat")

        # Management team filters
        elif user.department == Department.MANAGEMENT:
            if choice == "1":
                events = crud_events.get_events_without_support(db)
                if events:
                    print(f"\n⚠️ Événements sans support ({len(events)}):")
                    for e in events:
                        client = crud_clients.get_client_by_id(db, e.client_id)
                        client_name = client.full_name if client else "N/A"
                        print(f"  {e.id}: {e.name} - Client: {client_name} - {e.start_date}")
                else:
                    print("✅ Tous les événements ont un support")

            elif choice == "2":
                supports = crud_users.get_support_users(db)
                print("\n👥 Événements par support:")
                for support in supports:
                    events = crud_events.get_events_by_support(db, support.id)
                    print(f"\n  {support.full_name} ({len(events)} événements):")
                    for e in events:
                        print(f"    {e.id}: {e.name} - {e.start_date}")

            elif choice == "3":
                print("\n📅 Événements par période:")
                start_str = input("Date début (YYYY-MM-DD, vide pour aujourd'hui): ")
                end_str = input("Date fin (YYYY-MM-DD, vide pour +30 jours): ")

                try:
                    start_date = datetime.strptime(start_str, '%Y-%m-%d') if start_str else datetime.now()
                    end_date = datetime.strptime(end_str, '%Y-%m-%d') if end_str else datetime.now() + timedelta(
                        days=30)

                    events = crud_events.get_events_by_date_range(db, start_date, end_date)
                    if events:
                        print(f"\n📅 Événements du {start_date.date()} au {end_date.date()} ({len(events)}):")
                        for e in events:
                            print(f"  {e.id}: {e.name} - {e.start_date} - {e.location}")
                    else:
                        print("📭 Aucun événement sur cette période")
                except Exception as e:
                    print(f"❌ Erreur de date: {e}")

            elif choice == "4":
                location = input("\n📍 Lieu à rechercher: ")
                events = crud_events.get_events_by_location(db, location)
                if events:
                    print(f"\n📍 Événements à {location} ({len(events)}):")
                    for e in events:
                        print(f"  {e.id}: {e.name} - {e.start_date}")
                else:
                    print(f"📭 Aucun événement à {location}")

            elif choice == "5":
                print("\n🔍 Recherche avancée:")
                name = input("Nom (vide pour tous): ")
                location = input("Lieu (vide pour tous): ")
                client_id = input("ID client (vide pour tous): ")
                support_id = input("ID support (vide pour tous): ")

                filters = {}
                if name:
                    filters['name'] = name
                if location:
                    filters['location'] = location
                if client_id:
                    filters['client_id'] = int(client_id)
                if support_id:
                    filters['support_id'] = int(support_id)

                events = crud_events.search_events(db, **filters)
                if events:
                    print(f"\n🔍 Résultats ({len(events)}):")
                    for e in events:
                        support = f"Support: {e.support_id}" if e.support_id else "Sans support"
                        print(f"  {e.id}: {e.name} - {e.start_date} - {support}")
                else:
                    print("🔍 Aucun résultat")

        # Sales team filters
        elif user.department == Department.SALES:
            if choice == "1":
                # Événements des clients du commercial
                clients = crud_clients.get_clients_by_commercial(db, user.id)
                all_events = []
                for client in clients:
                    events = crud_events.get_events_by_client(db, client.id)
                    all_events.extend(events)

                if all_events:
                    print(f"\n👥 Événements de mes clients ({len(all_events)}):")
                    for e in all_events:
                        print(f"  {e.id}: {e.name} - {e.start_date} - {e.location}")
                else:
                    print("📭 Aucun événement pour vos clients")

            elif choice == "2":
                events = crud_events.get_upcoming_events(db, 30)
                # Filtrer pour ne garder que les événements des clients du commercial
                clients = crud_clients.get_clients_by_commercial(db, user.id)
                client_ids = [c.id for c in clients]
                user_events = [e for e in events if e.client_id in client_ids]

                if user_events:
                    print(f"\n📅 Événements à venir de mes clients ({len(user_events)}):")
                    for e in user_events:
                        print(f"  {e.id}: {e.name} - {e.start_date} - {e.location}")
                else:
                    print("📭 Aucun événement à venir pour vos clients")

        elif choice == "0":
            break

        else:
            print("❌ Option invalide")


def menu_client_filters(db, user):
    """Menu de filtres pour les clients"""
    while True:
        print("\n" + "=" * 50)
        print("        FILTRES CLIENTS")
        print("=" * 50)
        print("1. 🔍 Recherche clients")
        print("2. 📭 Clients sans contrat")
        print("3. ⏰ Clients sans contact (>30 jours)")
        print("4. 👥 Mes clients")
        print("0. ↩️ Retour")
        print("-" * 50)

        choice = input("Choisissez une option: ")

        if choice == "1":
            print("\n🔍 Recherche clients:")
            name = input("Nom (vide pour tous): ")
            company = input("Entreprise (vide pour tous): ")
            email = input("Email (vide pour tous): ")

            filters = {}
            if name:
                filters['name'] = name
            if company:
                filters['company'] = company
            if email:
                filters['email'] = email

            if user.department == Department.SALES:
                filters['commercial_id'] = user.id

            clients = crud_clients.search_clients(db, **filters)

            if clients:
                print(f"\n🔍 Clients trouvés ({len(clients)}):")
                for c in clients:
                    print(f"  {c.id}: {c.full_name} - {c.company_name} - {c.email}")
            else:
                print("🔍 Aucun client trouvé")

        elif choice == "2":
            clients = crud_clients.get_clients_without_contract(db)
            if user.department == Department.SALES:
                clients = [c for c in clients if c.commercial_id == user.id]

            if clients:
                print(f"\n📭 Clients sans contrat ({len(clients)}):")
                for c in clients:
                    print(f"  {c.id}: {c.full_name} - {c.company_name}")
            else:
                print("✅ Tous les clients ont au moins un contrat")

        elif choice == "3":
            clients = crud_clients.get_clients_last_contact_before(db, 30)
            if user.department == Department.SALES:
                clients = [c for c in clients if c.commercial_id == user.id]

            if clients:
                print(f"\n⏰ Clients sans contact >30 jours ({len(clients)}):")
                for c in clients:
                    days_since = (datetime.now() - c.last_contact).days
                    print(f"  {c.id}: {c.full_name} - {days_since} jours")
            else:
                print("✅ Tous les clients ont été contactés récemment")

        elif choice == "4":
            if user.department == Department.SALES:
                clients = crud_clients.get_clients_by_commercial(db, user.id)
                if clients:
                    print(f"\n👥 Mes clients ({len(clients)}):")
                    for c in clients:
                        contracts = crud_contracts.get_contracts_by_client(db, c.id)
                        signed = sum(1 for ct in contracts if ct.is_signed)
                        print(
                            f"  {c.id}: {c.full_name} - {c.company_name} - Contrats: {len(contracts)} (Signés: {signed})")
                else:
                    print("📭 Aucun client assigné")
            else:
                print("⚠️  Cette fonction est réservée aux commerciaux")

        elif choice == "0":
            break

        else:
            print("❌ Option invalide")