from datetime import datetime
import customtkinter as ctk
from tkinter import ttk, messagebox, Menu, simpledialog
import re
import mysql.connector
# --- CẤU HÌNH GIAO DIỆN TỔNG THỂ (NÂNG CẤP) ---
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Bảng màu mới: tông pastel, thanh lịch
COLORS = {
    "primary": "#3B82F6",           # Xanh dương tươi
    "primary_hover": "#2563EB",
    "success": "#10B981",           # Xanh lá mint
    "success_hover": "#059669",
    "danger": "#EF4444",            # Đỏ nhạt
    "danger_hover": "#DC2626",
    "warning": "#F59E0B",           # Cam vàng
    "warning_hover": "#D97706",
    "bg_light": "#F8FAFC",          # Nền tổng thể
    "bg_white": "#FFFFFF",
    "text_main": "#1E293B",         # Chữ chính
    "text_sub": "#64748B",          # Chữ phụ
    "border": "#E2E8F0",            # Viền nhẹ
    "sidebar_bg": "#FFFFFF",
    "card_shadow": "#0F172A"        # (dùng cho hiệu ứng nhẹ, không phải đổ bóng thật)
}

# Font chữ nâng cấp: sử dụng Inter nếu có, fallback Segoe UI
FONTS = {
    "h1": ("Inter", 26, "bold"),
    "h2": ("Inter", 20, "bold"),
    "h3": ("Inter", 15, "bold"),
    "body": ("Inter", 13),
    "table": ("Inter", 12),
    "button": ("Inter", 13, "bold")
}

ICONS = {
    "pat": "👤", "doc": "👨‍⚕️", "nur": "👩‍⚕️", "med": "💊", "vis": "📋", "dis": "🦠",
    "add": "＋", "edit": "✏️", "del": "🗑️", "save": "💾", "money": "💰", "salary": "📄", "logout": "🔒", "profile": "🆔"
}

db_config = {
    "host": "localhost",
    "user": "root",
    "passwd": "332007",
    "database": "btlon"
}

def get_connection():
    return mysql.connector.connect(**db_config)

conn = get_connection()
cursor = conn.cursor()

def validate_data(data):
    if 'cmt' in data and not (str(data['cmt']).isdigit() and len(str(data['cmt'])) == 12):
        messagebox.showerror("Lỗi", "CCCD phải là số và có đúng 12 chữ số!")
        return False
    if 'phone' in data and not (str(data['phone']).isdigit() and len(str(data['phone'])) == 10):
        messagebox.showerror("Lỗi", "Số điện thoại phải là số và có đúng 10 chữ số!")
        return False
    if 'dob' in data:
        date_pattern = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
        if not re.match(date_pattern, str(data['dob'])):
            messagebox.showerror("Lỗi", "Ngày sinh phải đúng định dạng dd/mm/yyyy")
            return False
    return True

# --- LỚP FORM NHẬP LIỆU (GIAO DIỆN ĐẸP HƠN) ---
class UniversalFormWindow(ctk.CTkToplevel):
    def __init__(self, master, title, fields, target_tree, mode="add", item_id=None, old_vals=None, icon=""):
        super().__init__(master)
        self.master = master
        self.target_tree = target_tree
        self.mode = mode
        self.item_id = item_id
        self.title(f"Cập nhật {title}")
        self.geometry("540x780")
        self.configure(fg_color=COLORS["bg_light"])
        self.attributes("-topmost", True)
        self.grab_set()

        # Header đẹp hơn
        header = ctk.CTkFrame(self, fg_color=COLORS["primary"], height=100, corner_radius=0)
        header.pack(fill="x", side="top")
        title_str = f"{icon} {title.upper()}" if icon else title.upper()
        ctk.CTkLabel(header, text=title_str, font=FONTS["h1"], text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        self.card = ctk.CTkFrame(self, fg_color="white", corner_radius=24, border_width=1, border_color=COLORS["border"])
        self.card.pack(padx=30, pady=30, fill="both", expand=True)

        container = ctk.CTkScrollableFrame(self.card, fg_color="transparent", corner_radius=0)
        container.pack(padx=20, pady=20, fill="both", expand=True)

        self.entries = {}
        for i, (label_text, key) in enumerate(fields):
            lbl = ctk.CTkLabel(container, text=label_text, font=("Inter", 13, "bold"), text_color=COLORS["text_sub"])
            lbl.pack(anchor="w", padx=25, pady=(15, 0))
            e = ctk.CTkEntry(container, height=46, corner_radius=10, border_color=COLORS["border"], fg_color="#F9FAFB")
            if mode == "edit" and old_vals:
                e.insert(0, str(old_vals[i]))
                if key == 'id': e.configure(state="disabled", fg_color="#F1F5F9")
            e.pack(fill="x", padx=25, pady=5)
            self.entries[key] = e

        btn_txt = f"{ICONS['add']} THÊM MỚI" if mode == "add" else f"{ICONS['edit']} CẬP NHẬT"
        btn_color = COLORS["success"] if mode == "add" else COLORS["primary"]
        btn_hover = COLORS["success_hover"] if mode == "add" else COLORS["primary_hover"]

        self.btn_save = ctk.CTkButton(self, text=btn_txt, fg_color=btn_color, hover_color=btn_hover,
                                      height=58, font=FONTS["button"], corner_radius=14, command=self.handle_save)
        self.btn_save.pack(pady=(0, 30), padx=50, fill="x")

#Luu du lieu va cap nhat vao db
    def handle_save(self):
        d = {k: str(e.get().strip()) for k, e in self.entries.items()}
        if any(v == "" for k, v in d.items() if k != 'lk'):
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ các trường!")
            return
        if not validate_data(d):
            return

        try:
            keys = list(d.keys())
            values = list(d.values())
            if keys == ['id', 'cmt', 'n', 'p', 'd', 'a']:
                if self.mode == "add":
                    cursor.execute("INSERT INTO benhnhan (mabenhnhan, cmt, tenbenhnhan, sdt, birth, diachi) VALUES (%s,%s,%s,%s,%s,%s)",
                                   (d['id'], d['cmt'], d['n'], d['p'], d['d'], d['a']))
                else:
                    cursor.execute("UPDATE benhnhan SET cmt=%s, tenbenhnhan=%s, sdt=%s, birth=%s, diachi=%s WHERE mabenhnhan=%s",
                                   (d['cmt'], d['n'], d['p'], d['d'], d['a'], d['id']))
            elif keys == ['id', 'cmt', 'n', 'p', 'd', 'a', 'l', 's', 'sl']:
                if self.mode == "add":
                    cursor.execute("INSERT INTO bsi VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", tuple(values))
                else:
                    cursor.execute("UPDATE bsi SET cmt=%s, tenbsi=%s, sdt=%s, birth=%s, diachi=%s, qualification=%s, department=%s, salary=%s WHERE mabsi=%s",
                                   (d['cmt'], d['n'], d['p'], d['d'], d['a'], d['l'], d['s'], d['sl'], d['id']))
            elif keys == ['id', 'cmt', 'n', 'p', 'd', 'a', 'l', 'sl']:
                if self.mode == "add":
                    cursor.execute("INSERT INTO yta VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", tuple(values))
                else:
                    cursor.execute("UPDATE yta SET cmt=%s, tenyta=%s, sdt=%s, birth=%s, diachi=%s, qualification=%s, salary=%s WHERE mayta=%s",
                                   (d['cmt'], d['n'], d['p'], d['d'], d['a'], d['l'], d['sl'], d['id']))
            elif keys == ['id', 'name', 'price_in', 'price_out']:
                if self.mode == "add":
                    cursor.execute("INSERT INTO thuoc VALUES (%s,%s,%s,%s)", tuple(values))
                else:
                    cursor.execute("UPDATE thuoc SET tenthuoc=%s, gianhap=%s, giaban=%s WHERE mathuoc=%s",
                                   (d['name'], d['price_in'], d['price_out'], d['id']))
            elif keys == ['id', 'bn', 'iv', 'ov', 'st', 'pr', 'bs', 'mb']:
                cursor.execute("SELECT mabenh FROM loaibenh")
                danh_sach_ma_benh = [str(row[0]) for row in cursor.fetchall()]
                if d['mb'] not in danh_sach_ma_benh:
                    messagebox.showinfo("Lỗi", "Mã bệnh chưa tồn tại trong danh mục Loại Bệnh!")
                    return
                if self.mode == "add":
                    cursor.execute("INSERT INTO luotkham (maluotkham, mabenhnhan, ngayvaovien, ngayravien, trangthai, tongtien, mabsi, mabenh) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                                   (d['id'], d['bn'], d['iv'], d['ov'], d['st'], d['pr'], d['bs'], d['mb']))
                else:
                    cursor.execute("UPDATE luotkham SET mabenhnhan=%s, ngayvaovien=%s, ngayravien=%s, trangthai=%s, tongtien=%s, mabsi=%s, mabenh=%s WHERE maluotkham=%s",
                                   (d['bn'], d['iv'], d['ov'], d['st'], d['pr'], d['bs'], d['mb'], d['id']))
            elif keys == ['id', 'name', 'lk']:
                ma_benh, ten_benh = d['id'], d['name']
                cursor.execute("SELECT * FROM loaibenh WHERE mabenh = %s OR tenbenh = %s", (ma_benh, ten_benh))
                if cursor.fetchone() and self.mode == "add":
                    messagebox.showwarning("Trùng dữ liệu", "Mã bệnh hoặc tên bệnh này đã tồn tại!")
                    return
                if self.mode == "add":
                    cursor.execute("INSERT INTO loaibenh (mabenh, tenbenh) VALUES (%s, %s)", (ma_benh, ten_benh))
                else:
                    cursor.execute("UPDATE loaibenh SET tenbenh=%s WHERE mabenh=%s", (ten_benh, ma_benh))

            conn.commit()
            if hasattr(self.master, 'load_all_data'): self.master.load_all_data()
            if hasattr(self.master, 'load_my_patients'): self.master.load_my_patients()
            if hasattr(self.master, 'salary_window') and self.master.salary_window:
                try:
                    self.master.salary_window.refresh_salary_data()
                except: pass
            if hasattr(self.master, 'revenue_window') and self.master.revenue_window:
                try:
                    self.master.revenue_window.refresh_revenue_thuoc()
                except: pass
            messagebox.showinfo("Thành công", "Dữ liệu đã được lưu thành công!")
            self.destroy()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi Database", f"Chi tiết lỗi: {str(e)}")
        self.dashboard_frame.load_recent_patients()
# --- HỒ SƠ CÁ NHÂN BÁC SĨ (ĐẸP HƠN) ---
class DoctorProfileWindow(ctk.CTkToplevel):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.title("Hồ Sơ Cá Nhân")
        self.geometry("480x620")
        self.configure(fg_color=COLORS["bg_light"])
        self.grab_set()

        try:
            cursor.execute("SELECT * FROM bsi WHERE mabsi = %s", (user_id,))
            bs_data = cursor.fetchone()
            if not bs_data:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin cá nhân!")
                self.destroy()
                return
            cursor.execute("SELECT COUNT(*) FROM luotkham WHERE mabsi = %s", (user_id,))
            so_luot_kham = cursor.fetchone()[0]
        except Exception as e:
            messagebox.showerror("Lỗi DB", str(e))
            self.destroy()
            return

        ma, cccd, ten, sdt, ns, dc, trinhdo, khoa, luong_cung = bs_data
        luong_tong = int(luong_cung) + (so_luot_kham * 500000)

        ctk.CTkLabel(self, text="👨‍⚕️ THÔNG TIN BÁC SĨ", font=FONTS["h2"], text_color=COLORS["primary"]).pack(pady=(20, 10))
        card = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        self.add_info_row(card, "Mã Bác Sĩ:", ma)
        self.add_info_row(card, "Họ và Tên:", ten, bold=True)
        self.add_info_row(card, "CCCD:", cccd)
        self.add_info_row(card, "Ngày Sinh:", ns)
        self.add_info_row(card, "Số Điện Thoại:", sdt)
        self.add_info_row(card, "Chuyên Môn:", khoa)

        ctk.CTkFrame(card, height=2, fg_color=COLORS["border"]).pack(fill="x", padx=20, pady=10)

        self.add_info_row(card, "Số Lượt Khám:", f"{so_luot_kham} lượt")
        self.add_info_row(card, "Lương Cứng:", f"{int(luong_cung):,} VNĐ")
        self.add_info_row(card, "Tổng Thu Nhập:", f"{luong_tong:,} VNĐ", highlight=True)

    def add_info_row(self, parent, label, value, bold=False, highlight=False):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(row, text=label, font=FONTS["body"], text_color=COLORS["text_sub"]).pack(side="left")
        font = FONTS["h3"] if bold or highlight else FONTS["body"]
        color = COLORS["success"] if highlight else COLORS["text_main"]
        ctk.CTkLabel(row, text=str(value), font=font, text_color=color).pack(side="right")

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, main_app):
        super().__init__(master, fg_color="transparent")
        self.main_app = main_app
        self.user_id = main_app.user_id      # Lưu ID bác sĩ (nếu là Doctor)
        self.role = main_app.role

        # Chia layout 2 cột: trái (thông báo) và phải (tìm kiếm + bệnh nhân)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- CỘT TRÁI: THÔNG BÁO ---
        left_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_width=1, border_color=COLORS["border"])
        left_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        header_left = ctk.CTkFrame(left_frame, fg_color="transparent", height=50)
        header_left.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")
        ctk.CTkLabel(header_left, text="🔔 THÔNG BÁO HOẠT ĐỘNG", font=FONTS["h2"], text_color=COLORS["primary"]).pack(side="left")
        ctk.CTkLabel(header_left, text="Hôm nay", font=FONTS["body"], text_color=COLORS["text_sub"]).pack(side="right")

        self.noti_container = ctk.CTkScrollableFrame(left_frame, fg_color="transparent")
        self.noti_container.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # --- CỘT PHẢI: TÌM KIẾM & DANH SÁCH BỆNH NHÂN ---
        right_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_width=1, border_color=COLORS["border"])
        right_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        right_frame.grid_rowconfigure(2, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        header_right = ctk.CTkFrame(right_frame, fg_color="transparent", height=50)
        header_right.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")
        ctk.CTkLabel(header_right, text="👥 TÌM KIẾM BỆNH NHÂN", font=FONTS["h2"], text_color=COLORS["primary"]).pack(side="left")

        # --- Thanh tìm kiếm + nút Tìm ---
        search_frame = ctk.CTkFrame(right_frame, fg_color=COLORS["bg_light"], corner_radius=12)
        search_frame.grid(row=1, column=0, padx=15, pady=10, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Nhập tên hoặc mã bệnh nhân...", height=40,
                                         border_width=0, fg_color="transparent")
        self.search_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.search_entry.bind("<Return>", lambda e: self.search_patients())

        search_btn = ctk.CTkButton(search_frame, text="Tìm", width=60, height=32, corner_radius=8,
                                   fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                                   command=self.search_patients)
        search_btn.grid(row=0, column=1, padx=5, pady=5)

        # --- Container hiển thị kết quả ---
        self.patient_container = ctk.CTkScrollableFrame(right_frame, fg_color="transparent")
        self.patient_container.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Nút "Xem tất cả"
        btn_all = ctk.CTkButton(right_frame, text="Xem tất cả bệnh nhân", fg_color=COLORS["primary"],
                                hover_color=COLORS["primary_hover"], height=40, corner_radius=10,
                                command=lambda: self.main_app.tabview.set(f"{ICONS['pat']} Bệnh Nhân"))
        btn_all.grid(row=3, column=0, padx=15, pady=(5, 15), sticky="ew")

        # Tải dữ liệu ban đầu
        self.load_notifications()
        self.load_recent_patients()

    def load_notifications(self):
        #Tải 8 lượt khám gần nhất làm thông báo
        for widget in self.noti_container.winfo_children():
            widget.destroy()
        try:
            cursor.execute("""
                SELECT lk.maluotkham, bn.tenbenhnhan, lk.ngayvaovien, lk.trangthai, bn.mabenhnhan
                FROM luotkham lk
                JOIN benhnhan bn ON lk.mabenhnhan = bn.mabenhnhan
                ORDER BY lk.ngayvaovien DESC
                LIMIT 8
            """)
            rows = cursor.fetchall()
            if not rows:
                self.show_empty_message(self.noti_container, "Chưa có thông báo nào")
                return
            for row in rows:
                ma_lk, ten_bn, ngay_vao, trang_thai, ma_bn = row
                self.create_notification_card(ma_lk, ten_bn, ngay_vao, trang_thai)
        except Exception as e:
            print("Lỗi tải thông báo:", e)
            self.show_empty_message(self.noti_container, "Không thể tải dữ liệu")

    def create_notification_card(self, ma_lk, ten_bn, ngay_vao, trang_thai):
        """Tạo một card thông báo"""
        card = ctk.CTkFrame(self.noti_container, fg_color=COLORS["bg_light"], corner_radius=12)
        card.pack(fill="x", pady=5, padx=5)

        icon_map = {"Đang điều trị": "🟡", "Đã ra viện": "🟢", "Chờ khám": "🔵"}
        icon = icon_map.get(trang_thai, "⚪")
        ctk.CTkLabel(card, text=icon, font=("Segoe UI", 20)).pack(side="left", padx=10, pady=10)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=5, pady=8)

        title = f"Lượt khám #{ma_lk} - {ten_bn}"
        ctk.CTkLabel(content, text=title, font=("Inter", 13, "bold"), text_color=COLORS["text_main"]).pack(anchor="w")
        ctk.CTkLabel(content, text=f"Ngày vào: {ngay_vao}  •  Trạng thái: {trang_thai}",
                     font=FONTS["body"], text_color=COLORS["text_sub"]).pack(anchor="w")

        ctk.CTkLabel(card, text="Hôm nay", font=("Inter", 11), text_color=COLORS["text_sub"]).pack(side="right", padx=10)

    def load_recent_patients(self):
        for widget in self.patient_container.winfo_children():
            widget.destroy()
        try:
            if self.role == "Doctor":
                query = """
                    SELECT bn.mabenhnhan, bn.tenbenhnhan, bn.sdt, bn.birth, bn.diachi
                    FROM benhnhan bn
                    JOIN luotkham lk ON bn.mabenhnhan = lk.mabenhnhan
                    WHERE lk.mabsi = %s
                    GROUP BY bn.mabenhnhan
                    ORDER BY MAX(lk.ngayvaovien) DESC
                    LIMIT 5
                """
                cursor.execute(query, (self.user_id,))
            elif self.role == "Admin":
                cursor.execute("""
                    SELECT mabenhnhan, tenbenhnhan, sdt, birth, diachi
                    FROM benhnhan
                    ORDER BY mabenhnhan DESC
                    LIMIT 5
                """)
            rows = cursor.fetchall()
            if not rows:
                self.show_empty_message(self.patient_container, "Chưa có bệnh nhân nào")
                return
            for row in rows:
                ma_bn, ten, sdt, ns, dc = row
                self.create_patient_card({"ma": ma_bn, "ten": ten, "sdt": sdt, "ns": ns, "dc": dc})
        except Exception as e:
            print("Lỗi tải bệnh nhân:", e)
            self.show_empty_message(self.patient_container, "Không thể tải dữ liệu")


    def search_patients(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.load_recent_patients()
            return

        for widget in self.patient_container.winfo_children():
            widget.destroy()

        try:
            if self.role == "Doctor":
                # Tìm theo mã hoặc tên, nhưng chỉ trong bệnh nhân của bác sĩ này
                query = """
                    SELECT DISTINCT bn.mabenhnhan, bn.tenbenhnhan, bn.sdt, bn.birth, bn.diachi
                    FROM benhnhan bn
                    JOIN luotkham lk ON bn.mabenhnhan = lk.mabenhnhan
                    WHERE lk.mabsi = %s
                      AND (bn.mabenhnhan = %s OR bn.tenbenhnhan LIKE %s)
                    ORDER BY bn.tenbenhnhan
                """
                cursor.execute(query, (self.user_id, keyword, f"%{keyword}%"))
            else:
                # Admin tìm toàn bộ
                query = """
                    SELECT mabenhnhan, tenbenhnhan, sdt, birth, diachi
                    FROM benhnhan
                    WHERE mabenhnhan = %s OR tenbenhnhan LIKE %s
                    ORDER BY tenbenhnhan
                """
                cursor.execute(query, (keyword, f"%{keyword}%"))
            rows = cursor.fetchall()

            if not rows:
                self.show_empty_message(self.patient_container, f"❌ Không tìm thấy bệnh nhân với từ khóa '{keyword}'")
                return

            for row in rows:
                ma_bn, ten, sdt, ns, dc = row
                self.create_patient_card({"ma": ma_bn, "ten": ten, "sdt": sdt, "ns": ns, "dc": dc})
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {e}")
            self.show_empty_message(self.patient_container, "Lỗi tìm kiếm")

    def create_patient_card(self, data):
        """Tạo card bệnh nhân"""
        card = ctk.CTkFrame(self.patient_container, fg_color=COLORS["bg_light"], corner_radius=12)
        card.pack(fill="x", pady=5, padx=5)

        # Avatar giả
        avatar = ctk.CTkFrame(card, width=45, height=45, corner_radius=22, fg_color=COLORS["primary"])
        avatar.pack(side="left", padx=10, pady=10)
        avatar.pack_propagate(False)
        ctk.CTkLabel(avatar, text="👤", font=("Segoe UI", 22), text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=5, pady=8)

        ctk.CTkLabel(info, text=data["ten"], font=("Inter", 13, "bold"), text_color=COLORS["text_main"]).pack(anchor="w")
        ctk.CTkLabel(info, text=f"Mã: {data['ma']}  •  SĐT: {data['sdt']}", font=FONTS["body"], text_color=COLORS["text_sub"]).pack(anchor="w")
        ctk.CTkLabel(info, text=f"Ngày sinh: {data['ns']}", font=FONTS["body"], text_color=COLORS["text_sub"]).pack(anchor="w")

    def show_empty_message(self, parent, message):
        for widget in parent.winfo_children():
            widget.destroy()
        ctk.CTkLabel(parent, text=message, font=FONTS["body"], text_color=COLORS["text_sub"]).pack(pady=20)
# --- GIAO DIỆN CHÍNH (NÂNG CẤP) ---
class MainApp(ctk.CTkToplevel):
    def __init__(self, login_app, role, user_id=None):
        super().__init__()
        self.search_entries = {}
        self.login_app = login_app
        self.role, self.user_id = role, str(user_id) if user_id else None
        self.salary_window = None
        self.revenue_window = None
        self.title(f"SUS - Dashboard ({role})")
        self.geometry("1440x920")
        self.configure(fg_color=COLORS["bg_light"])

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color=COLORS["sidebar_bg"], border_width=1,
                                    border_color=COLORS["border"])
        self.sidebar.pack(side="left", fill="y")

        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=40, padx=20, fill="x")
        ctk.CTkLabel(logo_frame, text="✚", font=("Arial", 38), text_color=COLORS["primary"]).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(logo_frame, text="SUS", font=FONTS["h2"], text_color=COLORS["primary"]).pack(side="left")

        user_card = ctk.CTkFrame(self.sidebar, fg_color=COLORS["bg_light"], corner_radius=18, border_width=1,
                                 border_color=COLORS["border"])
        user_card.pack(padx=20, pady=10, fill="x")
        ctk.CTkLabel(user_card, text=ICONS["doc"] if role == "Doctor" else "🛠️", font=("Arial", 32)).pack(pady=(15, 5))
        ctk.CTkLabel(user_card, text=f"{role}", font=FONTS["h3"]).pack()
        ctk.CTkLabel(user_card, text=f"ID: {user_id if user_id else 'Quản trị viên'}", font=FONTS["body"],
                     text_color=COLORS["text_sub"]).pack(pady=(0, 15))

        sys_btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        sys_btn_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        if self.role == "Doctor":
            self.btn_sys(sys_btn_frame, f"{ICONS['profile']} Hồ sơ cá nhân", self.open_profile, COLORS["primary"], "white")
        if self.role == "Admin":
            self.btn_sys(sys_btn_frame, f"{ICONS['salary']} Bảng Lương", self.open_salary, COLORS["bg_light"], COLORS["text_main"])
            self.btn_sys(sys_btn_frame, f"{ICONS['money']} Doanh Thu", self.open_revenue, COLORS["warning"], "black")
        self.btn_sys(sys_btn_frame, f"{ICONS['logout']} Đăng xuất", self.logout, COLORS["danger"], "white")

        # MAIN CONTAINER
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(side="right", fill="both", expand=True)

        self.top_bar = ctk.CTkFrame(self.main_container, height=90, fg_color=COLORS["bg_white"], corner_radius=0,
                                    border_width=1, border_color=COLORS["border"])
        self.top_bar.pack(side="top", fill="x")
        ctk.CTkLabel(self.top_bar, text="HỆ THỐNG QUẢN TRỊ PHÒNG KHÁM TỔNG THỂ", font=FONTS["h2"]).pack(side="left", padx=30)

        self.action_bar = ctk.CTkFrame(self.main_container, fg_color=COLORS["bg_white"], height=110, corner_radius=24,
                                       border_width=1, border_color=COLORS["border"])
        self.action_bar.pack(side="bottom", fill="x", padx=30, pady=(0, 25))

        btn_container = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        btn_container.pack(pady=25, padx=30, fill="x")

        self.tabview = ctk.CTkTabview(self.main_container, corner_radius=24, fg_color=COLORS["bg_white"],
                                      segmented_button_selected_color=COLORS["primary"], border_width=1,
                                      border_color=COLORS["border"])
        self.tabview.pack(padx=30, pady=30, fill="both", expand=True)

        # --- THÊM TAB DASHBOARD (MỚI) ---
        self.dashboard_tab = self.tabview.add("🏠 Tổng quan")
        self.dashboard_frame = DashboardFrame(self.dashboard_tab, self)
        self.dashboard_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tạo tab Hồ sơ điều trị với thanh tìm kiếm
        self.tab_hoso = self.tabview.add("🩺 Hồ Sơ Điều Trị")
        hoso_main = ctk.CTkFrame(self.tab_hoso, fg_color="transparent")
        hoso_main.pack(fill="both", expand=True, padx=15, pady=15)

        # Thanh tìm kiếm
        search_frame = ctk.CTkFrame(hoso_main, fg_color=COLORS["bg_light"], corner_radius=12)
        search_frame.pack(fill="x", pady=(0, 10))

        self.hoso_search_entry = ctk.CTkEntry(search_frame,
                                              placeholder_text="🔍 Nhập mã BN, tên BN hoặc mã lượt khám...",
                                              height=40, border_width=0, fg_color="transparent")
        self.hoso_search_entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        self.hoso_search_entry.bind("<Return>", lambda e: self.perform_search("my_pats", self.hoso_search_entry.get()))

        btn_search = ctk.CTkButton(search_frame, text="Tìm", width=80, height=32, corner_radius=8,
                                   fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                                   command=lambda: self.perform_search("my_pats", self.hoso_search_entry.get()))
        btn_search.pack(side="right", padx=10, pady=5)

        # Treeview frame
        tree_frame = ctk.CTkFrame(hoso_main, fg_color="white", corner_radius=20,
                                  border_width=1, border_color=COLORS["border"])
        tree_frame.pack(fill="both", expand=True)

        # Treeview Hồ sơ điều trị
        cols = ("Mã LK", "Mã BN", "Tên Bệnh Nhân", "CCCD", "SĐT", "Ngày Sinh",
                "Địa Chỉ", "Bệnh Đang Mắc", "Trạng Thái LK", "Thuốc Đã Kê",
                "Y Tá Hỗ Trợ", "Tổng Lần Khám")

        # Style đã được định nghĩa ở trên, dùng lại
        self.tree_my_pats = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree_my_pats.heading(c, text=c)
            self.tree_my_pats.column(c, width=180, anchor="center")

        sb_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_my_pats.yview)
        sb_y.pack(side="right", fill="y", padx=(0, 5), pady=10)
        sb_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree_my_pats.xview)
        sb_x.pack(side="bottom", fill="x", padx=10, pady=(0, 5))

        self.tree_my_pats.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
        self.tree_my_pats.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(10, 0))

        self.tree_my_pats.bind("<Button-3>", lambda e: self.pop_m(e, self.tree_my_pats))
        self.tree_my_pats.bind("<Double-1>", lambda e: self.on_double_click(e, self.tree_my_pats, "my_pats"))


        self.tree_bn = self.setup_tab(f"{ICONS['pat']} Bệnh Nhân",
                                      ("Mã BN", "CCCD", "Họ Tên", "SĐT", "Ngày Sinh", "Địa Chỉ"),
                                      "bn", searchable=True)

        if self.role == "Admin":
            self.tree_bs = self.setup_tab(f"{ICONS['doc']} Bác Sĩ",
                                          ("Mã BS", "CCCD", "Họ Tên", "SĐT", "Ngày Sinh", "Địa Chỉ", "Trình Độ",
                                           "Chuyên Môn", "Lương Cứng"),
                                          "bs", searchable=True)

        self.tree_yt = self.setup_tab(f"{ICONS['nur']} Y Tá",
                                      ("Mã NV", "CCCD", "Họ Tên", "SĐT", "Ngày Sinh", "Địa Chỉ", "Trình Độ",
                                       "Lương Cứng"),
                                      "yt", searchable=True)

        self.tree_th = self.setup_tab(f"{ICONS['med']} Kho Thuốc",
                                      ("Mã Thuốc", "Tên Thuốc", "Giá Nhập", "Giá Bán"),
                                      "th", searchable=True)

        self.tree_lk = self.setup_tab(f"{ICONS['vis']} Lượt Khám",
                                      ("Mã LK", "Mã BN", "Ngày Vào", "Ngày Ra", "Trạng Thái", "Tổng Tiền", "Mã BS",
                                       "Mã Bệnh"),
                                      "lk", searchable=True)

        self.tree_benh = self.setup_tab(f"{ICONS['dis']} Bệnh Lý",
                                        ("Mã bệnh", "Tên Bệnh", "Mã LK", "Số người mắc"),
                                        "benh", searchable=False)

        # Nút chức năng
        if self.role == "Admin":
            self.btn_add_data(btn_container, f"{ICONS['add']} Thêm Bác sĩ", self.form_bs, COLORS["primary"])
            self.btn_add_data(btn_container, f"{ICONS['add']} Thêm Y tá", self.form_yt, COLORS["primary"])
            self.btn_add_data(btn_container, f"{ICONS['add']} Nhập Thuốc", self.form_th, COLORS["primary"])
        self.btn_add_data(btn_container, f"{ICONS['add']} Tiếp nhận BN", self.form_bn, COLORS["success"])
        self.btn_add_data(btn_container, f"{ICONS['add']} Tạo Lượt khám", self.form_lk, COLORS["success"])
        self.btn_add_data(btn_container, f"{ICONS['add']} Khai báo Bệnh", self.form_benh, COLORS["success"])
        self.btn_add_data(btn_container, f"👩‍⚕️ Gán Y Tá", self.form_assign_nurse, COLORS["warning"])
        self.btn_add_data(btn_container, f"💊 Kê Đơn Thuốc", self.form_assign_medicine, COLORS["warning"])

        self.load_all_data()
        self.load_my_patients()
        if self.role == "Doctor":
            self.apply_doctor_filter()
        # Cập nhật lại dashboard sau khi load dữ liệu
        if self.role == "Admin":
            self.dashboard_frame.load_notifications()
            self.dashboard_frame.load_recent_patients()

    def setup_tab(self, tab_title, cols, t_name, searchable=False):
        tab = self.tabview.add(tab_title)

        # Container chính của tab
        main_frame = ctk.CTkFrame(tab, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Thanh tìm kiếm (chỉ hiển thị nếu searchable=True)
        if searchable:
            search_frame = ctk.CTkFrame(main_frame, fg_color=COLORS["bg_light"], corner_radius=12)
            search_frame.pack(fill="x", pady=(0, 10))

            entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Nhập từ khóa...", height=40,
                                 border_width=0, fg_color="transparent")
            entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            entry.bind("<Return>", lambda e, t=t_name: self.perform_search(t, entry.get()))

            btn = ctk.CTkButton(search_frame, text="Tìm", width=80, height=32, corner_radius=8,
                                fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                                command=lambda t=t_name: self.perform_search(t, entry.get()))
            btn.pack(side="right", padx=10, pady=5)

            # Lưu entry để có thể truy cập sau
            self.search_entries[t_name] = entry
        else:
            self.search_entries[t_name] = None

        # Treeview frame
        tree_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=20,
                                  border_width=1, border_color=COLORS["border"])
        tree_frame.pack(fill="both", expand=True)

        # Style Treeview (giữ nguyên)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=FONTS["table"], rowheight=40, borderwidth=0,
                        background="white", fieldbackground="white", foreground=COLORS["text_main"])
        style.configure("Treeview.Heading", font=("Inter", 12, "bold"),
                        background=COLORS["bg_light"], foreground=COLORS["text_main"],
                        borderwidth=1, relief="flat")
        style.map("Treeview", background=[('selected', '#EFF6FF')],
                  foreground=[('selected', COLORS["primary"])])
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            width = 180 if t_name == "my_pats" else 120
            tree.heading(c, text=c)
            tree.column(c, width=width, anchor="center")

        # Scrollbars
        sb_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        sb_y.pack(side="right", fill="y", padx=(0, 5), pady=10)
        sb_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        sb_x.pack(side="bottom", fill="x", padx=10, pady=(0, 5))

        tree.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
        tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(10, 0))

        # Bindings
        tree.bind("<Button-3>", lambda e: self.pop_m(e, tree))
        tree.bind("<Double-1>", lambda e: self.on_double_click(e, tree, t_name))

        return tree

    def btn_add_data(self, parent, txt, cmd, color):
        hover = COLORS["primary_hover"] if color == COLORS["primary"] else COLORS["success_hover"] if color == COLORS["success"] else COLORS["warning_hover"]
        text_clr = "black" if color == COLORS["warning"] else "white"
        ctk.CTkButton(parent, text=txt, text_color=text_clr, fg_color=color, hover_color=hover, font=FONTS["button"],
                      width=130, height=50, corner_radius=12, command=cmd).pack(side="left", padx=8)

    def btn_sys(self, parent, txt, cmd, color, txt_color="white"):
        hover = COLORS["danger_hover"] if color == COLORS["danger"] else COLORS["warning_hover"] if color == COLORS["warning"] else "#E2E8F0"
        if txt_color == "white" and color != "transparent":
            ctk.CTkButton(parent, text=txt, fg_color=color, hover_color=hover, font=FONTS["body"], height=45,
                          corner_radius=10, command=cmd).pack(fill="x", pady=6)
        else:
            ctk.CTkButton(parent, text=txt, fg_color="transparent", text_color=txt_color, border_width=1,
                          border_color=COLORS["border"] if txt_color != "black" else COLORS["warning"],
                          hover_color=hover, font=FONTS["body"], height=45, corner_radius=10, command=cmd).pack(fill="x", pady=6)

    # --- CÁC HÀM CHỨC NĂNG GIỮ NGUYÊN LOGIC ---
    def open_salary(self):
        if self.salary_window is None or not self.salary_window.winfo_exists():
            self.salary_window = SalaryWindow(self)
        else:
            self.salary_window.focus()

    def open_revenue(self):
        if self.revenue_window is None or not self.revenue_window.winfo_exists():
            self.revenue_window = RevenueWindow(self)
        else:
            self.revenue_window.focus()

    def open_profile(self):
        DoctorProfileWindow(self, self.user_id)

    def load_all_data(self):
        if self.role=="Admin":
            for tree in [self.tree_bn, self.tree_bs, self.tree_yt, self.tree_th, self.tree_lk]:
                tree.delete(*tree.get_children())
        elif self.role=="Doctor":
            for tree in [self.tree_bn, self.tree_yt, self.tree_th, self.tree_lk]:
                tree.delete(*tree.get_children())
        if self.role == "Admin":
            for table, tree in [("benhnhan", self.tree_bn), ("bsi", self.tree_bs), ("yta", self.tree_yt),
                                ("thuoc", self.tree_th), ("luotkham", self.tree_lk)]:
                cursor.execute(f"SELECT * FROM {table}")
                for row in cursor.fetchall(): tree.insert("", "end", values=row)
        elif self.role == "Doctor":
            query_bn = """SELECT DISTINCT bn.* FROM benhnhan bn JOIN luotkham lk ON bn.mabenhnhan = lk.mabenhnhan WHERE lk.mabsi = %s"""
            cursor.execute(query_bn, (self.user_id,))
            for row in cursor.fetchall(): self.tree_bn.insert("", "end", values=row)
            cursor.execute("SELECT * FROM luotkham WHERE mabsi = %s", (self.user_id,))
            for row in cursor.fetchall(): self.tree_lk.insert("", "end", values=row)
            for table, tree in [("yta", self.tree_yt), ("thuoc", self.tree_th)]:
                cursor.execute(f"SELECT * FROM {table}")
                for row in cursor.fetchall(): tree.insert("", "end", values=row)
        self.refresh_data_benh()

    #load lai data
    def refresh_data_benh(self):
        cursor.execute("SELECT mabenh, tenbenh FROM loaibenh")
        all_benh = cursor.fetchall()
        cursor.execute("""SELECT lb.mabenh, lb.tenbenh, lk.maluotkham, lk.mabenhnhan
                          FROM loaibenh lb INNER JOIN luotkham lk ON lk.mabenh = lb.mabenh""")
        join_data = cursor.fetchall()
        result = {}
        for row in join_data:
            mb, tb, mlk, mbn = row
            if mb not in result: result[mb] = {"ten": tb, "lks": [], "bns": set()}
            result[mb]["lks"].append(str(mlk)); result[mb]["bns"].add(mbn)
        for mb, tb in all_benh:
            if mb not in result: result[mb] = {"ten": tb, "lks": ["Chưa có"], "bns": set()}
        final_data = sorted([[mb, info["ten"], info["lks"], len(info["bns"])] for mb, info in result.items()],
                            key=lambda x: (-x[3]))
        self.tree_benh.delete(*self.tree_benh.get_children())
        for r in final_data: self.tree_benh.insert("", "end", values=r)

    def load_my_patients(self):
        self.tree_my_pats.delete(*self.tree_my_pats.get_children())
        if self.role == "Doctor":
            query = """SELECT lk.maluotkham, bn.mabenhnhan, bn.tenbenhnhan, bn.cmt, bn.sdt, bn.birth, bn.diachi,
                       lb.tenbenh as benh, lk.trangthai,
                       (SELECT GROUP_CONCAT(CONCAT(t.tenthuoc, ' (', dt.soluong, ')') SEPARATOR ', ') 
                        FROM donthuoc dt JOIN thuoc t ON dt.mathuoc = t.mathuoc 
                        WHERE dt.maluotkham = lk.maluotkham) as thuoc,
                       (SELECT GROUP_CONCAT(yt.tenyta SEPARATOR ', ') 
                        FROM luotkham_yta lky JOIN yta yt ON lky.mayta = yt.mayta 
                        WHERE lky.maluotkham = lk.maluotkham) as ytas,
                       (SELECT COUNT(*) FROM luotkham lk2 WHERE lk2.mabenhnhan = bn.mabenhnhan AND lk2.mabsi = %s) as sl_kham
                FROM luotkham lk JOIN benhnhan bn ON lk.mabenhnhan = bn.mabenhnhan LEFT JOIN loaibenh lb ON lk.mabenh = lb.mabenh
                WHERE lk.mabsi = %s"""
            params = (self.user_id, self.user_id)
        else:
            query = """SELECT lk.maluotkham, bn.mabenhnhan, bn.tenbenhnhan, bn.cmt, bn.sdt, bn.birth, bn.diachi,
                       lb.tenbenh as benh, lk.trangthai,
                       (SELECT GROUP_CONCAT(CONCAT(t.tenthuoc, ' (', dt.soluong, ')') SEPARATOR ', ') 
                        FROM donthuoc dt JOIN thuoc t ON dt.mathuoc = t.mathuoc 
                        WHERE dt.maluotkham = lk.maluotkham) as thuoc,
                       (SELECT GROUP_CONCAT(yt.tenyta SEPARATOR ', ') 
                        FROM luotkham_yta lky JOIN yta yt ON lky.mayta = yt.mayta 
                        WHERE lky.maluotkham = lk.maluotkham) as ytas,
                       (SELECT COUNT(*) FROM luotkham lk2 WHERE lk2.mabenhnhan = bn.mabenhnhan) as sl_kham
                FROM luotkham lk JOIN benhnhan bn ON lk.mabenhnhan = bn.mabenhnhan LEFT JOIN loaibenh lb ON lk.mabenh = lb.mabenh"""
            params = ()
        try:
            cursor.execute(query, params)
            for row in cursor.fetchall():
                cleaned_row = [str(item) if item is not None else "Chưa có" for item in row]
                self.tree_my_pats.insert("", "end", values=cleaned_row)
        except Exception as e:
            print("Lỗi tải dữ liệu Hồ sơ điều trị:", e)
    cursor.execute("SELECT * from benhnhan inner join luotkham on benhnhan.mabenhnhan=luotkham.mabenhnhan where month(luotkham.ngayvaovien)= 1 and year(luotkham.ngayvaovien)=2026")
    print(cursor.fetchall())
#Gan yta
    def form_assign_nurse(self):
        try:
            current_tab = self.tabview.get()
            if current_tab == f"🩺 Hồ Sơ Điều Trị" and hasattr(self, 'tree_my_pats'):
                sel = self.tree_my_pats.selection()[0]
                ma_lk = self.tree_my_pats.item(sel, "values")[0]
            elif current_tab == f"{ICONS['vis']} Lượt Khám":
                sel = self.tree_lk.selection()[0]
                ma_lk = self.tree_lk.item(sel, "values")[0]
            else:
                messagebox.showwarning("Nhắc nhở", "Vui lòng chuyển sang tab 'Hồ Sơ Điều Trị' hoặc 'Lượt Khám' và chọn 1 dòng!")
                return
        except:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn 1 lượt khám trước khi gán Y tá!")
            return
        ma_yt = simpledialog.askstring("Phân công Y Tá", f"Nhập Mã Y Tá hỗ trợ cho Lượt Khám [{ma_lk}]:", parent=self)
        if ma_yt:
            try:
                cursor.execute("SELECT mayta FROM yta WHERE mayta = %s", (ma_yt,))
                if not cursor.fetchone():
                    messagebox.showerror("Lỗi", "Mã Y Tá này không tồn tại!")
                    return
                cursor.execute("SELECT * FROM luotkham_yta WHERE maluotkham = %s AND mayta = %s", (ma_lk, ma_yt))
                if cursor.fetchone():
                    messagebox.showinfo("Thông báo", "Y tá này đã được gán cho lượt khám này rồi.")
                    return
                cursor.execute("INSERT INTO luotkham_yta (maluotkham, mayta) VALUES (%s, %s)", (ma_lk, ma_yt))
                conn.commit()
                messagebox.showinfo("Thành công", f"Đã phân công Y tá {ma_yt} cho lượt khám {ma_lk}!")
                if hasattr(self, 'load_my_patients'): self.load_my_patients()
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", f"Chi tiết: {e}")

    #ke them don thuoc
    def form_assign_medicine(self):
        try:
            current_tab = self.tabview.get()
            if current_tab == f"🩺 Hồ Sơ Điều Trị" and hasattr(self, 'tree_my_pats'):
                sel = self.tree_my_pats.selection()[0]
                ma_lk = self.tree_my_pats.item(sel, "values")[0]
            elif current_tab == f"{ICONS['vis']} Lượt Khám":
                sel = self.tree_lk.selection()[0]
                ma_lk = self.tree_lk.item(sel, "values")[0]
            else:
                messagebox.showwarning("Nhắc nhở", "Vui lòng chuyển sang tab 'Hồ Sơ Điều Trị' hoặc 'Lượt Khám' và chọn 1 dòng!")
                return
        except:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn 1 lượt khám trước khi kê đơn!")
            return
        ma_thuoc = simpledialog.askstring("Kê Đơn Thuốc", f"Nhập Mã Thuốc cho Lượt Khám [{ma_lk}]:", parent=self)
        if not ma_thuoc: return
        try:
            cursor.execute("SELECT mathuoc FROM thuoc WHERE mathuoc = %s", (ma_thuoc,))
            if not cursor.fetchone():
                messagebox.showerror("Lỗi", "Mã Thuốc này không tồn tại!")
                return
            so_luong_str = simpledialog.askstring("Số lượng", f"Nhập số lượng thuốc [{ma_thuoc}]:", parent=self)
            if not so_luong_str or not so_luong_str.isdigit() or int(so_luong_str) <= 0:
                messagebox.showerror("Lỗi", "Số lượng không hợp lệ!")
                return
            so_luong = int(so_luong_str)
            cursor.execute("SELECT soluong FROM donthuoc WHERE maluotkham = %s AND mathuoc = %s", (ma_lk, ma_thuoc))
            row = cursor.fetchone()
            if row:
                new_sl = row[0] + so_luong
                cursor.execute("UPDATE donthuoc SET soluong = %s WHERE maluotkham = %s AND mathuoc = %s", (new_sl, ma_lk, ma_thuoc))
            else:
                cursor.execute("INSERT INTO donthuoc (maluotkham, mathuoc, soluong) VALUES (%s, %s, %s)", (ma_lk, ma_thuoc, so_luong))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã kê thành công {so_luong} thuốc {ma_thuoc} cho lượt khám {ma_lk}!")
            if hasattr(self, 'load_my_patients'): self.load_my_patients()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Chi tiết: {e}")

    def on_double_click(self, e, t, n):
        try:
            if self.role == "Admin":
                sel = t.selection()[0]; v = t.item(sel, "values")
                mapping = {"bs": (self.form_bs, "Bác sĩ", ICONS["doc"]), "yt": (self.form_yt, "Y tá", ICONS["nur"]),
                           "bn": (self.form_bn, "Bệnh nhân", ICONS["pat"]), "lk": (self.form_lk, "Lượt khám", ICONS["vis"]),
                           "th": (self.form_th, "Thuốc", ICONS["med"])}
                if n in mapping: func, title, icon = mapping[n]; func("edit", sel, v)
            elif self.role == "Doctor":
                sel = t.selection()[0]; v = t.item(sel, "values")
                if n == "bn": self.form_bn("edit", sel, v)
        except: pass

    def logout(self):
        self.withdraw(); self.login_app.deiconify()

    def form_bs(self, m="add", i=None, v=None):
        f = [("Mã BS:", "id"), ("CCCD:", "cmt"), ("Họ tên:", "n"), ("SĐT:", "p"), ("Ngày sinh:", "d"),
             ("Địa chỉ:", "a"), ("Trình độ:", "l"), ("Chuyên môn:", "s"), ("Lương cứng:", "sl")]
        UniversalFormWindow(self, "Bác sĩ", f, self.tree_bs, m, i, v, ICONS["doc"])

    def form_yt(self, m="add", i=None, v=None):
        f = [("Mã NV:", "id"), ("CCCD:", "cmt"), ("Họ tên:", "n"), ("SĐT:", "p"), ("Ngày sinh:", "d"),
             ("Địa chỉ:", "a"), ("Trình độ:", "l"), ("Lương cứng:", "sl")]
        UniversalFormWindow(self, "Y tá", f, self.tree_yt, m, i, v, ICONS["nur"])

    def form_bn(self, m="add", i=None, v=None):
        f = [("Mã BN:", "id"), ("CCCD:", "cmt"), ("Họ tên:", "n"), ("SĐT:", "p"), ("Ngày sinh:", "d"), ("Địa chỉ:", "a")]
        UniversalFormWindow(self, "Bệnh nhân", f, self.tree_bn, m, i, v, ICONS["pat"])

    def form_lk(self, m="add", i=None, v=None):
        f = [("Mã LK:", "id"), ("Mã BN:", "bn"), ("Ngày vào:", "iv"), ("Ngày ra:", "ov"), ("Trạng thái:", "st"),
             ("Tổng tiền:", "pr"), ("Mã BS:", "bs"),("Mã Bệnh:","mb")]
        UniversalFormWindow(self, "Lượt khám", f, self.tree_lk, m, i, v, ICONS["vis"])

    def form_th(self, m="add", i=None, v=None):
        f = [("Mã Thuốc:", "id"), ("Tên Thuốc:", "name"), ("Giá Nhập:", "price_in"), ("Giá Bán:", "price_out")]
        UniversalFormWindow(self, "Thuốc", f, self.tree_th, m, i, v, ICONS["med"])

    def form_benh(self, m="add", i=None, v=None):
        f = [("Mã Bệnh:", "id"), ("Tên Bệnh:", "name")]
        UniversalFormWindow(self, "Bệnh lý", f, self.tree_benh, m, i, v, ICONS["dis"])


    #xoa du lieu
    def pop_m(self, e, t):
        if t == self.tree_benh or (hasattr(self, 'tree_my_pats') and t == self.tree_my_pats): return
        if self.role == "Doctor" and t in [self.tree_bs, self.tree_yt, self.tree_th]:
            messagebox.showwarning("Từ chối thao tác", "Tài khoản Bác sĩ không có quyền xóa hồ sơ nhân sự!")
            return
        idx = t.identify_row(e.y)
        if idx:
            t.selection_set(idx); val = t.item(idx)['values']
            def xoa():
                if not messagebox.askyesno("Xác nhận", "Hành động này không thể hoàn tác. Tiếp tục xóa?"): return
                try:
                    query_map = {self.tree_bn: "benhnhan WHERE mabenhnhan", self.tree_bs: "bsi WHERE mabsi",
                                 self.tree_lk: "luotkham WHERE maluotkham", self.tree_yt: "yta WHERE mayta",
                                 self.tree_th: "thuoc WHERE mathuoc"}
                    cursor.execute(f"DELETE FROM {query_map[t]} = %s", (val[0],))
                    conn.commit(); t.delete(idx)
                    messagebox.showinfo("Thành công", "Đã xóa bản ghi!")
                    self.load_all_data()
                except Exception as err:
                    messagebox.showerror("Lỗi hệ thống", str(err))
            m = Menu(self, tearoff=0); m.add_command(label=f"{ICONS['del']} Xóa dữ liệu này", command=xoa)
            m.post(e.x_root, e.y_root)

    def apply_doctor_filter(self):
        if self.role != "Doctor": return
        if hasattr(self, 'tree_bs'):
            for i in self.tree_bs.get_children():
                if str(self.tree_bs.item(i, "values")[0]) != self.user_id:
                    self.tree_bs.detach(i)
        my_pats_ids = [str(self.tree_lk.item(i, "values")[1]) for i in self.tree_lk.get_children()
                       if str(self.tree_lk.item(i, "values")[6]) == self.user_id]
        for i in self.tree_bn.get_children():
            if str(self.tree_bn.item(i, "values")[0]) not in my_pats_ids:
                self.tree_bn.detach(i)

    def search_benhnhan(self, tree, keyword):
        if self.role == "Admin":
            query = """SELECT mabenhnhan, cmt, tenbenhnhan, sdt, birth, diachi
                       FROM benhnhan
                       WHERE mabenhnhan = %s OR tenbenhnhan LIKE %s
                       ORDER BY tenbenhnhan"""
            cursor.execute(query, (keyword, f"%{keyword}%"))
        else:  # Doctor
            query = """SELECT DISTINCT bn.mabenhnhan, bn.cmt, bn.tenbenhnhan, bn.sdt, bn.birth, bn.diachi
                       FROM benhnhan bn
                       JOIN luotkham lk ON bn.mabenhnhan = lk.mabenhnhan
                       WHERE lk.mabsi = %s
                         AND (bn.mabenhnhan = %s OR bn.tenbenhnhan LIKE %s)
                       ORDER BY bn.tenbenhnhan"""
            cursor.execute(query, (self.user_id, keyword, f"%{keyword}%"))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def search_bacsi(self, tree, keyword):
        query = """SELECT mabsi, cmt, tenbsi, sdt, birth, diachi, qualification, department, salary
                   FROM bsi
                   WHERE mabsi = %s OR tenbsi LIKE %s
                   ORDER BY tenbsi"""
        cursor.execute(query, (keyword, f"%{keyword}%"))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def search_yta(self, tree, keyword):
        query = """SELECT mayta, cmt, tenyta, sdt, birth, diachi, qualification, salary
                   FROM yta
                   WHERE mayta = %s OR tenyta LIKE %s
                   ORDER BY tenyta"""
        cursor.execute(query, (keyword, f"%{keyword}%"))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def search_thuoc(self, tree, keyword):
        query = """SELECT mathuoc, tenthuoc, gianhap, giaban
                   FROM thuoc
                   WHERE mathuoc = %s OR tenthuoc LIKE %s
                   ORDER BY tenthuoc"""
        cursor.execute(query, (keyword, f"%{keyword}%"))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def search_luotkham(self, tree, keyword):
        if self.role == "Admin":
            query = """SELECT maluotkham, mabenhnhan, ngayvaovien, ngayravien, trangthai, tongtien, mabsi, mabenh
                       FROM luotkham
                       WHERE maluotkham = %s OR mabenhnhan = %s
                       ORDER BY ngayvaovien DESC"""
            cursor.execute(query, (keyword, keyword))
        else:  # Doctor
            query = """SELECT maluotkham, mabenhnhan, ngayvaovien, ngayravien, trangthai, tongtien, mabsi, mabenh
                       FROM luotkham
                       WHERE mabsi = %s AND (maluotkham = %s OR mabenhnhan = %s)
                       ORDER BY ngayvaovien DESC"""
            cursor.execute(query, (self.user_id, keyword, keyword))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def search_hoso_dieutri(self, tree, keyword):
        if self.role == "Doctor":
            query = """SELECT lk.maluotkham, bn.mabenhnhan, bn.tenbenhnhan, bn.cmt, bn.sdt, bn.birth, bn.diachi,
                              lb.tenbenh as benh, lk.trangthai,
                              (SELECT GROUP_CONCAT(CONCAT(t.tenthuoc, ' (', dt.soluong, ')') SEPARATOR ', ') 
                               FROM donthuoc dt JOIN thuoc t ON dt.mathuoc = t.mathuoc 
                               WHERE dt.maluotkham = lk.maluotkham) as thuoc,
                              (SELECT GROUP_CONCAT(yt.tenyta SEPARATOR ', ') 
                               FROM luotkham_yta lky JOIN yta yt ON lky.mayta = yt.mayta 
                               WHERE lky.maluotkham = lk.maluotkham) as ytas,
                              (SELECT COUNT(*) FROM luotkham lk2 WHERE lk2.mabenhnhan = bn.mabenhnhan AND lk2.mabsi = %s) as sl_kham
                       FROM luotkham lk
                       JOIN benhnhan bn ON lk.mabenhnhan = bn.mabenhnhan
                       LEFT JOIN loaibenh lb ON lk.mabenh = lb.mabenh
                       WHERE lk.mabsi = %s
                         AND (lk.maluotkham = %s OR bn.mabenhnhan = %s OR bn.tenbenhnhan LIKE %s)
                       ORDER BY lk.ngayvaovien DESC"""
            cursor.execute(query, (self.user_id, self.user_id, keyword, keyword, f"%{keyword}%"))
        else:  # Admin
            query = """SELECT lk.maluotkham, bn.mabenhnhan, bn.tenbenhnhan, bn.cmt, bn.sdt, bn.birth, bn.diachi,
                              lb.tenbenh as benh, lk.trangthai,
                              (SELECT GROUP_CONCAT(CONCAT(t.tenthuoc, ' (', dt.soluong, ')') SEPARATOR ', ') 
                               FROM donthuoc dt JOIN thuoc t ON dt.mathuoc = t.mathuoc 
                               WHERE dt.maluotkham = lk.maluotkham) as thuoc,
                              (SELECT GROUP_CONCAT(yt.tenyta SEPARATOR ', ') 
                               FROM luotkham_yta lky JOIN yta yt ON lky.mayta = yt.mayta 
                               WHERE lky.maluotkham = lk.maluotkham) as ytas,
                              (SELECT COUNT(*) FROM luotkham lk2 WHERE lk2.mabenhnhan = bn.mabenhnhan) as sl_kham
                       FROM luotkham lk
                       JOIN benhnhan bn ON lk.mabenhnhan = bn.mabenhnhan
                       LEFT JOIN loaibenh lb ON lk.mabenh = lb.mabenh
                       WHERE lk.maluotkham = %s OR bn.mabenhnhan = %s OR bn.tenbenhnhan LIKE %s
                       ORDER BY lk.ngayvaovien DESC"""
            cursor.execute(query, (keyword, keyword, f"%{keyword}%"))
        for row in cursor.fetchall():
            cleaned = [str(item) if item is not None else "Chưa có" for item in row]
            tree.insert("", "end", values=cleaned)


    def perform_search(self, tab_key, keyword):
        """Gọi hàm tìm kiếm tương ứng với tab và từ khóa"""
        tree_map = {
            "bn": self.tree_bn,
            "bs": self.tree_bs if hasattr(self, 'tree_bs') else None,
            "yt": self.tree_yt,
            "th": self.tree_th,
            "lk": self.tree_lk,
            "my_pats": self.tree_my_pats
        }
        tree = tree_map.get(tab_key)
        if not tree:
            return

        keyword = keyword.strip()
        if keyword == "":
            # Nếu từ khóa rỗng -> load lại toàn bộ dữ liệu
            if tab_key == "my_pats":
                self.load_my_patients()
            else:
                self.load_all_data()
            return

        # Xóa dữ liệu cũ
        tree.delete(*tree.get_children())

        try:
            if tab_key == "bn":
                self.search_benhnhan(tree, keyword)
            elif tab_key == "bs" and self.role == "Admin":
                self.search_bacsi(tree, keyword)
            elif tab_key == "yt":
                self.search_yta(tree, keyword)
            elif tab_key == "th":
                self.search_thuoc(tree, keyword)
            elif tab_key == "lk":
                self.search_luotkham(tree, keyword)
            elif tab_key == "my_pats":
                self.search_hoso_dieutri(tree, keyword)
        except Exception as e:
            messagebox.showerror("Lỗi tìm kiếm", str(e))


    cursor.execute("SELECT tenbenhnhan from benhnhan inner join luotkham on benhnhan.mabenhnhan=luotkham.mabenhnhan WHERE YEAR(CURDATE()) - birth < 30 and diachi = 'Ha Noi' and  trangthai = 'Dang dieu tri' ")
    print(cursor.fetchall())
# --- DOANH THU & LƯƠNG (GIAO DIỆN ĐẸP HƠN) ---
class RevenueWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master); self.master = master
        self.title("Doanh Thu"); self.geometry("550x600")
        self.grab_set()
        ctk.CTkLabel(self, text="📊 BÁO CÁO DOANH THU", font=FONTS["h2"], text_color=COLORS["primary"]).pack(pady=30)
        container = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        container.pack(padx=40, pady=10, fill="both", expand=True)
        cursor.execute("SELECT tongtien FROM luotkham")
        phi_dv = sum(float(row[0]) for row in cursor.fetchall() if row[0])
        tien_thuoc = 0
        cursor.execute("SELECT thuoc.gianhap, thuoc.giaban, donthuoc.soluong FROM donthuoc INNER JOIN thuoc ON thuoc.mathuoc = donthuoc.mathuoc")
        for row in cursor.fetchall():
            try: tien_thuoc += int(row[2]) * (float(row[1]) - float(row[0]))
            except: continue
        cursor.execute("SELECT salary, mabsi FROM bsi"); ds_bs = cursor.fetchall()
        cursor.execute("SELECT mabsi FROM luotkham"); lk_bs = [str(r[0]) for r in cursor.fetchall()]
        tong_luong_bs = sum(int(b[0]) + (lk_bs.count(str(b[1])) * 500000) for b in ds_bs)
        cursor.execute("SELECT salary, mayta FROM yta"); ds_yt = cursor.fetchall()
        cursor.execute("SELECT mayta FROM luotkham_yta"); lk_yt = [str(r[0]) for r in cursor.fetchall()]
        tong_luong_yt = sum(int(y[0]) + (lk_yt.count(str(y[1])) * 200000) for y in ds_yt)
        tong_chi_phi_luong = tong_luong_bs + tong_luong_yt
        tong_dt = phi_dv + tien_thuoc - tong_chi_phi_luong
        self.row(container, "Doanh thu dịch vụ:", f"{phi_dv:,.0f} VNĐ")
        self.row(container, "Lợi nhuận thuốc:", f"{int(tien_thuoc):,} VNĐ")
        self.row(container, "Tổng lương nhân viên (-):", f"{tong_chi_phi_luong:,.0f} VNĐ")
        ctk.CTkLabel(container, text=f"TỔNG: {int(tong_dt):,} VNĐ", font=("Inter", 22, "bold"), text_color=COLORS["success"]).pack(pady=30)

    def row(self, p, l, v):
        f = ctk.CTkFrame(p, fg_color="transparent"); f.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(f, text=l, font=FONTS["body"]).pack(side="left")
        ctk.CTkLabel(f, text=v, font=("Inter", 14, "bold")).pack(side="right")

class SalaryWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master); self.master = master
        self.title("Bảng Lương"); self.geometry("950x650")
        self.grab_set()
        tab = ctk.CTkTabview(self); tab.pack(padx=20, pady=20, fill="both", expand=True)
        self.t_bs = self.create_t(tab.add("👨‍⚕️ Bác Sĩ"), ("Mã BS", "Tên", "Lương Cứng", "Tổng Thu Nhập"))
        self.t_yt = self.create_t(tab.add("👩‍⚕️ Y Tá"), ("Mã YT", "Tên", "Lương Cứng", "Tổng Thu Nhập"))
        self.refresh_salary_data()
    #load luong bac si va y ta
    def refresh_salary_data(self):
        for row in self.t_bs.get_children(): self.t_bs.delete(row)
        for row in self.t_yt.get_children(): self.t_yt.delete(row)
        cursor.execute("SELECT mabsi FROM luotkham"); lk_bs = [str(r[0]) for r in cursor.fetchall()]
        cursor.execute("SELECT mayta FROM luotkham_yta"); lk_yt = [str(r[0]) for r in cursor.fetchall()]
        for item in self.master.tree_bs.get_children():
            v = self.master.tree_bs.item(item, "values"); ma, ten, cung = str(v[0]), v[2], int(v[8])
            tong = cung + (lk_bs.count(ma) * 500000)
            self.t_bs.insert("", "end", values=(ma, ten, f"{cung:,}", f"{tong:,}"))
        for item in self.master.tree_yt.get_children():
            v = self.master.tree_yt.item(item, "values"); ma, ten, cung = str(v[0]), v[2], int(v[7])
            tong = cung + (lk_yt.count(ma) * 200000)
            self.t_yt.insert("", "end", values=(ma, ten, f"{cung:,}", f"{tong:,}"))

    def create_t(self, p, cols):
        t = ttk.Treeview(p, columns=cols, show="headings")
        for c in cols: t.heading(c, text=c); t.column(c, width=130, anchor="center")
        t.pack(fill="both", expand=True)
        return t

# --- ĐĂNG NHẬP (NÂNG CẤP) ---
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SUS Login")
        self.geometry("520x760")
        self.configure(fg_color=COLORS["bg_light"])
        self.role_var = ctk.StringVar(value="Doctor")

        header_banner = ctk.CTkFrame(self, height=200, fg_color=COLORS["primary"], corner_radius=0)
        header_banner.pack(fill="x")
        ctk.CTkLabel(header_banner, text="✚", font=("Arial", 70), text_color="white").place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(header_banner, text="HỆ THỐNG Y TẾ CLINIC HUB", font=FONTS["h3"], text_color="white").place(relx=0.5, rely=0.8, anchor="center")

        content = ctk.CTkFrame(self, fg_color="white", corner_radius=30, border_width=1, border_color=COLORS["border"])
        content.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(content, text="Đăng nhập hệ thống", font=FONTS["h2"], text_color=COLORS["text_main"]).pack(pady=(35, 10))
        ctk.CTkLabel(content, text="Vui lòng chọn vai trò và nhập thông tin", font=FONTS["body"], text_color=COLORS["text_sub"]).pack()

        role_frame = ctk.CTkFrame(content, fg_color="#F1F5F9", corner_radius=14)
        role_frame.pack(pady=20, padx=30, fill="x")
        self.btn_admin = ctk.CTkButton(role_frame, text="QUẢN TRỊ", fg_color="transparent",
                                       text_color=COLORS["text_main"], hover_color="#E2E8F0", height=50, corner_radius=12,
                                       command=lambda: self.set_r("Admin"))
        self.btn_admin.pack(side="left", expand=True, padx=5, pady=5)
        self.btn_doc = ctk.CTkButton(role_frame, text="BÁC SĨ", fg_color=COLORS["primary"], text_color="white",
                                     hover_color=COLORS["primary_hover"], height=50, corner_radius=12,
                                     command=lambda: self.set_r("Doctor"))
        self.btn_doc.pack(side="left", expand=True, padx=5, pady=5)

        self.u = ctk.CTkEntry(content, placeholder_text="Tên đăng nhập / CCCD bác sĩ", height=56, corner_radius=12,
                              border_color=COLORS["border"])
        self.u.pack(pady=10, padx=30, fill="x")
        self.p = ctk.CTkEntry(content, placeholder_text="Mật khẩu", show="*", height=56, corner_radius=12,
                              border_color=COLORS["border"])
        self.p.pack(pady=10, padx=30, fill="x")

        ctk.CTkButton(content, text="ĐĂNG NHẬP NGAY", fg_color=COLORS["success"], hover_color=COLORS["success_hover"],
                      height=65, font=FONTS["button"], corner_radius=16, command=self.login).pack(pady=40, padx=30, fill="x")

    def set_r(self, r):
        self.role_var.set(r)
        if r == "Admin":
            self.btn_admin.configure(fg_color=COLORS["primary"], text_color="white")
            self.btn_doc.configure(fg_color="transparent", text_color=COLORS["text_main"])
        else:
            self.btn_doc.configure(fg_color=COLORS["primary"], text_color="white")
            self.btn_admin.configure(fg_color="transparent", text_color=COLORS["text_main"])
    #dang nhap lay cccd va sdt cua bsi tu db len lam mkhau
    def login(self):
        u, p, r = self.u.get().strip(), self.p.get().strip(), self.role_var.get()
        if r == "Admin" and u == "1" and p == "1":
            self.withdraw(); MainApp(self, "Admin").deiconify()
        elif r == "Doctor":
            cursor.execute("SELECT mabsi FROM bsi WHERE cmt=%s AND sdt=%s", (u, p))
            row = cursor.fetchone()
            if row:
                self.withdraw(); MainApp(self, "Doctor", row[0]).deiconify()
            else:
                messagebox.showerror("Lỗi", "Tài khoản bác sĩ không chính xác!")
        else:
            messagebox.showerror("Lỗi", "Thông tin không chính xác!")

if __name__ == "__main__":
    LoginApp().mainloop()