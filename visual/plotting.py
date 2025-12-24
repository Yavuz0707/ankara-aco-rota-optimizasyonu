import matplotlib.pyplot as plt
import os

def save_and_plot_convergence(history, folder='figure', filename='convergence.png'):
    """
    ACO yakınsama grafiğini çizer ve figure klasörüne kaydeder.
    """
    # Klasör yoksa oluştur
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(history, color='#e74c3c', linewidth=2, label='En Kısa Mesafe')
    ax.fill_between(range(len(history)), history, alpha=0.1, color='#e74c3c')
    
    ax.set_title("Yakınsama Analizi (Convergence)", fontsize=12)
    ax.set_xlabel("İterasyon Sayısı")
    ax.set_ylabel("Toplam Mesafe (km)")
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Dosyaya kaydet
    save_path = os.path.join(folder, filename)
    plt.savefig(save_path)
    
    return fig