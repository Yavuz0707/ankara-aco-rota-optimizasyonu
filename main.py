# =================================================================
# PROGRAMIN ADI: Ankara Su Numunesi ACO Optimizasyonu
# HAZIRLAYAN: ŞÜKRÜ YAVUZ - 2312729015
# PROJE REPO: https://github.com/Yavuz0707/ankara-aco-rota-optimizasyonu.git
# =================================================================

import streamlit as st                 # Arayüz bileşenleri için kütüphane
import folium                          # Harita alt yapısı için kütüphane
from streamlit_folium import st_folium # Haritayı web ekranına yerleştirmek için araç
from folium.plugins import AntPath     # Hareketli rota çizgisi eklentisi
import numpy as np                     # Matematiksel hesaplamalar için kütüphane
import requests                        # Google API veri transferi için kütüphane

# Proje ağacına uygun olarak harici dosyalardan veri, sınıf ve görselleştirme yükleme
from data.coordinates import LOCATIONS 
from core.ant_algorithm import AntColonyOptimizer
from visual.plotting import save_and_plot_convergence # Grafik fonksiyonu


# -----------------------------------------------------------------
# SAYFA AYARLARI
# -----------------------------------------------------------------
st.set_page_config(
    page_title="Ankara ACO Su Rotası",
    layout="wide"
)

st.title("Ankara Su Numunesi ACO Optimizasyonu")
st.markdown("Karınca Kolonisi Algoritması kullanılarak duraklar arası en verimli rota hesaplanmaktadır.")


# -----------------------------------------------------------------
# MESAFE MATRİSİ FONKSİYONU (GOOGLE MAPS)
# -----------------------------------------------------------------
@st.cache_data
def get_google_matrix(locations):
    # .streamlit/secrets.toml dosyasındaki anahtarı kullanır
    api_key = st.secrets["GOOGLE_API_KEY"] 

    coords = list(locations.values())
    origins = "|".join([f"{lat},{lon}" for lat, lon in coords])

    # Mesafe verilerini çekmek için API sorgu adresini oluşturur
    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={origins}&destinations={origins}&key={api_key}"
    )

    # API yanıtını alır ve metreyi kilometreye çevirerek matrise aktarır
    data = requests.get(url).json()
    n = len(coords)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            matrix[i][j] = data["rows"][i]["elements"][j]["distance"]["value"] / 1000

    return matrix


# -----------------------------------------------------------------
# YAN PANEL (KULLANICI PARAMETRELERİ)
# -----------------------------------------------------------------
with st.sidebar:
    st.header("ACO Parametreleri")
    
    # Algoritmanın çalışma prensibini belirleyen kullanıcı değişkenleri
    n_ants = st.slider("Karınca Sayısı", 5, 50, 25)
    n_iter = st.slider("İterasyon Sayısı", 10, 100, 40)
    decay = st.slider("Buharlaşma Oranı", 0.1, 0.99, 0.63)
    alpha = st.slider("Feromon Etkisi (Alpha)", 0.1, 5.0, 1.71)
    beta = st.slider("Mesafe Etkisi (Beta)", 0.1, 5.0, 1.01)

    st.markdown("---")
    st.write("Hazırlayan: Şükrü Yavuz")
    st.write("Öğrenci No: 2312729015")


# -----------------------------------------------------------------
# HESAPLAMA SÜRECİ
# -----------------------------------------------------------------
if st.button("ACO Algoritmasını Başlat"):
    # Google üzerinden gerçek yol mesafelerini alır
    matrix = get_google_matrix(LOCATIONS)
    
    # core/ant_algorithm.py içerisindeki sınıfı kullanarak optimizasyonu başlatır
  
    aco = AntColonyOptimizer(
        distances=matrix, 
        n_ants=n_ants, 
        n_best=5, 
        n_iterations=n_iter, 
        decay=decay, 
        alpha=alpha, 
        beta=beta
    )
    
    path, dist, history = aco.run()

    # Hesaplanan verileri sayfa yenilense de korumak için saklar
    st.session_state["path"] = path
    st.session_state["dist"] = dist
    st.session_state["history"] = history


# -----------------------------------------------------------------
# SONUÇLARIN GÖRSELLEŞTİRİLMESİ
# -----------------------------------------------------------------
if "path" in st.session_state:
    path = st.session_state["path"]
    dist = st.session_state["dist"]
    history = st.session_state["history"]

    names = list(LOCATIONS.keys())
    coords = list(LOCATIONS.values())

    # İstatistiksel özet sütunları
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Mesafe", f"{dist:.2f} km")
    improvement = ((history[0] - history[-1]) / history[0]) * 100
    c2.metric("İyileşme Oranı", f"% {improvement:.1f}")
    c3.metric("Tamamlanan Tur", len(history))

    st.markdown("---")

    # Sol tarafta harita, sağ tarafta yakınsama grafiği yer alır
    col_map, col_graph = st.columns([1.5, 1])

    with col_map:
        st.subheader("Optimum Rota Haritası")
        m = folium.Map(location=[39.95, 32.85], zoom_start=9)
        route_coords = [coords[i] for i in path]
        
        # Harita üzerine durak noktalarını işaretler
        for i, idx in enumerate(path[:-1]):
            folium.Marker(coords[idx], popup=f"{i+1}. Durak: {names[idx]}").add_to(m)
            
        # Animasyonlu çizgi ile rota yönünü gösterir
        AntPath(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)
        st_folium(m, height=450, use_container_width=True)

    with col_graph:
        st.subheader("Yakınsama Grafiği")
        # Grafik çizimi harici dosyadan (visual/plotting.py) çağrılır
        # Bu fonksiyon aynı zamanda grafiği figure/ klasörüne kaydeder
        fig = save_and_plot_convergence(history)
        st.pyplot(fig)

    # Detaylı durak listesi
    with st.expander("Sıralı Rota Listesini Görüntüle"):
        for i, step in enumerate(path):
            if i < len(path)-1:
                st.write(f"{i+1}. Durak: {names[step]}")
            else:
                st.write(f"Dönüş Noktası: {names[step]}")