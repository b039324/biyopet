# Biyopet — Bağımsız QA Raporu

**İnceleme anı:** 22.10.2026, 21:25 (kaynak üzerinden statik inceleme; tarayıcı kullanılmadı).
**Kapsam:** `index.html`, `urunler.html`, `hikayemiz.html`, `iletisim.html`, `yasal.html` (footer'dan bağlantılı yeni sayfa), `assets/css/style.css`, `assets/js/main.js`. Satır numaraları bu ana aittir.

## Genel değerlendirme

Görsel dil, tipografi ve bileşen tutarlılığı iyi; sayfa başına tek `h1`, tüm form alanlarında etiket, tüm görsellerde `alt` ve benzersiz `id`'ler var. Tüm iç bağlantı/çapa hedefleri (`urunler.html#kopek-*`, `#besleme`, `index.html#sss`, `hikayemiz.html#kalite`, `iletisim.html#form`, `yasal.html#kvkk/#gizlilik/#cerez`) çözülüyor; kırık link veya eksik görsel yok. Heading sırası, `#` placeholder linkleri ve "Koruyucu içermez" genellemesi önceki tura göre büyük ölçüde düzeltilmiş.

Yayına çıkmayı engelleyen üç konu var: formların gerçek gönderim yapmaması ve sayfada "önizleme" notları, `yasal.html`'deki örnek metin/hukuk uyarısı, ve bariz placeholder iletişim verileri. Bunların yanında onay kutusu hatasının gösterilmemesi (gerçek JS hatası), JS'siz içeriğin görünmemesi ve birkaç erişilebilirlik/okunabilirlik eksiği giderilmeli.

## Kritik

1. **Formlar sunucuya bağlı değil; "önizleme" metinleri canlı sayfada.**
   - `iletisim.html:217-221` ziyaretçiye görünen not: "Bu alan önizleme amaçlıdır. Form gönderimi bir sunucuya bağlı değildir; gerçek kullanımda e-posta servisi veya CRM entegrasyonu eklenmelidir."
   - `main.js:196-200` başarı mesajı "(Önizleme: form gönderimi simüle edilmiştir.)" içeriyor; `main.js:146-149` bülten "Teşekkürler! Kaydınız alındı." diyor ama hiçbir istek gönderilmiyor. Her iki formda da `action`/`method` yok (`iletisim.html:165,321`).
   - Düzeltme: formları gerçek bir endpoint'e (e-posta servisi/CRM) bağlayın; bu iki notu ve "simüle" ifadesini kaldırın; başarı/hatayı sunucu yanıtına göre verin.

2. **`yasal.html`'de yayın öncesi hukuk uyarısı görünür durumda.**
   - `yasal.html:133-137`: "Bu metinler genel bilgilendirme amacıyla hazırlanmış örnek metinlerdir. Yayına almadan önce hukuk danışmanınızla birlikte şirket bilgilerinize ve yürürlükteki mevzuata göre uyarlanmalıdır." Sayfa tüm footer'lardan erişilebilir (`index.html:623-625`, `urunler.html:594-596`, `hikayemiz.html:362-364`, `iletisim.html:335-337`).
   - Düzeltme: metinleri hukuk onayından geçirip uyarıyı kaldırın; uyarı gerekiyorsa yayın paketinde değil iç notta tutun.

3. **Placeholder iletişim verileri ve sosyal medya bağlantıları.**
   - Telefon "0850 000 00 00": `index.html:72,603`; `urunler.html:53,577`; `hikayemiz.html:52,345`; `iletisim.html:48,122,318`; `yasal.html:72,330`; JSON-LD `index.html:25`. WhatsApp `https://wa.me/908500000000` (`index.html:574` vd.) aynı sahte numaraya gidiyor.
   - Adres "Merkez Mah. Sanayi Cad. No: 12" (`iletisim.html:114`) ve "Temsili konum görseli" (`iletisim.html:157`) gerçek değil. Sosyal linkler marka profiline değil platform ana sayfalarına gidiyor (`index.html:571-573` vd.).
   - Düzeltme: gerçek numara/adres/e-posta ile marka profillerini koyun; olmayanları kaldırın; gömülü harita veya Google Maps linki ekleyin.

## Önemli

1. **Onay kutusu hatası kullanıcıya hiç gösterilmiyor (gerçek JS hatası).**
   - `main.js:174` `consentError` hesaplanıyor, `main.js:179` yalnızca `aria-invalid` atanıyor; `showError("consent", ...)` çağrılmadığı için `iletisim.html:203`'teki `[data-error-for="consent"]` boş kalıyor. Kullanıcı yalnızca genel "Lütfen işaretli alanları kontrol edin." mesajını görüyor ve odak onay kutusuna atlıyor; nedeni görünmüyor.
   - Düzeltme: `showError("consent", consentError)` ekleyin (ve `aria-describedby` ile mesajı bağlayın).

2. **Form hata mesajları alanlara programatik olarak bağlı değil.**
   - `iletisim.html:169-203` formunda hiç `aria-describedby` yok; hata metinleri yalnızca `.field__error` içinde. `aria-invalid` tek başına mesajı okutmuyor. Bültende `index.html:609` vd. input'ta `aria-invalid`/`aria-describedby` hiç yok.
   - Düzeltme: her hata `<p>`'sine `id` verip ilgili alana `aria-describedby`, hata durumunda `aria-invalid="true"` ekleyin.

3. **Onay etiketi içinde link var (geçersiz HTML + tıklama çakışması).**
   - `iletisim.html:198-202`: `<label for="consent">` içindeki `<a href="yasal.html#kvkk">` tıklanınca hem onay kutusu değişiyor hem sayfa yasal metne gidiyor. HTML'de label, etiketlediği kontrol dışında etkileşimli öğe içeremez.
   - Düzeltme: KVKK linkini label dışına alın; onay metnini ayrı bir blok olarak verin.

4. **JS olmadan site büyük ölçüde boş görünüyor, mobil menü çalışmıyor.**
   - `.reveal { opacity: 0 }` (`style.css:1487-1493`) yalnızca `main.js:45-63` IntersectionObserver'ı ile açılıyor; JS yüklenemezse ürün kartları, SSS, istatistikler, formlar görünmez kalır. ≤820px'te `.nav__links { display:none }` (`style.css:1538-1551`) ve toggle JS'siz işlevsiz olduğundan gezinme imkânsız.
   - Düzeltme: `<html class="no-js">` + JS'te sınıfı kaldırma ve `.no-js .reveal { opacity:1; transform:none }`; menü için `<noscript>`/CSS fallback ekleyin.

5. **"7/24 müşteri desteği" iletişim saatleriyle çelişiyor.**
   - `hikayemiz.html:262` "7/24 Müşteri desteği hedefi" ↔ `iletisim.html:146-148` (Hafta içi 09:00–18:00, Cumartesi 10:00–14:00, Pazar kapalı).
   - Düzeltme: ifadeyi gerçek saatlerle değiştirin veya "e-posta ile 7/24 ulaşabilirsiniz" şeklinde netleştirin.

6. **"Koruyucu içermez" iddiası ürün kapsamıyla uyuşmuyor.**
   - Bu ifade yalnızca yavru köpek ambalajında geçiyor; `hikayemiz.html:159` ise tüm formüller için "koruyucu içermeyen formüllerle" diyerek genelliyor. Reklam/etiket uyumu riski.
   - Düzeltme: ifadeyi yalnızca ilgili ürüne indirgeyin veya tüm SKU'lar için teyit edin.

7. **Odak halkası kontrastı yetersiz.**
   - `style.css:88-92`: `outline: 3px solid #C9A227`. Ölçüm: krem zemine (`#FDFBF6`) 2,34:1, beyaza 2,42:1 — WCAG 2.2 (2.4.11) için gereken 3:1'in altında. Koyu yeşil zeminde 5,17:1 ile sorunsuz.
   - Düzeltme: açık zeminlerde koyu yeşil halka (`green-800`) veya iki tonlu halka kullanın.

8. **İletişim sayfası metinlerinde dilbilgisi hatası.**
   - `iletisim.html:163` "Formu doldurun, talebinizi ilgili ekibe ileten kadar takip edelim." anlamsız/bozuk. `iletisim.html:95` "en kısa sürede dönüş yapalım" da düzeltilmeli.
   - Düzeltme: "Formu doldurun; talebinizi ilgili ekibe ilettikten sonra süreci takip edelim." / "…size en kısa sürede dönüş yapacağız."

## Öneri

- **Filtre çubuğu:** `urunler.html:119` `aria-label` role'süz bir `div`'de olduğu için yok sayılıyor → `role="group"` ekleyin; sonuç sayısı (`:125`) canlı bölge değil, filtre değişince duyurulmuyor. Ayrıca düğmeler tek seçimli (`main.js:71-89`): "Köpek + Yavru" birleştirilemiyor; çoklu seçim bekleniyorsa JS buna göre güncellenmeli (testlerde de "Köpek=2, Yavru=2" doğrulanmış).
- **Besleme sekmeleri:** `urunler.html:415-419` `role="tab"` öğelerinde `aria-controls`/`id`, panellerde (`:422,437,452,467`) `aria-labelledby` ve roving `tabindex` yok; `main.js:93-116` yalnızca ←/→ destekliyor (Home/End yok). APG tab desenine tamamlayın.
- **Bülten hata durumu:** `main.js:141` `is-error` sınıfı ekliyor ama CSS'te yalnızca `.form-status.is-error` var (`style.css:1355`); `.newsletter__status.is-error` ekleyin ve input'a `aria-invalid` verin.
- **Metin kontrastı:** `.newsletter__note` (`style.css:1093`) 4,17:1, placeholder (`:1077`) 3,56:1, `.guide__note` (`:864-875`) 4,47:1 — AA 4,5:1 sınırının altında/çok yakınında; renkleri koyulaştırın.
- **"15 kg e"**: `index.html:224,255,286,317`; `urunler.html:144,165,186,207,257,295,333,371` — web'de yazım hatası gibi duruyor; "15 kg" veya "15 kg (net)" kullanın (℮ işareti ambalajda kalabilir).
- **"4 Yaş grubu ürünü"**: `index.html:456`; `hikayemiz.html:259` — 4 SKU = 2 tür × 2 yaş; "4 ürün çeşidi" veya "2 yaş grubu" yapın.
- **Kedi tüketim süresi tutarsız:** `urunler.html:409-410` "bir kedi için 3–5 ay" ↔ `:458-461` tablosu (45–65 g/gün → 15 kg ≈ 8–11 ay). Notu tabloyla uyumlu hale getirin.
- **Ürün adı tutarsızlığı:** "Tavuklu Lezzeti" (`index.html:276`; `urunler.html:181,314`) vs "Tavuklu" (`index.html:307`; `urunler.html:202,352`); paket adıyla tek isim kullanın.
- **Bayilik CTA'ları:** `urunler.html:260,298,336,374` → `iletisim.html#form`, ancak Konu "Genel bilgi" (`iletisim.html:184-189`) seçili geliyor; "Toptan & bayilik" ön seçili gelsin (query/hash parametresi).
- **Harita:** `iletisim.html:152-158` `role="img"` içeriği ekran okuyucudan gizlediği için "Temsili konum görseli" (`:157`) duyurulmuyor; gerçek gömülü harita veya harita linki tercih edin.
- **Sosyal/SEO:** `og:image` tüm sayfalarda göreli (`index.html:16`, `urunler.html:16`, `hikayemiz.html:16`, `iletisim.html:16`, `yasal.html:16`) ve ~1,3 MB PNG; mutlak `https` URL + 1200×630 optimize görsel kullanın.
- **Küçük ekran riski:** `.hl { white-space: nowrap }` (`style.css:133-138`) + `overflow: clip` (`style.css:372-378`, `:1111-1118`); ≤340 px'te (280 px katlanır ekran, 320 px eski telefon) "yardımcı olabiliriz?" ~303 px, "kurulmuş bir marka" ~316 px olduğundan kırpılma riski var. 480 px altında satır kırmaya izin verin.
- **Canlı doğrulama görünümü:** `style.css:1348` `:invalid` kırmızı çerçevesi, kullanıcı henüz göndermeden (ör. ad 1 karakterken) hata izlenimi veriyor; stili submit sonrası `.was-validated` sınıfına bağlayın.
- **Yayın hijyeni:** Kullanılmayan 4 büyük PNG (`assets/img/*.png`, ~9,8 MB), `preview/` ekran görüntüleri (~15 MB) ve `tools/` yayın kökünde; deploy dışına alın veya ayıklayın.
- **CSS temizliği:** `--gold-200` tanımlı değil (`style.css:505`, fallback'e güveniyor); `--gold-200: #F1E3BE` tanımlayın. `.brand__leaf { display:none }` ve `.contact-info > .info-card:last-child` gibi artık etkisiz kuralları gözden geçirin.

**Öncelik:** Kritik 1-3 → Önemli 1, 2, 4 → kalan Önemli/Öneri maddeleri.
