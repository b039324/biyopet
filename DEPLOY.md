# GitHub'da yayınlama

## Kısa cevap

**Evet.** Site tamamen statiktir (HTML + CSS + JavaScript) ve sunucu tarafı gerektirmez.
GitHub deposuna yükleyip **GitHub Pages**'i açtığınızda ücretsiz, HTTPS'li olarak yayınlanır.
Tek istisna formlardır: GitHub Pages sunucu çalıştırmadığı için iletişim/bülten formları
gerçek e-posta göndermez (çözümü aşağıda).

> Önemli: Depoda bir HTML dosyasına tıklamak siteyi **çalıştırmaz**; GitHub yalnızca kodu
> gösterir. Siteyi görmek için Pages adresini açmanız gerekir.

## Yöntem A — Web arayüzüyle (en kolay)

1. GitHub'da **New repository** → isim verin (örn. `biyopet`) → **Public** → README eklemeden
   oluşturun.
2. Bilgisayarınızda `C:\Users\erhan\Documents\ai\biyopet` klasörünü açın.
3. Klasörün **içindeki** dosya ve klasörleri depo köküne yükleyin:
   `index.html`, `urunler.html`, `hikayemiz.html`, `iletisim.html`, `yasal.html`,
   `assets/`, `README.md`, `DEPLOY.md`, `.nojekyll`.
   `biyopet` klasörünü olduğu gibi sürüklemeyin; **içeriğini** yükleyin, `index.html`
   depo kökünde olmalı.
4. Depoda **Settings → Pages → Build and deployment**:
   - **Source:** Deploy from a branch
   - **Branch:** `main` · **Folder:** `/ (root)`
   - **Save**
5. 1–2 dakika sonra site şu adreste açılır:
   `https://KULLANICI_ADI.github.io/REPO_ADI/`

## Yöntem B — Git komutlarıyla

```powershell
cd C:\Users\erhan\Documents\ai\biyopet
git init
git add index.html urunler.html hikayemiz.html iletisim.html yasal.html assets README.md DEPLOY.md .nojekyll
git commit -m "Biyopet web sitesi"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADI/REPO_ADI.git
git push -u origin main
```

Ardından adım 4'teki gibi **Settings → Pages**'i açın.

## Klasörü olduğu gibi yüklerseniz ne olur?

Depo kökünde `biyopet/` alt klasörü varsa Pages "root" seçiminde `index.html` bulunamaz.
İki çözüm:

- **Önerilen:** `biyopet` klasörünün içeriğini depo köküne taşıyın.
- **Alternatif:** Klasörü `docs` olarak yeniden adlandırıp Pages'te **Folder: /docs** seçin.
  Adres yine `https://KULLANICI_ADI.github.io/REPO_ADI/` olur.

## Neler çalışır, neler çalışmaz?

| Çalışır | Çalışmaz |
| --- | --- |
| Tüm sayfalar ve göreli bağlantılar | İletişim formunun gerçek gönderimi |
| Görseller, CSS, JS, filtreler, sekmeler | Bülten kaydının gerçekten kaydedilmesi |
| Mobil menü, SSS, animasyonlar | Sunucu tarafı işlem / veritabanı |
| HTTPS, özel alan adı | `/` köküne bağımlı yapılandırmalar (site buna ihtiyaç duymaz) |

**Form çözümü:** Formspree, Netlify Forms, Google Apps Script veya kendi API'niz. `assets/js/main.js`
içindeki form `submit` olayında `fetch` ile endpoint'e gönderim yapılacak şekilde güncellenebilir.

## Özel alan adı (örn. biyopet.com)

1. **Settings → Pages → Custom domain** alanına alan adını yazın.
2. Alan adı sağlayıcınızda DNS kayıtları:
   - `A` kayıtları: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www` için `CNAME` → `KULLANICI_ADI.github.io`
3. DNS yayıldıktan sonra **Enforce HTTPS** seçeneğini işaretleyin.

## Yayın öncesi kontrol listesi

- [ ] Telefon, e-posta, adres ve sosyal medya bağlantıları gerçek bilgilerle değiştirildi.
- [ ] `yasal.html` metinleri hukuk onayından geçirildi.
- [ ] Form endpoint'i bağlandı (veya form kaldırıldı).
- [ ] `index.html` ve diğer sayfalara alan adıyla `canonical` eklendi.
- [ ] `og:image` tam URL'ye çevrildi (1200×630 önerilir).
- [ ] `preview/` ve `tools/` klasörleri yayına dahil edilmedi (isteğe bağlı).
- [ ] Ürün iddiaları ve besleme miktarları üretim/ambalaj ekibiyle teyit edildi.

## Alternatif ücretsiz barındırma

- **Netlify Drop:** `biyopet` klasörünü sürükleyip bırakın, site anında yayınlanır.
- **Cloudflare Pages / Vercel:** Depoyu bağlayın, derleme komutu boş, çıktı klasörü kök.

## "The file is too large" hatası (web arayüzü)

GitHub web yükleme sınırları: **dosya başına 25 MB**, tek seferde en fazla **100 dosya**.
Bu projedeki en büyük dosya ~1,3 MB'dır; yani tek bir görsel sınırı aşmıyor. Hata genellikle
şu nedenlerle alınır:

- Zip/arşiv dosyası yüklenmeye çalışılıyordur (GitHub zip'i açıp siteye dönüştürmez).
- Klasörün tamamı yerine çok büyük bir dosya (video, arşiv, başka proje) seçilmiştir.
- `preview` klasöründeki tam sayfa ekran görüntüleri gibi yayına gerek olmayan büyük dosyalar
  dahil edilmiştir.

**En kolay çözüm:** `biyopet-yayin` klasörünü kullanın (35 dosya, ~9,6 MB). GitHub'da
**Add file → Upload files** ekranında bu klasörün **içindeki** dosyaları ve `assets`
klasörünü sürükleyin; klasörün kendisini veya bir zip dosyasını yüklemeyin.

## Alternatif: Git ile yükleme (web sınırı yok)

`biyopet-yayin` klasörü hazır bir Git deposu olarak commit edilmiştir. GitHub'da boş bir
depo oluşturduktan sonra:

```powershell
cd C:\Users\erhan\Documents\ai\biyopet-yayin
git remote add origin https://github.com/KULLANICI_ADI/REPO_ADI.git
git branch -M main
git push -u origin main
```

Ardından **Settings → Pages → Branch: main / (root)** ile yayına alın. Bu yöntemde dosya
başına 100 MB'a kadar izin vardır ve tüm proje (preview/tools dahil) sorunsuz yüklenir.

## GitHub Desktop ile

1. GitHub Desktop → **File → Add local repository**
2. `C:\Users\erhan\Documents\ai\biyopet-yayin` klasörünü seçin.
3. **Publish repository** (public) → GitHub'a yüklenir.