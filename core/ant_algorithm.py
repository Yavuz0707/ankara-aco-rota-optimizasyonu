# =================================================================
# DOSYA ADI: core/ant_algorithm.py
# GÖREVİ: Karınca Kolonisi Algoritması (ACO) Mantıksal İşlemleri
# =================================================================

import numpy as np # Matris ve olasılık hesaplamaları için kütüphane
import random      # Rastgele seçim işlemleri için kütüphane

class AntColonyOptimizer:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        Algoritmanın temel ayarlarını ve hafızasını başlatan yapılandırıcı fonksiyon.
        """
        self.distances = distances # Duraklar arasındaki mesafeleri içeren matris
        # Başlangıçta tüm yollara düşük ve eşit miktarda feromon atanır
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances)) # Konumların indeks listesi (0, 1, 2...)
        self.n_ants = n_ants # Her turda kaç karıncanın rota arayacağını belirler
        self.n_best = n_best # Sadece en iyi sonuç veren belirli sayıdaki karıncanın feromon bırakmasını sağlar
        self.n_iterations = n_iterations # Algoritmanın toplam kaç nesil boyunca çalışacağını belirler
        self.decay = decay # Buharlaşma oranı: Feromonların zamanla ne kadarının silineceğini belirler
        self.alpha = alpha # Seçim sırasında feromon izine (geçmiş tecrübeye) verilen ağırlık
        self.beta = beta   # Seçim sırasında mesafeye (yakınlık avantajına) verilen ağırlık
        
        # En iyi sonuçları saklamak için başlangıç değerleri
        self.best_dist = float('inf') # En kısa mesafe başlangıçta sonsuz kabul edilir
        self.best_path = []           # En iyi rotanın durak listesi
        self.history = []             # Grafik çizimi için her turdaki en iyi sonucun kaydı

    def run(self):
        """
        Optimizasyon sürecini başlatan ana döngü fonksiyonu.
        """
        for i in range(self.n_iterations):
            # 1. Adım: Tüm karıncalar için rota oluşturulur
            all_paths = self.gen_all_paths()
            # 2. Adım: En iyi rotalara feromon eklenerek o yollar güçlendirilir
            self.spread_pheronome(all_paths, self.n_best)
            # 3. Adım: Buharlaşma işlemi ile feromonlar güncellenir
            self.decay_pheromone()
            
            # Bu turun içindeki en kısa yolu bulan karıncayı tespit eder
            shortest_path = min(all_paths, key=lambda x: x[1])
            
            # Eğer bulunan yol şimdiye kadarki en iyi yoldan kısaysa günceller
            if shortest_path[1] < self.best_dist:
                self.best_dist = shortest_path[1]
                self.best_path = shortest_path[0]
            
            # Grafik çizimi için her turun sonucunu hafızaya kaydeder
            self.history.append(self.best_dist)
            
        return self.best_path, self.best_dist, self.history

    def gen_all_paths(self):
        """
        Belirlenen karınca sayısı kadar bireysel rotayı toplu halde üretir.
        """
        all_paths = []
        for i in range(self.n_ants):
            # Her karınca 0. indeksten (başlangıç noktası) yola çıkar
            path = self.gen_path(0) 
            # Karıncanın toplam katettiği mesafe hesaplanır
            path_len = self.gen_path_dist(path)
            all_paths.append((path, path_len))
        return all_paths

    def gen_path(self, start_node):
        """
        Tek bir sanal karıncanın tüm durakları gezip merkeze döndüğü süreci yönetir.
        """
        path = [start_node]
        visited = set(path) # Karıncanın hangi duraklara gittiğini takip eder
        prev = start_node
        
        # Tüm şehirler gezilene kadar (toplam durak - 1 kez) döngü çalışır
        for i in range(len(self.distances) - 1):
            # Bir sonraki durağı olasılıksal formüle göre seçer
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append(move)
            visited.add(move)
            prev = move
        
        # Başlangıç noktasına geri dönerek rotayı kapatır (Dairesel rota)
        path.append(start_node) 
        return path

    def pick_move(self, pheromone, dist, visited):
        """
        ACO Karar Formülü: Karıncanın bir sonraki durağına karar verdiği matematiksel bölümdür.
        """
        pheromone = np.copy(pheromone)
        # Daha önce gidilen şehirlerin tekrar seçilme ihtimali 0 yapılır
        pheromone[list(visited)] = 0 

        # Karınca seçim formülü: (Feromon ^ Alpha) * ((1 / Mesafe) ^ Beta)
        # Mesafeye eklenen 0.0001 sıfıra bölünme hatasını (divide by zero) engeller
        row = (pheromone ** self.alpha) * (( 1.0 / (dist + 0.0001)) ** self.beta)
        
        # Değerleri toplamı 1 olacak şekilde oranlayarak olasılık dağılımı oluşturur
        norm_row = row / row.sum()
        
        # Belirlenen olasılıklara göre rastgele seçim yapar (Kumarhane çarkı mantığı)
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        return move

    def gen_path_dist(self, path):
        """
        Oluşturulan bir durak listesinin toplam uzunluğunu kilometre bazında toplar.
        """
        total_dist = 0
        for i in range(len(path) - 1):
            # Mevcut durak ile bir sonraki durak arasındaki mesafeyi matristen alır
            total_dist += self.distances[path[i]][path[i+1]]
        return total_dist

    def spread_pheronome(self, all_paths, n_best):
        """
        Başarılı karıncaların geçtiği yolları feromon miktarını artırarak ödüllendirir.
        """
        # Yolları mesafeye göre kısadan uzuna sıralar
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        # Sadece en iyi n_best kadar karıncanın geçişine feromon ekler
        for path, dist in sorted_paths[:n_best]:
            for i in range(len(path) - 1):
                # Mesafe ne kadar kısa ise yola o kadar fazla feromon (1/dist) eklenir
                self.pheromone[path[i]][path[i+1]] += 1.0 / dist

    def decay_pheromone(self):
        """
        Buharlaşma: Tüm yollardaki feromon izlerini zamanla azaltarak eski bilginin etkisini düşürür.
        """
        # Mevcut feromon miktarını (1 - decay) oranıyla çarparak azaltır
        self.pheromone = self.pheromone * (1 - self.decay)