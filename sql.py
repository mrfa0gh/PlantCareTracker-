import sqlite3, pytz, time, random
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('plants.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # تأكد من إضافة عمود vegetation_index إذا لم يكن موجودًا
    cursor.execute('''CREATE TABLE IF NOT EXISTS plant_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        plant TEXT,
                        uv REAL,
                        moisture REAL,
                        vegetation_index REAL,
                        time TEXT)''')
    
    # تأكد من أن العمود vegetation_index موجود. إذا لم يكن موجودًا، إضافته.
    try:
        cursor.execute("ALTER TABLE plant_data ADD COLUMN vegetation_index REAL")
    except sqlite3.OperationalError:
        pass  # العمود موجود بالفعل، لا حاجة لفعل شيء هنا

    conn.commit()
    conn.close()

def insert_fake_data():
    plants = ['Mint', 'Basil', 'Rose', 'Tomato', 'Cactus']
    
    utc_now = datetime.now(pytz.utc)
    time_str = utc_now.strftime('%Y-%m-%d %H:%M:%S')
    plant = random.choice(plants)
    uv = round(random.uniform(3.0, 6.0), 1)
    moisture = random.randint(50, 90)

    # حساب قيمة vegetation_index بشكل وهمي
    vegetation_index = round((uv * moisture) / 100, 2)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO plant_data (plant, uv, moisture, vegetation_index, time) VALUES (?, ?, ?, ?, ?) ",
                   (plant, uv, moisture, vegetation_index, time_str))
    conn.commit()
    conn.close()
    print(f"Data inserted: {plant}, {uv}, {moisture}, {vegetation_index}, {time_str}")

create_table()

# every 5 sec add random data
for _ in range(10):  # إدخال 10 بيانات وهمية كمثال
    insert_fake_data()
    time.sleep(5)  # تأخير 5 ثواني قبل إدخال البيانات التالية
