from app.crud import crud_events, crud_users
from datetime import datetime
from app.utils.auth import has_permission
from app.models.users import Department
from .filters_menu import menu_event_filters
from app.utils.validators import validate_datetime, validate_integer


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

        # 1. Liste des événements
        if choice == "1":
            events = crud_events.get_all_events(db)

            # SUPPORT : voir uniquement ses propres événements si manage_own_events
            if user.department == Department.SUPPORT and has_permission(user, "manage_own_events"):
                events = [e for e in events if e.support_id == user.id]

            display_events(events)

        # 2. Ajouter un événement
        elif choice == "2":
            # Le support ne peut pas créer d'événements (c'est le commercial / management)
            if user.department == Department.SUPPORT:
                print("❌ Le département support ne peut pas créer d'événements.")
                continue

            print("\n➕ Ajouter un événement:")

            try:
                name = input("Nom: ")

                start_str = input("Date début (YYYY-MM-DD HH:MM): ")
                if not validate_datetime(start_str, '%Y-%m-%d %H:%M'):
                    print("❌ Date/heure de début invalide")
                    continue

                end_str = input("Date fin (YYYY-MM-DD HH:MM): ")
                if not validate_datetime(end_str, '%Y-%m-%d %H:%M'):
                    print("❌ Date/heure de fin invalide")
                    continue

                location = input("Lieu: ")

                attendees_str = input("Nombre de participants: ")
                if not validate_integer(attendees_str):
                    print("❌ Nombre de participants invalide. Veuillez saisir un entier.")
                    continue
                attendees = int(attendees_str)

                notes = input("Notes: ")

                client_id_str = input("ID client: ")
                if not validate_integer(client_id_str):
                    print("❌ ID client invalide. Veuillez saisir un entier.")
                    continue
                client_id = int(client_id_str)

                contract_id_str = input("ID contrat: ")
                if not validate_integer(contract_id_str):
                    print("❌ ID contrat invalide. Veuillez saisir un entier.")
                    continue
                contract_id = int(contract_id_str)

                start_date = datetime.strptime(start_str, '%Y-%m-%d %H:%M')
                end_date = datetime.strptime(end_str, '%Y-%m-%d %H:%M')

                support_id = None
                assign_support = input("Assigner un support maintenant? (o/n): ")
                if assign_support.lower() == 'o':
                    supports = crud_users.get_support_users(db)
                    print("Supports disponibles:")
                    for s in supports:
                        print(f"  {s.id}: {s.full_name}")
                    support_id_str = input("ID support: ")
                    if not validate_integer(support_id_str):
                        print("❌ ID support invalide.")
                        continue
                    support_id = int(support_id_str)

                new_event = crud_events.create_event(
                    db, name, start_date, end_date, location,
                    attendees, notes, client_id, contract_id, support_id
                )
                print(f"✅ Événement créé: {new_event.name}")
            except Exception:
                db.rollback()
                print("❌ Erreur lors de la création de l'événement. Vérifiez les valeurs saisies.")

        # 3. Voir un événement
        elif choice == "3":
            event_id = input("\n👁️ ID de l'événement: ")
            if not validate_integer(event_id):
                print("❌ ID invalide. Veuillez saisir un entier.")
                continue
            try:
                event = crud_events.get_event_by_id(db, int(event_id))
                if event:
                    print("\n📅 Détails événement:")
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
            except Exception:
                print("❌ Erreur lors de la lecture de l'événement.")

        # 4. Modifier un événement
        elif choice == "4":
            event_id = input("\n✏️ ID de l'événement à modifier: ")
            if not validate_integer(event_id):
                print("❌ ID invalide. Veuillez saisir un entier.")
                continue
            try:
                existing = crud_events.get_event_by_id(db, int(event_id))
                if not existing:
                    print("❌ Événement non trouvé")
                    continue

                # SUPPORT : ne peut modifier que ses propres événements via manage_own_events
                if user.department == Department.SUPPORT:
                    if not has_permission(user, "manage_own_events"):
                        print("❌ Vous n'avez pas la permission de modifier des événements.")
                        continue
                    if existing.support_id != user.id:
                        print("❌ Vous ne pouvez modifier que vos événements qui vous sont assignés.")
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
                    if not validate_integer(new_attendees):
                        print("❌ Nombre de participants invalide.")
                        continue
                    updates['attendees'] = int(new_attendees)

                new_notes = input(f"Notes [{existing.notes}]: ")
                if new_notes:
                    updates['notes'] = new_notes

                if updates:
                    crud_events.update_event(db, existing.id, **updates)
                    print("✅ Événement mis à jour")
                else:
                    print("⚠️  Aucune modification")

            except Exception:
                db.rollback()
                print("❌ Erreur lors de la mise à jour de l'événement.")

        # 5. Assigner un support
        elif choice == "5":
            # Seul le management peut assigner un support
            if user.department != Department.MANAGEMENT:
                print("❌ Seul le management peut assigner un support à un événement.")
                continue

            event_id = input("\n👥 ID de l'événement: ")
            if not validate_integer(event_id):
                print("❌ ID invalide. Veuillez saisir un entier.")
                continue
            try:
                event = crud_events.get_event_by_id(db, int(event_id))
                if not event:
                    print("❌ Événement non trouvé")
                    continue

                supports = crud_users.get_support_users(db)
                print("Supports disponibles:")
                for s in supports:
                    print(f"  {s.id}: {s.full_name}")

                support_id_str = input("ID support: ")
                if not validate_integer(support_id_str):
                    print("❌ ID support invalide.")
                    continue
                support_id = int(support_id_str)

                crud_events.assign_support_to_event(db, event.id, support_id)
                print("✅ Support assigné")
            except Exception:
                db.rollback()
                print("❌ Erreur lors de l'assignation du support.")

        # 6. Supprimer un événement
        elif choice == "6":
            event_id = input("\n🗑️ ID de l'événement à supprimer: ")
            if not validate_integer(event_id):
                print("❌ ID invalide. Veuillez saisir un entier.")
                continue
            try:
                existing = crud_events.get_event_by_id(db, int(event_id))
                if not existing:
                    print("❌ Événement non trouvé")
                    continue

                # SUPPORT : ne peut supprimer que ses propres événements via manage_own_events
                if user.department == Department.SUPPORT:
                    if not has_permission(user, "manage_own_events"):
                        print("❌ Vous n'avez pas la permission de supprimer des événements.")
                        continue
                    if existing.support_id != user.id:
                        print("❌ Vous ne pouvez supprimer que vos événements qui vous sont assignés.")
                        continue

                confirm = input(f"Confirmer la suppression de {existing.name}? (o/n): ")
                if confirm.lower() == 'o':
                    crud_events.delete_event(db, existing.id)
                    print("✅ Événement supprimé")
                else:
                    print("❌ Annulé")
            except Exception:
                db.rollback()
                print("❌ Erreur lors de la suppression de l'événement.")

        # 7. Filtres
        elif choice == "7":
            menu_event_filters(db, user)

        # 8. Événements sans support
        elif choice == "8":
            events = crud_events.get_events_without_support(db)
            print(f"\n⚠️  Événements sans support ({len(events)}):")
            for event in events:
                print(f"  {event.id}: {event.name} - {event.start_date} - {event.location}")

        # 9. Événements à venir
        elif choice == "9":
            try:
                days_str = input("Nombre de jours à venir (défaut: 7): ") or "7"
                if not validate_integer(days_str):
                    print("❌ Nombre invalide. Veuillez saisir un entier.")
                    continue
                days = int(days_str)

                events = crud_events.get_upcoming_events(db, days)

                # SUPPORT : ne montrer que ses événements à venir
                if user.department == Department.SUPPORT and has_permission(user, "manage_own_events"):
                    events = [e for e in events if e.support_id == user.id]

                print(f"\n🔮 Événements à venir ({len(events)} dans {days} jours):")
                for event in events:
                    support = f"Support: {event.support_id}" if event.support_id else "⚠️ Sans support"
                    print(f"  {event.id}: {event.name} - {event.start_date} - {event.location} - {support}")
            except Exception:
                print("❌ Erreur lors du calcul des événements à venir.")

        # 10. Statistiques
        elif choice == "10":
            try:
                summary = crud_events.get_events_summary(db)
                print("\n📊 Statistiques des événements:")
                print(f"  Total: {summary['total']}")
                print(f"  Avec support: {summary['with_support']}")
                print(f"  Sans support: {summary['without_support']}")
                print(f"  À venir: {summary['upcoming']}")
                print(f"  En cours: {summary['ongoing']}")
                print(f"  Passés: {summary['past']}")

                if summary['total'] > 0:
                    percent = (summary['with_support'] / summary['total']) * 100
                    print(f"  Taux d'assignation: {percent:.1f}%")
            except Exception:
                db.rollback()
                print("❌ Erreur lors du calcul des statistiques.")

        elif choice == "0":
            break

        else:
            print("❌ Option invalide")
