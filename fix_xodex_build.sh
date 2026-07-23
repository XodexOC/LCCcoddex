#!/bin/bash

set -e

PROJECT="$HOME/Загрузки/LCCcoddex"

cd "$PROJECT"

echo "=== Xodex build repair ==="

echo "[1/5] Проверка start-stop-daemon..."

if [ ! -e chroot/usr/sbin/start-stop-daemon ]; then
    echo "start-stop-daemon отсутствует, копирую..."
    sudo mkdir -p chroot/usr/sbin
    sudo cp /usr/sbin/start-stop-daemon chroot/usr/sbin/
else
    echo "OK: start-stop-daemon найден"
fi


echo "[2/5] Проверка dpkg..."

if [ -x chroot/usr/bin/dpkg ]; then
    echo "OK: dpkg найден"
else
    echo "ERROR: dpkg отсутствует"
fi


echo "[3/5] Исправление владельцев chroot..."

sudo chown -R root:root chroot


echo "[4/5] Проверка PATH внутри chroot..."

sudo chroot chroot /bin/bash -c '
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
which start-stop-daemon || true
which dpkg || true
'


echo "[5/5] Очистка временных монтирований..."

sudo umount -lf chroot/proc 2>/dev/null || true
sudo umount -lf chroot/sys 2>/dev/null || true
sudo umount -lf chroot/dev 2>/dev/null || true


echo ""
echo "=== Repair finished ==="
echo "Продолжаю сборку..."
echo ""

sudo lb build
