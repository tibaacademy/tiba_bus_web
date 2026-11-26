import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="TIBA Language Academy", layout="wide", initial_sidebar_state="collapsed")

with open("style.css", encoding="utf-8") as f:
    st.markdown("<style>" + f.read() + "</style>", unsafe_allow_html=True)

@st.cache_resource
def init_connection() -> Client:
    url = "https://mpxpysulrjcpqgrbrpah.supabase.co"
    key = "sb_publishable_F4BMccrJCjHVo9vyD_pRkw_yvKdIajE"
    return create_client(url, key)

supabase = init_connection()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "كشوف الباصات"

def log_action(action_type: str, details: str):
    u_name = st.session_state.user_info["full_name"] if st.session_state.user_info else "System"
    try:
        supabase.table("action_logs").insert({"action": f"[{u_name}] {action_type}", "details": details}).execute()
    except Exception:
        pass

if not st.session_state.logged_in:
    st.markdown("<div style='height:45px;'></div>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.3, 1])
    with center_col:
        st.markdown("<div class='top-navbar' style='flex-direction:column;text-align:center;padding:28px;'><h1>TIBA LANGUAGE ACADEMY</h1><p>بوابة إدارة النقل المدرسي والحافلات</p></div>", unsafe_allow_html=True)
        with st.form("login_box"):
            st.markdown("#### تسجيل الدخول للنظام")
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            submitted = st.form_submit_button("دخول للوحة التحكم", use_container_width=True, type="primary")
            if submitted:
                if username and password:
                    res = supabase.table("app_users").select("*").eq("username", username.strip()).eq("password", password.strip()).execute()
                    if res.data:
                        st.session_state.logged_in = True
                        st.session_state.user_info = res.data[0]
                        st.rerun()
                    else:
                        st.error("بيانات الدخول غير صحيحة.")
                else:
                    st.warning("يرجى إدخال اسم المستخدم وكلمة المرور.")
    st.stop()

user = st.session_state.user_info
header_html = (
    "<div class='top-navbar'>"
    "<div><h1>TIBA LANGUAGE ACADEMY — Transportation Portal</h1>"
    "<p>نظام إدارة خطوط السير وتسكين الطلاب والمشرفات</p></div>"
    "<div style='display:flex;gap:10px;align-items:center;'>"
    f"<span class='user-badge'>المستخدم: <b>{user['full_name']}</b></span>"
    f"<span class='user-badge'>{datetime.now().strftime('%Y-%m-%d')}</span>"
    "</div></div>"
)
st.markdown(header_html, unsafe_allow_html=True)

ctrl_c1, ctrl_c2, ctrl_c3 = st.columns([2.5, 5.5, 2])
with ctrl_c1:
    shift = st.selectbox("المرحلة", ["KG", "Junior", "Middle", "Senior"], label_visibility="collapsed")
with ctrl_c2:
    st.markdown(f"<div style='padding-top:8px;font-weight:700;'>المرحلة النشطة: <span style='color:#d97706;'>{shift}</span></div>", unsafe_allow_html=True)
with ctrl_c3:
    if st.button("تسجيل خروج", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.rerun()

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

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

def get_buses(s_val):
    return supabase.table("buses").select("*").eq("shift", s_val).eq("archived", False).order("number").execute().data

def get_students(s_val):
    return supabase.table("students").select("*").eq("shift", s_val).eq("archived", False).order("name").execute().data

tab = st.session_state.active_tab

if tab == "كشوف الباصات":
    buses = get_buses(shift)
    students = get_students(shift)
    total_cap = sum(int(b.get("capacity") or 14) for b in buses)
    assigned_count = sum(1 for s in students if s.get("bus_id"))

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"<div class='kpi-card'><div class='kpi-title'>المرحلة الدراسية</div><div class='kpi-value'>{shift}</div></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-card'><div class='kpi-title'>الباصات النشطة</div><div class='kpi-value'>{len(buses)}</div></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-card'><div class='kpi-title'>الطلاب المسكنين</div><div class='kpi-value'>{assigned_count} / {len(students)}</div></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-card'><div class='kpi-title'>المقاعد المتاحة</div><div class='kpi-value'>{max(0, total_cap - assigned_count)} مقعد</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    if not buses:
        st.info("لا توجد باصات مسجلة في هذه المرحلة.")
    else:
        f_col1, f_col2 = st.columns([3, 1])
        with f_col1:
            bus_filter = st.selectbox("تصفية الباص", ["عرض جميع الباصات"] + [f"باص رقم ({b['number']}) — {b.get('route', '')}" for b in buses], label_visibility="collapsed")
        with f_col2:
            if st.button("طباعة الكشف المعروض", use_container_width=True, type="primary"):
                components.html("<script>window.parent.print();</script>", height=0)

        for bus in buses:
            label = f"باص رقم ({bus['number']}) — {bus.get('route', '')}"
            if bus_filter != "عرض جميع الباصات" and bus_filter != label:
                continue
            b_students = [s for s in students if s.get("bus_id") == bus["id"]]
            cap = int(bus.get("capacity") or 14)
            bus_html = (
                "<div class='bus-card'><div class='bus-card-header'>"
                f"<div class='bus-title'>باص رقم ({bus['number']}) | خط السير: {bus.get('route', '-')}</div>"
                f"<div class='bus-meta'>السائق: {bus.get('driver_name', '-')} ({bus.get('driver_phone', '-')}) | اللوحة: {bus.get('plate', '-')} | الإشغال: {len(b_students)} / {cap}</div>"
                "</div></div>"
            )
            st.markdown(bus_html, unsafe_allow_html=True)
            if b_students:
                df = pd.DataFrame(b_students)[["name", "grade", "detailed_address", "father_phone", "mother_phone", "notes"]]
                df.index = range(1, len(df) + 1)
                df.columns = ["اسم الطالب", "الصف", "العنوان التفصيلي", "هاتف الأب", "هاتف الأم", "ملاحظات"]
                st.table(df)
            else:
                st.caption("لا يوجد طلبة مسكنين على هذا الباص حالياً.")

elif tab == "تسكين ونقل الطلبة":
    buses = get_buses(shift)
    students = get_students(shift)
    if not students or not buses:
        st.warning("يرجى تسجيل الباصات والطلبة أولاً.")
    else:
        with st.form("assign_form"):
            st.markdown(f"#### تسكين أو نقل طالب ({shift})")
            c1, c2 = st.columns(2)
            bus_map = {f"باص ({b['number']}) — {b.get('route', '')}": b["id"] for b in buses}
            bus_map["إلغاء التسكين (بدون باص)"] = None
            stu_map = {f"{s['name']} — ({s.get('grade', '-')})": s for s in students}
            sel_stu = stu_map[c1.selectbox("اختر الطالب", list(stu_map.keys()))]
            sel_bus_label = c2.selectbox("اختر الباص المستهدف", list(bus_map.keys()))
            if st.form_submit_button("حفظ وتحديث التسكين", type="primary"):
                supabase.table("students").update({"bus_id": bus_map[sel_bus_label]}).eq("id", sel_stu["id"]).execute()
                log_action("تسكين طالب", f"نقل {sel_stu['name']} إلى {sel_bus_label}")
                st.success("تم التحديث بنجاح.")
                st.rerun()

elif tab == "إدارة الباصات":
    with st.form("add_bus_form"):
        st.markdown(f"#### إضافة باص جديد ({shift})")
        c1, c2, c3 = st.columns(3)
        num = c1.text_input("رقم الباص *")
        route = c2.text_input("خط السير *")
        b_type = c3.selectbox("نوع المركبة", ["ميكروباص", "ميني باص", "أتوبيس", "هاي إيس"])
        cap = c1.number_input("السعة", min_value=1, max_value=60, value=14)
        d_name = c2.text_input("اسم السائق")
        d_phone = c3.text_input("هاتف السائق")
        plate = c1.text_input("رقم اللوحة (اختياري)")
        if st.form_submit_button("إضافة الباص", type="primary") and num:
            supabase.table("buses").insert({
                "number": num, "route": route, "type": b_type, "capacity": cap,
                "driver_name": d_name, "driver_phone": d_phone, "plate": plate, "shift": shift
            }).execute()
            log_action("إضافة باص", f"إضافة باص {num}")
            st.success("تم تسجيل الباص.")
            st.rerun()

elif tab == "قاعدة بيانات الطلبة":
    buses = get_buses(shift)
    bus_opts = {"بدون باص حالياً": None}
    bus_opts.update({f"باص ({b['number']}) — {b.get('route', '')}": b["id"] for b in buses})
    with st.form("add_student_form"):
        st.markdown(f"#### تسجيل طالب جديد ({shift})")
        c1, c2, c3 = st.columns(3)
        s_name = c1.text_input("اسم الطالب *")
        s_grade = c2.text_input("الصف / الفصل")
        s_bus = c3.selectbox("الباص المخصص", list(bus_opts.keys()))
        s_addr = c1.text_input("العنوان التفصيلي")
        f_phone = c2.text_input("هاتف الأب")
        m_phone = c3.text_input("هاتف الأم")
        notes = st.text_input("ملاحظات")
        if st.form_submit_button("حفظ الطالب", type="primary") and s_name:
            supabase.table("students").insert({
                "name": s_name, "grade": s_grade, "detailed_address": s_addr,
                "father_phone": f_phone, "mother_phone": m_phone,
                "bus_id": bus_opts[s_bus], "notes": notes, "shift": shift
            }).execute()
            log_action("إضافة طالب", f"تسجيل {s_name}")
            st.success("تم تسجيل الطالب.")
            st.rerun()

elif tab == "المشرفات والمدرسين":
    buses = get_buses(shift)
    b_opts = {"بدون باص": None}
    b_opts.update({f"باص ({b['number']})": b["id"] for b in buses})
    col_s, col_t = st.columns(2)
    with col_s:
        with st.form("sup_form"):
            st.markdown("#### إضافة مشرفة")
            name = st.text_input("اسم المشرفة *")
            phone = st.text_input("الهاتف")
            bus = st.selectbox("الباص", list(b_opts.keys()), key="sb")
            if st.form_submit_button("حفظ المشرفة", type="primary") and name:
                supabase.table("supervisors").insert({"name": name, "phone": phone, "bus_id": b_opts[bus], "shift": shift}).execute()
                st.rerun()
        sups = supabase.table("supervisors").select("*").eq("shift", shift).eq("archived", False).execute().data
        if sups:
            st.table(pd.DataFrame(sups)[["name", "phone"]].rename(columns={"name": "الاسم", "phone": "الهاتف"}))
    with col_t:
        with st.form("tch_form"):
            st.markdown("#### إضافة مدرس")
            name = st.text_input("اسم المدرس *")
            phone = st.text_input("الهاتف")
            addr = st.text_input("العنوان (اختياري)")
            bus = st.selectbox("الباص", list(b_opts.keys()), key="tb")
            if st.form_submit_button("حفظ المدرس", type="primary") and name:
                supabase.table("teachers").insert({"name": name, "phone": phone, "address": addr, "bus_id": b_opts[bus], "shift": shift}).execute()
                st.rerun()
        tchs = supabase.table("teachers").select("*").eq("shift", shift).eq("archived", False).execute().data
        if tchs:
            st.table(pd.DataFrame(tchs)[["name", "phone", "address"]].rename(columns={"name": "الاسم", "phone": "الهاتف", "address": "العنوان"}))

elif tab == "سجل المتابعة":
    logs = supabase.table("action_logs").select("*").order("id", desc=True).limit(100).execute().data
    if logs:
        df_logs = pd.DataFrame(logs)[["created_at", "action", "details"]]
        df_logs.columns = ["التوقيت", "العملية والمستخدم", "التفاصيل"]
        st.table(df_logs)
    else:
        st.info("لا توجد حركات مسجلة.")

elif tab == "إدارة المستخدمين" and user.get("role") == "admin":
    with st.form("new_user_form"):
        st.markdown("#### إنشاء حساب جديد")
        c1, c2, c3, c4 = st.columns(4)
        u_full = c1.text_input("الاسم بالكامل *")
        u_name = c2.text_input("اسم المستخدم *")
        u_pass = c3.text_input("كلمة المرور *")
        u_role = c4.selectbox("الصلاحية", ["staff", "admin"])
        if st.form_submit_button("إنشاء الحساب", type="primary") and u_full and u_name and u_pass:
            supabase.table("app_users").insert({
                "full_name": u_full, "username": u_name.strip(), "password": u_pass.strip(), "role": u_role
            }).execute()
            st.success("تم إنشاء الحساب.")
            st.rerun()
    users_list = supabase.table("app_users").select("id, full_name, username, role").execute().data
    if users_list:
        st.table(pd.DataFrame(users_list).rename(columns={"id": "م", "full_name": "الاسم", "username": "اسم المستخدم", "role": "الصلاحية"}))
