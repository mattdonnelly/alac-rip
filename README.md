# Apple Music Downloader Web UI

A simple web interface for the Apple Music Downloader, making it easier to download your favorite tracks with a user-friendly GUI.

## 🎵 About

This project is a humble web interface wrapper built around the excellent work of other developers in the Apple Music downloading community. It provides a clean, browser-based UI to interact with the powerful Apple Music Downloader tools without needing to use command-line interfaces.

**This project would not exist without the amazing work of:**
- **[zhaarey/apple-music-downloader](https://github.com/zhaarey/apple-music-downloader)** - The core Go-based Apple Music downloader that powers all the downloading functionality
- **[zhaarey/wrapper](https://github.com/zhaarey/wrapper)** - The authentication wrapper that handles Apple Music login and session management

All credit for the actual downloading capabilities goes to these original creators. This UI is simply a convenience layer on top of their excellent tools.

## ✨ Features

- **🌐 Web-based Interface**: Clean, modern web UI accessible from any browser
- **🔐 Auto-Login**: Save credentials for automatic login on startup
- **🎵 Multiple Formats**: Support for ATMOS, AAC, and standard downloads
- **📊 Real-time Logs**: Live streaming of download progress and wrapper status
- **⚙️ Settings Management**: Easy configuration of all downloader options via web interface
- **🎯 Smart Controls**: Intuitive format selection with Special Audio toggle
- **📱 Responsive Design**: Works on desktop and mobile browsers
- **🔄 Auto-retry**: Intelligent handling of failed connections and auto-login

## 🚀 Quick Start

### Prerequisites

- **Linux environment** (this tool is designed for Linux, also works on WSL)
- **Python 3.7+** with Flask and PyYAML
- **System dependencies**: Git, Go, FFmpeg, GPAC (MP4Box), Wget
- **Internet connection** for downloading tools and dependencies

### Installation

1. **Install system dependencies:**
   ```bash
   sudo apt-get update
   # Note: Required dependencies are also checked/listed by main.py on first run
   sudo apt-get install git ffmpeg gpac golang-go wget python3-flask python3-yaml
   ```

2. **Clone this repository:**
   ```bash
   git clone https://github.com/lalit22km/alac-rip.git
   cd alac-rip
   ```

3. **Run the setup:**
   ```bash
   python3 main.py
   ```
   
   The first run will automatically:
   - Verify all required dependencies are installed
   - Download and setup Bento4
   - Download the wrapper tool
   - Clone the Apple Music Downloader

4. **Access the web interface:**
   - Open your browser and navigate to `http://localhost:5000`
   - The interface will be ready to use!

### Docker Installation (Alternative)

For a containerized setup that handles all dependencies automatically:

```bash
# Build the Docker image
docker build -t alac-rip .

# Run the container (bash/sh/zsh)
docker run -p 5000:5000 -v $(pwd)/downloads:/app/downloads alac-rip

# Or on Windows PowerShell:
# docker run -p 5000:5000 -v ${PWD}/downloads:/app/downloads alac-rip
```

**Note for Apple Silicon (M1/M2/M3) and ARM users:**
The wrapper binary is x86_64 only. Docker will automatically use QEMU emulation to run the container. If you encounter issues, ensure Docker Desktop has "Use Rosetta for x86_64/amd64 emulation on Apple Silicon" enabled in Settings → General, or explicitly specify the platform:

```bash
docker build --platform linux/amd64 -t alac-rip .
docker run --platform linux/amd64 -p 5000:5000 -v $(pwd)/downloads:/app/downloads alac-rip
```

Access the web interface at `http://localhost:5000`

## 📖 Usage

### First Time Setup

1. **Login**: Click "Login to Wrapper" and enter your Apple Music credentials
2. **Wait for Success**: Watch the wrapper logs until you see `[.] response type 6` 
3. **Configure Settings**: Click the ⚙️ Settings button to customize download preferences
4. **Start Downloading**: Paste Apple Music URLs and choose your format

### Download Options

- **Standard Download**: Uncheck "Special Audio" for basic downloads
- **ATMOS**: Check "Special Audio" and select "ATMOS" for spatial audio
- **AAC**: Check "Special Audio" and select "AAC" for AAC format

### Settings

The settings page allows you to configure:
- Download folders and file naming
- Audio quality and format preferences  
- Cover art and lyrics options
- Advanced downloader parameters

---

The application acts as a bridge between the web interface and the command-line tools, handling:
- Authentication state management
- Process lifecycle management
- Configuration file editing
- Real-time log streaming
- Download queue management


## ⚠️ Disclaimer

This tool is for educational purposes and personal use only. Please respect Apple's Terms of Service and only download content you have the legal right to access. The developers of this UI wrapper are not responsible for any misuse of the underlying downloading tools.

**Security Note:** This tool runs as a regular user and does not require root privileges. All dependencies should be installed separately using your system's package manager.

## 🙏 Acknowledgments

**Massive thanks to:**

- **[@zhaarey](https://github.com/zhaarey)** for creating both the [apple-music-downloader](https://github.com/zhaarey/apple-music-downloader) and [wrapper](https://github.com/zhaarey/wrapper) projects that make this possible
- The entire Apple Music downloading community for their research and tools
- All contributors who help improve these tools

---
