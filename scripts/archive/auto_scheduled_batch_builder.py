#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/auto_scheduled_batch_builder.py
Manages the structured batch queue for all Kurul 1 lectures.
Processes each lecture into deep %500 interactive decks on a planned schedule.
"""

import json
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

QUEUE_FILE = os.path.join('src', 'data', 'learning_batch_queue.json')

INITIAL_QUEUE = [
    {
        "id": "deck-urinary-obstruction",
        "title": "Üriner Obstrüksiyon; Patofizyoloji, Klinik ve Tedavi",
        "discipline": "Üroloji / Nefroloji",
        "status": "completed",
        "slidesCount": 21,
        "detailLevel": "500%"
    },
    {
        "id": "deck-urolithiasis-pathophysiology",
        "title": "Ürolitiyazis Patofizyolojisi (Taş Hastalığı)",
        "discipline": "Üroloji / Tıbbi Biyokimya & Patoloji",
        "status": "completed",
        "slidesCount": 20,
        "detailLevel": "500%"
    },
    {
        "id": "deck-urinary-tract-infections",
        "title": "Üriner Sistem Enfeksiyonları",
        "discipline": "Üroloji / Enfeksiyon Hastalıkları",
        "status": "completed",
        "slidesCount": 21,
        "detailLevel": "500%"
    },
    {
        "id": "deck-acute-inflammation-pathology",
        "title": "Akut Enflamasyon: Vasküler Değişiklikler ve Hücresel Olaylar",
        "discipline": "Tıbbi Patoloji",
        "status": "completed",
        "slidesCount": 22,
        "detailLevel": "500%"
    },
    {
        "id": "learn-hucre-hasari-hucre-olumu",
        "title": "Hücre Hasarı, Hücre Ölümü ve Nekroz Patolojisi",
        "discipline": "Tıbbi Patoloji",
        "status": "completed",
        "slidesCount": 24,
        "detailLevel": "500%"
    },
    {
        "id": "learn-odem-hiperemi-konjesyon",
        "title": "Hemodinamik Bozukluklar: Ödem, Hiperemi, Konjesyon ve Kanama",
        "discipline": "Tıbbi Patoloji",
        "status": "next_in_queue",
        "slidesCount": 20,
        "detailLevel": "500% (Planlanan)"
    },
    {
        "id": "learn-kronik-enflamasyon",
        "title": "Kronik Enflamasyon, Granülomlar ve Doku Onarımı",
        "discipline": "Tıbbi Patoloji",
        "status": "queued",
        "slidesCount": 20,
        "detailLevel": "500% (Planlanan)"
    },
    {
        "id": "learn-hucresel-adaptasyon-ve-hu",
        "title": "Hücresel Adaptasyonlar: Atrofi, Hipertrofi, Hiperplazi, Metaplazi",
        "discipline": "Tıbbi Patoloji",
        "status": "queued",
        "slidesCount": 18,
        "detailLevel": "500% (Planlanan)"
    },
    {
        "id": "learn-intraseluler-birikimler",
        "title": "İntraselüler Birikimler ve Patolojik Kalsifikasyonlar",
        "discipline": "Tıbbi Patoloji",
        "status": "queued",
        "slidesCount": 16,
        "detailLevel": "500% (Planlanan)"
    },
    {
        "id": "learn-dismorfoloji-terminolojisi",
        "title": "Dismorfolojide Genetik Terminoloji ve Malformasyonlar",
        "discipline": "Tıbbi Genetik",
        "status": "queued",
        "slidesCount": 16,
        "detailLevel": "500% (Planlanan)"
    },
    {
        "id": "learn-kromozomal-hastaliklar-ve",
        "title": "Kromozomal Hastalıklar ve Genetik Danışma",
        "discipline": "Tıbbi Genetik",
        "status": "queued",
        "slidesCount": 18,
        "detailLevel": "500% (Planlanan)"
    },
    {
        "id": "learn-halk-sagligi-salgin-has",
        "title": "Salgın Hastalıklarda Kontrol, Sürveyans ve Korunma",
        "discipline": "Halk Sağlığı",
        "status": "queued",
        "slidesCount": 16,
        "detailLevel": "500% (Planlanan)"
    },
    {
        "id": "learn-enfeksiyon-izolasyon",
        "title": "Hastane Enfeksiyonları ve İzolasyon Önlemleri",
        "discipline": "Enfeksiyon Hastalıkları",
        "status": "queued",
        "slidesCount": 14,
        "detailLevel": "500% (Planlanan)"
    }
]

def load_or_init_queue():
    if not os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
            json.dump(INITIAL_QUEUE, f, ensure_ascii=False, indent=2)
        return INITIAL_QUEUE
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_queue_status():
    queue = load_or_init_queue()
    print("=" * 70)
    print("📋 KURUL 1 DERSLERİ - %500 PLANLI BATCH ÖĞRENME KUYRUĞU")
    print("=" * 70)
    completed = [item for item in queue if item.get('status') == 'completed']
    next_item = [item for item in queue if item.get('status') == 'next_in_queue']
    queued = [item for item in queue if item.get('status') == 'queued']

    print(f"Tamamlanan Derin Güverteler: {len(completed)}")
    for item in completed:
        print(f"  ✓ [{item['discipline']}] {item['title']} ({item['slidesCount']} Slayt)")

    if next_item:
        n = next_item[0]
        print(f"\nSıradaki İşlemde Olan Ders:")
        print(f"  ▶ [{n['discipline']}] {n['title']} (Hedef: {n['slidesCount']} Slayt)")

    print(f"\nKuyrukta Bekleyen Dersler: {len(queued)}")
    for item in queued:
        print(f"  ⏳ [{item['discipline']}] {item['title']}")
    print("=" * 70)

if __name__ == '__main__':
    print_queue_status()
