from typing import List, Dict

def generate_rcm(process_name: str, risks: List[str], controls: List[Dict[str, str]]) -> str:
    """
    Returns a markdown Risk/Control Matrix.
    controls: list of dicts with keys: id, description, type (prevent/detect), freq, owner, evidence
    """
    md = [f"**Risk & Control Matrix – {process_name}**\n"]
    md.append("| Risk | Control ID | Control Description | Type | Frequency | Owner | Evidence |")
    md.append("|------|------------|--------------------|------|-----------|-------|----------|")
    for r in risks:
        # map multiple controls to a risk (simple 1:1 or n:1 by naive pairing)
        for c in controls:
            md.append(f"| {r} | {c.get('id','')} | {c.get('description','')} | {c.get('type','')} | {c.get('freq','')} | {c.get('owner','')} | {c.get('evidence','')} |")
    return "\n".join(md)
