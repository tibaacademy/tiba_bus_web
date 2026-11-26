import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# 1. إعداد الصفحة
st.set_page_config(
    page_title="TIBA Language Academy - Bus Management",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. الاتصال بقاعدة البيانات مباشرة بدون كاش
def init_connection() -> Client:
    url = "https://mpxpysulrjcpqgrbrpah.supabase.co"
    key = "sb_publishable_F4BMccrJCjHVo9vyD_pRkw_yvKdIajE"
    return create_client(url, key)

supabase = init_connection()

# 3. إدارة الجلسة والمظهر (النهاري / الليلي)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# تنسيق CSS الرسمي (ألوان هادئة، ترويسة رسمية، وإخفاء عناصر Streamlit غير الضرورية عند الطباعة)
def apply_custom_css():
    bg_color = "#0f172a" if st.session_state.dark_mode else "#f8fafc"
    card_bg = "#1e293b" if st.session_state.dark_mode else "#ffffff"
    text_color = "#f1f5f9" if st.session_state.dark_mode else "#1e293b"
    border_color = "#334155" if st.session_state.dark_mode else "#cbd5e1"
    header_bg = "#1e3a8a" if not st.session_state.dark_mode else "#020617"

    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
            direction: rtl;
            text-align: right;
        }}
        .official-header {{
            background-color: {header_bg};
            color: #ffffff;
            padding: 18px 25px;
            border-radius: 6px;
            border-bottom: 4px solid #d97706;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .official-header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        .official-header p {{
            margin: 4px 0 0 0;
            font-size: 14px;
            color: #e2e8f0;
        }}
        .stat-card {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-right: 4px solid #1e3a8a;
            padding: 14px 18px;
            border-radius: 6px;
            margin-bottom: 12px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-weight: 600;
        }}
        th {{
            background-color: #1e3a8a !important;
            color: white !important;
            text-align: right !important;
            padding: 10px !important;
        }}
        td {{
            padding: 8px 10px !important;
            border-bottom: 1px solid {border_color} !important;
        }}
        @media print {{
            @page {{ size: landscape; margin: 10mm; }}
            section[data-testid="stSidebar"], header, footer, .no-print {{
                display: none !important;
            }}
            .stApp {{
                background-color: #ffffff !important;
                color: #000000 !important;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# دالة تسجيل الحركات (Audit Log)
def log_action(action_type: str, details: str):
    user_name = st.session_state.user_info["full_name"] if st.session_state.user_info else "System"
    try:
        supabase.table("action_logs").insert({
            "action": f"[{user_name}] {action_type}",
            "details": details
        }).execute()
    except Exception:
        pass

# ==========================================
# شاشة تسجيل الدخول (Login Screen)
# ==========================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div class="official-header" style="text-align: center; display: block; margin-top: 40px;">
            <h1>TIBA LANGUAGE ACADEMY</h1>
            <p>نظام إدارة النقل المدرسي والحافلات | بوابة الدخول</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم (Username)")
            password = st.text_input("كلمة المرور (Password)", type="password")
            submit = st.form_submit_button("تسجيل الدخول", use_container_width=True)
            
            if submit:
    if username and password:
        try:
            res = supabase.table("app_users").select("*").execute()
            st.write("البيانات المستلمة من قاعدة البيانات:", res.data)
            for u in res.data:
                if str(u.get("username")).strip() == username.strip() and str(u.get("password")).strip() == password.strip():
                    st.session_state.logged_in = True
                    st.session_state.user_info = u
                    st.rerun()
            st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")
        except Exception as e:
            st.error(f"تفاصيل الخطأ: {e}")
    st.stop()

# ==========================================
# الواجهة الرئيسية بعد تسجيل الدخول
# ==========================================
user = st.session_state.user_info

# الترويسة الرسمية العلوية
st.markdown(f"""
<div class="official-header">
    <div>
        <h1>TIBA LANGUAGE ACADEMY — Transportation Management</h1>
        <p>إدارة خطوط السير وتسكين الطلاب | المستخدم الحالي: <b>{user['full_name']}</b></p>
    </div>
    <div style="text-align: left;">
        <span style="background: rgba(255,255,255,0.15); padding: 6px 12px; border-radius: 4px; font-size: 13px;">
            {datetime.now().strftime("%Y-%m-%d")}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# القائمة الجانبية (Sidebar)
with st.sidebar:
    st.markdown("### لوحة التحكم")
    shift = st.selectbox("المرحلة الدراسية (Shift)", ["KG", "Junior", "Middle", "Senior"])
    
    st.divider()
    menu_items = [
        "1. كشوف الباصات والطباعة",
        "2. تسكين ونقل الطلبة",
        "3. إدارة الباصات والسائقين",
        "4. قاعدة بيانات الطلبة",
        "5. دليل المشرفات والمدرسين",
        "6. سجل المتابعة (Audit Log)"
    ]
    if user.get("role") == "admin":
        menu_items.append("7. إدارة حسابات المستخدمين")
        
    menu = st.radio("القائمة الرئيسية", menu_items)
    
    st.divider()
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        theme_label = "الوضع النهاري" if st.session_state.dark_mode else "الوضع الليلي"
        if st.button(theme_label, use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    with col_t2:
        if st.button("تسجيل خروج", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.rerun()

# دوال جلب البيانات
def get_buses(s_val):
    return supabase.table("buses").select("*").eq("shift", s_val).eq("archived", False).order("number").execute().data

def get_students(s_val):
    return supabase.table("students").select("*").eq("shift", s_val).eq("archived", False).order("name").execute().data

# ------------------------------------------
# 1. كشوف الباصات والطباعة
# ------------------------------------------
if menu == "1. كشوف الباصات والطباعة":
    buses = get_buses(shift)
    students = get_students(shift)
    
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='stat-card'><b>المرحلة:</b> {shift}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='stat-card'><b>عدد الباصات النشطة:</b> {len(buses)}</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='stat-card'><b>إجمالي الطلبة المسجلين:</b> {len(students)}</div>", unsafe_allow_html=True)

    if not buses:
        st.info("لا توجد باصات مسجلة في هذه المرحلة.")
    else:
        bus_filter = st.selectbox("اختر باص لعرض كشفه وطباعته", ["عرض جميع الباصات"] + [f"باص {b['number']} - {b.get('route', '')}" for b in buses])
        
        if st.button("طباعة الكشف المعروض (Landscape)", type="primary"):
            components.html("<script>window.parent.print();</script>", height=0)

        for bus in buses:
            label = f"باص {bus['number']} - {bus.get('route', '')}"
            if bus_filter != "عرض جميع الباصات" and bus_filter != label:
                continue
                
            b_students = [s for s in students if s.get("bus_id") == bus["id"]]
            st.markdown(f"#### باص رقم ({bus['number']}) | خط السير: {bus.get('route', '-')} | السعة: {len(b_students)}/{bus.get('capacity', 14)}")
            st.caption(f"السائق: {bus.get('driver_name', '-')} ({bus.get('driver_phone', '-')}) | رقم اللوحة: {bus.get('plate', '-')}")
            
            if b_students:
                df = pd.DataFrame(b_students)[["name", "grade", "detailed_address", "father_phone", "mother_phone", "notes"]]
                df.index = range(1, len(df) + 1)
                df.columns = ["اسم الطالب", "الصف", "العنوان التفصيلي", "هاتف الأب", "هاتف الأم", "ملاحظات"]
                st.table(df)
            else:
                st.write("لا يوجد طلبة مسكنين على هذا الباص.")
            st.divider()

# ------------------------------------------
# 2. تسكين ونقل الطلبة
# ------------------------------------------
elif menu == "2. تسكين ونقل الطلبة":
    st.subheader(f"تسكين ونقل الطلبة — مرحلة {shift}")
    buses = get_buses(shift)
    students = get_students(shift)
    
    if not students or not buses:
        st.warning("يجب تسجيل الباصات والطلبة أولاً.")
    else:
        bus_map = {f"باص {b['number']} ({b.get('route', '')})": b["id"] for b in buses}
        bus_map["بدون باص (إلغاء التسكين)"] = None
        
        stu_map = {f"{s['name']} ({s.get('grade', '-')})": s for s in students}
        sel_stu_key = st.selectbox("ابحث واختر الطالب", list(stu_map.keys()))
        sel_stu = stu_map[sel_stu_key]
        
        sel_bus_key = st.selectbox("اختر الباص الجديد", list(bus_map.keys()))
        if st.button("تأكيد وحفظ التسكين", type="primary"):
            supabase.table("students").update({"bus_id": bus_map[sel_bus_key]}).eq("id", sel_stu["id"]).execute()
            log_action("تسكين طالب", f"نقل الطالب {sel_stu['name']} إلى {sel_bus_key} ({shift})")
            st.success("تم تحديث تسكين الطالب بنجاح.")
            st.rerun()

# ------------------------------------------
# 3. إدارة الباصات والسائقين
# ------------------------------------------
elif menu == "3. إدارة الباصات والسائقين":
    st.subheader(f"إضافة باص جديد — مرحلة {shift}")
    with st.form("bus_form"):
        col1, col2 = st.columns(2)
        num = col1.text_input("رقم الباص *")
        route = col2.text_input("خط السير *")
        b_type = col1.selectbox("نوع المركبة", ["ميكروباص", "ميني باص", "أتوبيس", "هاي إيس"])
        cap = col2.number_input("السعة الاستيعابية", min_value=1, max_value=60, value=14)
        d_name = col1.text_input("اسم السائق")
        d_phone = col2.text_input("هاتف السائق")
        plate = col1.text_input("رقم اللوحة (اختياري)")
        
        if st.form_submit_button("حفظ بيانات الباص", type="primary") and num:
            supabase.table("buses").insert({
                "number": num, "route": route, "type": b_type, "capacity": cap,
                "driver_name": d_name, "driver_phone": d_phone, "plate": plate, "shift": shift
            }).execute()
            log_action("إضافة باص", f"إضافة باص رقم {num} خط {route} ({shift})")
            st.success("تم إضافة الباص بنجاح.")
            st.rerun()

# ------------------------------------------
# 4. قاعدة بيانات الطلبة
# ------------------------------------------
elif menu == "4. قاعدة بيانات الطلبة":
    st.subheader(f"تسجيل طالب جديد — مرحلة {shift}")
    buses = get_buses(shift)
    bus_opts = {"بدون باص حالياً": None}
    bus_opts.update({f"باص {b['number']} ({b.get('route', '')})": b["id"] for b in buses})
    
    with st.form("student_form"):
        col1, col2 = st.columns(2)
        s_name = col1.text_input("اسم الطالب بالكامل *")
        s_grade = col2.text_input("الصف / الفصل")
        s_addr = col1.text_input("العنوان التفصيلي")
        s_bus = col2.selectbox("الباص المخصص", list(bus_opts.keys()))
        f_phone = col1.text_input("هاتف الأب")
        m_phone = col2.text_input("هاتف الأم")
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

# ------------------------------------------
# 5. دليل المشرفات والمدرسين
# ------------------------------------------
elif menu == "5. دليل المشرفات والمدرسين":
    t1, t2 = st.tabs(["المشرفات", "المدرسين"])
    buses = get_buses(shift)
    b_opts = {"بدون باص": None}
    b_opts.update({f"باص {b['number']}": b["id"] for b in buses})
    
    with t1:
        with st.form("sup_form"):
            c1, c2, c3 = st.columns(3)
            name = c1.text_input("اسم المشرفة *")
            phone = c2.text_input("الهاتف")
            bus = c3.selectbox("الباص", list(b_opts.keys()), key="sb")
            if st.form_submit_button("إضافة مشرفة") and name:
                supabase.table("supervisors").insert({"name": name, "phone": phone, "bus_id": b_opts[bus], "shift": shift}).execute()
                log_action("إضافة مشرفة", f"إضافة المشرفة {name}")
                st.rerun()
        sups = supabase.table("supervisors").select("*").eq("shift", shift).eq("archived", False).execute().data
        if sups:
            st.table(pd.DataFrame(sups)[["name", "phone"]])

    with t2:
        with st.form("tch_form"):
            c1, c2 = st.columns(2)
            name = c1.text_input("اسم المدرس *")
            phone = c2.text_input("الهاتف")
            addr = c1.text_input("العنوان (اختياري)")
            bus = c2.selectbox("الباص", list(b_opts.keys()), key="tb")
            if st.form_submit_button("إضافة مدرس") and name:
                supabase.table("teachers").insert({"name": name, "phone": phone, "address": addr, "bus_id": b_opts[bus], "shift": shift}).execute()
                log_action("إضافة مدرس", f"إضافة المدرس {name}")
                st.rerun()
        tchs = supabase.table("teachers").select("*").eq("shift", shift).eq("archived", False).execute().data
        if tchs:
            st.table(pd.DataFrame(tchs)[["name", "phone", "address"]])

# ------------------------------------------
# 6. سجل المتابعة (Audit Log)
# ------------------------------------------
elif menu == "6. سجل المتابعة (Audit Log)":
    st.subheader("سجل العمليات والتعديلات الزمني")
    logs = supabase.table("action_logs").select("*").order("id", desc=True).limit(100).execute().data
    if logs:
        df_logs = pd.DataFrame(logs)[["created_at", "action", "details"]]
        df_logs.columns = ["التوقيت", "العملية والمستخدم", "التفاصيل"]
        st.table(df_logs)
    else:
        st.info("لا توجد حركات مسجلة بعد.")

# ------------------------------------------
# 7. إدارة حسابات المستخدمين (للمدير فقط)
# ------------------------------------------
elif menu == "7. إدارة حسابات المستخدمين" and user.get("role") == "admin":
    st.subheader("إدارة حسابات فريق العمل (3 - 5 مستخدمين)")
    with st.form("new_user_form"):
        c1, c2, c3, c4 = st.columns(4)
        u_full = c1.text_input("الاسم بالكامل *")
        u_name = c2.text_input("اسم المستخدم (Username) *")
        u_pass = c3.text_input("كلمة المرور *")
        u_role = c4.selectbox("الصلاحية", ["staff", "admin"])
        if st.form_submit_button("إنشاء حساب") and u_full and u_name and u_pass:
            supabase.table("app_users").insert({
                "full_name": u_full, "username": u_name.strip(), "password": u_pass.strip(), "role": u_role
            }).execute()
            st.success(f"تم إنشاء حساب {u_full} بنجاح!")
            st.rerun()
            
    users_list = supabase.table("app_users").select("id, full_name, username, role").execute().data
    if users_list:
        st.table(pd.DataFrame(users_list))
