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

# Run the container
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

### Alternative for M1/M2/M3 Macs: QEMU VM Method

If you experience persistent issues with the Docker approach on Apple Silicon, the wrapper author provides a QEMU VM image that runs the wrapper in a fully emulated x86_64 environment. This method is more resource-intensive but may work better in some cases.

#### Prerequisites

Install QEMU on your Mac:
```bash
brew install qemu
```

#### Setup Instructions

1. **Download the QEMU VM image:**
   
   The wrapper author provides a pre-configured qcow2 VM image via GitHub Actions:
   - Go to: https://github.com/WorldObservationLog/wrapper/actions/runs/22147727310
   - Download the artifact (requires GitHub login)
   - Extract the qcow2 file from the downloaded zip

2. **Start the QEMU VM:**
   
   ```bash
   # Basic command to run the VM
   qemu-system-x86_64 \
     -m 2048 \
     -smp 2 \
     -drive file=/path/to/downloaded.qcow2,format=qcow2 \
     -net nic -net user,hostfwd=tcp::10020-:10020,hostfwd=tcp::20020-:20020,hostfwd=tcp::30020-:30020 \
     -nographic
   ```
   
   This command:
   - Allocates 2GB RAM (`-m 2048`)
   - Uses 2 CPU cores (`-smp 2`)
   - Forwards wrapper ports (10020, 20020, 30020) to your Mac
   - Runs in terminal mode (`-nographic`)

3. **Connect to the VM:**
   
   Once the VM boots, you should be able to access the wrapper service on the forwarded ports. The wrapper should be pre-configured and running inside the VM.

4. **Run the Flask app on your Mac:**
   
   Instead of running everything in Docker, you can:
   - Install dependencies on your Mac: `pip3 install flask pyyaml`
   - Run the Flask app locally: `python3 main.py`
   - Configure it to connect to the wrapper running in the QEMU VM (ports 10020, 20020, 30020)

#### Notes on QEMU Method

- **Performance**: Running a full VM is slower than Docker emulation
- **Resource usage**: Requires more RAM and CPU
- **Setup complexity**: More manual setup required
- **When to use**: Only if Docker method consistently fails
- **VM contents**: The qcow2 image contains a minimal Linux with wrapper pre-installed

#### Recommended Approach

For most M1/M2/M3 users, the **Docker method with explicit platform flags** (shown above) is simpler and sufficient. Only use the QEMU VM method if you encounter persistent issues that Docker cannot resolve.

**📚 For detailed QEMU VM setup instructions, see [QEMU_SETUP.md](QEMU_SETUP.md)**

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
