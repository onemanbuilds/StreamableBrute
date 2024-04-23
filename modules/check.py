import requests
from modules.helpers import _initTitle,_getRandomUserAgent,_getRandomProxy,_writeFile,_print,_findStringBetween
from threading import Thread,active_count
from pystyle import Colors
import urllib3
urllib3.disable_warnings()

class Check:
    def __init__(self,config,urls) -> None:
        _initTitle('SAB [CHECK]')

        self.use_proxy = config['use_proxy']
        self.proxy_type = config['proxy_type']
        self.threads = config['threads']+20
        self.download_results = config['download_results']
        self.proxies_path = config['proxies_path']
        self.urls = urls
        self.session = requests.session()
        print('')

    def _check(self,url):
        headers = {
            'User-Agent':_getRandomUserAgent('config/useragents.txt'),
            'Connection':'keep-alive'
        }

        proxy = _getRandomProxy(self.use_proxy,self.proxy_type,self.proxies_path)

        try:
            response = self.session.get(url,proxies=proxy,headers=headers,verify=False)
            if response.status_code == 404:
                _print(Colors.cyan,Colors.red,'BAD',url)
                _writeFile('saved/checked_bads.txt',url)
            elif response.status_code == 200:
                _print(Colors.cyan,Colors.green,'HIT',url)
                _writeFile('saved/checked_hits.txt',url)
                if self.download_results == 1:
                    download_url = _findStringBetween(response.text,f'<meta property="og:url" content="{url}" />\n<meta property="og:video" content="https://cdn-cf-east.streamable.com/video/mp4/','">\n<meta property="og:video:url"')
                    download_url = 'https://cdn-cf-east.streamable.com/video/mp4/'+download_url
                    filename = download_url.split('/')[-1].split('?')[0]
                    response = self.session.get(download_url,proxies=proxy,headers=headers)
                    with open(f'saved/downloads/{filename}','wb') as f:
                        for chunk in response.iter_content(chunk_size=128):
                            f.write(chunk)
            else:
                _print(Colors.cyan,Colors.yellow,'RETRY',url)
                self._check(url)
            response.close()
        except Exception:
            self._check(url)

    def _start(self):
        threads = []

        for url in self.urls:
            run = True

            while run:
                if active_count()<=self.threads:
                    thread = Thread(target=self._check,args=(url,))
                    threads.append(thread)
                    thread.start()
                    run = False
        for x in threads:
            x.join()

        print('')
        _print(Colors.cyan,Colors.yellow,'FINISH','Process done!')
