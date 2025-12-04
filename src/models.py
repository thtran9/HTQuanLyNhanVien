from datetime import *
from datetime import datetime, timedelta

# Cấu hình mặc định cho tính lương
WORKDAYS_PER_MONTH = 26
HOURS_PER_DAY = 8
# NHÂN VIÊN
class NhanVien:
    def __init__(self, employee_id, ho_ten, ngay_sinh, gioi_tinh, dept_id, position_id, ngay_vao_lam, email, phone, address, status="Active"):
        self.employee_id = employee_id
        self.ho_ten = ho_ten
        self.ngay_sinh = ngay_sinh
        self.gioi_tinh = gioi_tinh
        self.dept_id = dept_id
        self.position_id = position_id
        self.ngay_vao_lam = ngay_vao_lam
        self.email = email
        self.phone = phone
        self.address = address
        self.status = status

# PHÒNG BAN
class Department:
    def __init__(self, dept_id, name, manager_id, created_date, budget):
        self.dept_id = dept_id
        self.name = name
        self.manager_id = manager_id
        self.created_date = created_date
        self.budget = budget

# CHỨC VỤ

class Position:
    def __init__(self, position_id, title, level, min_salary, max_salary):
        self.position_id = position_id
        self.title = title
        self.level = level
        self.min_salary = min_salary
        self.max_salary = max_salary

# 4. CHẤM CÔNG
class Attendance:
    # Định nghĩa ca mặc định
    SHIFTS = {
        "morning": {"start": "08:00", "end": "12:00"},
        "afternoon": {"start": "13:00", "end": "17:00"}
    }

    def __init__(self, attendance_id, employee_id, date):
        self.attendance_id = attendance_id
        self.employee_id = employee_id
        self.date = date
        self.check_in = None
        self.check_out = None
        self.status = "Absent"
        self.late_minutes = 0
        self.leave_minutes = 0

    def mark_check_in(self):
        """Check-in tự động lấy giờ hiện tại (chỉ nhận nút bấm, không nhập thủ công)"""
        if self.check_in:
            raise ValueError("Check-in đã tồn tại")
        # Kiểm tra ngày hiện tại khớp với self.date
        today = datetime.now().strftime("%Y-%m-%d")
        if today != self.date:
            raise ValueError(f"Ngày không khớp: hôm nay là {today} nhưng record cho ngày {self.date}")
        self.check_in = datetime.now()
        self.status = "Present"

    def mark_check_out(self):
        """Check-out tự động lấy giờ hiện tại và tính muộn/về sớm (chỉ nhận nút bấm, không nhập thủ công)"""
        if not self.check_in:
            raise ValueError("Chưa check-in")
        if self.check_out:
            raise ValueError("Check-out đã tồn tại")
        # Kiểm tra ngày hiện tại khớp với self.date
        today = datetime.now().strftime("%Y-%m-%d")
        if today != self.date:
            raise ValueError(f"Ngày không khớp: hôm nay là {today} nhưng record cho ngày {self.date}")
        self.check_out = datetime.now()
        self._compute_late_and_early()

    def detect_shift(self):
        """Xác định ca dựa trên giờ check-in"""
        if not self.check_in:
            return "morning"
        time_only = self.check_in.time()
        for name, s in self.SHIFTS.items():
            start = datetime.strptime(s["start"], "%H:%M").time()
            end = datetime.strptime(s["end"], "%H:%M").time()
            if start <= time_only <= end:
                return name
        return "morning"

    def _compute_late_and_early(self):
        """Tính số phút đi muộn và về sớm theo ca"""
        shift = self.detect_shift()
        s = self.SHIFTS[shift]
        shift_start = datetime.combine(datetime.strptime(self.date, "%Y-%m-%d").date(),
                                       datetime.strptime(s["start"], "%H:%M").time())
        shift_end = datetime.combine(datetime.strptime(self.date, "%Y-%m-%d").date(),
                                     datetime.strptime(s["end"], "%H:%M").time())

        self.late_minutes = max(0, int((self.check_in - shift_start).total_seconds() // 60))
        self.leave_minutes = max(0, int((shift_end - self.check_out).total_seconds() // 60))

    def calculate_working_hours(self):
        """Tính tổng số giờ làm việc"""
        if not self.check_in or not self.check_out:
            return 0.0
        diff = self.check_out - self.check_in
        return round(diff.total_seconds() / 3600, 2)

    def to_dict(self):
        """Xuất dữ liệu dạng dictionary"""
        return {
            "attendance_id": self.attendance_id,
            "employee_id": self.employee_id,
            "date": self.date,
            "check_in": self.check_in.strftime("%Y-%m-%d %H:%M:%S") if self.check_in else "",
            "check_out": self.check_out.strftime("%Y-%m-%d %H:%M:%S") if self.check_out else "",
            "working_hours": self.calculate_working_hours(),
            "late_minutes": self.late_minutes,
            "leave_minutes": self.leave_minutes,
            "status": self.status
        }



# ===============================
# 6. BẢNG LƯƠNG
# =============================AD
# class SalaryRecord:
#     def __init__(self, salary_id, employee_id, month, year,
#                  basic_salary, working_days, overtime_hours,
#                  bonus, kpi, allowance, tax, position):
#         self.salary_id = salary_id
#         self.employee_id = employee_id
#         self.month = month
#         self.year = year
#         self.basic_salary = basic_salary
#         self.working_days = working_days
#         self.overtime_hours = overtime_hours
#         self.bonus = bonus
#         self.kpi = kpi
#         self.allowance = allowance
#         self.tax = tax  # thuế khác nếu có
#         self.position = position
#     def calculate_salary_by_position(self, late_minutes):
#         rules = POSITION_RULES.get(self.position, {})
        
#         # Phụ cấp và thưởng theo vị trí
#         allowance = rules.get("allowance_rate", 0) * self.basic_salary
#         bonus = rules.get("bonus_rate", 0) * self.basic_salary
        
#         # Overtime theo vị trí
#         try:
#             hourly = self.basic_salary / (WORKDAYS_PER_MONTH * HOURS_PER_DAY)
#         except Exception:
#             hourly = 0
#         overtime_pay = self.overtime_hours * rules.get("overtime_multiplier", 1.5) * hourly
        
#         # Tổng lương gộp
#         gross = (
#             self.calculate_basic_salary_by_workdays()
#             + overtime_pay
#             + bonus
#             + self.kpi
#             + allowance
#         )
        
#         # Khấu trừ
#         bhxh = 0.101 * self.basic_salary
#         cong_doan = 0.01 * self.basic_salary
#         thue_tncn = 0.05 * self.basic_salary
#         phat_di_muon = 2000 * late_minutes
        
#         deductions = bhxh + cong_doan + thue_tncn + phat_di_muon + self.tax
        
#         return gross - deductions
    
# ... (Giữ nguyên các class và hằng số khác)

# ===============================
# 6. BẢNG LƯƠNG
# ===============================

class SalaryRecord:
    def __init__(self, salary_id, employee_id, month, year,
                 working_days, overtime_hours, bonus, kpi, allowance, tax): # Bỏ basic_salary và position khỏi init
=======
WORKDAYS_PER_MONTH = 22
HOURS_PER_DAY = 8

class SalaryRecord:
    def __init__(self, salary_id, employee_id, month, year,
                 basic_salary, working_days, overtime_hours,
                 bonus=0, kpi=0, allowance=0, tax=0, position=""):

        self.salary_id = salary_id
        self.employee_id = employee_id
        self.month = month
        self.year = year
        self.working_days = working_days
        self.overtime_hours = overtime_hours
        self.bonus = bonus
        self.kpi = kpi
        self.allowance = allowance

        self.tax = tax  # thuế khác nếu có
    
    # Đổi tên và thêm tham số basic_salary, position vào hàm tính toán
    def calculate_net_salary(self, basic_salary, position, late_minutes):
        rules = POSITION_RULES.get(position, POSITION_RULES["Nhân viên"]) # Lấy rules theo position
        
        # 1. Tính Lương Gross
        
        # Lương theo ngày công (Giả định basic_salary là lương trọn gói/tháng)
        # Sử dụng basic_salary / WORKDAYS_PER_MONTH * working_days
        try:
            salary_by_workdays = (basic_salary / WORKDAYS_PER_MONTH) * self.working_days
        except Exception:
            salary_by_workdays = 0

        # Phụ cấp và thưởng cố định theo quy tắc
        allowance_by_rule = rules.get("allowance_rate", 0) * basic_salary
        bonus_by_rule = rules.get("bonus_rate", 0) * basic_salary
        
        # Overtime theo quy tắc
        try:
            hourly_rate = basic_salary / (WORKDAYS_PER_MONTH * HOURS_PER_DAY)
        except Exception:
            hourly_rate = 0
            
        overtime_pay = self.overtime_hours * rules.get("overtime_multiplier", 1.5) * hourly_rate
        
        # Tổng lương Gross
        gross = (
            salary_by_workdays
            + overtime_pay
            + bonus_by_rule
            + self.kpi  # Thưởng KPI nhập tay
            + allowance_by_rule # Phụ cấp theo quy tắc
            + self.allowance # Phụ cấp nhập tay khác
            + self.bonus # Thưởng nhập tay khác
        )
        
        # 2. Tính Khấu trừ
        
        # Các khoản khấu trừ cố định (tính trên basic_salary)
        bhxh = 0.101 * basic_salary
        cong_doan = 0.01 * basic_salary
        thue_tncn = 0.05 * basic_salary
        
        # Phạt
        PHAT_DI_MUON_MOT_PHUT = 2000
        phat_di_muon = PHAT_DI_MUON_MOT_PHUT * late_minutes
        
        deductions = bhxh + cong_doan + thue_tncn + phat_di_muon + self.tax
        
        self.gross_salary = gross # Thêm thuộc tính gross
        self.deductions = deductions # Thêm thuộc tính deductions
        self.net_salary = gross - deductions
        
        return self.net_salary
    
# ... (Giữ nguyên các class khác)


        self.tax = tax
        self.position = position

    def calculate_basic_salary_by_workdays(self):
        """Lương cơ bản theo số ngày công"""
        if WORKDAYS_PER_MONTH == 0:
            return 0
        return (self.basic_salary / WORKDAYS_PER_MONTH) * self.working_days

    def calculate_gross_salary(self):
        """Gross = lương cơ bản (theo ngày công) + OT + bonus + KPI + allowance"""
        hourly = self.basic_salary / (WORKDAYS_PER_MONTH * HOURS_PER_DAY) if WORKDAYS_PER_MONTH and HOURS_PER_DAY else 0
        overtime_pay = self.overtime_hours * 1.5 * hourly
        return (self.calculate_basic_salary_by_workdays()
                + overtime_pay
                + self.bonus
                + self.kpi
                + self.allowance)

    def calculate_net_salary(self, late_minutes=0):
        """Net = Gross - các khoản khấu trừ"""
        gross = self.calculate_gross_salary()
        bhxh = 0.101 * self.basic_salary
        cong_doan = 0.01 * self.basic_salary
        thue_tncn = 0.05 * self.basic_salary
        phat_di_muon = 2000 * late_minutes
        deductions = bhxh + cong_doan + thue_tncn + phat_di_muon + self.tax
        return gross - deductions

# 5. LÀM THÊM GIỜ (Overtime)
class OvertimeRequest:
    def __init__(self, request_id, employee_id, date, start_time, end_time, reason, request_status="Pending", approver_id=None):
        self.request_id = request_id
        self.employee_id = employee_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.reason = reason
        self.request_status = request_status
        self.approver_id = approver_id
    
    def calculate_overtime_hours(self):
        """Tính số giờ làm thêm"""
        try:
            start = datetime.strptime(self.start_time, "%H:%M")
            end = datetime.strptime(self.end_time, "%H:%M")
            hours = (end - start).seconds / 3600
            return max(0, hours)
        except:
            return 0
    
    def approve(self, approver_id):
        """Duyệt đơn làm thêm"""
        self.approver_id = approver_id
        self.request_status = "Approved"
    
    def reject(self, approver_id):
        """Từ chối đơn làm thêm"""
        self.approver_id = approver_id
        self.request_status = "Rejected"
    
    def is_approved(self):
        """Kiểm tra đã được duyệt chưa"""
        return self.request_status == "Approved"