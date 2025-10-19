import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models.bicycle import Bicycle, BicycleType, Status

class TestBicycle:
    
    def test_create_10_records(self, session):
        now = datetime.now()
        
        for i in range(10):
            bicycle = Bicycle(
                brand=f"Bike_{i+1}",
                type=BicycleType.MOUNTAIN,
                status=Status.AVAILABLE,
                rent_price=100.0 + i * 50,
                created=now,
                updated=now
            )
            session.add(bicycle)
        
        session.commit()
        
        all_bikes = session.query(Bicycle).all()
        assert len(all_bikes) >= 10
    
    def test_select_all_records(self, session):
        all_bikes = session.query(Bicycle).all()
        
        assert len(all_bikes) > 0
        print(f"Найдено записей: {len(all_bikes)}")
        
        for bike in all_bikes:
            assert bike.id is not None
            assert bike.brand is not None
    
    def test_update_4_records(self, session):
        bikes_to_update = session.query(Bicycle).limit(4).all()
        assert len(bikes_to_update) >= 4
        
        bike_ids = []
        
        for i, bike in enumerate(bikes_to_update[:4]):
            bike.status = Status.RENTED
            bike.rent_price = 1000.0 + i * 100
            bike_ids.append(bike.id)
        
        session.commit()
        
        updated_count = session.query(Bicycle).filter_by(status=Status.RENTED).count()
        assert updated_count >= 4
        
        print(f"Обновлено записей: {updated_count}")
    
    def test_delete_2_records(self, session):
        bikes_to_delete = session.query(Bicycle).limit(2).all()
        assert len(bikes_to_delete) >= 2
        
        bike_ids = [bike.id for bike in bikes_to_delete[:2]]
        
        deleted_count = session.query(Bicycle).filter(Bicycle.id.in_(bike_ids)).delete()
        session.commit()
        
        assert deleted_count == 2
        
        for bike_id in bike_ids:
            deleted_bike = session.query(Bicycle).filter_by(id=bike_id).first()
            assert deleted_bike is None
        
        print(f"Удалено записей: {deleted_count}")
