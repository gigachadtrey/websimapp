# WebSim Browser

A dedicated browser for websim.ai with enhanced features and plugin support.

![WebSim Browser](assets/websim_logo.png)

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

1. Download `websim.exe` from [here](https://cvws.icloud-content.com/B/ASokkJTTurV1lH7jczMJx-UBHe2uAXU9BDkjt-LdHb_EIc2jvQQDKSNw/websim.exe?o=AoWNRo4gjZNKtKSownzesTQBMTDNXpeNWTpfh8xNv2CL&v=1&x=3&a=CAogQAYOjxShVPz69DV71y8J48ssOJMsbb0ZaxFHU7Sflp0SbRCXy9aBvTIYl6iyg70yIgEAUgQBHe2uWgQDKSNwaiZ_51XUKyeYW8TMHHBrZkeW3eDV1uZA_nb_xf1w7VmaoCSSNqjCjHImrctVl22n72XpafdYNC2zrbJQgPNYLpCIEqfnX06_6-lZ55KREY4&e=1734368597&fl=&r=380c2a7e-d376-494e-aff7-f6dd81675e75-1&k=aoFcL_LrbMEoGWqb2azEqQ&ckc=com.apple.clouddocs&ckz=com.apple.CloudDocs&p=109&s=gonqWdellrcKWQ5JYYWlhJamD1A)
2. If Windows SmartScreen appears:
   - Click "More info"
   - Click "Run anyway"
   - Or: Right-click > Properties > Check "Unblock" > Apply

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
   pip install -r requirements.txt
   ```
3. Run the browser:
   ```bash
   python main.py
   ```

## Security Notes
- The browser uses secure settings by default
- Persistent storage is maintained in the user's AppData folder
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