DELIMITER //

-- Drop HoaDon triggers
DROP TRIGGER IF EXISTS after_hoadon_insert//

-- Drop DonNhapHang triggers
DROP TRIGGER IF EXISTS after_donnhaphang_insert//

-- Drop ChiTietHoaDon triggers
DROP TRIGGER IF EXISTS after_chitiethoadon_insert//
DROP TRIGGER IF EXISTS after_chitiethoadon_update//
DROP TRIGGER IF EXISTS after_chitiethoadon_delete//

-- Drop ChiTietNhapHang triggers
DROP TRIGGER IF EXISTS after_chitietnhaphang_insert//
DROP TRIGGER IF EXISTS after_chitietnhaphang_update//
DROP TRIGGER IF EXISTS after_chitietnhaphang_delete//

DELIMITER ; 