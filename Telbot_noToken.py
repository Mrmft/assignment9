from random import randint
import telebot
from gtts import gTTS
import qrcode
import jdatetime

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
def send_menu(message):
	bot.reply_to(message, help_text)

#####################

@bot.message_handler(commands=['game'])
def play_game(message):
	global my_random_number 
	my_random_number =  str(randint(0 , 31))
	user_number= bot.send_message(message.chat.id , 'من یک عدد فرضی بین 0 تا 30 انتخاب میکنم و شما باید اون عدد رو حدس بزنید.')	
	bot.register_next_step_handler(user_number , rand_game)

#####  NUMBER_GUESSING_GAME

def rand_game(user_number):
    if user_number.text == my_random_number:
        bot.send_message(user_number.chat.id , 'هوورررررا شما برنده شدید!!!!!!')
    elif user_number.text > my_random_number:
        user_number_new = bot.send_message(user_number.chat.id , 'یه عدد کمتر پیشنهاد بده')
        bot.register_next_step_handler(user_number_new , rand_game)
    elif user_number.text < my_random_number:
        user_number_new = bot.send_message(user_number.chat.id , 'یه عدد بیشتر پیشنهاد بده')
        bot.register_next_step_handler(user_number_new , rand_game)
        

####################+


#@bot.message_handler(commands=['age'])
#def send_age(message):
#    bot.send_message(message.chat.id, 'لطفا سن خودت رو در قالب زیر بفرس تا بهت بگم چند سالته!!! \n yyyy/mm/dd')
#    bot.register_next_step_handler(message , find_age)

#def find_age(message):
#    x = jdatetime.date.today().split('-')
#    print(x , type(x))

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

@bot.message_handler(commands=['max'])
def send_max_number(message):
	integer_string= bot.send_message(message.chat.id, 'یک رشته از اعداد به این صورت وارد نمایید: \n 1,2,3,4,5,6')
	bot.register_next_step_handler(integer_string, find_max)

#### FIND_MAX_NUMBER

def find_max(numbers_string):
    max_number = max(numbers_string.text.split(','))
    bot.send_message(numbers_string.chat.id , max_number)
    
##################

@bot.message_handler(commands=['argmax'])
def send_max_number_index(message):
	integer_string= bot.send_message(message.chat.id, 'یک رشته از اعداد به این صورت وارد نمایید: \n 1,2,3,4,5,6')
	bot.register_next_step_handler(integer_string, find_max_index)

#### FIND_INDEX_OF_MAX_NUMBER

def find_max_index(numbers_string):
    numbers_string_list = numbers_string.text.split(',')
    max_number = max(numbers_string_list)
    max_index = numbers_string_list.index(max_number)
    bot.send_message(numbers_string.chat.id , max_index+1)

##################

@bot.message_handler(commands=['qrcode'])
def send_qrcodemaker(message):
	qr_message= bot.send_message(message.chat.id , 'متنی وارد کنید تا برای شما بصورت qrcode نمایش داده شود')
	bot.register_next_step_handler(qr_message,qrcode_show)

###### SEND_QRCODE_IMAGE_OF_A_TEXT

def qrcode_show(qr_message):
    img= qrcode.make(qr_message.text)
    img.save('qrcode.png')
    photo = open('qrcode.png', 'rb')
    bot.send_photo(qr_message.chat.id , photo)

bot.infinity_polling()




