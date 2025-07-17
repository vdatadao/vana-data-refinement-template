# Instagram Data DAO - Vana Data Refinement

Bu repository, Instagram verilerini Vana ağında işlemek için özelleştirilmiş bir Data DAO template'idir. Ham Instagram verilerini normalize edilmiş ve gizlilik odaklı SQLite veritabanlarına dönüştürür.

## Instagram Data DAO Özellikleri

### Desteklenen Veri Türleri
- **Profil Bilgileri**: Kullanıcı adı, takipçi sayısı, gönderi sayısı (gizlilik korumalı)
- **Gönderiler**: Beğeni, yorum sayıları, medya türleri, hashtag analizleri
- **Hikayeler**: Görüntülenme sayıları, medya türü analizleri
- **Yorumlar**: Yorum uzunlukları ve etkileşim metrikleri
- **Direkt Mesajlar**: Mesaj uzunlukları ve türleri (içerik gizli)
- **Etkileşim Metrikleri**: Profil görüntülenmeleri, erişim, gösterim sayıları
- **Aktivite Desenleri**: Saatlik ve günlük aktivite analizleri
- **Hashtag Kullanımı**: Hashtag kullanım sıklığı ve desenleri

### Gizlilik Koruması
- **Kullanıcı Adları**: SHA-256 ile hash'lenir
- **Metin İçerikleri**: Sadece uzunluk bilgisi saklanır
- **Kişisel Bilgiler**: Bio, yorumlar, mesajlar hash'lenir veya analitik veriye dönüştürülür
- **Lokasyon Bilgileri**: Sadece varlık/yokluk bilgisi saklanır

## Kurulum ve Kullanım

### 1. Environment Ayarları
```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:
```env
SCHEMA_NAME=Instagram Analytics
SCHEMA_VERSION=0.0.1
SCHEMA_DESCRIPTION=Schema for Instagram DLP, representing user profile, posts, stories, and engagement analytics

# IPFS ayarları (Pinata için)
PINATA_API_KEY=your_pinata_api_key_here
PINATA_API_SECRET=your_pinata_api_secret_here
```

### 2. Instagram Verisi Formatı
Instagram verilerinizi `input/` klasörüne JSON formatında yerleştirin. Örnek format için `input/instagram_sample.json` dosyasına bakın.

### 3. Yerel Test
```bash
# Python ile
pip install -r requirements.txt
python -m refiner

# Docker ile
docker build -t instagram-refiner .
docker run --rm \
  --volume $(pwd)/input:/input \
  --volume $(pwd)/output:/output \
  --env-file .env \
  instagram-refiner
```

## Veri Şeması

### Ana Tablolar
1. **user_profiles**: Kullanıcı profil bilgileri (gizlilik korumalı)
2. **posts**: Gönderi metrikleri ve etkileşim verileri
3. **stories**: Hikaye görüntülenme ve medya analizleri
4. **comments**: Yorum etkileşim metrikleri
5. **direct_messages**: Mesaj istatistikleri (içerik korunmaz)
6. **engagement_metrics**: Günlük etkileşim metrikleri
7. **hashtag_usage**: Hashtag kullanım desenleri
8. **activity_patterns**: Saatlik/günlük aktivite analizleri

### Analitik Özellikler
- **Etkileşim Oranı**: (Beğeni + Yorum) / Takipçi sayısı
- **Aktivite Desenleri**: Hangi saatlerde daha aktif
- **Hashtag Analizleri**: En çok kullanılan hashtag'ler
- **Medya Türü Dağılımı**: Fotoğraf vs video tercihleri
- **Sosyal Etkileşim**: Yorum ve DM sıklığı

## Instagram Veri Kaynakları

Bu refiner aşağıdaki Instagram veri kaynaklarıyla çalışabilir:
- Instagram Data Export (resmi)
- Instagram Business API verileri
- Instagram Analytics verileri
- Üçüncü parti Instagram analiz araçları

## Deployment

GitHub Actions otomatik olarak Docker image'ını build eder ve release yapar:

```bash
# Manuel build
docker build -t instagram-refiner .

# Release
git tag v1.0.0
git push origin v1.0.0
```

## Vana Ağında Kullanım

1. Bu refiner'ı Vana ağına deploy edin
2. Instagram DLP'nizi bu refiner ile yapılandırın
3. Kullanıcılar Instagram verilerini yükleyebilir
4. Veriler otomatik olarak rafine edilir ve IPFS'e yüklenir
5. Vana Query Engine ile analiz edilebilir

## Katkıda Bulunma

Instagram veri işleme özelliklerini geliştirmek için:
1. Fork yapın
2. Yeni özellikler ekleyin
3. Pull request gönderin

## Lisans

[MIT License](LICENSE)