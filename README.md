# TechBot - IT Destek Asistanı

TechBot, kullanıcıların IT sorunlarını çözmelerine yardımcı olan bir Telegram botudur. Kullanıcılar sorunlarını bildirebilir, yeni çözümler ekleyebilir ve bilinmeyen soruları görüntüleyebilir.

## Özellikler

- 🤖 Sorun bildirme ve çözüm önerme
- 📝 Yeni çözüm ekleme
- 📊 Bilinmeyen soruları görüntüleme
- ⌨️ Kullanıcı dostu arayüz
- 🔄 Otomatik öğrenme sistemi

## Kurulum

1. Python 3.7 veya daha yüksek bir sürümü yükleyin
2. Gerekli paketleri yükleyin:
   ```bash
   pip install python-telegram-bot
   ```
3. Telegram Bot Token'ınızı alın:
   - [@BotFather](https://t.me/botfather) ile konuşun
   - `/newbot` komutunu kullanın
   - Bot adını ve kullanıcı adını belirleyin
   - Size verilen token'ı kopyalayın

4. Token'ı ayarlayın:
   ```bash
   # Windows
   set TELEGRAM_BOT_TOKEN=your_token_here
   
   # Linux/Mac
   export TELEGRAM_BOT_TOKEN=your_token_here
   ```

## Kullanım

1. Botu başlatın:
   ```bash
   python ItDesk.py
   ```

2. Telegram'da botunuzu bulun ve başlatın
3. Menüden istediğiniz işlemi seçin:
   - Sorun Bildir: Yaşadığınız sorunu bildirin
   - Yeni Çözüm Ekle: Bilgi tabanına yeni çözümler ekleyin
   - Bilinmeyen Sorular: Henüz çözümü olmayan soruları görüntüleyin
   - Çıkış: Botu kapatın

## Geliştirme

Bot iki ana dosyadan oluşur:
- `ItDesk.py`: Ana bot uygulaması
- `bilgi_tabani.py`: Bilgi tabanı ve ilgili fonksiyonlar

## Güvenlik

- Bot token'ınızı güvenli tutun
- Token'ı doğrudan kod içinde saklamak yerine çevre değişkeni olarak kullanın
- Düzenli olarak token'ı yenileyin

## Lisans

MIT License 