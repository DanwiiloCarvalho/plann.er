from app.adapters.outbound.database.repositories.trip_repository import TripRepository
from app.adapters.outbound.database.repositories.email_to_invite_repository import EmailToInviteRepository
from app.adapters.outbound.database.repositories.link_repository import LinkRepository
from app.adapters.outbound.database.models.trip import Trip
from app.adapters.outbound.database.models.link import Link
from app.adapters.outbound.database.models.email_to_invite import EmailToInvite
import datetime
import uuid


# async def test_get_trip_by_id(db_session):
#     trip_repo = TripRepository(db_session)
#     # 632f07da-352c-11f1-b1da-6a0d0496cd1a
#     result = await trip_repo.get_by_id(uuid.UUID('632f07da-352c-11f1-b1da-6a0d0496cd1a'))
#     print()
#     print(f'Resultado = {result.owner_name if result else None}')

# async def test_get_trip_by_id(db_session):
#     trip_repo = TripRepository(db_session)
#     result = await trip_repo.get_by_id(uuid.UUID('cb1df2f6-3857-11f1-b725-8e30235885fa'))
#     print()
#     print(f'Resultado = {result.owner_email if result else None}')


# async def test_create_trip(db_session):
#     trip_repo = TripRepository(db_session)
#     new_trip = Trip(
#         id=uuid.uuid1(),
#         destination='São Luís',
#         start_date=datetime.date(2026, 4, 25),
#         end_date=datetime.date(2026, 5, 2),
#         owner_name='Dandara Carvalho',
#         owner_email='dandara@email.com'
#     )
#     trip: Trip = await trip_repo.create(new_trip)
#     print()
#     print(f'Viagem cadastrada: {trip}')

# async def test_update_trip(db_session):
#     trip_repo = TripRepository(db_session)
#     trip_id = uuid.UUID('e20dd4b6-3c1e-11f1-bd56-a2fbf8161bbd')
#     data = {
#         'owner_name': 'Danilo Costa Carvalho'
#     }
#     trip: Trip | None = await trip_repo.update(obj_id=trip_id, obj_in=data)
#     print()
#     print(f'Viagem atualizada: {trip.owner_name if trip else None}')

# async def test_delete_trip_by_id(db_session):
#     trip_repo = TripRepository(db_session)
#     result = await trip_repo.delete_by_id(uuid.UUID('632f07da-352c-11f1-b1da-6a0d0496cd1a'))
#     print()
#     print(f'Resultado = {result}')

# async def test_list_all_trips(db_session):
#     trip_repo = TripRepository(db_session)
#     trips = await trip_repo.list_all()
#     print()
#     print(f'Todas as viagens: ')
#     for trip in trips:
#         print(trip.owner_name)

# async def test_get_trips_by_owner_name(db_session):
#     trip_repo = TripRepository(db_session)
#     trips = await trip_repo.get_by_owner_name('Danilo Costa Carvalho')
#     print()
#     print(f'Todas as viagens: ')
#     for trip in trips:
#         print(trip.owner_email)


# async def test_confirm_trip_by_id(db_session):
#     trip_repo = TripRepository(db_session)
#     confirmed_trip: Trip | None = await trip_repo.confirm_trip(uuid.UUID('1337d9ce-4502-11f1-9d3c-cada98130165'))
#     print()
#     print(
#         f'Viagem confirmada? {confirmed_trip.destination if confirmed_trip else None}')

# async def test_create_email_to_invite(db_session):
#     email_to_invite_repo = EmailToInviteRepository(db_session)
#     new_email_to_invite = EmailToInvite(
#         id=uuid.uuid1(),
#         email='deborah.irlanda@email.com',
#         fullname='Deborah Carvalho',
#         trip_id=uuid.UUID('e20dd4b6-3c1e-11f1-bd56-a2fbf8161bbd')
#     )
#     email_to_invite: EmailToInvite = await email_to_invite_repo.create(new_email_to_invite)
#     print()
#     print(f'E-mail cadastrado: {email_to_invite.email}')


# async def test_find_emails_from_trip(db_session):
#     email_to_invite_repo = EmailToInviteRepository(db_session)
#     emails_found = await email_to_invite_repo.find_emails_from_trip(
#         uuid.UUID('e20dd4b6-3c1e-11f1-bd56-a2fbf8161bbd'))
#     emails_found = [email.email for email in emails_found]
#     print()
#     print(f'Lista de emails da viagem: {emails_found}')


# async def test_create_link(db_session):
#     link_repo = LinkRepository(db_session)
#     new_link = Link(
#         id=uuid.uuid1(),
#         link='www.deborah.com.br',
#         title='Titulo de Deborah',
#         trip_id=uuid.UUID('e20dd4b6-3c1e-11f1-bd56-a2fbf8161bbd')
#     )
#     link: Link = await link_repo.create(new_link)
#     print()
#     print(f'Link cadastrado: {link.link}')


async def test_find_links_from_trip(db_session):
    link_repo = LinkRepository(db_session)
    links_found = await link_repo.find_links_from_trip(
        uuid.UUID('e20dd4b6-3c1e-11f1-bd56-a2fbf8161bbd'))
    links_found = [link.link for link in links_found]
    print()
    print(f'Lista de links da viagem: {links_found}')
