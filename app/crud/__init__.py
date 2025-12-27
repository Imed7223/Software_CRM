from .crud_users import (
    create_user, get_all_users, get_user_by_id, get_user_by_email,
    update_user, delete_user, get_users_by_department,
    get_sales_users, get_support_users, get_management_users
)
from .crud_clients import (
    create_client, get_all_clients, get_client_by_id,
    update_client, delete_client, get_clients_by_commercial
)
from .crud_contracts import (
    create_contract, get_all_contracts, get_contract_by_id,
    update_contract, delete_contract, get_contracts_by_client,
    sign_contract, add_payment, get_contract_summary
)
from .crud_events import (
    create_event, get_all_events, get_event_by_id,
    update_event, delete_event, get_events_by_client,
    assign_support_to_event, get_events_without_support,
    get_upcoming_events, get_events_summary
)

__all__ = [
    # Users
    'create_user', 'get_all_users', 'get_user_by_id', 'get_user_by_email',
    'update_user', 'delete_user', 'get_users_by_department',
    'get_sales_users', 'get_support_users', 'get_management_users',

    # Clients
    'create_client', 'get_all_clients', 'get_client_by_id',
    'update_client', 'delete_client', 'get_clients_by_commercial',

    # Contracts
    'create_contract', 'get_all_contracts', 'get_contract_by_id',
    'update_contract', 'delete_contract', 'get_contracts_by_client',
    'sign_contract', 'add_payment', 'get_contract_summary',

    # Events
    'create_event', 'get_all_events', 'get_event_by_id',
    'update_event', 'delete_event', 'get_events_by_client',
    'assign_support_to_event', 'get_events_without_support',
    'get_upcoming_events', 'get_events_summary'
]
