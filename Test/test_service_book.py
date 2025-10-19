import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models.service_book import ServiceBook
from db.models.bicycle import Bicycle, BicycleType, Status
from db.models.staff import Staff
from db.models.detail import Detail, Type

class TestServiceBook:
    
    def test_create_10_records(self, session):
        now = datetime.now()
        
        bicycle = Bicycle(
            brand="ServiceBike",
            type=BicycleType.ROAD,
            status=Status.AVAILABLE,
            rent_price=400.0,
            created=now,
            updated=now
        )
        session.add(bicycle)
        session.commit()
        
        timestamp = int(now.timestamp())
        staff = Staff(
            name="ServiceStaff",
            country="Russia",
            city="Moscow",
            address="Service Office 1",
            email=f"servicestaff{timestamp}@t.com",
            passport=f"SV{timestamp:06d}",
            phone=f"+790501234{timestamp%100+2:02d}",
            salary=2000.0,
            created=now,
            updated=now
        )
        session.add(staff)
        session.commit()
        
        detail = Detail(
            brand="ServiceBrand",
            type=Type.OTHER,
            name="ServiceDetail",
            price=100,
            in_stock=True,
            created=now,
            updated=now
        )
        session.add(detail)
        session.commit()
        
        for i in range(10):
            service_book = ServiceBook(
                bicycle_id=bicycle.id,
                detail_id=detail.id,
                price=200.0 + i * 50,
                staff_id=staff.id,
                created=now,
                updated=now
            )
            session.add(service_book)
        
        session.commit()
        
        all_service_books = session.query(ServiceBook).all()
        assert len(all_service_books) >= 10
    
    def test_select_all_records(self, session):
        all_service_books = session.query(ServiceBook).all()
        
        assert len(all_service_books) > 0
        print(f"Найдено записей: {len(all_service_books)}")
        
        for service_book in all_service_books:
            assert service_book.id is not None
            assert service_book.bicycle_id is not None
    
    def test_update_4_records(self, session):
        service_books_to_update = session.query(ServiceBook).limit(4).all()
        assert len(service_books_to_update) >= 4
        
        service_book_ids = []
        
        for i, service_book in enumerate(service_books_to_update[:4]):
            service_book.price = 2000.0 + i * 200
            service_book_ids.append(service_book.id)
        
        session.commit()
        
        updated_count = session.query(ServiceBook).filter(ServiceBook.price >= 2000.0).count()
        assert updated_count >= 4
        
        print(f"Обновлено записей: {updated_count}")
    
    def test_delete_2_records(self, session):
        service_books_to_delete = session.query(ServiceBook).limit(2).all()
        assert len(service_books_to_delete) >= 2
        
        service_book_ids = [service_book.id for service_book in service_books_to_delete[:2]]
        
        deleted_count = session.query(ServiceBook).filter(ServiceBook.id.in_(service_book_ids)).delete()
        session.commit()
        
        assert deleted_count == 2
        
        for service_book_id in service_book_ids:
            deleted_service_book = session.query(ServiceBook).filter_by(id=service_book_id).first()
            assert deleted_service_book is None
        
        print(f"Удалено записей: {deleted_count}")