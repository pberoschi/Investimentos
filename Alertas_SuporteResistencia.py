'''
import telepot
bot = telepot.Bot("5026686955:AAHvm0rJOf-_nSCi8sOHYVMhY8zPCBEd73k")

def recebeMsg(msg):
    texto = msg['text']
    #print(texto)
    if texto == '8579.5':
        print(f'SUPORTE CADASTRADO: {texto}')
    else:
        print('Texto diferente')
        
bot.message_loop(recebeMsg)

while True:
    pass





import telepot
from telepot.loop import MessageLoop
from pprint import pprint
bot = telepot.Bot("5026686955:AAHvm0rJOf-_nSCi8sOHYVMhY8zPCBEd73k")

#response = bot.getUpdates(offset=100000001)
#pprint(response)

def handle(msg):
    pprint(msg)

MessageLoop(bot, handle).run_as_thread()


bot.sendMessage(984798692, 'Hey!')

'''


import sys
import time
import telepot
from telepot.loop import MessageLoop
#from pprint import pprint

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #print(content_type, chat_type, chat_id)
    print(msg['text'])

    #if content_type == 'text':
        #bot.sendMessage(chat_id, msg['text'])
        #print(msg['text'])



bot = telepot.Bot("5026686955:AAHvm0rJOf-_nSCi8sOHYVMhY8zPCBEd73k")
MessageLoop(bot, handle).run_as_thread()
#print ('Listening ...')

# Keep the program running.
#while 1:
    #time.sleep(10)


#bot.sendMessage(984798692,'Teste')