import requests
from os import name,system
from random import choice,randint
from sys import stdout
from string import ascii_lowercase
from time import sleep
from colorama import init,Style,Fore
from threading import Thread, Lock,active_count
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        system("title {0}".format(title_name))
        
    def ReadFile(self,filename,method):
        with open(filename,method) as f:
            content = [line.strip('\n') for line in f]
            return content

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
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
            self.SetTitle('One Man Builds Streamable Video Brute Tool ^| HITS: {0} ^| DOWNLOADS: {1} ^| BADS: {2} ^| RETRIES: {3} ^| THREADS: {4}'.format(self.hits,self.downloads,self.bads,self.retries,active_count()-1))
            sleep(0.1)

    def __init__(self):
        self.SetTitle('One Man Builds Streamable Video Brute Tool')
        self.clear()
        self.title = Style.BRIGHT+Fore.RED+"""
                                
                        ____ ___ ____ ____ ____ _  _ ____ ___  _    ____    ___  ____ _  _ ___ ____ 
                        [__   |  |__/ |___ |__| |\/| |__| |__] |    |___    |__] |__/ |  |  |  |___ 
                        ___]  |  |  \ |___ |  | |  | |  | |__] |___ |___    |__] |  \ |__|  |  |___ 
                                                                                                    
                                
        """
        print(self.title)
        init(convert=True)
        self.hits = 0
        self.downloads = 0
        self.bads = 0
        self.retries = 0
        self.ua = UserAgent()
        self.use_proxy = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Proxy ['+Fore.RED+'0'+Fore.CYAN+']Proxyless: '))
        
        if self.use_proxy == 1:
            self.proxy_type = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Https ['+Fore.RED+'2'+Fore.CYAN+']Socks4 ['+Fore.RED+'3'+Fore.CYAN+']Socks5: '))
        
        self.download_video = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Download ['+Fore.RED+'0'+Fore.CYAN+']No Download: '))
        self.threads = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Threads: '))
        print('')
        self.header = headers = {'User-Agent':self.ua.random}
        self.lock = Lock()

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def Scrape(self):
        try:
            random_end = ''.join(choice(ascii_lowercase+'0123456789') for num in range(0,randint(5,6)))
            link = 'https://streamable.com/{0}'.format(random_end)

            response = ''

            if self.use_proxy == 1:
                response = requests.get(link,headers=self.header,proxies=self.GetRandomProxy())
            else:
                response = requests.get(link,headers=self.header)

            if response.status_code == 200:
                self.PrintText(Fore.CYAN,Fore.RED,'HIT',link)
                self.hits += 1
                with open('good_links.txt','a') as f:
                    f.write(link+'\n')

                if self.download_video == 1:
                    soup = BeautifulSoup(response.text,'html.parser')
                    download_link = soup.find('meta',{'property':'og:video:url'})
                    download_link = download_link['content']
                    response = requests.get(download_link,headers=self.header)

                    title = soup.title.string.replace(' ','_')

                    with open('Downloads/{0}'.format(title+'.mp4'),'wb') as f:
                        f.write(response.content)
                    
                    self.downloads += 1
                    

            elif response.status_code == 404:
                self.PrintText(Fore.RED,Fore.CYAN,'BAD',link)
                self.bads += 1
                with open('bad_links.txt','a') as f:
                    f.write(link+'\n')
            else:
                self.retries += 1
                self.Scrape()
                #self.PrintText('-','RATELIMITED WAITING FOR 10 SECONDS',Fore.RED)
                #sleep(10)
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