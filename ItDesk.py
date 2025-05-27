# TechBot - IT Destek Asistanı
# Bu dosya, Telegram üzerinden çalışan bir IT destek botunun ana kodudur.
# Kodun her bölümünde ne yaptığını açıklayan yorumlar eklenmiştir.

import os  # Ortam değişkenleriyle çalışmak için kullanılır
import logging  # Hata ve bilgi mesajlarını kaydetmek için kullanılır
from typing import Optional  # Fonksiyonlarda opsiyonel değerler için
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove  # Telegram API nesneleri
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler  # Telegram botu için gerekli modüller
from bilgi_tabani import cevapla, yeni_ifade_ekle, bilinmeyen_ifadeleri_getir  # Bilgi tabanı fonksiyonları

# Loglama ayarları (hata ve bilgi mesajlarını terminalde gösterir)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Konuşma adımlarını temsil eden sabitler (diyalog yönetimi için)
OGRETME, YANIT_BEKLEME = range(2)

# Ana menüde gösterilecek klavye butonları
MAIN_KEYBOARD = [['Sorun Bildir', 'Yeni Çözüm Ekle'], ['Bilinmeyen Sorular', 'Çıkış']]

# /start komutu ile çalışan, kullanıcıyı karşılayan fonksiyon
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Kullanıcıya hoş geldin mesajı ve ana menü klavyesi gönderilir
    keyboard = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        "TechBot'a Hoş Geldin! 👋\n\n"
        "Sorununuzu bildirmek için 'Sorun Bildir' düğmesine tıklayın.\n"
        "Yeni bir çözüm eklemek için 'Yeni Çözüm Ekle' düğmesini kullanın.\n"
        "Bilinmeyen soruları görmek için 'Bilinmeyen Sorular' düğmesine tıklayın.\n"
        "Çıkmak için 'Çıkış' düğmesini kullanın.",
        reply_markup=keyboard
    )

# Kullanıcı "Sorun Bildir" seçtiğinde çalışan fonksiyon
async def sorun_bildir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Kullanıcıdan yaşadığı sorunu yazmasını ister
    await update.message.reply_text(
        "Lütfen yaşadığınız sorunu detaylı bir şekilde yazın:"
    )
    return YANIT_BEKLEME  # Sonraki adımda yanıt bekleyecek

# Kullanıcıdan gelen sorunu bilgi tabanında arar ve yanıtlar
async def sorun_cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text  # Kullanıcının yazdığı metin
    yanit = cevapla(text)  # Bilgi tabanında arama yapılır
    await update.message.reply_text(yanit)  # Sonuç kullanıcıya gönderilir
    return ConversationHandler.END  # Diyalog biter

# Kullanıcı "Yeni Çözüm Ekle" seçtiğinde çalışan fonksiyon
async def yeni_cozum_ekle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Kullanıcıdan yeni bir sorun ifadesi ister
    await update.message.reply_text("Lütfen sorun ifadesini yazın:")
    return OGRETME  # Sonraki adımda öğretme beklenir

# Öğretme adımında, önce sorun ifadesi alınır
async def ogretme_yanit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['ifade'] = update.message.text  # Sorun ifadesi geçici olarak kaydedilir
    await update.message.reply_text("Şimdi bu sorunun çözümünü yazın:")
    return YANIT_BEKLEME  # Sonraki adımda çözüm beklenir

# Öğretme tamamlandığında, sorun ve çözüm bilgi tabanına eklenir
async def ogretme_tamamla(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    ifade = context.user_data.get('ifade')  # Daha önce alınan sorun ifadesi
    yanit = update.message.text  # Kullanıcının yazdığı çözüm
    # Sorun ve çözüm boş değilse bilgi tabanına eklenir
    if ifade and yeni_ifade_ekle(ifade, yanit):
        await update.message.reply_text("✅ Çözüm başarıyla eklendi!")
    else:
        await update.message.reply_text("❌ Çözüm eklenirken bir hata oluştu. Lütfen tekrar deneyin.")
    context.user_data.clear()  # Geçici veriler temizlenir
    return ConversationHandler.END  # Diyalog biter

# Bilinmeyen soruları listeleyen fonksiyon
async def bilinmeyen_sorular(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sorular = bilinmeyen_ifadeleri_getir()  # Bilinmeyen sorular alınır
    if sorular:
        mesaj = "Bilinmeyen Sorular:\n\n" + "\n".join(f"• {soru}" for soru in sorular)
        await update.message.reply_text(mesaj)
    else:
        await update.message.reply_text("Henüz bilinmeyen soru bulunmuyor.")

# Genel mesaj işleyici (ana menü dışındaki metinler için)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[int]:
    text = update.message.text.lower()  # Kullanıcıdan gelen metin
    if text == "çıkış":  # Kullanıcı çıkmak isterse
        await update.message.reply_text(
            "Görüşmek üzere! 👋"
        )
        return ConversationHandler.END
    yanit = cevapla(text)  # Bilgi tabanında arama yapılır
    await update.message.reply_text(yanit)
    return None

# Botun ana çalıştırma fonksiyonu
# Burada botun başlatılması, handler'ların eklenmesi ve Telegram'a bağlanması sağlanır

def main() -> None:
    """Bot'u başlatır."""
    # Telegram API anahtarı
    token = "7797161702:AAENmr-u4-fSleicXJXoB73rwporjEYrVxA"
    if not token:
        print("HATA: Telegram bot token'ı bulunamadı.")
        exit(1)
    # Bot uygulaması oluşturulur
    app = ApplicationBuilder().token(token).concurrent_updates(True).build()
    # Konuşma akışlarını yöneten handler (diyalog yönetimi)
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^Yeni Çözüm Ekle$'), yeni_cozum_ekle),
            MessageHandler(filters.Regex('^Sorun Bildir$'), sorun_bildir)
        ],
        states={
            OGRETME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ogretme_yanit)],
            YANIT_BEKLEME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ogretme_tamamla)]
        },
        fallbacks=[CommandHandler("start", start)]
    )
    # Komut ve mesaj işleyiciler eklenir
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex('^Bilinmeyen Sorular$'), bilinmeyen_sorular))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # Bot başlatılır
    logger.info("Bot başlatılıyor...")
    app.run_polling()

# Program doğrudan çalıştırılırsa bot başlatılır
if __name__ == "__main__":
    main()
