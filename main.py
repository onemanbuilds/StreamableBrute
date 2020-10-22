import requests
from os import name,system
from random import choice,randint
from sys import stdout
from string import ascii_lowercase
from time import sleep
from colorama import init,Fore
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
        proxies = {
            "http":"http://{0}".format(choice(proxies_file)),
            "https":"https://{0}".format(choice(proxies_file))
            }
        return proxies

    def __init__(self):
        self.SetTitle('One Man Builds Streamable Video Brute Tool')
        self.clear()
        title = Fore.YELLOW+"""
                        
                ____ ___ ____ ____ ____ _  _ ____ ___  _    ____    ___  ____ _  _ ___ ____ 
                [__   |  |__/ |___ |__| |\/| |__| |__] |    |___    |__] |__/ |  |  |  |___ 
                ___]  |  |  \ |___ |  | |  | |  | |__] |___ |___    |__] |  \ |__|  |  |___ 
                                                                                            
                        
        """
        print(title)
        init(convert=True)
        self.ua = UserAgent()
        self.use_proxy = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to use proxies [1] yes [0] no: '))
        self.download_video = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to download videos [1] yes [0] no: '))
        self.threads = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Threads: '))
        print('')
        self.header = headers = {'User-Agent':self.ua.random}
        self.lock = Lock()

    def PrintText(self,info_name,text,info_color:Fore):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(info_color+'['+Fore.WHITE+info_name+info_color+f'] {text}\n')
        self.lock.release()

    def Scrape(self):
        while True:
            try:
                random_end = ''.join(choice(ascii_lowercase+'0123456789') for num in range(0,randint(5,6)))
                link = 'https://streamable.com/{0}'.format(random_end)

                response = ''

                if self.use_proxy == 1:
                    response = requests.get(link,headers=self.header,proxies=self.GetRandomProxy())
                else:
                    response = requests.get(link,headers=self.header)

                if response.status_code == 200:
                    self.PrintText('!','GOOD | {0}'.format(link),Fore.GREEN)
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
                        

                elif response.status_code == 404:
                    self.PrintText('-','BAD | {0}'.format(link),Fore.RED)
                    with open('bad_links.txt','a') as f:
                        f.write(link+'\n')
                else:
                    self.PrintText('-','RATELIMITED WAITING FOR 10 SECONDS',Fore.RED)
                    sleep(10)
            except:
                pass
            
    def Start(self):
        while True:
            if active_count()<=self.threads:
                Thread(target=self.Scrape).start()

if __name__ == '__main__':
    main = Main()
    main.Start()