import os
import logging
from typing import Optional
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from bilgi_tabani import cevapla, yeni_ifade_ekle, bilinmeyen_ifadeleri_getir

# Loglama ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Konuşma durumları
OGRETME, YANIT_BEKLEME = range(2)

# Klavye düğmeleri
MAIN_KEYBOARD = [['Sorun Bildir', 'Yeni Çözüm Ekle'], ['Bilinmeyen Sorular', 'Çıkış']]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bot başlatıldığında çalışacak komut."""
    keyboard = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        "TechBot'a Hoş Geldin! 👋\n\n"
        "Sorununuzu bildirmek için 'Sorun Bildir' düğmesine tıklayın.\n"
        "Yeni bir çözüm eklemek için 'Yeni Çözüm Ekle' düğmesini kullanın.\n"
        "Bilinmeyen soruları görmek için 'Bilinmeyen Sorular' düğmesine tıklayın.\n"
        "Çıkmak için 'Çıkış' düğmesini kullanın.",
        reply_markup=keyboard
    )



async def sorun_bildir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Kullanıcıdan sorun girişi alır."""
    await update.message.reply_text(
        "Lütfen yaşadığınız sorunu detaylı bir şekilde yazın:"
    )
    return YANIT_BEKLEME



async def sorun_cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Kullanıcıdan alınan sorunu bilgi tabanında arar ve yanıtlar."""
    text = update.message.text
    yanit = cevapla(text)
    await update.message.reply_text(yanit)
    return ConversationHandler.END



async def yeni_cozum_ekle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Yeni çözüm ekleme sürecini başlatır."""
    await update.message.reply_text("Lütfen sorun ifadesini yazın:")
    return OGRETME



async def ogretme_yanit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Öğretme sürecinde sorun ifadesini alır ve çözüm ister."""
    context.user_data['ifade'] = update.message.text
    await update.message.reply_text("Şimdi bu sorunun çözümünü yazın:")
    return YANIT_BEKLEME

async def ogretme_tamamla(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Öğretme sürecini tamamlar ve bilgi tabanına ekler."""
    ifade = context.user_data.get('ifade')
    yanit = update.message.text
    if ifade and yeni_ifade_ekle(ifade, yanit):
        await update.message.reply_text("✅ Çözüm başarıyla eklendi!")
    else:
        await update.message.reply_text("❌ Çözüm eklenirken bir hata oluştu. Lütfen tekrar deneyin.")
    context.user_data.clear()
    return ConversationHandler.END

async def bilinmeyen_sorular(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bilinmeyen soruları listeler."""
    sorular = bilinmeyen_ifadeleri_getir()
    if sorular:
        mesaj = "Bilinmeyen Sorular:\n\n" + "\n".join(f"• {soru}" for soru in sorular)
        await update.message.reply_text(mesaj)
    else:
        await update.message.reply_text("Henüz bilinmeyen soru bulunmuyor.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[int]:
    """Ana mesaj işleyici."""
    text = update.message.text.lower()
    
    if text == "çıkış":
        await update.message.reply_text(
            "Görüşmek üzere! 👋"
        )
        return ConversationHandler.END
    
    yanit = cevapla(text)
    await update.message.reply_text(yanit)
    return None

def main() -> None:
    """Bot'u başlatır."""
    # Token'ı sadece çevre değişkeninden al
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("HATA: TELEGRAM_BOT_TOKEN çevre değişkeni tanımlı değil. Lütfen .env dosyasına veya sistem ortamına ekleyin.")
        exit(1)
    # Uygulama oluştur
    app = ApplicationBuilder().token(token).build()
    
    # Konuşma işleyici
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
    
    # İşleyicileri ekle
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex('^Bilinmeyen Sorular$'), bilinmeyen_sorular))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Bot'u başlat
    logger.info("Bot başlatılıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
