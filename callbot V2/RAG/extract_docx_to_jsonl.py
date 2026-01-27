import json
import re
from pathlib import Path
from docx import Document

Q_RE = re.compile(r"^\s*(Q[A-Z]?\d+)\s*[-–]\s*(.+?)\s*$", re.IGNORECASE)
SECTION_RE = re.compile(r"^\s*SECTION\s*(\d+)?\s*[-–:]?\s*(.+?)\s*$", re.IGNORECASE)
URL_RE = re.compile(r"(https?://[^\s)]+)")

def clean_lines(lines):
    out = []
    for x in lines:
        x = (x or "").strip()
        if not x:
            continue
        out.append(x)
    return out

def extract_source_url(text_lines):
    for line in reversed(text_lines):
        if "Source officielle" in line or "Source" in line:
            m = URL_RE.search(line)
            if m:
                return m.group(1)
    for line in reversed(text_lines):
        m = URL_RE.search(line)
        if m and "cnp.fr" in m.group(1):
            return m.group(1)
    return ""

def main():
    in_path = Path(r"C:\Users\DELL\Desktop\cnp_faq_scraper\CNP_FAQ_COMPLETE_68_QUESTIONS.docx")
    out_path = Path("data/kb.jsonl")
    doc = Document(str(in_path))

    current_section = ""
    current_id = None
    current_question = None
    buffer = []

    items = []

    def flush():
        nonlocal current_id, current_question, buffer, current_section, items
        if not current_id or not current_question:
            buffer = []
            return
        lines = clean_lines(buffer)
        source_url = extract_source_url(lines)
        answer = "\n".join(lines).strip()

        items.append({
            "id": current_id,
            "section": current_section,
            "question": current_question.strip(),
            "answer": answer,
            "source_url": source_url
        })
        buffer = []

    for p in doc.paragraphs:
        text = (p.text or "").strip()
        if not text:
            continue

        style = p.style.name if p.style else ""
        
        # Check for SECTION in Heading 1
        if style == "Heading 1":
            msec = SECTION_RE.match(text)
            if msec:
                section_num = msec.group(1) or ""
                section_name = msec.group(2).strip()
                current_section = f"{section_num} - {section_name}" if section_num else section_name
                continue

        # Check for Questions in Heading 2
        if style == "Heading 2":
            mq = Q_RE.match(text)
            if mq:
                flush()
                current_id = mq.group(1).upper()
                current_question = mq.group(2).strip()
                continue

        buffer.append(text)

    flush()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    print(f"OK: wrote {len(items)} items -> {out_path}")

if __name__ == "__main__":
    main()
