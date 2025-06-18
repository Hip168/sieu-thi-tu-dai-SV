import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

# MySQL Connection Settings
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
TIMEOUT = 10

def get_db_connection():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            conn = pymysql.connect(
                charset="utf8mb4",
                connect_timeout=TIMEOUT,
                cursorclass=pymysql.cursors.DictCursor,
                db=os.getenv('DB_NAME'),
                host=os.getenv('DB_HOST'),
                password=os.getenv('DB_PASSWORD'),
                read_timeout=TIMEOUT,
                port=int(os.getenv('DB_PORT')),
                user=os.getenv('DB_USER'),
                write_timeout=TIMEOUT,
            )
            print("Connected to MySQL successfully")
            return conn
        except pymysql.Error as e:
            retries += 1
            print(f"Failed to connect to MySQL (attempt {retries}/{MAX_RETRIES}): {str(e)}")
            if retries < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                raise Exception("Failed to connect to MySQL after multiple attempts")

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
CORS(app)  # Enable CORS for all routes

# Database connection
try:
    conn = get_db_connection()
except Exception as e:
    print(f"Critical error: {str(e)}")
    raise

# Add a health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test database connection
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

# Add error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Validation Functions
def validate_khachhang(data):
    if not all(key in data for key in ['IdKhachHang', 'HoTen', 'SoDienThoai']):
        return False, "Thiếu Dữ Liệu"
    if not isinstance(data['IdKhachHang'], int):
        return False, "IdKhachHang phải là số nguyên"
    if not isinstance(data['HoTen'], str) or len(data['HoTen']) > 100:
        return False, "HoTen không hợp lệ"
    if not isinstance(data['SoDienThoai'], str) or len(data['SoDienThoai']) > 10 or not data['SoDienThoai'].isdigit():
        return False, "SoDienThoai không hợp lệ"
    return True, "Dữ Liệu hợp lệ"

def validate_hoadon(data):
    if not all(key in data for key in ['MaDon', 'Ngay', 'TongTien', 'IdKhachHang', 'IdNhanVien']):
        return False, "Thiếu Dữ Liệu"
    if not isinstance(data['MaDon'], int):
        return False, "MaDon phải là số nguyên"
    try:
        datetime.strptime(data['Ngay'], '%Y-%m-%d')
    except:
        return False, "Ngày không hợp lệ"
    if not isinstance(data['TongTien'], (int, float)) or data['TongTien'] < 0:
        return False, "TongTien không hợp lệ"
    if not isinstance(data['IdKhachHang'], int):
        return False, "IdKhachHang phải là số nguyên"
    if not isinstance(data['IdNhanVien'], int):
        return False, "IdNhanVien phải là số nguyên"
    return True, "Dữ Liệu hợp lệ"

def validate_nhanvien(data):
    if not all(key in data for key in ['ID_NhanVien', 'HoTen', 'ChucVu', 'NgaySinh', 'DiaChi', 'Luong']):
        return False, "Thiếu Dữ Liệu"
    if not isinstance(data['ID_NhanVien'], int):
        return False, "ID_NhanVien phải là số nguyên"
    if not isinstance(data['HoTen'], str) or len(data['HoTen']) > 100:
        return False, "HoTen không hợp lệ"
    if not isinstance(data['ChucVu'], str) or len(data['ChucVu']) > 50:
        return False, "ChucVu không hợp lệ"
    try:
        datetime.strptime(data['NgaySinh'], '%Y-%m-%d')
    except:
        return False, "Ngày không hợp lệ"
    if not isinstance(data['DiaChi'], str) or len(data['DiaChi']) > 200:
        return False, "DiaChi không hợp lệ"
    if not isinstance(data['Luong'], (int, float)) or data['Luong'] < 0:
        return False, "Luong không hợp lệ"
    return True, "Dữ Liệu hợp lệ"

def validate_sanpham(data):
    # Kiểm tra đủ trường
    required_fields = ['MaSanPham', 'TenSanPham', 'DonViTinh', 'SoLuong', 'GiaTienBan', 'GiaTienNhap']
    for key in required_fields:
        if key not in data or data[key] is None:
            return False, f"Thiếu hoặc null trường {key}"
    # Kiểm tra kiểu và độ dài
    if not isinstance(data['MaSanPham'], int):
        return False, "MaSanPham phải là số nguyên"
    if not isinstance(data['TenSanPham'], str) or not data['TenSanPham'] or len(data['TenSanPham']) > 100:
        return False, "TenSanPham không hợp lệ (bắt buộc, tối đa 100 ký tự)"
    if not isinstance(data['DonViTinh'], str) or not data['DonViTinh'] or len(data['DonViTinh']) > 50:
        return False, "DonViTinh không hợp lệ (bắt buộc, tối đa 50 ký tự)"
    if not isinstance(data['SoLuong'], int) or data['SoLuong'] < 0:
        return False, "SoLuong không hợp lệ (bắt buộc, >=0)"
    if not isinstance(data['GiaTienBan'], (int, float)) or data['GiaTienBan'] < 0:
        return False, "GiaTienBan không hợp lệ (bắt buộc, >=0)"
    if not isinstance(data['GiaTienNhap'], (int, float)) or data['GiaTienNhap'] < 0:
        return False, "GiaTienNhap không hợp lệ (bắt buộc, >=0)"
    return True, "Dữ Liệu hợp lệ"

def validate_chitiethoadon(data):
    if not all(key in data for key in ['MaDon', 'MaSanPham', 'SoLuong', 'DonGia']):
        return False, "Thiếu trường bắt buộc"
    if not isinstance(data['MaDon'], int):
        return False, "MaDon phải là số nguyên"
    if not isinstance(data['MaSanPham'], int):
        return False, "MaSanPham phải là số nguyên"
    if not isinstance(data['SoLuong'], int) or data['SoLuong'] < 0:
        return False, "SoLuong không hợp lệ"
    if not isinstance(data['DonGia'], (int, float)) or data['DonGia'] < 0:
        return False, "DonGia không hợp lệ"
    return True, "Dữ Liệu hợp lệ"

def validate_nhacungcap(data):
    if not all(key in data for key in ['IdNhaCungCap', 'TenCongTy', 'SoDienThoai', 'Email']):
        return False, "Missing required fields"
    if not isinstance(data['IdNhaCungCap'], int):
        return False, "IdNhaCungCap phải là số nguyên"
    if not isinstance(data['TenCongTy'], str) or len(data['TenCongTy']) > 100:
        return False, "TenCongTy không hợp lệ"
    if not isinstance(data['SoDienThoai'], str) or len(data['SoDienThoai']) > 20:
        return False, "SoDienThoai không hợp lệ"
    if not isinstance(data['Email'], str) or len(data['Email']) > 100 or '@' not in data['Email']:
        return False, "Email không hợp lệ"
    return True, "Dữ Liệu hợp lệ"

def validate_donnhaphang(data):
    if not all(key in data for key in ['MaDon', 'Ngay', 'TongTien', 'IdNhaCungCap', 'IdNhanVien']):
        return False, "Missing required fields"
    if not isinstance(data['MaDon'], int):
        return False, "MaDon phải là số nguyên"
    try:
        datetime.strptime(data['Ngay'], '%Y-%m-%d')
    except:
        return False, "Sai Định Dạng Ngày (YYYY-MM-DD)"
    if not isinstance(data['TongTien'], (int, float)) or data['TongTien'] < 0:
        return False, "TongTien không hợp lệ"
    if not isinstance(data['IdNhaCungCap'], int):
        return False, "IdNhaCungCap phải là số nguyên"
    if not isinstance(data['IdNhanVien'], int):
        return False, "IdNhanVien phải là số nguyên"
    return True, "Dữ Liệu hợp lệ"

def validate_chitietnhaphang(data):
    if not all(key in data for key in ['MaDon', 'MaSanPham', 'SoLuong', 'DonGia']):
        return False, "Missing required fields"
    if not isinstance(data['MaDon'], int):
        return False, "MaDon phải là số nguyên"
    if not isinstance(data['MaSanPham'], int):
        return False, "MaSanPham phải là số nguyên"
    if not isinstance(data['SoLuong'], int) or data['SoLuong'] < 0:
        return False, "SoLuong không hợp lệ"
    if not isinstance(data['DonGia'], (int, float)) or data['DonGia'] < 0:
        return False, "DonGia không hợp lệ"
    return True, "Dữ Liệu hợp lệ"

def validate_ma_sanpham(ma):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM SanPham WHERE MaSanPham = %s", (ma,))
    count = cursor.fetchone()[0]
    return count > 0

def validate_ma_donnhaphang(ma):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM DonNhapHang WHERE MaDon = %s", (ma,))
    count = cursor.fetchone()[0]
    return count > 0

def validate_ma_hoadon(ma):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM HoaDon WHERE MaDon = %s", (ma,))
    count = cursor.fetchone()[0]
    return count > 0

# KhachHang CRUD
@app.route('/api/khachhang', methods=['GET'])
def get_khachhang():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM KhachHang")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/khachhang', methods=['POST'])
def create_khachhang():
    data = request.json
    is_valid, message = validate_khachhang(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO KhachHang (IdKhachHang, HoTen, SoDienThoai) VALUES (%s, %s, %s)",
                      (data['IdKhachHang'], data['HoTen'], data['SoDienThoai']))
        conn.commit()
        return jsonify({"message": "KhachHang created successfully"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/khachhang/<int:id>', methods=['PUT'])
def update_khachhang(id):
    data = request.json
    is_valid, message = validate_khachhang(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE KhachHang SET HoTen = %s, SoDienThoai = %s WHERE IdKhachHang = %s",
                      (data['HoTen'], data['SoDienThoai'], id))
        conn.commit()
        return jsonify({"message": "Cập Nhật KhachHang Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/khachhang/<int:id>', methods=['DELETE'])
def delete_khachhang(id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM KhachHang WHERE IdKhachHang = %s", (id,))
        conn.commit()
        return jsonify({"message": "Xóa KhachHang Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

# HoaDon CRUD
@app.route('/api/hoadon', methods=['GET'])
def get_hoadon():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM HoaDon")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/hoadon', methods=['POST'])
def create_hoadon():
    data = request.json
    is_valid, message = validate_hoadon(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO HoaDon (MaDon, Ngay, TongTien, IdKhachHang, IdNhanVien) VALUES (%s, %s, %s, %s, %s)",
                      (data['MaDon'], data['Ngay'], data['TongTien'], data['IdKhachHang'], data['IdNhanVien']))
        conn.commit()
        return jsonify({"message": "Tạo HoaDon Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/hoadon/<int:id>', methods=['PUT'])
def update_hoadon(id):
    data = request.json
    is_valid, message = validate_hoadon(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE HoaDon SET Ngay = %s, TongTien = %s, IdKhachHang = %s, IdNhanVien = %s WHERE MaDon = %s",
                      (data['Ngay'], data['TongTien'], data['IdKhachHang'], data['IdNhanVien'], id))
        conn.commit()
        return jsonify({"message": "Cập Nhật HoaDon Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/hoadon/<int:id>', methods=['DELETE'])
def delete_hoadon(id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM HoaDon WHERE MaDon = %s", (id,))
        conn.commit()
        return jsonify({"message": "Xóa HoaDon Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

# NhanVien CRUD
@app.route('/api/nhanvien', methods=['GET'])
def get_nhanvien():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM NhanVien")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/nhanvien', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['ID_NhanVien', 'HoTen', 'ChucVu', 'NgaySinh', 'DiaChi', 'Luong']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Thiếu thông tin bắt buộc'}), 400
            
        # Validate data types
        if not isinstance(data['Luong'], (int, float)) or data['Luong'] < 0:
            return jsonify({'error': 'Lương không hợp lệ'}), 400
            
        # Insert into database
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO NhanVien (ID_NhanVien, HoTen, ChucVu, NgaySinh, DiaChi, Luong) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['ID_NhanVien'],
            data['HoTen'],
            data['ChucVu'],
            data['NgaySinh'],
            data['DiaChi'],
            data['Luong']
        ))
        conn.commit()
        cursor.close()
        
        return jsonify({'message': 'Thêm nhân viên thành công'}), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/nhanvien/<id>', methods=['PUT'])
def update_employee(id):
    try:
        data = request.get_validated_json()
        
        # Validate required fields
        required_fields = ['HoTen', 'ChucVu', 'NgaySinh', 'DiaChi', 'Luong']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Thiếu thông tin bắt buộc'}), 400
            
        # Validate data types
        if not isinstance(data['Luong'], (int, float)) or data['Luong'] < 0:
            return jsonify({'error': 'Lương không hợp lệ'}), 400
            
        # Update in database
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE NhanVien 
            SET HoTen = %s, ChucVu = %s, NgaySinh = %s, DiaChi = %s, Luong = %s 
            WHERE ID_NhanVien = %s
        """, (
            data['HoTen'],
            data['ChucVu'],
            data['NgaySinh'],
            data['DiaChi'],
            data['Luong'],
            id
        ))
        conn.commit()
        cursor.close()
        
        return jsonify({'message': 'Cập nhật nhân viên thành công'}), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/nhanvien/<id>', methods=['DELETE'])
def delete_nhanvien(id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM NhanVien WHERE ID_NhanVien = %s", (id,))
        conn.commit()
        return jsonify({"message": "Xóa NhanVien Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

# SanPham CRUD
@app.route('/api/sanpham', methods=['GET'])
def get_sanpham():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM SanPham")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/sanpham', methods=['POST'])
def create_sanpham():
    data = request.json
    is_valid, message = validate_sanpham(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO SanPham (MaSanPham, TenSanPham, DonViTinh, SoLuong, GiaTienBan, GiaTienNhap) VALUES (%s, %s, %s, %s, %s, %s)",
                      (data['MaSanPham'], data['TenSanPham'], data['DonViTinh'], data['SoLuong'], data['GiaTienBan'], data['GiaTienNhap']))
        conn.commit()
        return jsonify({"message": "Tạo SanPham Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/sanpham/<int:id>', methods=['PUT'])
def update_sanpham(id):
    data = request.json
    is_valid, message = validate_sanpham(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE SanPham SET TenSanPham = %s, DonViTinh = %s, SoLuong = %s, GiaTienBan = %s, GiaTienNhap = %s WHERE MaSanPham = %s",
                      (data['TenSanPham'], data['DonViTinh'], data['SoLuong'], data['GiaTienBan'], data['GiaTienNhap'], id))
        conn.commit()
        return jsonify({"message": "Cập Nhật SanPham Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/sanpham/<int:id>', methods=['DELETE'])
def delete_sanpham(id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM SanPham WHERE MaSanPham = %s", (id,))
        conn.commit()
        return jsonify({"message": "Xóa SanPham Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/sanpham/<int:id>', methods=['GET'])
def get_sanpham_by_id(id):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM SanPham WHERE MaSanPham = %s", (id,))
    data = cursor.fetchone()
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Không tìm thấy sản phẩm"}), 404

# ChiTietHoaDon CRUD
@app.route('/api/chitiethoadon', methods=['GET'])
def get_chitiethoadon():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM ChiTietHoaDon")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/chitiethoadon', methods=['POST'])
def create_chitiethoadon():
    data = request.json
    is_valid, message = validate_chitiethoadon(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO ChiTietHoaDon (MaDon, MaSanPham, SoLuong, DonGia) VALUES (%s, %s, %s, %s)",
                      (data['MaDon'], data['MaSanPham'], data['SoLuong'], data['DonGia']))
        conn.commit()
        return jsonify({"message": "Tạo ChiTietHoaDon Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/chitiethoadon/<int:madon>/<int:masanpham>', methods=['PUT'])
def update_chitiethoadon(madon, masanpham):
    data = request.json
    if not all(key in data for key in ['SoLuong', 'DonGia']):
        return jsonify({"error": "Thiếu trường bắt buộc"}), 400
    
    if not isinstance(data['SoLuong'], int) or data['SoLuong'] < 0:
        return jsonify({"error": "SoLuong không hợp lệ"}), 400
    if not isinstance(data['DonGia'], (int, float)) or data['DonGia'] < 0:
        return jsonify({"error": "DonGia không hợp lệ"}), 400

    if not validate_ma_hoadon(madon):
        return jsonify({"error": "Mã đơn hàng không tồn tại"}), 400
    if not validate_ma_sanpham(masanpham):
        return jsonify({"error": "Mã sản phẩm không tồn tại"}), 400

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE ChiTietHoaDon SET SoLuong = %s, DonGia = %s WHERE MaDon = %s AND MaSanPham = %s",
                      (data['SoLuong'], data['DonGia'], madon, masanpham))
        conn.commit()
        return jsonify({"message": "Cập Nhật ChiTietHoaDon Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/chitiethoadon/<int:madon>/<int:masanpham>', methods=['DELETE'])
def delete_chitiethoadon(madon, masanpham):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ChiTietHoaDon WHERE MaDon = %s AND MaSanPham = %s", (madon, masanpham))
        conn.commit()
        return jsonify({"message": "Xóa ChiTietHoaDon Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

# NhaCungCap CRUD
@app.route('/api/nhacungcap', methods=['GET'])
def get_nhacungcap():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM NhaCungCap")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/nhacungcap', methods=['POST'])
def create_nhacungcap():
    data = request.json
    is_valid, message = validate_nhacungcap(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO NhaCungCap (IdNhaCungCap, TenCongTy, SoDienThoai, Email) VALUES (%s, %s, %s, %s)",
                      (data['IdNhaCungCap'], data['TenCongTy'], data['SoDienThoai'], data['Email']))
        conn.commit()
        return jsonify({"message": "Tạo NhaCungCap Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/nhacungcap/<int:id>', methods=['PUT'])
def update_nhacungcap(id):
    data = request.json
    is_valid, message = validate_nhacungcap(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE NhaCungCap SET TenCongTy = %s, SoDienThoai = %s, Email = %s WHERE IdNhaCungCap = %s",
                      (data['TenCongTy'], data['SoDienThoai'], data['Email'], id))
        conn.commit()
        return jsonify({"message": "Cập Nhật NhaCungCap Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/nhacungcap/<int:id>', methods=['DELETE'])
def delete_nhacungcap(id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM NhaCungCap WHERE IdNhaCungCap = %s", (id,))
        conn.commit()
        return jsonify({"message": "Xóa NhaCungCap Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

# DonNhapHang CRUD
@app.route('/api/donnhaphang', methods=['GET'])
def get_donnhaphang():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM DonNhapHang")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/donnhaphang', methods=['POST'])
def create_donnhaphang():
    data = request.json
    is_valid, message = validate_donnhaphang(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO DonNhapHang (MaDon, Ngay, TongTien, IdNhaCungCap, IdNhanVien) VALUES (%s, %s, %s, %s, %s)",
                      (data['MaDon'], data['Ngay'], data['TongTien'], data['IdNhaCungCap'], data['IdNhanVien']))
        conn.commit()
        return jsonify({"message": "Tạo DonNhapHang Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/donnhaphang/<int:id>', methods=['PUT'])
def update_donnhaphang(id):
    data = request.json
    is_valid, message = validate_donnhaphang(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE DonNhapHang SET Ngay = %s, TongTien = %s, IdNhaCungCap = %s, IdNhanVien = %s WHERE MaDon = %s",
                      (data['Ngay'], data['TongTien'], data['IdNhaCungCap'], data['IdNhanVien'], id))
        conn.commit()
        return jsonify({"message": "Cập Nhật DonNhapHang Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/donnhaphang/<int:id>', methods=['DELETE'])
def delete_donnhaphang(id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM DonNhapHang WHERE MaDon = %s", (id,))
        conn.commit()
        return jsonify({"message": "Xóa DonNhapHang Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

# ChiTietNhapHang CRUD
@app.route('/api/chitietnhaphang', methods=['GET'])
def get_chitietnhaphang():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM ChiTietNhapHang")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/chitietnhaphang', methods=['POST'])
def create_chitietnhaphang():
    data = request.json
    is_valid, message = validate_chitietnhaphang(data)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO ChiTietNhapHang (MaDon, MaSanPham, SoLuong, DonGia) VALUES (%s, %s, %s, %s)",
                      (data['MaDon'], data['MaSanPham'], data['SoLuong'], data['DonGia']))
        conn.commit()
        return jsonify({"message": "Tạo ChiTietNhapHang Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/chitietnhaphang/<int:madon>/<int:masanpham>', methods=['PUT'])
def update_chitietnhaphang(madon, masanpham):
    data = request.json
    if not all(key in data for key in ['SoLuong', 'DonGia']):
        return jsonify({"error": "Thiếu trường bắt buộc"}), 400
    
    if not isinstance(data['SoLuong'], int) or data['SoLuong'] < 0:
        return jsonify({"error": "SoLuong không hợp lệ"}), 400
    if not isinstance(data['DonGia'], (int, float)) or data['DonGia'] < 0:
        return jsonify({"error": "DonGia không hợp lệ"}), 400

    if not validate_ma_donnhaphang(madon):
        return jsonify({"error": "Mã đơn hàng không tồn tại"}), 400
    if not validate_ma_sanpham(masanpham):
        return jsonify({"error": "Mã sản phẩm không tồn tại"}), 400

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE ChiTietNhapHang SET SoLuong = %s, DonGia = %s WHERE MaDon = %s AND MaSanPham = %s",
                      (data['SoLuong'], data['DonGia'], madon, masanpham))
        conn.commit()
        return jsonify({"message": "Cập Nhật ChiTietNhapHang Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/chitietnhaphang/<int:madon>/<int:masanpham>', methods=['DELETE'])
def delete_chitietnhaphang(madon, masanpham):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ChiTietNhapHang WHERE MaDon = %s AND MaSanPham = %s", (madon, masanpham))
        conn.commit()
        return jsonify({"message": "Xóa ChiTietNhapHang Thành Công"})
    except pymysql.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({"error": "Missing date parameters"}), 400

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # tổng doanh thu
        cursor.execute("""
            SELECT COALESCE(SUM(TongTien), 0) as total_revenue 
            FROM HoaDon 
            WHERE Ngay BETWEEN %s AND %s
        """, (start_date, end_date))
        total_revenue = cursor.fetchone()['total_revenue']

        # tổng chi phí nhập hàng
        cursor.execute("""
            SELECT COALESCE(SUM(TongTien), 0) as total_import_cost 
            FROM DonNhapHang 
            WHERE Ngay BETWEEN %s AND %s
        """, (start_date, end_date))
        total_import_cost = cursor.fetchone()['total_import_cost']

        # tổng số hóa đơn
        cursor.execute("""
            SELECT COUNT(*) as total_orders 
            FROM HoaDon 
            WHERE Ngay BETWEEN %s AND %s
        """, (start_date, end_date))
        total_orders = cursor.fetchone()['total_orders']

        # tổng sản phẩm bán được
        cursor.execute("""
            SELECT 
                sp.MaSanPham,
                sp.TenSanPham,
                sp.DonViTinh,
                SUM(cthd.SoLuong) as SoLuongDaBan,
                SUM(cthd.SoLuong * cthd.DonGia) as DoanhThu,
                sp.GiaTienBan as DonGiaHienTai
            FROM ChiTietHoaDon cthd
            JOIN SanPham sp ON cthd.MaSanPham = sp.MaSanPham
            JOIN HoaDon hd ON cthd.MaDon = hd.MaDon
            WHERE hd.Ngay BETWEEN %s AND %s
            GROUP BY sp.MaSanPham, sp.TenSanPham, sp.DonViTinh, sp.GiaTienBan
            ORDER BY SoLuongDaBan DESC
            LIMIT 10
        """, (start_date, end_date))
        top_products = cursor.fetchall()

        # Tổng khách hàng
        cursor.execute("""
            SELECT COUNT(DISTINCT IdKhachHang) as total_customers
            FROM HoaDon
            WHERE Ngay BETWEEN %s AND %s
        """, (start_date, end_date))
        total_customers = cursor.fetchone()['total_customers']

        # Tổng nhà cung cấp
        cursor.execute("""
            SELECT COUNT(DISTINCT IdNhaCungCap) as total_suppliers
            FROM DonNhapHang
            WHERE Ngay BETWEEN %s AND %s
        """, (start_date, end_date))
        total_suppliers = cursor.fetchone()['total_suppliers']

        return jsonify({
            "total_revenue": float(total_revenue),
            "total_import_cost": float(total_import_cost),
            "total_profit": float(total_revenue - total_import_cost),
            "total_orders": total_orders,
            "total_customers": total_customers,
            "total_suppliers": total_suppliers,
            "top_products": top_products
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
