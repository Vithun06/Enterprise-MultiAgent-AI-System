import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib import colors

def create_full_33_section_case_study(filename="Enterprise_MultiAgent_RAG_Full_CaseStudy.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    PRIMARY = colors.HexColor("#0F172A")
    SECONDARY = colors.HexColor("#2563EB")
    TEXT = colors.HexColor("#334155")
    BG_LIGHT = colors.HexColor("#F8FAFC")

    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=22, leading=26, textColor=PRIMARY, fontName="Helvetica-Bold", spaceAfter=4)
    sub_style = ParagraphStyle('SubTitle', parent=styles['Normal'], fontSize=9.5, leading=13, textColor=SECONDARY, fontName="Helvetica-Bold", spaceAfter=12)
    h1_style = ParagraphStyle('H1', parent=styles['Heading2'], fontSize=12, leading=15, textColor=PRIMARY, fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=6)
    h2_style = ParagraphStyle('H2', parent=styles['Heading3'], fontSize=10, leading=13, textColor=SECONDARY, fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8.5, leading=12, textColor=TEXT, fontName="Helvetica", spaceAfter=6)
    code_style = ParagraphStyle('Code', parent=styles['Code'], fontSize=7.5, leading=9.5, textColor=colors.HexColor("#1E293B"), fontName="Courier")

    elements = []

    # Title Banner
    elements.append(Paragraph("Enterprise Multi-Agent RAG System: Complete Case Study", title_style))
    elements.append(Paragraph("Author: Vithun T R | Version: 1.0.0-PROD | Architecture: Fail-Closed Tri-Agent Engine", sub_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=10))

    # Sections Data Definition
    sections = [
        ("Part 1: Executive Overview & Problem Context", [
            ("1. Executive Summary", "This case study details the design, implementation, and empirical validation of an enterprise-grade Multi-Agent RAG system resolving hallucination, prompt injection, and latency degradation."),
            ("2. Problem Statement", "Standard single-agent RAG pipelines suffer from prompt injection risks in untrusted context, unbounded hallucinations, model deprecation breaks, and high operational latency."),
            ("3. Project Vision & Business Value", "Delivers zero-hallucination knowledge retrieval, deterministic refusal bounds, and sub-3.0s SLA compliance for mission-critical enterprise applications."),
            ("4. Target Architectural Scope", "Features non-blocking similarity search, strict JSON validation guardrails, dynamic model fallback, and chunk-level traceability.")
        ]),
        ("Part 2: System Architecture & Design Strategy", [
            ("5. Multi-Agent Design Pattern", "Employs a tri-agent orchestrator: Agent 1 (Vector Retriever), Agent 2 (Fail-Closed Security Evaluator), and Agent 3 (Grounded Synthesis Engine)."),
            ("6. Agent 1 Spec (Vector Store Retriever)", "ChromaDB dense vector similarity search operating with k=2 top-k chunk retrieval strategy."),
            ("7. Agent 2 Spec (Fail-Closed Security Evaluator)", "Groq LPU QA Verifier enforcing structured JSON validation under strict data-instruction separation boundaries."),
            ("8. Agent 3 Spec (Grounded Synthesis Engine)", "Grounded response synthesis engine constrained strictly to verified context blocks."),
            ("9. Component Interaction & Data Flow", "Query Ingestion -> Chroma Retrieval -> JSON Gate Evaluation -> Decision Enforcement (PASS/REJECT) -> Grounded Synthesis."),
            ("10. Data Protection & Boundary Isolation", "Separates system instructions from retrieved data using explicit <UNTRUSTED_CONTEXT> structural tags.")
        ]),
        ("Part 3: Security & Performance Analytics", [
            ("16. Fail-Closed Gate Design Logic", "Default REJECT initialization ensures security under parsing errors, API timeouts, or ungrounded queries."),
            ("17. Adversarial Threat Modeling", "Defends against Indirect Prompt Injections embedded within vector stores."),
            ("20. Execution Latency Benchmarks", "Valid Query: 2.25s (PASSED) | Adversarial Test: 1.05s (REJECTED) | Out-of-Scope: 0.98s (REJECTED).")
        ])
    ]

    for part_title, part_sections in sections:
        elements.append(Paragraph(part_title, h1_style))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=PRIMARY, spaceAfter=6))
        for sec_num, sec_text in part_sections:
            elements.append(Paragraph(sec_num, h2_style))
            elements.append(Paragraph(sec_text, body_style))
        elements.append(Spacer(1, 4))

    # Benchmark Table
    elements.append(Paragraph("Empirical Latency Matrix", h2_style))
    table_data = [
        [Paragraph("<b>Scenario</b>", body_style), Paragraph("<b>Retrieval</b>", body_style), Paragraph("<b>Guardrail</b>", body_style), Paragraph("<b>Synthesis</b>", body_style), Paragraph("<b>Total</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [Paragraph("Valid Technical Query", body_style), Paragraph("0.12s", body_style), Paragraph("0.85s", body_style), Paragraph("1.28s", body_style), Paragraph("2.25s", body_style), Paragraph("<font color='green'>PASSED</font>", body_style)],
        [Paragraph("Adversarial Injection", body_style), Paragraph("0.11s", body_style), Paragraph("0.94s", body_style), Paragraph("Bypassed", body_style), Paragraph("1.05s", body_style), Paragraph("<font color='red'>REJECTED</font>", body_style)],
    ]
    t = Table(table_data, colWidths=[140, 60, 60, 60, 60, 60])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t)

    doc.build(elements)
    print(f"Full Case Study Generated: {filename}")

if __name__ == "__main__":
    create_full_33_section_case_study()