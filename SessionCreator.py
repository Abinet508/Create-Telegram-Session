from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, InputPeerUserFromMessage
from telethon.errors.rpcerrorlist import (PeerFloodError, UserNotMutualContactError ,
                                          UserPrivacyRestrictedError, UserChannelsTooMuchError,
                                          UserBotError, InputUserDeactivatedError)
from telethon.tl.functions.channels import InviteToChannelRequest
import time, os, sys, json
from decouple import Config,RepositoryEnv
from qrcode import QRCode
path=os.path.dirname(__file__)

qr = QRCode()
DOTENV_FILE=os.path.join(path,'Environments\.env') 
print(DOTENV_FILE)
config = Config(RepositoryEnv(DOTENV_FILE))
Password = config('Password')
phone_number = config('phone_number')

def gen_qr(token:str):
    qr.clear()
    qr.add_data(token)
    qr.print_ascii()
    print("Please Scan the QR Code using your phone")
def display_url_as_qr(url):
    print(url)  # do whatever to show url as a qr to the user
    gen_qr(url)

def JsonWriter(filename,Environment,Api_detail):


    with open("{}\\{}".format(path,filename)) as file:
        data = json.load(file)
    file.close()
    for Env in data:

        try:
            Env[Environment]= Api_detail
            print(data)
            with open("{}\\{}".format(path,filename), "w+") as file:
                json.dump(data,file,indent=4)
            file.close()
        except:
            Env={Environment:Api_detail}
            with open("{}\\{}".format(path,filename), "w+") as file:
                json.dump(data, file, indent=4)
            file.close()


def JsonReader(filename,Environment):
    with open('{}\\{}'.format(path,filename))as f:
        data = json.load(f)
        for First in data:
            if Environment in First:
                        return (First[Environment])

COLORS = {
   "re": "\u001b[31;1m",
   "gr": "\u001b[32m",
   "ye": "\u001b[33;1m",
}
re = "\u001b[31;1m"
gr = "\u001b[32m"
ye = "\u001b[33;1m"
def colorText(text):
   for color in COLORS:
       text = text.replace("[[" + color + "]]", COLORS[color])
   return text
if sys.version_info[0] < 3:
    telet = lambda :os.system('pip install -U telethon')
elif sys.version_info[0] >= 3:
    telet = lambda :os.system('pip3 install -U telethon')

telet()
MyList =[]
for x in os.listdir("{}\\Sessions".format(path)):
    if x.endswith(".session"):
        # Prints only text file present in My Folder
        MyList.append(int(x.split("newsession")[1].split(".session")[0].strip()))  
try:
    NewSession=max(MyList)+1
except:
    NewSession=1

print(NewSession)              
async def main(client: TelegramClient):
                    if(not client.is_connected()):
                                                                        await client.connect()
                    
                    print(str(await client.get_me(input_peer= True)))
                    if(await client.get_me()==None):
                        qr_login = await client.qr_login()
                        print(client.is_connected())
                        r = False
                        try:
                            while not r:
                                display_url_as_qr(qr_login.url)
                                
                                try:
                                    r = await qr_login.wait()
                                       
                                except:
                                    await qr_login.recreate()
                            print("Session newsession{}.session created successfully".format(NewSession))        
                        except:
                            pass
                        finally:
                            await client.disconnect()     
                            time.sleep(2)    

api_id=20362593  
api_hash='cad3650e74373d3b79c3b728c9715f3e'
newdetail={'api_id': api_id, 'api_hash': api_hash}      
print(JsonWriter("getmem_log.json",'newsession{}'.format(NewSession),newdetail) )    
client = TelegramClient('Sessions//newsession{}'.format(NewSession),api_id,api_hash)                     
client.loop.run_until_complete(main(client))
