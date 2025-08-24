import qrcode
import json
import os

# تحميل العملاء
with open("data/clients.json", "r") as f:
    clients = json.load(f)

# إنشاء مجلد QR إذا ما موجود
os.makedirs("qrcodes", exist_ok=True)

# توليد QR لكل عميل
for client in clients:
    client_id = client["id"]
    url = f"http://127.0.0.1:5000/client?id={client_id}"  # رابط محلي لصفحة العميل
    img = qrcode.make(url)
    img.save(f"qrcodes/{client_id}.png")

print("✅ تم توليد QR Codes لكل العملاء في مجلد qrcodes!")
