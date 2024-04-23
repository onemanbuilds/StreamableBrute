from modules.helpers import _initTitle,_readJson,_readFile,_print
from modules.check import Check
from modules.brute import Brute
from modules.duplicateRemove import DuplicateRemove
from time import sleep
from pystyle import Colors

class Menu:
    def __init__(self) -> None:
        _initTitle('SAB [MENU]')

    def _menu(self):        
        _initTitle('SAB [MENU]')

        self.config = _readJson('config/config.json','r')
        self.urls_path = self.config['urls_path']
        self.urls = _readFile(self.urls_path,'r',0)

        options = ['Check Urls','Brute','Duplicate Remove']
        counter = 0
        for option in options:
            counter+=1
            _print(Colors.cyan,Colors.yellow,str(counter),option)
        print('')

        selected = int(input(f'{Colors.cyan}[{Colors.yellow}>{Colors.cyan}] {Colors.cyan}Select something:{Colors.yellow} '))

        if selected == 1:
            Check(self.config,self.urls)._start()
            sleep(2)
            self._menu()
        elif selected == 2:
            Brute(self.config)._start()
            sleep(2)
            self._menu()
        elif selected == 3:
            DuplicateRemove()._start()
            sleep(2)
            self._menu()
        else:
            self._menu()