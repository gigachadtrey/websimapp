import os
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from .interceptor import ChromeRequestInterceptor

class BrowserSettings:
    @staticmethod
    def setup_persistent_storage(browser):
        # Create persistent profile in AppData Local with custom name
        storage_path = os.path.join(
            os.path.expandvars("%LOCALAPPDATA%"),
            'WebSimBrowser'
        )
        
        # Print storage path for debugging
        print(f"Storage path: {storage_path}")
        
        # Ensure the directory exists
        os.makedirs(storage_path, exist_ok=True)
        
        # Create persistent profile with enhanced settings
        browser.profile = QWebEngineProfile('WebSimProfile', browser)
        
        # Set storage paths
        browser.profile.setPersistentStoragePath(storage_path)
        cookies_path = os.path.join(storage_path, 'cookies')
        os.makedirs(cookies_path, exist_ok=True)
        
        # Enable cache with specific paths
        cache_path = os.path.join(storage_path, 'cache')
        os.makedirs(cache_path, exist_ok=True)
        browser.profile.setCachePath(cache_path)
        browser.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        browser.profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # 100MB cache
        
        # Configure security settings
        settings = browser.profile.settings()
        BrowserSettings._configure_settings(settings)
        
        # Set modern Chrome user agent with full security features
        chrome_version = "120.0.0.0"
        webkit_version = "537.36"
        browser.profile.setHttpUserAgent(
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{webkit_version} "
            f"(KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version} "
            f"Chromium/{chrome_version}"
        )
        
        # Set language and encoding
        browser.profile.setHttpAcceptLanguage("en-US,en;q=0.9")
        
        # Create and set the request interceptor
        interceptor = ChromeRequestInterceptor(chrome_version)
        browser.profile.setUrlRequestInterceptor(interceptor)
        
        # Enhanced persistence settings for login
        browser.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanPaste, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        
        # Set cookie path explicitly
        browser.profile.setPersistentStoragePath(cookies_path)
        
        # Additional storage settings for better persistence
        settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanPaste, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        
        # Additional persistence settings
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        
        # Set cookie settings
        browser.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        # Remove the unsupported setFilterCallback
        # browser.profile.cookieStore().setFilterCallback(lambda _: True)  # Accept all cookies

    @staticmethod
    def setup_page_settings(page):
        """Configure page settings for better compatibility"""
        settings = page.settings()
        BrowserSettings._configure_settings(settings)
        
        # Set default fonts to match Chrome
        settings.setFontFamily(QWebEngineSettings.FontFamily.StandardFont, "Segoe UI")
        settings.setFontFamily(QWebEngineSettings.FontFamily.SansSerifFont, "Segoe UI")
        settings.setFontFamily(QWebEngineSettings.FontFamily.SerifFont, "Times New Roman")
        settings.setFontFamily(QWebEngineSettings.FontFamily.FixedFont, "Consolas")
        
        # Set font sizes
        settings.setFontSize(QWebEngineSettings.FontSize.DefaultFontSize, 16)
        settings.setFontSize(QWebEngineSettings.FontSize.DefaultFixedFontSize, 13)
        settings.setFontSize(QWebEngineSettings.FontSize.MinimumFontSize, 0)
        settings.setFontSize(QWebEngineSettings.FontSize.MinimumLogicalFontSize, 6)

    @staticmethod
    def _configure_settings(settings):
        """Configure common settings for both profile and page"""
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanPaste, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebRTCPublicInterfacesOnly, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ErrorPageEnabled, True) 