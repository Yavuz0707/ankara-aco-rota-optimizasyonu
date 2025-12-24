# =================================================================
# DOSYA ADI: core/matrix_utils.py
# GÖREVİ: Google Maps API Kullanarak Mesafe Matrisi Oluşturma
# =================================================================

import googlemaps # Google Maps servisleri için resmi istemci kütüphanesi
import pandas as pd
import numpy as np # Sayısal matris işlemleri için kütüphane
import streamlit as st # Hata mesajlarını arayüzde göstermek için
import os

def get_distance_matrix(locations, api_key):
    """
    Google Maps Distance Matrix API kullanarak noktalar arasındaki 
    gerçek yol mesafelerini kilometre cinsinden çeker.
    """
    # Verilen API anahtarı ile Google Maps istemcisini başlatır
    gmaps = googlemaps.Client(key=api_key)
    
    # Lokasyon sözlüğünden isimleri ve koordinatları listeler halinde ayırır
    names = list(locations.keys())
    coords = list(locations.values())
    n = len(names)
    
    # Mesafeleri saklamak için n x n boyutunda, içi sıfır dolu bir matris hazırlar
    dist_matrix = np.zeros((n, n))
    
    # Not: Google API limitleri gereği tek seferde maksimum 100 eleman sorgulanabilir.
    # 10 duraklı bir set (10x10=100) tam limit sınırındadır.
    
    try:
        # Koordinat çiftlerini API'nin kabul ettiği 'lat,lng' metin formatına dönüştürür
        origins = [f"{lat},{lng}" for lat, lng in coords]
        destinations = origins # Başlangıç ve varış noktaları aynı settir
        
        # Google Maps Distance Matrix servisine sürüş modu (driving) ile istek gönderir
        response = gmaps.distance_matrix(origins, destinations, mode="driving")
        
        # API yanıtının başarılı olup olmadığını kontrol eder
        if response['status'] != 'OK':
            st.error("Google Maps API sorgusu sırasında bir hata oluştu.")
            return None

        # API'den gelen satır verilerini (rows) döngüye alarak işler
        rows = response['rows']
        for i in range(n):
            elements = rows[i]['elements']
            for j in range(n):
                # Noktanın kendisine olan mesafesi her zaman sıfırdır
                if i == j:
                    dist_matrix[i][j] = 0
                else:
                    try:
                        # API'den gelen metre birimindeki değeri (value) alır
                        meters = elements[j]['distance']['value']
                        # Metreyi kilometreye çevirerek matrisin ilgili hücresine yazar
                        dist_matrix[i][j] = meters / 1000.0 
                    except KeyError:
                        # Eğer iki nokta arasında sürüş rotası bulunamazsa (KeyError)
                        # Algoritmanın o yolu seçmemesi için çok yüksek bir maliyet atar
                        dist_matrix[i][j] = 9999.0
                        
        return dist_matrix

    except Exception as e:
        # Beklenmedik bağlantı veya veri hatalarını yakalar ve kullanıcıya bildirir
        st.error(f"Mesafe matrisi oluşturulurken teknik bir hata oluştu: {e}")
        return None