# Biyopet — Kurumsal Web Sitesi (Önizleme)

Biyopet kedi ve köpek mamaları için hazırlanmış, tamamen statik (HTML + CSS + vanilla JS)
kurumsal web sitesi. Kurulum, derleme veya bağımlılık gerektirmez; herhangi bir statik
sunucuda doğrudan yayınlanabilir.

## Sayfalar

| Sayfa | Dosya | İçerik |
| --- | --- | --- |
| Ana sayfa | `index.html` | Hero, ürün kartları, neden Biyopet, üretim yaklaşımı, rakamlar, SSS, CTA |
| Ürünler | `urunler.html` | Filtrelenebilir ürün listesi, 4 ürün detayı, besleme rehberi sekmeleri |
| Hikayemiz | `hikayemiz.html` | Marka hikayesi, değerler, kalite yaklaşımı, üretim adımları |
| İletişim | `iletisim.html` | İletişim bilgileri, harita paneli, çalışma saatleri, doğrulamalı form |
| Yasal metinler | `yasal.html` | KVKK aydınlatma metni, gizlilik politikası, çerez politikası |

## Klasör yapısı

```
biyopet/
├── index.html
├── urunler.html
├── hikayemiz.html
├── iletisim.html
├── yasal.html
├── assets/
│   ├── css/style.css        # Tasarım sistemi + bileşenler + duyarlı tasarım
│   ├── js/main.js           # Menü, filtre, sekmeler, SSS, form doğrulama, animasyonlar
│   └── img/
│       ├── favicon.svg
│       ├── kaynak/          # Orijinal ambalaj görselleri (saydam zemin, gölgesiz)
│       └── opt/             # Optimize çıktılar (WebP + PNG, 620/1100 px)
├── preview/                 # Önizleme ekran görüntüleri
├── tools/                   # Görsel hazırlama, statik kontrol ve ekran görüntüsü betikleri
└── README.md
```

## Yayınlama

Site statik olduğu için GitHub Pages, Netlify, Vercel veya Cloudflare Pages'te doğrudan
çalışır. Adım adım GitHub Pages kurulumu için [DEPLOY.md](DEPLOY.md) dosyasına bakın.

## Yerel önizleme

```powershell
cd C:\Users\erhan\Documents\ai\biyopet
python -m http.server 8099 --bind 127.0.0.1
```

Ardından tarayıcıda `http://127.0.0.1:8099` adresini açın.
(Site doğrudan `index.html` çift tıklanarak da açılabilir; sunucu, göreli yollar ve
paylaşılan görüntülerin doğru çalışması için önerilir.)

## Önizleme görselleri

- `preview/onizleme-masaustu.png` — 5 sayfanın masaüstü tam sayfa görünümü
- `preview/onizleme-mobil.png` — ana sayfa, ürünler ve iletişim mobil görünümü
- `preview/urun-kartlari.png`, `preview/urun-detay.png` — yeni orijinal görsellerle ürün bölümleri
- `preview/urunler-hero.png`, `preview/hikayemiz-hero.png` — görselli sayfa başlıkları (masaüstü)
- `preview/urunler-mobile-hero.png`, `preview/hikayemiz-mobile-hero.png` — mobil banner görünümü
- `preview/*-hero.png` — sayfa başı ekran görüntüleri (1440 px / 390 px)
- `preview/*-desktop.png`, `preview/*-mobile.png` — tam sayfa görüntüler
- `preview/test-results.json` — tarayıcı işlev testlerinin sonuçları (28/28)

## Tasarım

- **Renkler:** koyu orman yeşili (`#0F3B29`, `#061D14`), altın (`#C9A227`, `#EBD39B`),
  krem (`#FDFBF6`, `#F3EADA`) — ambalaj paletiyle uyumlu.
- **Tipografi:** Segoe UI / sistem sans-serif ailesi; güçlü ağırlıklar ve sıkı harf aralığı.
  Web fontu kullanılmaz, bu nedenle dış bağlantıya ihtiyaç duymaz.
- **Bileşenler:** yapışkan üst menü, kayan avantaj şeridi, ürün kartları, arşiv kemerli hero,
  süreç adımları, veri tabloları, SSS akordeonu, iletişim formu, CTA panelleri.
- **Erişilebilirlik:** atlama bağlantısı, tek `h1`, sıralı başlıklar, form etiketleri,
  `aria-*` durumları, klavye ile kullanılabilir filtre/sekme/akordeon, `prefers-reduced-motion`
  desteği, görünür odak halkaları.
- **Duyarlı tasarım:** 1080 / 960 / 820 / 640 px kırılımları; mobilde hamburger menü,
  tek sütunlu kartlar, yatay kaydırılabilir besleme tabloları.

## Etkileşimler

- Ürün filtreleri (Tümü / Köpek / Kedi / Yetişkin / Yavru) ve sonuç sayacı
- Besleme rehberi sekmeleri (4 ürün grubu, klavye ok tuşları destekli)
- SSS akordeonu (aynı anda tek açık öğe)
- Mobil menü (dışına tıklama / Escape ile kapanma)
- İletişim ve bülten formlarında istemci tarafı doğrulama + durum mesajları
- Kaydırma ile görünme animasyonları, kayan avantaj şeridi

## Yayına almadan önce güncellenmesi gerekenler

1. **İletişim bilgileri:** `0850 000 00 00`, `info@biyopet.com`, `bayilik@biyopet.com` ve
   açık adres tüm sayfalarda (üst duyuru çubuğu, footer, iletişim sayfası) yer tutucudur.
2. **Sosyal medya:** footer'daki Instagram/Facebook/YouTube/WhatsApp bağlantıları platform
   ana sayfalarına gider; marka hesaplarıyla değiştirilmelidir.
3. **Form gönderimi:** formlar yalnızca istemci tarafında çalışır. Gerçek kullanım için
   e-posta servisi, CRM veya bir form endpoint'i bağlanmalı; KVKK onay kutusu sunucuda da
   doğrulanmalıdır.
4. **Yasal metinler:** `yasal.html` içeriği genel bilgilendirme amaçlı örnek metindir;
   hukuk danışmanıyla şirket bilgilerine göre uyarlanmalıdır.
5. **SEO:** sayfalara gerçek alan adıyla `canonical` ve `og:image` (tam URL) ekleyin,
   gerekirse `sitemap.xml` / `robots.txt` oluşturun.
6. **Analitik ve çerez onayı:** ölçümleme aracı eklenecekse çerez politikası ve onay bandı
   buna göre güncellenmelidir.
7. **İçerik doğrulaması:** ürün faydaları, besleme miktarları ve üretim süreci ifadeleri
   ambalaj/üretim ekibiyle son kez teyit edilmelidir.

## Görseller

Ambalaj görselleri kullanıcı tarafından sağlanmıştır; kaynak dosyalar saydam zeminli ve
gölgesizdir. Kaynaklar `assets/img/kaynak/` altında, optimize çıktılar `assets/img/opt/`
altında tutulur. Görseller WebP + PNG olarak 620 px (kart) ve 1100 px (hero/detay)
boyutlarında üretilir; zemindeki çok düşük alfalı gürültü temizlenir, ambalajın kenarları
korunur. Ürün fotoğraflarına CSS ile ayrıca gölge eklenmez.

Yeni kaynak görsel eklenecekse `assets/img/kaynak/` içine aynı adla koyup ardından şu betiği
çalıştırmak yeterlidir (HTML `width`/`height` değerleri de otomatik güncellenir):

```powershell
python tools/prep_images.py
```

### Sayfa başı arka plan görselleri

Ürünler ve Hikayemiz sayfalarının üst bandında aile/pati fotoğrafları arka plan olarak
kullanılır. Kaynaklar `assets/img/bg/kaynak/`, çıktılar `assets/img/bg/` altındadır:

- Masaüstü: **1920 × 823 px** (`urunler-hero`, `hikayemiz-hero`)
- Mobil: **1080 × 760 px** (`*-mobil`)
- Format: WebP + JPEG yedeği; metin okunabilirliği için CSS'te krem degrade overlay uygulanır.
- Masaüstünde görsel tam genişlikte arkadadır; mobilde içeriğin üstünde bir banner olarak
  yumuşak bir geçişle yer alır.

Yeniden üretmek için:

```powershell
python tools/prep_hero_bg.py
```

## Kontroller

- `tools/check_site.py` — kırık bağlantı/çapa, eksik görsel, başlık sırası, form etiketi,
  yinelenen `id` kontrolü (lxml ile).
- `tools/site_test.mjs` — Chrome DevTools Protocol ile işlevsel testler (filtreler, sekmeler,
  mobil menü, formlar, yatay taşma, konsol hataları).
- `tools/screenshot.mjs` — masaüstü/mobil tam sayfa önizleme görüntüleri.
