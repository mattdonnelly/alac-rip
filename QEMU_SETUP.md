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

## Accessing the VM Shell

If you need to access the VM's shell for troubleshooting:

### Option 1: Serial Console (if `-nographic` is used)

When running with `-nographic`, you'll have direct access to the VM's console. You can:
- Log in if prompted (credentials depend on the VM image)
- Run commands directly
- Check running processes: `ps aux`
- Check network: `netstat -tlnp`

### Option 2: SSH Access (if configured)

If the VM has SSH configured, you can add SSH port forwarding:

```bash
qemu-system-x86_64 \
  -m 2048 \
  -smp 2 \
  -drive file=qemu-vm/wrapper.qcow2,format=qcow2 \
  -net nic \
  -net user,hostfwd=tcp::2222-:22,hostfwd=tcp::10020-:10020,hostfwd=tcp::20020-:20020,hostfwd=tcp::30020-:30020 \
  -nographic
```

Then connect via:
```bash
ssh -p 2222 user@localhost
```

### Inspecting the VM

Once you have shell access, you can:

1. **Check if wrapper is running:**
   ```bash
   ps aux | grep wrapper
   ```

2. **Check wrapper installation location:**
   ```bash
   which wrapper
   find / -name "wrapper" -type f 2>/dev/null
   ```

3. **Check listening ports:**
   ```bash
   netstat -tlnp | grep -E "10020|20020|30020"
   # or
   ss -tlnp | grep -E "10020|20020|30020"
   ```

4. **Check wrapper logs (if available):**
   ```bash
   journalctl -u wrapper
   # or check common log locations
   cat /var/log/wrapper.log
   dmesg | tail
   ```

5. **Check filesystem structure:**
   ```bash
   ls -la /
   ls -la /root
   ls -la /home
   pwd
   ```

## Running the Flask Application

Once the QEMU VM is running, you can run the Flask web interface on your Mac:

### 1. Install Python Dependencies

```bash
pip3 install flask pyyaml
```

### 2. Configure Wrapper Connection

The Flask app will automatically connect to `localhost:10020`, `localhost:20020`, and `localhost:30020`, which are forwarded from the QEMU VM.

**Important Note about Flask App with QEMU VM:**

The current Flask application is designed to run the wrapper binary locally. When using the QEMU VM method, there are some limitations:

- **Wrapper Login via Flask UI won't work** - The Flask app tries to execute a local wrapper binary, which won't interact with the wrapper running in the VM
- **You need to authenticate directly in the VM** - Login to the wrapper must be done inside the QEMU VM, not through the Flask web interface
- **The Flask app becomes a monitoring tool only** - You can use it to monitor downloads, but not to manage wrapper authentication

**Recommended Approach:**

1. Start the QEMU VM with the wrapper
2. Login to the wrapper inside the VM using the command line
3. Then use the Flask app for downloading and monitoring

**Alternative:** If you need the full Flask integration (including login via web UI), use the Docker method instead of QEMU VM.

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

### "chdir: No such file or directory" Error

**Symptom:** When running the wrapper manually inside the VM, you see:
```
chdir: No such file or directory
```

**Root Cause:** The wrapper binary is trying to change to a working directory that doesn't exist in the VM's filesystem.

**Solutions:**

1. **Create the working directory:**
   
   If you have shell access to the VM, create the directory the wrapper expects:
   ```bash
   # Inside the QEMU VM
   mkdir -p /root
   cd /root
   ./wrapper -L email:password
   ```
   
   Or create a specific working directory:
   ```bash
   mkdir -p /app/wrapper
   cd /app/wrapper
   ./wrapper -L email:password
   ```

2. **Run wrapper from its installation directory:**
   
   The wrapper should be pre-installed in the VM. Find and run it from there:
   ```bash
   # Inside the QEMU VM - find where wrapper is installed
   find / -name "wrapper" -type f 2>/dev/null
   
   # Then cd to that directory and run it
   cd /path/to/wrapper/directory
   ./wrapper -L email:password
   ```

3. **Check if wrapper is already running:**
   
   The VM image should auto-start the wrapper service. Check if it's already running:
   ```bash
   # Inside the QEMU VM
   ps aux | grep wrapper
   netstat -tlnp | grep -E "10020|20020|30020"
   ```
   
   If it's already running, you don't need to start it manually!

4. **Use absolute paths:**
   
   Instead of relying on the current directory, use absolute paths:
   ```bash
   /usr/local/bin/wrapper -L email:password
   # or wherever the wrapper is installed in the VM
   ```

**Important Note:** The QEMU VM image provided by the wrapper author should have the wrapper pre-configured to auto-start. If you're getting this error, it likely means:
- You're trying to manually run the wrapper when it's already running
- The wrapper isn't installed where you expect in the VM
- You need to check the VM's filesystem structure

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
