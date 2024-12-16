# WebSim Browser

A dedicated browser for websim.ai with enhanced features and plugin support.

![WebSim Browser](assets/favicon.ico)

(This readme is ai generated, so it may not be 100% accurate.)

## Features

### Core Features
- 🏠 Dedicated websim.ai browser with persistent login
- 🔒 Enhanced security settings for websim.ai
- 💾 Persistent cache and cookie storage
- 🌐 Chrome-compatible user agent and headers

### Navigation Controls
- Home button - Return to websim.ai homepage
- Reload button - Refresh the current page
- Settings button - Configure browser settings
- Clear Cache button - Clear browsing data

### Advanced Features
- 🔌 Plugin System
  - Support for websim.ai plugins
  - Built-in plugin manager
  - Default plugins:
    - @Trey6383/test123
    - @Trey6383/injectify
    - @hintbl0ck/edit5
    - @Trey6383/edit6-real
  - Custom plugin support

- 🛠️ API Features (Experimental)
  - Some features may be limited or unavailable
  - Project Management
  - Analytics Integration
  - Team Management
  - Security Settings

## Installation

### Windows Users
1. Download `websim.exe` from [here](https://cvws.icloud-content.com/B/ASokkJTTurV1lH7jczMJx-UBHe2uAXU9BDkjt-LdHb_EIc2jvQQDKSNw/websim.exe?o=AoWNRo4gjZNKtKSownzesTQBMTDNXpeNWTpfh8xNv2CL&v=1&x=3&a=CAogQAYOjxShVPz69DV71y8J48ssOJMsbb0ZaxFHU7Sflp0SbRCXy9aBvTIYl6iyg70yIgEAUgQBHe2uWgQDKSNwaiZ_51XUKyeYW8TMHHBrZkeW3eDV1uZA_nb_xf1w7VmaoCSSNqjCjHImrctVl22n72XpafdYNC2zrbJQgPNYLpCIEqfnX06_6-lZ55KREY4&e=1734368597&fl=&r=380c2a7e-d376-494e-aff7-f6dd81675e75-1&k=aoFcL_LrbMEoGWqb2azEqQ&ckc=com.apple.clouddocs&ckz=com.apple.CloudDocs&p=109&s=gonqWdellrcKWQ5JYYWlhJamD1A)
2. If Windows SmartScreen appears:
   - Click "More info"
   - Click "Run anyway"
   - Or: Right-click > Properties > Check "Unblock" > Apply

### Mac Users
Since this is a Windows executable, Mac users have two options:

1. Run from source:
   ```bash
   # Install Homebrew if you haven't already
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python and Qt dependencies
   brew install python@3.11
   brew install pyqt@6
   
   # Clone and run the browser
   git clone [repository-url]
   cd WebsimBrowser
   pip3 install -r requirements.txt
   python3 main.py
   ```

2. Use virtualization:
   - Install Parallels Desktop, VMware Fusion, or VirtualBox
   - Set up a Windows virtual machine
   - Run the Windows executable inside the VM

Note: Running from source is recommended for Mac users as it provides better performance and native integration.

## Usage

### Basic Navigation
1. Launch the browser
2. Log in to your websim.ai account
3. Use the navigation buttons at the top:
   - 🏠 Home: Return to websim.ai
   - 🔄 Reload: Refresh the page
   - ⚙️ Settings: Configure browser
   - 🧹 Clear Cache: Clear browsing data

### Using Plugins
1. Click the 🔌 Plugins button
2. Choose from preset plugins or add a new one
3. To add a custom plugin:
   - Click "New Plugin..."
   - Enter the creator's websim username (with @)
   - Enter the plugin name
   - The plugin will be applied to the current page

### Settings
- JavaScript toggle
- Cache size configuration
- Data clearing options
- Security preferences

## Development

### Requirements
- Python 3.11+
- PyQt6
- PyQt6-WebEngine

### Building from Source
1. Clone the repository
2. Install dependencies:
   ```bash
   # Windows
   pip install -r requirements.txt
   
   # Mac
   pip3 install -r requirements.txt
   ```
3. Run the browser:
   ```bash
   # Windows
   python main.py
   
   # Mac
   python3 main.py
   ```

## Security Notes
- The browser uses secure settings by default
- Persistent storage is maintained in the user's AppData folder (Windows) or ~/Library/Application Support (Mac)
- All connections use HTTPS
- Cookies and cache are encrypted

## Contributing
Feel free to submit issues and pull requests for:
- New features
- Bug fixes
- Documentation improvements
- UI enhancements

## License
This project is open source and available under the MIT License.

## Credits
- Created for use with websim.ai
- Built with PyQt6 and QtWebEngine
- Icons and emojis provided by standard Unicode