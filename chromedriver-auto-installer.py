import os
import io
import sys
import requests
import untangle
import win32api
import zipfile

class ChromeDriverInstaller():
    def __init__(self):
        if os.path.isfile('chromedriver.exe'):
            classFunctionType = type(self.auto_install)
            for attribute in dir(self):
                if attribute.startswith('__') and attribute.endswith('__'):
                    continue
                if isinstance(self.__getattribute__(attribute), classFunctionType):
                    self.__setattr__(attribute, lambda: None)

        drive = __file__[:2]
        chrome_path = [
            fr'{drive}\Program Files\Google\Chrome\Application\chrome.exe',
            fr'{drive}\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        ]
        chrome_path = list(
            filter(lambda chrome: os.path.isfile(chrome), chrome_path),
        )
        if not chrome_path:
            raise FileNotFoundError('Cannot find original chrome location.')

        def fetch_file_version():
            info = win32api.GetFileVersionInfo(chrome_path[0], '\\')
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            return [win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls)]

        self.__full_version__ = fetch_file_version()
        self.__inner_version__ = self.__full_version__[0]
        self.__compatiable__ = None

    def get_compatiable_chrome_version(self):
        text = requests.get('https://chromedriver.storage.googleapis.com/?delimiter=/&prefix=').text
        file = io.StringIO(text)
        xml = untangle.parse(file).ListBucketResult.CommonPrefixes
        compatible_driver_version = list(
            filter(lambda prefix: prefix.children[0].cdata.startswith(self.inner_version.__str__()), xml),
        )
        self.__compatiable__ = compatible_driver_version[0].children[0].cdata
        self.__compatiable__ = self.__compatiable__[:-1] if self.compatiable_version.endswith('/') else self.compatiable_version
        return self.__compatiable__

    def install_compatiable_chrome(self):
        url = sys.intern(f'https://chromedriver.storage.googleapis.com/{self.compatiable_version}/chromedriver_win32.zip')
        content = requests.get(url).content
        with open('chromedriver.zip', 'wb') as f:
            f.write(content)
        f.close()
        
        with zipfile.ZipFile('chromedriver.zip', 'r', allowZip64=True) as z:
            z.extract('chromedriver.exe')
        z.close()

        os.remove('chromedriver.zip')
        return None

    def auto_install(self):
        self.get_compatiable_chrome_version()
        self.install_compatiable_chrome()
        return None

    @property
    def compatiable_version(self):
        return self.__compatiable__

    @property
    def full_version(self):
        return self.__full_version__

    @property
    def inner_version(self):
        return self.__inner_version__
