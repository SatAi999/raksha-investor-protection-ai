import os
import json
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

REPORTS_OUTPUT_DIR = os.path.join("data", "reports")
os.makedirs(REPORTS_OUTPUT_DIR, exist_ok=True)

class ReportGenerator:
    def __init__(self):
        pass

    def generate_pdf_report(self, investigation_data: dict) -> str:
        inv_id = investigation_data.get("investigation_id", "INV-UNKNOWN")
        pdf_path = os.path.join(REPORTS_OUTPUT_DIR, f"{inv_id}_EVIDENCE_REPORT.pdf")

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Custom Styles
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#1E293B')
        )

        subtitle_style = ParagraphStyle(
            'DocSubTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            textColor=colors.HexColor('#64748B')
        )

        section_heading = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#0F172A'),
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#334155')
        )

        bold_label = ParagraphStyle(
            'BoldLabel',
            parent=body_style,
            fontName='Helvetica-Bold'
        )

        story = []

        # Header
        story.append(Paragraph("RAKSHA Investor Scam Intelligence Report", title_style))
        story.append(Paragraph("OFFICIAL EVIDENCE FORENSIC SUMMARY | BEFORE YOU PAY. VERIFY.", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0284C7'), spaceBefore=1, spaceAfter=12))

        # Overview Table
        risk_lvl = investigation_data.get("risk_level", "UNKNOWN")
        risk_color = colors.HexColor('#DC2626') if risk_lvl in ["HIGH", "CRITICAL"] else colors.HexColor('#D97706')

        meta_data = [
            [Paragraph("Investigation ID:", bold_label), Paragraph(inv_id, body_style), Paragraph("Risk Level:", bold_label), Paragraph(f"<b><font color='{risk_color.hexval()}'>{risk_lvl}</font></b>", body_style)],
            [Paragraph("Timestamp:", bold_label), Paragraph(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"), body_style), Paragraph("Calibrated Scam Prob:", bold_label), Paragraph(f"{round(investigation_data.get('risk_probability', 0.0)*100, 1)}%", body_style)],
            [Paragraph("Confidence Score:", bold_label), Paragraph(f"{round(investigation_data.get('confidence', 0.0)*100, 1)}%", body_style), Paragraph("Uncertainty Estimate:", bold_label), Paragraph(f"{round(investigation_data.get('uncertainty', 0.0)*100, 1)}%", body_style)]
        ]

        t_meta = Table(meta_data, colWidths=[110, 160, 120, 150])
        t_meta.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_meta)
        story.append(Spacer(1, 12))

        # Extracted Text Section
        story.append(Paragraph("1. User-Submitted Input Evidence", section_heading))
        user_text = investigation_data.get("input_text", "No text provided.")
        story.append(Paragraph(f"<i>\"{user_text[:500]}\"</i>", body_style))
        story.append(Spacer(1, 10))

        # Authoritative Checks Table
        story.append(Paragraph("2. Authoritative Regulatory & Cybercrime Verification", section_heading))
        sebi_res = investigation_data.get("sebi_verification", {})
        cyber_res = investigation_data.get("cybercrime_verification", {})

        auth_table_data = [
            [Paragraph("Verification Source", bold_label), Paragraph("Claimed Identifier", bold_label), Paragraph("Verification Status", bold_label), Paragraph("Source Type", bold_label)],
            [Paragraph("SEBI Official Intermediary Registry", body_style), Paragraph(investigation_data.get("claims", {}).get("registration_numbers", ["None"])[0] if investigation_data.get("claims", {}).get("registration_numbers") else "N/A", body_style), Paragraph(sebi_res.get("status", "UNAVAILABLE"), body_style), Paragraph("Level 1 Authoritative Fact", body_style)],
            [Paragraph("NCRP Cybercrime Intelligence (I4C)", body_style), Paragraph(investigation_data.get("claims", {}).get("phone_numbers", ["None"])[0] if investigation_data.get("claims", {}).get("phone_numbers") else "N/A", body_style), Paragraph(cyber_res.get("status", "NOT_FOUND"), body_style), Paragraph("Level 2 Authoritative Fact", body_style)]
        ]

        t_auth = Table(auth_table_data, colWidths=[150, 120, 120, 150])
        t_auth.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_auth)
        story.append(Spacer(1, 12))

        # Explainable Reasons
        story.append(Paragraph("3. Explainable Risk Findings", section_heading))
        reasons = investigation_data.get("explainable_reasons", [])
        for idx, r in enumerate(reasons, 1):
            story.append(Paragraph(f"<b>[{r['category']}] {r['signal']}</b> - <i>Source: {r['source']}</i>", bold_label))
            story.append(Paragraph(f"Details: {r['details']}", body_style))
            story.append(Spacer(1, 4))

        story.append(Spacer(1, 10))

        # Protective Guidance
        story.append(Paragraph("4. Protective Safety Action Plan", section_heading))
        story.append(Paragraph(f"<b>RECOMMENDED ACTION:</b> {investigation_data.get('recommended_action', 'PAUSE BEFORE YOU PAY.')}", bold_label))
        story.append(Spacer(1, 6))

        for item in investigation_data.get("safety_do_not_list", []):
            story.append(Paragraph(f"• {item}", body_style))

        story.append(Spacer(1, 16))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#94A3B8'), spaceBefore=6, spaceAfter=6))
        story.append(Paragraph("RAKSHA Non-Commercial Public-Good Safety Infrastructure | Verifiable Digital Evidence Report", subtitle_style))

        doc.build(story)
        print(f"Generated Evidence PDF Report -> {pdf_path}")
        return pdf_path

report_generator = ReportGenerator()
