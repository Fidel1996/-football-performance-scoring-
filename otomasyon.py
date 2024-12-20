import pandas as pd

# 1. Veri Setini Yükleme ve Temizleme
def yukle_ve_temizle(dosya_yolu, eksik_veri_esik=50, dakika_esik=300):
    """
    Veri setini yükler, temizler ve eksik verileri düzenler.
    """
    # Veri setini yükle
    df = pd.read_excel(dosya_yolu)

    # Eksik verisi %50'den fazla olan sütunları çıkar
    eksik_veri_orani = df.isnull().sum() / len(df) * 100
    df = df.loc[:, eksik_veri_orani <= eksik_veri_esik]

    # Sayısal sütunlardaki eksik verileri ortalama ile doldur
    sayisal_sutunlar = df.select_dtypes(include=['float64', 'int64']).columns
    df[sayisal_sutunlar] = df[sayisal_sutunlar].fillna(df[sayisal_sutunlar].mean())

    # Kategorik sütunlardaki eksik verileri mod ile doldur
    kategorik_sutunlar = df.select_dtypes(exclude=['float64', 'int64']).columns
    for sutun in kategorik_sutunlar:
        df[sutun] = df[sutun].fillna(df[sutun].mode()[0])

    # Minimum oynama süresine göre filtrele
    if 'Oynadığı dakikar' in df.columns:
        df = df[df['Oynadığı dakikar'] >= dakika_esik]
    else:
        print("'Oynadığı dakikar' sütunu bulunamadı!")

    return df

# 2. Pozisyonları Genelleştirme
def pozisyon_genelle(df):
    """
    Pozisyonları genelleştirerek yeni 'Mevki' sütununu oluşturur.
    """
    def genelleme_pozisyon(pozisyon):
        if isinstance(pozisyon, str):
            if 'CF' in pozisyon:
                return 'Santrfor'
            elif 'LW' in pozisyon or 'RW' in pozisyon or 'LAMF' in pozisyon or 'RAMF' in pozisyon:
                return 'Kanat'
            elif 'LB' in pozisyon or 'RB' in pozisyon or 'RWB' in pozisyon or 'LWB' in pozisyon:
                return 'Bek'
            elif 'CB' in pozisyon or 'LCB' in pozisyon or 'RCB' in pozisyon:
                return 'Stoper'
            elif 'DMF' in pozisyon or 'LDMF' in pozisyon or 'RDMF' in pozisyon:
                return 'Defansif Orta Saha'
            elif 'CMF' in pozisyon or 'LCMF' in pozisyon or 'RCMF' in pozisyon:
                return 'Merkez Orta Saha'
            elif 'AMF' in pozisyon:
                return 'Ofansif Orta Saha'
            elif 'GK' in pozisyon:
                return 'Kaleci'
        return 'Bilinmeyen'

    if 'Pozisyon' in df.columns:
        df['Pozisyon'] = df['Pozisyon'].apply(lambda x: x.split(',')[0] if isinstance(x, str) else x)
        df['Mevki'] = df['Pozisyon'].apply(genelleme_pozisyon)
    else:
        print("'Pozisyon' sütunu bulunamadı!")

    return df

# 3. Santrfor Performansı Hesaplama
def hesapla_santrfor_performansi(df, agirliklar):
    """
    Santrfor oyuncuları için performans puanı hesaplama fonksiyonu.
    """
    # Santrforlar için sütunlar
    santrfor_sutunlar = list(agirliklar.keys())

    # Sadece Santrforları filtrele
    if 'Mevki' in df.columns:
        santrfor_df = df[df['Mevki'] == 'Santrfor'][['Oyuncu'] + santrfor_sutunlar]
    else:
        print("'Mevki' sütunu bulunamadı!")
        return pd.DataFrame()

    # Performans puanını hesapla
    santrfor_df['Performans Puanı'] = santrfor_df[santrfor_sutunlar].apply(
        lambda row: sum(row[col] * agirliklar[col] for col in santrfor_sutunlar if col in row.index), axis=1
    )

    # Performans puanına göre sıralama
    santrfor_df = santrfor_df.sort_values('Performans Puanı', ascending=False)

    return santrfor_df[['Oyuncu', 'Performans Puanı'] + santrfor_sutunlar]

# 4. Ağırlıklar
agirliklar = {
    'Goller': 30, 'xG': 10, 'Asistler': 10, 'Kazanılan ikili mücadeleler, %': 3.0,
    '90 dakikada başarılı defansif aksiyonlar': 1, 'Kazanılan defansif mücadele, %': 0.1,
    'Kazanılan hava topu mücadelesi, %': 1.0, '90 dakikada başarılı ofansif aksiyonlar': 5,
    "90'da şutlar": 2.5, 'Hedefi bulan şut, %': 0.1, '90 dakikada top sürme': 2,
    'Başarılı top sürme, %': 1.5, 'Kazanılan ofansif mücadele, %': 1.0,
    '90 dakikada ceza sahasına giriş': 4, '90 dakikada devamlı koşular': 3.0,
    '90 dakikada hızlanmalar': 0.001, 'Başarılı pas, %': 0.000001, '90 dakika son paslar': 0.5,
    '90 dakikada yaptığı şut asistleri': 2, '90 dakikada akıllı paslar': 0.00000001,
    'Başarılı akıllı pas, %': 0.000000001, 'Maç başına kilit paslar': 10,
    'Rakip sahaya iletilen başarılı pas, %': 0.0000001, '90 dakikada ara paslar': 0.001,
    'Başarılı ara pas, %':0.000000001
}

# 5. Kullanım
dosya_yolu = r"C:\Users\fidel\PycharmProjects\pythonProject10\LWFDS\Search results (28).xlsx"
df = yukle_ve_temizle(dosya_yolu)
df = pozisyon_genelle(df)
sonuc = hesapla_santrfor_performansi(df, agirliklar)

# 6. Sonuçları Görüntüleme
print(sonuc.head(10))
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

import numpy as np

import numpy as np

# Logaritmik dönüşüm
sonuc['Log Ölçekli Puan'] = np.log1p(sonuc['Performans Puanı'])

# Sonuçları sıralı görüntüle
print(sonuc[['Oyuncu', 'Performans Puanı', 'Log Ölçekli Puan']].head(10))

# İstenmeyen sütunları liste olarak tanımla
istenmeyen_sutunlar = ['Log Ölçekli Puan', 'Kare Kök Ölçekli Puan', '0-10 Ölçekli Puan', 'Özelleştirilmiş Puan']

# Bu sütunları kaldır
sonuc = sonuc.drop(columns=istenmeyen_sutunlar, errors='ignore')

# Kalan sütunları kontrol et
print(sonuc.columns)

# Her sütunun maksimum değerini bul
max_degerler = sonuc.max()

# Ağırlıklar ile çarpılarak maksimum performans hesaplanır
teorik_max_puan = sum(max_degerler[col] * agirliklar[col] for col in agirliklar.keys() if col in max_degerler.index)

print(f"Bir oyuncunun teorik maksimum performans puanı: {teorik_max_puan:.2f}")



# Maksimum değerler ile çarpım sonucu
sonuc['Teorik Maksimum Performans'] = sonuc.apply(
    lambda row: sum(max_degerler[col] * agirliklar[col] for col in agirliklar.keys() if col in row.index),
    axis=1
)

# Performans puanını teorik maksimuma oranla hesaplayarak normalleştirme
sonuc['Normalleştirilmiş Performans'] = sonuc['Performans Puanı'] / sonuc['Teorik Maksimum Performans'] * 10

# Sonuçları kontrol et
print(sonuc[['Oyuncu', 'Performans Puanı', 'Teorik Maksimum Performans', 'Normalleştirilmiş Performans']].head(20))


