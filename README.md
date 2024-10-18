# Test Question Management System

## Tavsif
Ushbu loyiha test savollari, foydalanuvchilar va ularning natijalarini boshqarish uchun mo'ljallangan. Loyiha SQLAlchemy va PostgreSQL ma'lumotlar bazasidan foydalanadi. Foydalanuvchilar ro'yxatdan o'tishlari, savollar qo'shishlari va o'z natijalarini ko'rishlari mumkin.

## O'rnatish

### Talablar
- Python 3.x
- PostgreSQL
- Psycopg2
- SQLAlchemy

### O'rnatish uchun:
1. **Muvofiq muhitni tayyorlash:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux / MacOS
   venv\Scripts\activate  # Windows
2. Kerakli kutubxonalani o'rnatish
pip install -r requirements.txt pip install sqlalchemy psycopg2

3.python main.py



### Qo'shimcha Tavsiyalar:

- **O'rnatish** bo'limida `requirements.txt` faylini ham yaratish foydali bo'lishi mumkin. Bu faylga loyiha uchun kerakli kutubxonalarni kiritishingiz mumkin. Buni qilish uchun quyidagi buyruqni bajaring:
   ```bash
   pip freeze > requirements.txt
