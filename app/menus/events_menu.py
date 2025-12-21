from app.crud import crud_events, crud_clients, crud_contracts, crud_users
from datetime import datetime
from app.models.users import Department


def display_events(events):
    """Afficher la liste des événements"""
    if not events:
        print("Aucun événement trouvé")
        return

    print(f"\n📅 Événements ({len(events)}):")
    for event in events:
        support = f"Support: {event.support_id}" if event.support_id else "Sans support"
        print(f"  {event.id}: {event.name} - {event.start_date} - {event.location} - {support}")


def menu_events(db, user):
    """Menu gestion des événements"""
    while True:
        print("\n" + "=" * 50)
        print("        GESTION DES ÉVÉNEMENTS")
        print("=" * 50)
        print("1. 📋  Liste des événements")
        print("2. ➕  Ajouter un événement")
        print("3. 👁️  Voir un événement")
        print("4. ✏️  Modifier un événement")
        print("5. 👥  Assigner un support")
        print("6. 🗑️  Supprimer un événement")
        print("7. 🔍  Filtres et recherche")
        print("8. ⚠️  Événements sans support")
        print("9. 🔮  Événements à venir")
        print("10. 📊  Statistiques")
        print("0. ↩️  Retour")
        print("-" * 50)

        choice = input("Choisissez une option: ")

        if choice == "1":
            events = crud_events.get_all_events(db)
            display_events(events)

        elif choice == "2":
            print("\n➕ Ajouter un événement:")

            try:
                name = input("Nom: ")
                start_str = input("Date début (YYYY-MM-DD HH:MM): ")
                end_str = input("Date fin (YYYY-MM-DD HH:MM): ")
                location = input("Lieu: ")
                attendees = int(input("Nombre de participants: "))
                notes = input("Notes: ")
                client_id = int(input("ID client: "))
                contract_id = int(input("ID contrat: "))

                start_date = datetime.strptime(start_str, '%Y-%m-%d %H:%M')
                end_date = datetime.strptime(end_str, '%Y-%m-%d %H:%M')

                # Optionnel: assigner un support
                support_id = None
                assign_support = input("Assigner un support maintenant? (o/n): ")
                if assign_support.lower() == 'o':
                    supports = crud_users.get_support_users(db)
                    print("Supports disponibles:")
                    for s in supports:
                        print(f"  {s.id}: {s.full_name}")
                    support_id = int(input("ID support: "))

                new_event = crud_events.create_event(
                    db, name, start_date, end_date, location,
                    attendees, notes, client_id, contract_id, support_id
                )
                print(f"✅ Événement créé: {new_event.name}")
            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "3":
            event_id = input("\n👁️ ID de l'événement: ")
            try:
                event = crud_events.get_event_by_id(db, int(event_id))
                if event:
                    print(f"\n📅 Détails événement:")
                    print(f"  ID: {event.id}")
                    print(f"  Nom: {event.name}")
                    print(f"  Début: {event.start_date}")
                    print(f"  Fin: {event.end_date}")
                    print(f"  Lieu: {event.location}")
                    print(f"  Participants: {event.attendees}")
                    print(f"  Notes: {event.notes}")
                    print(f"  Support ID: {event.support_id}")
                    print(f"  Client ID: {event.client_id}")
                    print(f"  Contrat ID: {event.contract_id}")
                else:
                    print("❌ Événement non trouvé")
            except:
                print("❌ ID invalide")

        elif choice == "4":
            event_id = input("\n✏️ ID de l'événement à modifier: ")
            try:
                existing = crud_events.get_event_by_id(db, int(event_id))
                if not existing:
                    print("❌ Événement non trouvé")
                    continue

                print(f"Modification de {existing.name}")
                print("Laissez vide pour ne pas modifier")

                updates = {}
                new_name = input(f"Nom [{existing.name}]: ")
                if new_name:
                    updates['name'] = new_name

                new_location = input(f"Lieu [{existing.location}]: ")
                if new_location:
                    updates['location'] = new_location

                new_attendees = input(f"Participants [{existing.attendees}]: ")
                if new_attendees:
                    updates['attendees'] = int(new_attendees)

                new_notes = input(f"Notes [{existing.notes}]: ")
                if new_notes:
                    updates['notes'] = new_notes

                if updates:
                    updated = crud_events.update_event(db, existing.id, **updates)
                    print(f"✅ Événement mis à jour")
                else:
                    print("⚠️  Aucune modification")

            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "5":
            event_id = input("\n👥 ID de l'événement: ")
            try:
                event = crud_events.get_event_by_id(db, int(event_id))
                if not event:
                    print("❌ Événement non trouvé")
                    continue

                supports = crud_users.get_support_users(db)
                print("Supports disponibles:")
                for s in supports:
                    print(f"  {s.id}: {s.full_name}")

                support_id = int(input("ID support: "))
                updated = crud_events.assign_support_to_event(db, event.id, support_id)
                print(f"✅ Support assigné")
            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "6":
            event_id = input("\n🗑️ ID de l'événement à supprimer: ")
            try:
                existing = crud_events.get_event_by_id(db, int(event_id))
                if not existing:
                    print("❌ Événement non trouvé")
                    continue

                confirm = input(f"Confirmer la suppression de {existing.name}? (o/n): ")
                if confirm.lower() == 'o':
                    deleted = crud_events.delete_event(db, existing.id)
                    print(f"✅ Événement supprimé")
                else:
                    print("❌ Annulé")
            except:
                print("❌ ID invalide")

        elif choice == "7":  # Nouvelle option
            from .filters_menu import menu_event_filters
            menu_event_filters(db, user)

        elif choice == "8":
            events = crud_events.get_events_without_support(db)
            print(f"\n⚠️  Événements sans support ({len(events)}):")
            for event in events:
                print(f"  {event.id}: {event.name} - {event.start_date} - {event.location}")

        elif choice == "9":
            try:
                days = int(input("Nombre de jours à venir (défaut: 7): ") or "7")
                events = crud_events.get_upcoming_events(db, days)
                print(f"\n🔮 Événements à venir ({len(events)} dans {days} jours):")
                for event in events:
                    support = f"Support: {event.support_id}" if event.support_id else "⚠️ Sans support"
                    print(f"  {event.id}: {event.name} - {event.start_date} - {event.location} - {support}")
            except:
                print("❌ Nombre invalide")

        elif choice == "10":
            try:
                summary = crud_events.get_events_summary(db)
                print(f"\n📊 Statistiques des événements:")
                print(f"  Total: {summary['total']}")
                print(f"  Avec support: {summary['with_support']}")
                print(f"  Sans support: {summary['without_support']}")
                print(f"  À venir: {summary['upcoming']}")
                print(f"  En cours: {summary['ongoing']}")
                print(f"  Passés: {summary['past']}")

                if summary['total'] > 0:
                    percent = (summary['with_support'] / summary['total']) * 100
                    print(f"  Taux d'assignation: {percent:.1f}%")
            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "0":
            break

        else:
            print("❌ Option invalide")