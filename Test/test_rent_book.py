import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models.rent_book import RentBook
from db.models.bicycle import Bicycle, BicycleType, Status
from db.models.client import Client
from db.models.staff import Staff

class TestRentBook:
    
    def test_create_10_records(self, session):
        now = datetime.now()
        
        bicycle = Bicycle(
            brand="RentBike",
            type=BicycleType.CITY,
            status=Status.AVAILABLE,
            rent_price=300.0,
            created=now,
            updated=now
        )
        session.add(bicycle)
        session.commit()
        
        timestamp = int(now.timestamp())
        client = Client(
            name="RentClient",
            passport=f"RC{timestamp:06d}",
            phone=f"+790501234{timestamp%100:02d}",
            country="Russia",
            city="Moscow",
            address="Rent St 1",
            email=f"rent{timestamp}@t.com",
            created=now,
            updated=now
        )
        session.add(client)
        session.commit()
        
        staff = Staff(
            name="RentStaff",
            country="Russia",
            city="Moscow",
            address="Rent Office 1",
            email=f"rentstaff{timestamp}@t.com",
            passport=f"RS{timestamp:06d}",
            phone=f"+790501234{timestamp%100+1:02d}",
            salary=1500.0,
            created=now,
            updated=now
        )
        session.add(staff)
        session.commit()
        
        for i in range(10):
            rent_book = RentBook(
                time=60 + i * 10,
                paid=True,
                bicycle_id=bicycle.id,
                client_id=client.id,
                staff_id=staff.id,
                created=now,
                updated=now
            )
            session.add(rent_book)
        
        session.commit()
        
        all_rent_books = session.query(RentBook).all()
        assert len(all_rent_books) >= 10
    
    def test_select_all_records(self, session):
        all_rent_books = session.query(RentBook).all()
        
        assert len(all_rent_books) > 0
        print(f"Найдено записей: {len(all_rent_books)}")
        
        for rent_book in all_rent_books:
            assert rent_book.id is not None
            assert rent_book.bicycle_id is not None
    
    def test_update_4_records(self, session):
        rent_books_to_update = session.query(RentBook).limit(4).all()
        assert len(rent_books_to_update) >= 4
        
        rent_book_ids = []
        
        for i, rent_book in enumerate(rent_books_to_update[:4]):
            rent_book.time = 120 + i * 20
            rent_book.paid = False
            rent_book_ids.append(rent_book.id)
        
        session.commit()
        
        updated_count = session.query(RentBook).filter(RentBook.paid == False).count()
        assert updated_count >= 4
        
        print(f"Обновлено записей: {updated_count}")
    
    def test_delete_2_records(self, session):
        rent_books_to_delete = session.query(RentBook).limit(2).all()
        assert len(rent_books_to_delete) >= 2
        
        rent_book_ids = [rent_book.id for rent_book in rent_books_to_delete[:2]]
        
        deleted_count = session.query(RentBook).filter(RentBook.id.in_(rent_book_ids)).delete()
        session.commit()
        
        assert deleted_count == 2
        
        for rent_book_id in rent_book_ids:
            deleted_rent_book = session.query(RentBook).filter_by(id=rent_book_id).first()
            assert deleted_rent_book is None
        
        print(f"Удалено записей: {deleted_count}")