"""Compose yasal.html using the shared header/footer from index.html."""
import re, io

ROOT = r"C:\Users\erhan\Documents\ai\biyopet"
with io.open(ROOT + r"\index.html", encoding="utf-8") as f:
    index = f.read()

prefix = index[: index.index('<main id="icerik">')]
suffix = index[index.index("</main>") + len("</main>"):]

# Head adjustments
prefix = re.sub(r"<title>.*?</title>", "<title>Yasal Metinler | Biyopet</title>", prefix, count=1, flags=re.S)
prefix = re.sub(
    r'<meta name="description" content="[^"]*">',
    '<meta name="description" content="Biyopet KVKK aydınlatma metni, gizlilik politikası ve çerez politikası.">',
    prefix,
    count=1,
)
prefix = re.sub(r"<meta property=\"og:title\"[^>]*>", '<meta property="og:title" content="Yasal Metinler | Biyopet">', prefix)
prefix = re.sub(r"<meta property=\"og:description\"[^>]*>", '<meta property="og:description" content="Biyopet KVKK aydınlatma metni, gizlilik politikası ve çerez politikası.">', prefix)
# Nav: drop active state from home
prefix = prefix.replace(
    '<a class="nav__link is-active" href="index.html" aria-current="page">Ana Sayfa</a>',
    '<a class="nav__link" href="index.html">Ana Sayfa</a>',
)
# Keep the announcement/header, just mark nothing active.

main = r'''<main id="icerik">
    <section class="page-hero">
      <div class="container">
        <nav class="breadcrumb" aria-label="Site yolu">
          <a href="index.html">Ana Sayfa</a>
          <svg aria-hidden="true"><use href="#i-chevron"/></svg>
          <span aria-current="page">Yasal Metinler</span>
        </nav>
        <div class="page-hero__inner">
          <h1>Yasal metinler</h1>
          <p class="page-hero__lead">
            Kişisel verilerinizin nasıl işlendiği, gizliliğin nasıl korunduğu ve sitede
            kullanılan çerezler hakkında bilgi edinin.
          </p>
          <p class="legal__updated">Son güncelleme: Ekim 2026</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="legal">
          <div class="guide__note">
            <svg aria-hidden="true"><use href="#i-info"/></svg>
            <span>Bu metinler genel bilgilendirme amacıyla hazırlanmış örnek metinlerdir.
              Yayına almadan önce hukuk danışmanınızla birlikte şirket bilgilerinize ve
              yürürlükteki mevzuata göre uyarlanmalıdır.</span>
          </div>

          <nav class="legal__toc" aria-label="Yasal metin başlıkları">
            <a href="#kvkk">KVKK Aydınlatma Metni</a>
            <a href="#gizlilik">Gizlilik Politikası</a>
            <a href="#cerez">Çerez Politikası</a>
          </nav>

          <article id="kvkk">
            <h2>KVKK Aydınlatma Metni</h2>
            <p>
              6698 sayılı Kişisel Verilerin Korunması Kanunu ("KVKK") kapsamında, veri sorumlusu
              <strong>Biyopet</strong> olarak kişisel verilerinizin işlenmesine ilişkin olarak
              sizi bilgilendirmek isteriz.
            </p>

            <h3>İşlenen kişisel veriler</h3>
            <ul>
              <li>Kimlik ve iletişim verileri: ad, soyad, e-posta adresi, telefon numarası.</li>
              <li>Talep verileri: iletişim formu ve e-posta yoluyla ilettiğiniz mesaj içeriği ve konu başlığı.</li>
              <li>İşlem güvenliği verileri: IP adresi, tarayıcı ve cihaz bilgileri, çerez kayıtları.</li>
            </ul>

            <h3>İşleme amaçları</h3>
            <ul>
              <li>Taleplerinizin ve sorularınızın yanıtlanması,</li>
              <li>Ürün ve beslenme bilgilendirmesi yapılması,</li>
              <li>Toptan ve bayilik süreçlerinin yürütülmesi,</li>
              <li>Site güvenliğinin sağlanması ve hukuki yükümlülüklerin yerine getirilmesi.</li>
            </ul>

            <h3>Hukuki sebepler</h3>
            <p>
              Veriler; KVKK'nın 5. maddesinin 2. fıkrasında yer alan "sözleşmenin kurulması veya
              ifasıyla doğrudan ilgili olması", "veri sorumlusunun hukuki yükümlülüğünü yerine
              getirebilmesi" ve "meşru menfaat" hukuki sebeplerine dayanılarak işlenir. Açık rıza
              gerektiren hâllerde ayrıca rızanız alınır.
            </p>

            <h3>Aktarım ve saklama</h3>
            <p>
              Veriler; barındırma, e-posta, kargo ve muhasebe gibi hizmet aldığımız tedarikçilerle,
              hizmetin gerektirdiği ölçüde ve gizlilik yükümlülükleri çerçevesinde paylaşılabilir.
              Veriler, işleme amacının gerektirdiği süre ve mevzuatta öngörülen saklama süreleri
              boyunca muhafaza edilir.
            </p>

            <h3>Haklarınız</h3>
            <p>KVKK'nın 11. maddesi kapsamında; kişisel verilerinizin işlenip işlenmediğini öğrenme,
              işlenmişse buna ilişkin bilgi talep etme, amacına uygun kullanılıp kullanılmadığını
              öğrenme, eksik veya yanlış işlenmiş verilerin düzeltilmesini, silinmesini veya yok
              edilmesini isteme ve işlemeye itiraz etme haklarına sahipsiniz. Başvurularınızı
              <a href="mailto:info@biyopet.com">info@biyopet.com</a> adresine iletebilirsiniz.</p>
          </article>

          <article id="gizlilik">
            <h2>Gizlilik Politikası</h2>
            <p>
              Bu politika, Biyopet web sitesini ziyaret eden ve iletişim kanallarımızı kullanan
              kişilerin bilgilerinin nasıl toplandığını, kullanıldığını ve korunduğunu açıklar.
            </p>

            <h3>Toplanan bilgiler</h3>
            <p>
              Sitemizi ziyaret ettiğinizde teknik veriler (IP adresi, tarayıcı türü, ziyaret
              edilen sayfalar) ve iletişim formunu doldurduğunuzda paylaştığınız bilgiler
              toplanabilir. Bilgiler, yalnızca belirtilen amaçlar doğrultusunda kullanılır.
            </p>

            <h3>Bilgilerin kullanımı</h3>
            <ul>
              <li>İletişim taleplerinizin yanıtlanması,</li>
              <li>Hizmet kalitesinin ve site deneyiminin iyileştirilmesi,</li>
              <li>Yasal yükümlülüklerin yerine getirilmesi.</li>
            </ul>

            <h3>Paylaşım ve güvenlik</h3>
            <p>
              Bilgileriniz, açık rızanız olmadan üçüncü kişilerle pazarlama amacıyla paylaşılmaz.
              Verilerin yetkisiz erişime karşı korunması için teknik ve idari önlemler uygulanır;
              ancak internet üzerinden iletimin tamamen güvenli olduğu garanti edilemez.
            </p>

            <h3>Üçüncü taraf bağlantılar</h3>
            <p>
              Site, sosyal medya platformlarına bağlantılar içerebilir. Bu platformların gizlilik
              uygulamaları kendi politikalarına tabidir.
            </p>
          </article>

          <article id="cerez">
            <h2>Çerez Politikası</h2>
            <p>
              Çerezler, ziyaret ettiğiniz web siteleri tarafından tarayıcınıza kaydedilen küçük
              metin dosyalarıdır. Siteyi daha işlevsel ve güvenli hâle getirmek için çerezlerden
              yararlanabiliriz.
            </p>

            <h3>Kullanılan çerez türleri</h3>
            <ul>
              <li><strong>Zorunlu çerezler:</strong> Sitenin temel işlevleri ve güvenliği için gereklidir.</li>
              <li><strong>Performans ve analitik çerezleri:</strong> Sayfaların nasıl kullanıldığını anonim olarak ölçmeye yardımcı olur.</li>
              <li><strong>İşlevsel çerezler:</strong> Dil ve tercih gibi ayarların hatırlanmasını sağlar.</li>
            </ul>

            <h3>Çerezlerin yönetimi</h3>
            <p>
              Tarayıcı ayarlarınızdan çerezleri silebilir veya engelleyebilirsiniz. Zorunlu
              çerezlerin devre dışı bırakılması, sitenin bazı bölümlerinin beklendiği gibi
              çalışmamasına neden olabilir.
            </p>

            <h3>Sorularınız</h3>
            <p>
              Gizlilik ve çerez uygulamalarımızla ilgili sorularınız için
              <a href="mailto:info@biyopet.com">info@biyopet.com</a> adresinden bize ulaşabilirsiniz.
            </p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section--cream section--tight">
      <div class="container">
        <div class="band__inner" style="padding:0">
          <div class="band__text">
            <svg aria-hidden="true"><use href="#i-mail"/></svg>
            <div>
              <strong>Verilerinizle ilgili bir talebiniz mi var?</strong>
              <span>Başvurularınızı info@biyopet.com adresine iletebilirsiniz.</span>
            </div>
          </div>
          <a class="btn btn--primary" href="iletisim.html">İletişime Geçin<svg aria-hidden="true"><use href="#i-arrow"/></svg></a>
        </div>
      </div>
    </section>
  </main>'''

with io.open(ROOT + r"\yasal.html", "w", encoding="utf-8", newline="") as f:
    f.write(prefix + main + suffix)
print("yasal.html written", len(prefix + main + suffix))
