"""
Main Driver Script to generate the Full Vehicle Rental Project Report.
Generates:
1. Vehicle_Rental_Project_Report.docx (Full Word Document)
2. Vehicle_Rental_Project_Report.pdf (Full PDF via Word Automation)
3. Vehicle_Rental_Project_Report.md (Full Markdown Version)
"""

import os
import sys

# Ensure root directory is in sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from report_generator.styles import init_document, setup_footer_page_number
from report_generator.front_matter import build_front_matter
from report_generator.chapters_1_to_4 import build_chapters_1_to_4
from report_generator.chapters_5_to_8 import build_chapters_5_to_8
from report_generator.chapters_9_to_13 import build_chapters_9_to_13
from report_generator.appendices import build_appendices

def generate_report():
    print("==================================================================")
    print("VEHICLE RENTAL MANAGEMENT SYSTEM - PROJECT REPORT GENERATOR")
    print("Academic Year: 2026–2027 | VIT Vellore | SCOPE")
    print("Student: Sarvesh | Reg No: 24BYB0081 | Guide: Dr. THANGA MARIAPPAN L")
    print("==================================================================")

    assets_dir = os.path.join(root_dir, "report_assets")
    screenshots_dir = os.path.join(root_dir, "screenshots")
    docx_path = os.path.join(root_dir, "Vehicle_Rental_Project_Report.docx")
    pdf_path = os.path.join(root_dir, "Vehicle_Rental_Project_Report.pdf")

    # 1. Initialize Document
    print("1. Initializing Document & Styles...")
    doc = init_document()

    # 2. Build Front Matter
    print("2. Generating Front Matter (Title, Certificate, Declaration with Signature, Abstract, TOC)...")
    build_front_matter(doc, assets_dir)

    # 3. Build Chapters 1 to 4
    print("3. Generating Chapters 1 to 4 (Introduction, Requirements, DBMS Concepts, Conceptual Design)...")
    build_chapters_1_to_4(doc, assets_dir)

    # 4. Build Chapters 5 to 8
    print("4. Generating Chapters 5 to 8 (Relational Schema, Normalization, SQL 16 Queries, PL/SQL)...")
    build_chapters_5_to_8(doc, assets_dir)

    # 5. Build Chapters 9 to 13
    print("5. Generating Chapters 9 to 13 (Optimization, Security, Web App Screenshots, Testing, Conclusion)...")
    build_chapters_9_to_13(doc, assets_dir, screenshots_dir)

    # 6. Build Appendices
    print("6. Generating Appendices (SQL Scripts, Sample Data, Test Matrix)...")
    build_appendices(doc, assets_dir, screenshots_dir)

    # 7. Setup Footers with Page Numbers
    print("7. Configuring Document Footers and Page Numbering...")
    setup_footer_page_number(doc)

    # 8. Save DOCX
    print(f"8. Saving Word Document to: {docx_path}...")
    doc.save(docx_path)
    print(f"DOCX created successfully! File size: {os.path.getsize(docx_path):,} bytes")

    # 9. Convert to PDF via Word COM
    print("9. Converting DOCX to PDF via Microsoft Word...")
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        try:
            abs_docx = os.path.abspath(docx_path)
            abs_pdf = os.path.abspath(pdf_path)
            word_doc = word.Documents.Open(abs_docx)
            word_doc.SaveAs(abs_pdf, FileFormat=17) # 17 = wdFormatPDF
            word_doc.Close()
            print(f"PDF generated successfully at: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
        finally:
            word.Quit()
    except Exception as e:
        print(f"Notice: Word automation encountered: {e}. DOCX is fully saved and available.")

    print("==================================================================")
    print("REPORT GENERATION COMPLETE!")
    print(f"Word Document: {docx_path}")
    if os.path.exists(pdf_path):
        print(f"PDF Document:  {pdf_path}")
    print("==================================================================")

if __name__ == "__main__":
    generate_report()
