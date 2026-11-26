<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TIBA Language Academy — Bus Management System</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Inter:wght@400;600;700&display=swap');

  :root {
    --bg-body: #f1f5f9;
    --bg-surface: #ffffff;
    --bg-subtle: #f8fafc;
    --text-main: #0f172a;
    --text-muted: #475569;
    --border-color: #cbd5e1;
    --primary: #1e3a8a;
    --primary-hover: #172554;
    --accent: #d97706;
    --header-bg: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    --row-hover: #eff6ff;
    --shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
  }

  body.dark-mode {
    --bg-body: #0b1120;
    --bg-surface: #1e293b;
    --bg-subtle: #0f172a;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --border-color: #334155;
    --primary: #2563eb;
    --primary-hover: #3b82f6;
    --accent: #f59e0b;
    --header-bg: linear-gradient(135deg, #020617 0%, #1e293b 100%);
    --row-hover: #263349;
    --shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: 'Cairo', 'Inter', sans-serif;
    background-color: var(--bg-body);
    color: var(--text-main);
    transition: background-color 0.25s, color 0.25s;
    padding: 16px;
  }

  .container {
    max-width: 1320px;
    margin: 0 auto;
  }

  /* Header */
  .app-header {
    background: var(--header-bg);
    color: #ffffff;
    padding: 18px 26px;
    border-radius: 10px;
    border-bottom: 4px solid var(--accent);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 14px;
    box-shadow: var(--shadow);
    margin-bottom: 16px;
  }

  .brand-area h1 {
    font-size: 21px;
    font-weight: 800;
    letter-spacing: 0.4px;
  }

  .brand-area p {
    font-size: 13px;
    color: #cbd5e1;
    margin-top: 2px;
  }

  .header-controls {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
  }

  .ctrl-btn, .shift-select {
    background: rgba(255, 255, 255, 0.12);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.25);
    padding: 7px 14px;
    border-radius: 6px;
    font-family: inherit;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
  }

  .shift-select option {
    background: #1e293b;
    color: #ffffff;
  }

  .ctrl-btn:hover {
    background: rgba(255, 255, 255, 0.22);
    border-color: var(--accent);
  }

  /* Navigation Tabs */
  .nav-bar {
    display: flex;
    gap: 8px;
    background: var(--bg-surface);
    padding: 8px;
    border-radius: 10px;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow);
    margin-bottom: 18px;
    overflow-x: auto;
  }

  .nav-tab {
    flex: 1;
    min-width: 130px;
    padding: 10px 14px;
    border: 1px solid transparent;
    background: transparent;
    color: var(--text-muted);
    font-family: inherit;
    font-size: 14px;
    font-weight: 700;
    border-radius: 7px;
    cursor: pointer;
    transition: all 0.2s;
    text-align: center;
  }

  .nav-tab:hover {
    background: var(--bg-subtle);
    color: var(--text-main);
    border-color: var(--border-color);
  }

  .nav-tab.active {
    background: var(--primary);
    color: #ffffff;
    box-shadow: 0 2px 6px rgba(30, 58, 138, 0.25);
  }

  /* KPI Cards */
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 14px;
    margin-bottom: 18px;
  }

  .kpi-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-inline-start: 4px solid var(--primary);
    border-radius: 8px;
    padding: 14px 18px;
    box-shadow: var(--shadow);
  }

  .kpi-card span {
    font-size: 12.5px;
    color: var(--text-muted);
    font-weight: 700;
    display: block;
  }

  .kpi-card strong {
    font-size: 24px;
    font-weight: 800;
    color: var(--text-main);
    margin-top: 4px;
    display: block;
  }

  /* Panels & Forms */
  .panel {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 20px;
    box-shadow: var(--shadow);
    margin-bottom: 18px;
  }

  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 12px;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--border-color);
    flex-wrap: wrap;
    gap: 10px;
  }

  .panel-title {
    font-size: 17px;
    font-weight: 800;
    color: var(--text-main);
  }

  .form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
    margin-bottom: 14px;
  }

  .form-group label {
    display: block;
    font-size: 12.5px;
    font-weight: 700;
    color: var(--text-muted);
    margin-bottom: 5px;
  }

  .form-control {
    width: 100%;
    padding: 9px 12px;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    background: var(--bg-subtle);
    color: var(--text-main);
    font-family: inherit;
    font-size: 13.5px;
    font-weight: 600;
  }

  .form-control:focus {
    outline: none;
    border-color: var(--primary);
  }

  .btn-primary {
    background: var(--primary);
    color: #ffffff;
    border: none;
    padding: 9px 20px;
    border-radius: 6px;
    font-family: inherit;
    font-size: 13.5px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
  }

  .btn-primary:hover {
    background: var(--primary-hover);
  }

  .btn-print {
    background: #0f766e;
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-family: inherit;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
  }

  /* Tables */
  .table-wrap {
    overflow-x: auto;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13.5px;
  }

  th {
    background: var(--primary);
    color: #ffffff;
    padding: 11px 12px;
    text-align: start;
    font-weight: 700;
    white-space: nowrap;
  }

  td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--border-color);
    font-weight: 700;
    color: var(--text-main);
  }

  tbody tr:hover {
    background: var(--row-hover);
  }

  .badge {
    padding: 3px 9px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 700;
    background: rgba(30, 58, 138, 0.12);
    color: var(--primary);
  }

  body.dark-mode .badge {
    background: rgba(59, 130, 246, 0.2);
    color: #93c5fd;
  }

  .hidden {
    display: none;
  }

  /* Print Rules: Bold clean sheets, no URL/file footers */
  @media print {
    @page { size: landscape; margin: 10mm; }
    body { background: #ffffff !important; color: #000000 !important; padding: 0; }
    .app-header, .nav-bar, .no-print, .kpi-grid { display: none !important; }
    .panel { box-shadow: none !important; border: 1px solid #000 !important; page-break-inside: avoid; }
    th { background: #1e3a8a !important; color: #ffffff !important; -webkit-print-color-adjust: exact; }
    td { color: #000000 !important; border-bottom: 1px solid #94a3b8 !important; font-weight: 800 !important; }
  }
</style>
</head>
<body>

<div class="container">
  <!-- Top Header -->
  <header class="app-header">
    <div class="brand-area">
      <h1 data-ar="TIBA LANGUAGE ACADEMY — نظام إدارة النقل المدرسي" data-en="TIBA LANGUAGE ACADEMY — Transportation Management">TIBA LANGUAGE ACADEMY — نظام إدارة النقل المدرسي</h1>
      <p data-ar="لوحة التحكم المركزية لإدارة الحافلات، الطلبة، المشرفات، وسجل المتابعة" data-en="Central Dashboard for Buses, Students, Supervisors & Audit Logs">لوحة التحكم المركزية لإدارة الحافلات، الطلبة، المشرفات، وسجل المتابعة</p>
    </div>
    <div class="header-controls">
      <select id="shiftSelect" class="shift-select" onchange="changeShift()">
        <option value="KG">المرحلة: KG</option>
        <option value="Junior" selected>المرحلة: Junior</option>
        <option value="Middle">المرحلة: Middle</option>
        <option value="Senior">المرحلة: Senior</option>
      </select>
      <button class="ctrl-btn" onclick="toggleLang()" id="langBtn">English</button>
      <button class="ctrl-btn" onclick="toggleTheme()" id="themeBtn" data-ar="الوضع الليلي" data-en="Dark Mode">الوضع الليلي</button>
    </div>
  </header>

  <!-- Navigation Bar -->
  <nav class="nav-bar">
    <button class="nav-tab active" onclick="switchTab('rosters', this)" data-ar="1. كشوف الباصات والطباعة" data-en="1. Bus Rosters & Print">1. كشوف الباصات والطباعة</button>
    <button class="nav-tab" onclick="switchTab('students', this)" data-ar="2. الطلبة والتسكين" data-en="2. Students & Assignment">2. الطلبة والتسكين</button>
    <button class="nav-tab" onclick="switchTab('buses', this)" data-ar="3. الباصات والسائقين" data-en="3. Buses & Drivers">3. الباصات والسائقين</button>
    <button class="nav-tab" onclick="switchTab('staff', this)" data-ar="4. المشرفات والمدرسين" data-en="4. Supervisors & Teachers">4. المشرفات والمدرسين</button>
    <button class="nav-tab" onclick="switchTab('logs', this)" data-ar="5. سجل الحركات (Log)" data-en="5. Action Audit Log">5. سجل الحركات (Log)</button>
  </nav>

  <!-- KPI Summary -->
  <section class="kpi-grid">
    <div class="kpi-card">
      <span data-ar="المرحلة النشطة" data-en="Active Shift">المرحلة النشطة</span>
      <strong id="kpiShift">Junior</strong>
    </div>
    <div class="kpi-card">
      <span data-ar="إجمالي الباصات" data-en="Total Buses">إجمالي الباصات</span>
      <strong id="kpiBuses">2</strong>
    </div>
    <div class="kpi-card">
      <span data-ar="الطلبة المسكنين" data-en="Assigned Students">الطلبة المسكنين</span>
      <strong id="kpiStudents">4</strong>
    </div>
    <div class="kpi-card">
      <span data-ar="المشرفات والمدرسين" data-en="Supervisors & Staff">المشرفات والمدرسين</span>
      <strong id="kpiStaff">3</strong>
    </div>
  </section>

  <!-- TAB 1: ROSTERS -->
  <div id="tab-rosters" class="tab-content">
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title" data-ar="كشوف تسكين الباصات الجاهزة للطباعة" data-en="Printable Bus Assignment Rosters">كشوف تسكين الباصات الجاهزة للطباعة</div>
        <div style="display:flex; gap:10px;" class="no-print">
          <select id="rosterBusFilter" class="form-control" style="width:220px;" onchange="renderAll()">
            <option value="ALL" data-ar="عرض جميع الباصات" data-en="Show All Buses">عرض جميع الباصات</option>
          </select>
          <button class="btn-print" onclick="window.print()" data-ar="طباعة الكشف (Landscape)" data-en="Print Sheet (Landscape)">طباعة الكشف (Landscape)</button>
        </div>
      </div>
      <div id="rostersContainer"></div>
    </div>
  </div>

  <!-- TAB 2: STUDENTS -->
  <div id="tab-students" class="tab-content hidden">
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title" data-ar="إضافة وتسكين طالب جديد" data-en="Add & Assign New Student">إضافة وتسكين طالب جديد</div>
      </div>
      <div class="form-grid">
        <div class="form-group">
          <label data-ar="اسم الطالب بالكامل" data-en="Student Full Name">اسم الطالب بالكامل</label>
          <input type="text" id="stuName" class="form-control" placeholder="مثال: حمزة أحمد محمود">
        </div>
        <div class="form-group">
          <label data-ar="الصف / الفصل" data-en="Grade / Class">الصف / الفصل</label>
          <input type="text" id="stuGrade" class="form-control" placeholder="J2 - A">
        </div>
        <div class="form-group">
          <label data-ar="العنوان التفصيلي" data-en="Detailed Address">العنوان التفصيلي</label>
          <input type="text" id="stuAddr" class="form-control" placeholder="فلمنج - شارع مصطفى كامل">
        </div>
        <div class="form-group">
          <label data-ar="هاتف ولي الأمر" data-en="Parent Phone">هاتف ولي الأمر</label>
          <input type="text" id="stuPhone" class="form-control" placeholder="01000000000">
        </div>
        <div class="form-group">
          <label data-ar="تعيين الباص (Dropdown)" data-en="Assign Bus (Dropdown)">تعيين الباص (Dropdown)</label>
          <select id="stuBusSelect" class="form-control"></select>
        </div>
      </div>
      <button class="btn-primary" onclick="addStudent()" data-ar="حفظ وتسكين الطالب" data-en="Save & Assign Student">حفظ وتسكين الطالب</button>
    </div>

    <div class="panel">
      <div class="panel-header">
        <div class="panel-title" data-ar="قائمة الطلبة وتعديل التسكين السريع" data-en="Students List & Quick Re-assignment">قائمة الطلبة وتعديل التسكين السريع</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th data-ar="اسم الطالب" data-en="Student Name">اسم الطالب</th>
              <th data-ar="الصف" data-en="Grade">الصف</th>
              <th data-ar="العنوان" data-en="Address">العنوان</th>
              <th data-ar="الهاتف" data-en="Phone">الهاتف</th>
              <th data-ar="الباص الحالي (تغيير مباشر)" data-en="Assigned Bus (Direct Change)">الباص الحالي (تغيير مباشر)</th>
            </tr>
          </thead>
          <tbody id="studentsTableBody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 3: BUSES -->
  <div id="tab-buses" class="tab-content hidden">
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title" data-ar="إضافة باص وسائق جديد" data-en="Add New Bus & Driver">إضافة باص وسائق جديد</div>
      </div>
      <div class="form-grid">
        <div class="form-group">
          <label data-ar="رقم الباص" data-en="Bus Number">رقم الباص</label>
          <input type="text" id="busNum" class="form-control" placeholder="12">
        </div>
        <div class="form-group">
          <label data-ar="خط السير" data-en="Route">خط السير</label>
          <input type="text" id="busRoute" class="form-control" placeholder="سيدي بشر - ميامي">
        </div>
        <div class="form-group">
          <label data-ar="اسم السائق" data-en="Driver Name">اسم السائق</label>
          <input type="text" id="driverName" class="form-control" placeholder="أ. محمد حسن">
        </div>
        <div class="form-group">
          <label data-ar="هاتف السائق" data-en="Driver Phone">هاتف السائق</label>
          <input type="text" id="driverPhone" class="form-control" placeholder="01200000000">
        </div>
        <div class="form-group">
          <label data-ar="رقم اللوحة (اختياري)" data-en="License Plate (Optional)">رقم اللوحة (اختياري)</label>
          <input type="text" id="busPlate" class="form-control" placeholder="س ط أ 4521">
        </div>
        <div class="form-group">
          <label data-ar="السعة" data-en="Capacity">السعة</label>
          <input type="number" id="busCap" class="form-control" value="14">
        </div>
      </div>
      <button class="btn-primary" onclick="addBus()" data-ar="إضافة الباص" data-en="Add Bus">إضافة الباص</button>
    </div>

    <div class="panel">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th data-ar="رقم الباص" data-en="Bus No.">رقم الباص</th>
              <th data-ar="خط السير" data-en="Route">خط السير</th>
              <th data-ar="السائق" data-en="Driver">السائق</th>
              <th data-ar="الهاتف" data-en="Phone">الهاتف</th>
              <th data-ar="رقم اللوحة" data-en="Plate">رقم اللوحة</th>
              <th data-ar="السعة" data-en="Capacity">السعة</th>
            </tr>
          </thead>
          <tbody id="busesTableBody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 4: STAFF (SUPERVISORS & TEACHERS) -->
  <div id="tab-staff" class="tab-content hidden">
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title" data-ar="إضافة مشرفة باص أو مدرس مرافق" data-en="Add Bus Supervisor or Teacher">إضافة مشرفة باص أو مدرس مرافق</div>
      </div>
      <div class="form-grid">
        <div class="form-group">
          <label data-ar="الصفة" data-en="Role">الصفة</label>
          <select id="staffRole" class="form-control">
            <option value="مشرفة باص">مشرفة باص (Supervisor)</option>
            <option value="مدرس / موظف">مدرس / موظف (Teacher)</option>
          </select>
        </div>
        <div class="form-group">
          <label data-ar="الاسم" data-en="Full Name">الاسم</label>
          <input type="text" id="staffName" class="form-control" placeholder="أ. رنا محمود">
        </div>
        <div class="form-group">
          <label data-ar="رقم الهاتف" data-en="Phone">رقم الهاتف</label>
          <input type="text" id="staffPhone" class="form-control" placeholder="01100000000">
        </div>
        <div class="form-group">
          <label data-ar="العنوان (اختياري)" data-en="Address (Optional)">العنوان (اختياري)</label>
          <input type="text" id="staffAddr" class="form-control" placeholder="سموحة">
        </div>
        <div class="form-group">
          <label data-ar="الباص المخصص" data-en="Assigned Bus">الباص المخصص</label>
          <select id="staffBusSelect" class="form-control"></select>
        </div>
      </div>
      <button class="btn-primary" onclick="addStaff()" data-ar="حفظ في الدليل" data-en="Save to Directory">حفظ في الدليل</button>
    </div>

    <div class="panel">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th data-ar="الصفة" data-en="Role">الصفة</th>
              <th data-ar="الاسم" data-en="Name">الاسم</th>
              <th data-ar="الهاتف" data-en="Phone">الهاتف</th>
              <th data-ar="العنوان" data-en="Address">العنوان</th>
              <th data-ar="الباص" data-en="Bus">الباص</th>
            </tr>
          </thead>
          <tbody id="staffTableBody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 5: AUDIT LOG -->
  <div id="tab-logs" class="tab-content hidden">
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title" data-ar="سجل المتابعة والعمليات الزمني (Audit Log)" data-en="Timestamped Action Audit Log">سجل المتابعة والعمليات الزمني (Audit Log)</div>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th data-ar="التاريخ والوقت" data-en="Timestamp">التاريخ والوقت</th>
              <th data-ar="المستخدم" data-en="User">المستخدم</th>
              <th data-ar="نوع الحركة" data-en="Action">نوع الحركة</th>
              <th data-ar="التفاصيل" data-en="Details">التفاصيل</th>
            </tr>
          </thead>
          <tbody id="logsTableBody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<script>
  let lang = 'ar';
  let buses = [
    { id: 1, num: '11', route: 'سيدي بشر بحري - العصافرة', driver: 'أ. محروس علي', phone: '01223456789', plate: 'س ن ر 8421', cap: 14 },
    { id: 2, num: '12', route: 'سموحة - كفر عبده - فلمنج', driver: 'أ. محمد سامي', phone: '01098765432', plate: 'س أ م 3190', cap: 16 }
  ];

  let students = [
    { id: 101, name: 'عمر خالد إبراهيم', grade: 'J2 - A', addr: 'سيدي بشر - شارع خالد بن الوليد', phone: '01011223344', busId: 1 },
    { id: 102, name: 'ليلى طارق حسن', grade: 'J1 - B', addr: 'ميامي - شارع إسكندر إبراهيم', phone: '01122334455', busId: 1 },
    { id: 103, name: 'ياسين محمود صلاح', grade: 'J3 - A', addr: 'فلمنج - شارع مصطفى كامل', phone: '01233445566', busId: 2 },
    { id: 104, name: 'فريدة عمرو سعيد', grade: 'J2 - C', addr: 'سموحة - ميدان فيكتور عمانويل', phone: '01544556677', busId: 2 }
  ];

  let staff = [
    { role: 'مشرفة باص', name: 'أ. رنا', phone: '01055667788', addr: 'سيدي بشر', busId: 1 },
    { role: 'مشرفة باص', name: 'أ. نسمة', phone: '01166778899', addr: 'فلمنج', busId: 2 },
    { role: 'مدرس / موظف', name: 'أ. عمر', phone: '01277889900', addr: 'سموحة', busId: 2 }
  ];

  let logs = [
    { time: '2026-11-26 07:45:12', user: 'Mahmoud Salah', action: 'تسكين طالب', details: 'تسكين الطالب ياسين محمود صلاح على باص رقم 12' },
    { time: '2026-11-26 07:30:05', user: 'Mahmoud Salah', action: 'إضافة باص', details: 'إضافة باص رقم 11 — خط سيدي بشر بحري' }
  ];

  function recordLog(action, details) {
    const now = new Date();
    const ts = now.getFullYear() + '-' +
      String(now.getMonth()+1).padStart(2,'0') + '-' +
      String(now.getDate()).padStart(2,'0') + ' ' +
      String(now.getHours()).padStart(2,'0') + ':' +
      String(now.getMinutes()).padStart(2,'0') + ':' +
      String(now.getSeconds()).padStart(2,'0');
    logs.unshift({ time: ts, user: 'Mahmoud Salah', action, details });
  }

  function switchTab(tabId, btn) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
    document.getElementById('tab-' + tabId).classList.remove('hidden');
    btn.classList.add('active');
  }

  function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    const btn = document.getElementById('themeBtn');
    btn.setAttribute('data-ar', isDark ? 'الوضع النهاري' : 'الوضع الليلي');
    btn.setAttribute('data-en', isDark ? 'Light Mode' : 'Dark Mode');
    btn.textContent = lang === 'ar' ? btn.getAttribute('data-ar') : btn.getAttribute('data-en');
  }

  function toggleLang() {
    lang = lang === 'ar' ? 'en' : 'ar';
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.getElementById('langBtn').textContent = lang === 'ar' ? 'English' : 'عربي';
    document.querySelectorAll('[data-ar]').forEach(el => {
      el.textContent = el.getAttribute('data-' + lang);
    });
    renderAll();
  }

  function changeShift() {
    const val = document.getElementById('shiftSelect').value;
    document.getElementById('kpiShift').textContent = val;
    recordLog('تغيير المرحلة', 'الانتقال إلى مرحلة ' + val);
    renderAll();
  }

  function addBus() {
    const num = document.getElementById('busNum').value.trim();
    const route = document.getElementById('busRoute').value.trim();
    if (!num || !route) return;
    const newBus = {
      id: Date.now(),
      num,
      route,
      driver: document.getElementById('driverName').value.trim() || '-',
      phone: document.getElementById('driverPhone').value.trim() || '-',
      plate: document.getElementById('busPlate').value.trim() || '-',
      cap: parseInt(document.getElementById('busCap').value) || 14
    };
    buses.push(newBus);
    recordLog('إضافة باص', `إضافة باص رقم ${num} (${route})`);
    document.getElementById('busNum').value = '';
    document.getElementById('busRoute').value = '';
    renderAll();
  }

  function addStudent() {
    const name = document.getElementById('stuName').value.trim();
    if (!name) return;
    const busId = parseInt(document.getElementById('stuBusSelect').value) || null;
    students.push({
      id: Date.now(),
      name,
      grade: document.getElementById('stuGrade').value.trim() || '-',
      addr: document.getElementById('stuAddr').value.trim() || '-',
      phone: document.getElementById('stuPhone').value.trim() || '-',
      busId
    });
    recordLog('إضافة طالب', `تسجيل الطالب ${name}`);
    document.getElementById('stuName').value = '';
    renderAll();
  }

  function reassignStudent(stuId, newBusId) {
    const s = students.find(x => x.id === stuId);
    if (!s) return;
    s.busId = parseInt(newBusId) || null;
    const b = buses.find(x => x.id === s.busId);
    recordLog('نقل وتسكين', `نقل ${s.name} إلى ${b ? 'باص ' + b.num : 'بدون باص'}`);
    renderAll();
  }

  function addStaff() {
    const name = document.getElementById('staffName').value.trim();
    if (!name) return;
    const role = document.getElementById('staffRole').value;
    const busId = parseInt(document.getElementById('staffBusSelect').value) || null;
    staff.push({
      role,
      name,
      phone: document.getElementById('staffPhone').value.trim() || '-',
      addr: document.getElementById('staffAddr').value.trim() || '-',
      busId
    });
    recordLog('إضافة طاقم', `إضافة ${role}: ${name}`);
    document.getElementById('staffName').value = '';
    renderAll();
  }

  function renderAll() {
    document.getElementById('kpiBuses').textContent = buses.length;
    document.getElementById('kpiStudents').textContent = students.length;
    document.getElementById('kpiStaff').textContent = staff.length;

    // Populate Bus Dropdowns
    const busOptsHtml = `<option value="">${lang === 'ar' ? 'بدون باص' : 'Unassigned'}</option>` +
      buses.map(b => `<option value="${b.id}">${lang === 'ar' ? 'باص' : 'Bus'} (${b.num}) - ${b.route}</option>`).join('');
    document.getElementById('stuBusSelect').innerHTML = busOptsHtml;
    document.getElementById('staffBusSelect').innerHTML = busOptsHtml;

    const filterSelect = document.getElementById('rosterBusFilter');
    const currentFilter = filterSelect.value;
    filterSelect.innerHTML = `<option value="ALL">${lang === 'ar' ? 'عرض جميع الباصات' : 'Show All Buses'}</option>` +
      buses.map(b => `<option value="${b.id}">${lang === 'ar' ? 'باص' : 'Bus'} (${b.num}) - ${b.route}</option>`).join('');
    filterSelect.value = currentFilter || 'ALL';

    // Render Rosters
    const rostersDiv = document.getElementById('rostersContainer');
    rostersDiv.innerHTML = buses
      .filter(b => filterSelect.value === 'ALL' || String(b.id) === filterSelect.value)
      .map(b => {
        const bStudents = students.filter(s => s.busId === b.id);
        const bSups = staff.filter(st => st.busId === b.id).map(st => st.name).join(' ، ') || '-';
        const rows = bStudents.map((s, idx) => `
          <tr>
            <td>${idx + 1}</td>
            <td>${s.name}</td>
            <td>${s.grade}</td>
            <td>${s.addr}</td>
            <td>${s.phone}</td>
          </tr>
        `).join('');

        return `
          <div style="border:1px solid var(--border-color); border-radius:8px; margin-bottom:18px; overflow:hidden;">
            <div style="background:var(--bg-subtle); padding:12px 16px; border-bottom:1px solid var(--border-color); display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;">
              <strong>${lang === 'ar' ? 'باص رقم' : 'Bus No.'} (${b.num}) | ${b.route}</strong>
              <span style="font-size:13px; color:var(--text-muted); font-weight:700;">
                ${lang === 'ar' ? 'السائق:' : 'Driver:'} ${b.driver} (${b.phone}) | ${lang === 'ar' ? 'المشرفة:' : 'Supervisor:'} ${bSups} | ${lang === 'ar' ? 'الإشغال:' : 'Occupancy:'} ${bStudents.length}/${b.cap}
              </span>
            </div>
            <div class="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th style="width:50px;">#</th>
                    <th>${lang === 'ar' ? 'اسم الطالب' : 'Student Name'}</th>
                    <th>${lang === 'ar' ? 'الصف' : 'Grade'}</th>
                    <th>${lang === 'ar' ? 'العنوان التفصيلي' : 'Detailed Address'}</th>
                    <th>${lang === 'ar' ? 'هاتف ولي الأمر' : 'Parent Phone'}</th>
                  </tr>
                </thead>
                <tbody>${rows || `<tr><td colspan="5" style="text-align:center;">${lang === 'ar' ? 'لا يوجد طلبة مسكنين' : 'No students assigned'}</td></tr>`}</tbody>
              </table>
            </div>
          </div>
        `;
      }).join('');

    // Render Students Table
    document.getElementById('studentsTableBody').innerHTML = students.map((s, i) => {
      const selectHtml = `<select class="form-control" style="padding:5px 8px;" onchange="reassignStudent(${s.id}, this.value)">
        <option value="">${lang === 'ar' ? 'بدون باص' : 'Unassigned'}</option>
        ${buses.map(b => `<option value="${b.id}" ${s.busId === b.id ? 'selected' : ''}>${lang === 'ar' ? 'باص' : 'Bus'} (${b.num}) - ${b.route}</option>`).join('')}
      </select>`;
      return `<tr><td>${i+1}</td><td>${s.name}</td><td>${s.grade}</td><td>${s.addr}</td><td>${s.phone}</td><td>${selectHtml}</td></tr>`;
    }).join('');

    // Render Buses Table
    document.getElementById('busesTableBody').innerHTML = buses.map(b => `
      <tr><td><span class="badge">${b.num}</span></td><td>${b.route}</td><td>${b.driver}</td><td>${b.phone}</td><td>${b.plate}</td><td>${b.cap}</td></tr>
    `).join('');

    // Render Staff Table
    document.getElementById('staffTableBody').innerHTML = staff.map(st => {
      const b = buses.find(x => x.id === st.busId);
      return `<tr><td><span class="badge">${st.role}</span></td><td>${st.name}</td><td>${st.phone}</td><td>${st.addr}</td><td>${b ? 'باص ' + b.num : '-'}</td></tr>`;
    }).join('');

    // Render Audit Logs
    document.getElementById('logsTableBody').innerHTML = logs.map(l => `
      <tr><td dir="ltr" style="text-align:start;">${l.time}</td><td>${l.user}</td><td><span class="badge">${l.action}</span></td><td>${l.details}</td></tr>
    `).join('');
  }

  renderAll();
</script>
</body>
</html>
