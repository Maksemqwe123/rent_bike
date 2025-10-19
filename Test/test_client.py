import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models.client import Client

class TestClient:
    
    def test_create_10_records(self, session):
        now = datetime.now()
        
        timestamp = int(now.timestamp())
        for i in range(10):
            client = Client(
                name=f"C{i+1}",
                passport=f"AB{i+timestamp+i:06d}",
                phone=f"+7905012345{i+timestamp+i:02d}",
                country="Russia",
                city="Moscow",
                address=f"St{i+1}",
                email=f"c{i+1}_{timestamp}@t.com",
                created=now,
                updated=now
            )
            session.add(client)
        
        session.commit()
        
        all_clients = session.query(Client).all()
        assert len(all_clients) >= 10
    
    def test_select_all_records(self, session):
        all_clients = session.query(Client).all()
        
        assert len(all_clients) > 0
        print(f"Найдено записей: {len(all_clients)}")
        
        for client in all_clients:
            assert client.id is not None
            assert client.name is not None
    
    def test_update_4_records(self, session):
        clients_to_update = session.query(Client).limit(4).all()
        assert len(clients_to_update) >= 4
        
        client_ids = []
        
        for i, client in enumerate(clients_to_update[:4]):
            client.name = f"U{i+1}"
            client.email = f"u{i+1}_{client.id}@t.com"
            client_ids.append(client.id)
        
        session.commit()
        
        updated_count = session.query(Client).filter(Client.name.like("U%")).count()
        assert updated_count >= 4
        
        print(f"Обновлено записей: {updated_count}")
    
    def test_delete_2_records(self, session):
        clients_to_delete = session.query(Client).limit(2).all()
        assert len(clients_to_delete) >= 2
        
        client_ids = [client.id for client in clients_to_delete[:2]]
        
        deleted_count = session.query(Client).filter(Client.id.in_(client_ids)).delete()
        session.commit()
        
        assert deleted_count == 2
        
        for client_id in client_ids:
            deleted_client = session.query(Client).filter_by(id=client_id).first()
            assert deleted_client is None
        
        print(f"Удалено записей: {deleted_count}")