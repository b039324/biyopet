# Biyopet — Tanıtım Sitesi

Biyopet kedi ve köpek maması firması için hazırlanmış, tek sayfalık, tamamen statik
bir tanıtım sitesi. HTML + CSS + vanilla JavaScript kullanılmıştır; sunucu,
veritabanı veya build aracı gerektirmez.

---

## 📁 Dosya Yapısı

```
/
├── index.html
├── css/
│   └── style.css
├── js/
│   └── main.js
├── data/
│   └── urunler.json
├── images/
│   ├── logo.png
│   ├── hero.jpg
│   ├── urun-kopek-yetiskin.jpg
│   ├── urun-kopek-yavru.jpg
│   ├── urun-kedi-yetiskin.jpg
│   └── urun-kedi-yavru.jpg
└── README.md
```

### Görsel dosyaları (aynı isimlerle koyman gerekenler)

- `logo.png` — site logosu (header + footer)
- `hero.jpg` — ana sayfa açılış fotoğrafı (aile + kedi + köpek)
- `urun-kopek-yetiskin.jpg` — ürün 1
- `urun-kopek-yavru.jpg` — ürün 2
- `urun-kedi-yetiskin.jpg` — ürün 3
- `urun-kedi-yavru.jpg` — ürün 4

Farklı isim kullanacaksan `data/urunler.json` içindeki `gorsel` alanlarını
güncelle. Logo ve hero için `index.html` ve `css/style.css` içindeki yolları
güncellemen gerekir (`style.css` içinde `hero-bg` background-image).

---

## ⚠️ Önemli: Yerel Test

Ürünler `fetch('data/urunler.json')` ile yüklenir. Tarayıcılar güvenlik nedeniyle
`file://` protokolünde `fetch` isteğini engelleyebilir. Bu yüzden siteyi **yerel
bir sunucu ile** test etmelisin:

**Seçenek 1 — VS Code Live Server eklentisi**
1. VS Code'da klasörü aç.
2. Live Server eklentisini kur.
3. `index.html`'e sağ tık → "Open with Live Server".

**Seçenek 2 — Python ile**
```bash
cd proje-klasoru
python -m http.server 8000
```
Ardından tarayıcıda `http://localhost:8000` adresini aç.

**Seçenek 3 — Node.js ile**
```bash
npx serve .
```

---

## ✏️ İçerik Nasıl Düzenlenir?

### 1. Ürün eklemek / düzenlemek
Tüm ürünler `data/urunler.json` dosyasından okunur. HTML/CSS'e dokunmadan
düzenleme yapabilirsin.

Yeni ürün eklemek için `urunler` dizisine yeni bir nesne ekle:

```json
{
  "id": 5,
  "kategori": "kopek",
  "ad": "Somonlu Yetişkin Köpek Maması",
  "kisaAciklama": "Kısa tanıtım cümlesi.",
  "uzunAciklama": "Modalda görünecek detaylı açıklama.",
  "gorsel": "images/urun-kopek-somon.jpg",
  "ozellikler": ["Özellik 1", "Özellik 2"]
}
```

- `kategori`: `"kopek"` veya `"kedi"` olmalı.
- `id`: her üründe benzersiz olmalı.
- `gorsel`: `images/` klasörüne göre yol.
- Yeni görseli `images/` klasörüne eklemeyi unutma.

### 2. Hakkımızda, slogan, iletişim bilgileri
`index.html` içinde yorum satırlarıyla işaretlenmiştir:

- `<!-- HERO SLOGAN METNİ: burayı düzenle -->`
- `<!-- HAKKIMIZDA METNİ: burayı düzenle -->`
- `<!-- İkonlu maddeler: buradaki metinleri düzenleyebilirsin -->`
- `<!-- İletişim bilgileri: buradaki metinleri düzenle -->`
- `<!-- FOOTER KISA BİLGİ: burayı düzenle -->`
- `<!-- TELİF SATIRI: yılı ve firma adını düzenle -->`

### 3. Renkleri değiştirmek
Tüm renkler `css/style.css` dosyasının en üstündeki `:root` bloğunda tanımlıdır.
Örneğin ana yeşili değiştirmek için:

```css
--color-primary: #3f7d4f;   /* yeni renk kodu */
--color-primary-dark: #2f5f3b;
```

---

## 🚀 Yayınlama — Netlify (sürükle-bırak)

1. [netlify.com](https://www.netlify.com) adresine git, ücretsiz hesap oluştur.
2. Giriş yaptıktan sonra ana panelde **"Add new site" → "Deploy manually"**
   (veya doğrudan "Sites" sayfasında sürükle-bırak alanı) seçeneğini kullan.
3. Proje klasörünün tamamını (`index.html`, `css`, `js`, `data`, `images`
   dahil) tarayıcı penceresine sürükle-bırak.
4. Netlify birkaç saniye içinde siteyi yayınlar ve sana
   `https://rastgele-isim.netlify.app` şeklinde bir adres verir.
5. **Site settings → Change site name** ile adresi
   `biyopet.netlify.app` gibi özelleştirebilirsin.

> Not: Netlify klasörün kökünde `index.html` görmelidir. Yani klasörü
> sürüklerken içinde doğrudan `index.html` bulunan klasörü sürükle.

### Alternatifler
- **Vercel**: [vercel.com](https://vercel.com) → "Add New Project" →
  klasörü yükle veya GitHub reposunu bağla.
- **GitHub Pages**: Projeyi bir GitHub reposuna yükle → Settings → Pages →
  Branch olarak `main` ve `/root` seç.

---

## ✅ Test Kontrol Listesi

- [ ] Site yerel sunucuda açılıyor, ürünler görünüyor.
- [ ] Köpek / Kedi sekmeleri arasında geçiş çalışıyor.
- [ ] "Detaylar" butonu modalı açıyor, ESC ve çarpı ile kapanıyor.
- [ ] Mobil görünümde hamburger menü açılıyor, linke tıklayınca kapanıyor.
- [ ] İletişim formu boş gönderimde uyarı, dolu gönderimde teşekkür mesajı veriyor.
- [ ] Tüm görseller `images/` klasöründe doğru isimlerle mevcut.
- [ ] `urunler.json` geçerli JSON (virgül/parantez hatası yok).

---

## 🎨 Tasarım Notları

- Yeşil + krem tonları, yuvarlatılmış köşeler, yumuşak gölgeler.
- CSS değişkenleriyle merkezi renk yönetimi.
- `prefers-reduced-motion` desteği (animasyon hassasiyeti olan kullanıcılar için).
- Anlamlı başlık hiyerarşisi, alt metinler, ARIA etiketleri.
- Yumuşak fade-in animasyonları (abartısız).