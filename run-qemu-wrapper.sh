#!/bin/bash

# Helper script to run the wrapper in QEMU VM on M1/M2/M3 Macs
# This is an alternative to Docker when emulation issues occur

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QEMU_DIR="$SCRIPT_DIR/qemu-vm"
QCOW2_FILE="$QEMU_DIR/wrapper.qcow2"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=================================================="
echo "  QEMU Wrapper VM Runner for M1/M2/M3 Macs"
echo "=================================================="
echo ""

# Check if QEMU is installed
if ! command -v qemu-system-x86_64 &> /dev/null; then
    echo -e "${RED}Error: QEMU is not installed${NC}"
    echo ""
    echo "Install QEMU with Homebrew:"
    echo "  brew install qemu"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ QEMU is installed${NC}"

# Check if qcow2 file exists
if [ ! -f "$QCOW2_FILE" ]; then
    echo -e "${YELLOW}⚠ QEMU VM image not found${NC}"
    echo ""
    echo "You need to download the wrapper QEMU image:"
    echo ""
    echo "1. Go to: https://github.com/WorldObservationLog/wrapper/actions/runs/22147727310"
    echo "2. Download the artifact (requires GitHub login)"
    echo "3. Extract the qcow2 file from the zip"
    echo "4. Place it at: $QCOW2_FILE"
    echo ""
    echo "Or create the directory and place your qcow2 file there:"
    echo "  mkdir -p $QEMU_DIR"
    echo "  cp /path/to/your/wrapper.qcow2 $QCOW2_FILE"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ QEMU VM image found${NC}"
echo ""
echo "Starting QEMU VM with wrapper..."
echo "The VM will forward wrapper ports to localhost:"
echo "  - Port 10020 (decrypt)"
echo "  - Port 20020 (m3u8)"
echo "  - Port 30020 (account)"
echo ""
echo -e "${YELLOW}Note: Press Ctrl+A then X to exit QEMU${NC}"
echo ""
echo "Starting in 3 seconds..."
sleep 3

# Run QEMU with appropriate settings
qemu-system-x86_64 \
    -m 2048 \
    -smp 2 \
    -drive file="$QCOW2_FILE",format=qcow2 \
    -net nic \
    -net user,hostfwd=tcp::10020-:10020,hostfwd=tcp::20020-:20020,hostfwd=tcp::30020-:30020 \
    -nographic

echo ""
echo "QEMU VM stopped."
