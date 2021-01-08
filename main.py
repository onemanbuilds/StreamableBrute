import requests
import json
from os import name,system
from random import choice,randint
from sys import stdout
from string import ascii_lowercase
from time import sleep
from colorama import init,Style,Fore
from threading import Thread, Lock,active_count
from bs4 import BeautifulSoup
from datetime import datetime

class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title:str):
        if name == 'posix':
            stdout.write(f"\x1b]2;{title}\x07")
        elif name in ('ce', 'nt', 'dos'):
            system(f'title {title}')
        else:
            stdout.write(f"\x1b]2;{title}\x07")
        
    def ReadFile(self,filename,method):
        with open(filename,method,encoding='utf8') as f:
            content = [line.strip('\n') for line in f]
            return content

    def ReadJson(self,filename,method):
        with open(filename,method) as f:
            return json.load(f)
    
    def GetRandomUserAgent(self):
        useragents = self.ReadFile('[Data]/useragents.txt','r')
        return choice(useragents)

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('[Data]/proxies.txt','r')
        proxies = {}
        if self.proxy_type == 1:
            proxies = {
                "http":"http://{0}".format(choice(proxies_file)),
                "https":"https://{0}".format(choice(proxies_file))
            }
        elif self.proxy_type == 2:
            proxies = {
                "http":"socks4://{0}".format(choice(proxies_file)),
                "https":"socks4://{0}".format(choice(proxies_file))
            }
        else:
            proxies = {
                "http":"socks5://{0}".format(choice(proxies_file)),
                "https":"socks5://{0}".format(choice(proxies_file))
            }
        return proxies

    def TitleUpdate(self):
        while True:
            self.SetTitle(f'[One Man Builds Streamable Video Brute Tool] ^| HITS: {self.hits} ^| DOWNLOADS: {self.downloads} ^| BADS: {self.bads} ^| WEBHOOK RETRIES: {self.webhook_retries} ^| RETRIES: {self.retries} ^| THREADS: {active_count()-1}')
            sleep(0.1)

    def __init__(self):
        self.SetTitle('[One Man Builds Streamable Video Brute Tool]')
        self.clear()
        self.title = Style.BRIGHT+Fore.GREEN+"""
                                  ╔═════════════════════════════════════════════════╗
                                    ╔═╗╔╦╗╦═╗╔═╗╔═╗╔╦╗╔═╗╔╗ ╦  ╔═╗  ╔╗ ╦═╗╦ ╦╔╦╗╔═╗
                                    ╚═╗ ║ ╠╦╝║╣ ╠═╣║║║╠═╣╠╩╗║  ║╣   ╠╩╗╠╦╝║ ║ ║ ║╣ 
                                    ╚═╝ ╩ ╩╚═╚═╝╩ ╩╩ ╩╩ ╩╚═╝╩═╝╚═╝  ╚═╝╩╚═╚═╝ ╩ ╚═╝
                                  ╚═════════════════════════════════════════════════╝
                                                                                                    
                                
        """
        print(self.title)
        init(convert=True)
        self.hits = 0
        self.downloads = 0
        self.bads = 0
        self.retries = 0
        self.webhook_retries = 0

        config = self.ReadJson('[Data]/configs.json','r')

        self.use_proxy = config['use_proxy']
        self.proxy_type = config['proxy_type']
        self.download_video = config['download_video']
        self.threads = config['threads']
        self.webhook_enable = config['webhook_enable']
        self.webhook_url = config['webhook_url']

        self.lock = Lock()

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def SendWebhook(self,title,message,icon_url,thumbnail_url,proxy,useragent):
        try:
            timestamp = str(datetime.utcnow())

            message_to_send = {"embeds": [{"title": title,"description": message,"color": 65362,"author": {"name": "AUTHOR'S DISCORD SERVER [CLICK HERE]","url": "https://discord.gg/9bHfzyCjPQ","icon_url": icon_url},"footer": {"text": "MADE BY ONEMANBUILDS","icon_url": icon_url},"thumbnail": {"url": thumbnail_url},"timestamp": timestamp}]}
            
            headers = {
                'User-Agent':useragent,
                'Pragma':'no-cache',
                'Accept':'*/*',
                'Content-Type':'application/json'
            }

            payload = json.dumps(message_to_send)

            if self.use_proxy == 1:
                response = requests.post(self.webhook_url,data=payload,headers=headers,proxies=proxy)
            else:
                response = requests.post(self.webhook_url,data=payload,headers=headers)

            if response.text == "":
                pass
            elif "You are being rate limited." in response.text:
                self.webhook_retries += 1
                self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)
            else:
                self.webhook_retries += 1
                self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)
        except:
            self.webhook_retries += 1
            self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)

    def Scrape(self):
        try:
            random_end = ''.join(choice(ascii_lowercase+'0123456789') for num in range(0,randint(5,6)))
            link = f'https://streamable.com/{random_end}'

            response = ''
            proxy = ''
            useragent = self.GetRandomUserAgent()

            headers = {
                'User-Agent':useragent
            }

            if self.use_proxy == 1:
                proxy = self.GetRandomProxy()
                response = requests.get(link,headers=headers,proxies=proxy)
            else:
                response = requests.get(link,headers=headers)

            if response.status_code == 404:
                self.PrintText(Fore.WHITE,Fore.RED,'BAD',link)
                self.bads += 1
                with open('[Data]/[Results]/bad_links.txt','a') as f:
                    f.write(link+'\n')
            elif response.status_code == 200:
                self.PrintText(Fore.WHITE,Fore.GREEN,'HIT',link)
                self.hits += 1
                with open('[Data]/[Results]/good_links.txt','a') as f:
                    f.write(link+'\n')

                if self.webhook_enable == 1:
                    self.SendWebhook('Streamable Result',link,'https://cdn.discordapp.com/attachments/776819723731206164/796935218166497352/onemanbuilds_new_logo_final.png','https://pbs.twimg.com/profile_images/601124726832955393/GYp5MlPf_400x400.png',proxy,useragent)

                if self.download_video == 1:
                    soup = BeautifulSoup(response.text,'html.parser')
                    download_link = soup.find('meta',{'property':'og:video:url'})
                    download_link = download_link['content']
                    response = requests.get(download_link,headers=headers)

                    title = soup.title.string.replace(' ','_')

                    with open(f'[Data]/[Results]/[Downloads]/{title}.mp4','wb') as f:
                        f.write(response.content)
                    self.downloads += 1
            else:
                self.retries += 1
                self.Scrape()
        except:
            self.retries += 1
            self.Scrape()
            
    def Start(self):
        Thread(target=self.TitleUpdate).start()
        while True:
            if active_count()<=self.threads:
                Thread(target=self.Scrape).start()

if __name__ == '__main__':
    main = Main()
    main.Start()