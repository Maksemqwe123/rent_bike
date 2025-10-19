#!/usr/bin/env python3
"""
Скрипт для запуска всех тестов базы данных.
"""

import subprocess
import sys
import os

def run_tests():
    test_files = [
        "Test/test_bicycle.py",
        "Test/test_client.py", 
        "Test/test_staff.py",
        "Test/test_detail.py",
        "Test/test_detail_for_bicycle.py",
        "Test/test_rent_book.py",
        "Test/test_service_book.py"
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📋 Запуск тестов: {test_file}")
            print("-" * 30)
            
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pytest", 
                    test_file, "-v", "--tb=short"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ {test_file} - ПРОЙДЕН")
                    passed_tests += 1
                else:
                    print(f"❌ {test_file} - ПРОВАЛЕН")
                    print(result.stdout)
                    print(result.stderr)
                    failed_tests += 1
                
                total_tests += 1
                
            except Exception as e:
                print(f"❌ Ошибка при запуске {test_file}: {e}")
                failed_tests += 1
                total_tests += 1
        else:
            print(f"⚠️  Файл {test_file} не найден")
    
    print("\n" + "=" * 50)
    print(f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"   Всего файлов: {total_tests}")
    print(f"   ✅ Пройдено: {passed_tests}")
    print(f"   ❌ Провалено: {failed_tests}")
    
    if failed_tests == 0:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        return 0
    else:
        print("💥 ЕСТЬ ПРОВАЛЕННЫЕ ТЕСТЫ!")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
