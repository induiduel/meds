#!/bin/bash
# MedSoru GPU & Audio Otomatik Uyandırma ve Kurtarma Scripti
echo "[$(date '+%Y-%m-%d %H:%M:%S')] GPU/Ses kurtarma başlatılıyor..."

# 1. Ses aygıtını unbind / bind et (GPU D3cold kilidini açar)
if [ -d "/sys/bus/pci/drivers/snd_hda_intel" ]; then
    echo "0000:01:00.1" | sudo tee /sys/bus/pci/drivers/snd_hda_intel/unbind > /dev/null 2>&1
    sleep 0.5
    echo "0000:01:00.1" | sudo tee /sys/bus/pci/drivers/snd_hda_intel/bind > /dev/null 2>&1
fi

# 2. wake-audio fallback
if [ -x "/usr/local/bin/wake-audio" ]; then
    sudo /usr/local/bin/wake-audio > /dev/null 2>&1
fi

# 3. GPU Runtime Power modunu ON yap
echo on | sudo tee /sys/bus/pci/devices/0000:01:00.0/power/control > /dev/null 2>&1
echo on | sudo tee /sys/bus/pci/devices/0000:01:00.1/power/control > /dev/null 2>&1

# 4. nvidia-smi ile GPU'yu tetikle
if nvidia-smi > /dev/null 2>&1; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] GPU başarıyla uyandırıldı ve hazır!"
    exit 0
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] UYARI: nvidia-smi yanıt vermedi!"
    exit 1
fi
