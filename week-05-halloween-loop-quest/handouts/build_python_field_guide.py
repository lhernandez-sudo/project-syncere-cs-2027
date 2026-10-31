from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = Path(__file__).parent
DOCX = OUT / "python-field-guide-editable.docx"
PDF = OUT / "python-field-guide-print-booklet.pdf"

PAGES = [
    ("Python Field Guide", "A beginner lookup guide", [
        ("Use this book while you code", "Look up a pattern, copy its shape, then change the names and values for your program."),
        ("You do not need to memorize everything", "Programmers look up syntax. Your job is to understand what the code is doing and test it."),
        ("Concepts inside", "Variables  Lists  Conditions  For loops  While loops  Functions  return  None"),
    ]),
    ("How to read Python", "Trace one line at a time", [
        ("Assignment", "coins = 3 means store 3 in the name coins. The = sign assigns a value."),
        ("Indentation", "Indented lines belong to the if, loop, or function above them."),
        ("Function call", "print(coins) runs the function named print with coins as its argument."),
        ("Predict then run", "Before you press Run, predict the output. Then compare your prediction with Python."),
    ]),
    ("Variables and lists", "Store one value or a collection", [
        ("Variables", "name = \"Luigi\"\nlives = 3\nis_ready = True"),
        ("Lists", "items = [\"key\", \"star\"]\nitems.append(\"mushroom\")"),
        ("List lookup", "items[0] is the first item. Python starts counting indexes at 0."),
        ("Useful checks", "len(items) counts items.  value in items checks whether a value is present."),
    ]),
    ("Conditions and logic", "Choose which code runs", [
        ("Basic pattern", "if coins >= 10:\n    print(\"1-UP\")\nelse:\n    print(\"Keep going\")"),
        ("Comparisons", "== equal   != not equal   > greater   < less   >= at least   <= at most"),
        ("Logic", "and needs both conditions.  or needs either condition.  not reverses True and False."),
        ("Remember", "Use == to compare. Use = to assign a value."),
    ]),
    ("For loops and range", "Repeat a known number of times", [
        ("Loop through a list", "for enemy in [\"Boo\", \"Goomba\"]:\n    print(enemy)"),
        ("What range means", "range(4) produces 0, 1, 2, 3. It starts at 0 and stops before 4."),
        ("Three useful forms", "range(4) -> 0,1,2,3\nrange(2, 5) -> 2,3,4\nrange(2, 9, 2) -> 2,4,6,8"),
        ("Accumulator", "total = 0\nfor coin in [2, 4, 6]:\n    total = total + coin"),
    ]),
    ("While loops", "Repeat while a condition stays True", [
        ("Basic pattern", "lives = 3\nwhile lives > 0:\n    lives = lives - 1"),
        ("Ask two questions", "What condition keeps the loop running? What changes so the loop can stop?"),
        ("Avoid infinite loops", "If the condition never becomes False, the loop never stops. Update the condition variable inside the loop."),
        ("Choose the loop", "Use for for a list or known count. Use while when repetition depends on a condition."),
    ]),
    ("Functions return and None", "Give reusable code a name", [
        ("Define and call", "def power(base, bonus):\n    return base + bonus\n\nscore = power(7, 5)"),
        ("Vocabulary", "Parameters are names in the definition. Arguments are values sent into the call."),
        ("return", "return sends a value back to the caller. Here, power(7, 5) returns 12."),
        ("None", "None means no value. A function without return still runs, but its result is None."),
        ("Print is different", "print shows text on screen. return gives a value back so the program can reuse it."),
    ]),
    ("Debug and look it up", "A routine for getting unstuck", [
        ("1 Read the error", "The last line usually names the error and points toward the problem."),
        ("2 Check the shape", "Look for missing colons, parentheses, quotes, indentation, or misspelled names."),
        ("3 Trace values", "Use print(variable) to see what a value is during the program."),
        ("4 Test a small piece", "Run one line, one condition, or one function call before testing the whole program."),
        ("Good search", "Search the exact goal: Python add item to list or Python range start stop step."),
        ("Final check", "Can you explain what each variable stores, when each loop stops, and what each function returns?"),
    ]),
]

ACCENT = "2F6FEB"
INK = "172033"
MUTED = "556070"
PALE = "EAF2FF"

def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)

def add_run(p, text, bold=False, size=9, color=INK, font="Aptos"):
    r = p.add_run(text)
    r.bold = bold; r.font.size = Pt(size); r.font.color.rgb = RGBColor.from_string(color)
    r.font.name = font
    r._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), font)
    r._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), font)
    return r

def build_docx():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(5.5), Inches(8.5)
    sec.top_margin = sec.bottom_margin = Inches(.48)
    sec.left_margin = sec.right_margin = Inches(.48)
    styles = doc.styles
    styles["Normal"].font.name = "Aptos"; styles["Normal"].font.size = Pt(9)
    for page_no, (title, subtitle, cards) in enumerate(PAGES, 1):
        if page_no > 1:
            doc.add_page_break()
        p = doc.add_paragraph(); p.style = styles["Title"]; p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        add_run(p, title, True, 20, "000000")
        p.paragraph_format.space_after = Pt(2)
        p = doc.add_paragraph(); add_run(p, subtitle, False, 10, MUTED)
        p.paragraph_format.space_after = Pt(9)
        for heading, body in cards:
            t = doc.add_table(rows=1, cols=1); t.autofit = False; t.columns[0].width = Inches(4.5)
            cell = t.cell(0,0); set_cell_shading(cell, PALE)
            cell.margin_top = cell.margin_bottom = 90; cell.margin_left = cell.margin_right = 110
            p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(3)
            add_run(p, heading, True, 10, ACCENT)
            lines = body.split("\n")
            for i, line in enumerate(lines):
                p = cell.add_paragraph() if i or p.text else p
                p.paragraph_format.space_after = Pt(1)
                is_code = any(x in body for x in [" = ", "def ", "for ", "while ", "if ", "print(", "range(", ".append"])
                add_run(p, line, False, 8.4 if is_code else 8.8, INK, "Consolas" if is_code else "Aptos")
            spacer = doc.add_paragraph(); spacer.paragraph_format.space_after = Pt(3)
        footer = doc.add_paragraph(); footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        add_run(footer, f"PYTHON FIELD GUIDE   {page_no}", True, 7.5, MUTED)
    doc.core_properties.title = "Python Field Guide"
    doc.core_properties.subject = "Beginner Python syntax and concept lookup guide"
    doc.save(DOCX)

def wrap(canvas, text, font, size, width):
    words = text.split(); lines=[]; line=""
    for word in words:
        trial = (line + " " + word).strip()
        if stringWidth(trial, font, size) <= width: line=trial
        else: lines.append(line); line=word
    if line: lines.append(line)
    return lines

def draw_logical_page(c, x0, y0, title, subtitle, cards, page_no):
    w, h = 5.5*72, 8.5*72
    c.setFillColor(white); c.rect(x0,y0,w,h,fill=1,stroke=0)
    c.setFillColor(HexColor("#000000")); c.setFont("Helvetica-Bold",19); c.drawString(x0+34,y0+h-48,title)
    c.setFillColor(HexColor("#556070")); c.setFont("Helvetica",9.5); c.drawString(x0+34,y0+h-65,subtitle)
    y=y0+h-88
    available = y-(y0+36); gap=7
    heights=[]
    for heading, body in cards:
        code = any(k in body for k in [" = ","def ","for ","while ","if ","print(","range(",".append"])
        font="Courier" if code else "Helvetica"; size=7.5 if code else 8
        n=sum(max(1,len(wrap(c,line,font,size,w-82))) for line in body.split("\n"))
        heights.append(28+n*10)
    scale=min(1,available/(sum(heights)+gap*(len(cards)-1)))
    for (heading,body),raw_h in zip(cards,heights):
        ch=raw_h*scale
        c.setFillColor(HexColor("#EAF2FF")); c.roundRect(x0+34,y-ch,w-68,ch,6,fill=1,stroke=0)
        c.setFillColor(HexColor("#2F6FEB")); c.setFont("Helvetica-Bold",9); c.drawString(x0+43,y-15,heading)
        code = any(k in body for k in [" = ","def ","for ","while ","if ","print(","range(",".append"])
        font="Courier" if code else "Helvetica"; size=7.5 if code else 8
        ty=y-28; c.setFont(font,size); c.setFillColor(HexColor("#172033"))
        for source_line in body.split("\n"):
            for line in wrap(c,source_line,font,size,w-86) or [""]:
                c.drawString(x0+43,ty,line); ty-=10*scale
        y-=ch+gap
    c.setFillColor(HexColor("#556070")); c.setFont("Helvetica-Bold",7)
    c.drawRightString(x0+w-34,y0+20,f"PYTHON FIELD GUIDE   {page_no}")

def build_booklet_pdf():
    c=Canvas(str(PDF),pagesize=landscape(letter))
    # Two sheets, ordered for duplex printing on short edge, fold, then staple.
    faces=[(8,1),(2,7),(6,3),(4,5)]
    for left,right in faces:
        draw_logical_page(c,0,0,*PAGES[left-1],left)
        draw_logical_page(c,5.5*72,0,*PAGES[right-1],right)
        c.setStrokeColor(HexColor("#C8CDD5")); c.setDash(2,3); c.line(5.5*72,0,5.5*72,8.5*72); c.setDash()
        c.showPage()
    c.save()

if __name__ == "__main__":
    OUT.mkdir(parents=True,exist_ok=True)
    build_docx(); build_booklet_pdf()
    print(DOCX); print(PDF)
