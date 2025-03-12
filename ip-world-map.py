import requests
import pandas as pd
import folium

# IP manzilini geolokatsiya ma'lumotlari bilan olish
def get_geolocation(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    return response.json()

# IP manzillar ro'yxati
ip_addresses = [
    "8.8.8.8",
    "1.1.1.1",
    "128.101.101.101",
    "172.217.5.78",
    "199.247.16.90",
    "178.218.203.109",
    "89.236.249.253",

]

# IP manzillar uchun ma'lumotlarni yig'ish
geolocation_data = []

for ip in ip_addresses:
    data = get_geolocation(ip)
    if data.get('status') == 'success':  # Xatoliklarni filtr qilish
        geolocation_data.append({
            "IP": ip,
            "City": data.get('city', 'N/A'),
            "Country": data.get('country', 'N/A'),
            "Latitude": data.get('lat', 0),
            "Longitude": data.get('lon', 0),
            "ISP": data.get('isp', 'N/A')
        })

# Ma'lumotlarni DataFrame'ga o'zgartirish
df = pd.DataFrame(geolocation_data)

# Folium xarita yaratish
m = folium.Map(location=[20, 0], zoom_start=2)

# IP manzillarni xaritaga marker sifatida qo'shish
for _, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"IP: {row['IP']}\nCity: {row['City']}\nCountry: {row['Country']}\nISP: {row['ISP']}",
        tooltip=row['IP'],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Xarita saqlash
m.save("ip_map.html")

print("Xarita ip_map.html fayliga saqlandi. Brauzerda oching.")
