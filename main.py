import os
import subprocess
import urllib.request
import zipfile
from pathlib import Path
import sys
import shutil

PROJECT_DIR = Path(__file__).resolve().parent
BENTO4_DIR = PROJECT_DIR / "bento4"
WRAPPER_DIR = PROJECT_DIR / "wrapper"
AMD_DIR = PROJECT_DIR / "apple-music-downloader"

def firstsetup():
    # --- Check for required dependencies ---
    print("Checking for required dependencies...")
    
    # Check system binaries
    required_binaries = {
        'git': 'git',
        'ffmpeg': 'ffmpeg',
        'MP4Box': 'gpac',
        'go': 'golang-go',
        'wget': 'wget'
    }
    
    missing_binaries = []
    for binary, package in required_binaries.items():
        if shutil.which(binary) is None:
            missing_binaries.append(package)
            print(f"  ✗ {binary} not found (package: {package})")
        else:
            print(f"  ✓ {binary} found")
    
    # Check Python dependencies
    required_python_modules = {
        'flask': 'flask',
        'yaml': 'pyyaml'
    }
    
    missing_python = []
    for module, package in required_python_modules.items():
        try:
            __import__(module)
            print(f"  ✓ Python module '{module}' found")
        except ImportError:
            missing_python.append(package)
            print(f"  ✗ Python module '{module}' not found (package: {package})")
    
    # If any dependencies are missing, exit with helpful message
    if missing_binaries or missing_python:
        print("\n❌ ERROR: Missing required dependencies!\n")
        
        if missing_binaries:
            print("System packages needed (Debian/Ubuntu):")
            print(f"  sudo apt-get install {' '.join(missing_binaries)}")
            print("\nFor other distributions, install equivalent packages using your package manager.")
            print("Or use Docker for automatic dependency management.\n")
        
        if missing_python:
            # Mapping for PyPI package name to apt package name
            pypi_to_apt = {'pyyaml': 'yaml'}
            
            print("Python packages needed:")
            print(f"  pip install {' '.join(missing_python)}")
            print("  OR (Debian/Ubuntu):")
            apt_packages = [f"python3-{pypi_to_apt.get(p, p)}" for p in missing_python]
            print(f"  sudo apt-get install {' '.join(apt_packages)}")
        
        sys.exit(1)
    
    print("\n✅ All dependencies satisfied!\n")

    try:

        # Step 2: Download and set up Bento4
        BENTO4_URL = "https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip"
        zip_path = PROJECT_DIR / "bento4.zip"

        if not BENTO4_DIR.exists():
            print(f"Downloading Bento4 from {BENTO4_URL}...")
            urllib.request.urlretrieve(BENTO4_URL, zip_path)
            print("Extracting Bento4...")

            BENTO4_DIR.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(BENTO4_DIR)
            os.remove(zip_path)

            print("Bento4 installed inside project folder.")
            
            # Find Bento4 bin directory and make files executable
            bin_candidates = list(BENTO4_DIR.glob("Bento4*"))
            if bin_candidates:
                bin_dir = bin_candidates[0] / "bin"
                print(f"Setting up Bento4 tools from: {bin_dir}")
                
                if not bin_dir.exists():
                    print(f"ERROR: Bin directory does not exist: {bin_dir}")
                    return
                
                # Make all files executable (ZIP extraction doesn't preserve execute permissions)
                print("Setting execute permissions on all Bento4 tools...")
                all_files = list(bin_dir.glob("*"))
                for exe_file in all_files:
                    if exe_file.is_file():
                        try:
                            # Add execute permission for owner, group, and others
                            current_mode = exe_file.stat().st_mode
                            new_mode = current_mode | 0o755  # rwxr-xr-x
                            exe_file.chmod(new_mode)
                            print(f"  Set execute permission on {exe_file.name}")
                        except Exception as e:
                            print(f"  ERROR: Failed to set execute permission on {exe_file.name}: {e}")
                
                # Add Bento4 tools to PATH for current session
                os.environ["PATH"] = f"{bin_dir}:{os.environ['PATH']}"
                print(f"Added Bento4 bin directory to PATH: {bin_dir}")
            else:
                print("WARN: Could not find Bento4 extracted folder")
                
        else:
            print("INFO: Bento4 already exists, skipping download")
            
            # Ensure Bento4 tools are available even if already downloaded
            bin_candidates = list(BENTO4_DIR.glob("Bento4*"))
            if bin_candidates:
                bin_dir = bin_candidates[0] / "bin"
                os.environ["PATH"] = f"{bin_dir}:{os.environ['PATH']}"
                print(f"Added existing Bento4 bin to PATH: {bin_dir}")


        # Step 3: Download and extract wrapper
        WRAPPER_URL = "https://github.com/WorldObservationLog/wrapper/releases/download/Wrapper.x86_64.0df45b5/Wrapper.x86_64.0df45b5.zip"
        wrapper_zip = PROJECT_DIR / "wrapper.x86_64.zip"

        if not WRAPPER_DIR.exists():
            print(f"Downloading wrapper from {WRAPPER_URL}...")
            urllib.request.urlretrieve(WRAPPER_URL, wrapper_zip)
            print("Extracting wrapper...")

            WRAPPER_DIR.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(wrapper_zip, "r") as zip_ref:
                zip_ref.extractall(WRAPPER_DIR)
            os.remove(wrapper_zip)

            # Ensure the wrapper binary is executable
            wrapper_bin = WRAPPER_DIR / "wrapper"
            try:
                if wrapper_bin.exists():
                    current_mode = wrapper_bin.stat().st_mode
                    wrapper_bin.chmod(current_mode | 0o755)
                    print("Set execute permission on wrapper binary")
                else:
                    print("WARN: Wrapper binary not found after extraction")
            except Exception as e:
                print(f"WARN: Failed to chmod wrapper binary: {e}")

            print("Wrapper extracted inside project folder")
        else:
            print("INFO: Wrapper already exists, skipping download")

        # Step 4: Clone Apple Music Downloader repo
        if not AMD_DIR.exists():
            print("Cloning Apple Music Downloader...")
            subprocess.run(
                ["git", "clone", "https://github.com/zhaarey/apple-music-downloader", str(AMD_DIR)],
                check=True
            )
            print("Apple Music Downloader cloned inside project folder")
            
            # Fix Go version format in go.mod (e.g., change "go 1.23.1" to "go 1.23")
            go_mod_path = AMD_DIR / "go.mod"
            if go_mod_path.exists():
                try:
                    with open(go_mod_path, 'r') as f:
                        content = f.read()
                    
                    # Replace 3-part version numbers with 2-part format
                    import re
                    fixed_content = re.sub(r'^go (\d+\.\d+)\.\d+', r'go \1', content, flags=re.MULTILINE)
                    
                    if fixed_content != content:
                        with open(go_mod_path, 'w') as f:
                            f.write(fixed_content)
                        print("Fixed Go version format in go.mod")
                except Exception as e:
                    print(f"WARN: Could not fix go.mod: {e}")
        else:
            print("INFO: Apple Music Downloader already exists, skipping clone")

        print("First setup complete!")

    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed during setup: {e}")
        sys.exit(1)

def start():
    print("Starting Apple Music Downloader Web UI...")

    # Ensure Bento4 and Wrapper are in PATH locally
    bin_candidates = list(BENTO4_DIR.glob("Bento4*"))  # find extracted folder
    if bin_candidates:
        bin_dir = bin_candidates[0] / "bin"
        os.environ["PATH"] = f"{bin_dir}:{os.environ['PATH']}"

    os.environ["PATH"] = f"{WRAPPER_DIR}:{os.environ['PATH']}"

    # Import and run the Flask app
    from app import app   # FIXED: no double "app.app"
    app.run(host="0.0.0.0", port=5000, debug=True)

# === First run check ===
marker_file = PROJECT_DIR / "firstrun"

if not marker_file.exists():
    firstsetup()
    with open(marker_file, "w") as f:
        f.write("This file marks that first setup has been completed.\n")

start()
