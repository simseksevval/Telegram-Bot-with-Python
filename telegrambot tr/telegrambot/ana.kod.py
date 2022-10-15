import logging
import random  # rastgele sayılar almak için
import psutil
import os  # dosya işlemleri için bir modül
import time  # time.sleep için kullandım
import zipfile  # dosya zipleme için
from datetime import datetime # kullanıcının dosya, ses kaydı ve fotoğraf gönderebilmesi için
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Poll  #rastgele soru sormak için

# Enable logging (you will know when (and why) things don't work as expected):
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def size(byte):
    # this the function to convert bytes into more suitable reading format.
    # Suffixes for the size
    for x in ["B", "KB", "MB", "GB", "TB"]:
        if byte < 1024:
            return f"{byte:.2f}{x}"
        byte = byte/1024

# Fonksiyonumuzun ismini yazarak iki parametre eklememiz gerekli; update ve context.

#botun başlaması için /start komutu çalıştırıldığında aşağıdaki bilgiler ekrana gelir.
def start_command(update, context):
    update.message.reply_text('Merhaba Ben InnoBot!')
    time.sleep(3)
    update.message.reply_text('''Bana çeşitli komutlar vererek beni yönetebilirsin.
- /start komutu ile çalışmaya başlar,
- /havadurumusorgula komutu ile sana dünya başkentlerindeki hava durumlarını rastgele olarak gönderebilirim.
- /DISKbilgilerinioku komutu ile çalıştığın bilgisayarın diskine ait değerleri,
- /CPUbilgilerinioku komutu ile CPU'ya ait değerleri,
- ve /RAMbilgilerinioku komutu ile de bilgisayarının RAM'ine ait bilgileri görüntüleyebilirsin.
- /banasorusor komutunu yazarsan sana bir quiz yaparım ve rastgele 2 sayı gönderip bunları toplamanı isterim.
- /dosyaislemleri komutuyla pek çok dosya işlemi yapabilirsin. Yapabileceğin işlemleri görmek için bu komutu yazman yeterli olacak, böylece sana bir bilgilendirme mesajı göndereceğim.
- İstersen bana herhangi bir komut yazmadan ses kaydı, fotoğraf ve dosya gönderebilirsin,
- Ve son olarak InnoChannel adlı bir grubumuz var ve her saat bu gruba bir fıkra yazıyorum. Grubumuza katılmak istersen kapımız her zaman açık :)
Şimdi istediğin komuttan başlayabilirsin seçim senin :)''')

    
# Bu fonksiyon disk bilgisini okur ve ekrana yazdırır.
def disk_bilgisi(update, context):
    diskTotal = int(psutil.disk_usage('/').total/(1024*1024*1024))
    diskUsed = int(psutil.disk_usage('/').used/(1024*1024*1024))
    diskAvail = int(psutil.disk_usage('/').free/(1024*1024*1024))
    diskPercent = psutil.disk_usage('/').percent
    msg = '''
# Disk Bilgisi (HDD/SSD)
Toplam = {} GB
Kullanılan = {} GB
Boş = {} GB
Kullanım Oranı = % {}'''.format(diskTotal, diskUsed, diskAvail, diskPercent)
    update.message.reply_text(msg)


# Bu fonksiyon CPU bilgisini okur ve ekrana yazdırır.
def cpu_bilgisi(update, context):
    cpuUsage = psutil.cpu_percent(interval=1)
    msg = '''
# CPU Bilgisi
CPU Kullanım Oranı = % {} '''.format(cpuUsage)
    update.message.reply_text(msg)


# Bu fonksiyon RAM bilgisini okur ve ekrana yazdırır.
def ram_bilgisi(update, context):
    ramTotal = int(psutil.virtual_memory().total/(1024*1024))  # GB
    ramUsage = int(psutil.virtual_memory().used/(1024*1024))  # GB
    ramFree = int(psutil.virtual_memory().free/(1024*1024))  # GB
    ramUsagePercent = psutil.virtual_memory().percent
    msg = '''
# RAM Bilgisi
Toplam = {} MB
Kullanılan = {} MB
Boş  = {} MB
Kullanım Oranı = % {} \n'''.format(ramTotal, ramUsage, ramFree, ramUsagePercent)
    update.message.reply_text(msg)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

#Bu fonksiyon InnoChannel grubuna 283. satırda belirlendiği gibi saatte bir rastgele fıkra gönderir.
def fikra_yap(context: CallbackContext):
    context.bot.send_message(chat_id='type channeel id here (putting -100 per)',
                             text=random.choice(
                                 ['''Akıl hastanesinde her hasta kendisini mısır tanesi zannediyor ve zıplıyormuş. Doktorlar bir tanesinin kenarda öylece durduğunu görmüş ve onun düzeldiğini zannetmişler. Yanına gitmiş ve; -Sen neden zıplamıyorsun, mısır tanesi değil misin? Deli adam hiç hareket etmeden; -Ben tavaya yapıştım…''',
                                  '''Adam aldığı bir daktiloyu bozuk diye geri vermek istemiş. Satıcı; -Bozuk değil, dün aldığınızda gayet sağlamdı. Adam; -Bu daktiloda saat yazamıyorum iki tane “A” yok…''',
                                  '''Üniversiteye kayıt olmak için giden gence Müdür sorar; -Adın ne yavrum? +Memememehmet Yayayayakup… -Kekeme misin evladım? +Hayır hocam babam kekemeydi. Nüfusa o kayıt ettirdi.''',
                                  '''Küçük çocuk, keman dersi için evde prova yapıyor, babası da oturmuş gazete okuyordu. Evin köpeği de çocuğun kemanından çıkan melodilere havlayarak eşlik ediyordu. Bu gürültüde babanın gazete okuması mümkün mü? Bir duruyor, iki duruyor, ama ne çocuk keman çalmayı ne de öteki havlamayı kesiyordu.  En sonunda baba, oğluna seslendi: -Oğlum, şunun bilmediği bir parça çalsana!''',
                                  ''' Temel iyice yaşlanmış, yaş doksan beş olmuş. Bir gün Azrail çıkagelmiş. Temel, ' Ne yapsam da paçayı yırtsam' diye düşünmeye başlamış. 'Hah buldum. Çocuk taklidi yapayım, beni tanımasın demiş' Azrail iyice yaklaşınca başlamış ağlamaya; ”Ingaa! Ingaa!..” Azrail Temel'in kulağına eğilmiş ve şöyle demiş;- “Atta! Atta!..”''']))


#Bu fonksiyon /havadurumusorgula komutu çalıştırıldığında rastgele bir havadurumu gönderir.
def havadurumusorgula(update, context):
    update.message.reply_text(text=random.choice(
        ["Varşova : Bugün hava güneşli!",
         "Tiflis : Hava 25 derece, parçalı bulutlu.",
         "Londra : Bugün hava yağmurlu, sağanak yağış bekleniyor.",
         "Ankara : Bugün hava yağmurlu, dolu yağma riski yüksek.",
         "Washington : Bugün hava sıcaklığı mevsim normallerinin üzerinde.",
         "Moskova : Hava sıcaklığı -5 derece, kar yağışı bekleniyor."]))


#Bu fonksiyon kodlarda tanımlı olmayan bir komut girildiğinde uyarı verir.
def wrong_command(update, context):
    update.message.reply_text(
        text="Kodlarımda tanımlı olmayan bir komut girdiniz. Lütfen başka bir komut giriniz :)")


#Bu fonksiyon /dosyaislemleri komutu yazıldığında ekrana aşağıdaki bilgileri yazdırır.
def dosyaislemleri(update, context):
    update.message.reply_text(text=''' 
Dosya işlemlerine hoşgeldin. Aşağıda listelediğim komutlarla istediğin dosya işlemini gerçekleştirebilirsin :)
- /dosyamial komutuyla bana istediğin herhangi bir dosyanı gönderebilirsin.
- /txtdosyagonder komutu ile sana elimdeki txt dosyaları arasından rastgele birini gönderirim,
- /pdfdosyagonder komutu ile sana elimdeki pdf dosyaları arasından rastgele birini gönderirim,
- /ziple komutunun yanına çalıştığın dizindeki dosyalardan birinin ismini yazıp bana gönderirsen o dosyayı senin için ziplerim,
- /5saniyesonraresimgonder komutu ile sana bazı resimleri ve resimlere ait bilgileri 5 saniye sonra gönderirim.''')


#Bu fonksiyon /txtdosyagonder komutu yazıldığında ekrana aşağıdaki belgelerden rastgele birini gönderir.
def txt_gonder(update, context):
    update.message.reply_text(
        text="Şimdi sana IMDB puanı en yüksek filmlerden birini gönderiyorum. Umarım keyifle izlersin. İyi seyirler :)")
    time.sleep(2)
    chat_id = update.message.chat_id
    txt1 = open('txt1.txt', 'r')
    txt2 = open('txt2.txt', 'r')
    txt3 = open('txt3.txt', 'r')
    txt4 = open('txt4.txt', 'r')

    txt_dosya = random.choice([txt1, txt2, txt3, txt4])
    context.bot.send_document(chat_id, txt_dosya)


#Bu fonksiyon /pdfdosyagonder komutu yazıldığında ekrana aşağıdaki belgelerden rastgele birini gönderir.
def pdf_gonder(update, context):
    update.message.reply_text(
        text="Şimdi sana yapay zeka ile oluşturulmuş, gerçek olmayan insan resimlerinden birini pdf dosyası olarak gönderiyorum.")
    chat_id = update.message.chat_id
    pdf1 = open('avatar1.pdf', 'rb')
    pdf2 = open('avatar2.pdf', 'rb')
    pdf3 = open('avatar3.pdf', 'rb')
    pdf4 = open('avatar4.pdf', 'rb')

    pdf_dosya = random.choice([pdf1, pdf2, pdf3, pdf4])
    time.sleep(2)
    context.bot.send_document(chat_id, pdf_dosya)


#Bu fonksiyon /rastgeleresimgonder komutu yazıldığında ekrana aşağıdaki resimlerden rastgele birini, bilgileriyle beraber 5 saniye sonra gönderir.
def rastgeleresim(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text(
        text="Sana 5 saniye sonra Güneş sistemindeki gezegenlerden birinin resmini ve o gezegen hakkında kısa birkaç bilgi göndereceğim.")
    time.sleep(5)
    png1 = open('jupyter.png', 'rb')
    png2 = open('mars.png', 'rb')
    png3 = open('mercury.png', 'rb')
    png4 = open('neptune.png', 'rb')
    png5 = open('saturn.png', 'rb')
    png6 = open('uranus.png', 'rb')
    png7 = open('venus.png', 'rb')
    png8 = open('earth.png', 'rb')

    photo = random.choice([png1, png2, png3, png4, png5, png6, png7, png8])
    if photo == png1:
        update.message.reply_text(
            text="Jüpiter, Güneş sistemimizdeki en büyük gezegendir. Hatta o kadar büyüktür ki içine 1321 Dünya sığabilir. Toplam 79 uydusu vardır. Adını Roma mitolojisindeki tanrıların en büyüğü olan Jüpiter'den alır.")
    elif photo == png2:
        update.message.reply_text(text="Mars, en fazla sayıda uzay aracının gönderildiği (50 civarında) gezegendir. Mars’ın kırmızı görünmesinin nedeni esas nedeni Mars kayalarında, toprağında ve atmosferdeki tozda bulunan demirin oksitlenmesi sonucu renk değiştirmesidir bu yüzden 'Kızıl Gezegen' de denir. Roma mitolojisindeki savaş tanrısı Mars'a ithafen adlandırılmıştır.")
    elif photo == png3:
        update.message.reply_text(
            text="Merkür, adını tanrıların habercisi Roma tanrısı Merkür'den alır. Bilinen hiç doğal uydusu yoktur. Güneşe en yakın gezegen olan Merkür’ün sıcaklığı 450 dereceye kadar ulaşılabilmektedir. ")
    elif photo == png4:
        update.message.reply_text(text="Neptün, Güneş Sistemi'nin sekizinci, Güneş'e en uzak ve katı yüzeyi bulunmayan gezegenidir. Adını Roma deniz tanrısı Neptunus'ten alan gezegen, Güneş Sistemi'nde çapına göre en büyük dördüncü, kütlesine göre ise en büyük üçüncü gezegendir. Dünya'dan 17 kat fazla kütlesiyle, ikizi sayılabilecek Uranüs'ten biraz daha büyük ve daha yoğundur. Jüpiter’deki rüzgarlardan 3 kat Dünya’daki rüzgarlardan ise 9 kat daha şiddetli rüzgarlar Neptün Gezegeninde meydana gelmektedir.")
    elif photo == png5:
        update.message.reply_text(text="Satürn, Güneş Sisteminin Güneş'e yakınlık sırasına göre 6. gezegenidir.  Adını Yunan mitolojisindeki Kronos'tan alır. Büyüklük açısından Jüpiter'den sonra ikinci sırada gelmesine rağmen yoğunluğu çok düşüktür. Hatta o kadar düşüktür ki Satürn'ün sığabileceği kadar büyük bir deniz olsa, denizin üstünde yüzebilirdi.")
    elif photo == png6:
        update.message.reply_text(text="Uranüs, Güneş Sisteminin Güneş'ten uzaklık sıralamasına göre 7. gezegenidir. Adını Yunan mitolojisindeki gökyüzü tanrısı Uranos'tan alır. Uranüs’ün oluşmasından hemen sonra Dünya boyutundaki bir gezegenle çarpışmasından kaynaklandığı düşünülen olağandışı bir eğime sahiptir.")
    elif photo == png7:
        update.message.reply_text(text="Venüs, Güneş Sisteminde, Güneş'e uzaklık bakımından ikinci sıradaki, sıcaklık bakımından da birinci sıradaki gezegendir. Güneşe uzaklık bakımından ikinci sırada olmasına rağmen en sıcak gezegen olmasının nedeni de atmosferinin gelen güneş ışınlarının dışarı çıkmasına izin vermemesidir. Bu gezegen adını Eski Roma tanrıçası Venüs'ten alır. Kendi ekseni etrafında, Güneş Sistemi'ndeki diğer tüm gezegenlerin aksi istikametinde döner.")
    elif photo == png8:
        update.message.reply_text(text="Diğer yedi Gezegen arasında ismi mitolojiden gelmeyen tek gezegen üzerinde yaşadığımız Dünya’dır. Şu an için üzerinde yaşam ve sıvı su barındırdığı bilinen tek astronomik cisimdir. Dünya’nın dönüşü her yüzyılda yaklaşık 17 ms yavaşlamaktadır. Diğer bir ifadeyle gün süresi uzamaktadır. Güneş Sistemi’ndeki birçok gezegende atmosfer var olmasına rağmen nefes alabileceğimiz tek atmosfer Dünya’da bulunmaktadır.")
    context.bot.send_photo(chat_id, photo)


#Bu fonksiyon /ziple komutunun yanına bir dosya ismi yazıldığında, ismi yazılan dosyayı zipleyip gönderir.
def ziple(update, context):
    chat_id = update.message.chat_id
    try:
        tam_dosya_adi = " ".join(context.args)
        if len(context.args) == 0:
            update.message.reply_text(text="Üzgünüm, dosya adını girmediniz.")
        else:
            dosya_adi = ".".join(tam_dosya_adi.split(".")[:-1])
            dosya_boyutu = os.path.getsize(tam_dosya_adi)
            if dosya_boyutu >= 1024*1024:
                update.message.reply_text(
                    text="Üzgünüm, dosyanız 1 MB'den büyük.")
            else:
                update.message.reply_text(text='''İşte ziplenmiş dosyan! :)''')
                zip_dosya_adi = f'{dosya_adi}.zip'
                # Var olan bir zip arşivine yeni bir dosya eklemek için “a” parametresini kullanıyoruz. (a=append)
                zip = zipfile.ZipFile(zip_dosya_adi, 'a') # w yazarsak dosyanın içindeki verileri silip üzerine ekler
                zip.write(tam_dosya_adi)
                zip.close()
                dosyamiac = open(zip_dosya_adi, 'rb')
                context.bot.send_document(chat_id, dosyamiac)
    except OSError:
        update.message.reply_text(text="Üzgünüm, böyle bir dosya bulamadım.")
    

#Bu fonksiyon /dosyamial komutunun yanına bir dosya ismi yazıldığında ismi yazılan belgenin aynısını gönderir.
def dosyamial(update, context):
      dosyaadi = " ".join(context.args)
      if ".".join(dosyaadi.split(".")[:-1]):
          update.message.reply_text(text=f'"{dosyaadi}" dosyanı aldım! İşte dosyan:')
          dosyaac = open(dosyaadi, 'rb')
          chat_id = update.message.chat_id
          context.bot.send_document(chat_id, dosyaac)  
      elif len(context.args) == 0:
          update.message.reply_text(
              text="Üzgünüm, dosya adını girmediniz.Lütfen dosya adını /dosyamial komutunun yanına yazarak tekrar deneyiniz.")
      elif OSError:
          update.message.reply_text(text="Üzgünüm, böyle bir dosya bulamadım.")
          

#Bu fonksiyon /banasorusor komutu yazıldığında ekrana rastgele 2 sayı gönderir ve bu sayıların toplamını sorar.
def banasorusor(update, context):
    update.message.reply_text(
        text="Şimdi sana 2 sayı gönderiyorum ve bu sayıları toplamanı istiyorum. ")
    time.sleep(2)
    x = random.randrange(100)
    y = random.randrange(100)
    questions = [str(random.randrange(100)), str(
        x+y), str(random.randrange(100)), str(random.randrange(100))]

    message = update.effective_message.reply_poll(
        f"{x} + {y} işleminin sonucu kaçtır ?", questions, type=Poll.QUIZ, correct_option_id=1)

    payload = {
        message.poll.id: {"chat_id": update.effective_chat.id, "message_id": message.message_id}}
    context.bot_data.update(payload)


#Bu fonksiyon, bota ses kaydı gönderildiğinde ses kaydının aynısını tekrar gönderir.
def ses_kaydi(update, context):
    chat_id = update.message.chat_id
    ses_kaydi = context.bot.get_file(update.message.voice.file_id)
    zaman = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    ses_kaydi.download(f"{zaman}.ogg")
    update.message.reply_text('Sesli mesajını aldım!')
    context.bot.send_document(chat_id, open(f"{zaman}.ogg", 'rb'))
    
    
#Bu fonksiyon, bota fotoğraf gönderildiğinde fotoğrafın aynısını tekrar gönderir.    
def take_photo(update, context):
    chat_id = update.message.chat_id
    file = update.message.photo[0].file_id 
    obj = context.bot.get_file(file)
    zaman = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    obj.download(f"{zaman}.png") 
    update.message.reply_text("Gönderdiğin görseli aldım!")
    context.bot.send_document(chat_id, open(f"{zaman}.png", 'rb'))

    
#Bu fonksiyon, bota dosya gönderildiğinde dosyanın aynısını tekrar gönderir.  
def tel_dosya_gonderme(update, context):
     chat_id = update.message.chat_id
     file = update.message.document
     obj = context.bot.get_file(file)
     zaman = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
     obj.download(f"{zaman}.pptx") 
     update.message.reply_text("Gönderdiğin dosyayı aldım!")
     context.bot.send_document(chat_id, open(f"{zaman}.pptx", 'rb'))
 

def main():

    token = "type token here" #API id
    
    # Dispatcher’ın yardımı ile botumuzla iletişimi sağlayabileceğiz
    updater = Updater(token, use_context=True) # Updater, botla etkileşime geçmek için kod yazmamızı sağlayan güncelleyici.
    dp = updater.dispatcher # updater'dan dispatcher'ı aldık bunu dp isimli değişkene atadık

    j = updater.job_queue
    j.run_repeating(fikra_yap, interval=3600, first=5) # run_repeating can help to do any periodic calls for your Telegram Bot.

    # komutların handlelarini ekle
    # with dispatcher.add_handler you associate a specific function to run when the bot receive a message
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("DISKbilgilerinioku", disk_bilgisi))
    dp.add_handler(CommandHandler("CPUbilgilerinioku", cpu_bilgisi))
    dp.add_handler(CommandHandler("RAMbilgilerinioku", ram_bilgisi))
    dp.add_handler(CommandHandler("havadurumusorgula", havadurumusorgula))
    dp.add_handler(CommandHandler("banasorusor", banasorusor))
    dp.add_handler(CommandHandler("5saniyesonraresimgonder", rastgeleresim))
    dp.add_handler(CommandHandler("dosyaislemleri", dosyaislemleri))
    dp.add_handler(CommandHandler("txtdosyagonder", txt_gonder))
    dp.add_handler(CommandHandler("pdfdosyagonder", pdf_gonder))
    dp.add_handler(CommandHandler("ziple", ziple))
    dp.add_handler(CommandHandler("dosyamial", dosyamial))
    dp.add_handler(MessageHandler(Filters.photo, take_photo))
    dp.add_handler(MessageHandler(Filters.voice , ses_kaydi))
    dp.add_handler(MessageHandler(Filters.document , tel_dosya_gonderme))
    dp.add_handler(MessageHandler(Filters.text, wrong_command)) # Burada CommandHandler yerine MessageHandler kullandık. Bota tanımlı olmayan bir mesaj yazıldığında direkt olarak bu kod satırı devreye girecek
    #bu satır en sona eklenmeli 
    
    
    # log all errors
    dp.add_error_handler(error)


    # start_polling() metodu ile botumuzu başlatıyoruz ve idle() ile sürekli çalışır halde kalmasını sağlıyoruz.
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
