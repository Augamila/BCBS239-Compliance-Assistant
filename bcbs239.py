from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Principle:
    id: int
    name: str
    focus: str
    examples: List[str]

# A compact, paraphrased reference list for in-app guidance.
BCBS239: Dict[int, Principle] = {
    1: Principle(1, "Governance", "Board/senior mgmt ownership of risk data and reports.",
                 ["Define data governance roles/responsibilities",
                  "Approve risk reporting standards",
                  "Periodic oversight review"]),
    2: Principle(2, "Data architecture & IT", "Scalable, well-documented data architecture for aggregation.",
                 ["Document data models & lineage", "Standardize identifiers", "Change management controls"]),
    3: Principle(3, "Accuracy & integrity", "Accurate, reliable, controlled risk data aggregation.",
                 ["Automated reconciliations", "Validation checks", "Edit/error monitoring"]),
    4: Principle(4, "Completeness", "Capture all critical risk data elements across entities/products.",
                 ["Data element inventory", "Coverage testing", "Gap remediation plans"]),
    5: Principle(5, "Timeliness", "Produce reports quickly enough for effective decision-making.",
                 ["SLA tracking", "Late-report root cause", "Contingency procedures"]),
    6: Principle(6, "Adaptability", "Rapidly produce ad‑hoc reports during stress/crisis.",
                 ["Stress playbooks", "Flexible data marts", "Scenario drill tests"]),
    7: Principle(7, "Accuracy (Reports)", "Reports must be precise and reflect defined metrics.",
                 ["KPI/KRI definitions", "Thresholds & tolerances", "Peer review checkpoints"]),
    8: Principle(8, "Comprehensiveness", "Holistic risk coverage across entities and risk types.",
                 ["Entity/product mapping", "Aggregation by dimension", "Completeness attestations"]),
    9: Principle(9, "Clarity & usefulness", "Audience-tailored, decision‑useful reporting.",
                 ["Executive summaries", "Visualizations", "Plain-language definitions"]),
    10: Principle(10, "Frequency", "Appropriate cadence aligned to risk & regulatory need.",
                 ["Daily liquidity, monthly stress", "Quarterly Y‑14", "Crisis escalations"]),
    11: Principle(11, "Distribution", "Secure, controlled, and timely distribution.",
                 ["Access controls", "Attestation workflow", "Versioning & audit trail"]),
    12: Principle(12, "Review", "Regular assessment of reporting processes.",
                 ["Periodic QA/QC", "Independent testing", "Lessons learned log"]),
    13: Principle(13, "Remedial actions", "Prompt corrective actions and tracking.",
                 ["MAPs with owners/dates", "Effectiveness validation", "Closure evidence"]),
    14: Principle(14, "Supervisory review", "Meet supervisory expectations & address findings.",
                 ["Exam responses", "Sustained remediation", "Ongoing monitoring"]),
}
