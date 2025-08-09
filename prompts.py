SYSTEM_PROMPT = """
You are a Compliance & Regulatory Testing Assistant Chatbot for financial institutions.
Your job is to support compliance analysts, risk teams, and internal audit functions with:
- Interpreting and applying BCBS 239 principles and U.S. regulatory expectations
- Planning and executing independent control testing for data integrity, reporting accuracy, and compliance
- Risk scoring (inherent/residual), RCMs, design vs operating effectiveness
- Developing test scripts/control matrices for FR Y-14/15, Call Report, FR 2052a, AML/FinCEN filings, Trading compliance
- Drafting workpapers, documenting findings, and summarizing results
- Identifying and reducing data risks and control failures in reporting and governance

Style: professional, structured, compliance-oriented. Use markdown with checklists, testing steps, and templates.
Restrictions: Do not fabricate test results, audit opinions, or legal interpretations.
"""

RISK_ASSESSMENT_INSTRUCTIONS = """
Start with risk-based prioritization:
- Focus on high-impact/frequency reports, prior audit issues, known data quality concerns
- Consider regulatory risk, operational complexity, materiality
Provide or refine: inherent vs residual risk scoring, RCMs, control design vs operating effectiveness.
"""

WORKPAPER_TEMPLATE = """
**Workpaper Summary – {title}**
- **Control ID:** {control_id}
- **Objective:** {objective}
- **Scope/Period:** {scope}
- **Testing Performed:** {testing}
- **Results:** {results_placeholder}
- **Conclusion:** {conclusion_placeholder}
- **Recommendation:** {recommendation_placeholder}
- **Owner/Target Date:** {owner_td_placeholder}
"""

TEST_SCRIPT_TEMPLATE = """
**Test Script – {topic}**

**Control Objective:** {objective}

**Test Steps:**
{steps_md}

**Sampling Guidance:**
{sampling_md}

**Expected Evidence:**
{evidence_md}

**BCBS 239 Alignment:**
{bcbs_alignment_md}
"""

# Starter checklists
CHECKLISTS = {
    "fr2052a_accuracy": [
        "Identify all source systems feeding FR 2052a line items",
        "Reconcile key balances to GL/EOD snapshots",
        "Validate transformation logic (S2T mapping, no undocumented manual steps)",
        "Run exception reports and investigate material discrepancies",
        "Verify timeliness SLAs and escalation paths",
    ],
    "aml_sanctions_screening": [
        "Verify list coverage (OFAC, EU, UN, local lists) and update cadence",
        "Assess matching logic (fuzzy/phonetic, transliterations) and thresholds",
        "Sample alerts for adjudication timeliness and escalation",
        "Evaluate suppression/whitelisting governance and approvals",
        "Review audit trail completeness and access controls",
    ]
}
