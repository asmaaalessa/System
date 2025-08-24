from flask import Flask, render_template, request, redirect, url_for, session, abort
import json, os, qrcode
from pathlib import Path

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "supersecretkey-please-change"  # لأي سيشن

BASE_URL = "http://127.0.0.1:5000"  # الرابط المحلي
CLIENTS_FILE = "clients.json"
QRCODES_DIR = Path("static/qrcodes")
USERNAME = "Zhor"
PASSWORD = "Zhor"

def load_clients():
    if not os.path.exists(CLIENTS_FILE):
        # إنشاء أول مرة: C001..C050 كلهم 10 خدمات
        clients = {f"C{str(i).zfill(3)}": {"services": 10} for i in range(1, 51)}
        save_clients(clients)
    with open(CLIENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_clients(clients):
    with open(CLIENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(clients, f, ensure_ascii=False, indent=2)

def ensure_qrcodes():
    clients = load_clients()
    QRCODES_DIR.mkdir(parents=True, exist_ok=True)
    for cid in clients.keys():
        img_path = QRCODES_DIR / f"{cid}.png"
        # لو الصورة موجودة خلاص
        if img_path.exists():
            continue
        url = f"{BASE_URL}/client/{cid}"
        img = qrcode.make(url)
        img.save(img_path)

@app.route("/")
def home():
    return '<h2 style="font-family:Tahoma">مرحبًا 👋</h2><p><a href="/login">دخول الموظف</a> — امسح QR العميل لزيارة /client/C001 مثلًا.</p>'

@app.route("/client/<cid>")
def client_view(cid):
    clients = load_clients()
    if cid not in clients:
        return "❌ العميل غير موجود", 404
    left = clients[cid]["services"]
    # صفحة عرض فقط—لا يوجد خصم هنا
    return render_template("client.html", cid=cid, services=left)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")
        if u == USERNAME and p == PASSWORD:
            session["user"] = USERNAME
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="❌ اسم المستخدم أو كلمة المرور غير صحيحة")
    return render_template("login.html", error="")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

def require_login():
    if "user" not in session or session["user"] != USERNAME:
        abort(403)

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    require_login()
    clients = load_clients()
    message = ""
    if request.method == "POST":
        # يقبل ID مباشر مثل C001 أو رابط كامل /client/C001
        raw = request.form.get("cid", "").strip()
        count = int(request.form.get("count", "1") or "1")
        if count < 1:
            count = 1

        # استخراج الـ ID لو كان رابط
        cid = raw.upper()
        if "/CLIENT/" in cid:
            cid = cid.split("/CLIENT/")[-1]
        cid = cid.strip()

        if cid in clients:
            before = clients[cid]["services"]
            after = max(0, before - count)
            clients[cid]["services"] = after
            save_clients(clients)
            message = f"✅ تم خصم {count} — {cid}: من {before} إلى {after}"
        else:
            message = "❌ العميل غير موجود"

    # نعرض لستة مبسطة
    items = sorted(clients.items(), key=lambda x: x[0])
    return render_template("dashboard.html", items=items, message=message)

if __name__ == "__main__":
    ensure_qrcodes()
    app.run(debug=True)
