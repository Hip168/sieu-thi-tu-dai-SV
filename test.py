import pymysql
import os 
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
timeout = 10
conn = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db=os.getenv('DB_NAME'),
  host=os.getenv('DB_HOST'),
  password=os.getenv('DB_PASSWORD'),
  read_timeout=timeout,
  port=int(os.getenv('DB_PORT')),
  user=os.getenv('DB_USER'),
  write_timeout=timeout,
)
if conn : 
    print('thanhcong')
else : 
    print('thatbai')
cursor = conn.cursor()
exe = '''ALTER TABLE `btldbs`.`NhanVien` 
          DROP COLUMN `Tuoi`;'''
cursor.execute(exe) 
print('thanhcong')
cursor.close()
conn.close()