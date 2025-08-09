import os
from typing import List, Dict, Optional
from dataclasses import dataclass
from .prompts import SYSTEM_PROMPT, WORKPAPER_TEMPLATE, TEST_SCRIPT_TEMPLATE, RISK_ASSESSMENT_INSTRUCTIONS, CHECKLISTS
from .bcbs239 import BCBS239

# Optional: OpenAI client (user supplies API key)
try:
    from openai import OpenAI
    _has_openai = True
except Exception:
    _has_openai = False
    OpenAI = None  # type: ignore

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

@dataclass
class LLMConfig:
    api_key: Optional[str] = None
    model: str = DEFAULT_MODEL

def _llm_call(prompt: str, cfg: LLMConfig) -> str:
    """
    Calls OpenAI if API key provided; otherwise returns a safe, rule-based fallback.
    """
    if _has_openai and cfg.api_key:
        client = OpenAI(api_key=cfg.api_key)
        resp = client.chat.completions.create(
            model=cfg.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content
    # Fallback: minimal templated response
    return (
        "⚠️ **Offline mode (no API key detected).**\n\n"
        "Here is a structured template based on your inputs. Add your specifics and, if needed, set the OPENAI_API_KEY to enable LLM drafting.\n\n"
        + prompt
    )

def generate_risk_assessment(context: Dict, cfg: LLMConfig) -> str:
    prompt = f"""
{RISK_ASSESSMENT_INSTRUCTIONS}

Context:
- Business area: {context.get('business_area','(not provided)')}
- Reports in scope: {context.get('reports','(not provided)')}
- Prior issues: {context.get('prior_issues','(not provided)')}
- Risk criteria: {context.get('criteria','regulatory risk, complexity, materiality')}

Output a markdown table with columns: Report Type | Inherent Risk | Control Strength | Residual Risk | Rationale.
"""
    return _llm_call(prompt, cfg)

def generate_test_script(topic: str, objective: str, steps: List[str], sampling: List[str], evidence: List[str], bcbs: List[int], cfg: LLMConfig) -> str:
    steps_md = "\n".join([f"{i+1}. {s}" for i, s in enumerate(steps)])
    sampling_md = "\n".join([f"- {s}" for s in sampling]) if sampling else "- Define a risk-based sample size and stratify by risk tier or dollar threshold."
    evidence_md = "\n".join([f"- {e}" for e in evidence]) if evidence else "- System logs, reconciliations, case audit trails, and approvals."
    bcbs_alignment_md = ", ".join([f"P{p}-{BCBS239[p].name}" for p in bcbs if p in BCBS239])

    content = TEST_SCRIPT_TEMPLATE.format(
        topic=topic,
        objective=objective,
        steps_md=steps_md,
        sampling_md=sampling_md,
        evidence_md=evidence_md,
        bcbs_alignment_md=bcbs_alignment_md or "P3 Accuracy & Integrity; P4 Completeness; P5 Timeliness"
    )
    return content

def generate_workpaper(title: str, control_id: str, objective: str, scope: str, testing: str, cfg: LLMConfig) -> str:
    content = WORKPAPER_TEMPLATE.format(
        title=title, control_id=control_id, objective=objective, scope=scope, testing=testing,
        results_placeholder="(Do not populate without evidence)",
        conclusion_placeholder="(Avoid audit opinions; state whether control design/operation met criteria)",
        recommendation_placeholder="(Actionable, risk-based recommendation)",
        owner_td_placeholder="(Control owner / Target remediation date)"
    )
    return content

def checklist(name: str) -> List[str]:
    return CHECKLISTS.get(name, [])
