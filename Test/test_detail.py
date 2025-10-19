import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models.detail import Detail, Type

class TestDetail:
    
    def test_create_10_records(self, session):
        now = datetime.now()
        
        detail_names = ["Brake Pad", "Chain", "Tire", "Handlebar", "Seat", "Pedal", "Gear", "Cable", "Tube", "Light"]
        types = [Type.BRAKE, Type.CHAIN, Type.TIRE, Type.OTHER, Type.OTHER, Type.PEDAL, Type.SHIFT, Type.CHAIN, Type.TIRE, Type.OTHER]
        
        for i in range(10):
            detail = Detail(
                brand=f"Brand_{i+1}",
                type=types[i],
                name=detail_names[i],
                price=50 + i * 25,
                in_stock=True,
                created=now,
                updated=now
            )
            session.add(detail)
        
        session.commit()
        
        all_details = session.query(Detail).all()
        assert len(all_details) >= 10
    
    def test_select_all_records(self, session):
        all_details = session.query(Detail).all()
        
        assert len(all_details) > 0
        print(f"Найдено записей: {len(all_details)}")
        
        for detail in all_details:
            assert detail.id is not None
            assert detail.name is not None
    
    def test_update_4_records(self, session):
        details_to_update = session.query(Detail).limit(4).all()
        assert len(details_to_update) >= 4
        
        detail_ids = []
        
        for i, detail in enumerate(details_to_update[:4]):
            detail.name = f"Updated_Detail_{i+1}"
            detail.price = 1000 + i * 100
            detail.in_stock = False
            detail_ids.append(detail.id)
        
        session.commit()
        
        updated_count = session.query(Detail).filter(Detail.name.like("Updated_%")).count()
        assert updated_count >= 4
        
        print(f"Обновлено записей: {updated_count}")
    
    def test_delete_2_records(self, session):
        details_to_delete = session.query(Detail).limit(2).all()
        assert len(details_to_delete) >= 2
        
        detail_ids = [detail.id for detail in details_to_delete[:2]]
        
        deleted_count = session.query(Detail).filter(Detail.id.in_(detail_ids)).delete()
        session.commit()
        
        assert deleted_count == 2
        
        for detail_id in detail_ids:
            deleted_detail = session.query(Detail).filter_by(id=detail_id).first()
            assert deleted_detail is None
        
        print(f"Удалено записей: {deleted_count}")