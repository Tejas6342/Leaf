"""
LeafScan PPT Generator
Creates a PowerPoint presentation from LeafScan documentation and PCL report.
Format matches bcd8903e reference PDF: plain white background, black text,
flowcharts/architecture diagrams allowed in color.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ─── Palette ──────────────────────────────────────────────────────────────────
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BLACK  = RGBColor(0x00, 0x00, 0x00)
GRAY   = RGBColor(0xCC, 0xCC, 0xCC)
# Accent colours ONLY for flowcharts / diagrams / architecture slides
BLUE   = RGBColor(0x1F, 0x4E, 0x79)
LBLUE  = RGBColor(0xBD, 0xD7, 0xEE)
GREEN  = RGBColor(0x37, 0x86, 0x44)
LGREEN = RGBColor(0xC6, 0xEF, 0xCE)
ORANGE = RGBColor(0xED, 0x7D, 0x31)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def new_prs() -> Presentation:
    prs = Presentation()
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def blank_slide(prs: Presentation):
    """Add a completely blank slide with white background."""
    layout = prs.slide_layouts[6]  # blank layout
    slide  = prs.slides.add_slide(layout)
    bg     = slide.background
    fill   = bg.fill
    fill.solid()
    fill.fore_color.rgb = WHITE
    return slide


def add_textbox(slide, left, top, width, height,
                text, font_size=18, bold=False, color=BLACK,
                align=PP_ALIGN.LEFT, wrap=True, italic=False):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf    = txBox.text_frame
    tf.word_wrap = wrap
    p  = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = Pt(font_size)
    run.font.bold  = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def add_title_bar(slide, title_text, subtitle=None):
    """Dark title bar across top of slide."""
    bar = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(0), Inches(0), SLIDE_W, Inches(1.1)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLACK
    bar.line.fill.background()

    # Title text
    tf = bar.text_frame
    tf.word_wrap = True
    p  = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = title_text
    run.font.size  = Pt(28)
    run.font.bold  = True
    run.font.color.rgb = WHITE

    if subtitle:
        add_textbox(slide,
                    Inches(0.5), Inches(1.2),
                    Inches(12.3), Inches(0.5),
                    subtitle, font_size=14, italic=True, color=GRAY)


def add_bullet_content(slide, items, top_start=Inches(1.3),
                       left=Inches(0.6), width=Inches(12.1),
                       font_size=18, bullet_char="•"):
    """Add a list of bullet-point paragraphs."""
    y = top_start
    line_h = Pt(font_size) * 1.6  # approximate line height
    for item in items:
        box_h = Inches(0.42)
        txBox = slide.shapes.add_textbox(left, y, width, box_h)
        tf    = txBox.text_frame
        tf.word_wrap = True
        p  = tf.paragraphs[0]
        run = p.add_run()
        indent = ""
        char   = bullet_char
        if item.startswith("  "):
            indent = "    "
            char   = "◦"
            item   = item.strip()
        run.text = f"{indent}{char} {item}"
        run.font.size  = Pt(font_size)
        run.font.color.rgb = BLACK
        y += line_h.pt * 914  # convert Pt units → EMU rough


def add_rect(slide, left, top, width, height, fill_color, text="",
             font_size=12, text_color=BLACK, bold=False):
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = BLACK
    shape.line.width = Pt(1)
    if text:
        tf = shape.text_frame
        tf.word_wrap = True
        p  = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = text
        run.font.size  = Pt(font_size)
        run.font.bold  = bold
        run.font.color.rgb = text_color
    return shape


def add_arrow(slide, x, y, vertical=True):
    """Simple thin line arrow."""
    if vertical:
        conn = slide.shapes.add_connector(1, x, y, x, y + Inches(0.35))
    else:
        conn = slide.shapes.add_connector(1, x, y, x + Inches(0.5), y)
    conn.line.color.rgb = BLACK
    conn.line.width = Pt(1.5)


# ─── Slides ───────────────────────────────────────────────────────────────────

def slide_title(prs):
    slide = blank_slide(prs)

    # Centre title block
    add_textbox(slide,
                Inches(0.5), Inches(1.5), Inches(12.3), Inches(1.5),
                "LeafScan: A Deep Learning-Based Approach\nfor Plant Leaf Disease Detection Using EfficientNet",
                font_size=32, bold=True, color=BLACK, align=PP_ALIGN.CENTER)

    # Horizontal rule
    line = slide.shapes.add_shape(1, Inches(2), Inches(3.3), Inches(9.3), Inches(0.04))
    line.fill.solid(); line.fill.fore_color.rgb = BLACK
    line.line.fill.background()

    add_textbox(slide, Inches(0.5), Inches(3.5), Inches(12.3), Inches(0.4),
                "Guided By:", font_size=16, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(0.5), Inches(3.9), Inches(12.3), Inches(0.4),
                "Dr. S. Kanithan  |  Department of CSE (AI & ML), JAIN (Deemed-to-be-university)",
                font_size=14, color=BLACK, align=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(0.5), Inches(4.5), Inches(12.3), Inches(0.4),
                "Presented By:", font_size=16, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
    team = ("Abdul Sami  |  Yedhoti Hari Prasad  |  S Dhruva  |  Tejas K  |  Varish Gada\n"
            "Department of CSE (AI & ML), JAIN (Deemed-to-be-university), Karnataka, India")
    add_textbox(slide, Inches(0.5), Inches(4.9), Inches(12.3), Inches(0.6),
                team, font_size=13, color=BLACK, align=PP_ALIGN.CENTER)


def slide_contents(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "CONTENTS")

    items = [
        "Abstract",
        "Introduction",
        "Dataset Description",
        "Data Preprocessing & Augmentation",
        "Model Architecture (EfficientNetB3)",
        "3-Phase Training Strategy",
        "Not-a-Leaf Detection",
        "System Design & Workflow",
        "Performance & Results",
        "Limitations & Future Work",
        "Conclusion",
        "References",
    ]
    y = Inches(1.35)
    for item in items:
        add_textbox(slide, Inches(1.2), y, Inches(11), Inches(0.38),
                    f"❖ {item}", font_size=18, color=BLACK)
        y += Inches(0.44)


def slide_abstract(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "ABSTRACT")

    text = (
        "LeafScan is a full-stack machine learning application that identifies plant leaf diseases from "
        "any photo. It works on images from cameras, the internet, or anywhere — not just dataset images — "
        "and correctly rejects non-leaf inputs.\n\n"
        "Diseases that impact healthy plants are a significant problem for farmers because they lower the "
        "quality and quantity of crops. For good crop management and food security, it is important to "
        "detect these diseases early and accurately.\n\n"
        "The system is built on EfficientNetB3, a deep CNN architecture trained on the PlantVillage dataset "
        "(54,306 images, 39 classes across 14 crops). It achieves 94–96 % test accuracy, runs inference in "
        "20–50 ms on a GPU, and employs a 3-layer rejection mechanism so that non-leaf inputs are "
        "automatically flagged rather than misclassified."
    )
    add_textbox(slide, Inches(0.6), Inches(1.3), Inches(12.1), Inches(5.8),
                text, font_size=17, color=BLACK)


def slide_introduction(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "INTRODUCTION")

    bullets = [
        "Plant diseases cause significant losses in global agricultural yield every year.",
        "Traditional disease identification relies on visual inspection by experts — slow, expensive, unscalable.",
        "Deep learning-based computer vision enables automated, fast, and accurate disease classification.",
        "LeafScan uses EfficientNetB3 (pretrained on ImageNet) fine-tuned on the PlantVillage dataset.",
        "The system detects 38 crop-disease combinations plus a 'not-a-leaf' rejection class (39 total).",
        "Supports real-time inference via a REST API backed by Flask, with an HTML/CSS/JS frontend.",
        "Key design goals: high accuracy, generalisation to real-world photos, robust input validation.",
    ]
    y = Inches(1.35)
    for b in bullets:
        add_textbox(slide, Inches(0.8), y, Inches(11.9), Inches(0.5),
                    f"• {b}", font_size=16, color=BLACK)
        y += Inches(0.53)


def slide_dataset(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "DATASET DESCRIPTION — PlantVillage")

    left_items = [
        "Source: Penn State University (2016)",
        "Images: 54,306 labelled photos of plant leaves",
        "Crops: 14 species (Apple, Tomato, Potato, Corn, Grape, Orange,",
        "  Peach, Pepper, Raspberry, Blueberry, Soybean, Squash,",
        "  Strawberry, Cherry)",
        "Classes: 38 (26 disease + 12 healthy) + 1 custom 'not_a_leaf'",
        "Format: RGB JPG, lab and field conditions",
        "License: CC BY 4.0",
    ]
    right_items = [
        "Dataset Split:",
        "  Train   : 70 %  →  ~38,000 images",
        "  Validation: 15 %  →  ~8,300 images",
        "  Test    : 15 %  →  ~8,300 images",
        "",
        "Limitations:",
        "  – Controlled background (lab conditions)",
        "  – Missing crops: Mango, Rice, Wheat",
        "  – Plain backgrounds differ from real farms",
    ]

    y = Inches(1.35)
    for item in left_items:
        prefix = "  " if item.startswith("  ") else "• "
        add_textbox(slide, Inches(0.6), y, Inches(6.2), Inches(0.42),
                    f"{prefix}{item.strip()}", font_size=15, color=BLACK)
        y += Inches(0.43)

    y = Inches(1.35)
    for item in right_items:
        add_textbox(slide, Inches(7.0), y, Inches(5.8), Inches(0.42),
                    item, font_size=15, color=BLACK)
        y += Inches(0.43)

    # Vertical divider
    div = slide.shapes.add_shape(1, Inches(6.7), Inches(1.3), Inches(0.03), Inches(5.8))
    div.fill.solid(); div.fill.fore_color.rgb = GRAY
    div.line.fill.background()


def slide_model_comparison(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "MODEL COMPARISON")

    add_textbox(slide, Inches(0.6), Inches(1.3), Inches(12), Inches(0.4),
                "Comparison of CNN architectures on ImageNet benchmark:",
                font_size=16, bold=True, color=BLACK)

    # Table header
    cols = ["Model", "Accuracy (ImageNet)", "Parameters", "Speed"]
    col_w = [Inches(3.0), Inches(3.2), Inches(2.8), Inches(2.8)]
    col_x = [Inches(0.6), Inches(3.6), Inches(6.8), Inches(9.6)]
    header_y = Inches(1.85)

    for i, (col, w, x) in enumerate(zip(cols, col_w, col_x)):
        add_rect(slide, x, header_y, w - Inches(0.05), Inches(0.45),
                 BLACK, col, font_size=14, text_color=WHITE, bold=True)

    rows = [
        ("MobileNetV2",   "72.0 %",  "3.4 M",  "Very Fast"),
        ("ResNet50",       "76.1 %",  "25 M",   "Medium"),
        ("VGG16",          "71.0 %",  "138 M",  "Slow"),
        ("EfficientNetB3", "81.6 %",  "12 M",   "Medium"),
        ("EfficientNetB7", "84.3 %",  "66 M",   "Slow"),
    ]
    row_colors = [WHITE, GRAY, WHITE, GRAY, WHITE]

    for r_idx, (row, rc) in enumerate(zip(rows, row_colors)):
        row_y = Inches(2.3) + r_idx * Inches(0.5)
        is_effb3 = row[0] == "EfficientNetB3"
        bg = LBLUE if is_effb3 else rc
        for i, (cell, w, x) in enumerate(zip(row, col_w, col_x)):
            add_rect(slide, x, row_y, w - Inches(0.05), Inches(0.45),
                     bg, cell, font_size=14,
                     text_color=BLACK, bold=is_effb3)

    add_textbox(slide, Inches(0.6), Inches(4.95), Inches(12), Inches(0.5),
                "★  EfficientNetB3 is the sweet spot — highest accuracy/parameter ratio, medium speed, "
                "suitable for GPU & CPU deployment.",
                font_size=14, bold=True, color=BLACK)


def slide_architecture(prs):
    """EfficientNetB3 architecture flowchart — colour allowed."""
    slide = blank_slide(prs)
    add_title_bar(slide, "MODEL ARCHITECTURE — EfficientNetB3")

    boxes = [
        (LBLUE,  "Input Image\n300 × 300 × 3"),
        (LGREEN, "Stem Conv 3×3, stride 2\n→ 150 × 150 × 40"),
        (LGREEN, "MBConv Blocks (7 stages)\nDepthwise Sep. Conv + Squeeze-Excitation"),
        (LGREEN, "Head Conv 1×1\n→ 1536 feature maps"),
        (LGREEN, "Global Average Pooling\n→ 1536-dim vector"),
        (LBLUE,  "Custom Classification Head\nBN → Linear(1536→512)+GELU+Dropout(0.4)\nBN → Linear(512→256)+GELU+Dropout(0.3)"),
        (LBLUE,  "Output Layer\nLinear(256→39)  →  Softmax\n→ 39 class probabilities"),
    ]

    box_w = Inches(5.5)
    box_x = (SLIDE_W - box_w) / 2
    box_h = Inches(0.62)
    gap   = Inches(0.22)
    start_y = Inches(1.25)

    for i, (color, label) in enumerate(boxes):
        y = start_y + i * (box_h + gap)
        add_rect(slide, box_x, y, box_w, box_h, color, label, font_size=12, bold=False)
        if i < len(boxes) - 1:
            arrow_y = y + box_h
            add_arrow(slide, box_x + box_w / 2 - Inches(0.01), arrow_y)


def slide_augmentation(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "DATA PREPROCESSING & AUGMENTATION")

    left_title = "Preprocessing Steps"
    right_title = "Augmentation Techniques"

    add_textbox(slide, Inches(0.6), Inches(1.3), Inches(5.8), Inches(0.4),
                left_title, font_size=17, bold=True, color=BLACK)
    add_textbox(slide, Inches(6.9), Inches(1.3), Inches(5.8), Inches(0.4),
                right_title, font_size=17, bold=True, color=BLACK)

    left = [
        "Resize all images to 300 × 300 pixels",
        "Normalise with ImageNet mean/std",
        "  mean=[0.485, 0.456, 0.406]",
        "  std=[0.229, 0.224, 0.225]",
        "Convert to PyTorch tensor",
    ]
    right = [
        "RandomCrop(300) after Resize(332)",
        "RandomHorizontalFlip",
        "RandomVerticalFlip",
        "ColorJitter (brightness, contrast, saturation)",
        "RandomPerspective(0.2)",
        "GaussianBlur — simulate low-quality cameras",
        "RandomErasing(0.2) — Cutout regularisation",
        "RandomAffine — translate ±10 %",
    ]

    y = Inches(1.8)
    for item in left:
        prefix = "  " if item.startswith("  ") else "• "
        add_textbox(slide, Inches(0.6), y, Inches(5.8), Inches(0.42),
                    f"{prefix}{item.strip()}", font_size=15, color=BLACK)
        y += Inches(0.43)

    y = Inches(1.8)
    for item in right:
        add_textbox(slide, Inches(6.9), y, Inches(5.8), Inches(0.42),
                    f"• {item}", font_size=15, color=BLACK)
        y += Inches(0.43)

    div = slide.shapes.add_shape(1, Inches(6.6), Inches(1.25), Inches(0.03), Inches(5.8))
    div.fill.solid(); div.fill.fore_color.rgb = GRAY
    div.line.fill.background()


def slide_class_balancing(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "CLASS BALANCING & LOSS FUNCTION")

    add_textbox(slide, Inches(0.6), Inches(1.3), Inches(12), Inches(0.4),
                "Class Balancing — WeightedRandomSampler", font_size=18, bold=True, color=BLACK)

    body = (
        "PlantVillage has unequal class sizes. For example, 'Tomato — Healthy' has 1,591 images "
        "while 'Raspberry — Healthy' has only 266. Without balancing, the model ignores rare classes.\n\n"
        "Fix — Weighted Random Sampling:\n"
        "    class_weight = 1.0 / count_per_class\n"
        "    sample_weight = class_weight[label_of_each_image]\n"
        "    sampler = WeightedRandomSampler(sample_weight, replacement=True)\n\n"
        "Every class gets roughly equal representation per epoch regardless of its size."
    )
    add_textbox(slide, Inches(0.6), Inches(1.85), Inches(12), Inches(2.5),
                body, font_size=15, color=BLACK)

    add_textbox(slide, Inches(0.6), Inches(4.4), Inches(12), Inches(0.4),
                "Loss Function — Cross-Entropy with Label Smoothing", font_size=18, bold=True, color=BLACK)
    loss_body = (
        "Standard cross-entropy pushes the model to output exactly 1.0 for the correct class. "
        "Label smoothing (ε = 0.1) distributes a small probability mass across wrong classes, "
        "preventing overconfident predictions and improving generalisation on unseen images."
    )
    add_textbox(slide, Inches(0.6), Inches(4.9), Inches(12), Inches(1.8),
                loss_body, font_size=15, color=BLACK)


def slide_training_strategy(prs):
    """3-Phase Training flowchart — colour allowed."""
    slide = blank_slide(prs)
    add_title_bar(slide, "3-PHASE TRAINING STRATEGY")

    phases = [
        (LBLUE,  "Phase 1 — Backbone Frozen",
         "Only custom head trains.  Backbone retains ImageNet weights.\n"
         "Fast convergence, no risk of destroying pretrained features."),
        (LGREEN, "Phase 2 — Partial Unfreeze",
         "Last 2 MBConv stages unfrozen with low LR (1e-4).\n"
         "Fine-tunes high-level features for plant disease patterns."),
        (LBLUE,  "Phase 3 — Full Unfreeze",
         "Entire network trains end-to-end with very low LR (1e-5).\n"
         "Gradient clipping (max_norm=1.0) prevents exploding gradients."),
    ]

    y = Inches(1.35)
    for color, title, desc in phases:
        box = slide.shapes.add_shape(1, Inches(0.8), y, Inches(11.7), Inches(1.5))
        box.fill.solid(); box.fill.fore_color.rgb = color
        box.line.color.rgb = BLACK; box.line.width = Pt(1)
        tf = box.text_frame; tf.word_wrap = True
        p  = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
        run = p.add_run(); run.text = title
        run.font.size = Pt(16); run.font.bold = True; run.font.color.rgb = BLACK
        para2 = tf.add_paragraph(); para2.alignment = PP_ALIGN.LEFT
        run2 = para2.add_run(); run2.text = desc
        run2.font.size = Pt(14); run2.font.color.rgb = BLACK
        y += Inches(1.65)

    add_textbox(slide, Inches(0.8), Inches(6.7), Inches(11.7), Inches(0.4),
                "Optimizer: AdamW  |  Scheduler: OneCycleLR  |  Mixed Precision: float16 on GPU  (~2× faster)",
                font_size=13, italic=True, color=BLACK)


def slide_not_a_leaf(prs):
    """Not-a-Leaf 3-layer detection flowchart — colour allowed."""
    slide = blank_slide(prs)
    add_title_bar(slide, "NOT-A-LEAF DETECTION — 3-Layer Mechanism")

    layers = [
        (LGREEN, "Layer 1", "predicted_class == 'not_a_leaf'",
         "Model explicitly trained on 1,500 synthetic non-leaf images\n"
         "(solid colours, random noise, gradients, patterns)."),
        (LBLUE,  "Layer 2", "not_a_leaf_probability > 35 %",
         "Even if 'not_a_leaf' is not the top-1 prediction,\n"
         "high probability triggers rejection."),
        (LBLUE,  "Layer 3", "max_confidence < 50 %",
         "If the model isn't confident about any class,\n"
         "it is safer to return 'unknown' than to guess."),
    ]

    y = Inches(1.35)
    for bg, layer_label, rule, explanation in layers:
        # Layer label box
        add_rect(slide, Inches(0.6), y, Inches(1.5), Inches(1.4),
                 BLACK, layer_label, font_size=14, text_color=WHITE, bold=True)
        # Rule box
        add_rect(slide, Inches(2.2), y, Inches(4.5), Inches(1.4),
                 bg, rule, font_size=13, text_color=BLACK, bold=True)
        # Explanation box
        add_rect(slide, Inches(6.8), y, Inches(6.0), Inches(1.4),
                 WHITE, explanation, font_size=13, text_color=BLACK)
        y += Inches(1.65)

    add_textbox(slide, Inches(0.6), Inches(6.4), Inches(12), Inches(0.55),
                "Why 3 layers? Any single layer can be fooled. The combination is robust against adversarial inputs.",
                font_size=14, bold=True, color=BLACK)


def slide_system_design(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "SYSTEM DESIGN")

    add_textbox(slide, Inches(0.6), Inches(1.3), Inches(12), Inches(0.4),
                "System Overview", font_size=18, bold=True, color=BLACK)
    overview = (
        "LeafScan is a full-stack application consisting of three tiers:\n"
        "  1. Frontend  — HTML/CSS/JavaScript web interface\n"
        "  2. Backend   — Flask REST API (Python)\n"
        "  3. ML Engine — EfficientNetB3 inference engine"
    )
    add_textbox(slide, Inches(0.6), Inches(1.8), Inches(12), Inches(1.2),
                overview, font_size=15, color=BLACK)

    cols_title = ["Component", "Technology", "Responsibility"]
    col_w = [Inches(3.5), Inches(3.5), Inches(5.5)]
    col_x = [Inches(0.6), Inches(4.15), Inches(7.7)]

    header_y = Inches(3.1)
    for title, w, x in zip(cols_title, col_w, col_x):
        add_rect(slide, x, header_y, w - Inches(0.05), Inches(0.45),
                 BLACK, title, font_size=14, text_color=WHITE, bold=True)

    rows = [
        ("Frontend", "HTML / CSS / JS", "Image upload, drag-drop, results display"),
        ("Backend",  "Flask (Python)",  "/predict, /predict-url, /health endpoints"),
        ("ML Engine","EfficientNetB3",  "Inference, not-a-leaf detection, confidence scoring"),
        ("Data Store","PlantVillage (54k imgs)", "Training dataset, 39 classes"),
    ]
    row_bgs = [WHITE, GRAY, WHITE, GRAY]
    for r_idx, (row, rb) in enumerate(zip(rows, row_bgs)):
        ry = Inches(3.55) + r_idx * Inches(0.5)
        for cell, w, x in zip(row, col_w, col_x):
            add_rect(slide, x, ry, w - Inches(0.05), Inches(0.45),
                     rb, cell, font_size=13, text_color=BLACK)


def slide_workflow(prs):
    """System workflow flowchart — colour allowed."""
    slide = blank_slide(prs)
    add_title_bar(slide, "WORKFLOW SUMMARY")

    steps = [
        (LBLUE,  "Step 1 — Input",
         "User uploads image via web UI, camera, or URL (JPEG/PNG)"),
        (LGREEN, "Step 2 — Preprocessing",
         "Resize to 300×300, normalise with ImageNet mean/std, convert to tensor"),
        (LGREEN, "Step 3 — Model Inference",
         "EfficientNetB3 produces 39-class probability distribution"),
        (LBLUE,  "Step 4 — Not-a-Leaf Check",
         "3-layer rejection: class == not_a_leaf  OR  P(not_leaf)>35%  OR  max_conf<50%"),
        (LGREEN, "Step 5 — Output",
         "Predicted disease, confidence score, severity level, treatment recommendation"),
    ]

    y = Inches(1.3)
    for color, title, desc in steps:
        box = slide.shapes.add_shape(1, Inches(1.0), y, Inches(11.3), Inches(0.9))
        box.fill.solid(); box.fill.fore_color.rgb = color
        box.line.color.rgb = BLACK; box.line.width = Pt(1)
        tf = box.text_frame; tf.word_wrap = True
        p  = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
        run = p.add_run(); run.text = f"{title}:  "
        run.font.size = Pt(14); run.font.bold = True; run.font.color.rgb = BLACK
        run2 = p.add_run(); run2.text = desc
        run2.font.size = Pt(14); run2.font.color.rgb = BLACK
        if y + Inches(0.9) < Inches(7.0):
            add_arrow(slide, Inches(1.0) + Inches(11.3) / 2, y + Inches(0.9))
        y += Inches(1.12)


def slide_api_endpoints(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "BACKEND — Flask REST API Endpoints")

    cols = ["Endpoint", "Method", "Input", "Use Case"]
    col_w = [Inches(3.0), Inches(1.5), Inches(3.5), Inches(4.8)]
    col_x = [Inches(0.5), Inches(3.5), Inches(5.0), Inches(8.5)]

    header_y = Inches(1.4)
    for title, w, x in zip(cols, col_w, col_x):
        add_rect(slide, x, header_y, w - Inches(0.05), Inches(0.45),
                 BLACK, title, font_size=14, text_color=WHITE, bold=True)

    rows = [
        ("/api/predict",      "POST", "Image file",       "Upload and classify a leaf image"),
        ("/api/predict-url",  "POST", "Image URL",        "Classify image from a URL"),
        ("/api/predict-b64",  "POST", "Base64 string",    "Classify base64-encoded image"),
        ("/api/classes",      "GET",  "—",                "List all 39 supported disease classes"),
        ("/health",           "GET",  "—",                "Server health check / model status"),
    ]
    row_bgs = [WHITE, GRAY, WHITE, GRAY, WHITE]
    for r_idx, (row, rb) in enumerate(zip(rows, row_bgs)):
        ry = Inches(1.85) + r_idx * Inches(0.5)
        for cell, w, x in zip(row, col_w, col_x):
            add_rect(slide, x, ry, w - Inches(0.05), Inches(0.45),
                     rb, cell, font_size=13, text_color=BLACK)

    add_textbox(slide, Inches(0.5), Inches(4.8), Inches(12), Inches(0.4),
                "File Breakdown:", font_size=17, bold=True, color=BLACK)

    files = [
        ("model.py (128 lines)",    "EfficientNetB3 class, freeze/unfreeze methods"),
        ("train.py (385 lines)",    "3-phase training, augmentation, weighted sampler"),
        ("predict.py (318 lines)",  "Inference engine, 3-layer not-a-leaf detection"),
        ("app.py (252 lines)",      "Flask REST API, 5 endpoints"),
        ("evaluate.py (207 lines)", "Test evaluation, confusion matrix, plots"),
        ("frontend/index.html",     "Complete web UI (891 lines)"),
    ]
    y = Inches(5.3)
    for fname, desc in files:
        add_textbox(slide, Inches(0.5), y, Inches(12), Inches(0.38),
                    f"• {fname}  —  {desc}", font_size=14, color=BLACK)
        y += Inches(0.4)


def slide_results(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "PERFORMANCE & RESULTS")

    add_textbox(slide, Inches(0.6), Inches(1.3), Inches(12), Inches(0.4),
                "Overall Performance Metrics", font_size=18, bold=True, color=BLACK)

    metrics = [
        ("Test Accuracy (in-dataset)",  "94 – 96 %"),
        ("Inference Time on T4 GPU",    "20 – 50 ms"),
        ("Inference Time on CPU",       "200 – 500 ms"),
        ("Model File Size",             "~48 MB"),
        ("Training Time on T4",         "~1.5 – 2 hours"),
        ("Not-a-Leaf Rejection Rate",   "> 99 % on synthetic images"),
        ("Parameters",                  "12 M  (vs. VGG16: 138 M)"),
    ]

    col_w = [Inches(6.5), Inches(5.0)]
    col_x = [Inches(0.6), Inches(7.2)]

    header_y = Inches(1.85)
    for title, w, x in zip(["Metric", "Value"], col_w, col_x):
        add_rect(slide, x, header_y, w - Inches(0.1), Inches(0.45),
                 BLACK, title, font_size=14, text_color=WHITE, bold=True)

    row_bgs = [WHITE, GRAY] * 10
    for r_idx, (metric, value) in enumerate(metrics):
        ry = Inches(2.3) + r_idx * Inches(0.5)
        rb = row_bgs[r_idx]
        add_rect(slide, Inches(0.6), ry, Inches(6.4), Inches(0.45), rb, metric, font_size=13)
        add_rect(slide, Inches(7.2), ry, Inches(4.9), Inches(0.45), rb, value, font_size=13, bold=True)

    add_textbox(slide, Inches(0.6), Inches(6.1), Inches(12), Inches(0.7),
                "Key Findings:\n"
                "• Transfer learning greatly improved classification performance.\n"
                "• Balanced dataset (WeightedRandomSampler) lowered prediction bias.\n"
                "• Minimal overfitting observed — lightweight architecture suitable for real-time deployment.",
                font_size=13, color=BLACK)


def slide_limitations(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "LIMITATIONS & FUTURE WORK")

    add_textbox(slide, Inches(0.6), Inches(1.3), Inches(12), Inches(0.4),
                "Current Limitations", font_size=18, bold=True, color=BLACK)
    lims = [
        "Limited to the 14 crop species present in the PlantVillage training dataset.",
        "Performance degrades with very blurry or poorly lit real-world images.",
        "Not-a-Leaf rejection trained on synthetic images — less robust to real non-plant photos.",
        "Missing important crops: Mango, Rice, Wheat.",
        "Controlled lab backgrounds in training data differ from real farm conditions.",
    ]
    y = Inches(1.8)
    for l in lims:
        add_textbox(slide, Inches(0.8), y, Inches(11.9), Inches(0.42),
                    f"• {l}", font_size=15, color=BLACK)
        y += Inches(0.44)

    add_textbox(slide, Inches(0.6), Inches(4.2), Inches(12), Inches(0.4),
                "Future Work", font_size=18, bold=True, color=BLACK)
    future = [
        "Expand dataset to include Mango, Rice, Wheat, Banana and other crops.",
        "Replace synthetic not-a-leaf images with real photos (soil, hands, walls, animals).",
        "Deploy as a mobile app (Android/iOS) for field use by farmers.",
        "Integrate with IoT sensors for real-time continuous field monitoring.",
        "Add Nginx + Gunicorn + Docker for production-grade deployment.",
    ]
    y = Inches(4.7)
    for f in future:
        add_textbox(slide, Inches(0.8), y, Inches(11.9), Inches(0.42),
                    f"• {f}", font_size=15, color=BLACK)
        y += Inches(0.44)


def slide_conclusion(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "CONCLUSION")

    text = (
        "LeafScan is a robust, full-stack deep learning system that accurately detects plant leaf diseases "
        "using the EfficientNetB3 architecture trained on the PlantVillage dataset.\n\n"
        "Key achievements:\n"
        "• Achieved 94–96 % test accuracy across 39 classes (38 disease/healthy + not-a-leaf).\n"
        "• 3-layer not-a-leaf rejection mechanism prevents misclassification of invalid inputs.\n"
        "• 3-phase training strategy prevents catastrophic forgetting of ImageNet features.\n"
        "• WeightedRandomSampler + label smoothing ensure balanced, generalised learning.\n"
        "• Real-time REST API (Flask) with a responsive HTML/CSS/JS frontend.\n"
        "• Model is compact (~48 MB, 12 M parameters) and deployable on CPU or GPU.\n\n"
        "The system demonstrates that transfer learning, careful data augmentation, and class balancing "
        "together deliver high classification accuracy and strong real-world generalisation for automated "
        "plant disease detection — contributing to precision agriculture and food security."
    )
    add_textbox(slide, Inches(0.6), Inches(1.3), Inches(12.1), Inches(5.8),
                text, font_size=16, color=BLACK)


def slide_references(prs):
    slide = blank_slide(prs)
    add_title_bar(slide, "REFERENCES")

    refs = [
        "1. Hughes, D. P., & Salathé, M. (2015). An open access repository of images on plant health to "
           "enable the development of mobile disease diagnostics. arXiv:1511.08060.",
        "2. Tan, M., & Le, Q. V. (2019). EfficientNet: Rethinking model scaling for convolutional neural "
           "networks. Proceedings of ICML 2019.",
        "3. Mohanty, S. P., et al. (2016). Using deep learning for image-based plant disease detection. "
           "Frontiers in Plant Science, 7, 1419.",
        "4. Howard, A., et al. (2019). Searching for MobileNetV3. Proceedings of ICCV 2019.",
        "5. He, K., et al. (2016). Deep residual learning for image recognition. Proceedings of CVPR 2016.",
        "6. Loshchilov, I., & Hutter, F. (2019). Decoupled weight decay regularisation. ICLR 2019.",
        "7. Smith, L. N. (2018). A disciplined approach to neural network hyper-parameters. arXiv:1803.09820.",
        "8. PyTorch Documentation — https://pytorch.org/docs",
        "9. Flask Documentation — https://flask.palletsprojects.com",
        "10. timm library (Ross Wightman) — https://github.com/rwightman/pytorch-image-models",
    ]
    y = Inches(1.3)
    for ref in refs:
        add_textbox(slide, Inches(0.6), y, Inches(12.1), Inches(0.5),
                    ref, font_size=13, color=BLACK)
        y += Inches(0.51)


def slide_thankyou(prs):
    slide = blank_slide(prs)
    add_textbox(slide,
                Inches(0.5), Inches(2.8), Inches(12.3), Inches(1.2),
                "THANK YOU",
                font_size=54, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
    line = slide.shapes.add_shape(1, Inches(2), Inches(4.2), Inches(9.3), Inches(0.04))
    line.fill.solid(); line.fill.fore_color.rgb = BLACK
    line.line.fill.background()
    add_textbox(slide,
                Inches(0.5), Inches(4.4), Inches(12.3), Inches(0.5),
                "LeafScan — Plant Leaf Disease Detection Using EfficientNetB3",
                font_size=18, italic=True, color=BLACK, align=PP_ALIGN.CENTER)


# ─── Main ─────────────────────────────────────────────────────────────────────

def build_ppt(output_path: str):
    prs = new_prs()

    slide_title(prs)
    slide_contents(prs)
    slide_abstract(prs)
    slide_introduction(prs)
    slide_dataset(prs)
    slide_model_comparison(prs)
    slide_architecture(prs)         # diagram / flowchart — colour
    slide_augmentation(prs)
    slide_class_balancing(prs)
    slide_training_strategy(prs)    # diagram / flowchart — colour
    slide_not_a_leaf(prs)           # diagram / flowchart — colour
    slide_system_design(prs)
    slide_workflow(prs)             # flowchart — colour
    slide_api_endpoints(prs)
    slide_results(prs)
    slide_limitations(prs)
    slide_conclusion(prs)
    slide_references(prs)
    slide_thankyou(prs)

    prs.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    build_ppt("/home/runner/work/Leaf/Leaf/LeafScan_Presentation.pptx")
