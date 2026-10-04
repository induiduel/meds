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

    def execute_react_cycle(self, question: str, max_steps: int = 4, graph_triples: str = "") -> Dict[str, Any]:
        """
        ReAct Döngüsü (XML ve Zorunlu CoT Akıl Yürütme ile Güçlendirilmiş):
        <THOUGHT>: Adım adım klinik düşünce zinciri
        <ACTION>: Fonksiyon çağırma [FonksiyonAdı(arg=...)]
        <OBSERVATION>: Fonksiyon çıktısı
        <YANIT>: Tıbbi kanıtlara dayalı nihai cevap
        """
        prompt_tools = "\n".join([f"- {name}: {desc}" for name, desc in self.tool_descriptions.items()])
        graph_section = f"\n{graph_triples}\n" if graph_triples else ""
        
        history = (
            "Sen uzman bir tıp fakültesi asistanısın. Yalnızca amfi ders slaytlarındaki kanıtlara dayan.\n"
            f"{graph_section}"
            f"<SORU>\n{question}\n</SORU>\n\n"
            f"<KULLANILABİLİR_ARAÇLAR>\n{prompt_tools}\n</KULLANILABİLİR_ARAÇLAR>\n\n"
            "Format Kuralları:\n"
            "<THOUGHT>: Klinik bulguları analiz et ve sonraki adımı planla.\n"
            "<ACTION>: AracAdi(parametre)\n"
            "(Action sonrasında bekle, <OBSERVATION> sistem tarafından verilecektir)\n\n"
            "Soruyu çözdüğünde doğrudan:\n"
            "<ANALİZ>: 1. Soru kökündeki anahtar klinik bulgu. 2. Slayt kanıtları. 3. Yanlış şıkların elenmesi.\n"
            "<YANIT>: Doğru şık ve slayttan kanıtlı kısa akademik gerekçe.\n"
        )

        steps = []
        for step in range(max_steps):
            # Model çağrısı
            response = self.llm_chat_fn(history)
            history += "\n" + response

            # Final Answer / <YANIT> kontrolü
            if "<YANIT>" in response:
                final_ans = response.split("<YANIT>")[-1].split("</YANIT>")[0].strip()
                return {
                    "status": "success",
                    "final_answer": final_ans,
                    "steps": steps,
                    "full_trace": history
                }
            elif "Final Answer:" in response:
                final_ans = response.split("Final Answer:")[-1].strip()
                return {
                    "status": "success",
                    "final_answer": final_ans,
                    "steps": steps,
                    "full_trace": history
                }

            # Action tespiti (Action: ... veya <ACTION>...</ACTION>)
            action_match = re.search(r"(?:<ACTION>|Action:\s*)(\w+)\((.*?)\)(?:</ACTION>)?", response)
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
