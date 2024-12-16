from PyQt6.QtWebEngineCore import QWebEngineUrlRequestInterceptor

class ChromeRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, chrome_version):
        super().__init__()
        self.chrome_version = chrome_version
        
    def interceptRequest(self, info):
        # Add Chrome-specific headers
        info.setHttpHeader(
            b"sec-ch-ua",
            f'"Not_A Brand";v="8", "Chromium";v="{self.chrome_version}", "Google Chrome";v="{self.chrome_version}"'.encode()
        )
        info.setHttpHeader(b"sec-ch-ua-mobile", b"?0")
        info.setHttpHeader(b"sec-ch-ua-platform", b'"Windows"') 