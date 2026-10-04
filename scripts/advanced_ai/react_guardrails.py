"""
ReAct (Reasoning + Acting) & Function Calling & Guardrails Motoru
- Düşünce (Thought) -> Eylem (Action) -> Gözlem (Observation) döngüsü
- Guardrails: Tıbbi uydurma (hallucination) engelleme, kaynak doğrulaması
- Function Registry: Arama, Soru Getirme, Graf Sorgulama araçları
"""
import json
import re
from typing import Dict, Any, Callable

class MedicalGuardrails:
    @staticmethod
    def validate_clinical_claim(claim: str, context: str) -> tuple[bool, str]:
        """Tıbbi iddianın ders slaytlarında/kaynakta desteklenip desteklenmediğini denetler"""
        claim_terms = set(re.findall(r"\w{4,}", claim.lower()))
        context_terms = set(re.findall(r"\w{4,}", context.lower()))
        
        if not claim_terms:
            return True, "Geçerli"
        
        overlap = len(claim_terms & context_terms) / len(claim_terms)
        if overlap < 0.35:
            return False, f"Guardrail Uyarısı: Cevap amfi ders notlarında geçmeyen yabancı kavramlar içeriyor! (Örtüşme: {overlap:.2f})"
        return True, "Onaylandı"

    @staticmethod
    def censor_unsafe_treatment(text: str) -> str:
        """Klinik uygulama veya reçeteleme riski içeren durumlarda akademik disclaimer ekler"""
        disclaimer = "\n\n*[MedSoru Akademik Bilgilendirme: Bu içerik Tıp Fakültesi Dönem 3 ders notlarından amfi sınavlarına hazırlık amacıyla derlenmiştir. Gerçek klinik tanı veya tedavi yerine geçmez.]*"
        return text + disclaimer

class MedicalReActAgent:
    def __init__(self, llm_chat_fn: Callable):
        self.llm_chat_fn = llm_chat_fn
        self.tools: Dict[str, Callable] = {}
        self.tool_descriptions: Dict[str, str] = {}

    def register_tool(self, name: str, description: str, fn: Callable):
        self.tools[name] = fn
        self.tool_descriptions[name] = description

    def execute_react_cycle(self, question: str, max_steps: int = 4) -> Dict[str, Any]:
        """
        ReAct Döngüsü:
        Thought: Modelin sonraki adımı planlaması
        Action: Fonksiyon çağırma [FonksiyonAdı(arg=...)]
        Observation: Fonksiyon çıktısı
        Final Answer: Nihai yanıt
        """
        prompt_tools = "\n".join([f"- {name}: {desc}" for name, desc in self.tool_descriptions.items()])
        history = (
            f"Kullanıcı Sorusu: {question}\n\n"
            f"Kullanabileceğin Araçlar:\n{prompt_tools}\n\n"
            "Format Kuralları:\n"
            "Thought: Ne yapman gerektiğini açıkla.\n"
            "Action: AracAdi(parametre)\n"
            "Action sonrasında bekle, Observation sistem tarafından verilecek.\n"
            "Bilgiyi doğruladığında:\n"
            "Final Answer: Tıbbi kanıtlara dayalı net cevabını yaz.\n"
        )

        steps = []
        for step in range(max_steps):
            # Model çağrısı
            response = self.llm_chat_fn(history)
            history += "\n" + response

            # Final Answer kontrolü
            if "Final Answer:" in response:
                final_ans = response.split("Final Answer:")[-1].strip()
                return {
                    "status": "success",
                    "final_answer": final_ans,
                    "steps": steps,
                    "full_trace": history
                }

            # Action tespiti
            action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", response)
            if action_match:
                func_name = action_match.group(1)
                func_arg = action_match.group(2).strip("\"'")
                steps.append({"thought": response, "action": func_name, "arg": func_arg})

                if func_name in self.tools:
                    try:
                        obs = str(self.tools[func_name](func_arg))
                    except Exception as e:
                        obs = f"Araç çalıştırma hatası: {e}"
                else:
                    obs = f"Hata: {func_name} adında bir araç tanımlı değil."

                obs_text = f"\nObservation: {obs}\n"
                history += obs_text
                steps[-1]["observation"] = obs
            else:
                # Eylem üretmediyse devam et veya bitir
                break

        return {
            "status": "partial",
            "final_answer": "Maksimum adım sayısına ulaşıldı veya doğrudan yanıt üretildi.",
            "steps": steps,
            "full_trace": history
        }
