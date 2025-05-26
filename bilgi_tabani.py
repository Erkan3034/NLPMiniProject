from typing import Dict, List

# Bilgi tabanı
bilgi_tabani: Dict[str, str] = {
    "erkan turgut kimdir": "Erkan Turgut, ItDesk'in yöneticisi ve kurucularındadır. Kendisi Yapay Zeka alanında uzmanlaşmaya devam etmektedir.",
    "aslı aydın kimdir": "Aslı Aydın, ItDesk'in yöneticisi ve kurucularındadır. Kendisi Yapay Zeka alanında uzmanlaşmaya devam etmektedir.",
    "merhaba": "Merhaba! Ben TechBot, size teknik destek sunuyorum.",
    "nasılsın": "Ben iyiyim,Teşekkürler siz nasılsınız?",
    "teşekkürler": "Rica ederim,İyi günler dilerim.",
    "Bende iyiyim": "Bunu duyduğuma sevindim.",
    "tolgahan toy kimdir": "Tolgahan Toy, Bartın Üniversiteside Alanında Uzman bir Eğitim Görevlisidir.",
    "iyi günler": "İyi günler dilerim.",
    "yapay zeka nedir": "Yapay zeka, insan zekasının bilgisayarlar tarafından kopyalanmasıdır.",
    "yapay zeka nasıl çalışır": "Yapay zeka, veri ve algoritmaların birleştirilmesiyle çalışır.",
    "yapay zeka uygulamaları": "Yapay zeka, otomatik sınıflandırma, tahmin ve öneri sistemleri gibi uygulamalar için kullanılır.",
    "wifi çalışmıyor": "Modeminizi kapatıp tekrar açmayı deneyin.",
    "bilgisayar donuyor": "Arka background uygulamalarını kapatıp cihazı yeniden başlatın.",
    "şarj olmuyor": "Şarj kablonuzu ve priz bağlantınızı kontrol edin.",
    "uygulamalarım açılmıyor": "Uygulamalarınızı tekrar açın veya uygulama ayarlarını kontrol edin.",
    "yavaşladı": "Disk temizliği yapın ve başlangıç uygulamalarını sınırlandırın.",
    "dosya yüklenmiyor": "Dosya yüklemek için internet bağlantınızı kontrol edin.",
    "ekran titriyor": "Monitör kablosunu kontrol et.",
}

bilinmeyen_ifadeler: List[str] = []

def cevapla(metin: str) -> str:
    """
    Verilen metne göre bilgi tabanından yanıt döndürür.
    
    Args:
        metin (str): Kullanıcının sorduğu sorun
        
    Returns:
        str: Bilgi tabanından bulunan yanıt veya bilinmeyen ifade mesajı
    """
    metin = metin.lower().strip()
    for anahtar, yanit in bilgi_tabani.items():
        anahtar_kelimeler = anahtar.lower().split()
        for kelime in anahtar_kelimeler:
            if kelime in metin:
                return yanit
    if metin not in bilinmeyen_ifadeler:
        bilinmeyen_ifadeler.append(metin)
    return "Bu konuda bilgim yok. Yeni bir çözüm öğretmek ister misiniz? (evet/hayır)"

def yeni_ifade_ekle(ifade: str, yanit: str) -> bool:
    """
    Bilgi tabanına yeni bir ifade ve yanıt ekler.
    
    Args:
        ifade (str): Eklenecek sorun ifadesi
        yanit (str): Eklenecek çözüm yanıtı
        
    Returns:
        bool: İşlemin başarılı olup olmadığı
    """
    try:
        ifade = ifade.lower().strip()
        yanit = yanit.strip()
        if not ifade or not yanit:
            return False
        bilgi_tabani[ifade] = yanit
        if ifade in bilinmeyen_ifadeler:
            bilinmeyen_ifadeler.remove(ifade)
        return True
    except Exception:
        return False

def bilinmeyen_ifadeleri_getir() -> List[str]:
    """Bilinmeyen ifadelerin listesini döndürür."""
    return bilinmeyen_ifadeler.copy() 