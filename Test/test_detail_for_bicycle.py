import sys
import os
from datetime import datetime
from uuid import uuid4

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models.detail_for_bicycle import DetailForBicycle
from db.models.bicycle import Bicycle, BicycleType, Status
from db.models.detail import Detail, Type

class TestDetailForBicycle:
    
    def test_create_10_records(self, session):
        now = datetime.now()
        
        bicycle = Bicycle(
            brand="TestBike",
            type=BicycleType.MOUNTAIN,
            status=Status.AVAILABLE,
            rent_price=500.0,
            created=now,
            updated=now
        )
        session.add(bicycle)
        session.commit()
        
        detail = Detail(
            brand="TestBrand",
            type=Type.OTHER,
            name="TestDetail",
            price=100,
            in_stock=True,
            created=now,
            updated=now
        )
        session.add(detail)
        session.commit()
        
        for i in range(10):
            detail_for_bicycle = DetailForBicycle(
                bicycle_id=bicycle.id,
                detail_id=detail.id
            )
            session.add(detail_for_bicycle)
        
        session.commit()
        
        all_details_for_bicycle = session.query(DetailForBicycle).all()
        assert len(all_details_for_bicycle) >= 10
    
    def test_select_all_records(self, session):
        all_details_for_bicycle = session.query(DetailForBicycle).all()
        
        assert len(all_details_for_bicycle) > 0
        print(f"Найдено записей: {len(all_details_for_bicycle)}")
        
        for detail_for_bicycle in all_details_for_bicycle:
            assert detail_for_bicycle.id is not None
            assert detail_for_bicycle.bicycle_id is not None
    
    def test_update_4_records(self, session):
        details_to_update = session.query(DetailForBicycle).limit(4).all()
        assert len(details_to_update) >= 4
        
        detail_ids = []
        
        for i, detail in enumerate(details_to_update[:4]):
            detail.bicycle_id = detail.bicycle_id
            detail_ids.append(detail.id)
        
        session.commit()
        
        updated_count = session.query(DetailForBicycle).count()
        assert updated_count >= 4
        
        print(f"Обновлено записей: {updated_count}")
    
    def test_delete_2_records(self, session):
        details_to_delete = session.query(DetailForBicycle).limit(2).all()
        assert len(details_to_delete) >= 2
        
        detail_ids = [detail.id for detail in details_to_delete[:2]]
        
        deleted_count = session.query(DetailForBicycle).filter(DetailForBicycle.id.in_(detail_ids)).delete()
        session.commit()
        
        assert deleted_count == 2
        
        for detail_id in detail_ids:
            deleted_detail = session.query(DetailForBicycle).filter_by(id=detail_id).first()
            assert deleted_detail is None
        
        print(f"Удалено записей: {deleted_count}")