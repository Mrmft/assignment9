import telebot
from telebot.types import Voice
from gtts import gTTS
import qrcode

bot = telebot.TeleBot("TOKEN", parse_mode=None) 

#######################

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, f"{message.from_user.first_name}, how are you doing?")

######################

help_text= """
	/help : نمایش منو
	/game : بازی حدس عدد
	/age : محاسبه سن
	/voice : تبدیل متن انگلیسی به ویس
	/max : نمایش بزرگترین عدد از میان اعداد ورودی شما
	/argmax : نمایش اندیس بزرگترین عدد
	/qrcode : نمایش کد qr متن ورودی شما
 	"""

#PRINT MENU  
  
@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, help_text)

#####################

@bot.message_handler(commands=['game'])
def send_welcome(message):
	bot.reply_to(message, help_text)

#####################

@bot.message_handler(commands=['age'])
def send_welcome(message):
	bot.reply_to(message, help_text) 

#####################

@bot.message_handler(commands=['voice'])
def send_Txt2Voice(message):
	voicemessage = bot.send_message(message.chat.id , 'متن خود را به زبان انگللیسی وارد کنید:')
	bot.register_next_step_handler(voicemessage,Txt2Voice)

#TEXT TO VOICE PART

def Txt2Voice(voicemessage):
    mytext= voicemessage.text
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save('voice.mp3') 
    voice = open('voice.mp3' , 'rb')
    bot.send_voice(voicemessage.chat.id ,voice)

##################

# @bot.message_handler(commands=['max'])
# def send_welcome(message):
# 	bot.reply_to(message, help_text)

# @bot.message_handler(commands=['argmax'])
# def send_welcome(message):
# 	bot.reply_to(message, help_text)
##################

@bot.message_handler(commands=['qrcode'])
def send_qrcodemaker(message):
	qr_message= bot.send_message(message.chat.id , 'متنی وارد کنید تا برای شما بصورت qrcode نمایش داده شود')
	bot.register_next_step_handler(qr_message,qrcode_show)

def qrcode_show(message):
    img= qrcode.make(message.text)
    img.save('qrcode1.png')
    photo = open('qrcode1.png', 'rb')
    bot.send_photo(message , photo)

bot.infinity_polling()




