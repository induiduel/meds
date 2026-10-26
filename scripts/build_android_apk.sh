#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

export ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
export ANDROID_SDK_ROOT="$ANDROID_HOME"

if [ -d "$HOME/.gradle/jdks/azul_systems__inc_-21-amd64-linux.2" ]; then
  export JAVA_HOME="$HOME/.gradle/jdks/azul_systems__inc_-21-amd64-linux.2"
elif [ -d "/snap/android-studio/current/jbr" ]; then
  export JAVA_HOME="/snap/android-studio/current/jbr"
fi
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/platform-tools:$PATH"

echo "[1/5] Vite ön yüz derleniyor..."
npx vite build

echo "[2/5] Güncel derleme parçaları dist-android/ içine hazırlanıyor..."
node scripts/prepare-android-dist.mjs

echo "[3/5] MeDSor uygulama ikonları Android kaynaklarına kopyalanıyor..."
for pair in "mdpi:72" "hdpi:96" "xhdpi:144" "xxhdpi:192" "xxxhdpi:512"; do
  dpi="${pair%%:*}"
  sz="${pair##*:}"
  src="public/icons/icon-${sz}x${sz}.png"
  target_dir="android/app/src/main/res/mipmap-${dpi}"
  if [ -f "$src" ] && [ -d "$target_dir" ]; then
    cp "$src" "$target_dir/ic_launcher.png"
    cp "$src" "$target_dir/ic_launcher_round.png"
    cp "$src" "$target_dir/ic_launcher_foreground.png"
  fi
done

echo "[4/5] Capacitor Android projesi eşitleniyor..."
npx cap sync android

echo "[5/5] Android APK (Gradle assembleDebug) derleniyor..."
cd android
./gradlew assembleDebug --no-daemon
cd ..

APK_SRC="android/app/build/outputs/apk/debug/app-debug.apk"
if [ -f "$APK_SRC" ]; then
  mkdir -p public/apk dist/apk
  cp "$APK_SRC" public/apk/medsor-yonetim.apk
  cp "$APK_SRC" dist/apk/medsor-yonetim.apk
  SIZE=$(du -h public/apk/medsor-yonetim.apk | cut -f1)
  echo "✅ MeDSor Yönetim APK hazır: public/apk/medsor-yonetim.apk ($SIZE)"
else
  echo "❌ APK çıktısı bulunamadı: $APK_SRC"
  exit 1
fi
