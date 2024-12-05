import streamlit as st
import folium
import networkx as nx
import requests
from folium import plugins
from io import StringIO
from streamlit_folium import folium_static


# Fungsi untuk mengambil data JSON dari GitHub atau URL lain
def load_data_from_github(url):
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}

# Fungsi untuk memuat data kota dan koordinatnya
def load_city_coordinates():
    # Koordinat untuk kota-kota di Provinsi Banten
    return {
        "Serang": {"lat": -6.1169309, "lon": 106.1538494},
        "Tangerang": {"lat": -6.176654, "lon": 106.633728},
        "Tangerang Selatan": {"lat": -6.342414, "lon": 106.738881},
        "Cilegon": {"lat": -6.0186834, "lon": 106.0558263},
        "Pandeglang": {"lat": -6.308830, "lon": 106.106520},
        "Serpong": {"lat": -6.300641, "lon": 106.652548}
    }

# Fungsi untuk membuat peta dan menambahkan marker
def create_map(city_connections, city_coordinates, province_name):
    # Memulai peta di posisi tengah Provinsi Banten
    map_center = [-6.1754, 106.6321]  # Lokasi Tangerang sebagai pusat
    m = folium.Map(location=map_center, zoom_start=10)

    # Menambahkan marker untuk setiap kota
    for city, coords in city_coordinates.items():
        folium.Marker(
            location=[coords["lat"], coords["lon"]],
            popup=city,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    # Membuat grafik jaringan untuk visualisasi hubungan antar kota
    G = nx.Graph()

    # Menambahkan simpul (nodes)
    for city in city_connections:
        G.add_node(city)

    # Menambahkan hubungan (edges)
    for city, connections in city_connections.items():
        for connected_city in connections:
            if connected_city in city_connections:  # Pastikan kota tujuan ada
                G.add_edge(city, connected_city)

    # Menambahkan edge ke peta sebagai garis
    for edge in G.edges():
        city1_coords = city_coordinates[edge[0]]
        city2_coords = city_coordinates[edge[1]]
        folium.PolyLine(
            locations=[[city1_coords["lat"], city1_coords["lon"]], [city2_coords["lat"], city2_coords["lon"]]],
            color="red", weight=2.5, opacity=1
        ).add_to(m)

    return m

# UI untuk aplikasi Streamlit
def app():
    st.title("Visualisasi Jaringan Kota Provinsi Banten")

    # URL file JSON yang berisi koneksi antar kota
    url = "https://raw.githubusercontent.com/Achphasesyafiq/Discrete/refs/heads/main/koneksi.json"
    
    # Memuat data dari GitHub
    city_connections = load_data_from_github(url)
    
    if not city_connections:
        st.error("Gagal memuat data atau URL tidak valid.")
        return
    
    # Menampilkan dropdown untuk memilih provinsi
    provinces = list(city_connections.keys())
    selected_province = st.selectbox("Pilih Provinsi", provinces)
    
    # Memuat koordinat kota
    city_coordinates = load_city_coordinates()
    
    # Mendapatkan koneksi kota dari provinsi yang dipilih
    province_connections = city_connections.get(selected_province, {})
    
    if province_connections:
        st.write(f"Menampilkan koneksi kota untuk provinsi {selected_province}...")
        
        # Membuat peta interaktif
        m = create_map(province_connections, city_coordinates, selected_province)
        
        # Menampilkan peta dengan Streamlit
        folium_static(m)
    else:
        st.error("Data koneksi untuk provinsi ini tidak ditemukan.")
        
# Fungsi untuk menampilkan peta di Streamlit
from streamlit_folium import folium_static

if __name__ == "__main__":
    app()
