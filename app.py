import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# 1. إعداد الصفحة
st.set_page_config(
    page_title="TIBA Language Academy | Transportation System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. الاتصال بقاعدة البيانات
@st.cache_resource
def init_connection() -> Client:
    url = "https://mpxpysulrjcpqgrbrpah.supabase.co"
    key = "sb_publishable_F4BMccrJCjHVo9vyD_pRkw_yvKdIajE"
    return create_client(url, key)

supabase = init_connection()

# 3. تهيئة متغيرات الجلسة
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "كشوف الباصات"

# 4. تصميم CSS احترافي يحاكي مواقع الويب الحديثة
def inject_modern_ui():
    dark = st.session_state.dark_mode
    bg_main = "#0b1120" if dark else "#f1f5f9"
    surface = "#1e293b" if dark else "#ffffff"
    surface_alt = "#0f172a" if dark else "#f8fafc"
    text_primary = "#f8fafc" if dark else "#0f172a"
    text_secondary = "#94a3b8" if dark else "#475569"
    border_col = "#334155" if dark else "#e2e8f0"
    brand_primary = "#1e3a8a"
    brand_accent = "#d97706"

    css = (
        f"<style>"
        f"@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');"
        f"html, body, [class*='css'] {{ font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; }}"
        f".stApp {{ background-color: {bg_main}; color: {text_primary}; }}"
        f"#MainMenu, footer, header[data-testid='stHeader'] {{ visibility: hidden; height: 0; }}"
        f"section[data-testid='stSidebar'] {{ display: none !important; }}"
        f".block-container {{ padding-top: 1.2rem !important; padding-bottom: 2rem !important; max-width: 1380px !important; }}"
        
        /* شريط الترويسة العلوي */
        f".top-navbar {{ background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); color: #ffffff; padding: 18px 28px; border-radius: 12px; border-bottom: 4px solid {brand_accent}; box-shadow: 0 4px 20px rgba(0,0,0,0.12); display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }}"
        f".top-navbar h1 {{ margin: 0; font-size: 22px; font-weight: 800; color: #ffffff; }}"
        f".top-navbar p {{ margin: 2px 0 0 0; font-size: 13px; color: #cbd5e1; }}"
        f".user-badge {{ background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 20px; font-size: 13px; color: #f8fafc; }}"

        /* بطاقات الإحصائيات */
        f".kpi-card {{ background-color: {surface}; border: 1px solid {border_col}; border-top: 4px solid {brand_primary}; border-radius: 10px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: transform 0.2s ease; }}"
        f".kpi-card:hover {{ transform: translateY(-2px); }}"
        f".kpi-title {{ font-size: 13px; color: {text_secondary}; font-weight: 600; margin-bottom: 4px; }}"
        f".kpi-value {{ font-size: 26px; font-weight: 800; color: {text_primary}; }}"

        /* بطاقة كل باص */
        f".bus-card {{ background-color: {surface}; border: 1px solid {border_col}; border-radius: 12px; overflow: hidden; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}"
        f".bus-card-header {{ background-color: {surface_alt}; border-bottom: 1px solid {border_col}; padding: 14px 20px; display: flex; justify-content: space-between; align-items: center; }}"
        f".bus-title {{ font-size: 17px; font-weight: 800; color: {brand_primary if not dark else '#60a5fa'}; }}"
        f".bus-meta {{ font-size: 13px; color: {text_secondary}; font-weight: 600; }}"

        /* الأزرار والحقول */
        f"div.stButton > button {{ border-radius: 8px !important; font-weight: 700 !important; border: 1px solid {border_col} !important; transition: all 0.2s ease !important; padding: 0.45rem 1rem !important; }}"
        f"div.stButton > button:hover {{ border-color: {brand_accent} !important; transform: translateY(-1px); }}"
        f"div[data-testid='stForm'] {{ background-color: {surface}; border: 1px solid {border_col}; border-radius: 12px; padding: 22px; box-shadow: 0 2px 10px rgba(0,0,0,0.04); }}"

        /* الجداول */
        f"table {{ width: 100%; border-collapse: collapse; background-color: {surface}; }}"
        f"th {{ background-color: #1e3a8a !important; color: #ffffff !important; font-weight: 700 !important; padding: 11px 14px !important; text-align: right !important; font-size: 13px !important; }}"
        f"td {{ padding: 10px 14px !important; border-bottom: 1px solid {border_col} !important; color: {text_primary} !important; font-weight: 600 !important; font-size: 13px !important; }}"
        f"tr:hover td {{ background-color: {surface_alt} !important; }}"

        /* تنسيق الطباعة */
        f"@media print {{ @page {{ size: landscape; margin: 10mm; }} .no-print, div.stButton, div[data-testid='stSelectbox'], .top-navbar {{ display: none !important; }} .stApp {{ background: #ffffff !important; color: #000000 !important; }} .bus-card {{ box-shadow: none !important; border: 1px solid #000 !important; page-break-inside: avoid; }} }}"
        f"</style>"
    )
    st.markdown(css, unsafe_allow_html=True)

inject_modern_ui()

def log_action(action_type: str, details: str):
    user_name = st.session_state.user_info["full_name"] if st.session_state.user_info else "System"
    try:
        supabase.table("action_logs").insert({"action": f"[{user_name}] {action_type}", "details": details}).execute()
    except Exception:
        pass

# ==========================================
# بوابة تسجيل الدخول الحديثة
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.3, 1])
    with center_col:
        st.markdown(
            "<div class='top-navbar' style='flex-direction: column; text-align: center; padding: 28px;'>"
            "<h1 style='font-size: 24px;'>TIBA LANGUAGE ACADEMY</h1>"
            "<p style='font-size: 14px; margin-top: 6px;'>بوابة إدارة النقل المدرسي والحافلات</p>"
            "</div>",
            unsafe_allow_html=True
        )
        with st.form("login_box"):
            st.markdown("#### تسجيل الدخول للنظام")
            username = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم...")
            password = st.text_input("كلمة المرور", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("دخول للوحة التحكم", use_container_width=True, type="primary")
            if submitted:
                if username and password:
                    res = supabase.table("app_users").select("*").eq("username", username.strip()).eq("password", password.strip()).execute()
                    if res.data:
                        st.session_state.logged_in = True
                        st.session_state.user_info = res.data[0]
                        st.rerun()
                    else:
                        st.error("بيانات الدخول غير صحيحة، يرجى التحقق والمحاولة مرة أخرى.")
                else:
                    st.warning("يرجى إدخال اسم المستخدم وكلمة المرور.")
    st.stop()

# ==========================================
# الترويسة العلوية وشريط التنقل (Top Navigation)
# ==========================================
user = st.session_state.user_info
st.markdown(
    f"<div class='top-navbar'>"
    f"<div><h1>TIBA LANGUAGE ACADEMY — Transportation Portal</h1>"
    f"<p>نظام إدارة خطوط السير وتسكين الطلاب والمشرفات</p></div>"
    f"<div style='display:flex; gap:10px; align-items:center;'>"
    f"<span class='user-badge'>المستخدم: <b>{user['full_name']}</b></span>"
    f"<span class='user-badge'>{datetime.now().strftime('%Y-%m-%d')}</span>"
    f"</div></div>",
    unsafe_allow_html=True
)

# شريط التحكم العلوي (اختيار المرحلة + المظهر + الخروج)
ctrl_c1, ctrl_c2, ctrl_c3, ctrl_c4 = st.columns([2.2, 4.8, 1.5, 1.5])
with ctrl_c1:
    shift = st.selectbox("المرحلة الدراسية (Shift):", ["KG", "Junior", "Middle", "Senior"], label_visibility="collapsed")
with ctrl_c2:
    st.markdown(f"<div style='padding-top:8px; font-weight:700; font-size:15px;'>المرحلة النشطة حالياً: <span style='color:#d97706;'>{shift}</span></div>", unsafe_allow_html=True)
with ctrl_c3:
    mode_txt = "الوضع النهاري" if st.session_state.dark_mode else "الوضع الليلي"
    if st.button(mode_txt, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
with ctrl_c4:
    if st.button("تسجيل خروج", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.rerun()

# أزرار التنقل الرئيسية كشريط موقع ويب (Navigation Tabs)
nav_options = ["كشوف الباصات", "تسكين ونقل الطلبة", "إدارة الباصات", "قاعدة بيانات الطلبة", "المشرفات والمدرسين", "سجل المتابعة"]
if user.get("role") == "admin":
    nav_options.append("إدارة المستخدمين")

nav_cols = st.columns(len(nav_options))
for idx, label in enumerate(nav_options):
    with nav_cols[idx]:
        btn_type = "primary" if st.session_state.active_tab == label else "secondary"
        if st.button(label, key=f"nav_{idx}", use_container_width=True, type=btn_type):
            st.session_state.active_tab = label
            st.rerun()

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# دوال جلب البيانات
def get_buses(s_val):
    return supabase.table("buses").select("*").eq("shift", s_val).eq("archived", False).order("number").execute().data

def get_students(s_val):
    return supabase.table("students").select("*").eq("shift", s_val).eq("archived", False).order("name").execute().data

tab = st.session_state.active_tab

# ==========================================
# 1. كشوف الباصات والطباعة
# ==========================================
if tab == "كشوف الباصات":
    buses = get_buses(shift)
    students = get_students(shift)
    total_cap = sum(int(b.get("capacity") or 14) for b in buses)
    assigned_count = sum(1 for s in students if s.get("bus_id"))

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"<div class='kpi-card'><div class='kpi-title'>المرحلة الدراسية</div><div class='kpi-value'>{shift}</div></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-card'><div class='kpi-title'>الباصات النشطة</div><div class='kpi-value'>{len(buses)}</div></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-card'><div class='kpi-title'>الطلاب المسكنين</div><div class='kpi-value'>{assigned_count} / {len(students)}</div></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-card'><div class='kpi-title'>السعة الإجمالية المتاحة</div><div class='kpi-value'>{max(0, total_cap - assigned_count)} مقعد</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    if not buses:
        st.info("لا توجد باصات مسجلة في هذه المرحلة حتى الآن. انتقل إلى تبويب 'إدارة الباصات' لإضافة أول باص.")
    else:
        f_col1, f_col2 = st.columns([3, 1])
        with f_col1:
            bus_filter = st.selectbox("تصفية حسب الباص:", ["عرض جميع الباصات"] + [f"باص رقم ({b['number']}) — {b.get('route', '')}" for b in buses], label_visibility="collapsed")
        with f_col2:
            if st.button("طباعة الكشف المعروض", use_container_width=True, type="primary"):
                components.html("<script>window.parent.print();</script>", height=0)

        for bus in buses:
            label = f"باص رقم ({bus['number']}) — {bus.get('route', '')}"
            if bus_filter != "عرض جميع الباصات" and bus_filter != label:
                continue

            b_students = [s for s in students if s.get("bus_id") == bus["id"]]
            cap = int(bus.get("capacity") or 14)

            st.markdown(
                f"<div class='bus-card'>"
                f"<div class='bus-card-header'>"
                f"<div class='bus-title'>باص رقم ({bus['number']}) | خط السير: {bus.get('route', '-')}</div>"
                f"<div class='bus-meta'>السائق: {bus.get('driver_name', '-')} ({bus.get('driver_phone', '-')}) | اللوحة: {bus.get('plate', '-')} | الإشغال: {len(b_students)} / {cap}</div>"
                f"</div></div>",
                unsafe_allow_html=True
            )

            if b_students:
                df = pd.DataFrame(b_students)[["name", "grade", "detailed_address", "father_phone", "mother_phone", "notes"]]
                df.index = range(1, len(df) + 1)
                df.columns = ["اسم الطالب", "الصف", "العنوان التفصيلي", "هاتف الأب", "هاتف الأم", "ملاحظات"]
                st.table(df)
            else:
                st.caption("لا يوجد طلبة مسكنين على هذا الباص حالياً.")

# ==========================================
# 2. تسكين ونقل الطلبة
# ==========================================
elif tab == "تسكين ونقل الطلبة":
    buses = get_buses(shift)
    students = get_students(shift)
    if not students or not buses:
        st.warning("يرجى التأكد من تسجيل الباصات والطلبة في هذه المرحلة أولاً.")
    else:
        with st.form("assign_form"):
            st.markdown(f"#### تسكين أو نقل طالب بين الباصات ({shift})")
            c1, c2 = st.columns(2)
            bus_map = {f"باص ({b['number']}) — {b.get('route', '')}": b["id"] for b in buses}
            bus_map["إلغاء التسكين (بدون باص)"] = None
            stu_map = {f"{s['name']} — ({s.get('grade', '-')})": s for s in students}

            sel_stu = stu_map[c1.selectbox("اختر الطالب", list(stu_map.keys()))]
            sel_bus_label = c2.selectbox("اختر الباص المستهدف", list(bus_map.keys()))
            if st.form_submit_button("حفظ وتحديث التسكين", type="primary"):
                supabase.table("students").update({"bus_id": bus_map[sel_bus_label]}).eq("id", sel_stu["id"]).execute()
                log_action("تسكين طالب", f"نقل الطالب {sel_stu['name']} إلى {sel_bus_label} ({shift})")
                st.success("تم تحديث تسكين الطالب بنجاح.")
                st.rerun()

# ==========================================
# 3. إدارة الباصات
# ==========================================
elif tab == "إدارة الباصات":
    with st.form("add_bus_form"):
        st.markdown(f"#### إضافة باص جديد لمرحلة ({shift})")
        c1, c2, c3 = st.columns(3)
        num = c1.text_input("رقم الباص *")
        route = c2.text_input("خط السير *")
        b_type = c3.selectbox("نوع المركبة", ["ميكروباص", "ميني باص", "أتوبيس", "هاي إيس"])
        cap = c1.number_input("السعة الاستيعابية", min_value=1, max_value=60, value=14)
        d_name = c2.text_input("اسم السائق")
        d_phone = c3.text_input("هاتف السائق")
        plate = c1.text_input("رقم اللوحة المعدنية (اختياري)")

        if st.form_submit_button("إضافة الباص للنظام", type="primary") and num:
            supabase.table("buses").insert({
                "number": num, "route": route, "type": b_type, "capacity": cap,
                "driver_name": d_name, "driver_phone": d_phone, "plate": plate, "shift": shift
            }).execute()
            log_action("إضافة باص", f"إضافة باص رقم {num} خط {route} ({shift})")
            st.success("تم تسجيل الباص بنجاح.")
            st.rerun()

# ==========================================
# 4. قاعدة بيانات الطلبة
# ==========================================
elif tab == "قاعدة بيانات الطلبة":
    buses = get_buses(shift)
    bus_opts = {"بدون باص حالياً": None}
    bus_opts.update({f"باص ({b['number']}) — {b.get('route', '')}": b["id"] for b in buses})

    with st.form("add_student_form"):
        st.markdown(f"#### تسجيل بيانات طالب جديد ({shift})")
        c1, c2, c3 = st.columns(3)
        s_name = c1.text_input("اسم الطالب بالكامل *")
        s_grade = c2.text_input("الصف / الفصل")
        s_bus = c3.selectbox("الباص المخصص", list(bus_opts.keys()))
        s_addr = c1.text_input("العنوان التفصيلي")
        f_phone = c2.text_input("هاتف ولي الأمر (الأب)")
        m_phone = c3.text_input("هاتف الأم")
        notes = st.text_input("ملاحظات إضافية")

        if st.form_submit_button("حفظ بيانات الطالب", type="primary") and s_name:
            supabase.table("students").insert({
                "name": s_name, "grade": s_grade, "detailed_address": s_addr,
                "father_phone": f_phone, "mother_phone": m_phone,
                "bus_id": bus_opts[s_bus], "notes": notes, "shift": shift
            }).execute()
            log_action("إضافة طالب", f"تسجيل الطالب {s_name} ({shift})")
            st.success("تم تسجيل الطالب بنجاح.")
            st.rerun()

# ==========================================
# 5. المشرفات والمدرسين
# ==========================================
elif tab == "المشرفات والمدرسين":
    buses = get_buses(shift)
    b_opts = {"بدون باص": None}
    b_opts.update({f"باص ({b['number']})": b["id"] for b in buses})
    col_s, col_t = st.columns(2)

    with col_s:
        with st.form("sup_form"):
            st.markdown("#### إضافة مشرفة باص")
            name = st.text_input("اسم المشرفة *")
            phone = st.text_input("رقم الهاتف")
            bus = st.selectbox("الباص المسؤول عنه", list(b_opts.keys()), key="sb")
            if st.form_submit_button("حفظ المشرفة", type="primary") and name:
                supabase.table("supervisors").insert({"name": name, "phone": phone, "bus_id": b_opts[bus], "shift": shift}).execute()
                log_action("إضافة مشرفة", f"إضافة المشرفة {name}")
                st.rerun()
        sups = supabase.table("supervisors").select("*").eq("shift", shift).eq("archived", False).execute().data
        if sups:
            st.table(pd.DataFrame(sups)[["name", "phone"]].rename(columns={"name": "الاسم", "phone": "الهاتف"}))

    with col_t:
        with st.form("tch_form"):
            st.markdown("#### إضافة مدرس / موظف")
            name = st.text_input("اسم المدرس *")
            phone = st.text_input("رقم الهاتف")
            addr = st.text_input("العنوان (اختياري)")
            bus = st.selectbox("الباص المرافق", list(b_opts.keys()), key="tb")
            if st.form_submit_button("حفظ المدرس", type="primary") and name:
                supabase.table("teachers").insert({"name": name, "phone": phone, "address": addr, "bus_id": b_opts[bus], "shift": shift}).execute()
                log_action("إضافة مدرس", f"إضافة المدرس {name}")
                st.rerun()
        tchs = supabase.table("teachers").select("*").eq("shift", shift).eq("archived", False).execute().data
        if tchs:
            st.table(pd.DataFrame(tchs)[["name", "phone", "address"]].rename(columns={"name": "الاسم", "phone": "الهاتف", "address": "العنوان"}))

# ==========================================
# 6. سجل المتابعة
# ==========================================
elif tab == "سجل المتابعة":
    logs = supabase.table("action_logs").select("*").order("id", desc=True).limit(100).execute().data
    if logs:
        df_logs = pd.DataFrame(logs)[["created_at", "action", "details"]]
        df_logs.columns = ["التوقيت", "العملية والمستخدم", "التفاصيل"]
        st.table(df_logs)
    else:
        st.info("لا توجد حركات مسجلة حتى الآن.")

# ==========================================
# 7. إدارة المستخدمين
# ==========================================
elif tab == "إدارة المستخدمين" and user.get("role") == "admin":
    with st.form("new_user_form"):
        st.markdown("#### إنشاء حساب جديد لفريق العمل")
        c1, c2, c3, c4 = st.columns(4)
        u_full = c1.text_input("الاسم بالكامل *")
        u_name = c2.text_input("اسم المستخدم *")
        u_pass = c3.text_input("كلمة المرور *")
        u_role = c4.selectbox("الصلاحية", ["staff", "admin"])
        if st.form_submit_button("إنشاء الحساب", type="primary") and u_full and u_name and u_pass:
            supabase.table("app_users").insert({
                "full_name": u_full, "username": u_name.strip(), "password": u_pass.strip(), "role": u_role
            }).execute()
            st.success(f"تم إنشاء حساب {u_full} بنجاح.")
            st.rerun()

    users_list = supabase.table("app_users").select("id, full_name, username, role").execute().data
    if users_list:
        st.table(pd.DataFrame(users_list).rename(columns={"id": "م", "full_name": "الاسم", "username": "اسم المستخدم", "role": "الصلاحية"}))
