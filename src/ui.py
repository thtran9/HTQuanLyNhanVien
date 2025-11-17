from services import *
from models import *
from datetime import datetime, date

nv_service = NhanVienService()
dept_service = DepartmentService()
pos_service = PositionService()
att_service = AttendanceService()
ot_service = OvertimeService()
salary_service = SalaryService()

def nhap_khong_trong(label):
    while True:
        val = input(f"{label}: ").strip()
        if val == "":
            print("❌ Không được để trống! Nhập lại.")
            continue
        return val

def nhap_ngay(label):
    while True:
        s = input(f"{label} (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(s, "%Y-%m-%d")
            return s
        except:
            print("❌ Sai định dạng ngày (YYYY-MM-DD). Hãy nhập lại!")

def nhap_float(label):
    while True:
        s = input(f"{label}: ").strip()
        if s == "":
            print("❌ Không được để trống!")
            continue
        try:
            return float(s)
        except:
            print("❌ Giá trị phải là số! Nhập lại.")


# ================================
# MENU QUẢN LÝ NHÂN VIÊN
# ================================
def menu_nhan_vien():
    while True:
        print("\n=== QUẢN LÝ NHÂN VIÊN ===")
        print("1. Thêm nhân viên")
        print("2. Danh sách nhân viên")
        print("3. Tìm theo ID")
        print("4. Xóa")
        print("5. Cập nhật")
        print("0. Quay lại")
        ch = input("Chọn: ").strip()

        if ch == "1":
            print("\n--- Thêm nhân viên ---")
            employee_id = nhap_khong_trong("ID")
            ho_ten = nhap_khong_trong("Họ tên")
            ngay_sinh = nhap_ngay("Ngày sinh")
            gioi_tinh = nhap_khong_trong("Giới tính")
            dept_id = nhap_khong_trong("Mã phòng ban")
            position_id = nhap_khong_trong("Mã chức vụ")
            ngay_vao_lam = nhap_ngay("Ngày vào làm")
            email = nhap_khong_trong("Email")
            phone = nhap_khong_trong("SĐT")
            address = nhap_khong_trong("Địa chỉ")

            nv = NhanVien(employee_id, ho_ten, ngay_sinh, gioi_tinh,
                           dept_id, position_id, ngay_vao_lam,
                           email, phone, address)

            nv_service.them_nhan_vien(nv)

        elif ch == "2":
            print("\n--- Danh sách nhân viên ---")
            ds = nv_service.lay_ds_nhan_vien()
            for nv in ds:
                print(nv)

        elif ch == "3":
            eid = nhap_khong_trong("Nhập ID")
            print(nv_service.tim_theo_id(eid))

        elif ch == "4":
            eid = nhap_khong_trong("Nhập ID để xóa")
            nv_service.xoa_nhan_vien(eid)

        elif ch == "5":
            eid = nhap_khong_trong("ID nhân viên cần cập nhật")
            field = nhap_khong_trong("Trường cần sửa")
            value = nhap_khong_trong("Giá trị mới")
            nv_service.cap_nhat_nhan_vien(eid, {field: value})

        elif ch == "0":
            break

        else:
            print("❌ Lựa chọn không hợp lệ!")


# ================================
# MENU PHÒNG BAN
# ================================
def menu_phong_ban():
    while True:
        print("\n=== PHÒNG BAN ===")
        print("1. Thêm phòng ban")
        print("2. Danh sách phòng ban")
        print("0. Quay lại")
        ch = input("Chọn: ").strip()

        if ch == "1":
            dept_id = nhap_khong_trong("ID phòng ban")
            name = nhap_khong_trong("Tên phòng ban")
            manager_id = nhap_khong_trong("ID trưởng phòng")
            created_date = nhap_ngay("Ngày tạo")
            budget = nhap_float("Ngân sách")

            dept = Department(dept_id, name, manager_id, created_date, budget)
            dept_service.them_phong_ban(dept)

        elif ch == "2":
            ds = dept_service.lay_ds_phong_ban()
            for d in ds:
                print(d)

        elif ch == "0":
            break

        else:
            print("❌ Lựa chọn không hợp lệ!")


# ================================
# MENU CHỨC VỤ
# ================================
def menu_chuc_vu():
    while True:
        print("\n=== CHỨC VỤ ===")
        print("1. Thêm chức vụ")
        print("2. Danh sách chức vụ")
        print("0. Quay lại")
        ch = input("Chọn: ").strip()

        if ch == "1":
            pid = nhap_khong_trong("ID chức vụ")
            title = nhap_khong_trong("Tên chức vụ")
            level = nhap_khong_trong("Level")
            min_salary = nhap_float("Lương tối thiểu")
            max_salary = nhap_float("Lương tối đa")
            basic_salary = nhap_float("Lương cơ bản")

            pos = Position(pid, title, level, min_salary, max_salary, basic_salary)
            pos_service.them_chuc_vu(pos)

        elif ch == "2":
            for p in pos_service.lay_ds_chuc_vu():
                print(p)

        elif ch == "0":
            break

        else:
            print("❌ Lựa chọn không hợp lệ!")


# ================================
# MENU CHẤM CÔNG
# ================================
def menu_cham_cong():
    while True:
        print("\n=== CHẤM CÔNG ===")
        print("1. Check-in")
        print("2. Check-out")
        print("3. Xem chấm công nhân viên")
        print("0. Quay lại")

        ch = input("Chọn: ").strip()

        if ch == "1":
            eid = nhap_khong_trong("ID nhân viên")
            today = str(date.today())
            time_in = nhap_khong_trong("Check-in (HH:MM)")

            a = Attendance("AT" + eid + today, eid, today, time_in, None, "Present")
            att_service.check_in(a)

        elif ch == "2":
            eid = nhap_khong_trong("ID nhân viên")
            today = str(date.today())
            time_out = nhap_khong_trong("Check-out (HH:MM)")

            att_service.check_out(eid, today, time_out)

        elif ch == "3":
            eid = nhap_khong_trong("ID nhân viên")
            for item in att_service.lay_cham_cong(eid):
                print(item)

        elif ch == "0":
            break

        else:
            print("❌ Lựa chọn không hợp lệ!")


# ================================
# MENU CHÍNH
# ================================
def menu_chinh():
    while True:
        print("\n===== MENU CHÍNH =====")
        print("1. Quản lý nhân viên")
        print("2. Quản lý phòng ban")
        print("3. Quản lý chức vụ")
        print("4. Chấm công")
        print("0. Thoát")
        ch = input("Chọn: ").strip()

        if ch == "1":
            menu_nhan_vien()
        elif ch == "2":
            menu_phong_ban()
        elif ch == "3":
            menu_chuc_vu()
        elif ch == "4":
            menu_cham_cong()
        elif ch == "0":
            print("Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")
