
CREATE TABLE KhachHang (
    IdKhachHang INT PRIMARY KEY,
    HoTen VARCHAR(100),
    SoDienThoai VARCHAR(20)
);

CREATE TABLE HoaDon (
    MaDon INT PRIMARY KEY,
    Ngay DATE,
    TongTien DECIMAL(15,2),
    IdKhachHang INT,
    FOREIGN KEY (IdKhachHang) REFERENCES KhachHang(IdKhachHang)
);

CREATE TABLE NhanVien (
    IdNhanVien INT PRIMARY KEY,
    Ten VARCHAR(100),
    ChucVu VARCHAR(50),
    NgayThangNamSinh DATE,
    DiaChi VARCHAR(255),
    Luong DECIMAL(15,2),
    Tuoi INT
);

CREATE TABLE SanPham (
    MaSanPham INT PRIMARY KEY,
    TenSanPham VARCHAR(100),
    DonViTinh VARCHAR(50),
    SoLuong INT,
    NgaySanXuat DATE,
    HanSuDung DATE,
    GiaTien DECIMAL(15,2)
);

CREATE TABLE ChiTietHoaDon (
    MaDon INT,
    MaSanPham INT,
    SoLuong INT,
    DonGia DECIMAL(15,2),
    PRIMARY KEY (MaDon, MaSanPham),
    FOREIGN KEY (MaDon) REFERENCES HoaDon(MaDon),
    FOREIGN KEY (MaSanPham) REFERENCES SanPham(MaSanPham)
);

CREATE TABLE NhaCungCap (
    IdNhaCungCap INT PRIMARY KEY,
    TenCongTy VARCHAR(100),
    SoDienThoai VARCHAR(20),
    Email VARCHAR(100)
);

CREATE TABLE DonNhapHang (
    MaDon INT PRIMARY KEY,
    Ngay DATE,
    TongTien DECIMAL(15,2),
    IdNhaCungCap INT,
    FOREIGN KEY (IdNhaCungCap) REFERENCES NhaCungCap(IdNhaCungCap)
);

CREATE TABLE ChiTietNhapHang (
    MaDon INT,
    MaSanPham INT,
    SoLuong INT,
    DonGia DECIMAL(15,2),
    PRIMARY KEY (MaDon, MaSanPham),
    FOREIGN KEY (MaDon) REFERENCES DonNhapHang(MaDon),
    FOREIGN KEY (MaSanPham) REFERENCES SanPham(MaSanPham)
);
