import requests
import urllib3
import time

# Tắt cảnh báo HTTPS không xác thực
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

all_ids = []
page_index = 1
page_size = 20

base_url = "https://getway.vieclamhanoi.net/api/CongBoNguoiSdLaoDong/TatCa"

while True:
    params = {
        "PageIndex": page_index,
        "PageSize": page_size,
        "Code": "",
        "MucLuong": "",
        "KinhNghiem": "",
        "NganhKinhDoanh": "",
        "HuyenId": "",
        "TenCongViec": "",
        "UserId": "",
        "IsSuperAdmin": "false",
        "UnitId": "0",
        "AccountId": "0",
        "DeparmentId": "0",
        "IpAddress": "",
        "Role": ""
    }

    try:
        response = requests.get(base_url, params=params, verify=False)
        if response.status_code != 200:
            print(f"⚠️ Lỗi HTTP {response.status_code} tại trang {page_index}")
            break

        data = response.json().get("data", [])
        if not data:
            print("⛔ Hết dữ liệu.")
            break

        for item in data:
            id_ = item.get("id")
            if id_:
                all_ids.append(id_)

        print(f"✅ Trang {page_index}: Đã lấy {len(data)} ID")

        page_index += 1
        time.sleep(0.2)

    except Exception as e:
        print(f"❌ Lỗi ở trang {page_index}: {e}")
        break

# In ra kết quả
print(f"\n🎯 Tổng số ID thu được: {len(all_ids)}")
print("🔢 Một vài ID đầu tiên:", all_ids[:10])
