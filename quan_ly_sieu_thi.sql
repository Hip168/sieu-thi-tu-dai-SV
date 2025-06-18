CREATE TABLE KhachHang (
    IdKhachHang INT PRIMARY KEY check (IdKhachHang > 0),
    HoTen VARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE NhanVien (
    ID_NhanVien INT PRIMARY KEY check (ID_NhanVien > 0),
    HoTen NVARCHAR(100) NOT NULL,
    ChucVu NVARCHAR(50) NOT NULL,
    NgaySinh DATE NOT NULL,
    DiaChi NVARCHAR(255) NOT NULL,
    Luong DECIMAL(15,2) NOT NULL check (Luong >= 0)
);

CREATE TABLE NhaCungCap (
    IdNhaCungCap INT PRIMARY KEY check (IdNhaCungCap > 0),
    TenCongTy VARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(10) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE HoaDon (
    MaDon INT PRIMARY KEY check (MaDon > 0),
    Ngay DATE NOT NULL,
    TongTien DECIMAL(15,2) check (TongTien >= 0),
    IdKhachHang INT ,
    IdNhanVien INT ,
    CONSTRAINT fk_hoadon_khachhang FOREIGN KEY (IdKhachHang)
        REFERENCES KhachHang(IdKhachHang) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_hoadon_nhanvien FOREIGN KEY (IdNhanVien)
        REFERENCES NhanVien(ID_NhanVien) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE DonNhapHang (
    MaDon INT PRIMARY KEY check (MaDon > 0),
    Ngay DATE NOT NULL,
    TongTien DECIMAL(15,2) check (TongTien >= 0),
    IdNhanVien INT ,
    IdNhaCungCap INT ,
    CONSTRAINT fk_donnhaphang_nhanvien FOREIGN KEY (IdNhanVien)
        REFERENCES NhanVien(ID_NhanVien) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_donnhaphang_nhacungcap FOREIGN KEY (IdNhaCungCap)
        REFERENCES NhaCungCap(IdNhaCungCap) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE SanPham (
    MaSanPham INT PRIMARY KEY check (MaSanPham > 0),
    TenSanPham VARCHAR(100) NOT NULL,
    DonViTinh VARCHAR(50) NOT NULL,
    SoLuong INT NOT NULL CHECK (SoLuong >= 0),
    GiaTienBan DECIMAL(15,2) NOT NULL CHECK (GiaTienBan >= 0),
    GiaTienNhap DECIMAL(15,2) NOT NULL CHECK (GiaTienNhap >= 0)
);

CREATE TABLE ChiTietHoaDon (
    MaDon INT,
    MaSanPham INT,
    SoLuong INT CHECK (SoLuong >= 0),
    DonGia DECIMAL(15,2) CHECK (DonGia >= 0),
    PRIMARY KEY (MaDon, MaSanPham),
    CONSTRAINT fk_chitiethoadon_hoadon FOREIGN KEY (MaDon)
        REFERENCES HoaDon(MaDon) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_chitiethoadon_sanpham FOREIGN KEY (MaSanPham)
        REFERENCES SanPham(MaSanPham) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE ChiTietNhapHang (
    MaDon INT,
    MaSanPham INT,
    SoLuong INT CHECK (SoLuong >= 0),
    DonGia DECIMAL(15,2) CHECK (DonGia >= 0),
    PRIMARY KEY (MaDon, MaSanPham),
    CONSTRAINT fk_chitietnhaphang_donnhaphang FOREIGN KEY (MaDon)
        REFERENCES DonNhapHang(MaDon) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_chitietnhaphang_sanpham FOREIGN KEY (MaSanPham)
        REFERENCES SanPham(MaSanPham) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Nâng cấp bảng SanPham cho database đang chạy
ALTER TABLE SanPham
    DROP COLUMN NgaySanXuat,
    DROP COLUMN HanSuDung;

ALTER TABLE SanPham
    CHANGE GiaTien GiaTienBan DECIMAL(15,2) NOT NULL DEFAULT 0;

ALTER TABLE SanPham
    ADD COLUMN GiaTienNhap DECIMAL(15,2) NOT NULL DEFAULT 0;

UPDATE SanPham SET GiaTienNhap = GiaTienBan;