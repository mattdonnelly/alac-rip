# QEMU VM Setup Guide for M1/M2/M3 Macs

This guide explains how to use the QEMU VM image as an alternative to Docker for running the wrapper on Apple Silicon Macs.

## When to Use This Method

Use the QEMU VM method if:
- Docker with `--platform linux/amd64` consistently fails or crashes
- You experience "chroot" errors or segmentation faults
- The wrapper authentication doesn't work in Docker
- You need better compatibility at the cost of performance

**Most users should try the Docker method first** (see main README.md)

## Prerequisites

### 1. Install QEMU

Using Homebrew:
```bash
brew install qemu
```

Verify installation:
```bash
qemu-system-x86_64 --version
```

### 2. Download the QEMU VM Image

The wrapper author provides a pre-configured VM image:

1. **Access the artifact:**
   - Go to: https://github.com/WorldObservationLog/wrapper/actions/runs/22147727310
   - You need to be logged into GitHub to download artifacts
   - Click on the artifact name to download (it will be a zip file)

2. **Extract the image:**
   ```bash
   # After downloading the zip file
   unzip wrapper-artifact.zip
   # This should extract a .qcow2 file
   ```

3. **Place the image:**
   ```bash
   mkdir -p qemu-vm
   mv wrapper*.qcow2 qemu-vm/wrapper.qcow2
   ```

## Running the QEMU VM

### Option 1: Using the Helper Script (Recommended)

The repository includes a helper script that automates the process:

```bash
./run-qemu-wrapper.sh
```

This script will:
- Check if QEMU is installed
- Verify the qcow2 image exists
- Start the VM with appropriate port forwarding
- Forward wrapper ports (10020, 20020, 30020) to your Mac

### Option 2: Manual QEMU Command

If you prefer to run QEMU manually:

```bash
qemu-system-x86_64 \
  -m 2048 \
  -smp 2 \
  -drive file=qemu-vm/wrapper.qcow2,format=qcow2 \
  -net nic \
  -net user,hostfwd=tcp::10020-:10020,hostfwd=tcp::20020-:20020,hostfwd=tcp::30020-:30020 \
  -nographic
```

**Parameter explanation:**
- `-m 2048`: Allocate 2GB RAM to the VM
- `-smp 2`: Use 2 CPU cores
- `-drive`: Specify the qcow2 disk image
- `-net user,hostfwd`: Forward wrapper ports to localhost
- `-nographic`: Run in terminal mode (no GUI window)

### Exiting QEMU

To exit the QEMU VM:
1. Press `Ctrl+A`
2. Then press `X`

Or run `poweroff` inside the VM if you have shell access.

## Running the Flask Application

Once the QEMU VM is running, you can run the Flask web interface on your Mac:

### 1. Install Python Dependencies

```bash
pip3 install flask pyyaml
```

### 2. Configure Wrapper Connection

The Flask app will automatically connect to `localhost:10020`, `localhost:20020`, and `localhost:30020`, which are forwarded from the QEMU VM.

### 3. Start the Flask App

```bash
python3 main.py
```

### 4. Access the Web Interface

Open your browser and go to:
```
http://localhost:5000
```

## VM Image Contents

The qcow2 image provided by the wrapper author contains:
- Minimal Linux distribution (likely Alpine or similar)
- Wrapper binary pre-installed and configured
- Auto-start services to run wrapper on boot
- All necessary dependencies

## Troubleshooting

### VM Won't Boot

**Symptom:** QEMU exits immediately or shows errors

**Solutions:**
1. Verify the qcow2 file is not corrupted:
   ```bash
   qemu-img check qemu-vm/wrapper.qcow2
   ```
2. Try with more memory:
   ```bash
   qemu-system-x86_64 -m 4096 ... # 4GB instead of 2GB
   ```
3. Check QEMU installation:
   ```bash
   brew reinstall qemu
   ```

### Cannot Connect to Wrapper

**Symptom:** Flask app shows "connection refused" for wrapper

**Solutions:**
1. Verify the VM is running and ports are forwarded
2. Check if wrapper service started inside VM:
   ```bash
   # If you have VM shell access
   ps aux | grep wrapper
   ```
3. Test port forwarding:
   ```bash
   nc -zv localhost 10020
   nc -zv localhost 20020
   nc -zv localhost 30020
   ```

### Slow Performance

**Symptom:** VM is very slow or unresponsive

**Solutions:**
1. Increase VM resources:
   ```bash
   -m 4096 -smp 4  # 4GB RAM, 4 CPU cores
   ```
2. Close other applications to free up resources
3. Consider using the Docker method instead if performance is critical

### VM Disk is Full

**Symptom:** VM shows "no space left on device"

**Solutions:**
1. Resize the qcow2 image:
   ```bash
   qemu-img resize qemu-vm/wrapper.qcow2 +10G
   ```
2. Boot the VM and resize the filesystem inside

## Performance Considerations

- **RAM**: The VM needs at least 2GB, 4GB recommended
- **CPU**: Uses 2-4 CPU cores depending on configuration
- **Disk**: Minimal disk usage, image is typically < 1GB
- **Network**: Port forwarding has minimal overhead

## Comparing Methods

| Aspect | Docker | QEMU VM |
|--------|--------|---------|
| Setup Complexity | Simple | Complex |
| Performance | Better | Slower |
| Resource Usage | Lower | Higher |
| Compatibility | Usually works | Maximum compatibility |
| Recommended | Yes | Only if Docker fails |

## Additional Resources

- Wrapper GitHub: https://github.com/WorldObservationLog/wrapper
- QEMU Documentation: https://www.qemu.org/docs/master/
- Original artifact: https://github.com/WorldObservationLog/wrapper/actions/runs/22147727310

## Need Help?

If you encounter issues:
1. First try the Docker method (see main README.md)
2. Check this troubleshooting section
3. Open an issue on GitHub with:
   - Your Mac model (M1/M2/M3)
   - macOS version
   - QEMU version
   - Complete error messages
   - Steps you've already tried
