# Tài Liệu Hướng Dẫn API

## Các Endpoint

### 1. Quản Lý Khách Hàng

#### Lấy Danh Sách Khách Hàng
- **URL**: `/api/khachhang`
- **Method**: `GET`
- **Response**: Danh sách khách hàng

#### Thêm Khách Hàng Mới
- **URL**: `/api/khachhang`
- **Method**: `POST`
- **Body**:
```json
{
    "IdKhachHang": 1,
    "HoTen": "Nguyễn Văn A",
    "SoDienThoai": "0123456789"
}
```

#### Cập Nhật Khách Hàng
- **URL**: `/api/khachhang/{id}`
- **Method**: `PUT`
- **Body**: Tương tự như thêm mới

#### Xóa Khách Hàng
- **URL**: `/api/khachhang/{id}`
- **Method**: `DELETE`

### 2. Quản Lý Hóa Đơn

#### Lấy Danh Sách Hóa Đơn
- **URL**: `/api/hoadon`
- **Method**: `GET`

#### Thêm Hóa Đơn Mới
- **URL**: `/api/hoadon`
- **Method**: `POST`
- **Body**:
```json
{
    "MaDon": 1,
    "Ngay": "2024-03-20",
    "TongTien": 1000000,
    "IdKhachHang": 1
}
```

#### Cập Nhật Hóa Đơn
- **URL**: `/api/hoadon/{id}`
- **Method**: `PUT`
- **Body**: Tương tự như thêm mới

#### Xóa Hóa Đơn
- **URL**: `/api/hoadon/{id}`
- **Method**: `DELETE`

### 3. Quản Lý Nhân Viên

#### Lấy Danh Sách Nhân Viên
- **URL**: `/api/nhanvien`
- **Method**: `GET`

#### Thêm Nhân Viên Mới
- **URL**: `/api/nhanvien`
- **Method**: `POST`
- **Body**:
```json
{
    "IdNhanVien": 1,
    "Ten": "Nguyễn Văn B",
    "ChucVu": "Nhân viên bán hàng",
    "NgayThangNamSinh": "1990-01-01",
    "DiaChi": "Hà Nội",
    "Luong": 5000000,
    "Tuoi": 34
}
```

#### Cập Nhật Nhân Viên
- **URL**: `/api/nhanvien/{id}`
- **Method**: `PUT`
- **Body**: Tương tự như thêm mới

#### Xóa Nhân Viên
- **URL**: `/api/nhanvien/{id}`
- **Method**: `DELETE`

### 4. Quản Lý Sản Phẩm

#### Lấy Danh Sách Sản Phẩm
- **URL**: `/api/sanpham`
- **Method**: `GET`

#### Thêm Sản Phẩm Mới
- **URL**: `/api/sanpham`
- **Method**: `POST`
- **Body**:
```json
{
    "MaSanPham": 1,
    "TenSanPham": "Sản phẩm A",
    "DonViTinh": "Cái",
    "SoLuong": 100,
    "NgaySanXuat": "2024-01-01",
    "HanSuDung": "2024-12-31",
    "GiaTien": 100000
}
```

#### Cập Nhật Sản Phẩm
- **URL**: `/api/sanpham/{id}`
- **Method**: `PUT`
- **Body**: Tương tự như thêm mới

#### Xóa Sản Phẩm
- **URL**: `/api/sanpham/{id}`
- **Method**: `DELETE`

### 5. Quản Lý Chi Tiết Hóa Đơn

#### Lấy Danh Sách Chi Tiết Hóa Đơn
- **URL**: `/api/chitiethoadon`
- **Method**: `GET`

#### Thêm Chi Tiết Hóa Đơn Mới
- **URL**: `/api/chitiethoadon`
- **Method**: `POST`
- **Body**:
```json
{
    "MaDon": 1,
    "MaSanPham": 1,
    "SoLuong": 2,
    "DonGia": 100000
}
```

#### Cập Nhật Chi Tiết Hóa Đơn
- **URL**: `/api/chitiethoadon/{madon}/{masanpham}`
- **Method**: `PUT`
- **Body**:
```json
{
    "SoLuong": 3,
    "DonGia": 100000
}
```

#### Xóa Chi Tiết Hóa Đơn
- **URL**: `/api/chitiethoadon/{madon}/{masanpham}`
- **Method**: `DELETE`

### 6. Quản Lý Nhà Cung Cấp

#### Lấy Danh Sách Nhà Cung Cấp
- **URL**: `/api/nhacungcap`
- **Method**: `GET`

#### Thêm Nhà Cung Cấp Mới
- **URL**: `/api/nhacungcap`
- **Method**: `POST`
- **Body**:
```json
{
    "IdNhaCungCap": 1,
    "TenCongTy": "Công ty A",
    "SoDienThoai": "0123456789",
    "Email": "contact@company.com"
}
```

#### Cập Nhật Nhà Cung Cấp
- **URL**: `/api/nhacungcap/{id}`
- **Method**: `PUT`
- **Body**: Tương tự như thêm mới

#### Xóa Nhà Cung Cấp
- **URL**: `/api/nhacungcap/{id}`
- **Method**: `DELETE`

### 7. Quản Lý Đơn Nhập Hàng

#### Lấy Danh Sách Đơn Nhập Hàng
- **URL**: `/api/donnhaphang`
- **Method**: `GET`

#### Thêm Đơn Nhập Hàng Mới
- **URL**: `/api/donnhaphang`
- **Method**: `POST`
- **Body**:
```json
{
    "MaDon": 1,
    "Ngay": "2024-03-20",
    "TongTien": 1000000,
    "IdNhaCungCap": 1
}
```

#### Cập Nhật Đơn Nhập Hàng
- **URL**: `/api/donnhaphang/{id}`
- **Method**: `PUT`
- **Body**: Tương tự như thêm mới

#### Xóa Đơn Nhập Hàng
- **URL**: `/api/donnhaphang/{id}`
- **Method**: `DELETE`

### 8. Quản Lý Chi Tiết Nhập Hàng

#### Lấy Danh Sách Chi Tiết Nhập Hàng
- **URL**: `/api/chitietnhaphang`
- **Method**: `GET`

#### Thêm Chi Tiết Nhập Hàng Mới
- **URL**: `/api/chitietnhaphang`
- **Method**: `POST`
- **Body**:
```json
{
    "MaDon": 1,
    "MaSanPham": 1,
    "SoLuong": 10,
    "DonGia": 100000
}
```

#### Cập Nhật Chi Tiết Nhập Hàng
- **URL**: `/api/chitietnhaphang/{madon}/{masanpham}`
- **Method**: `PUT`
- **Body**:
```json
{
    "SoLuong": 15,
    "DonGia": 100000
}
```

#### Xóa Chi Tiết Nhập Hàng
- **URL**: `/api/chitietnhaphang/{madon}/{masanpham}`
- **Method**: `DELETE`

## Mã Lỗi và Xử Lý

### Mã Lỗi Chung
- `400`: Dữ liệu không hợp lệ
- `500`: Lỗi server

### Thông Báo Lỗi
Khi có lỗi xảy ra, API sẽ trả về response với format:
```json
{
    "error": "Mô tả lỗi"
}
```

## Lưu ý
1. Tất cả các ngày tháng phải được định dạng theo chuẩn `YYYY-MM-DD`
2. Các trường số phải là số nguyên hoặc số thực
3. Các trường chuỗi không được vượt quá độ dài cho phép
4. Khi thêm mới hoặc cập nhật, tất cả các trường bắt buộc phải được cung cấp
5. ID phải là số nguyên dương 