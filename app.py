# Add the project's root directory to the Python path
# This ensures that the 'backend' module can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import os
import sys
import streamlit as st
import pandas as pd
from typing import List

from backend.generators import (
    LLMConfig, generate_risk_assessment, generate_test_script, generate_report
)
from backend.rcm import generate_rcm

# ... the rest of your app.py code

from backend.generators import (
    LLMConfig, generate_risk_assessment, generate_test_script, generate_workpaper, checklist
)
from backend.rcm import generate_rcm
from backend.sampling import attribute_sample_size, stratify_by_thresholds
from backend.bcbs239 import BCBS239
from backend.export import export_markdown, export_docx, ensure_dir
from backend.storage import save_project, load_project

st.set_page_config(page_title="Compliance & Regulatory Testing Assistant", page_icon="✅", layout="wide")

st.title("✅ Compliance & Regulatory Testing Assistant Chatbot")
st.caption("BCBS 239 • Independent Testing • Regulatory Reporting • Workpapers")

with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("OpenAI API Key (optional for drafting)", type="password", help="Set to enable LLM drafting. Otherwise templates will be used.")
    model = st.selectbox("Model", ["gpt-4o-mini","gpt-4o","gpt-4.1-mini","gpt-4.1"])
    project = st.text_input("Project Name", value="sample_project")
    if st.button("💾 Save Project"):
        state = st.session_state.get("state_blob", {})
        save_project(project, state)
        st.success(f"Saved project: {project}")
    if st.button("📂 Load Project"):
        st.session_state["state_blob"] = load_project(project)
        st.success(f"Loaded project: {project}")
    st.markdown("---")
    st.write("**BCBS 239 Principles (Quick Reference)**")
    for i in sorted(BCBS239):
        p = BCBS239[i]
        with st.expander(f"P{i} – {p.name}"):
            st.write(p.focus)
            st.write("Examples:")
            st.write("\n".join([f"- {e}" for e in p.examples]))

cfg = LLMConfig(api_key=api_key, model=model)

tabs = st.tabs(["🧭 Risk Assessment","🔍 Test Scripts","📄 Workpapers","📊 RCM & Sampling","📦 Export"])

# ------------------ Risk Assessment Tab ------------------
with tabs[0]:
    st.subheader("🧭 Risk Assessment (Start Here)")
    business_area = st.text_input("Business Area (e.g., Liquidity, AML, Credit Risk)")
    reports = st.text_area("Reports in Scope (comma-separated)", placeholder="FR 2052a, FR Y-14, Call Report, SARs")
    prior_issues = st.text_area("Prior Audit/Exam Issues")
    criteria = st.multiselect("Risk Criteria", ["Regulatory Risk","Operational Complexity","Materiality","Prior Findings","Data Quality History"], default=["Regulatory Risk","Operational Complexity","Materiality"])

    if st.button("Generate Risk Assessment Table"):
        ctx = dict(
            business_area=business_area,
            reports=reports,
            prior_issues=prior_issues,
            criteria=", ".join(criteria) if criteria else "regulatory risk, complexity, materiality",
        )
        output = generate_risk_assessment(ctx, cfg)
        st.markdown(output)
        st.session_state.setdefault("state_blob", {})["risk_assessment"] = output

# ------------------ Test Scripts Tab ------------------
with tabs[1]:
    st.subheader("🔍 Test Script Generator")
    topic = st.text_input("Test Topic", value="AML Transaction Monitoring Controls")
    objective = st.text_area("Control Objective", value="Alerts are investigated within 2 business days.")
    steps = st.text_area("Test Steps (one per line)", value="\n".join([
        "Retrieve alert data for period in scope.",
        "Sample alerts across risk tiers.",
        "Compare alert date vs investigation start date.",
        "Document exceptions beyond 2 business days."
    ]))
    sampling = st.text_area("Sampling Guidance (one per line)", value="Stratify by risk tier\nInclude edge cases and near-threshold items")
    evidence = st.text_area("Expected Evidence (one per line)", value="System alert logs\nCase audit trails\nException reports")
    bcbs_str = st.text_input("BCBS Principles (comma-separated)", value="3,4,5,9")

    if st.button("Build Test Script"):
        step_list = [s.strip() for s in steps.splitlines() if s.strip()]
        sampling_list = [s.strip() for s in sampling.splitlines() if s.strip()]
        evidence_list = [s.strip() for s in evidence.splitlines() if s.strip()]
        bcbs = [int(x.strip()) for x in bcbs_str.split(",") if x.strip().isdigit()]
        md = generate_test_script(topic, objective, step_list, sampling_list, evidence_list, bcbs, cfg)
        st.markdown(md)
        st.session_state.setdefault("state_blob", {})["test_script"] = md

    st.markdown("---")
    st.write("Quick Checklists")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("FR 2052a – Accuracy Checklist"):
            st.write("\n".join([f"- {x}" for x in checklist("fr2052a_accuracy")]))
    with col2:
        if st.button("AML – Sanctions Screening Checklist"):
            st.write("\n".join([f"- {x}" for x in checklist("aml_sanctions_screening")]))

# ------------------ Workpapers Tab ------------------
with tabs[2]:
    st.subheader("📄 Workpaper Builder")
    wp_title = st.text_input("Workpaper Title", value="SAR Control Review")
    control_id = st.text_input("Control ID", value="AML-SAR-002")
    objective = st.text_input("Objective", value="Confirm timely filing of SARs per BSA/FinCEN guidelines.")
    scope = st.text_input("Scope/Period", value="Jan–Mar 2025")
    testing = st.text_area("Testing Performed", value="Reviewed 25 SAR case files for filing timeliness and escalation handling.")

    if st.button("Generate Workpaper"):
        md = generate_workpaper(wp_title, control_id, objective, scope, testing, cfg)
        st.markdown(md)
        st.session_state.setdefault("state_blob", {})["workpaper"] = md

# ------------------ RCM & Sampling Tab ------------------
with tabs[3]:
    st.subheader("📊 Risk & Control Matrix (RCM)")
    process = st.text_input("Process Name", value="Liquidity Reporting – FR 2052a")
    risks = st.text_area("Key Risks (one per line)", value="Incomplete capture of cash flows\nIncorrect product classification\nLate submissions")
    controls_rows = st.text_area("Controls (pipe-separated fields per line)", value="LC-001|Automated reconciliation to GL|Detect|Daily|Liquidity Ops|Reconciliation logs\nLC-002|Lineage documentation review|Prevent|Quarterly|Data Governance|Approved lineage pack")
    if st.button("Build RCM"):
        risks_list = [r.strip() for r in risks.splitlines() if r.strip()]
        controls = []
        for line in controls_rows.splitlines():
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 6:
                controls.append({"id":parts[0],"description":parts[1],"type":parts[2],"freq":parts[3],"owner":parts[4],"evidence":parts[5]})
        md = generate_rcm(process, risks_list, controls)
        st.markdown(md)
        st.session_state.setdefault("state_blob", {})["rcm"] = md

    st.markdown("---")
    st.subheader("📐 Sampling Helper")
    pop = st.number_input("Population Size", min_value=1, value=500)
    eer = st.number_input("Expected Exception Rate (0-1)", min_value=0.0, max_value=1.0, value=0.05)
    prec = st.number_input("Precision (0-1)", min_value=0.01, max_value=0.5, value=0.05)
    if st.button("Plan Sample Size"):
        n = attribute_sample_size(pop, eer, prec, 0.95)
        st.success(f"Planned sample size (approx.): {n}")

# ------------------ Export Tab ------------------
with tabs[4]:
    st.subheader("📦 Export Outputs")
    export_dir = st.text_input("Export Directory", value="exports")
    fname = st.text_input("Base File Name", value="compliance_package")
    to_export = st.multiselect("Include", ["risk_assessment","test_script","workpaper","rcm"], default=["risk_assessment","test_script","workpaper","rcm"])
    if st.button("Export Files"):
        ensure_dir(os.path.join(export_dir, "dummy"))
        blob = st.session_state.get("state_blob", {})
        md_bundle = []
        for key in to_export:
            if key in blob:
                md_bundle.append(f"## {key.replace('_',' ').title()}\n\n{blob[key]}\n")
        if not md_bundle:
            st.warning("Nothing to export yet.")
        else:
            md_text = "\n\n---\n\n".join(md_bundle)
            md_path = os.path.join(export_dir, f"{fname}.md")
            docx_path = os.path.join(export_dir, f"{fname}.docx")
            export_markdown(md_text, md_path)
            export_docx(md_text, docx_path)
            st.success(f"Exported:\n- {md_path}\n- {docx_path}")
            st.download_button("⬇️ Download Markdown", data=md_text.encode("utf-8"), file_name=f"{fname}.md")
