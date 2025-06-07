-- Trigger for ChiTietHoaDon
DELIMITER //

-- Trigger for HoaDon to calculate total when created
CREATE TRIGGER after_hoadon_insert
AFTER INSERT ON HoaDon
FOR EACH ROW
BEGIN
    UPDATE HoaDon 
    SET TongTien = (
        SELECT COALESCE(SUM(SoLuong * DonGia), 0)
        FROM ChiTietHoaDon
        WHERE MaDon = NEW.MaDon
    )
    WHERE MaDon = NEW.MaDon;
END//

-- Trigger for DonNhapHang to calculate total when created
CREATE TRIGGER after_donnhaphang_insert
AFTER INSERT ON DonNhapHang
FOR EACH ROW
BEGIN
    UPDATE DonNhapHang 
    SET TongTien = (
        SELECT COALESCE(SUM(SoLuong * DonGia), 0)
        FROM ChiTietNhapHang
        WHERE MaDon = NEW.MaDon
    )
    WHERE MaDon = NEW.MaDon;
END//

-- Existing triggers for ChiTietHoaDon
CREATE TRIGGER after_chitiethoadon_insert
AFTER INSERT ON ChiTietHoaDon
FOR EACH ROW
BEGIN
    UPDATE HoaDon 
    SET TongTien = (
        SELECT SUM(SoLuong * DonGia)
        FROM ChiTietHoaDon
        WHERE MaDon = NEW.MaDon
    )
    WHERE MaDon = NEW.MaDon;
END//

CREATE TRIGGER after_chitiethoadon_update
AFTER UPDATE ON ChiTietHoaDon
FOR EACH ROW
BEGIN
    UPDATE HoaDon 
    SET TongTien = (
        SELECT SUM(SoLuong * DonGia)
        FROM ChiTietHoaDon
        WHERE MaDon = NEW.MaDon
    )
    WHERE MaDon = NEW.MaDon;
END//

CREATE TRIGGER after_chitiethoadon_delete
AFTER DELETE ON ChiTietHoaDon
FOR EACH ROW
BEGIN
    UPDATE HoaDon 
    SET TongTien = (
        SELECT COALESCE(SUM(SoLuong * DonGia), 0)
        FROM ChiTietHoaDon
        WHERE MaDon = OLD.MaDon
    )
    WHERE MaDon = OLD.MaDon;
END//

-- Existing triggers for ChiTietNhapHang
CREATE TRIGGER after_chitietnhaphang_insert
AFTER INSERT ON ChiTietNhapHang
FOR EACH ROW
BEGIN
    UPDATE DonNhapHang 
    SET TongTien = (
        SELECT SUM(SoLuong * DonGia)
        FROM ChiTietNhapHang
        WHERE MaDon = NEW.MaDon
    )
    WHERE MaDon = NEW.MaDon;
END//

CREATE TRIGGER after_chitietnhaphang_update
AFTER UPDATE ON ChiTietNhapHang
FOR EACH ROW
BEGIN
    UPDATE DonNhapHang 
    SET TongTien = (
        SELECT SUM(SoLuong * DonGia)
        FROM ChiTietNhapHang
        WHERE MaDon = NEW.MaDon
    )
    WHERE MaDon = NEW.MaDon;
END//

CREATE TRIGGER after_chitietnhaphang_delete
AFTER DELETE ON ChiTietNhapHang
FOR EACH ROW
BEGIN
    UPDATE DonNhapHang 
    SET TongTien = (
        SELECT COALESCE(SUM(SoLuong * DonGia), 0)
        FROM ChiTietNhapHang
        WHERE MaDon = OLD.MaDon
    )
    WHERE MaDon = OLD.MaDon;
END//

DELIMITER ; 