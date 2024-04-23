import requests
from modules.helpers import _initTitle,_getRandomUserAgent,_getRandomProxy,_writeFile,_print,_genLettersDigits,_findStringBetween
from threading import Thread,active_count
from pystyle import Colors
import urllib3
urllib3.disable_warnings()

class Brute:
    def __init__(self,config) -> None:
        _initTitle('SAB [BRUTE]')

        self.use_proxy = config['use_proxy']
        self.proxy_type = config['proxy_type']
        self.threads = config['threads']+20
        self.amount_to_brute = config['amount_to_brute']
        self.download_results = config['download_results']
        self.proxies_path = config['proxies_path']
        self.session = requests.session()
        print('')

    def _brute(self):
        headers = {
            'User-Agent':_getRandomUserAgent('config/useragents.txt'),
            'Connection':'keep-alive'
        }

        proxy = _getRandomProxy(self.use_proxy,self.proxy_type,self.proxies_path)
        url_end = _genLettersDigits(5,6)

        try:
            brute_url = f'https://streamable.com/{url_end}'
            response = self.session.get(brute_url,proxies=proxy,headers=headers,verify=False)
            if response.status_code == 404:
                _print(Colors.cyan,Colors.red,'BAD',brute_url)
                _writeFile('saved/bads.txt',brute_url)
            elif response.status_code == 200:
                _print(Colors.cyan,Colors.green,'HIT',brute_url)
                _writeFile('saved/hits.txt',brute_url)
                if self.download_results == 1:
                    download_url = _findStringBetween(response.text,f'<meta property="og:url" content="{brute_url}" />\n<meta property="og:video" content="https://cdn-cf-east.streamable.com/video/mp4/','">\n<meta property="og:video:url"')
                    download_url = 'https://cdn-cf-east.streamable.com/video/mp4/'+download_url
                    filename = download_url.split('/')[-1].split('?')[0]
                    response = self.session.get(download_url,proxies=proxy,headers=headers)
                    with open(f'saved/downloads/{filename}','wb') as f:
                        for chunk in response.iter_content(chunk_size=128):
                            f.write(chunk)
            else:
                _print(Colors.cyan,Colors.yellow,'RETRY',brute_url)
                self._brute()
            response.close()
        except Exception:
            self._brute()

    def _start(self):
        if self.amount_to_brute > 0:
            threads = []
            for i in range(self.amount_to_brute):
                run = True
                while run:
                    if active_count()<=self.threads:
                        thread = Thread(target=self._brute)
                        threads.append(thread)
                        thread.start()
                        run = False
            for x in threads:
                x.join()
        else:
            run = True
            while run:
                if active_count()<=self.threads:
                    thread = Thread(target=self._brute)
                    thread.start()
        print('')
        _print(Colors.cyan,Colors.yellow,'FINISH','Process done!')
