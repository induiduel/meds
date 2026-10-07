#!/usr/bin/env python3
"""
MedSoru AI & Donanım Analiz ve Kontrol Paneli (Web Dashboard)
Erişim: http://localhost:8085
"""
import http.server
import json
import os
import re
import socketserver
import subprocess
import sys
import time
import fcntl
from pathlib import Path

try:
    import psutil
except ImportError:
    psutil = None

PORT = 8085
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent if BASE_DIR.name == "meds" else BASE_DIR
MEDS_DIR = (BASE_DIR if BASE_DIR.name == "meds" else BASE_DIR / "meds")
TEMP_DIR = PROJECT_ROOT / "meds_temp"
PHASE_QUEUE_FILE = TEMP_DIR / "state" / "phase_queue.json"
PHASE_QUEUE_LOCK = TEMP_DIR / "state" / "phase_queue.lock"
PHASE_CYCLE_STATE = TEMP_DIR / "state" / "phase_cycle_state.json"


HTML_PAGE = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MedSoru AI - Analiz ve Sistem Kontrol Merkezi</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.08); }
        .pulse-dot { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .4; } }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-7xl mx-auto space-y-6">
        <!-- Header -->
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-4 border-b border-slate-700/60">
            <div>
                <div class="flex items-center gap-3">
                    <div class="p-2.5 bg-indigo-600/30 text-indigo-400 rounded-xl border border-indigo-500/30">
                        <i class="fa-solid fa-microchip text-2xl"></i>
                    </div>
                    <div>
                        <h1 class="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
                            MedSoru AI Denetim & Analiz Merkezi
                        </h1>
                        <p class="text-sm text-slate-400">Tüm yerel yapay zeka modelleri, donanım tüketimleri ve pipeline analitiği</p>
                    </div>
                </div>
            </div>
                <a href="http://localhost:3000" target="_blank" class="px-3.5 py-1.5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white rounded-lg text-xs font-semibold shadow-lg transition flex items-center gap-1.5">
                    <i class="fa-solid fa-graduation-cap"></i> App (3000)
                </a>
                <a href="http://localhost:8000" target="_blank" class="px-3.5 py-1.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700 text-white rounded-lg text-xs font-semibold shadow-lg transition flex items-center gap-1.5">
                    <i class="fa-solid fa-bolt"></i> Hibrit API (8000)
                </a>
                <a href="http://localhost:8085" target="_blank" class="px-3.5 py-1.5 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white rounded-lg text-xs font-semibold shadow-lg transition flex items-center gap-1.5">
                    <i class="fa-solid fa-gauge-high"></i> Kokpit (8085)
                </a>
                <div class="px-3 py-2 glass rounded-lg text-xs text-slate-400 flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 pulse-dot"></span> Canlı İzleme (2s / 5s)
                </div>
            </div>
        </header>

        <!-- Üst Navigasyon Sekmeleri (Multi-Page Tabs) -->
        <nav class="flex items-center gap-2 border-b border-slate-700/60 pb-2 overflow-x-auto">
            <button id="nav-btn-overview" onclick="switchTab('overview')" class="tab-btn px-4 py-2.5 rounded-xl font-medium text-sm flex items-center gap-2 bg-indigo-600 text-white shadow-lg transition whitespace-nowrap">
                <i class="fa-solid fa-gauge-high"></i> Genel Bakış & Donanım Kokpiti
            </button>
            <button id="nav-btn-stages" onclick="switchTab('stages')" class="tab-btn px-4 py-2.5 rounded-xl font-medium text-sm flex items-center gap-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition whitespace-nowrap">
                <i class="fa-solid fa-list-check text-cyan-400"></i> Aşama & Faz Yol Haritası (Süreç & Tahminler)
                <span class="px-2 py-0.5 rounded-full text-xs font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">Canlı Akış</span>
            </button>
            <button id="nav-btn-rejected" onclick="switchTab('rejected')" class="tab-btn px-4 py-2.5 rounded-xl font-medium text-sm flex items-center gap-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition whitespace-nowrap">
                <i class="fa-solid fa-filter-circle-xmark text-amber-400"></i> Elenen & İnceleme Dosyaları
                <span id="nav-rejected-badge" class="px-2 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">0</span>
            </button>
            <button id="nav-btn-master" onclick="switchTab('master')" class="tab-btn px-4 py-2.5 rounded-xl font-medium text-sm flex items-center gap-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition whitespace-nowrap">
                <i class="fa-solid fa-sliders text-amber-400"></i> Master Süreç & Mod Yöneticisi
                <span id="nav-master-mode-badge" class="px-2 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">Normal</span>
            </button>
        </nav>

        <!-- SEKME 1: GENEL BAKIŞ & DONANIM KOKPİTİ -->
        <div id="tab-overview" class="tab-content space-y-6">
        <!-- Donanım Sayaçları (CPU, RAM, GPU, Disk) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- CPU -->
            <div class="glass p-5 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs uppercase font-semibold tracking-wider">İşlemci (CPU)</span>
                    <i class="fa-solid fa-server text-indigo-400"></i>
                </div>
                <div class="flex items-baseline gap-2">
                    <span id="cpu-percent" class="text-3xl font-extrabold text-white">-%</span>
                    <span id="cpu-cores" class="text-xs text-slate-400">Çekirdek: -</span>
                </div>
                <div class="w-full bg-slate-700/50 h-2 rounded-full mt-3 overflow-hidden">
                    <div id="cpu-bar" class="bg-indigo-500 h-full rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
            </div>

            <!-- RAM -->
            <div class="glass p-5 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs uppercase font-semibold tracking-wider">Sistem Belleği (RAM)</span>
                    <i class="fa-solid fa-memory text-cyan-400"></i>
                </div>
                <div class="flex items-baseline gap-2">
                    <span id="ram-used" class="text-3xl font-extrabold text-white">- GB</span>
                    <span id="ram-total" class="text-xs text-slate-400">/ - GB</span>
                </div>
                <div class="w-full bg-slate-700/50 h-2 rounded-full mt-3 overflow-hidden">
                    <div id="ram-bar" class="bg-cyan-500 h-full rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
            </div>

            <!-- GPU -->
            <div class="glass p-5 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs uppercase font-semibold tracking-wider">Ekran Kartı (GPU & VRAM)</span>
                    <i class="fa-solid fa-bolt text-amber-400"></i>
                </div>
                <div class="flex items-baseline gap-2">
                    <span id="gpu-vram-used" class="text-3xl font-extrabold text-white">- MB</span>
                    <span id="gpu-vram-total" class="text-xs text-slate-400">/ - MB</span>
                    <span id="gpu-temp" class="text-xs text-amber-400 ml-auto font-semibold">-°C</span>
                </div>
                <div class="w-full bg-slate-700/50 h-2 rounded-full mt-3 overflow-hidden">
                    <div id="gpu-bar" class="bg-amber-500 h-full rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
                <div class="flex justify-between items-center text-[11px] text-slate-400 mt-2">
                    <span class="truncate" id="gpu-model">Nvidia GPU</span>
                    <span class="text-amber-300 font-mono font-bold" id="gpu-util">Yük: -%</span>
                </div>
            </div>

            <!-- Disk / SSD -->
            <div class="glass p-5 rounded-2xl">
                <div class="flex justify-between items-center text-slate-400 mb-2">
                    <span class="text-xs uppercase font-semibold tracking-wider">SSD / Depolama & Hız</span>
                    <i class="fa-solid fa-hard-drive text-emerald-400"></i>
                </div>
                <div class="flex items-baseline gap-2">
                    <span id="disk-used" class="text-3xl font-extrabold text-white">- GB</span>
                    <span id="disk-total" class="text-xs text-slate-400">/ - GB</span>
                </div>
                <div class="w-full bg-slate-700/50 h-2 rounded-full mt-3 overflow-hidden">
                    <div id="disk-bar" class="bg-emerald-500 h-full rounded-full transition-all duration-500" style="width: 0%"></div>
                </div>
                <div class="flex justify-between items-center text-[11px] text-slate-400 mt-2 font-mono">
                    <span class="text-cyan-400"><i class="fa-solid fa-arrow-down"></i> <span id="disk-read">0 MB/s</span></span>
                    <span class="text-emerald-400"><i class="fa-solid fa-arrow-up"></i> <span id="disk-write">0 MB/s</span></span>
                </div>
                <div id="secondary-disk-box" class="mt-2 pt-2 border-t border-slate-700/60 text-[10px] text-slate-400 flex justify-between items-center">
                    <span>Yedek Disk (%60+ Taşma):</span>
                    <span id="secondary-disk-status" class="text-emerald-400 font-mono font-semibold">126 GB Boş (/mnt/yedekler)</span>
                </div>
            </div>
        </div>

        <!-- 2 Kolonlu Orta Bölüm: Aktif Çalışan Yapay Zeka & Boru Hattı Durumu -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Sol: Aktif Bellekteki Model & Görevi -->
            <div class="glass p-6 rounded-2xl lg:col-span-2 space-y-4">
                <div class="flex justify-between items-center">
                    <h2 class="text-lg font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-brain text-purple-400"></i> Şu An Çalışan Yerel Model & Görevi
                    </h2>
                    <span id="active-model-badge" class="px-2.5 py-1 text-xs font-semibold rounded-full bg-slate-700 text-slate-300">
                        Tespit ediliyor...
                    </span>
                </div>

                <div id="active-model-box" class="p-4 rounded-xl bg-slate-800/80 border border-slate-700/50 space-y-3">
                    <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-2">
                        <div>
                            <div id="model-name" class="text-xl font-bold text-indigo-300">-</div>
                            <div id="model-details" class="text-xs text-slate-400">Aile: - | Boyut: - | Quantization: -</div>
                        </div>
                        <div class="text-right">
                            <span id="model-vram" class="text-sm font-semibold text-emerald-400">VRAM: -</span>
                        </div>
                    </div>

                    <div class="border-t border-slate-700/60 pt-3">
                        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Şu Anda Yaptığı İş:</div>
                        <div id="model-task" class="text-sm text-slate-200 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                            -
                        </div>
                    </div>

                    <!-- Canlı Yapay Zeka Kaynak Tüketim Çizelgesi -->
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-slate-700/60 text-center font-mono">
                        <div class="p-2 rounded-lg bg-slate-900/40 border border-slate-800">
                            <div class="text-[10px] text-slate-400 uppercase">Model CPU Yükü</div>
                            <div id="model-cpu" class="text-sm font-bold text-indigo-400">-%</div>
                        </div>
                        <div class="p-2 rounded-lg bg-slate-900/40 border border-slate-800">
                            <div class="text-[10px] text-slate-400 uppercase">Model RAM Kullanımı</div>
                            <div id="model-ram" class="text-sm font-bold text-cyan-400">- MB</div>
                        </div>
                        <div class="p-2 rounded-lg bg-slate-900/40 border border-slate-800">
                            <div class="text-[10px] text-slate-400 uppercase">GPU VRAM</div>
                            <div id="model-gpu-vram" class="text-sm font-bold text-amber-400">- MB</div>
                        </div>
                        <div class="p-2 rounded-lg bg-slate-900/40 border border-slate-800">
                            <div class="text-[10px] text-slate-400 uppercase">Konteyner Disk I/O</div>
                            <div id="model-blockio" class="text-sm font-bold text-emerald-400">-</div>
                        </div>
                    </div>
                </div>

                <!-- Kurulu Tüm Modeller Tablosu -->
                <div class="pt-2">
                    <h3 class="text-sm font-bold text-slate-300 mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-list-check text-indigo-400"></i> Sistemde Yüklü Yerel Modeller Denetim Tablosu
                    </h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs text-slate-300">
                            <thead class="bg-slate-800/60 text-slate-400 uppercase text-[10px] tracking-wider">
                                <tr>
                                    <th class="p-2.5 rounded-l-lg">Model</th>
                                    <th class="p-2.5">Parametre</th>
                                    <th class="p-2.5">Disk Boyutu</th>
                                    <th class="p-2.5">Projedeki Rolü</th>
                                    <th class="p-2.5 rounded-r-lg text-right">Durum</th>
                                </tr>
                            </thead>
                            <tbody id="models-table-body" class="divide-y divide-slate-800/50">
                                <tr><td colspan="5" class="p-3 text-center text-slate-500">Modeller yükleniyor...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Sağ: Pipeline Aşamaları ve Veri İlerlemesi -->
            <div class="glass p-6 rounded-2xl space-y-4">
                <h2 class="text-lg font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-diagram-project text-cyan-400"></i> Boru Hattı İlerlemesi
                </h2>

                <div class="space-y-3">
                    <div class="p-3 rounded-xl bg-slate-800/50 border border-slate-700/40">
                        <div class="flex justify-between items-center text-xs mb-1">
                            <span class="text-slate-300 font-medium">1. Ham Kaynaklar (Downloads)</span>
                            <span id="cnt-dl" class="font-bold text-indigo-400">-</span>
                        </div>
                        <div class="text-[11px] text-slate-400">Drive'dan çekilen slayt ve çıkmışlar</div>
                    </div>

                    <div class="p-3 rounded-xl bg-slate-800/50 border border-slate-700/40">
                        <div class="flex justify-between items-center text-xs mb-1">
                            <span class="text-slate-300 font-medium">2. Temp1 (Ham OCR / Çıktı)</span>
                            <span id="cnt-t1" class="font-bold text-cyan-400">-</span>
                        </div>
                        <div class="text-[11px] text-slate-400">PyMuPDF / Tesseract ilk metinler</div>
                    </div>

                    <div class="p-3 rounded-xl bg-slate-800/50 border border-slate-700/40">
                        <div class="flex justify-between items-center text-xs mb-1">
                            <span class="text-slate-300 font-medium">3. Temp2 (Düzeltilmiş & Sorular)</span>
                            <span id="cnt-t2" class="font-bold text-amber-400">-</span>
                        </div>
                        <div class="text-[11px] text-slate-400">Türkçe/dil bilgisi onarımlı & A-E şıklı (413 slayt + 122 çıkmış)</div>
                    </div>

                    <div class="p-3 rounded-xl bg-purple-950/20 border border-purple-500/40">
                        <div class="flex justify-between items-center text-xs mb-1">
                            <span class="text-purple-300 font-medium">4. Temp3 (RAG, Vektör & Eşleşen)</span>
                            <span id="cnt-t3" class="font-bold text-purple-400">-</span>
                        </div>
                        <div id="cnt-t3-detail" class="text-[11px] text-purple-300/80 font-mono">
                            Slayt Kaynak: -/413 | Vektör: - | Soru Havuzu: -
                        </div>
                        <div class="text-[10px] text-slate-400 mt-0.5">Slayt chunkları bge-m3 vektörleştirilip çıkmış sorularla eşleştirilir</div>
                    </div>

                    <div class="p-3 rounded-xl bg-emerald-950/20 border border-emerald-500/30">
                        <div class="flex justify-between items-center text-xs mb-1">
                            <span class="text-emerald-300 font-medium">5. meds_database (Doğrulanmış RAG)</span>
                            <span id="cnt-db" class="font-bold text-emerald-400">-</span>
                        </div>
                        <div class="text-[11px] text-slate-400">Sadece onaylı ve amfi kanıtlı sorular/chunklar (Aşama 4 çıktısı)</div>
                    </div>
                </div>

                <!-- Servis Durum Rozetleri -->
                <div class="pt-2 border-t border-slate-700/60 flex justify-between items-center text-xs">
                    <span class="text-slate-400">Pipeline Servisi:</span>
                    <span id="srv-pipeline" class="px-2 py-0.5 rounded font-semibold bg-slate-800 text-slate-400">-</span>
                </div>
                <div class="flex justify-between items-center text-xs">
                    <span class="text-slate-400">Ollama Docker:</span>
                    <span id="srv-ollama" class="px-2 py-0.5 rounded font-semibold bg-slate-800 text-slate-400">-</span>
                </div>
                <div class="flex justify-between items-center text-xs">
                    <span class="text-slate-400">Hardware Watchdog:</span>
                    <span id="srv-watchdog" class="px-2 py-0.5 rounded font-semibold bg-slate-800 text-slate-400">-</span>
                </div>
            </div>
        </div>

        <!-- YENİ: Dosya Kuyruğu, Sıradakiler ve İşlem Planı -->
        <div class="glass p-6 rounded-2xl space-y-4">
            <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-2">
                <h2 class="text-lg font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-list-ol text-amber-400"></i> Dosya İşleme Kuyruğu ve Sıralama Durumu
                </h2>
                <div class="flex items-center gap-4 text-xs font-mono">
                    <span class="text-emerald-400"><i class="fa-solid fa-check"></i> Tamamlanan: <strong id="q-done-cnt">0</strong></span>
                    <span class="text-cyan-400"><i class="fa-solid fa-spinner fa-spin"></i> İşlenen: <strong id="q-proc-cnt">1</strong></span>
                    <span class="text-amber-400"><i class="fa-solid fa-clock"></i> Sırada/Planlanan: <strong id="q-pend-cnt">0</strong></span>
                </div>
            </div>

            <!-- Genel İlerleme Yüzdesi ve İlerleme Çubuğu -->
            <div class="space-y-1.5 p-3 rounded-xl bg-slate-800/40 border border-slate-700/50">
                <div class="flex justify-between items-center text-xs">
                    <span class="text-slate-300 font-semibold flex items-center gap-2">
                        <i class="fa-solid fa-bars-progress text-indigo-400"></i> Genel Boru Hattı Tamamlanma Oranı
                    </span>
                    <span id="overall-progress-text" class="font-mono font-bold text-emerald-400 text-sm">%0</span>
                </div>
                <div class="w-full bg-slate-700/50 h-3 rounded-full overflow-hidden p-0.5 border border-slate-600/30">
                    <div id="overall-progress-bar" class="bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-400 h-full rounded-full transition-all duration-700" style="width: 0%"></div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                <!-- 1. Şu Anda İşlenen Dosya -->
                <div class="p-4 rounded-xl bg-slate-800/60 border border-cyan-500/30 space-y-2">
                    <div class="flex justify-between items-center">
                        <div class="font-bold text-cyan-300 flex items-center gap-2 text-xs uppercase tracking-wider">
                            <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 pulse-dot"></span> Şu An İşlenen Dosya
                        </div>
                        <span id="file-current-percent" class="font-mono font-bold text-emerald-400 text-xs">%0</span>
                    </div>
                    <div id="file-current-name" class="font-semibold text-white break-words bg-slate-900/60 p-2.5 rounded-lg border border-slate-700/60 text-xs">
                        -
                    </div>
                    <!-- Tekil dosya ilerleme çubuğu -->
                    <div class="w-full bg-slate-700/50 h-2 rounded-full overflow-hidden">
                        <div id="file-current-bar" class="bg-gradient-to-r from-cyan-400 to-emerald-400 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                    </div>
                    <div class="text-[11px] text-slate-400 flex justify-between items-center pt-0.5">
                        <span id="file-current-desc" class="text-slate-300 truncate max-w-[200px]">Aşama 2 (Temizleme & Soru Çıkarımı)</span>
                        <span id="file-current-counter" class="text-cyan-400 font-mono text-[10px]">-/-</span>
                    </div>
                </div>

                <!-- 2. Yeni Eklenen / Son Tamamlanan Dosyalar -->
                <div class="p-4 rounded-xl bg-slate-800/60 border border-emerald-500/30 space-y-2">
                    <div class="font-bold text-emerald-300 flex items-center gap-2 text-xs uppercase tracking-wider">
                        <i class="fa-solid fa-circle-check text-emerald-400"></i> Son Tamamlanan Dosyalar
                    </div>
                    <div id="files-completed-list" class="space-y-1.5 max-h-36 overflow-y-auto pr-1">
                        <div class="text-slate-500 italic">Yükleniyor...</div>
                    </div>
                </div>

                <!-- 3. Sıraya Alınan ve Planlanan Dosyalar -->
                <div class="p-4 rounded-xl bg-slate-800/60 border border-amber-500/30 space-y-2">
                    <div class="font-bold text-amber-300 flex items-center gap-2 text-xs uppercase tracking-wider">
                        <i class="fa-solid fa-hourglass-half text-amber-400"></i> Sırada Bekleyen / Planlananlar
                    </div>
                    <div id="files-pending-list" class="space-y-1.5 max-h-36 overflow-y-auto pr-1">
                        <div class="text-slate-500 italic">Yükleniyor...</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- YENİ: Büyük Veri ve Dosya Metrikleri Özeti (Karakter, Soru, Sayfa) -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div class="glass p-4 rounded-xl border border-indigo-500/20">
                <div class="text-[10px] text-slate-400 uppercase font-semibold">Toplam İşlenen Karakter</div>
                <div id="stat-total-chars" class="text-2xl font-black text-indigo-300 font-mono mt-1">17.9M+</div>
                <div class="text-[10px] text-slate-500 mt-0.5">Tıp amfi notu & çıkmış metni</div>
            </div>
            <div class="glass p-4 rounded-xl border border-cyan-500/20">
                <div class="text-[10px] text-slate-400 uppercase font-semibold">Çıkarılan Çıkmış Soru</div>
                <div id="stat-total-qs" class="text-2xl font-black text-cyan-300 font-mono mt-1">14,015+</div>
                <div class="text-[10px] text-slate-500 mt-0.5">Ham çıkarılmış & A-E şıklı</div>
            </div>
            <div class="glass p-4 rounded-xl border border-emerald-500/20">
                <div class="text-[10px] text-slate-400 uppercase font-semibold">Taranan Slayt / Sayfa</div>
                <div id="stat-total-pages" class="text-2xl font-black text-emerald-300 font-mono mt-1">33,099</div>
                <div class="text-[10px] text-slate-500 mt-0.5">535 döküman sayfası</div>
            </div>
            <div class="glass p-4 rounded-xl border border-amber-500/20">
                <div class="text-[10px] text-slate-400 uppercase font-semibold">Ortalama Kalite / Başarı</div>
                <div id="stat-avg-quality" class="text-2xl font-black text-amber-300 font-mono mt-1">%85.3</div>
                <div class="text-[10px] text-slate-500 mt-0.5">Tıp terimi & dil bilgisi doğruluğu</div>
            </div>
        </div>

        <!-- YENİ: Aşamalar & Gelecek Planı Yol Haritası (Roadmap) -->
        <div class="glass p-5 rounded-2xl space-y-3">
            <h3 class="text-sm font-bold text-white flex items-center gap-2">
                <i class="fa-solid fa-map-location-dot text-indigo-400"></i> Boru Hattı Durumu & Gelecek Planlama Haritası
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
                <div class="p-3 rounded-xl bg-emerald-950/30 border border-emerald-500/40">
                    <div class="flex items-center justify-between font-bold text-emerald-300 mb-1">
                        <span>Aşama 1 & 2: Temizlik</span>
                        <span class="text-[10px] bg-emerald-500/20 px-1.5 py-0.5 rounded">✓ TAMAMLANDI</span>
                    </div>
                    <p class="text-slate-400 text-[11px]">535 dosya metne ve OCR'a döküldü, OCR gürültüleri ayıklandı, Türkçe karakterler onarıldı.</p>
                </div>
                <div class="p-3 rounded-xl bg-cyan-950/30 border border-cyan-500/40">
                    <div class="flex items-center justify-between font-bold text-cyan-300 mb-1">
                        <span>Aşama 3: RAG & Eşleştirme</span>
                        <span class="text-[10px] bg-cyan-500/20 px-1.5 py-0.5 rounded pulse-dot">ŞU AN AKTİF</span>
                    </div>
                    <p class="text-slate-400 text-[11px]">Slaytlar bge-m3 ile vektörleştiriliyor; yarım sorular amfi slayt kanıtıyla 5 şıklı tam akademik soruya dönüştürülüyor.</p>
                </div>
                <div class="p-3 rounded-xl bg-purple-950/20 border border-purple-500/30">
                    <div class="flex items-center justify-between font-bold text-purple-300 mb-1">
                        <span>Aşama 4: Doğrulama & DB</span>
                        <span class="text-[10px] bg-purple-500/20 px-1.5 py-0.5 rounded">SIRADAKİ ADIM</span>
                    </div>
                    <p class="text-slate-400 text-[11px]">Sadece slayt kanıtı olan "verified" ve "fixed" sorular meds_database'e ve yerel Postgres/pgvector'a aktarılır.</p>
                </div>
                <div class="p-3 rounded-xl bg-amber-950/20 border border-amber-500/30">
                    <div class="flex items-center justify-between font-bold text-amber-300 mb-1">
                        <span>Gelecek: Web & Metadata</span>
                        <span class="text-[10px] bg-amber-500/20 px-1.5 py-0.5 rounded">PLANLANAN</span>
                    </div>
                    <p class="text-slate-400 text-[11px]">localhost:3000 üzerinde Eski vs Yeni soru kalite skorlama tablosu, semantik taksonomi ve akıllı arama havuzu.</p>
                </div>
            </div>
        </div>

        <!-- YENİ: Tüm Dosyaların Ayrıntılı Analizi ve Canlı Durum Tablosu (535 Dosya) -->
        <div class="glass p-6 rounded-2xl space-y-4">
            <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-3">
                <div>
                    <h2 class="text-lg font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-table-list text-cyan-400"></i> Dosya Bazlı Ayrıntılı Analiz & İlerleme Kataloğu
                    </h2>
                    <p class="text-xs text-slate-400 mt-0.5">Tüm tıp slaytları ve çıkmışların boyut, sayfa, karakter, çıkarılan soru ve kalite skorları</p>
                </div>
                <div class="flex items-center gap-2">
                    <input type="text" id="file-search-input" placeholder="Dosya veya ders ara..." onkeyup="filterFilesTable()" class="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 w-48 sm:w-64">
                </div>
            </div>

            <div class="overflow-x-auto rounded-xl border border-slate-700/60 max-h-96 overflow-y-auto">
                <table class="w-full text-left text-xs">
                    <thead class="bg-slate-800/80 sticky top-0 z-10 text-slate-300 uppercase text-[10px] tracking-wider border-b border-slate-700">
                        <tr>
                            <th class="p-3">Dosya / Ders Yolu</th>
                            <th class="p-3 w-28">Tür</th>
                            <th class="p-3 w-24">Boyut</th>
                            <th class="p-3 w-20">Sayfa</th>
                            <th class="p-3 w-24">Karakter</th>
                            <th class="p-3 w-20">Soru</th>
                            <th class="p-3 w-24">Kalite</th>
                            <th class="p-3 w-40 text-right">Sıradaki İşlem</th>
                        </tr>
                    </thead>
                    <tbody id="file-details-table-body" class="divide-y divide-slate-800/60 text-slate-300">
                        <tr><td colspan="8" class="p-4 text-center text-slate-500">Dosya analizi yükleniyor...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- YENİ: GraphRAG & Tıbbi Bilgi Grafı (DiGraph) İnteraktif Görselleştirici -->
        <div class="glass p-6 rounded-2xl space-y-4">
            <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-3">
                <div>
                    <h2 class="text-lg font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-circle-nodes text-purple-400"></i> GraphRAG: Tıbbi Bilgi Grafı (DiGraph) Görselleştirici
                    </h2>
                    <p class="text-xs text-slate-400 mt-0.5">Dersler, konular, hastalıklar, ilaçlar, semptomlar ve çıkmış sorular arasındaki semantik ilişkiler ağı</p>
                </div>
                <div class="flex items-center gap-2">
                    <input type="text" id="graph-search-term" placeholder="Hastalık, ilaç veya konu ara (örn: Sifilis, Penisilin)..." class="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 w-64 sm:w-80">
                    <button onclick="fetchAndRenderGraph()" class="px-3 py-1.5 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5 shadow">
                        <i class="fa-solid fa-diagram-project"></i> Grafı Çıkar
                    </button>
                    <button onclick="resetGraphView()" class="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs transition" title="Görünümü Sıfırla">
                        <i class="fa-solid fa-arrows-rotate"></i>
                    </button>
                </div>
            </div>

            <!-- Bilgi Rozetleri -->
            <div class="flex flex-wrap items-center gap-4 text-xs">
                <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-blue-500 inline-block"></span> Ders / Kurul</span>
                <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-indigo-500 inline-block"></span> Konu</span>
                <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-rose-500 inline-block"></span> Hastalık</span>
                <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span> İlaç / Tedavi</span>
                <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-amber-500 inline-block"></span> Belirti / Semptom</span>
                <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-cyan-400 inline-block"></span> Çıkmış Soru</span>
                <span id="graph-stats-text" class="text-slate-500 font-mono text-[11px] ml-auto">Grafik hazır</span>
            </div>

            <!-- Vis.js Kanvas Alanı -->
            <div id="medical-graph-container" class="w-full h-96 rounded-xl border border-slate-700/60 bg-slate-950/80 relative overflow-hidden">
                <div id="graph-loading-overlay" class="absolute inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center text-slate-400 text-xs gap-2 z-10 hidden">
                    <i class="fa-solid fa-spinner fa-spin text-purple-400"></i> Alt graf hesaplanıyor ve yerleştiriliyor...
                </div>
                <div id="graph-placeholder" class="absolute inset-0 flex flex-col items-center justify-center text-slate-500 text-xs">
                    <i class="fa-solid fa-share-nodes text-4xl mb-2 text-slate-600"></i>
                    <span>Tıbbi bir terim aratarak veya "Grafı Çıkar" butonuna basarak DiGraph ilişkilerini keşfedin.</span>
                </div>
            </div>
        </div>

        <!-- Alt Bölüm: Canlı Log Akışı & Aktif İşlem PID'leri -->
        <div class="glass p-6 rounded-2xl space-y-4">
            <!-- YENİ: Anlık Blok İlerleme & Dönüşüm Tablosu (Açılır Kapanır, Renkli Diff/Marker, Tümünü Göster) -->
            <div class="space-y-2">
                <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-2">
                    <div class="flex items-center gap-2">
                        <h3 class="text-sm font-bold text-slate-200 flex items-center gap-2">
                            <i class="fa-solid fa-wand-magic-sparkles text-amber-400"></i> Yapay Zeka Canlı Dönüşüm & Blok Akışı
                        </h3>
                        <span id="trans-count-badge" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">0 Dönüşüm</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-[11px] text-slate-400 hidden sm:inline">Neyi Neye Dönüştürdüğünün Canlı Karşılaştırması</span>
                        <button id="toggle-all-trans-btn" onclick="toggleAllTransforms()" class="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700 transition-colors flex items-center gap-1.5 shadow-sm">
                            <i class="fa-solid fa-expand text-indigo-400"></i>
                            <span id="toggle-all-trans-text">Tümünü Göster</span>
                        </button>
                    </div>
                </div>
                <div class="overflow-x-auto rounded-xl border border-slate-700/60 bg-slate-900/40">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-800/60 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-700/50">
                            <tr>
                                <th class="p-2.5 w-16">Saat</th>
                                <th class="p-2.5 w-36">Dosya & İşlem</th>
                                <th class="p-2.5 w-5/12 text-rose-300">
                                    <span class="inline-flex items-center gap-1"><i class="fa-solid fa-arrow-left"></i> Girdi Metni (Ham / Öncesi)</span>
                                </th>
                                <th class="p-2.5 w-5/12 text-emerald-300">
                                    <span class="inline-flex items-center gap-1"><i class="fa-solid fa-sparkles text-emerald-400"></i> Yapay Zeka Çıktısı (Değişiklik Vurgulu)</span>
                                </th>
                                <th class="p-2.5 text-right w-24">Ayrıntı</th>
                            </tr>
                        </thead>
                        <tbody id="blocks-table-body" class="divide-y divide-slate-800/60 font-mono text-[11px] text-slate-300">
                            <tr><td colspan="5" class="p-4 text-center text-slate-500 font-sans">Yapay zeka ilk blok dönüşümünü gerçekleştirdiğinde burada canlı görünecektir...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Konsol Log Çıktısı -->
            <div class="pt-2 border-t border-slate-700/50">
                <div class="flex justify-between items-center mb-2">
                    <h2 class="text-xs font-bold text-slate-300 flex items-center gap-2 uppercase tracking-wider">
                        <i class="fa-solid fa-terminal text-emerald-400"></i> Ham Terminal Log Akışı
                    </h2>
                    <span class="text-xs text-slate-400">pipeline.log</span>
                </div>
                <div id="logs-container" class="bg-black/60 rounded-xl p-4 font-mono text-xs text-slate-300 h-44 overflow-y-auto space-y-1 border border-slate-800">
                    <div class="text-slate-500">Loglar yükleniyor...</div>
                </div>
            </div>
        </div>
        </div> <!-- End of tab-overview -->

        <!-- YENİ SEKME: AŞAMA & FAZ YOL HARİTASI (SÜREÇ & TAHMİNLER) -->
        <div id="tab-stages" class="tab-content hidden space-y-6">
            <!-- Genel İlerleme Özeti & Tahmini Süre Banner -->
            <div class="glass p-6 rounded-2xl border-l-4 border-cyan-500 space-y-4">
                <div class="flex flex-col md:flex-row justify-between md:items-center gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">Otonom Boru Hattı Durumu</span>
                            <span class="text-xs text-slate-400 font-mono">5 Aşamalı Tıp Pipeline'ı</span>
                        </div>
                        <h2 class="text-xl font-bold text-white mt-1">Uçtan Uca Boru Hattı ve Aşama Analitiği</h2>
                        <p class="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
                            Sistem her aşamayı sıralı ve bağımlı olarak yürütür. Biten aşamalar yeşil ile işaretlenir, aktif aşama canlı GPU/VRAM ile işlenir ve sıradaki aşama otomatik tetiklenir.
                        </p>
                    </div>
                    <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-center min-w-[200px] shadow-inner">
                        <div class="text-[11px] uppercase font-bold text-slate-400">Genel Tamamlanma &amp; Kalan Süre</div>
                        <div class="text-2xl font-extrabold text-cyan-400 mt-1" id="stages-overall-eta">Hesaplanıyor...</div>
                        <div class="text-[10px] text-slate-400 mt-1" id="stages-overall-sub">Aşama 3 soru eşleştirmesi devam ediyor</div>
                    </div>
                </div>
            </div>

            <!-- 5 Aşama Kartları (Sıralı İlerleme Akışı) -->
            <div class="space-y-4" id="stages-cards-container">
                <!-- JS ile dinamik olarak stages_progress üzerinden doldurulur -->
            </div>

            <!-- Boru Hattı Toplam Dosya & İşlem Matrisi -->
            <div class="glass p-6 rounded-2xl space-y-4">
                <h3 class="text-sm font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-layer-group text-indigo-400"></i> Boru Hattı Toplam Dosya &amp; İşlem Matrisi
                </h3>
                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 text-center font-mono">
                    <div class="p-3 rounded-xl bg-slate-900/50 border border-slate-800">
                        <div class="text-[10px] uppercase text-slate-400">1. Ham İndirilen</div>
                        <div class="text-lg font-bold text-slate-200 mt-1" id="m-dl">0</div>
                        <div class="text-[9px] text-slate-500">PDF / PPTX</div>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/50 border border-slate-800">
                        <div class="text-[10px] uppercase text-slate-400">2. Ham Çıkarım (Temp1)</div>
                        <div class="text-lg font-bold text-emerald-400 mt-1" id="m-t1">0</div>
                        <div class="text-[9px] text-emerald-500">✓ %100 Bitti</div>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/50 border border-slate-800">
                        <div class="text-[10px] uppercase text-slate-400">3. Onarılan (Temp2)</div>
                        <div class="text-lg font-bold text-emerald-400 mt-1" id="m-t2">0</div>
                        <div class="text-[9px] text-emerald-500">✓ %100 Bitti</div>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/50 border border-cyan-900/40 bg-cyan-950/10">
                        <div class="text-[10px] uppercase text-cyan-400">4. RAG & Vektör (Temp3)</div>
                        <div class="text-lg font-bold text-cyan-300 mt-1" id="m-t3">0</div>
                        <div class="text-[9px] text-cyan-400">Aktif İşleniyor</div>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/50 border border-slate-800">
                        <div class="text-[10px] uppercase text-slate-400">5. Soru Bankası (DB)</div>
                        <div class="text-lg font-bold text-purple-300 mt-1" id="m-db-q">0</div>
                        <div class="text-[9px] text-slate-500">Doğrulanmış</div>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/50 border border-slate-800">
                        <div class="text-[10px] uppercase text-slate-400">6. Kanıt Parçaları</div>
                        <div class="text-lg font-bold text-amber-300 mt-1" id="m-db-c">0</div>
                        <div class="text-[9px] text-slate-500">RAG Chunkları</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SEKME 2: ELENEN, EKÂRTE EDİLEN & İNCELEME DOSYALARI -->
        <div id="tab-rejected" class="tab-content hidden space-y-6">
            <!-- Üst İstatistik Kartları -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="glass p-5 rounded-2xl border-l-4 border-rose-500">
                    <div class="flex justify-between items-center text-slate-400 mb-1">
                        <span class="text-xs uppercase font-semibold">Toplam Ayıklanan Dosya</span>
                        <i class="fa-solid fa-filter-circle-xmark text-rose-400"></i>
                    </div>
                    <div class="text-3xl font-extrabold text-white" id="rej-stat-total">0</div>
                    <div class="text-xs text-slate-400 mt-1">İşlem kalitesini korumak için elendi</div>
                </div>

                <div class="glass p-5 rounded-2xl border-l-4 border-amber-500">
                    <div class="flex justify-between items-center text-slate-400 mb-1">
                        <span class="text-xs uppercase font-semibold">Düşük Kalite / OCR Uyarısı</span>
                        <i class="fa-solid fa-triangle-exclamation text-amber-400"></i>
                    </div>
                    <div class="text-3xl font-extrabold text-white" id="rej-stat-lowq">0</div>
                    <div class="text-xs text-slate-400 mt-1">Kalite skoru %65'in altında</div>
                </div>

                <div class="glass p-5 rounded-2xl border-l-4 border-slate-500">
                    <div class="flex justify-between items-center text-slate-400 mb-1">
                        <span class="text-xs uppercase font-semibold">Yetersiz / Boş İçerik</span>
                        <i class="fa-solid fa-file-excel text-slate-400"></i>
                    </div>
                    <div class="text-3xl font-extrabold text-white" id="rej-stat-empty">0</div>
                    <div class="text-xs text-slate-400 mt-1">&lt;80 karakter içeren slaytlar</div>
                </div>

                <div class="glass p-5 rounded-2xl border-l-4 border-purple-500">
                    <div class="flex justify-between items-center text-slate-400 mb-1">
                        <span class="text-xs uppercase font-semibold">İnceleme Bekleyen Soru</span>
                        <i class="fa-solid fa-user-doctor text-purple-400"></i>
                    </div>
                    <div class="text-3xl font-extrabold text-white" id="rej-stat-review">0</div>
                    <div class="text-xs text-slate-400 mt-1">DeepSeek-R1 Hakem Ajan kuyruğu</div>
                </div>
            </div>

            <!-- Tablo: Elenen Dosyalar ve Nedenleri -->
            <div class="glass p-6 rounded-2xl space-y-4">
                <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-3">
                    <div>
                        <h2 class="text-lg font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-list-check text-rose-400"></i>
                            Ekarte Edilen Dosyalar & İnceleme Kuyruğu Denetim Listesi
                        </h2>
                        <p class="text-xs text-slate-400 mt-0.5">Sistemin uydurma bilgi (hallucination) üretmesini engellemek için filtrelenen dosyalar ve kurtarma planları</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <input id="rej-search-input" onkeyup="filterRejectedTable()" type="text" placeholder="Dosya adı veya neden ara..." class="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-rose-500 w-64">
                        <select id="rej-category-filter" onchange="filterRejectedTable()" class="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-xs text-slate-300 focus:outline-none focus:border-rose-500">
                            <option value="all">Tüm Kategoriler</option>
                            <option value="low_quality">Düşük Kalite (%65 altı)</option>
                            <option value="empty_files">Yetersiz / Boş Slaytlar</option>
                            <option value="review_questions">İnceleme Soruları</option>
                        </select>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="bg-slate-800/80 text-slate-400 uppercase text-[10px] tracking-wider">
                            <tr>
                                <th class="p-3 rounded-l-lg">Dosya / Soru Başlığı</th>
                                <th class="p-3">Kategori & Tür</th>
                                <th class="p-3">Sayfa / Karakter</th>
                                <th class="p-3">Kalite Puanı</th>
                                <th class="p-3">Elenme / Ayrılma Sebebi</th>
                                <th class="p-3 rounded-r-lg">Gelişmiş AI Aksiyon Planı (Faz 3)</th>
                            </tr>
                        </thead>
                        <tbody id="rej-table-body" class="divide-y divide-slate-800/50">
                            <tr><td colspan="6" class="p-4 text-center text-slate-500">Veriler taranıyor...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Bilgilendirme Kutusu: Sıfır Halüsinasyon Prensibi -->
            <div class="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-start gap-4">
                <div class="p-3 bg-indigo-500/20 text-indigo-400 rounded-xl text-xl">
                    <i class="fa-solid fa-shield-halved"></i>
                </div>
                <div class="text-xs space-y-1">
                    <h3 class="font-bold text-white text-sm">MedSoru Zero-Hallucination & Kalite Güvencesi</h3>
                    <p class="text-slate-400 leading-relaxed">
                        Tıbbi eğitimde yanlış veya hayali bilginin yeri yoktur. Amfi slaytlarında doğrulanabilir kanıtı bulunmayan sorular (<code class="text-cyan-300">support_ratio &lt; 0.65</code>) veya kalitesiz taranmış boş sayfalar hiçbir koşulda doğrudan veritabanına aktarılmaz. Bu dosyalar Faz 3'te <strong>Qwen3-VL 2x2 dilimleme (image tiling)</strong> ve <strong>DeepSeek-R1 Hakem Ajan</strong> ile yeniden işlenir.
                    </p>
                </div>
            </div>
        </div>

        <!-- SEKME 3: AŞAMA 4 & 5 BİLGİ MERKEZİ (FAZ 2 & FAZ 3) -->
        <div id="tab-phase45" class="tab-content hidden space-y-6">
            <!-- Üst Mimari Başlık & Durum Bannerı -->
            <div class="p-6 rounded-2xl bg-gradient-to-r from-purple-950/40 via-indigo-950/30 to-slate-900/70 border border-purple-500/30 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30 uppercase tracking-wide">İleri Seviye AI Ekosistemi</span>
                        <span id="phase45-live-indicator" class="text-xs text-emerald-400 font-medium flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-400 pulse-dot"></span> Canlı İzleme (5s)</span>
                    </div>
                    <h2 class="text-xl font-extrabold text-white mt-2">Aşama 4 & 5: Doğrulanmış Tıp Veritabanı, GraphRAG ve Hibrit Arama</h2>
                    <p class="text-xs text-slate-300 mt-1">Yerel RTX 4060 GPU üzerinde sıfır maliyetle çalışan ilişkisel tıp bilgi grafı, MemGPT hafıza katmanı ve ReAct koruyucu bariyerleri.</p>
                </div>
                <div class="flex items-center gap-3 bg-black/40 px-4 py-3 rounded-xl border border-purple-500/20">
                    <div class="text-right">
                        <div class="text-[10px] text-slate-400 uppercase font-semibold">Orkestratör Durumu</div>
                        <div id="stage5-status-badge" class="text-sm font-bold text-purple-300">Hazır / Tetiklenmeyi Bekliyor</div>
                    </div>
                    <i class="fa-solid fa-microchip text-2xl text-purple-400"></i>
                </div>
            </div>

            <!-- 4 Ana Modül Kartı (Grid) -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Modül 1: Aşama 4 Doğrulanmış Veritabanı & Supabase -->
                <div class="glass p-6 rounded-2xl space-y-4 border-t-2 border-emerald-500">
                    <div class="flex justify-between items-start">
                        <div>
                            <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Aşama 4: Depolama & İndeksleme</span>
                            <h3 class="text-base font-bold text-white mt-1 flex items-center gap-2">
                                <i class="fa-solid fa-database text-emerald-400"></i> Doğrulanmış Tıp Veritabanı & Supabase
                            </h3>
                        </div>
                        <span id="p4-db-status" class="px-2 py-0.5 rounded text-xs font-semibold bg-slate-800 text-slate-400">Taranıyor</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        Yalnızca <code class="text-emerald-300">verified</code> ve <code class="text-emerald-300">fixed</code> statüsündeki, amfi ders slaytından kanıtı bulunan sorular <code class="text-slate-200">meds_database/</code> altına yazılır.
                    </p>
                    <div class="grid grid-cols-2 gap-2 text-xs">
                        <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                            <div class="text-slate-400 text-[10px]">Doğrulanmış Soru Grubu</div>
                            <div id="p4-db-qs" class="text-lg font-extrabold text-emerald-400">-</div>
                        </div>
                        <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                            <div class="text-slate-400 text-[10px]">Kanıtlı RAG Chunk</div>
                            <div id="p4-db-ch" class="text-lg font-extrabold text-cyan-400">-</div>
                        </div>
                        <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                            <div class="text-slate-400 text-[10px]">İndeks Standardı</div>
                            <div class="text-xs font-bold text-slate-200">IVFFlat &amp; HNSW (Cosine)</div>
                        </div>
                        <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                            <div class="text-slate-400 text-[10px]">Vektör Boyutu</div>
                            <div class="text-xs font-bold text-indigo-300">1024-d (BGE-M3 Yerel)</div>
                        </div>
                    </div>
                </div>

                <!-- Modül 2: GraphRAG Tıbbi Bilgi Grafı -->
                <div class="glass p-6 rounded-2xl space-y-4 border-t-2 border-indigo-500">
                    <div class="flex justify-between items-start">
                        <div>
                            <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">Aşama 5.1: GraphRAG</span>
                            <h3 class="text-base font-bold text-white mt-1 flex items-center gap-2">
                                <i class="fa-solid fa-circle-nodes text-indigo-400"></i> NetworkX DiGraph Bilgi Grafı
                            </h3>
                        </div>
                        <span id="p5-graph-status" class="px-2 py-0.5 rounded text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Aktif</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        Tıbbi terimler, hastalıklar, ilaçlar, semptomlar ve sınav soruları yönlü bir graf üzerinde birbirine bağlanır (<code class="text-indigo-300">Ego-Graph radius=2</code>).
                    </p>
                    <div class="grid grid-cols-2 gap-2 text-xs">
                        <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                            <div class="text-slate-400 text-[10px]">Graf Düğüm Sayısı</div>
                            <div id="p5-graph-nodes" class="text-lg font-extrabold text-indigo-400">-</div>
                        </div>
                        <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                            <div class="text-slate-400 text-[10px]">İlişki (Edge) Sayısı</div>
                            <div id="p5-graph-edges" class="text-lg font-extrabold text-purple-400">-</div>
                        </div>
                        <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800 col-span-2">
                            <div class="text-slate-400 text-[10px]">Varlık Türleri</div>
                            <div class="text-xs font-mono text-slate-300 flex flex-wrap gap-1.5 mt-1">
                                <span class="px-1.5 py-0.5 bg-blue-500/20 text-blue-300 rounded">Ders</span>
                                <span class="px-1.5 py-0.5 bg-indigo-500/20 text-indigo-300 rounded">Konu</span>
                                <span class="px-1.5 py-0.5 bg-rose-500/20 text-rose-300 rounded">Hastalik</span>
                                <span class="px-1.5 py-0.5 bg-emerald-500/20 text-emerald-300 rounded">Ilac</span>
                                <span class="px-1.5 py-0.5 bg-amber-500/20 text-amber-300 rounded">Belirti</span>
                                <span class="px-1.5 py-0.5 bg-cyan-500/20 text-cyan-300 rounded">Soru</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Modül 3: Hibrit Arama & RRF Reranking -->
                <div class="glass p-6 rounded-2xl space-y-4 border-t-2 border-cyan-500">
                    <div class="flex justify-between items-start">
                        <div>
                            <span class="text-[10px] font-bold uppercase tracking-wider text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20">Aşama 5.2: Hybrid Search</span>
                            <h3 class="text-base font-bold text-white mt-1 flex items-center gap-2">
                                <i class="fa-solid fa-magnifying-glass-chart text-cyan-400"></i> BM25 + Dense BGE-M3 (RRF)
                            </h3>
                        </div>
                        <span class="px-2 py-0.5 rounded text-xs font-semibold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">Hibrit Motor</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        Hem tam kelime tıbbi eşleşmesi (BM25) hem de anlamsal bağlam (Dense) Reciprocal Rank Fusion formülüyle birleştirilir:
                        <code class="block mt-1 p-1 bg-black/40 text-cyan-300 rounded text-center font-mono">RRF(d) = 1/(60 + rank_dense) + 1/(60 + rank_bm25)</code>
                    </p>
                    <div class="grid grid-cols-2 gap-2 text-xs">
                        <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                            <div class="text-slate-400 text-[10px]">BM25 İndeksli Terim</div>
                            <div id="p5-bm25-status" class="text-sm font-bold text-cyan-400">Hazırlandı (IDF Sözlük)</div>
                        </div>
                        <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                            <div class="text-slate-400 text-[10px]">Reranker Filtresi</div>
                            <div class="text-sm font-bold text-amber-300">Top-20 -&gt; Top-5 (Cross-Attn)</div>
                        </div>
                    </div>
                </div>

                <!-- Modül 4: MemGPT Hiyerarşik Bellek & ReAct Guardrails -->
                <div class="glass p-6 rounded-2xl space-y-4 border-t-2 border-amber-500">
                    <div class="flex justify-between items-start">
                        <div>
                            <span class="text-[10px] font-bold uppercase tracking-wider text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">Aşama 5.3 &amp; 5.4: Agentic AI</span>
                            <h3 class="text-base font-bold text-white mt-1 flex items-center gap-2">
                                <i class="fa-solid fa-user-astronaut text-amber-400"></i> MemGPT OS &amp; ReAct Guardrails
                            </h3>
                        </div>
                        <span class="px-2 py-0.5 rounded text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30">Devrede</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        Öğrencinin dönem, hedef puan ve zayıf komiteleri Core Memory'de saklanır. ReAct ajanı ise ders notunda doğrudan kanıtı olmayan sorulara cevap vermez (Zero-Hallucination).
                    </p>
                    <div class="grid grid-cols-2 gap-2 text-xs">
                        <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                            <div class="text-slate-400 text-[10px]">Core / Recall Bellek</div>
                            <div class="text-sm font-bold text-amber-400">SQLite + JSONB (NVMe)</div>
                        </div>
                        <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                            <div class="text-slate-400 text-[10px]">Halüsinasyon Engeli</div>
                            <div class="text-sm font-bold text-emerald-400">Katı &lt;SLAYT_KANITLARI&gt; XML</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Faz 2 & Faz 3 Yol Haritası ve Görev Durumları -->
            <div class="glass p-6 rounded-2xl space-y-4">
                <h3 class="text-base font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-timeline text-indigo-400"></i> Faz 2 & Faz 3 Gelişmiş Mimari Yol Haritası
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                    <!-- Faz 2 -->
                    <div class="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-3">
                        <div class="flex justify-between items-center">
                            <span class="font-bold text-white text-sm flex items-center gap-2">
                                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Faz 2: RAG Vektörleme & Zenginleştirme
                            </span>
                            <span class="px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-semibold text-[10px]">YÜRÜTÜLÜYOR</span>
                        </div>
                        <ul class="space-y-1.5 text-slate-400 pl-4 list-disc">
                            <li><strong class="text-slate-200">Context Metadata Injection:</strong> 900 karakterlik chunk'lara statik <code class="text-cyan-300">[Komite|Ders|Başlık]</code> enjeksiyonu.</li>
                            <li><strong class="text-slate-200">Yerel BGE-M3 Embedding:</strong> Tüm chunk'lar RTX 4060 GPU üzerinde 1024-d matrislere dönüştürülüyor.</li>
                            <li><strong class="text-slate-200">Gemma 3 Akıl Yürütme:</strong> Çıkmış sorular amfi slaytlarıyla doğrulanıp eksik şıklar tamamlanıyor.</li>
                        </ul>
                    </div>

                    <!-- Faz 3 -->
                    <div class="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-3">
                        <div class="flex justify-between items-center">
                            <span class="font-bold text-white text-sm flex items-center gap-2">
                                <span class="w-2.5 h-2.5 rounded-full bg-purple-500 pulse-dot"></span> Faz 3: İleri Seviye Tıp Ajanları & Fine-Tuning
                            </span>
                            <span class="px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded font-semibold text-[10px]">SIRADA</span>
                        </div>
                        <ul class="space-y-1.5 text-slate-400 pl-4 list-disc">
                            <li><strong class="text-slate-200">Görüntü Dilimleme (2x2 Tiling):</strong> Yoğun slaytlarda Qwen-VL kayıplarını önleyen 4 kadranlı yüksek çözünürlüklü OCR.</li>
                            <li><strong class="text-slate-200">DeepSeek-R1 Hakem Ajan:</strong> Sınırda kalan (%65-%85) soruların otonom klinik muhakemesi.</li>
                            <li><strong class="text-slate-200">4-bit QLoRA Tıp Modeli:</strong> Doğrulanmış soru çiftleriyle RTX 4060 üzerinde yerel model adaptasyonu.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- SEKME 4: MASTER SÜREÇ & MOD YÖNETİCİSİ -->
        <div id="tab-master" class="tab-content hidden space-y-6">
            <!-- Mod Seçim Bannerı -->
            <div class="glass p-6 rounded-2xl border-l-4 border-amber-500 space-y-4">
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">Orkestrasyon & Güç Yönetimi</span>
                            <span id="master-active-mode-label" class="text-xs font-mono text-cyan-400">Aktif Mod: Normal</span>
                        </div>
                        <h2 class="text-xl font-bold text-white mt-1">Master Sistem & Süreç Denetim Masası</h2>
                        <p class="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
                            Arka plandaki tüm yapay zeka, arama ve senkronizasyon scriptlerini tek merkezden açıp kapatabilir, sistem gücünü ve çalışma takvimini anlık olarak yapılandırabilirsiniz.
                        </p>
                    </div>
                    <!-- 3 Mod Seçim Buton Grubu -->
                    <div class="flex flex-wrap items-center gap-2 bg-slate-900/80 p-2 rounded-xl border border-slate-800">
                        <button onclick="changeMasterMode('normal')" id="btn-mode-normal" class="px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-blue-600 text-white shadow-md">
                            <i class="fa-solid fa-gauge"></i> 1 - Normal (1-3GB GPU)
                        </button>
                        <button onclick="changeMasterMode('safe')" id="btn-mode-safe" class="px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-slate-800 text-slate-300 hover:bg-slate-700">
                            <i class="fa-solid fa-shield-halved text-emerald-400"></i> 2 - Güvenli (Zero GPU)
                        </button>
                        <button onclick="changeMasterMode('extreme')" id="btn-mode-extreme" class="px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-slate-800 text-slate-300 hover:bg-slate-700">
                            <i class="fa-solid fa-bolt text-rose-400"></i> 3 - Aşırı Güç (Max GPU)
                        </button>
                    </div>
                </div>
            </div>

            <!-- Hızlı Bağlantılar & Servis Portları -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <a href="http://localhost:3000" target="_blank" class="glass p-4 rounded-xl hover:border-emerald-500/50 transition flex items-center justify-between group">
                    <div class="flex items-center gap-3">
                        <div class="p-3 bg-emerald-500/20 text-emerald-400 rounded-lg group-hover:scale-110 transition">
                            <i class="fa-solid fa-graduation-cap text-xl"></i>
                        </div>
                        <div>
                            <div class="text-sm font-bold text-white">MedSoru Web Uygulaması</div>
                            <div class="text-xs text-slate-400 font-mono">http://localhost:3000</div>
                        </div>
                    </div>
                    <i class="fa-solid fa-arrow-up-right-from-square text-slate-500 group-hover:text-emerald-400 transition"></i>
                </a>

                <a href="http://localhost:8000" target="_blank" class="glass p-4 rounded-xl hover:border-cyan-500/50 transition flex items-center justify-between group">
                    <div class="flex items-center gap-3">
                        <div class="p-3 bg-cyan-500/20 text-cyan-400 rounded-lg group-hover:scale-110 transition">
                            <i class="fa-solid fa-bolt text-xl"></i>
                        </div>
                        <div>
                            <div class="text-sm font-bold text-white">Hibrit Arama & Supabase REST</div>
                            <div class="text-xs text-slate-400 font-mono">http://localhost:8000</div>
                        </div>
                    </div>
                    <i class="fa-solid fa-arrow-up-right-from-square text-slate-500 group-hover:text-cyan-400 transition"></i>
                </a>

                <a href="http://localhost:8085" target="_blank" class="glass p-4 rounded-xl hover:border-purple-500/50 transition flex items-center justify-between group">
                    <div class="flex items-center gap-3">
                        <div class="p-3 bg-purple-500/20 text-purple-400 rounded-lg group-hover:scale-110 transition">
                            <i class="fa-solid fa-gauge-high text-xl"></i>
                        </div>
                        <div>
                            <div class="text-sm font-bold text-white">Canlı Analiz Kokpiti (Bu Panel)</div>
                            <div class="text-xs text-slate-400 font-mono">http://localhost:8085</div>
                        </div>
                    </div>
                    <i class="fa-solid fa-arrow-up-right-from-square text-slate-500 group-hover:text-purple-400 transition"></i>
                </a>
            </div>

            <!-- Çalışma Takvimi & Saat Koşulları (Scheduler) -->
            <div class="glass p-5 rounded-2xl space-y-3">
                <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-3">
                    <div class="flex items-center gap-2">
                        <i class="fa-solid fa-business-time text-cyan-400"></i>
                        <h3 class="text-sm font-bold text-white">Otomasyon Çalışma Saatleri & Koşulları</h3>
                    </div>
                    <div class="flex items-center gap-3">
                        <label class="inline-flex items-center gap-2 cursor-pointer text-xs text-slate-300">
                            <input type="checkbox" id="sched-enabled" onchange="updateScheduleSettings()" class="rounded bg-slate-800 border-slate-700 text-indigo-500 focus:ring-0">
                            <span>Zamanlayıcı Aktif</span>
                        </label>
                        <div class="flex items-center gap-1 text-xs text-slate-400 font-mono">
                            <span>Başlangıç:</span>
                            <input type="number" id="sched-start" min="0" max="23" value="8" onchange="updateScheduleSettings()" class="w-14 bg-slate-900 border border-slate-700 rounded px-2 py-0.5 text-center text-white">
                            <span>Bitiş:</span>
                            <input type="number" id="sched-end" min="0" max="23" value="23" onchange="updateScheduleSettings()" class="w-14 bg-slate-900 border border-slate-700 rounded px-2 py-0.5 text-center text-white">
                        </div>
                        <span id="sched-status-badge" class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300">Çalışma Saati İçi</span>
                    </div>
                </div>
            </div>

            <!-- Faz Zinciri & Sıralı Otomasyon Orkestratörü -->
            <div class="glass p-6 rounded-2xl space-y-5 border border-indigo-500/30">
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-700/50 pb-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Otonom Döngü & Faz Orkestrasyonu</span>
                            <span id="cycle-turn-badge" class="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">Tur: -</span>
                            <span id="cycle-active-badge" class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">Aktif: -</span>
                            <button id="btn-stop-active-phase" onclick="stopActivePhase()" class="hidden px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-600 hover:bg-rose-500 text-white border border-rose-400 shadow-sm transition items-center gap-1 cursor-pointer">
                                <i class="fa-solid fa-stop text-[10px]"></i> Aktif Fazı Durdur
                            </button>
                        </div>
                        <h3 class="text-lg font-bold text-white mt-1.5 flex items-center gap-2">
                            <i class="fa-solid fa-arrows-spin text-indigo-400"></i> Faz Zinciri, İlerleme & Çalıştırma Sırası Yönetimi
                        </h3>
                        <p class="text-xs text-slate-400 mt-1 max-w-2xl">
                            Her fazın üzerine tıklayarak canlı konsol loglarını açabilir, tamamlanan/kalan çıktıları ve işlem hızlarını izleyebilir, fazların çalışma sırasını kuyruğa alıp manuel tetikleyebilirsiniz.
                        </p>
                    </div>
                    <div class="flex items-center gap-2 self-end md:self-auto">
                        <button onclick="updateMasterPhases()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700 flex items-center gap-1.5 transition">
                            <i class="fa-solid fa-rotate text-cyan-400"></i> Fazları Yenile
                        </button>
                    </div>
                </div>

                <!-- Özel Faz 7 v2 ve Çelişki Durum Bilgi Kartı -->
                <div id="p7v2-notice-box" class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
                    <div class="flex items-center gap-2.5 text-slate-300 font-mono">
                        <i class="fa-solid fa-microchip text-indigo-400"></i>
                        <span>Faz 7 v2 (elle, zincir dışı): işlenen <strong id="p7v2-processed" class="text-emerald-400 font-bold">0</strong> | anahtar çelişkisi <strong id="p7v2-celiski" class="text-rose-400 font-bold">0</strong></span>
                        <span class="text-slate-600">·</span>
                        <span class="text-slate-400">Faz 7 (eski): <span class="text-amber-400">karantinada</span></span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-[11px] text-slate-400">Canlı Sıra Kuyruğu:</span>
                        <div id="phase-queue-tags" class="flex flex-wrap items-center gap-1">
                            <span class="text-slate-500 font-mono text-[10px]">Kuyruk boş</span>
                        </div>
                        <button onclick="clearPhaseQueue()" id="btn-clear-queue" class="hidden px-2 py-0.5 rounded text-[10px] bg-rose-950/80 text-rose-300 border border-rose-800/60 hover:bg-rose-900 transition">
                            Kuyruğu Temizle
                        </button>
                    </div>
                </div>

                <!-- 20 Faz İnteraktif Tablo -->
                <div class="overflow-x-auto rounded-xl border border-slate-800">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-800/80 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-700/50 font-mono">
                            <tr>
                                <th class="p-3 w-72">Faz Adı & Görevi</th>
                                <th class="p-3 w-32">Durum</th>
                                <th class="p-3 w-24">Son Süre</th>
                                <th class="p-3 w-36">Çıktı / İlerleme</th>
                                <th class="p-3 w-36">Hız</th>
                                <th class="p-3 w-28">Son Bitiş</th>
                                <th class="p-3 text-right w-44">Sıralama & Eylemler</th>
                            </tr>
                        </thead>
                        <tbody id="master-phases-table-body" class="divide-y divide-slate-800/60 font-sans text-slate-300">
                            <tr><td colspan="7" class="p-4 text-center text-slate-500">Faz bilgileri yükleniyor...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Scriptler Yönetim Masası (Tablo & Kontroller) -->
            <div class="glass p-6 rounded-2xl space-y-4">
                <div class="flex justify-between items-center">
                    <div>
                        <h3 class="text-base font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-list-check text-indigo-400"></i> Yönetilen Arka Plan Scriptleri & Görev Envanteri
                        </h3>
                        <p class="text-xs text-slate-400 mt-0.5">Her scriptin amacını görüntüleyebilir, tek tıkla başlatıp durdurabilirsiniz.</p>
                    </div>
                    <button onclick="updateMasterStatus()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700 flex items-center gap-1.5">
                        <i class="fa-solid fa-rotate text-cyan-400"></i> Yenile
                    </button>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-800/60 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-700/50">
                            <tr>
                                <th class="p-3 w-56">Script & Servis</th>
                                <th class="p-3">Görevi ve Açıklaması</th>
                                <th class="p-3 w-28">Durum</th>
                                <th class="p-3 w-28">Çalışma Süresi</th>
                                <th class="p-3 text-right w-32">Kontrol</th>
                            </tr>
                        </thead>
                        <tbody id="master-scripts-table-body" class="divide-y divide-slate-800/60 font-sans text-slate-300">
                            <tr><td colspan="5" class="p-4 text-center text-slate-500">Script bilgileri alınıyor...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    <script>
        let currentTab = 'overview';
        let tabIntervalId = null;
        let showAllTransformsState = false;
        let expandedRowId = null;

        function toggleAllTransforms() {
            showAllTransformsState = !showAllTransformsState;
            const btnText = document.getElementById('toggle-all-trans-text');
            const btn = document.getElementById('toggle-all-trans-btn');
            if (btnText && btn) {
                if (showAllTransformsState) {
                    btnText.innerText = "Son 5 Satıra Daralt";
                    btn.className = "px-3 py-1 bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold text-white rounded-lg border border-indigo-500 transition-colors flex items-center gap-1.5 shadow-sm";
                } else {
                    btnText.innerText = "Tümünü Göster";
                    btn.className = "px-3 py-1 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700 transition-colors flex items-center gap-1.5 shadow-sm";
                }
            }
            updateDashboard();
        }

        function toggleRowDetail(idx) {
            expandedRowId = expandedRowId === idx ? null : idx;
            updateDashboard();
        }

        function highlightWordDiff(oldStr, newStr) {
            if (!oldStr && !newStr) return { oldHtml: '', newHtml: '' };
            if (!oldStr) return { oldHtml: '', newHtml: `<span class="bg-emerald-500/30 text-emerald-200 px-1 py-0.5 rounded border border-emerald-500/40">${escapeHtml(newStr)}</span>` };
            if (!newStr) return { oldHtml: `<span class="bg-rose-500/30 text-rose-200 line-through px-1 py-0.5 rounded border border-rose-500/40">${escapeHtml(oldStr)}</span>`, newHtml: '' };

            const oldWords = oldStr.split(/(\s+|[.,;!?()]+)/);
            const newWords = newStr.split(/(\s+|[.,;!?()]+)/);
            const oldSet = new Set(oldWords.map(w => w.trim().toLowerCase()).filter(w => w.length > 0));
            const newSet = new Set(newWords.map(w => w.trim().toLowerCase()).filter(w => w.length > 0));

            // Eski metinde silinen veya değiştirilen kelimeleri kırmızı/markerla göster
            const oldHtml = oldWords.map(w => {
                const clean = w.trim().toLowerCase();
                if (clean && !newSet.has(clean)) {
                    return `<span class="bg-rose-950/70 text-rose-300 line-through px-1 py-0.5 rounded border border-rose-800/50">${escapeHtml(w)}</span>`;
                }
                return escapeHtml(w);
            }).join('');

            // Yeni metinde eklenen veya onarılan kelimeleri yeşil/amber markerla göster
            const newHtml = newWords.map(w => {
                const clean = w.trim().toLowerCase();
                if (clean && !oldSet.has(clean)) {
                    return `<span class="bg-emerald-900/60 text-emerald-200 font-bold px-1.5 py-0.5 rounded border border-emerald-600/60 shadow-sm">${escapeHtml(w)}</span>`;
                }
                return escapeHtml(w);
            }).join('');

            return { oldHtml, newHtml };
        }

        function escapeHtml(str) {
            if (!str) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
        }

        function switchTab(tabId) {
            currentTab = tabId;
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            const target = document.getElementById('tab-' + tabId);
            if (target) target.classList.remove('hidden');

            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.className = "tab-btn px-4 py-2.5 rounded-xl font-medium text-sm flex items-center gap-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition";
            });
            const activeBtn = document.getElementById('nav-btn-' + tabId);
            if (activeBtn) {
                activeBtn.className = "tab-btn px-4 py-2.5 rounded-xl font-medium text-sm flex items-center gap-2 bg-indigo-600 text-white shadow-lg transition";
            }

            // Sayfa geçişinde anında veri çek
            if (tabId === 'overview') {
                updateDashboard();
            } else if (tabId === 'stages') {
                updateStagesPage();
            } else if (tabId === 'rejected') {
                updateRejectedPage();
            } else if (tabId === 'phase45') {
                updatePhase45Page();
            } else if (tabId === 'master') {
                updateMasterStatus();
                updateMasterPhases();
            }

            // Otomatik polling: Görüntülenen sayfa her 2-5 saniyede bir güncellensin
            if (tabIntervalId) clearInterval(tabIntervalId);
            const refreshTime = (tabId === 'overview' || tabId === 'stages' || tabId === 'master') ? 2000 : 5000;
            tabIntervalId = setInterval(() => {
                if (currentTab === 'overview') updateDashboard();
                else if (currentTab === 'stages') updateStagesPage();
                else if (currentTab === 'rejected') updateRejectedPage();
                else if (currentTab === 'phase45') updatePhase45Page();
                else if (currentTab === 'master') {
                    updateMasterStatus();
                    updateMasterPhases();
                }
            }, refreshTime);
        }

        async function updateDashboard() {
            try {
                const res = await fetch('/api/stats');
                const d = await res.json();

                // 1. Donanım Sayaçları
                document.getElementById('cpu-percent').innerText = '%' + d.system.cpu_percent;
                document.getElementById('cpu-cores').innerText = 'Çekirdek: ' + d.system.cpu_count;
                document.getElementById('cpu-bar').style.width = d.system.cpu_percent + '%';

                document.getElementById('ram-used').innerText = d.system.ram_used_gb + ' GB';
                document.getElementById('ram-total').innerText = '/ ' + d.system.ram_total_gb + ' GB';
                document.getElementById('ram-bar').style.width = d.system.ram_percent + '%';

                const vramUsed = d.system.gpu_vram_used || 0;
                const vramTotal = d.system.gpu_vram_total || 1;
                const vramPct = Math.round((vramUsed / vramTotal) * 100);
                document.getElementById('gpu-vram-used').innerText = vramUsed + ' MB';
                document.getElementById('gpu-vram-total').innerText = '/ ' + vramTotal + ' MB';
                document.getElementById('gpu-util').innerText = 'Yük: ' + d.system.gpu_util;
                document.getElementById('gpu-temp').innerText = d.system.gpu_temp;
                document.getElementById('gpu-bar').style.width = vramPct + '%';
                document.getElementById('gpu-model').innerText = d.system.gpu_name;

                document.getElementById('disk-used').innerText = d.system.disk_used_gb + ' GB';
                document.getElementById('disk-total').innerText = '/ ' + d.system.disk_total_gb + ' GB';
                document.getElementById('disk-bar').style.width = d.system.disk_percent + '%';
                document.getElementById('disk-read').innerText = d.system.disk_read || '0.0 MB/s';
                document.getElementById('disk-write').innerText = d.system.disk_write || '0.0 MB/s';

                // 2. Aktif Çalışan Model
                if (d.active_model && d.active_model.name) {
                    document.getElementById('active-model-badge').className = "px-2.5 py-1 text-xs font-semibold rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30";
                    document.getElementById('active-model-badge').innerText = "GPU / RAM'de Aktif";
                    document.getElementById('model-name').innerText = d.active_model.name;
                    document.getElementById('model-details').innerText = `Parametre: ${d.active_model.parameter_size} | Format: ${d.active_model.format} (${d.active_model.quantization_level})`;
                    document.getElementById('model-vram').innerText = `Boyut: ${d.active_model.size_gb} GB`;
                    document.getElementById('model-task').innerText = d.current_task;

                    const os = d.system.ollama_stats || {};
                    document.getElementById('model-cpu').innerText = os.cpu || '-%';
                    document.getElementById('model-ram').innerText = os.mem || '- MB';
                    document.getElementById('model-gpu-vram').innerText = d.system.gpu_util || '-%';
                    document.getElementById('model-blockio').innerText = os.blockio || '-';
                } else {
                    document.getElementById('active-model-badge').className = "px-2.5 py-1 text-xs font-semibold rounded-full bg-slate-700 text-slate-400";
                    document.getElementById('active-model-badge').innerText = "Boşta / Beklemede";
                    document.getElementById('model-name').innerText = "Model Bellekte Beklemede";
                    document.getElementById('model-details').innerText = "Gerektiğinde pipeline modeli otomatik çağırır.";
                    document.getElementById('model-vram').innerText = "";
                    document.getElementById('model-task').innerText = d.current_task || "Yeni dosya işleme sırası bekleniyor.";
                    document.getElementById('model-cpu').innerText = '0%';
                    document.getElementById('model-ram').innerText = '0 MB';
                    document.getElementById('model-gpu-vram').innerText = '0%';
                    document.getElementById('model-blockio').innerText = '-';
                }

                // 3. Modeller Tablosu
                const tbody = document.getElementById('models-table-body');
                tbody.innerHTML = '';
                const roleMap = {
                    'gemma3:4b': 'Aşama 2: Türkçe Onarım & Soru (A-E) Ayrıştırma',
                    'medgemma1.5:4b': 'Aşama 3: Tıbbi Terim Çıkarımı & Zenginleştirme',
                    'bge-m3': 'Vektörel Benzerlik & RAG Chunk Embedding',
                    'bge-m3:latest': 'Vektörel Benzerlik & RAG Chunk Embedding',
                    'qwen3-vl:8b': 'Aşama 1: Görsel Slayt OCR (Vision)',
                    'deepseek-r1:1.5b': 'Tıbbi Mantık & Doğrulama',
                    'deepseek-r1:8b': 'Detaylı Tıbbi Akıl Yürütme & Eşleştirme',
                    'qwen3:1.7b': 'Hızlı Metin Sınıflandırma'
                };

                d.models.forEach(m => {
                    const isRunning = d.active_model && d.active_model.name === m.name;
                    const role = roleMap[m.name] || 'Genel Tıbbi Görev';
                    const tr = document.createElement('tr');
                    tr.className = "hover:bg-slate-800/40 transition";
                    tr.innerHTML = `
                        <td class="p-2.5 font-bold text-white flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full ${isRunning ? 'bg-emerald-400 pulse-dot' : 'bg-slate-600'}"></span>
                            ${m.name}
                        </td>
                        <td class="p-2.5 text-slate-300">${m.details.parameter_size || '-'}</td>
                        <td class="p-2.5 text-slate-400">${(m.size / (1024*1024*1024)).toFixed(2)} GB</td>
                        <td class="p-2.5 text-indigo-300 font-medium">${role}</td>
                        <td class="p-2.5 text-right font-semibold ${isRunning ? 'text-emerald-400' : 'text-slate-500'}">
                            ${isRunning ? 'ÇALIŞIYOR' : 'HAZIR'}
                        </td>
                    `;
                    tbody.appendChild(tr);
                });

                // 4. Sayaçlar
                document.getElementById('cnt-dl').innerText = d.counts.downloads + ' dosya';
                document.getElementById('cnt-t1').innerText = d.counts.temp1 + ' dosya';
                document.getElementById('cnt-t2').innerText = d.counts.temp2 + ' dosya';
                document.getElementById('cnt-t3').innerText = d.counts.temp3 + ' dosya';
                const t3det = document.getElementById('cnt-t3-detail');
                if (t3det && d.counts.temp3_sources !== undefined) {
                    const srcDone = d.counts.temp3_sources;
                    const srcTot = d.counts.temp3_sources_total || 413;
                    const srcRem = Math.max(0, srcTot - srcDone);
                    const qDone = d.counts.temp3_questions_done || 0;
                    t3det.innerHTML = `Slayt: <strong>${srcDone}/${srcTot}</strong> (${srcRem} kaldı) | Vektör: <strong>${d.counts.temp3_vectors || 0}</strong> | Soru: <strong>${qDone > 0 ? qDone + ' işlendi' : 'Sırada bekliyor'}</strong>`;
                }
                document.getElementById('cnt-db').innerText = d.counts.db_questions + ' soru grubu (' + d.counts.db_chunks + ' chunk)';

                // Servis rozetleri
                const sp = document.getElementById('srv-pipeline');
                sp.innerText = d.services.pipeline.toUpperCase();
                const isPipeActive = ['active', 'activating'].includes(d.services.pipeline);
                sp.className = isPipeActive ? 'px-2 py-0.5 rounded font-semibold bg-emerald-500/20 text-emerald-400' : 'px-2 py-0.5 rounded font-semibold bg-red-500/20 text-red-400';

                const so = document.getElementById('srv-ollama');
                so.innerText = d.services.ollama.toUpperCase();
                so.className = d.services.ollama === 'running' ? 'px-2 py-0.5 rounded font-semibold bg-emerald-500/20 text-emerald-400' : 'px-2 py-0.5 rounded font-semibold bg-red-500/20 text-red-400';

                const sw = document.getElementById('srv-watchdog');
                if (sw) {
                    sw.innerText = (d.services.watchdog || 'inactive').toUpperCase();
                    sw.className = d.services.watchdog === 'active' ? 'px-2 py-0.5 rounded font-semibold bg-emerald-500/20 text-emerald-400' : 'px-2 py-0.5 rounded font-semibold bg-red-500/20 text-red-400';
                }

                // 5. Dosya Kuyruğu (İşlenen, Tamamlanan, Planlanan)
                const q = d.file_queue || {};
                const nDone = (q.completed || []).length;
                const nPend = (q.pending || []).length;
                const nProc = q.current ? 1 : 0;
                const nTotal = nDone + nPend + nProc;
                const pct = nTotal > 0 ? ((nDone / nTotal) * 100).toFixed(1) : 0;

                document.getElementById('q-done-cnt').innerText = nDone;
                document.getElementById('q-proc-cnt').innerText = nProc;
                document.getElementById('q-pend-cnt').innerText = nPend;
                document.getElementById('overall-progress-text').innerText = `%${pct} (${nDone} / ${nTotal} Dosya)`;
                document.getElementById('overall-progress-bar').style.width = pct + '%';
                document.getElementById('file-current-name').innerText = q.current || 'Şu an aktif işlenen dosya yok (beklemede).';

                // Tekil dosya ilerleme durumu (% ve çubuk)
                const fp = q.current_progress;
                if (fp && fp.file === q.current) {
                    const filePct = fp.percent || 0;
                    document.getElementById('file-current-percent').innerText = `%${filePct}`;
                    document.getElementById('file-current-bar').style.width = `${filePct}%`;
                    document.getElementById('file-current-desc').innerText = fp.desc || 'İşleniyor...';
                    document.getElementById('file-current-counter').innerText = `${fp.current}/${fp.total}`;
                } else if (q.current) {
                    document.getElementById('file-current-percent').innerText = `-%`;
                    document.getElementById('file-current-bar').style.width = `15%`;
                    document.getElementById('file-current-desc').innerText = 'Aşama 2 (Temizleme & Soru Çıkarımı)';
                    document.getElementById('file-current-counter').innerText = `-/-`;
                } else {
                    document.getElementById('file-current-percent').innerText = `%0`;
                    document.getElementById('file-current-bar').style.width = `0%`;
                    document.getElementById('file-current-desc').innerText = 'Beklemede';
                    document.getElementById('file-current-counter').innerText = `-/-`;
                }

                const compList = document.getElementById('files-completed-list');
                compList.innerHTML = '';
                if (!q.completed || q.completed.length === 0) {
                    compList.innerHTML = '<div class="text-slate-500 italic">Henüz tamamlanan dosya yok.</div>';
                } else {
                    q.completed.slice(-8).reverse().forEach(f => {
                        const item = document.createElement('div');
                        item.className = "flex items-center gap-1.5 text-slate-300 py-0.5 truncate";
                        item.innerHTML = `<span class="text-emerald-400 font-bold">✓</span> <span class="truncate" title="${f.name}">${f.name} <span class="text-[10px] text-slate-500">(${f.info || 'tamamlandı'})</span></span>`;
                        compList.appendChild(item);
                    });
                }

                const pendList = document.getElementById('files-pending-list');
                pendList.innerHTML = '';
                if (!q.pending || q.pending.length === 0) {
                    pendList.innerHTML = '<div class="text-slate-500 italic">Sırada bekleyen dosya yok.</div>';
                } else {
                    q.pending.slice(0, 10).forEach((f, idx) => {
                        const item = document.createElement('div');
                        item.className = "flex items-center gap-1.5 text-slate-300 py-0.5 truncate";
                        item.innerHTML = `<span class="text-amber-400 font-bold font-mono text-[10px]">${idx+1}.</span> <span class="truncate" title="${f}">${f}</span>`;
                        pendList.appendChild(item);
                    });
                    if (q.pending.length > 10) {
                        const more = document.createElement('div');
                        more.className = "text-[10px] text-slate-500 italic text-center pt-1";
                        more.innerText = `... ve ${q.pending.length - 10} dosya daha planlandı`;
                        pendList.appendChild(more);
                    }
                }

                // 6. Rolling Blok Tablosu (5 Satır Sınırı - FIFO)
                if (!window.recentBlocks) {
                    window.recentBlocks = [];
                }
                const fpData = q.current_progress;
                if (fpData && fpData.desc) {
                    const blockKey = `${fpData.file}_${fpData.current}_${fpData.total}_${fpData.desc}`;
                    const lastEntry = window.recentBlocks[window.recentBlocks.length - 1];
                    if (!lastEntry || lastEntry.key !== blockKey) {
                        const nowStr = new Date().toLocaleTimeString('tr-TR', { hour12: false });
                        window.recentBlocks.push({
                            key: blockKey,
                            time: nowStr,
                            file: fpData.file || '-',
                            desc: fpData.desc || 'İşleniyor',
                            progress: `${fpData.current || 0}/${fpData.total || 0} (%${fpData.percent || 0})`,
                            status: 'İşleniyor...'
                        });
                        // 5 satır sınırı: Eskisi kaybolur, yenisi eklenir (FIFO)
                        if (window.recentBlocks.length > 5) {
                            window.recentBlocks.shift();
                        }
                    }
                }

                // 6. Rolling Blok ve Canlı Dönüşüm Tablosu (Açılır Kapanır, Renkli Diff/Marker, Tümünü Göster)
                const transforms = d.transform_history || [];
                const bTable = document.getElementById('blocks-table-body');
                const transCountBadge = document.getElementById('trans-count-badge');
                if (transCountBadge) {
                    transCountBadge.innerText = `${transforms.length} Dönüşüm`;
                }

                if (bTable) {
                    if (transforms.length === 0) {
                        bTable.innerHTML = '<tr><td colspan="5" class="p-4 text-center text-slate-500 font-sans">Yapay zeka ilk metin/soru bloğunu işlediğinde öncesi ve sonrası canlı burada akacaktır...</td></tr>';
                    } else {
                        bTable.innerHTML = '';
                        // showAllTransformsState true ise tümünü, false ise son 5 tanesini göster (yeniden eskiye)
                        const listToShow = showAllTransformsState ? [...transforms].reverse() : transforms.slice(-5).reverse();

                        listToShow.forEach((t, idx) => {
                            const isLatest = idx === 0;
                            const timeStr = t.ts ? new Date(t.ts * 1000).toLocaleTimeString('tr-TR', { hour12: false }) : '-';
                            const isExpanded = expandedRowId === idx;
                            const diff = highlightWordDiff(t.input, t.output);

                            const tr = document.createElement('tr');
                            tr.className = isLatest ? "bg-amber-950/20 text-white cursor-pointer hover:bg-slate-800/60 transition" : "hover:bg-slate-800/40 text-slate-300 cursor-pointer transition";
                            tr.onclick = (e) => {
                                // buton tıklamalarını engelle
                                if (e.target.tagName !== 'BUTTON' && !e.target.closest('button')) {
                                    toggleRowDetail(idx);
                                }
                            };

                            tr.innerHTML = `
                                <td class="p-2.5 text-slate-400 whitespace-nowrap align-top">${timeStr}</td>
                                <td class="p-2.5 align-top">
                                    <div class="font-bold text-cyan-300 truncate max-w-[150px]" title="${escapeHtml(t.file)}">${escapeHtml(t.file)}</div>
                                    <div class="text-[10px] text-amber-400 font-semibold">${escapeHtml(t.step)}</div>
                                </td>
                                <td class="p-2.5 font-mono text-[11px] bg-rose-950/20 rounded border border-rose-900/30 p-2 align-top">
                                    <div class="flex justify-between items-center mb-1">
                                        <span class="text-rose-400 font-bold text-[9px] uppercase tracking-wider flex items-center gap-1">
                                            <i class="fa-solid fa-circle-minus text-rose-500"></i> Önceki / Ham Girdi
                                        </span>
                                        <span class="text-[9px] text-slate-500 font-mono">${(t.input || '').length} karakter</span>
                                    </div>
                                    <div class="${isExpanded ? '' : 'line-clamp-3'} leading-relaxed text-slate-300 selection:bg-rose-900">
                                        ${diff.oldHtml || escapeHtml(t.input)}
                                    </div>
                                </td>
                                <td class="p-2.5 font-mono text-[11px] bg-emerald-950/20 rounded border border-emerald-900/30 p-2 align-top">
                                    <div class="flex justify-between items-center mb-1">
                                        <span class="text-emerald-400 font-bold text-[9px] uppercase tracking-wider flex items-center gap-1">
                                            <i class="fa-solid fa-circle-plus text-emerald-400"></i> Yapay Zeka Çıktısı (Onarılan)
                                        </span>
                                        <span class="text-[9px] text-slate-500 font-mono">${(t.output || '').length} karakter</span>
                                    </div>
                                    <div class="${isExpanded ? '' : 'line-clamp-3'} leading-relaxed text-slate-200 selection:bg-emerald-900">
                                        ${diff.newHtml || escapeHtml(t.output)}
                                    </div>
                                </td>
                                <td class="p-2.5 text-right whitespace-nowrap align-top">
                                    <div class="flex flex-col items-end gap-1.5">
                                        <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${isLatest ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-emerald-500/20 text-emerald-400'}">
                                            ${isLatest ? 'YENİ' : '✓ İŞLENDİ'}
                                        </span>
                                        <button onclick="toggleRowDetail(${idx})" class="text-[10px] text-indigo-400 hover:text-indigo-300 font-sans flex items-center gap-1 mt-1">
                                            <i class="fa-solid ${isExpanded ? 'fa-chevron-up' : 'fa-chevron-down'}"></i>
                                            ${isExpanded ? 'Daralt' : 'Aç'}
                                        </button>
                                    </div>
                                </td>
                            `;
                            bTable.appendChild(tr);

                            // Eğer satır genişletilmişse tam diff detay panelini altına aç
                            if (isExpanded) {
                                const detailTr = document.createElement('tr');
                                detailTr.className = "bg-slate-900/90 border-b border-indigo-900/40 text-slate-200";
                                detailTr.innerHTML = `
                                    <td colspan="5" class="p-4 bg-slate-950/70 border-x border-slate-800 space-y-3">
                                        <div class="flex justify-between items-center text-xs border-b border-slate-800 pb-2">
                                            <div class="font-bold text-amber-300 flex items-center gap-2">
                                                <i class="fa-solid fa-code-compare text-indigo-400"></i> Ayrıntılı Karşılaştırma & Değişiklik İncelemesi: ${escapeHtml(t.file)}
                                            </div>
                                            <div class="flex items-center gap-3 text-[11px]">
                                                <span class="inline-flex items-center gap-1 text-rose-300"><span class="w-2.5 h-2.5 rounded-sm bg-rose-950 border border-rose-800 inline-block"></span> Silinen / Düzeltilen</span>
                                                <span class="inline-flex items-center gap-1 text-emerald-300"><span class="w-2.5 h-2.5 rounded-sm bg-emerald-900 border border-emerald-600 inline-block"></span> Eklenen / İyileştirilen</span>
                                            </div>
                                        </div>
                                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
                                            <div class="p-3 bg-slate-900/80 rounded-xl border border-rose-900/40 space-y-1">
                                                <div class="text-[10px] uppercase font-bold text-rose-400 flex justify-between">
                                                    <span>Önceki Ham Metin</span>
                                                    <span>${(t.input || '').length} Karakter</span>
                                                </div>
                                                <div class="whitespace-pre-wrap leading-relaxed text-slate-300 bg-black/40 p-2.5 rounded-lg border border-slate-800 max-h-60 overflow-y-auto">
                                                    ${diff.oldHtml || escapeHtml(t.input)}
                                                </div>
                                            </div>
                                            <div class="p-3 bg-slate-900/80 rounded-xl border border-emerald-900/40 space-y-1">
                                                <div class="text-[10px] uppercase font-bold text-emerald-400 flex justify-between">
                                                    <span>Yapay Zeka Zenginleştirilmiş / Düzeltilmiş Çıktı</span>
                                                    <span>${(t.output || '').length} Karakter</span>
                                                </div>
                                                <div class="whitespace-pre-wrap leading-relaxed text-slate-200 bg-black/40 p-2.5 rounded-lg border border-slate-800 max-h-60 overflow-y-auto">
                                                    ${diff.newHtml || escapeHtml(t.output)}
                                                </div>
                                            </div>
                                        </div>
                                    </td>
                                `;
                                bTable.appendChild(detailTr);
                            }
                        });
                    }
                }

                // 7. Loglar
                const logBox = document.getElementById('logs-container');
                logBox.innerHTML = '';
                d.logs.forEach(l => {
                    const row = document.createElement('div');
                    row.className = l.includes('ERROR') || l.includes('✗') ? 'text-red-400' : (l.includes('WARNING') ? 'text-amber-400' : (l.includes('✓') ? 'text-emerald-300' : 'text-slate-300'));
                    row.innerText = l;
                    logBox.appendChild(row);
                });

                // 8. Büyük Veri Metrik Sayaçları
                const sm = d.summary_metrics || {};
                if (sm.total_chars) {
                    document.getElementById('stat-total-chars').innerText = (sm.total_chars / 1000000).toFixed(1) + 'M';
                    document.getElementById('stat-total-qs').innerText = (sm.total_questions || 0).toLocaleString('tr-TR');
                    document.getElementById('stat-total-pages').innerText = (sm.total_pages || 0).toLocaleString('tr-TR');
                }

                // 9. Ayrıntılı Dosya Kataloğu Tablosu (535 Dosya)
                window.allFilesData = d.file_details || [];
                renderFilesTable();

            } catch (err) {
                console.error("Dashboard güncelleme hatası:", err);
            }
        }

        function renderFilesTable() {
            const tbody = document.getElementById('file-details-table-body');
            if (!tbody || !window.allFilesData) return;
            const qFilter = (document.getElementById('file-search-input')?.value || '').toLowerCase();
            const filtered = window.allFilesData.filter(f => f.name.toLowerCase().includes(qFilter) || f.type.toLowerCase().includes(qFilter));
            
            if (filtered.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" class="p-4 text-center text-slate-500">Aramaya uygun dosya bulunamadı.</td></tr>';
                return;
            }

            tbody.innerHTML = '';
            filtered.forEach(f => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-800/40 transition";
                const qualPct = Math.round(f.quality * 100);
                const qualColor = qualPct >= 85 ? 'text-emerald-400' : (qualPct >= 70 ? 'text-amber-400' : 'text-rose-400');
                const isPastQ = f.type === 'Çıkmış Soru';
                tr.innerHTML = `
                    <td class="p-3 font-semibold text-slate-200 truncate max-w-xs" title="${f.name}">
                        <div class="truncate">${f.name}</div>
                    </td>
                    <td class="p-3 whitespace-nowrap">
                        <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${isPastQ ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'}">
                            ${f.type}
                        </span>
                    </td>
                    <td class="p-3 font-mono text-slate-400 whitespace-nowrap">${(f.size_kb / 1024).toFixed(2)} MB</td>
                    <td class="p-3 font-mono text-slate-300 whitespace-nowrap">${f.pages} sf</td>
                    <td class="p-3 font-mono text-slate-300 whitespace-nowrap">${f.chars.toLocaleString('tr-TR')}</td>
                    <td class="p-3 font-mono ${f.questions > 0 ? 'text-cyan-300 font-bold' : 'text-slate-500'} whitespace-nowrap">${f.questions > 0 ? f.questions : '-'}</td>
                    <td class="p-3 font-mono ${qualColor} font-bold whitespace-nowrap">%${qualPct}</td>
                    <td class="p-3 text-right whitespace-nowrap">
                        <span class="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-800 text-slate-300 border border-slate-700">
                            ${f.next_stage}
                        </span>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function filterFilesTable() {
            renderFilesTable();
        }

        // 10. GraphRAG Vis.js İnteraktif Graf Çizici
        let networkInstance = null;
        async function fetchAndRenderGraph() {
            const term = (document.getElementById('graph-search-term')?.value || '').trim();
            const overlay = document.getElementById('graph-loading-overlay');
            const placeholder = document.getElementById('graph-placeholder');
            const container = document.getElementById('medical-graph-container');
            const statsText = document.getElementById('graph-stats-text');

            if (overlay) overlay.classList.remove('hidden');
            if (placeholder) placeholder.classList.add('hidden');

            try {
                const res = await fetch(`/api/graph?term=${encodeURIComponent(term)}`);
                const data = await res.json();

                if (!data.nodes || data.nodes.length === 0) {
                    if (statsText) statsText.innerText = 'Eşleşen düğüm bulunamadı.';
                    if (overlay) overlay.classList.add('hidden');
                    if (placeholder) {
                        placeholder.classList.remove('hidden');
                        placeholder.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-3xl mb-2 text-amber-500"></i><span>"${term}" için bilgi grafında düğüm bulunamadı.</span>`;
                    }
                    return;
                }

                if (statsText) {
                    statsText.innerText = `${data.nodes.length} düğüm, ${data.edges.length} ilişki`;
                }

                const colorMap = {
                    'Ders': '#3b82f6',
                    'Konu': '#6366f1',
                    'Hastalik': '#f43f5e',
                    'Ilac': '#10b981',
                    'Belirti': '#f59e0b',
                    'Soru': '#06b6d4',
                    'Kaynak': '#8b5cf6'
                };

                const visNodes = data.nodes.map(n => {
                    const nType = n.data?.type || 'Genel';
                    return {
                        id: n.id,
                        label: (n.data?.name || n.id).replace(/^(Ders:|Konu:|Hastalik:|Ilac:|Belirti:|Soru:|Kaynak:)/, ''),
                        title: `${nType}: ${n.data?.name || n.id}`,
                        color: {
                            background: colorMap[nType] || '#64748b',
                            border: '#ffffff',
                            highlight: { background: '#ffffff', border: colorMap[nType] || '#64748b' }
                        },
                        font: { color: '#ffffff', size: 12, face: 'system-ui' },
                        shape: nType === 'Soru' ? 'box' : (nType === 'Hastalik' ? 'diamond' : 'dot'),
                        size: nType === 'Ders' ? 24 : 16
                    };
                });

                const visEdges = data.edges.map(e => ({
                    from: e.source,
                    to: e.target,
                    label: e.relation || '',
                    arrows: 'to',
                    color: { color: '#475569', highlight: '#a855f7' },
                    font: { color: '#94a3b8', size: 9, align: 'middle' },
                    length: 140
                }));

                const graphData = {
                    nodes: new vis.DataSet(visNodes),
                    edges: new vis.DataSet(visEdges)
                };

                const options = {
                    nodes: { borderWidth: 1.5, shadow: true },
                    edges: { smooth: { type: 'continuous' } },
                    physics: {
                        stabilization: { iterations: 120 },
                        barnesHut: { gravitationalConstant: -3000, springLength: 120, springConstant: 0.04 }
                    },
                    interaction: { hover: true, tooltipDelay: 200, zoomView: true, dragView: true }
                };

                if (networkInstance) {
                    networkInstance.destroy();
                }
                networkInstance = new vis.Network(container, graphData, options);

            } catch (err) {
                console.error("Graf yükleme hatası:", err);
            } finally {
                if (overlay) overlay.classList.add('hidden');
            }
        }

        function resetGraphView() {
            if (networkInstance) {
                networkInstance.fit();
            }
        }

        // ==========================================
        // SEKME 2: ELENEN & İNCELEME DOSYALARI JS
        // ==========================================
        window.rejectedData = null;

        async function updateRejectedPage() {
            try {
                const res = await fetch('/api/rejected');
                const d = await res.json();
                window.rejectedData = d;

                const summary = d.summary || {};
                document.getElementById('rej-stat-total').innerText = summary.total_rejected || 0;
                document.getElementById('rej-stat-lowq').innerText = summary.low_quality_count || 0;
                document.getElementById('rej-stat-empty').innerText = summary.empty_files_count || 0;
                document.getElementById('rej-stat-review').innerText = summary.review_questions_count || 0;
                
                const navBadge = document.getElementById('nav-rejected-badge');
                if (navBadge) navBadge.innerText = summary.total_rejected || 0;

                renderRejectedTable();
            } catch (err) {
                console.error("Elenen dosyalar verisi çekilemedi:", err);
            }
        }

        function renderRejectedTable() {
            const tbody = document.getElementById('rej-table-body');
            if (!tbody || !window.rejectedData) return;

            const qFilter = (document.getElementById('rej-search-input')?.value || '').toLowerCase();
            const catFilter = document.getElementById('rej-category-filter')?.value || 'all';

            let items = window.rejectedData.items || [];
            if (catFilter !== 'all') {
                items = items.filter(it => it.category === catFilter);
            }
            if (qFilter) {
                items = items.filter(it => 
                    (it.name || '').toLowerCase().includes(qFilter) || 
                    (it.reason || '').toLowerCase().includes(qFilter) ||
                    (it.action || '').toLowerCase().includes(qFilter)
                );
            }

            if (items.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="p-4 text-center text-slate-500">Seçilen kriterlere uygun elenen dosya bulunamadı.</td></tr>';
                return;
            }

            tbody.innerHTML = '';
            items.forEach(it => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-800/40 transition";
                
                let qualText = '-';
                let qualClass = 'text-slate-500';
                if (it.quality !== undefined && it.quality !== null) {
                    const qp = Math.round(it.quality * 100);
                    qualText = `%${qp}`;
                    qualClass = qp >= 65 ? 'text-amber-400' : 'text-rose-400 font-bold';
                }

                let catBadge = '';
                if (it.category === 'low_quality') {
                    catBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30">Düşük Kalite</span>';
                } else if (it.category === 'empty_files') {
                    catBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700">Yetersiz İçerik</span>';
                } else {
                    catBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-purple-500/20 text-purple-300 border border-purple-500/30">İnceleme Sorusu</span>';
                }

                tr.innerHTML = `
                    <td class="p-3 font-semibold text-slate-200 truncate max-w-xs" title="${it.name}">
                        <div class="truncate">${it.name}</div>
                    </td>
                    <td class="p-3 whitespace-nowrap">
                        ${catBadge} <span class="text-[10px] text-slate-400 ml-1">(${it.type || '-'})</span>
                    </td>
                    <td class="p-3 font-mono text-slate-300 whitespace-nowrap">${it.pages || 0} sf / ${it.chars || 0} kr</td>
                    <td class="p-3 font-mono ${qualClass} whitespace-nowrap">${qualText}</td>
                    <td class="p-3 text-slate-300 max-w-sm">
                        <span class="text-rose-300 font-medium">${it.reason}</span>
                    </td>
                    <td class="p-3 text-slate-400 text-xs">
                        <span class="text-cyan-300 font-mono text-[11px]">${it.action}</span>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function filterRejectedTable() {
            renderRejectedTable();
        }

        // ==========================================
        // SEKME 3: AŞAMA 4 & 5 (FAZ 2 & 3) JS
        // ==========================================
        async function updatePhase45Page() {
            try {
                const [statsRes, graphRes] = await Promise.all([
                    fetch('/api/stats'),
                    fetch('/api/graph')
                ]);
                const stats = await statsRes.json();
                const graph = await graphRes.json();

                // 1. Veritabanı ve Chunk sayaçları
                const cnt = stats.counts || {};
                document.getElementById('p4-db-qs').innerText = (cnt.db_questions || 0) + ' Dosya';
                document.getElementById('p4-db-ch').innerText = (cnt.db_chunks || 0) + ' Chunk';
                const p4Status = document.getElementById('p4-db-status');
                if (cnt.db_questions > 0 || cnt.db_chunks > 0) {
                    p4Status.className = "px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";
                    p4Status.innerText = "Aktif Veri Mevcut";
                } else {
                    p4Status.className = "px-2 py-0.5 rounded text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30";
                    p4Status.innerText = "Aşama 3'ün Bitmesi Bekleniyor";
                }

                // 2. GraphRAG istatistikleri
                const gNodes = (graph.nodes || []).length;
                const gEdges = (graph.edges || []).length;
                document.getElementById('p5-graph-nodes').innerText = gNodes.toLocaleString('tr-TR');
                document.getElementById('p5-graph-edges').innerText = gEdges.toLocaleString('tr-TR');
                
                const s5Badge = document.getElementById('stage5-status-badge');
                if (cnt.temp3_sources >= 400) {
                    s5Badge.className = "text-sm font-bold text-emerald-400";
                    s5Badge.innerText = "Aşama 5 Otomasyonuna Hazır ✓";
                } else {
                    s5Badge.className = "text-sm font-bold text-purple-300";
                    s5Badge.innerText = "Aşama 3 Tamamlandığında Başlayacak";
                }

            } catch (err) {
                console.error("Aşama 4 & 5 telemetri verisi çekilemedi:", err);
            }
        }

        // ==========================================
        // YENİ SEKME: AŞAMA & FAZ YOL HARİTASI JS
        // ==========================================
        async function updateStagesPage() {
            try {
                const res = await fetch('/api/stats');
                const d = await res.json();

                // 1. Genel Matris Sayaçları
                const cnt = d.counts || {};
                document.getElementById('m-dl').innerText = (cnt.downloads || 0) + ' Dosya';
                document.getElementById('m-t1').innerText = (cnt.temp1 || 0) + ' Dosya';
                document.getElementById('m-t2').innerText = (cnt.temp2 || 0) + ' Dosya';
                document.getElementById('m-t3').innerText = (cnt.temp3_sources || 0) + ' Slayt / ' + (cnt.temp3_chunks || 0) + ' Chunk';
                document.getElementById('m-db-q').innerText = (cnt.db_questions || 0) + ' Grup';
                document.getElementById('m-db-c').innerText = (cnt.db_chunks || 0) + ' Chunk';

                // 2. Aşamalar İlerleme Kartları
                const stages = d.stages_progress || [];
                const container = document.getElementById('stages-cards-container');
                if (!container) return;

                container.innerHTML = '';
                let activeStageEta = "Hesaplanıyor...";

                stages.forEach((st, idx) => {
                    const isDone = st.status === 'completed';
                    const isRunning = st.status === 'running';
                    const isQueued = st.status === 'queued';

                    if (isRunning) {
                        activeStageEta = st.eta;
                    }

                    // Durum Stilleri
                    let cardBorder = "border-slate-800";
                    let statusBadge = `<span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-800 text-slate-400 border border-slate-700">Sırada Bekliyor</span>`;
                    let progressColor = "bg-slate-600";
                    let orderBadge = `<span class="w-7 h-7 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center font-bold text-xs border border-slate-700">${st.order}</span>`;

                    if (isDone) {
                        cardBorder = "border-emerald-900/50 bg-emerald-950/10";
                        statusBadge = `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center gap-1.5"><i class="fa-solid fa-check"></i> Tamamlandı</span>`;
                        progressColor = "bg-emerald-500";
                        orderBadge = `<span class="w-7 h-7 rounded-full bg-emerald-500 text-slate-950 flex items-center justify-center font-bold text-xs"><i class="fa-solid fa-check"></i></span>`;
                    } else if (isRunning) {
                        cardBorder = "border-cyan-500/60 bg-cyan-950/20 shadow-lg shadow-cyan-950/30";
                        statusBadge = `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-cyan-400 pulse-dot"></span> Şu An Çalışıyor</span>`;
                        progressColor = "bg-cyan-500";
                        orderBadge = `<span class="w-7 h-7 rounded-full bg-cyan-500 text-slate-950 flex items-center justify-center font-bold text-xs animate-pulse">${st.order}</span>`;
                    }

                    const card = document.createElement('div');
                    card.className = `glass p-5 rounded-2xl border ${cardBorder} transition-all space-y-4`;
                    card.innerHTML = `
                        <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-3">
                            <div class="flex items-center gap-3">
                                ${orderBadge}
                                <div>
                                    <div class="flex items-center gap-2">
                                        <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">${st.phase}</span>
                                        <h3 class="text-base font-bold text-white">${st.name}</h3>
                                    </div>
                                    <p class="text-xs text-slate-400 mt-0.5">${st.desc}</p>
                                </div>
                            </div>
                            <div class="flex items-center gap-3 self-end sm:self-auto">
                                ${statusBadge}
                            </div>
                        </div>

                        <!-- İlerleme Çubuğu -->
                        <div class="space-y-1.5">
                            <div class="flex justify-between text-xs font-mono">
                                <span class="text-slate-400">İşlem Durumu: <strong class="text-slate-200">${st.processed}</strong> / ${st.total}</span>
                                <span class="font-bold ${isDone ? 'text-emerald-400' : (isRunning ? 'text-cyan-400' : 'text-slate-500')}">%${st.progress_pct}</span>
                            </div>
                            <div class="w-full bg-slate-800/80 h-2.5 rounded-full overflow-hidden border border-slate-700/50">
                                <div class="${progressColor} h-full rounded-full transition-all duration-700" style="width: ${st.progress_pct}%"></div>
                            </div>
                        </div>

                        <!-- Detay Veri Tablosu / Kutuları -->
                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-2 border-t border-slate-800/60 text-xs font-mono">
                            <div class="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 flex justify-between items-center">
                                <span class="text-slate-400 font-sans text-[11px]">Üretilen / Çıktı:</span>
                                <span class="font-bold text-slate-200 truncate ml-2">${st.created_files}</span>
                            </div>
                            <div class="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 flex justify-between items-center">
                                <span class="text-slate-400 font-sans text-[11px]">Kalan / Bekleyen:</span>
                                <span class="font-semibold ${isDone ? 'text-slate-500' : 'text-amber-400'} truncate ml-2">${st.pending}</span>
                            </div>
                            <div class="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 flex justify-between items-center">
                                <span class="text-slate-400 font-sans text-[11px]">Tahmini Bitiş / Süre:</span>
                                <span class="font-bold ${isDone ? 'text-emerald-400' : (isRunning ? 'text-cyan-300' : 'text-slate-500')} ml-2">${st.eta}</span>
                            </div>
                        </div>

                        ${st.id === 14 ? `
                        <!-- Faz 14 Özel Manuel Çalıştırma Kontrol Paneli -->
                        <div class="pt-3 border-t border-slate-800/60 flex flex-wrap items-center justify-between gap-3">
                            <div class="flex items-center gap-2 text-xs text-slate-400">
                                <i class="fa-solid fa-bolt text-amber-400"></i>
                                <span>Manuel Tetikleme (Bulut veya Yerel GPU):</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <button onclick="runPhase14('cloud')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${st.is_running_cloud ? 'bg-amber-600 text-white animate-pulse' : 'bg-indigo-600 hover:bg-indigo-500 text-white'}">
                                    <i class="fa-solid fa-cloud"></i>
                                    <span>${st.is_running_cloud ? 'Bulut Çalışıyor...' : 'Bulut Başlat (Gemini)'}</span>
                                </button>
                                <button onclick="runPhase14('local')" class="px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${st.is_running_local ? 'bg-emerald-600 text-white animate-pulse' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}">
                                    <i class="fa-solid fa-microchip"></i>
                                    <span>${st.is_running_local ? 'Yerel GPU Çalışıyor...' : 'Yerel Başlat (RTX 4060)'}</span>
                                </button>
                                ${(st.is_running_cloud || st.is_running_local) ? `
                                <button onclick="stopPhase14()" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-rose-600/80 hover:bg-rose-600 text-white transition flex items-center gap-1.5">
                                    <i class="fa-solid fa-stop"></i>
                                    <span>Durdur</span>
                                </button>
                                ` : ''}
                                <a href="http://localhost:3000/test/cikmis" target="_blank" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-950/60 hover:bg-cyan-900/60 border border-cyan-800/50 text-cyan-300 transition flex items-center gap-1.5">
                                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                                    <span>/test/cikmis İncele</span>
                                </a>
                            </div>
                        </div>
                        ` : ''}
                    `;
                    container.appendChild(card);
                });

                document.getElementById('stages-overall-eta').innerText = activeStageEta;
            } catch (err) {
                console.error("Aşama analitiği verisi çekilemedi:", err);
            }
        }

        // ==========================================
        // SEKME 4: MASTER SÜREÇ & MOD YÖNETİCİSİ JS
        // ==========================================
        async function updateMasterStatus() {
            try {
                const res = await fetch('/api/master/status');
                const d = await res.json();

                // 1. Mod Göstergeleri
                const curMode = d.mode || 'normal';
                const modeLabel = document.getElementById('master-active-mode-label');
                const navBadge = document.getElementById('nav-master-mode-badge');
                if (modeLabel) modeLabel.innerText = "Aktif Mod: " + (curMode === 'normal' ? 'Normal (1-3GB GPU)' : (curMode === 'safe' ? 'Güvenli (Zero GPU)' : 'Aşırı Güç (Max GPU)'));
                if (navBadge) {
                    navBadge.innerText = curMode.toUpperCase();
                    navBadge.className = curMode === 'safe' ? "px-2 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30" : (curMode === 'extreme' ? "px-2 py-0.5 rounded-full text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30" : "px-2 py-0.5 rounded-full text-xs font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30");
                }

                // Buton stillerini güncelle
                ['normal', 'safe', 'extreme'].forEach(m => {
                    const btn = document.getElementById('btn-mode-' + m);
                    if (btn) {
                        if (m === curMode) {
                            btn.className = (m === 'normal' ? 'bg-blue-600' : (m === 'safe' ? 'bg-emerald-600' : 'bg-rose-600')) + " px-3.5 py-2 rounded-lg text-xs font-bold text-white shadow-md transition flex items-center gap-1.5";
                        } else {
                            btn.className = "bg-slate-800 text-slate-300 hover:bg-slate-700 px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5";
                        }
                    }
                });

                // 2. Zamanlayıcı Bilgileri
                const sched = d.schedule || {};
                const schedChk = document.getElementById('sched-enabled');
                const schedStart = document.getElementById('sched-start');
                const schedEnd = document.getElementById('sched-end');
                const schedBadge = document.getElementById('sched-status-badge');
                if (schedChk) schedChk.checked = sched.enabled || false;
                if (schedStart) schedStart.value = sched.start_hour ?? 8;
                if (schedEnd) schedEnd.value = sched.end_hour ?? 23;
                if (schedBadge) {
                    if (d.within_schedule) {
                        schedBadge.innerText = "Çalışma Saati İçi (Aktif)";
                        schedBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30";
                    } else {
                        schedBadge.innerText = "Zamanlama Dışı (Beklemede)";
                        schedBadge.className = "px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30";
                    }
                }

                // 3. Scriptler Tablosu
                const tbody = document.getElementById('master-scripts-table-body');
                const scripts = d.scripts || {};
                const sKeys = Object.keys(scripts);
                if (tbody && sKeys.length > 0) {
                    tbody.innerHTML = '';
                    sKeys.forEach(k => {
                        const s = scripts[k];
                        const isRun = s.running;
                        const tr = document.createElement('tr');
                        tr.className = "hover:bg-slate-800/40 transition";
                        tr.innerHTML = `
                            <td class="p-3 font-semibold text-white">
                                <div class="flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full ${isRun ? 'bg-emerald-400 pulse-dot' : 'bg-slate-600'}"></span>
                                    <span>${s.name}</span>
                                </div>
                            </td>
                            <td class="p-3 text-slate-300 text-xs">${s.desc}</td>
                            <td class="p-3">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold ${isRun ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-slate-800 text-slate-400 border border-slate-700'}">
                                    ${isRun ? '● ÇALIŞIYOR' : '○ DURDURULDU'}
                                </span>
                            </td>
                            <td class="p-3 font-mono text-xs ${isRun ? 'text-cyan-300 font-bold' : 'text-slate-500'}">
                                ${s.uptime_formatted}
                            </td>
                            <td class="p-3 text-right">
                                <button onclick="toggleScriptAction('${k}', ${isRun})" class="px-3 py-1 rounded text-xs font-bold transition shadow-sm ${isRun ? 'bg-rose-600 hover:bg-rose-500 text-white' : 'bg-emerald-600 hover:bg-emerald-500 text-white'}">
                                    ${isRun ? 'Durdur' : 'Başlat'}
                                </button>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            } catch (err) {
                console.error("Master durum verisi çekilemedi:", err);
            }
        }

        async function changeMasterMode(modeKey) {
            try {
                await fetch('/api/master/mode', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mode: modeKey })
                });
                updateMasterStatus();
            } catch (e) {
                alert('Mod değiştirilemedi: ' + e);
            }
        }

        async function runPhase14(mode) {
            const scriptKey = mode === 'cloud' ? 'phase14_cloud' : 'phase14_local';
            try {
                const res = await fetch('/api/master/action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'start', script: scriptKey })
                });
                const data = await res.json();
                if (data.success) {
                    alert(`✓ Faz 14 (${mode === 'cloud' ? 'Gemini Bulut' : 'Gemma 3 Yerel GPU'}) arka planda başlatıldı!`);
                } else {
                    alert(`Başlatılamadı: ${data.error || 'Bilinmeyen hata'}`);
                }
                updateStagesPage();
                updateMasterStatus();
            } catch (err) {
                alert('Faz 14 başlatma hatası: ' + err);
            }
        }

        async function stopPhase14() {
            try {
                await fetch('/api/master/action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'stop', script: 'phase14_cloud' })
                });
                await fetch('/api/master/action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'stop', script: 'phase14_local' })
                });
                alert('✓ Faz 14 süreçleri durduruldu.');
                updateStagesPage();
                updateMasterStatus();
            } catch (err) {
                alert('Durdurma hatası: ' + err);
            }
        }

        async function toggleScriptAction(scriptKey, currentlyRunning) {
            const act = currentlyRunning ? 'stop' : 'start';
            try {
                await fetch('/api/master/action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: act, script: scriptKey })
                });
                updateMasterStatus();
            } catch (e) {
                alert('İşlem başarısız: ' + e);
            }
        }


        async function updateScheduleSettings() {
            const en = document.getElementById('sched-enabled')?.checked || false;
            const sh = parseInt(document.getElementById('sched-start')?.value || 8);
            const eh = parseInt(document.getElementById('sched-end')?.value || 23);
            try {
                await fetch('/api/master/schedule', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ enabled: en, start_hour: sh, end_hour: eh })
                });
                updateMasterStatus();
            } catch (e) {
                console.error('Schedule hatası:', e);
            }
        }

        // ==========================================
        // FAZ ZİNCİRİ & ORKESTRASYON JS (MASTER PANEL)
        // ==========================================
        let activeExpandedPhase = null;
        let masterPhasesData = null;

        async function updateMasterPhases() {
            try {
                const res = await fetch('/api/master/phases');
                const d = await res.json();
                masterPhasesData = d;

                // 1. Tur ve Aktif Rozetleri
                const turnBadge = document.getElementById('cycle-turn-badge');
                const activeBadge = document.getElementById('cycle-active-badge');
                const stopActiveBtn = document.getElementById('btn-stop-active-phase');
                if (turnBadge) turnBadge.innerText = `Tur: ${d.tur ?? '-'}`;
                if (activeBadge) {
                    if (d.aktif) {
                        activeBadge.innerText = `● Aktif: ${d.aktif}`;
                        activeBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40 animate-pulse";
                        if (stopActiveBtn) {
                            stopActiveBtn.classList.remove('hidden');
                            stopActiveBtn.classList.add('inline-flex');
                            stopActiveBtn.setAttribute('title', `'${d.aktif}' sürecini durdur`);
                        }
                    } else {
                        activeBadge.innerText = `○ Boşta (Hazır)`;
                        activeBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-800 text-slate-400 border border-slate-700";
                        if (stopActiveBtn) {
                            stopActiveBtn.classList.remove('inline-flex');
                            stopActiveBtn.classList.add('hidden');
                        }
                    }
                }

                // 2. Faz 7 v2 İstatistiği
                const p7 = d.p7v2 || {};
                const elP7Proc = document.getElementById('p7v2-processed');
                const elP7Cel = document.getElementById('p7v2-celiski');
                if (elP7Proc) elP7Proc.innerText = p7.n || 0;
                if (elP7Cel) elP7Cel.innerText = p7.celiski || 0;

                // 3. Kuyruk Etiketleri
                const qContainer = document.getElementById('phase-queue-tags');
                const clearBtn = document.getElementById('btn-clear-queue');
                const qList = d.queue || [];
                if (qContainer) {
                    if (qList.length === 0) {
                        qContainer.innerHTML = '<span class="text-slate-500 font-mono text-[10px]">Kuyruk boş</span>';
                        if (clearBtn) clearBtn.classList.add('hidden');
                    } else {
                        if (clearBtn) clearBtn.classList.remove('hidden');
                        qContainer.innerHTML = qList.map((qk, idx) => `
                            <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-[11px] font-mono font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                                <span class="w-3.5 h-3.5 rounded-full bg-indigo-500 text-slate-950 flex items-center justify-center text-[9px] font-bold">${idx + 1}</span>
                                <span>${qk}</span>
                                <button onclick="event.stopPropagation(); removePhaseFromQueue('${qk}')" class="text-rose-400 hover:text-rose-200 ml-0.5" title="Kuyruktan Çıkar">×</button>
                            </span>
                        `).join('');
                    }
                }

                // 4. Fazlar Tablosunu Çiz
                renderMasterPhasesTable(d.phases || []);

                // Eğer bir faz açık ise logunu tazele
                if (activeExpandedPhase) {
                    loadPhaseLog(activeExpandedPhase, false);
                }
            } catch (err) {
                console.error("Faz verisi çekilemedi:", err);
            }
        }

        function renderMasterPhasesTable(phases) {
            const tbody = document.getElementById('master-phases-table-body');
            if (!tbody) return;

            tbody.innerHTML = '';
            phases.forEach(p => {
                const tr = document.createElement('tr');
                const isExpanded = activeExpandedPhase === p.key;
                tr.id = `phase-row-${p.key}`;
                tr.className = `cursor-pointer transition border-b border-slate-800/60 ${isExpanded ? 'bg-indigo-950/30' : 'hover:bg-slate-800/40'}`;
                tr.onclick = (e) => {
                    // Buton tıklamalarını ayıkla
                    if (e.target.closest('button')) return;
                    togglePhaseLog(p.key);
                };

                // Durum Rozetleri
                let badgeClass = "bg-slate-800 text-slate-400 border border-slate-700";
                if (p.status_code === 'running') {
                    badgeClass = "bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold animate-pulse";
                } else if (p.status_code === 'completed_this') {
                    badgeClass = "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold";
                } else if (p.status_code === 'completed_prev') {
                    badgeClass = "bg-blue-500/20 text-blue-300 border border-blue-500/30";
                } else if (p.status_code === 'error') {
                    badgeClass = "bg-rose-500/20 text-rose-300 border border-rose-500/40 font-bold";
                }

                // Kuyruk Sıra Göstergesi
                let queueBadge = '';
                if (p.in_queue) {
                    queueBadge = `<span class="ml-1.5 px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-indigo-500/30 text-indigo-300 border border-indigo-400/40">Sıra: #${p.queue_pos}</span>`;
                }

                tr.innerHTML = `
                    <td class="p-3">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-chevron-${isExpanded ? 'down' : 'right'} text-indigo-400 text-xs w-3 transition-transform"></i>
                            <div>
                                <div class="font-bold text-white flex items-center gap-1.5">
                                    <span>${p.name}</span>
                                    ${queueBadge}
                                </div>
                                <div class="text-[11px] text-slate-400 truncate max-w-sm" title="${p.desc}">${p.desc}</div>
                            </div>
                        </div>
                    </td>
                    <td class="p-3 whitespace-nowrap">
                        <span class="px-2.5 py-1 rounded-md text-xs inline-block ${badgeClass}">
                            ${p.status_tr}
                        </span>
                    </td>
                    <td class="p-3 font-mono text-xs whitespace-nowrap text-slate-300">
                        ${p.duration}
                    </td>
                    <td class="p-3 whitespace-nowrap font-mono text-xs">
                        <div class="flex items-center gap-1.5">
                            <span class="font-bold text-white">${p.output_count.toLocaleString('tr-TR')}</span>
                            <span class="text-slate-400 text-[10px]">${p.unit}</span>
                        </div>
                        <div class="w-24 bg-slate-800 h-1.5 rounded-full mt-1 overflow-hidden">
                            <div class="bg-indigo-500 h-full rounded-full" style="width: ${p.pct}%"></div>
                        </div>
                    </td>
                    <td class="p-3 font-mono text-xs whitespace-nowrap ${p.status_code === 'running' ? 'text-amber-300 font-bold' : 'text-slate-300'}">
                        ${p.speed}
                    </td>
                    <td class="p-3 font-mono text-[11px] whitespace-nowrap text-slate-400">
                        ${p.last_end}
                    </td>
                    <td class="p-3 text-right whitespace-nowrap space-x-1">
                        ${p.status_code === 'running' ? `
                            <button onclick="stopSpecificPhase('${p.key}')" class="px-2.5 py-1 rounded text-xs font-bold transition shadow-sm bg-rose-600 hover:bg-rose-500 text-white" title="Bu fazın sürecini durdur">
                                <i class="fa-solid fa-stop text-[10px]"></i> Durdur
                            </button>
                        ` : `
                            <button onclick="runMasterPhase('${p.key}')" class="px-2.5 py-1 rounded text-xs font-bold transition shadow-sm bg-indigo-600 hover:bg-indigo-500 text-white" title="Öncelikli olarak hemen çalıştır">
                                <i class="fa-solid fa-play text-[10px]"></i> Çalıştır
                            </button>
                        `}
                        ${p.in_queue ? `
                            <button onclick="removePhaseFromQueue('${p.key}')" class="px-2 py-1 rounded text-xs font-semibold bg-slate-800 text-rose-300 hover:bg-rose-950/60 border border-slate-700 transition" title="Kuyruktan Çıkar">
                                Kaldır
                            </button>
                        ` : `
                            <button onclick="enqueuePhase('${p.key}')" class="px-2 py-1 rounded text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700 transition" title="Kuyruğun sonuna ekle">
                                + Sıraya Al
                            </button>
                        `}
                    </td>
                `;
                tbody.appendChild(tr);

                // Eğer bu satır tıklandıysa altına log akordiyon panelini aç
                if (isExpanded) {
                    const logTr = document.createElement('tr');
                    logTr.id = `phase-log-drawer-${p.key}`;
                    logTr.className = "bg-slate-950/90 border-b border-indigo-900/40 text-slate-200";
                    logTr.innerHTML = `
                        <td colspan="7" class="p-4 bg-slate-950/80 border-x border-slate-800 space-y-3">
                            <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-2 border-b border-slate-800 pb-2">
                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 rounded-full ${p.status_code === 'running' ? 'bg-amber-400 pulse-dot' : 'bg-emerald-400'}"></span>
                                    <span class="font-bold text-white text-xs">${p.name} &mdash; Canlı Konsol Günlüğü & Ayrıntılar</span>
                                    <span class="text-slate-500 text-[11px] font-mono">(${p.script})</span>
                                </div>
                                <div class="flex items-center gap-2 text-xs">
                                    <button onclick="loadPhaseLog('${p.key}', true)" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] font-mono flex items-center gap-1 border border-slate-700 transition">
                                        <i class="fa-solid fa-arrows-rotate text-cyan-400"></i> Logu Tazele
                                    </button>
                                    <button onclick="togglePhaseLog('${p.key}')" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white text-[11px] transition">
                                        Kapat ✕
                                    </button>
                                </div>
                            </div>

                            <!-- Bilgi Metrik Şeridi -->
                            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono">
                                <div class="p-2 rounded bg-slate-900 border border-slate-800">
                                    <div class="text-[10px] text-slate-500">Mevcut Çıktı</div>
                                    <div class="font-bold text-emerald-400">${p.output_count.toLocaleString('tr-TR')} ${p.unit}</div>
                                </div>
                                <div class="p-2 rounded bg-slate-900 border border-slate-800">
                                    <div class="text-[10px] text-slate-500">Hedef / Toplam</div>
                                    <div class="font-bold text-white">${p.target.toLocaleString('tr-TR')} ${p.unit}</div>
                                </div>
                                <div class="p-2 rounded bg-slate-900 border border-slate-800">
                                    <div class="text-[10px] text-slate-500">Kalan Miktar</div>
                                    <div class="font-bold text-amber-400">${p.kalan.toLocaleString('tr-TR')} ${p.unit}</div>
                                </div>
                                <div class="p-2 rounded bg-slate-900 border border-slate-800">
                                    <div class="text-[10px] text-slate-500">İşlem Hızı</div>
                                    <div class="font-bold text-cyan-400">${p.speed}</div>
                                </div>
                            </div>

                            <!-- Konsol Terminal Penceresi -->
                            <div class="space-y-1">
                                <div class="flex justify-between items-center text-[10px] font-mono text-slate-400">
                                    <span>Son Log Satırları (Canlı Akış)</span>
                                    <span id="log-file-name-${p.key}" class="text-slate-500 truncate">phase_cycle_${p.key}.log</span>
                                </div>
                                <div id="log-content-${p.key}" class="font-mono text-xs leading-relaxed text-slate-300 bg-black/60 p-3 rounded-lg border border-slate-800 max-h-72 overflow-y-auto whitespace-pre-wrap select-text">
                                    <div class="text-slate-500 italic">Log yükleniyor...</div>
                                </div>
                            </div>
                        </td>
                    `;
                    tbody.appendChild(logTr);
                }
            });
        }

        async function togglePhaseLog(phaseKey) {
            if (activeExpandedPhase === phaseKey) {
                activeExpandedPhase = null;
            } else {
                activeExpandedPhase = phaseKey;
            }
            if (masterPhasesData) {
                renderMasterPhasesTable(masterPhasesData.phases || []);
            }
            if (activeExpandedPhase) {
                loadPhaseLog(activeExpandedPhase, true);
            }
        }

        async function loadPhaseLog(key, scrollToBottom) {
            const container = document.getElementById(`log-content-${key}`);
            const fileNameEl = document.getElementById(`log-file-name-${key}`);
            if (!container) return;

            try {
                const res = await fetch(`/api/master/phase_log?key=${encodeURIComponent(key)}`);
                const data = await res.json();
                if (fileNameEl && data.file) fileNameEl.innerText = data.file;

                const lines = data.lines || [];
                if (lines.length === 0) {
                    container.innerHTML = '<div class="text-slate-500 italic">Log içeriği boş.</div>';
                    return;
                }

                container.innerHTML = '';
                lines.forEach(l => {
                    const row = document.createElement('div');
                    if (l.includes('ERROR') || l.includes('✗') || l.includes('Traceback') || l.includes('HATA')) {
                        row.className = "text-rose-400";
                    } else if (l.includes('WARNING') || l.includes('bekleniyor') || l.includes('sürüyor')) {
                        row.className = "text-amber-300";
                    } else if (l.includes('✓') || l.includes('tamamlandı') || l.includes('100%')) {
                        row.className = "text-emerald-300";
                    } else {
                        row.className = "text-slate-300";
                    }
                    row.innerText = l;
                    container.appendChild(row);
                });

                if (scrollToBottom) {
                    container.scrollTop = container.scrollHeight;
                }
            } catch (err) {
                container.innerHTML = `<div class="text-rose-400">Log okunamadı: ${err}</div>`;
            }
        }

        async function runMasterPhase(key) {
            try {
                const res = await fetch('/api/master/phase_action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'run_now', key: key })
                });
                const data = await res.json();
                if (data.success) {
                    // Kullanıcıya hissettir
                    updateMasterPhases();
                } else {
                    alert('Çalıştırma hatası: ' + (data.error || 'Bilinmeyen hata'));
                }
            } catch (err) {
                alert('İstek başarısız: ' + err);
            }
        }

        async function enqueuePhase(key) {
            try {
                const res = await fetch('/api/master/phase_action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'enqueue', key: key })
                });
                const data = await res.json();
                if (data.success) {
                    updateMasterPhases();
                }
            } catch (err) {
                alert('Kuyruğa eklenemedi: ' + err);
            }
        }

        async function removePhaseFromQueue(key) {
            try {
                const res = await fetch('/api/master/phase_action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'remove', key: key })
                });
                const data = await res.json();
                if (data.success) {
                    updateMasterPhases();
                }
            } catch (err) {
                alert('Kuyruktan çıkarılamadı: ' + err);
            }
        }

        async function stopActivePhase() {
            if (!confirm('Şu an aktif çalışan faz sürecini sonlandırmak istiyor musunuz?')) return;
            try {
                const res = await fetch('/api/master/phase_action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'stop_active' })
                });
                const data = await res.json();
                if (data.success) {
                    alert('✓ ' + (data.message || 'Aktif faz durduruldu.'));
                    updateMasterPhases();
                } else {
                    alert('Durdurulamadı: ' + (data.error || 'Bilinmeyen hata'));
                }
            } catch (err) {
                alert('Durdurma isteği başarısız: ' + err);
            }
        }

        async function stopSpecificPhase(key) {
            if (!confirm(`'${key}' fazı sürecini durdurmak istediğinize emin misiniz?`)) return;
            try {
                const res = await fetch('/api/master/phase_action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'stop_phase', key: key })
                });
                const data = await res.json();
                if (data.success) {
                    alert('✓ ' + (data.message || 'Faz süreci durduruldu.'));
                    updateMasterPhases();
                } else {
                    alert('Durdurulamadı: ' + (data.error || 'Bilinmeyen hata'));
                }
            } catch (err) {
                alert('İstek başarısız: ' + err);
            }
        }

        // Başlangıç: İlk yüklemede ve 2 saniyede bir overview çek
        updateDashboard();
        updateRejectedPage(); // rozet sayısını almak için arka planda çağır
        updateMasterStatus(); // Master durumunu ilk anda al
        updateMasterPhases(); // Faz zincirini ilk anda al
        tabIntervalId = setInterval(() => {
            if (currentTab === 'overview') updateDashboard();
            else if (currentTab === 'stages') updateStagesPage();
            else if (currentTab === 'rejected') updateRejectedPage();
            else if (currentTab === 'phase45') updatePhase45Page();
            else if (currentTab === 'master') {
                updateMasterStatus();
                updateMasterPhases();
            }
        }, 2000);
    </script>
</body>
</html>
"""


def get_stats():
    # 1. Sistem Kaynakları (psutil)
    cpu_pct = psutil.cpu_percent(interval=None) if psutil else 0
    cpu_count = psutil.cpu_count() if psutil else 1
    ram = psutil.virtual_memory() if psutil else None
    disk = psutil.disk_usage("/") if psutil else None

    # SSD Canlı Okuma / Yazma Hızı
    disk_read_mbs = "0.0 MB/s"
    disk_write_mbs = "0.0 MB/s"
    try:
        global _last_disk_io, _last_disk_time
        if '_last_disk_io' not in globals():
            _last_disk_io = psutil.disk_io_counters() if psutil else None
            _last_disk_time = time.time()
        else:
            now = time.time()
            dt = max(0.1, now - _last_disk_time)
            cur_io = psutil.disk_io_counters() if psutil else None
            if cur_io and _last_disk_io:
                r_speed = (cur_io.read_bytes - _last_disk_io.read_bytes) / (1024 * 1024 * dt)
                w_speed = (cur_io.write_bytes - _last_disk_io.write_bytes) / (1024 * 1024 * dt)
                disk_read_mbs = f"{r_speed:.1f} MB/s"
                disk_write_mbs = f"{w_speed:.1f} MB/s"
            _last_disk_io = cur_io
            _last_disk_time = now
    except Exception:
        pass

    # GPU & VRAM
    gpu_util = "-%"
    gpu_temp = "-°C"
    gpu_name = "Nvidia GPU"
    gpu_vram_used = 0
    gpu_vram_total = 0
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=name,utilization.gpu,temperature.gpu,memory.used,memory.total",
                            "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=2)
        if r.returncode == 0 and r.stdout.strip():
            parts = [x.strip() for x in r.stdout.strip().split(",")]
            if len(parts) >= 5:
                gpu_name = parts[0]
                gpu_util = "%" + parts[1]
                gpu_temp = parts[2] + "°C"
                gpu_vram_used = int(parts[3])
                gpu_vram_total = int(parts[4])
    except Exception:
        pass

    # Docker meds-ollama Tüketimi (CPU %, RAM, BlockIO)
    ollama_docker_stats = {"cpu": "-%", "mem": "- MB", "blockio": "-"}
    try:
        r = subprocess.run(["sudo", "-n", "docker", "stats", "--no-stream", "meds-ollama",
                            "--format", "{{.CPUPerc}}|{{.MemUsage}}|{{.BlockIO}}"],
                           capture_output=True, text=True, timeout=2)
        if r.returncode == 0 and r.stdout.strip():
            c_cpu, c_mem, c_bio = [x.strip() for x in r.stdout.strip().split("|")]
            ollama_docker_stats = {
                "cpu": c_cpu,
                "mem": c_mem.split("/")[0].strip(),
                "blockio": c_bio
            }
    except Exception:
        pass

    # 2. Ollama Modelleri
    models = []
    active_model = None
    try:
        import urllib.request
        req = urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=3)
        data = json.loads(req.read().decode())
        models = data.get("models", [])

        req_ps = urllib.request.urlopen("http://127.0.0.1:11434/api/ps", timeout=3)
        data_ps = json.loads(req_ps.read().decode())
        running_models = data_ps.get("models", [])
        if running_models:
            m = running_models[0]
            active_model = {
                "name": m.get("name"),
                "size_gb": round(m.get("size", 0) / (1024**3), 2),
                "parameter_size": m.get("details", {}).get("parameter_size", "-"),
                "format": m.get("details", {}).get("format", "gguf"),
                "quantization_level": m.get("details", {}).get("quantization_level", "-")
            }
    except Exception:
        pass

    # 3. Dosya Sayaçları
    def c(p, ext=None):
        if not p.exists(): return 0
        if ext: return sum(1 for _ in p.rglob(f"*.{ext}"))
        return sum(1 for x in p.rglob("*") if x.is_file())

    td = PROJECT_ROOT / "meds_downloads"
    t1 = PROJECT_ROOT / "meds_temp" / "temp1"
    t2 = PROJECT_ROOT / "meds_temp" / "temp2"
    t3 = PROJECT_ROOT / "meds_temp" / "temp3"
    db = PROJECT_ROOT / "meds_database"
    phase65_dir = PROJECT_ROOT / "meds_database_v2" / "medical_thesaurus"
    phase65_state = {}
    try:
        phase65_state = json.loads((phase65_dir / "phase6_5_state.json").read_text())
    except Exception:
        pass
    phase65_terms = int(phase65_state.get("thesaurus_terms") or 0)
    phase65_anchors = int(phase65_state.get("total_anchors") or 0)
    phase65_fmt = lambda value: f"{value:,}".replace(",", ".")
    if not phase65_anchors:
        anchor_file = phase65_dir / "phase6_5_question_slide_anchors.jsonl"
        if anchor_file.exists():
            phase65_anchors = sum(1 for line in anchor_file.open(encoding="utf-8") if line.strip())
    if not phase65_terms:
        thesaurus_file = phase65_dir / "medical_thesaurus.json"
        if thesaurus_file.exists():
            try: phase65_terms = len(json.loads(thesaurus_file.read_text()))
            except Exception: pass

    # 4. Servis Durumları
    def srv(name):
        try:
            r = subprocess.run(["systemctl", "--user", "is-active", name], capture_output=True, text=True, timeout=2)
            return r.stdout.strip()
        except Exception:
            return "kapalı"

    def dock(name):
        try:
            r = subprocess.run(["sudo", "-n", "docker", "inspect", "-f", "{{.State.Status}}", name], capture_output=True, text=True, timeout=2)
            return r.stdout.strip() if r.returncode == 0 else "kapalı"
        except Exception:
            return "kapalı"

    # 5. Detaylı Temp3 Sayaçları ve İlerleme
    src_cnt = len(list((t3 / "sources").glob("*.json"))) if (t3 / "sources").exists() else 0
    chk_cnt = len(list((t3 / "chunks").glob("*.jsonl"))) if (t3 / "chunks").exists() else 0
    vec_cnt = len(list((t3 / "vectors").glob("*.npy"))) if (t3 / "vectors").exists() else 0
    q_file = t3 / "questions.jsonl"
    q_rq_file = t3 / "review_queue.jsonl"
    q_verified_cnt = sum(1 for _ in open(q_file, "r", encoding="utf-8")) if q_file.exists() else 0
    q_rq_cnt = sum(1 for _ in open(q_rq_file, "r", encoding="utf-8")) if q_rq_file.exists() else 0
    q_processed_cnt = q_verified_cnt + q_rq_cnt

    # temp3'te işlenmiş olan ders slayt yollarını tara
    t3_processed_paths = set()
    if (t3 / "sources").exists():
        for sf in (t3 / "sources").glob("*.json"):
            try:
                sd = json.loads(sf.read_text(encoding="utf-8"))
                p = sd.get("path")
                if p:
                    t3_processed_paths.add(p)
            except Exception:
                pass

    # 6. Çok Aşamalı Dosya Kuyruğu Analizi (Stage 3 ve Stage 2 Takibi)
    file_queue = {
        "completed": [],
        "current": None,
        "pending": [],
        "current_progress": None,
        "stage_info": "Aşama 3: RAG Vektörleme & Soru Eşleştirme"
    }
    try:
        state_file = PROJECT_ROOT / "meds_temp" / "state" / "pipeline_state.json"
        state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}
        current_progress = state.get("current_progress")

        # temp2 içerisindeki dosyalar
        t2_json_files = sorted(t2.rglob("*.json"))
        lecture_rels = []
        pastq_rels = []
        for f in t2_json_files:
            try:
                d_json = json.loads(f.read_text(encoding="utf-8"))
                rel_name = d_json.get("rel", "")
                if d_json.get("meta", {}).get("doc_type") == "past_question":
                    pastq_rels.append(rel_name)
                else:
                    lecture_rels.append(rel_name)
            except Exception:
                pass

        # Tamamlanan ders slaytları (temp3/sources'a girenler)
        for rel in lecture_rels:
            if rel in t3_processed_paths:
                file_queue["completed"].append({
                    "name": rel,
                    "info": "RAG ve BGE-M3 vektörleri hazır"
                })
            else:
                file_queue["pending"].append(rel)

        # Çıkmış sorular soru eşleştirmede kullanılacağı için kuyruğa ekle
        for qrel in pastq_rels:
            if q_processed_cnt > 0:
                file_queue["completed"].append({
                    "name": qrel,
                    "info": "sorular amfi slaytlarıyla eşleştirildi"
                })
            else:
                file_queue["pending"].append(qrel)

        if current_progress and current_progress.get("file"):
            file_queue["current"] = current_progress.get("file")
            file_queue["current_progress"] = current_progress
            if file_queue["current"] in file_queue["pending"]:
                file_queue["pending"].remove(file_queue["current"])
        elif file_queue["pending"]:
            file_queue["current"] = file_queue["pending"][0]
            file_queue["pending"] = file_queue["pending"][1:]
    except Exception:
        pass

    # 7. Son Loglar & Aktif İş
    log_file = PROJECT_ROOT / "meds_temp" / "logs" / "pipeline.log"
    logs = []
    current_task = "Beklemede veya planlanan görev yok."
    if log_file.exists():
        try:
            with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                lines = [x.strip() for x in f.readlines() if x.strip()]
                logs = lines[-12:]
                for ln in reversed(lines[-20:]):
                    if "temp3 kaynak ✓" in ln:
                        current_task = f"Aşama 3 (RAG/Vektör): {ln.split('temp3 kaynak ✓')[-1].strip()}"
                        break
                    elif "stage3" in ln:
                        current_task = f"Aşama 3 (Birleştirme & Soru Zenginleştirme) çalışıyor..."
                        break
                    elif "stage4" in ln:
                        current_task = f"Aşama 4 (Veritabanı Entegrasyonu) çalışıyor..."
                        break
                    elif "temp2 ✓" in ln:
                        current_task = f"Aşama 2: {ln.split('temp2 ✓')[-1].strip()}"
                        break
        except Exception:
            pass

    # 8. Tüm Dosyaların Ayrıntılı Analizi (Boyut, Sayfa, Karakter, Soru Sayısı, Kalite Skoru)
    file_details = []
    total_chars_all = 0
    total_pages_all = 0
    total_qs_all = 0
    t2_json_files = sorted(t2.rglob("*.json"))
    for f in t2_json_files:
        try:
            d_json = json.loads(f.read_text(encoding="utf-8"))
            rel_name = d_json.get("rel", "")
            pgs = d_json.get("pages", [])
            p_len = len(pgs)
            c_len = sum(len(p.get("text", "")) for p in pgs)
            q_len = len(d_json.get("questions", []))
            qual = float(d_json.get("quality", 0.0))
            d_type = d_json.get("meta", {}).get("doc_type", "lecture_slide")

            orig_size_kb = 0.0
            for ext in [".pdf", ".pptx", ".ppt", ".docx"]:
                cand = td / f"{rel_name}{ext}"
                if cand.exists():
                    orig_size_kb = round(cand.stat().st_size / 1024, 1)
                    break

            total_chars_all += c_len
            total_pages_all += p_len
            total_qs_all += q_len

            # Gerçek aşama tespiti
            if d_type == "past_question":
                if q_processed_cnt > 0:
                    next_stage = "Aşama 4 (Veritabanına Yazım)"
                else:
                    next_stage = "Aşama 3 (Soru Eşleştirme & Zenginleştirme)"
            else:
                if rel_name in t3_processed_paths:
                    next_stage = "Aşama 4 (Veritabanı Aktarımı)"
                else:
                    next_stage = "Aşama 3 (RAG/Vektör)"

            file_details.append({
                "name": rel_name,
                "type": "Çıkmış Soru" if d_type == "past_question" else "Ders Slaytı",
                "pages": p_len,
                "chars": c_len,
                "questions": q_len,
                "quality": qual,
                "size_kb": orig_size_kb,
            "next_stage": next_stage
            })
        except Exception:
            pass

    # 9. Tüm Boru Hattı Aşamaları & Fazları İlerleme ve Süre Tahmini Analizi
    total_dl = c(td)
    t1_done = c(t1, "json")
    t2_done = c(t2, "json")
    t3_src_done = src_cnt
    t3_src_total = 413
    t3_q_total = 7219  # Tekilleştirilmiş soru sayısı
    t3_q_done = q_processed_cnt
    db_done = c(db / "questions", "jsonl")

    # Süre ve Aşama Durumları
    # Aşama 1: Tamamlandı (%100)
    # Aşama 2: Tamamlandı (%100)
    # Aşama 3: Aktif Çalışıyor (Slaytlar %100, Sorular % ilerliyor)
    # Aşama 4: Sırada (Aşama 3 bitince otomatik başlar)
    # Aşama 5: Sırada (Aşama 4 bitince otomatik başlar)
    
    # Soru işleme tahmini: Saniyede ~1.8 soru
    questions_remaining = max(0, t3_q_total - t3_q_done)
    est_sec_q = int(questions_remaining / 1.8) if questions_remaining > 0 else 0
    est_min_q = round(est_sec_q / 60, 1)

    # GraphRAG ve Aşama 5 durumunu tespit et
    graph_file = t3 / "advanced_ai" / "medical_knowledge_graph.json"
    graph_nodes = 0
    graph_edges = 0
    if graph_file.exists():
        try:
            g_data = json.loads(graph_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Faz 14 Redaksiyon & İnceleme Metrikleri
    phase14_reviews_file = PROJECT_ROOT / "meds_database_v2" / "phase14_past_question_editor" / "reviews.jsonl"
    phase14_reviews_cnt = 0
    phase14_approved_cnt = 0
    phase14_pending_cnt = 0
    if phase14_reviews_file.exists():
        try:
            for l in phase14_reviews_file.read_text(encoding="utf-8").splitlines():
                if not l.strip():
                    continue
                phase14_reviews_cnt += 1
                try:
                    r_obj = json.loads(l)
                    st_val = r_obj.get("status")
                    if st_val == "approved":
                        phase14_approved_cnt += 1
                    elif st_val == "review_required":
                        phase14_pending_cnt += 1
                except Exception:
                    pass
        except Exception:
            pass

    phase14_total_q = 4926
    phase14_remaining = max(0, phase14_total_q - phase14_reviews_cnt)
    phase14_pct = round((phase14_reviews_cnt / max(1, phase14_total_q)) * 100, 1)

    phase14_is_cloud_running = bool(subprocess.run(["pgrep", "-f", "phase14_cloud_question_editor.py"], capture_output=True).stdout.strip())
    phase14_is_local_running = bool(subprocess.run(["pgrep", "-f", "phase14_past_question_editor.py"], capture_output=True).stdout.strip())

    stages_progress = [
        {
            "id": 1,
            "phase": "Faz 1",
            "name": "Faz 1 (Aşama 1): Ham Çıkarım & OCR",
            "desc": "PDF ve PPTX slaytlarının metin ve görsel katmanlarının okunması",
            "status": "completed",
            "status_tr": "Tamamlandı ✓",
            "progress_pct": 100,
            "processed": t1_done,
            "total": total_dl,
            "unit": "Dosya",
            "created_files": f"{t1_done} JSON / MD",
            "pending": 0,
            "eta": "Bitti ✓",
            "order": 1
        },
        {
            "id": 2,
            "phase": "Faz 2",
            "name": "Faz 2 (Aşama 2): Türkçe Onarım & Soru Ayrıştırma",
            "desc": "OCR gürültü temizliği, Türkçe karakter onarımı ve soru kalıplarının ayrıştırılması",
            "status": "completed",
            "status_tr": "Tamamlandı ✓",
            "progress_pct": 100,
            "processed": t2_done,
            "total": t1_done or 413,
            "unit": "Dosya",
            "created_files": f"{t2_done} Temiz Dosya",
            "pending": 0,
            "eta": "Bitti ✓",
            "order": 2
        },
        {
            "id": 3,
            "phase": "Faz 3",
            "name": "Faz 3 (Aşama 3): RAG Bölümleme & Soru Zenginleştirme",
            "desc": "Slaytların 900 karakterlik bloklara bölünmesi, BGE-M3 vektörleri ve 8.838 sorunun amfi slaytlarıyla eşleştirilmesi",
            "status": "completed" if q_processed_cnt >= 2000 else "running",
            "status_tr": "Tamamlandı ✓" if q_processed_cnt >= 2000 else "Şu An Çalışıyor",
            "progress_pct": 100 if q_processed_cnt >= 2000 else round((q_processed_cnt / 8838) * 100, 1),
            "processed": f"413 Slayt (%100) + {q_processed_cnt} Soru Onaylandı",
            "total": "413 Slayt / 8.838 Soru",
            "unit": "Birim",
            "created_files": f"{chk_cnt} Chunk Dosyası ({vec_cnt} Vektör Matrisi)",
            "pending": 0 if q_processed_cnt >= 2000 else f"{questions_remaining} Soru İnceleniyor",
            "eta": "Bitti ✓" if q_processed_cnt >= 2000 else "Tamamlanmak üzere",
            "order": 3
        },
        {
            "id": 4,
            "phase": "Faz 4",
            "name": "Faz 4 (Aşama 4): Doğrulama & Veritabanı Aktarımı",
            "desc": "Sadece doğrulanmış (verified/fixed) kanıtlı 2.194 sorunun meds_database ve PostgreSQL şemalarına aktarılması",
            "status": "completed" if db_done > 0 or q_processed_cnt >= 2000 else "running",
            "status_tr": "Tamamlandı ✓" if db_done > 0 or q_processed_cnt >= 2000 else "Aktarılıyor",
            "progress_pct": 100 if db_done > 0 or q_processed_cnt >= 2000 else 75,
            "processed": q_processed_cnt,
            "total": f"{q_processed_cnt} Onaylı Soru",
            "unit": "Kayıt",
            "created_files": f"2.194 Onaylı Soru, 24.657 Chunk",
            "pending": 0,
            "eta": "Bitti ✓",
            "order": 4
        },
        {
            "id": 5,
            "phase": "Faz 5",
            "name": "Faz 5 (Aşama 5): Çoklu AI Konsensüsü & Slayt İğne-Delik Tespiti",
            "desc": "Yerel RTX 4060 GPU ve Bulut AI (Groq/Gemini) eşzamanlı konsensüsü, pedagojik analiz, tıbbi varlık çıkarımı ve slayt chunk eşleştirme",
            "status": "completed" if c(PROJECT_ROOT / "meds_database_v2" / "questions", "jsonl") > 0 else "running",
            "status_tr": "Tamamlandı ✓" if c(PROJECT_ROOT / "meds_database_v2" / "questions", "jsonl") > 0 else "Konsensüs Analizinde",
            "progress_pct": 100 if c(PROJECT_ROOT / "meds_database_v2" / "questions", "jsonl") > 0 else 80,
            "processed": f"{c(PROJECT_ROOT / 'meds_database_v2' / 'questions', 'jsonl')} Soru Dosyası",
            "total": "Tüm Çıkmış Sorular & Slaytlar",
            "unit": "Konsensüs Havuzu",
            "created_files": "meds_database_v2/questions/*.jsonl + Karantina",
            "pending": 0,
            "eta": "Canlı Arka Plan",
            "order": 5
        },
        {
            "id": 6,
            "phase": "Faz 6",
            "name": "Faz 6 (Aşama 6): Derin Tıbbi Metadata & Hiper-Etiket Motoru",
            "desc": "Çoklu AI katmanı (RTX 4060 Gemma 3, OpenRouter, Groq, Gemini) ile 5-10 dakikada 5 soru, 2 saatte 1 ders notu temposuyla ICD-10 kodları, ayırıcı tanı ve hiper-arama etiketleri üretimi",
            "status": "running",
            "status_tr": "Otonom Çalışıyor (5-10 dk / 5 Soru & 2 Saatte 1 Ders)",
            "progress_pct": 88,
            "processed": "Dinamik Zamanlama Korumalı",
            "total": "5-10 dk / 5 Soru | 2 Saat / 1 Ders",
            "unit": "Metadata Havuzu",
            "created_files": "meds_database_v2/deep_metadata/*.jsonl",
            "pending": 0,
            "eta": "Sürekli Aktif",
            "order": 6
        },
        {
            "id": 65,
            "phase": "Faz 6.5",
            "name": "Faz 6.5: Tıbbi Sözlük (Thesaurus) & Co-occurrence Kanıt Motoru",
            "desc": f"Türkçe/Latince tıp ontolojisi, eşanlamlılar ve kavram kümeleri üzerinden {phase65_fmt(phase65_anchors)} soru-ders köprüsünün kurulması",
            "status": "completed",
            "status_tr": f"Tamamlandı ✓ ({phase65_fmt(phase65_anchors)} Köprü Kancalandı)",
            "progress_pct": 100,
            "processed": f"{phase65_fmt(phase65_terms)} Terim / Eşanlamlı · {phase65_fmt(phase65_anchors)} Soru-Slayt Köprüsü",
            "total": f"{phase65_fmt(phase65_anchors)} Eşleşen Kanıt",
            "unit": "Sözlük Köprüsü",
            "created_files": "medical_thesaurus.json + anchors.jsonl",
            "pending": 0,
            "eta": "Bitti ✓",
            "order": 6.5
        },
        {
            "id": 7,
            "phase": "Faz 7",
            "name": "Faz 7 (Aşama 7): 5 Adımlı Mikro-Ajans Soru Hikaye & Modelleme",
            "desc": "Kısıtlı parametreli yerel modeller için 5 adımlı mikro-ajan (Varlık Çıkarımı -> RAG Doğrulama -> Çeldirici Otopsisi -> Sebep-Sonuç -> Klinik Hikaye Sentezi) mimarisi ve 100 altın soru modellemesi",
            "status": "completed",
            "status_tr": "Tamamlandı ✓ (100 Altın Soru Modeli)",
            "progress_pct": 100,
            "processed": f"{c(PROJECT_ROOT / 'meds_database_v2' / 'phase7_stories', 'json')} Hikaye Üretildi",
            "total": "100 Altın Modelleme / Tüm Sorular",
            "unit": "Klinik Hikaye Havuzu",
            "created_files": "meds_database_v2/phase7_stories/*.json",
            "pending": 0,
            "eta": "Bitti ✓",
            "order": 7
        },
        {
            "id": 75,
            "phase": "Faz 7.5",
            "name": "Faz 7.5: Amfi Ders Slaytlarını Resmi Müfredatla Düzenleme",
            "desc": "KBÜ Tıp Fakültesi Dönem 3 (TIP320, TIP340, TIP350, TIP360) resmi müfredat hedefleriyle 410 amfi ders slaytının yapılandırılması ve çıkmış sorularla kancalanması",
            "status": "completed",
            "status_tr": "Tamamlandı ✓ (410 Slayt Müfredatla Eşlendi)",
            "progress_pct": 100,
            "processed": f"{c(PROJECT_ROOT / 'meds_database_v2' / 'slide_reconstructed', 'json')} Slayt Düzenlendi",
            "total": "410 Amfi Dersi",
            "unit": "Müfredat Slayt Kartı",
            "created_files": "meds_database_v2/slide_reconstructed/*.json",
            "pending": 0,
            "eta": "Bitti ✓",
            "order": 7.5
        },
        {
            "id": 14,
            "phase": "Faz 14",
            "name": "Faz 14: Çıkmış Soru Redaksiyonu & YZV Doğrulama",
            "desc": "Çıkmış soruların Gemini Flash (Bulut) ve Gemma 3 (Yerel GPU) ile incelenerek OCR/imla onarımı, YZV bloğu ve literatür referanslarının üretilmesi",
            "status": "running" if (phase14_is_cloud_running or phase14_is_local_running) else ("completed" if phase14_reviews_cnt > 0 else "queued"),
            "status_tr": "Şu An Çalışıyor (" + ("Bulut AI" if phase14_is_cloud_running else "Yerel GPU") + ")" if (phase14_is_cloud_running or phase14_is_local_running) else (f"Hazır ({phase14_reviews_cnt} Soru İncelendi)" if phase14_reviews_cnt > 0 else "Bekliyor"),
            "progress_pct": phase14_pct,
            "processed": f"{phase14_reviews_cnt} İnceleme ({phase14_approved_cnt} Onaylı, {phase14_pending_cnt} İnceleme Bekleyen)",
            "total": f"{phase14_total_q} Soru",
            "unit": "Soru",
            "created_files": f"reviews.jsonl ({phase14_reviews_cnt} Kayıt)",
            "pending": f"{phase14_remaining} Soru",
            "eta": "Canlı İncelemede" if (phase14_is_cloud_running or phase14_is_local_running) else f"{phase14_approved_cnt} onaylandı",
            "order": 14,
            "is_running_cloud": phase14_is_cloud_running,
            "is_running_local": phase14_is_local_running,
            "actions": ["run_phase14_cloud", "run_phase14_local", "stop_phase14"]
        }
    ]



    return {
        "system": {
            "cpu_percent": cpu_pct,
            "cpu_count": cpu_count,
            "ram_used_gb": round((ram.total - ram.available) / (1024**3), 1) if ram else 0,
            "ram_total_gb": round(ram.total / (1024**3), 1) if ram else 0,
            "ram_percent": ram.percent if ram else 0,
            "disk_used_gb": round(disk.used / (1024**3), 1) if disk else 0,
            "disk_total_gb": round(disk.total / (1024**3), 1) if disk else 0,
            "disk_percent": disk.percent if disk else 0,
            "disk_read": disk_read_mbs,
            "disk_write": disk_write_mbs,
            "gpu_name": gpu_name,
            "gpu_util": gpu_util,
            "gpu_temp": gpu_temp,
            "gpu_vram_used": gpu_vram_used,
            "gpu_vram_total": gpu_vram_total,
            "ollama_stats": ollama_docker_stats
        },
        "active_model": active_model,
        "models": models,
        "current_task": current_task,
        "counts": {
            "downloads": c(td),
            "temp1": c(t1, "json"),
            "temp2": c(t2, "json"),
            "temp3": c(t3, "json") + c(t3, "jsonl"),
            "temp3_sources": src_cnt,
            "temp3_sources_total": 413,
            "temp3_vectors": vec_cnt,
            "temp3_chunks": chk_cnt,
            "temp3_questions_done": q_processed_cnt,
            "db_questions": c(db / "questions", "jsonl"),
            "db_chunks": c(db / "chunks", "jsonl")
        },
        "summary_metrics": {
            "total_chars": total_chars_all,
            "total_pages": total_pages_all,
            "total_questions": total_qs_all,
            "total_files": len(file_details)
        },
        "file_details": file_details,
        "stages_progress": stages_progress,
        "services": {
            "pipeline": srv("meds-pipeline") if srv("meds-pipeline") != "inactive" else ("active" if subprocess.run(["pgrep", "-f", "pipeline_runner.py"], capture_output=True).stdout.strip() else "inactive"),
            "ollama": dock("meds-ollama"),
            "watchdog": "active" if subprocess.run(["pgrep", "-f", "watchdog.py"], capture_output=True).stdout.strip() else "inactive"
        },
        "file_queue": file_queue,
        "transform_history": state.get("transform_history", []),
        "logs": logs
    }

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path == "/api/stats":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(get_stats(), ensure_ascii=False).encode("utf-8"))
        elif self.path.startswith("/api/graph"):
            import urllib.parse
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            term = params.get("term", [""])[0]

            graph_file = Path("/home/indu/medsor/meds_temp/temp3/advanced_ai/medical_knowledge_graph.json")
            data = {"nodes": [], "edges": []}
            if graph_file.exists():
                try:
                    import networkx as nx
                    raw_data = json.loads(graph_file.read_text())
                    G = nx.node_link_graph(raw_data)
                    if term:
                        matched = [n for n in G.nodes if term.lower() in str(n).lower()]
                        if matched:
                            sub_nodes = set(matched)
                            for m in matched:
                                neighbors = nx.single_source_shortest_path_length(G.to_undirected(), m, cutoff=2)
                                sub_nodes.update(list(neighbors.keys())[:25])
                            sub = G.subgraph(sub_nodes)
                            data = {
                                "nodes": [{"id": str(n), "data": sub.nodes[n]} for n in sub.nodes],
                                "edges": [{"source": str(u), "target": str(v), "relation": sub.edges[u, v].get("relation", "")} for u, v in sub.edges]
                            }
                    else:
                        # İlk 40 düğümü örnek göster
                        sample_nodes = list(G.nodes)[:40]
                        sub = G.subgraph(sample_nodes)
                        data = {
                            "nodes": [{"id": str(n), "data": sub.nodes[n]} for n in sub.nodes],
                            "edges": [{"source": str(u), "target": str(v), "relation": sub.edges[u, v].get("relation", "")} for u, v in sub.edges]
                        }
                except Exception as e:
                    data = {"error": str(e), "nodes": [], "edges": []}
            else:
                # Canlı önizleme için örnek tıp grafı
                data = {
                    "nodes": [
                        {"id": "Ders:Enfeksiyon Hastalıkları", "data": {"type": "Ders", "name": "Enfeksiyon Hastalıkları"}},
                        {"id": "Konu:Cinsel Yolla Bulaşan Enfeksiyonlar", "data": {"type": "Konu", "name": "Cinsel Yolla Bulaşan Enfeksiyonlar"}},
                        {"id": "Hastalik:Sifilis (Frengi)", "data": {"type": "Hastalik", "name": "Sifilis (Frengi)"}},
                        {"id": "Belirti:Ağrısız Şankr (Ülser)", "data": {"type": "Belirti", "name": "Ağrısız Şankr (Ülser)"}},
                        {"id": "Ilac:Benzatin Penisilin G", "data": {"type": "Ilac", "name": "Benzatin Penisilin G"}},
                        {"id": "Soru:D3K1-2024-Q5", "data": {"type": "Soru", "name": "24y erkek, ağrısız şankr, VDRL (+)"}},
                        {"id": "Hastalik:Üriner Sistem Enfeksiyonları", "data": {"type": "Hastalik", "name": "Üriner Sistem Enfeksiyonları"}},
                        {"id": "Ilac:Siprofloksasin", "data": {"type": "Ilac", "name": "Siprofloksasin"}}
                    ],
                    "edges": [
                        {"source": "Ders:Enfeksiyon Hastalıkları", "target": "Konu:Cinsel Yolla Bulaşan Enfeksiyonlar", "relation": "İÇERİR"},
                        {"source": "Konu:Cinsel Yolla Bulaşan Enfeksiyonlar", "target": "Hastalik:Sifilis (Frengi)", "relation": "BAHSEDER"},
                        {"source": "Hastalik:Sifilis (Frengi)", "target": "Belirti:Ağrısız Şankr (Ülser)", "relation": "SEMPTOM_GÖSTERİR"},
                        {"source": "Ilac:Benzatin Penisilin G", "target": "Hastalik:Sifilis (Frengi)", "relation": "TEDAVİ_EDER"},
                        {"source": "Soru:D3K1-2024-Q5", "target": "Hastalik:Sifilis (Frengi)", "relation": "SORGULAR"},
                        {"source": "Konu:Cinsel Yolla Bulaşan Enfeksiyonlar", "target": "Hastalik:Üriner Sistem Enfeksiyonları", "relation": "İLİŞKİLİDİR"},
                        {"source": "Ilac:Siprofloksasin", "target": "Hastalik:Üriner Sistem Enfeksiyonları", "relation": "TEDAVİ_EDER"}
                    ]
                }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/rejected":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(get_rejected_data(), ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/master/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(get_master_status(), ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/master/phases":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(get_master_phases(), ensure_ascii=False).encode("utf-8"))
        elif self.path.startswith("/api/master/phase_log"):
            import urllib.parse
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            key = params.get("key", [""])[0]
            log_data = get_phase_log(key)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(log_data, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_error(404)

    def do_POST(self):
        # Değiştiren istekler yalnız bu makineden ve panelin kendi sayfasından (başka sitelerden CSRF engeli)
        origin = self.headers.get("Origin") or ""
        local_origins = (f"http://localhost:{PORT}", f"http://127.0.0.1:{PORT}", f"http://[::1]:{PORT}")
        if self.client_address[0] not in ("127.0.0.1", "::1") or (origin and origin not in local_origins):
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "yalniz localhost paneli"}')
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if self.path == "/api/master/mode":
            res = handle_master_mode(payload.get("mode", "normal"))
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/master/action":
            res = handle_master_action(payload.get("action", ""), payload.get("script", ""))
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/master/schedule":
            res = handle_master_schedule(payload)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/master/phase_action":
            action = payload.get("action", "")
            key = payload.get("key", "")
            queue_order = payload.get("queue", [])
            res = handle_master_phase_action(action, key, queue_order)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_error(404)


def get_rejected_data():
    t2 = PROJECT_ROOT / "meds_temp" / "temp2"
    t3 = PROJECT_ROOT / "meds_temp" / "temp3"

    items = []
    low_q_count = 0
    empty_count = 0
    review_count = 0

    if t2.exists():
        for f in sorted(t2.rglob("*.json")):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
                rel = d.get("rel") or f.stem
                q = float(d.get("quality", 1.0))
                pages = d.get("pages", [])
                total_chars = sum(len(p.get("text", "")) for p in pages)
                d_type = d.get("meta", {}).get("doc_type", "lecture_slide")

                if total_chars < 80:
                    empty_count += 1
                    items.append({
                        "name": rel,
                        "category": "empty_files",
                        "type": "Çıkmış Soru" if d_type == "past_question" else "Ders Slaytı",
                        "pages": len(pages),
                        "chars": total_chars,
                        "quality": round(q, 3),
                        "reason": f"Yetersiz / boş içerik ({total_chars} karakter, minimum 80 gerekli)",
                        "action": "Faz 3 Gelişmiş Qwen-VL OCR / Tiling ile yeniden okunacak"
                    })
                elif q < 0.65:
                    low_q_count += 1
                    items.append({
                        "name": rel,
                        "category": "low_quality",
                        "type": "Çıkmış Soru" if d_type == "past_question" else "Ders Slaytı",
                        "pages": len(pages),
                        "chars": total_chars,
                        "quality": round(q, 3),
                        "reason": f"Düşük OCR ve imla kalitesi (%{round(q * 100)} < %65 eşiği)",
                        "action": "Faz 3 Lancet kontrast adaptasyonu & LLM Post-OCR ile onarılacak"
                    })
            except Exception:
                pass

    # Review Queue soruları (support_ratio < 0.85 veya şık sayısı eksik olanlar)
    rq_file = t3 / "review_queue.jsonl"
    if rq_file.exists():
        try:
            for line in rq_file.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                qobj = json.loads(line)
                review_count += 1
                issues_str = "; ".join(qobj.get("issues", [])) or "Destek oranı sınırda"
                sup = qobj.get("support_ratio", 0.0)
                items.append({
                    "name": f"Soru {qobj.get('question_id', '')}: {qobj.get('stem', '')[:70]}...",
                    "category": "review_questions",
                    "type": "Soru İnceleme",
                    "pages": 1,
                    "chars": len(qobj.get("stem", "")),
                    "quality": round(sup, 3),
                    "reason": f"Slayt desteği sınırda ({sup:.2f}) | {issues_str}",
                    "action": "DeepSeek-R1 Hakem Ajan (Referee Agent) inceleme kuyruğunda"
                })
        except Exception:
            pass

    return {
        "summary": {
            "total_rejected": len(items),
            "low_quality_count": low_q_count,
            "empty_files_count": empty_count,
            "review_questions_count": review_count
        },
        "items": items
    }

def get_master_status():
    master_state_file = PROJECT_ROOT / "meds_temp" / "state" / "master_controller_state.json"
    if master_state_file.exists():
        try:
            return json.loads(master_state_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Eğer master state dosyası henüz yoksa doğrudan master_controller'dan derle
    try:
        sys.path.insert(0, str(MEDS_DIR / "scripts"))
        import master_controller
        ctrl = master_controller.MasterController()
        return ctrl.get_all_status()
    except Exception as e:
        return {"error": str(e), "mode": "normal", "scripts": {}, "telemetry": {}}

def handle_master_mode(mode_key: str):
    try:
        sys.path.insert(0, str(MEDS_DIR / "scripts"))
        import master_controller
        ctrl = master_controller.MasterController()
        ctrl.set_mode(mode_key)
        ctrl.write_state_file()
        return {"success": True, "mode": mode_key}
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_master_action(action: str, script_key: str):
    try:
        sys.path.insert(0, str(MEDS_DIR / "scripts"))
        import master_controller
        ctrl = master_controller.MasterController()
        if action == "start":
            res = ctrl.start_script(script_key)
        elif action == "stop":
            res = ctrl.stop_script(script_key)
        else:
            res = False
        ctrl.write_state_file()
        return {"success": res, "script": script_key, "action": action}
    except Exception as e:
        return {"success": False, "error": str(e)}

_MASTER_PHASES_CACHE = {"data": None, "ts": 0}

def get_master_phases():
    """Tüm fazların sıralama, telemetri, hız, son bitiş ve çıktı bilgilerini döner (3s TTL önbellekli)."""
    now = time.time()
    if _MASTER_PHASES_CACHE["data"] and (now - _MASTER_PHASES_CACHE["ts"] < 3.0):
        return _MASTER_PHASES_CACHE["data"]

    db_dir = PROJECT_ROOT / "meds_database"
    db_v2_dir = PROJECT_ROOT / "meds_database_v2"
    temp_dir = PROJECT_ROOT / "meds_temp"

    def _fast_lines(p):
        if not p.exists(): return 0
        try:
            with open(p, "rb") as f: return sum(1 for _ in f)
        except Exception: return 0

    def _safe_json(p):
        if not p.exists(): return {}
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception: return {}

    def _json_count(p, key=None):
        d = _safe_json(p)
        if key: d = d.get(key) or {}
        return len(d) if isinstance(d, (dict, list)) else 0

    def _fmt_dur(sec):
        if sec is None: return "-"
        sec = int(sec)
        return f"{sec}s" if sec < 60 else (f"{sec // 60}dk{sec % 60:02d}" if sec < 3600 else f"{sec // 3600}sa{(sec % 3600) // 60:02d}")

    # Faz tanımları ve sayaçları
    rows_def = [
        ("faz5", "Faz 5 · Çoklu AI konsensüs", "soru", "Çıkmış soruların yerel/bulut modellerle taranması ve doğrulanması", "scripts/advanced_ai/multi_ai_consensus_phase5.py",
         lambda: sum(_fast_lines(f) for f in (db_v2_dir / "questions").glob("*.jsonl")), 7219),
        ("faz6", "Faz 6 · Derin metadata", "soru", "Tıbbi hiper-metadata, ICD-10 kodları ve ayırıcı tanı entegrasyonu", "scripts/advanced_ai/deep_metadata_generator_phase6.py",
         lambda: _safe_json(db_v2_dir / "deep_metadata" / "phase6_metadata_state.json").get("total_questions_processed", 0), 7219),
        ("faz6_dogrulama", "Faz 6 doğrulama (CPU)", "soru", "Üretilen derin metadatanın CPU üzerinde sentaktik ve şema denetimi", "scripts/advanced_ai/validate_phase6_metadata.py",
         lambda: _fast_lines(db_v2_dir / "deep_metadata_validated" / "dogrulama.jsonl"), 7219),
        ("faz6_5", "Faz 6.5 · Sözlük & çapa", "çapa", "Tıbbi terimler ontolojisi ve soru-slayt kanıt çapalaması", "scripts/advanced_ai/thesaurus_anchor_phase6_5.py",
         lambda: _fast_lines(db_v2_dir / "medical_thesaurus" / "phase6_5_question_slide_anchors.jsonl"), 4926),
        ("faz7_5", "Faz 7.5 · Müfredat slaytları", "ders", "Ders slaytlarının resmi KBÜ Dönem 3 müfredat kartlarına dönüştürülmesi", "scripts/advanced_ai/reconstruct_slides_phase7_5.py",
         lambda: len(list((db_v2_dir / "slide_reconstructed").glob("*.json"))), 415),
        ("faz8", "Faz 8 · Kazanım ağacı", "soru", "Soru-kazanım-konu-ders-kurul hiyerarşik graf ağacı inşası", "scripts/advanced_ai/phase8_curriculum_graph.py",
         lambda: _fast_lines(temp_dir / "phase8" / "soru_kazanim.jsonl"), 7219),
        ("sozluk", "Kanıtlı sözlük", "terim", "Amfi ders slaytlarından kısaltma ve yazım varyantı sözlüğü", "scripts/advanced_ai/build_evidence_thesaurus.py",
         lambda: _json_count(db_v2_dir / "evidence_thesaurus" / "kanitli_sozluk.json"), 3000),
        ("faz9", "Faz 9 · Sözlüklü ağaç", "soru", "Kanıtlı sözlük destekli tıbbi müfredat ağacı", "scripts/advanced_ai/phase9_thesaurus_graph.py",
         lambda: _fast_lines(temp_dir / "phase9" / "soru_kazanim.jsonl"), 7219),
        ("faz10", "Faz 10 · Kavram kimlikleri", "kavram", "Wikidata ve UMLS kavram kimlik eşleştirmesi", "scripts/advanced_ai/phase10_concept_ids.py",
         lambda: _json_count(db_v2_dir / "concept_ids" / "kavramlar.json"), 2500),
        ("faz11", "Faz 11 · Soru–slayt eşleşmesi", "soru", "BM25, E5 vektör ve cross-encoder ile soru-slayt kanıt eşleme", "scripts/advanced_ai/phase11_question_slide.py",
         lambda: _fast_lines(temp_dir / "phase11" / "soru_slayt.jsonl"), 2839),
        ("ogren", "Öğren bağlantıları", "soru", "Öğrenci çalışma portalı için soru-slayt navigasyon bağları", "scripts/advanced_ai/learn_links.py",
         lambda: _json_count(db_dir / "derived" / "learn_links.json", "baglantilar"), 7219),
        ("yeniden_bolme", "Sınav çıktısını yeniden bölme", "adım", "Sınav dökümlerinin kurallı bloklara yeniden ayrıştırılması", "scripts/advanced_ai/resplit_exam_printout.py",
         lambda: 1 if (temp_dir / "logs" / "phase_cycle_yeniden_bolme.log").exists() else 0, 1),
        ("karantina", "Soru karantinası", "soru", "Hatalı şıklı veya desteklenmeyen soruların izole edilmesi ve onarımı", "scripts/advanced_ai/quarantine_questions.py",
         lambda: len((_safe_json(db_dir / "derived" / "quarantine" / "karantina.json").get("sorular") or {})), 1000),
        ("veritabani", "Veritabanı yüklemesi", "kayıt", "Doğrulanmış müfredat bağlarının güvenli veritabanına yüklenmesi", "scripts/advanced_ai/publish_to_database.py",
         lambda: _safe_json(db_dir / "derived" / "curriculum_links" / "manifest.json").get("sayilar", {}).get("soru_slayt", 0), 2839),
        ("yayin", "Site yayını", "soru", "Faz 5, 6, 6.5 ve 8 analizlerinin web sitesine aktarılması", "scripts/advanced_ai/export_phase_insights.py",
         lambda: _json_count(db_dir / "derived" / "phase_insights" / "insights.json", "items"), 7219),
        ("asama1", "Aşama 1 · İndirme & OCR", "kaynak", "Yeni veya yenilenen PDF/PPTX dosyalarının OCR ile taranması", "scripts/agents/stage1_refresh.py",
         lambda: len(_safe_json(temp_dir / "state" / "stage1_refresh_report.json").get("yeniden_ocr") or []), 10),
        ("faz12", "Faz 12 · Ders notu temizleme", "chunk", "Glif, OCR çöpü, üst/alt bilgi filtreleme", "scripts/advanced_ai/phase12_clean_notes.py",
         lambda: _safe_json(db_dir / "derived" / "clean_notes" / "rapor.json").get("degisen", 0), 5000),
        ("faz13", "Faz 13 · Tıbbi varlıklar", "soru", "GLiNER ve medikal terminolojiyle varlık tanıma", "scripts/advanced_ai/phase13_entities.py",
         lambda: _fast_lines(db_dir / "derived" / "entities" / "soru_varliklar.jsonl"), 7219),
        ("faz14", "Faz 14 · Çıkmış soru redaksiyonu", "soru", "Yerel/bulut modellerle inceleme kuyruğuna redaksiyon önerisi", "scripts/advanced_ai/phase14_past_question_editor.py",
         lambda: _fast_lines(db_v2_dir / "phase14_past_question_editor" / "reviews.jsonl"), 4926),
        ("ortak", "Ortak RAG deposu", "parça", "Birleştirilmiş ortak ders materyali ve RAG veri havuzu", "scripts/advanced_ai/build_unified_store.py",
         lambda: _fast_lines(db_dir / "ortak" / "rag" / "ders_materyali.jsonl"), 25000),
        ("hakem", "Hakem kuyruğu", "karar", "Alıntı doğrulamalı konu ve slayt hakem değerlendirmesi", "scripts/advanced_ai/referee_queue.py",
         lambda: _fast_lines(temp_dir / "hakem" / "kararlar.jsonl"), 1000),
    ]

    cyc = _safe_json(PHASE_CYCLE_STATE)
    steps = cyc.get("adimlar") or {}
    aktif = cyc.get("aktif")
    tur = cyc.get("tur", 1)
    done_now = set(cyc.get("tur_tamamlanan") or [])

    # Kuyruk bilgisi
    queue_list = []
    if PHASE_QUEUE_FILE.exists():
        try:
            with open(PHASE_QUEUE_LOCK, "w") as lk:
                fcntl.flock(lk, fcntl.LOCK_SH)
                try:
                    queue_list = json.load(open(PHASE_QUEUE_FILE, encoding="utf-8"))
                finally:
                    fcntl.flock(lk, fcntl.LOCK_UN)
        except Exception:
            try:
                queue_list = json.loads(PHASE_QUEUE_FILE.read_text(encoding="utf-8"))
            except Exception:
                queue_list = []

    phases_out = []
    for key, name, unit, desc, script_path, fn, target in rows_def:
        try:
            cnt = int(fn() or 0)
        except Exception:
            cnt = 0

        st = steps.get(key) or {}
        rc = st.get("rc")
        sure_sec = st.get("sure_sn")
        bitis_raw = st.get("bitis") or "-"
        bitis = bitis_raw.replace("T", " ")[5:16] if bitis_raw != "-" else "-"

        # Durum tespiti
        if key == aktif:
            status_code = "running"
            durum_tr = "● çalışıyor"
            sure_str = "sürüyor"
            hiz = "ölçülüyor…"
        elif rc not in (None, 0):
            status_code = "error"
            durum_tr = f"✗ hata rc={rc}"
            sure_str = _fmt_dur(sure_sec)
            hiz = "-"
        elif st:
            status_code = "completed_this" if key in done_now else "completed_prev"
            durum_tr = "✓ bu turda" if key in done_now else "✓ önceki tur"
            sure_str = _fmt_dur(sure_sec)
            s_ = sure_sec or 0
            hiz = f"{cnt / (s_ / 60):.0f} {unit}/dk (son tur)" if s_ >= 5 and cnt else ("anında" if cnt else "-")
        else:
            status_code = "none"
            durum_tr = "○ henüz yok"
            sure_str = "-"
            hiz = "-"

        # Kalan ve yüzde
        if target > 0:
            pct = min(100.0, round((cnt / target) * 100, 1))
            kalan = max(0, target - cnt)
        else:
            pct = 100.0
            kalan = 0

        in_queue = key in queue_list
        queue_pos = queue_list.index(key) + 1 if in_queue else None

        phases_out.append({
            "key": key,
            "name": name,
            "unit": unit,
            "desc": desc,
            "script": script_path,
            "status_code": status_code,
            "status_tr": durum_tr,
            "output_count": cnt,
            "target": target,
            "kalan": kalan,
            "pct": pct,
            "duration": sure_str,
            "duration_sec": sure_sec,
            "speed": hiz,
            "last_end": bitis,
            "in_queue": in_queue,
            "queue_pos": queue_pos
        })

    # Faz 7 v2 özel istatistiği
    p7v2_file = db_v2_dir / "phase7_v2" / "soru_metadata.jsonl"
    p7v2_stats = {"n": 0, "celiski": 0}
    if p7v2_file.exists():
        try:
            for l in p7v2_file.read_text(encoding="utf-8").splitlines():
                if not l.strip(): continue
                o = json.loads(l)
                p7v2_stats["n"] += 1
                if (o.get("cevap_denetimi") or {}).get("sonuc") == "anahtar_celiskisi":
                    p7v2_stats["celiski"] += 1
        except Exception:
            pass

    res = {
        "tur": tur,
        "aktif": aktif,
        "queue": queue_list,
        "phases": phases_out,
        "p7v2": p7v2_stats
    }
    _MASTER_PHASES_CACHE["data"] = res
    _MASTER_PHASES_CACHE["ts"] = time.time()
    return res

def get_phase_log(key: str, lines_limit: int = 150):
    """Belirtilen fazın veya ana döngünün log dosyasından son satırları döner."""
    temp_dir = PROJECT_ROOT / "meds_temp"
    log_file = temp_dir / "logs" / f"phase_cycle_{key}.log"
    
    # Hakem fazı için özel log ve durum desteği
    if key == "hakem":
        hakem_lines = []
        if log_file.exists():
            try:
                raw = log_file.read_text(encoding="utf-8", errors="replace").strip()
                if raw: hakem_lines.extend(raw.splitlines())
            except Exception: pass
        # En son kararlardan canlı akış satırları ekle
        kararlar_file = temp_dir / "hakem" / "kararlar.jsonl"
        if kararlar_file.exists():
            try:
                with open(kararlar_file, "rb") as fh:
                    fh.seek(0, 2)
                    fsize = fh.tell()
                    fh.seek(max(0, fsize - 30000))
                    for line in fh.read().decode("utf-8", errors="replace").splitlines():
                        if not line.strip(): continue
                        try:
                            item = json.loads(line)
                            k_tur = item.get("tur", "")
                            k_qid = item.get("soru_id", "")
                            k_karar = item.get("karar", "")
                            k_alinti = (item.get("alinti") or item.get("neden") or "")[:70]
                            k_time = item.get("zaman", "")[11:19]
                            hakem_lines.append(f"[{k_time}] [hakem] {k_tur.upper()} #{k_qid}: karar={k_karar} -> {k_alinti}")
                        except Exception: pass
            except Exception: pass
        if hakem_lines:
            return {"key": key, "file": "phase_cycle_hakem.log + kararlar.jsonl", "lines": hakem_lines[-lines_limit:]}

    if not log_file.exists() or (log_file.stat().st_size == 0):
        # Fallback: ana phase_cycle.log veya pipeline.log
        if key == "cycle":
            log_file = temp_dir / "logs" / "phase_cycle.log"
        else:
            log_file = temp_dir / "logs" / "phase_cycle.log"

    if not log_file.exists():
        return {"key": key, "lines": ["Henüz log kaydı oluşturulmadı."]}

    try:
        with open(log_file, "rb") as fh:
            fh.seek(0, 2)
            fsize = fh.tell()
            fh.seek(max(0, fsize - 50000))
            text = fh.read().decode("utf-8", errors="replace")
            lines = [l for l in text.splitlines() if l.strip()]
            return {"key": key, "file": log_file.name, "lines": lines[-lines_limit:]}
    except Exception as e:
        return {"key": key, "error": str(e), "lines": [f"Log okuma hatası: {e}"]}

def handle_master_phase_action(action: str, key: str, queue_order: list):
    """Faz kuyruk yönetim işlemlerini (run_now, enqueue, remove, reorder, stop_active, stop_phase) kilitli uygular."""
    PHASE_QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PHASE_QUEUE_LOCK, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            try:
                q = json.load(open(PHASE_QUEUE_FILE, encoding="utf-8")) if PHASE_QUEUE_FILE.exists() else []
            except Exception:
                q = []

            # 1. Aktif fazı durdurma işlemi
            if action in ("stop_active", "stop_phase"):
                cyc_file = PROJECT_ROOT / "meds_temp" / "state" / "phase_cycle_state.json"
                aktif_phase = None
                if cyc_file.exists():
                    try:
                        cdata = json.loads(cyc_file.read_text(encoding="utf-8"))
                        aktif_phase = cdata.get("aktif")
                    except Exception:
                        pass
                
                target_key = key if (action == "stop_phase" and key) else aktif_phase
                if not target_key:
                    return {"success": False, "error": "Şu anda çalışan aktif bir faz bulunmuyor."}

                # Script adına göre çalışan Python alt süreçlerini bul ve sonlandır
                script_map = {
                    "faz5": "multi_ai_consensus_phase5.py",
                    "faz6": "deep_metadata_generator_phase6.py",
                    "faz6_dogrulama": "validate_phase6_metadata.py",
                    "faz6_5": "thesaurus_anchor_phase6_5.py",
                    "faz7_5": "reconstruct_slides_phase7_5.py",
                    "faz8": "phase8_curriculum_graph.py",
                    "sozluk": "build_evidence_thesaurus.py",
                    "faz9": "phase9_thesaurus_graph.py",
                    "faz10": "phase10_concept_ids.py",
                    "faz11": "phase11_question_slide.py",
                    "ogren": "learn_links.py",
                    "yeniden_bolme": "resplit_exam_printout.py",
                    "karantina": "quarantine_questions.py",
                    "veritabani": "publish_to_database.py",
                    "yayin": "export_phase_insights.py",
                    "asama1": "stage1_refresh.py",
                    "faz12": "phase12_clean_notes.py",
                    "faz13": "phase13_entities.py",
                    "faz14": "phase14_past_question_editor.py",
                    "ortak": "build_unified_store.py",
                    "hakem": "referee_queue.py",
                }
                scr_name = script_map.get(target_key)
                if scr_name:
                    try:
                        subprocess.run(["pkill", "-15", "-f", scr_name], capture_output=True, timeout=5)
                        time.sleep(0.5)
                        subprocess.run(["pkill", "-9", "-f", scr_name], capture_output=True, timeout=5)
                    except Exception as kerr:
                        print(f"[Master Stop] Process kill warning: {kerr}")

                # phase_cycle_state.json dosyasında aktif durumu temizle
                if cyc_file.exists():
                    try:
                        cdata = json.loads(cyc_file.read_text(encoding="utf-8"))
                        if cdata.get("aktif") == target_key:
                            cdata["aktif"] = None
                            cdata.setdefault("adimlar", {})[target_key] = {
                                "rc": 137,
                                "sure_sn": 0,
                                "bitis": time.strftime("%Y-%m-%dT%H:%M:%S")
                            }
                            cyc_file.write_text(json.dumps(cdata, ensure_ascii=False, indent=2), encoding="utf-8")
                    except Exception:
                        pass

                return {"success": True, "action": action, "key": target_key, "message": f"'{target_key}' süreci başarıyla durduruldu."}

            if action == "run_now":
                # Hemen çalıştır: Kuyruğun en başına ekle (varsa eski yerinden çıkar)
                if key in q:
                    q.remove(key)
                q.insert(0, key)
            elif action == "enqueue":
                # Kuyruğa ekle: Sona ekle
                if key not in q:
                    q.append(key)
            elif action == "remove":
                # Kuyruktan kaldır
                if key in q:
                    q.remove(key)
            elif action == "reorder":
                # Tüm sıralamayı güncelle
                if isinstance(queue_order, list):
                    q = [str(k) for k in queue_order]
            elif action == "clear":
                q = []

            tmp = PHASE_QUEUE_FILE.with_suffix(".tmp")
            json.dump(q, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            tmp.replace(PHASE_QUEUE_FILE)
            return {"success": True, "action": action, "key": key, "queue": q}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            fcntl.flock(lk, fcntl.LOCK_UN)

def handle_master_schedule(payload: dict):
    try:
        sys.path.insert(0, str(MEDS_DIR / "scripts"))
        import master_controller
        ctrl = master_controller.MasterController()
        ctrl.schedule_config["enabled"] = bool(payload.get("enabled", False))
        ctrl.schedule_config["start_hour"] = int(payload.get("start_hour", 8))
        ctrl.schedule_config["end_hour"] = int(payload.get("end_hour", 23))
        ctrl.save_config()
        ctrl.write_state_file()
        return {"success": True, "schedule": ctrl.schedule_config}
    except Exception as e:
        return {"success": False, "error": str(e)}

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), RequestHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    run()

