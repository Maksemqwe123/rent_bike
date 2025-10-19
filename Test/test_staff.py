import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models.staff import Staff

class TestStaff:
    
    def test_create_10_records(self, session):
        now = datetime.now()
        
        timestamp = int(now.timestamp())
        for i in range(10):
            staff = Staff(
                name=f"Staff_{i+1}",
                country="Russia",
                city="Moscow",
                address=f"Office {i+1}",
                email=f"staff{i+1}_{timestamp}@test.com",
                passport=f"ST{i+timestamp:06d}",
                phone=f"+790501234{i+timestamp:02d}",
                salary=1000.0 + i * 100,
                created=now,
                updated=now
            )
            session.add(staff)
        
        session.commit()
        
        all_staff = session.query(Staff).all()
        assert len(all_staff) >= 10
    
    def test_select_all_records(self, session):
        all_staff = session.query(Staff).all()
        
        assert len(all_staff) > 0
        print(f"Найдено записей: {len(all_staff)}")
        
        for staff in all_staff:
            assert staff.id is not None
            assert staff.name is not None
    
    def test_update_4_records(self, session):
        staff_to_update = session.query(Staff).limit(4).all()
        assert len(staff_to_update) >= 4
        
        staff_ids = []
        
        for i, staff in enumerate(staff_to_update[:4]):
            staff.name = f"Updated_Staff_{i+1}"
            staff.salary = 5000.0 + i * 500
            staff_ids.append(staff.id)
        
        session.commit()
        
        updated_count = session.query(Staff).filter(Staff.name.like("Updated_%")).count()
        assert updated_count >= 4
        
        print(f"Обновлено записей: {updated_count}")
    
    def test_delete_2_records(self, session):
        staff_to_delete = session.query(Staff).limit(2).all()
        assert len(staff_to_delete) >= 2
        
        staff_ids = [staff.id for staff in staff_to_delete[:2]]
        
        deleted_count = session.query(Staff).filter(Staff.id.in_(staff_ids)).delete()
        session.commit()
        
        assert deleted_count == 2
        
        for staff_id in staff_ids:
            deleted_staff = session.query(Staff).filter_by(id=staff_id).first()
            assert deleted_staff is None
        
        print(f"Удалено записей: {deleted_count}")