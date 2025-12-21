#!/usr/bin/env python3
"""
Script d'initialisation de la base de données avec des données de démonstration
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from app.database.database import SessionLocal, init_db
from app.models.users import User, Department
from app.models.clients import Client
from app.models.contracts import Contract
from app.models.events import Event
from app.utils.auth import hash_password


def create_initial_data():
    """Crée les données initiales pour la démonstration"""
    db = SessionLocal()

    try:
        # 1. Créer les utilisateurs
        users_data = [
            {
                'employee_id': 'EMP001',
                'full_name': 'Bill Boquet',
                'email': 'bill.boquet@epicevents.com',
                'department': Department.SALES,
                'password': 'password123'
            },
            {
                'employee_id': 'EMP002',
                'full_name': 'Kate Hastroff',
                'email': 'kate.hastroff@epicevents.com',
                'department': Department.SUPPORT,
                'password': 'password123'
            },
            {
                'employee_id': 'EMP003',
                'full_name': 'Alienor Vichum',
                'email': 'alienor.vichum@epicevents.com',
                'department': Department.SUPPORT,
                'password': 'password123'
            },
            {
                'employee_id': 'EMP004',
                'full_name': 'Marc Dubois',
                'email': 'marc.dubois@epicevents.com',
                'department': Department.SALES,
                'password': 'password123'
            },
            {
                'employee_id': 'EMP005',
                'full_name': 'Sophie Martin',
                'email': 'sophie.martin@epicevents.com',
                'department': Department.SALES,
                'password': 'password123'
            },
            {
                'employee_id': 'EMP006',
                'full_name': 'Thomas Leroy',
                'email': 'thomas.leroy@epicevents.com',
                'department': Department.SUPPORT,
                'password': 'password123'
            },
            {
                'employee_id': 'EMP007',
                'full_name': 'Julie Bernard',
                'email': 'julie.bernard@epicevents.com',
                'department': Department.MANAGEMENT,
                'password': 'admin123'
            },
            {
                'employee_id': 'EMP008',
                'full_name': 'Paul Richard',
                'email': 'paul.richard@epicevents.com',
                'department': Department.MANAGEMENT,
                'password': 'admin123'
            }
        ]

        users = {}
        for user_data in users_data:
            user = User(
                employee_id=user_data['employee_id'],
                full_name=user_data['full_name'],
                email=user_data['email'],
                hashed_password=hash_password(user_data['password']),
                department=user_data['department']
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            users[user_data['employee_id']] = user

        # 2. Créer les clients
        clients_data = [
            {
                'full_name': 'Kevin Casey',
                'email': 'kevin@startup.io',
                'phone': '+33612345678',
                'company_name': 'Cool Startup LLC',
                'commercial_id': users['EMP001'].id
            },
            {
                'full_name': 'John Quick',
                'email': 'john.quick@gmail.com',
                'phone': '+12345678901',
                'company_name': 'Quick Enterprises',
                'commercial_id': users['EMP001'].id
            },
            {
                'full_name': 'Lou Bouzin',
                'email': 'contact@bouzin.group',
                'phone': '+33698765432',
                'company_name': 'Bouzin Group',
                'commercial_id': users['EMP004'].id
            },
            {
                'full_name': 'Marie Dupont',
                'email': 'marie.dupont@techcorp.fr',
                'phone': '+33123456789',
                'company_name': 'TechCorp France',
                'commercial_id': users['EMP005'].id
            },
            {
                'full_name': 'Ahmed Khan',
                'email': 'ahmed.khan@globaltrade.com',
                'phone': '+442012345678',
                'company_name': 'Global Trade Ltd',
                'commercial_id': users['EMP004'].id
            },
            {
                'full_name': 'Sarah Chen',
                'email': 'sarah.chen@innovate.asia',
                'phone': '+85212345678',
                'company_name': 'Innovate Asia',
                'commercial_id': users['EMP005'].id
            },
            {
                'full_name': 'Roberto Silva',
                'email': 'roberto@silva.br',
                'phone': '+5511987654321',
                'company_name': 'Silva Construções',
                'commercial_id': users['EMP001'].id
            },
            {
                'full_name': 'Anna Schmidt',
                'email': 'anna.schmidt@engineering.de',
                'phone': '+4915123456789',
                'company_name': 'Schmidt Engineering',
                'commercial_id': users['EMP004'].id
            }
        ]

        clients = {}
        for client_data in clients_data:
            client = Client(
                full_name=client_data['full_name'],
                email=client_data['email'],
                phone=client_data['phone'],
                company_name=client_data['company_name'],
                commercial_id=client_data['commercial_id'],
                created_date=datetime.now(),
                last_contact=datetime.now()
            )
            db.add(client)
            db.commit()
            db.refresh(client)
            clients[client_data['email']] = client

        # 3. Créer les contrats
        contracts_data = [
            {
                'total_amount': 15000.00,
                'remaining_amount': 5000.00,
                'is_signed': True,
                'client_id': clients['kevin@startup.io'].id,
                'commercial_id': users['EMP001'].id
            },
            {
                'total_amount': 8000.00,
                'remaining_amount': 0.00,
                'is_signed': True,
                'client_id': clients['john.quick@gmail.com'].id,
                'commercial_id': users['EMP001'].id
            },
            {
                'total_amount': 20000.00,
                'remaining_amount': 0.00,
                'is_signed': True,
                'client_id': clients['contact@bouzin.group'].id,
                'commercial_id': users['EMP004'].id
            },
            {
                'total_amount': 12000.00,
                'remaining_amount': 3000.00,
                'is_signed': True,
                'client_id': clients['marie.dupont@techcorp.fr'].id,
                'commercial_id': users['EMP005'].id
            },
            {
                'total_amount': 25000.00,
                'remaining_amount': 15000.00,
                'is_signed': True,
                'client_id': clients['ahmed.khan@globaltrade.com'].id,
                'commercial_id': users['EMP004'].id
            },
            {
                'total_amount': 18000.00,
                'remaining_amount': 18000.00,
                'is_signed': False,
                'client_id': clients['sarah.chen@innovate.asia'].id,
                'commercial_id': users['EMP005'].id
            },
            {
                'total_amount': 30000.00,
                'remaining_amount': 30000.00,
                'is_signed': False,
                'client_id': clients['roberto@silva.br'].id,
                'commercial_id': users['EMP001'].id
            },
            {
                'total_amount': 9500.00,
                'remaining_amount': 0.00,
                'is_signed': True,
                'client_id': clients['anna.schmidt@engineering.de'].id,
                'commercial_id': users['EMP004'].id
            }
        ]

        contracts = {}
        for i, contract_data in enumerate(contracts_data, 1):
            contract = Contract(
                total_amount=contract_data['total_amount'],
                remaining_amount=contract_data['remaining_amount'],
                is_signed=contract_data['is_signed'],
                client_id=contract_data['client_id'],
                commercial_id=contract_data['commercial_id']
            )
            db.add(contract)
            db.commit()
            db.refresh(contract)
            contracts[i] = contract

        # 4. Créer les événements
        events_data = [
            {
                'name': 'Kevin Startup Launch',
                'start_date': datetime(2023, 6, 4, 13, 0),
                'end_date': datetime(2023, 6, 4, 18, 0),
                'location': 'Paris Convention Center',
                'attendees': 150,
                'support_id': users['EMP002'].id,
                'client_id': clients['kevin@startup.io'].id,
                'contract_id': contracts[1].id,
                'notes': 'Lancement produit innovant. Catering inclus.'
            },
            {
                'name': 'John Quick Wedding',
                'start_date': datetime(2023, 6, 4, 13, 0),
                'end_date': datetime(2023, 6, 5, 2, 0),
                'location': '53 Rue du Château, Candé-sur-Beuvron',
                'attendees': 75,
                'support_id': users['EMP002'].id,
                'client_id': clients['john.quick@gmail.com'].id,
                'contract_id': contracts[2].id,
                'notes': 'Mariage avec réception. DJ à organiser.'
            },
            {
                'name': 'Lou Bouzin General Assembly',
                'start_date': datetime(2023, 5, 5, 15, 0),
                'end_date': datetime(2023, 5, 5, 17, 0),
                'location': 'Salle des fêtes de Mufflins',
                'attendees': 200,
                'support_id': users['EMP003'].id,
                'client_id': clients['contact@bouzin.group'].id,
                'contract_id': contracts[3].id,
                'notes': 'Assemblée générale des actionnaires.'
            },
            {
                'name': 'TechCorp Annual Conference',
                'start_date': datetime(2023, 7, 20, 9, 0),
                'end_date': datetime(2023, 7, 20, 17, 0),
                'location': 'Palais des Congrès, Lyon',
                'attendees': 300,
                'support_id': users['EMP006'].id,
                'client_id': clients['marie.dupont@techcorp.fr'].id,
                'contract_id': contracts[4].id,
                'notes': 'Conférence annuelle sur les nouvelles technologies.'
            },
            {
                'name': 'Global Trade Summit',
                'start_date': datetime(2023, 8, 10, 10, 0),
                'end_date': datetime(2023, 8, 11, 16, 0),
                'location': 'Excel London',
                'attendees': 500,
                'support_id': users['EMP003'].id,
                'client_id': clients['ahmed.khan@globaltrade.com'].id,
                'contract_id': contracts[5].id,
                'notes': 'Sommet annuel du commerce international.'
            },
            {
                'name': 'Innovate Asia Demo Day',
                'start_date': datetime(2023, 9, 15, 14, 0),
                'end_date': datetime(2023, 9, 15, 19, 0),
                'location': 'Hong Kong Convention Centre',
                'attendees': 250,
                'support_id': users['EMP002'].id,
                'client_id': clients['sarah.chen@innovate.asia'].id,
                'contract_id': contracts[6].id,
                'notes': 'Présentation des startups asiatiques.'
            },
            {
                'name': 'Silva Construction Inauguration',
                'start_date': datetime(2023, 10, 5, 11, 0),
                'end_date': datetime(2023, 10, 5, 15, 0),
                'location': 'São Paulo Business Center',
                'attendees': 100,
                'support_id': users['EMP006'].id,
                'client_id': clients['roberto@silva.br'].id,
                'contract_id': contracts[7].id,
                'notes': 'Inauguration nouveau siège social.'
            },
            {
                'name': 'Schmidt Engineering Workshop',
                'start_date': datetime(2023, 11, 20, 8, 30),
                'end_date': datetime(2023, 11, 22, 17, 0),
                'location': 'Berlin Tech Hub',
                'attendees': 80,
                'support_id': users['EMP003'].id,
                'client_id': clients['anna.schmidt@engineering.de'].id,
                'contract_id': contracts[8].id,
                'notes': 'Atelier de formation ingénierie avancée.'
            }
        ]

        for event_data in events_data:
            event = Event(
                name=event_data['name'],
                start_date=event_data['start_date'],
                end_date=event_data['end_date'],
                location=event_data['location'],
                attendees=event_data['attendees'],
                support_id=event_data['support_id'],
                client_id=event_data['client_id'],
                contract_id=event_data['contract_id'],
                notes=event_data['notes']
            )
            db.add(event)

        db.commit()

        print("✅ Base de données initialisée avec succès!")
        print(f"   {len(users)} utilisateurs créés")
        print(f"   {len(clients)} clients créés")
        print(f"   {len(contracts)} contrats créés")
        print(f"   {len(events_data)} événements créés")
        print("\n📋 CRÉDENTIELS DE TEST:")
        print("   Commercial: bill.boquet@epicevents.com / password123")
        print("   Support: kate.hastroff@epicevents.com / password123")
        print("   Management: julie.bernard@epicevents.com / admin123")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'initialisation: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🔄 Initialisation de la base de données Epicevents CRM...")

    # Créer les tables
    init_db()

    # Créer les données initiales
    create_initial_data()

    print("\n🎉 Installation terminée! Lancez l'application avec: python main.py")