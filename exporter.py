from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors
import io
import re

class DocumentExporter:
    @staticmethod
    def export_docx(paper_data):
        doc = Document()
        
        # Style configuration
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Times New Roman'
        font.size = Pt(12)

        # Title
        title_para = doc.add_paragraph(paper_data.get('Title', 'Untitled Paper'))
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_run = title_para.runs[0]
        title_run.bold = True
        title_run.font.size = Pt(18)
        
        # Authors
        if 'Authors' in paper_data:
            auth_para = doc.add_paragraph(paper_data['Authors'])
            auth_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            auth_para.runs[0].italic = True

        doc.add_paragraph() # Spacer

        # Sections
        sections = [
            'Abstract', 'Introduction', 'Literature Review', 
            'Methodology', 'Results and Discussion', 
            'Future Work', 'Conclusion', 'References'
        ]

        for sec in sections:
            if sec in paper_data and paper_data[sec]:
                # Heading
                h = doc.add_paragraph(sec.upper())
                h.alignment = WD_ALIGN_PARAGRAPH.LEFT
                hr = h.runs[0]
                hr.bold = True
                hr.font.size = Pt(14)
                
                # Content
                content = paper_data[sec]
                # Simple markdown cleanup for DOCX
                content = content.replace('**', '').replace('##', '')
                
                p = doc.add_paragraph(content)
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                
                doc.add_paragraph()

        bio = io.BytesIO()
        doc.save(bio)
        return bio.getvalue()

    @staticmethod
    def export_pdf(paper_data):
        bio = io.BytesIO()
        doc = SimpleDocTemplate(bio, pagesize=A4,
                                rightMargin=40, leftMargin=40,
                                topMargin=40, bottomMargin=40)
        
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Times-Roman', fontSize=12, leading=14))
        styles.add(ParagraphStyle(name='CenterTitle', alignment=TA_CENTER, fontName='Times-Bold', fontSize=18, leading=22))
        styles.add(ParagraphStyle(name='SectionHeader', alignment=TA_LEFT, fontName='Times-Bold', fontSize=14, leading=18, spaceBefore=10, spaceAfter=5))
        styles.add(ParagraphStyle(name='AuthorStyle', alignment=TA_CENTER, fontName='Times-Italic', fontSize=11))

        flowables = []

        # Title
        flowables.append(Paragraph(paper_data.get('Title', 'Untitled'), styles['CenterTitle']))
        flowables.append(Spacer(1, 12))
        
        # Authors
        if 'Authors' in paper_data:
            flowables.append(Paragraph(paper_data['Authors'], styles['AuthorStyle']))
            flowables.append(Spacer(1, 12))

        sections = [
            'Abstract', 'Introduction', 'Literature Review', 
            'Methodology', 'Results and Discussion', 
            'Future Work', 'Conclusion', 'References'
        ]

        for sec in sections:
            if sec in paper_data and paper_data[sec]:
                flowables.append(Paragraph(sec.upper(), styles['SectionHeader']))
                
                text = paper_data[sec]
                # Basic Markdown handling for ReportLab
                text = text.replace('\n', '<br/>')
                # Handle bolding from markdown
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
                
                flowables.append(Paragraph(text, styles['Justify']))
                flowables.append(Spacer(1, 12))

        doc.build(flowables)
        return bio.getvalue()
