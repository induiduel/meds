#!/usr/bin/env python3
"""
MedSoru 4-Bit QLoRA Fine-Tuning Eğitici (RTX 4060 8GB VRAM Optimize)
Kaynak : meds/training_data/medsoru_train.jsonl & medsoru_val.jsonl
Hedef  : Tıp Fakültesi Dönem 3'e özel yerel tıp uzmanı modeli (LoRA Adaptörü)

Özellikler:
- 4-Bit NormalFloat (NF4) kuantizasyon (BitsAndBytes)
- Gradient Checkpointing & Paged AdamW 8-bit ile 8GB VRAM sınırında sıfır OOM
- AGENTS.md Termal Güvenlik Freni (GPU > 80°C olduğunda otomatik soğuma beklemesi)
- Alpaca formatı şablonlaması ve SFT Trainer entegrasyonu
- Eğitim sonrası LoRA adaptör kaydı ve Ollama Modelfile üretimi
"""

import argparse
import os
import subprocess
import sys
import time
import warnings
from pathlib import Path

# PyTorch / pynvml uyarısını sustur
warnings.filterwarnings("ignore", category=FutureWarning, module="torch.cuda")

ROOT = Path(__file__).resolve().parents[2]
if not (ROOT / "meds_database").exists():
    ROOT = Path(__file__).resolve().parents[3]

TRAIN_DATA_FILE = ROOT / "meds" / "training_data" / "medsoru_train.jsonl"
VAL_DATA_FILE = ROOT / "meds" / "training_data" / "medsoru_val.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "meds" / "models" / "medsoru-d3-qlora"


def check_gpu_status():
    """NVIDIA GPU kullanılabilirliğini ve sıcaklığını denetler."""
    try:
        cmd = [
            "nvidia-smi",
            "--query-gpu=name,memory.total,memory.free,temperature.gpu,utilization.gpu",
            "--format=csv,noheader,nounits",
        ]
        out = subprocess.check_output(cmd, text=True).strip().split("\n")[0]
        name, total_mem, free_mem, temp, util = [x.strip() for x in out.split(",")]
        return {
            "available": True,
            "name": name,
            "total_mem_mb": float(total_mem),
            "free_mem_mb": float(free_mem),
            "temp_c": float(temp),
            "util_percent": float(util),
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


def wait_for_gpu_cooling(max_temp: float = 78.0, safe_temp: float = 68.0):
    """GPU aşırı ısındığında (AGENTS.md Kuralı) güvenli sıcaklığa inene kadar bekletir."""
    status = check_gpu_status()
    if not status["available"]:
        return
    current_temp = status.get("temp_c", 0.0)
    if current_temp >= max_temp:
        print(f"\n[TERMAL FREN] GPU sıcaklığı {current_temp}°C >= {max_temp}°C! Soğutma bekleniyor...")
        while current_temp > safe_temp:
            time.sleep(5)
            status = check_gpu_status()
            current_temp = status.get("temp_c", 0.0)
            print(f"  -> Soğuma durumu: {current_temp}°C (Hedef: <={safe_temp}°C)", end="\r")
        print(f"\n[TERMAL FREN] GPU güvenli sıcaklığa ({current_temp}°C) ulaştı. Eğitime devam ediliyor.\n")


def build_thermal_callback(TrainerCallback):
    """HuggingFace Trainer için termal izleme callback'i."""
    class ThermalSafetyCallback(TrainerCallback):
        def on_step_end(self, args, state, control, **kwargs):
            if state.global_step % 25 == 0:
                wait_for_gpu_cooling(max_temp=80.0, safe_temp=70.0)
    return ThermalSafetyCallback


def generate_ollama_modelfile(adapter_path: Path, base_model: str, out_modelfile: Path):
    """Eğitilen LoRA adaptörü için Ollama Modelfile üretir."""
    content = f"""# MedSoru Özel Dönem 3 Tıp Modeli (QLoRA Adaptörlü)
FROM {base_model}
ADAPTER {adapter_path}

# Hiperparametreler (Akademik hassasiyet, düşük halüsinasyon)
PARAMETER temperature 0.2
PARAMETER top_p 0.9
PARAMETER stop "<end_of_turn>"
PARAMETER stop "<eos>"

# Sistem Rolü
SYSTEM \"\"\"
Sen Tıp Fakültesi Dönem 3 (Patoloji, Farmakoloji, Mikrobiyoloji, Dahiliye, Genel Cerrahi) kurulları için özel olarak fine-tune edilmiş MedSoru Akademik Tıp Asistanısın.
Ders slaytları ve çıkmış kurul soruları doğrultusunda klinik mantığı ve soru çözümlerini kanıtlarıyla açıklarsın.
\"\"\"
"""
    out_modelfile.parent.mkdir(parents=True, exist_ok=True)
    out_modelfile.write_text(content, encoding="utf-8")
    print(f"[MODELFILE] Ollama Modelfile oluşturuldu: {out_modelfile}")


def run_training(args):
    # Kütüphane Kontrolleri
    try:
        import torch
        from datasets import load_dataset
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            BitsAndBytesConfig,
            TrainerCallback,
        )
        from trl import SFTTrainer, SFTConfig
    except ImportError as e:
        print("\n[HATA] Gerekli yapay zeka kütüphaneleri eksik:")
        print(f"  Detay: {e}")
        print("\nLütfen önce şu komutu çalıştırarak bağımlılıkları yükleyin:")
        print("  pip install -r scripts/training/requirements-train.txt")
        print("\nYa da izole bir sanal ortam oluşturup kurun:")
        print("  python3 -m venv meds_venv && source meds_venv/bin/activate && pip install -r scripts/training/requirements-train.txt\n")
        sys.exit(1)

    # CUDA Kontrolü
    if not torch.cuda.is_available():
        print("[HATA] PyTorch CUDA desteği bulunamadı. GPU üzerinden eğitim yapılamaz.")
        sys.exit(1)

    gpu_info = check_gpu_status()
    print("=" * 60)
    print("MedSoru 4-Bit QLoRA Fine-Tuning Başlatılıyor (RTX 4060 8GB)")
    print(f"Cihaz             : {gpu_info.get('name')}")
    print(f"Kullanılabilir VRAM: {gpu_info.get('free_mem_mb'):.0f} MB / {gpu_info.get('total_mem_mb'):.0f} MB")
    print(f"Mevcut Sıcaklık   : {gpu_info.get('temp_c')}°C")
    print(f"Taban Model       : {args.base_model}")
    print(f"Eğitim Verisi     : {TRAIN_DATA_FILE}")
    print(f"Çıktı Dizini      : {args.output_dir}")
    print("=" * 60)

    if not TRAIN_DATA_FILE.exists() or os.path.getsize(TRAIN_DATA_FILE) == 0:
        print("[HATA] Eğitim veri seti bulunamadı. Lütfen önce 'prepare_dataset.py' çalıştırın.")
        sys.exit(1)

    # HF Token kontrolü (Hızlı indirme ve kimlik doğrulama için)
    hf_token = args.hf_token or os.environ.get("HF_TOKEN") or None

    # 1. 4-Bit Kuantizasyon Yapılandırması (NF4 + Double Quantization)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16,
    )

    # 2. Tokenizer & Taban Model Yükleme
    print(f"\n[1/5] Taban Model ve Tokenizer Yükleniyor ({args.base_model})...")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model, token=hf_token, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        token=hf_token,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )

    # 3. K-Bit Eğitime Hazırlama & LoRA Konfigürasyonu
    print("[2/5] 4-Bit Modeli K-Bit Eğitime Hazırlanıyor & LoRA Konfigürasyonu Tanımlanıyor...")
    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)

    lora_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
    )

    # 4. Veri Seti Yükleme ve Alpaca Formatına Dönüştürme
    print("[3/5] Alpaca Formatındaki Tıp Veri Seti Yükleniyor...")
    data_files = {"train": str(TRAIN_DATA_FILE)}
    if VAL_DATA_FILE.exists():
        data_files["validation"] = str(VAL_DATA_FILE)

    raw_datasets = load_dataset("json", data_files=data_files)

    def apply_alpaca_template(example):
        inst = example["instruction"]
        inp = example["input"]
        out = example["output"]
        return {
            "text": f"### Instruction:\n{inst}\n\n### Input:\n{inp}\n\n### Response:\n{out}{tokenizer.eos_token}"
        }

    train_ds = raw_datasets["train"].map(apply_alpaca_template, desc="Alpaca şablonu uygulanıyor (Train)")
    val_ds = raw_datasets["validation"].map(apply_alpaca_template, desc="Alpaca şablonu uygulanıyor (Val)") if VAL_DATA_FILE.exists() else None

    # 5. Eğitim Argümanları (RTX 4060 8GB Optimize)
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    has_val = val_ds is not None
    training_args = SFTConfig(
        output_dir=str(output_path),
        dataset_text_field="text",
        max_length=args.max_seq_length,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_steps=20,
        num_train_epochs=args.epochs,
        logging_steps=10,
        save_strategy="steps",
        save_steps=100,
        eval_strategy="steps" if has_val else "no",
        eval_steps=100 if has_val else None,
        save_total_limit=2,
        optim="paged_adamw_8bit",
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        gradient_checkpointing=True,
        report_to="none",
    )

    ThermalSafetyCallback = build_thermal_callback(TrainerCallback)

    trainer = SFTTrainer(
        model=model,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        peft_config=lora_config,
        processing_class=tokenizer,
        args=training_args,
        callbacks=[ThermalSafetyCallback()],
    )

    print("\n[4/5] 4-Bit QLoRA Eğitimi Başlatılıyor...")
    trainer.train()

    print(f"\n[5/5] Eğitim Tamamlandı! Adaptör Ağırlıkları Kaydediliyor: {output_path}")
    trainer.model.save_pretrained(str(output_path))
    tokenizer.save_pretrained(str(output_path))

    # Ollama Modelfile oluştur
    modelfile_path = output_path / "Modelfile"
    generate_ollama_modelfile(output_path, args.base_model, modelfile_path)

    print("\n" + "=" * 60)
    print("TEBRİKLER! MedSoru Dönem 3 Yerel Modeli Başarıyla Eğitildi.")
    print(f"LoRA Adaptör Yolu : {output_path}")
    print(f"Ollama Modelfile  : {modelfile_path}")
    print(f"Ollama'ya Almak İçin:")
    print(f"  ollama create medsoru-d3 -f '{modelfile_path}'")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="MedSoru 4-Bit QLoRA Fine-Tuning (RTX 4060 8GB)")
    parser.add_argument("--base-model", type=str, default="Qwen/Qwen2.5-3B-Instruct", help="Taban model (Örn: Qwen/Qwen2.5-3B-Instruct, google/gemma-2-2b-it)")
    parser.add_argument("--batch-size", type=int, default=1, help="Cihaz başına mini-batch boyutu (8GB VRAM için 1)")
    parser.add_argument("--gradient-accumulation-steps", type=int, default=16, help="Gradyan biriktirme adımı (Efektif batch: 16)")
    parser.add_argument("--epochs", type=int, default=3, help="Eğitim epoch sayısı (varsayılan: 3)")
    parser.add_argument("--lr", type=float, default=2e-4, help="Öğrenme oranı (Learning rate)")
    parser.add_argument("--max-seq-length", type=int, default=1024, help="Maksimum token uzunluğu")
    parser.add_argument("--lora-r", type=int, default=16, help="LoRA Rank (r)")
    parser.add_argument("--lora-alpha", type=int, default=32, help="LoRA Alpha")
    parser.add_argument("--lora-dropout", type=float, default=0.05, help="LoRA Dropout")
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR), help="Model adaptörü kayıt dizini")
    parser.add_argument("--hf-token", type=str, default=None, help="Hugging Face erişim anahtarı (HF_TOKEN)")
    parser.add_argument("--check-gpu", action="store_true", help="Yalnızca GPU durumunu ve sıcaklığını kontrol et")

    args = parser.parse_args()

    if args.check_gpu:
        status = check_gpu_status()
        print("GPU Durumu:")
        for k, v in status.items():
            print(f"  {k}: {v}")
        return

    run_training(args)


if __name__ == "__main__":
    main()
