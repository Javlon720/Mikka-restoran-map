from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import os

def create_card(slide, left, top, width, height, bg_color, border_color=None):
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_clean_textbox(slide, left, top, width, height, text, font_size, font_color, bold=False, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_top = Inches(0.05)
    tf.margin_bottom = Inches(0.05)
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.name = 'MS Gothic'
    p.font.color.rgb = font_color
    p.alignment = align
    return tf

def rebuild_self_intro():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Colors (Slate Dark style)
    bg_color = RGBColor(15, 23, 42)
    card_color = RGBColor(30, 41, 59)
    text_white = RGBColor(241, 245, 249)
    text_gray = RGBColor(148, 163, 184)
    accent_indigo = RGBColor(99, 102, 241)
    accent_amber = RGBColor(245, 158, 11)
    
    blank_layout = prs.slide_layouts[6]
    
    # ----------------------------------------------------
    # SLIDE 1: Title (自己紹介)
    # ----------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    slide1.background.fill.solid()
    slide1.background.fill.fore_color.rgb = bg_color
    
    # Accent decoration
    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.2), Inches(0.15), Inches(3.0))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = accent_indigo
    accent_bar.line.fill.background()
    
    txBox = slide1.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.5), Inches(3.0))
    tf = txBox.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "自己紹介 (Self-Introduction)"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.name = 'MS Gothic'
    p1.font.color.rgb = text_white
    p1.space_after = Pt(12)
    
    p2 = tf.add_paragraph()
    p2.text = "アブドゥラエフ・ジャブロン (Abdullayev Javlon)"
    p2.font.size = Pt(22)
    p2.font.name = 'MS Gothic'
    p2.font.color.rgb = accent_amber
    p2.space_after = Pt(20)
    
    p3 = tf.add_paragraph()
    p3.text = "Japan Digital University (JDU) / コンピュータ工学専攻\nウズベキスタン世界言語大学 / コンピュータ言語学専攻"
    p3.font.size = Pt(14)
    p3.font.name = 'MS Gothic'
    p3.font.color.rgb = text_gray
    
    # ----------------------------------------------------
    # SLIDE 2: Strength 1 (強み1：Web開発力)
    # ----------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    slide2.background.fill.solid()
    slide2.background.fill.fore_color.rgb = bg_color
    
    add_clean_textbox(slide2, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), "私の強み①：フルスタックなWeb開発力", 28, accent_indigo, bold=True)
    
    create_card(slide2, Inches(1.0), Inches(1.5), Inches(11.3), Inches(5.0), card_color)
    tf = add_clean_textbox(slide2, Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.4), "■ システム開発の技術と経験", 20, text_white, bold=True)
    
    points_s2 = [
        "",
        "・得意な技術スタック",
        "  JavaScript, Node.js, TypeScript, PostgreSQL, React, Vite, Fastify, GitHub",
        "",
        "・コワーク授業での開発実績：飲食店口コミサイト『Mikka（ミッカ）』の構築",
        "  - 地図（Leaflet.js）と店舗情報を連動させ、場所から飲食店を探せる機能を実装しました。",
        "  - Google Gemini APIを搭載し、最新店舗データをもとにおすすめ店舗を推薦するAIを開発しました。",
        "  - 日本語・ウズベク語・英語・ロシア語に対応した多言語切り替え機能を実装しました。",
        "  - パスワードのハッシュ化（bcryptjs）と安全なJWTセッション管理（HTTP-only Cookie）を行いました。"
    ]
    for b in points_s2:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(12) if b.startswith("  ") else Pt(13)
        p.font.color.rgb = text_gray if b.startswith("  ") else text_white
        p.font.name = 'MS Gothic'
        if b.startswith("・") or b.startswith("■"):
            p.font.bold = True
            
    # ----------------------------------------------------
    # SLIDE 3: Strength 2 (強み2：日本語・デザイン)
    # ----------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    slide3.background.fill.solid()
    slide3.background.fill.fore_color.rgb = bg_color
    
    add_clean_textbox(slide3, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), "私の強み②：日本語コミュニケーション ✕ デザイン表現力", 28, accent_indigo, bold=True)
    
    create_card(slide3, Inches(1.0), Inches(1.5), Inches(11.3), Inches(5.0), card_color)
    tf = add_clean_textbox(slide3, Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.4), "■ 言語とビジュアル表現を組み合わせた実績", 20, text_white, bold=True)
    
    points_s3 = [
        "",
        "・日本語コミュニケーション能力",
        "  日本語能力試験（JLPT）N3に合格し、現在はN2の勉強を進めています。日本語での会話が大好きです。",
        "",
        "・豊富なグラフィックデザイン実務経験",
        "  JDUおよびIT企業でデザイナーとして、日本向けに輸出されるTシャツデザインを1,000件以上作成しました。",
        "  日本のパートナーと日本語でコミュニケーションを取りながら、デザイン制作や生産管理を行いました。",
        "",
        "・分かりやすく伝える教育スキル",
        "  日本語教師として、他校で20名以上の学生（子供から大人）に日本語（N5レベル）を教えた経験があります。"
    ]
    for b in points_s3:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(12) if b.startswith("  ") else Pt(13)
        p.font.color.rgb = text_gray if b.startswith("  ") else text_white
        p.font.name = 'MS Gothic'
        if b.startswith("・") or b.startswith("■"):
            p.font.bold = True

    # ----------------------------------------------------
    # SLIDE 4: Future Goal (将来の目標)
    # ----------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    slide4.background.fill.solid()
    slide4.background.fill.fore_color.rgb = bg_color
    
    add_clean_textbox(slide4, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), "将来の目標", 28, accent_indigo, bold=True)
    
    create_card(slide4, Inches(1.0), Inches(1.5), Inches(11.3), Inches(5.0), card_color)
    tf = add_clean_textbox(slide4, Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.4), "■ ブリッジシステムエンジニアとしての活躍", 20, text_white, bold=True)
    
    points_s4 = [
        "",
        "・日本とウズベキスタンを繋ぐ『ブリッジエンジニア』",
        "  私の強みである『Web開発技術』と『日本語コミュニケーション』、そして『デザイン表現力』を活かして、",
        "  日本企業と海外開発拠点を繋ぐエンジニアになりたいと考えています。",
        "",
        "・ユーザーに優しいグローバルプロダクトの創出",
        "  高いUXデザインとセキュリティを備えた、世界中で使われる使いやすいWebサービスを作りたいです。",
        "",
        "・常に学び続ける姿勢",
        "  AI連携やモダンな設計（クリーンアーキテクチャ等）など、最新の技術を勉強し続け、組織の成長に貢献します。"
    ]
    for b in points_s4:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(12) if b.startswith("  ") else Pt(13)
        p.font.color.rgb = text_gray if b.startswith("  ") else text_white
        p.font.name = 'MS Gothic'
        if b.startswith("・") or b.startswith("■"):
            p.font.bold = True

    # ====================================================
    # 全4スライドへ N3レベル・ます形のスピーカーノートを流し込む
    # ====================================================
    self_intro_notes = [
        "【発表原稿（スライド1）】[N3レベル・ます形] ※制限時間：30秒〜45秒\n"
        "はじめまして。アブドゥラエフ・ジャブロンと申します。本日はよろしくお願いいたします。\n"
        "私は現在、ウズベキスタン世界言語大学でコンピュータ言語学を勉強しています。同時に、JDU（Japan Digital University）でコンピュータエンジニアリングを専攻しています。また、産業能率大学でビジネスも勉強しました。\n"
        "将来は日本やグローバル企業で、ソフトウェアエンジニアとして働きたいと考えています。\n"
        "本日は、私の強みを2点、お話しさせていただきます。",
        
        "【発表原稿（スライド2）】[N3レベル・ます形] ※制限時間：60秒\n"
        "私の強みの1つ目は、『自分でWebシステムを作る力』です。\n"
        "私はJavaScriptやNode.js、PostgreSQLを使った開発が得意です。\n"
        "最近のコワーク授業では、レストランの口コミサイト『Mikka（ミッカ）』を自分で作りました。\n"
        "このサイトでは、地図で行きたい店を探したり、GeminiのAIチャットを使っておすすめの店を聞いたりすることができます。フロントエンドからバックエンドまで、一人で工夫して開発を行いました。",
        
        "【発表原稿（スライド3）】[N3レベル・ます形] ※制限時間：60秒\n"
        "強みの2つ目は、『日本語でのコミュニケーション力とデザインの経験』です。\n"
        "私の日本語レベルはN3で、現在はN2の勉強をしています。日本語で話すことが大好きです。\n"
        "これまでJDUでグラフィックデザイナーとして働き、日本のパートナーと日本語で連絡を取りながら、日本向けのTシャツデザインを1,000件以上作りました。また、日本語の先生として、20人以上の生徒に日本語を教えた経験もあります。",
        
        "【発表原稿（スライド4）】[N3レベル・ます形] ※制限時間：30秒〜45秒\n"
        "最後に、私の将来の目標についてです。\n"
        "将来は、この『Web開発 of 技術』『デザイン of 経験』、そして『日本語力』を活かして、日本とウズベキスタンを繋ぐブリッジシステムエンジニアとして、人の役に立つシステムを作りたいです。\n"
        "本日は私のことを知っていただけるよう、一生懸命話します。ありがとうございました。どうぞよろしくお願いいたします。"
    ]
    
    for i, slide in enumerate(prs.slides):
        if i < len(self_intro_notes):
            slide.notes_slide.notes_text_frame.text = self_intro_notes[i]
            
    ppt_out = "/Users/macbook-projavlon/Desktop/JDU_bitiruv/employability/7_自己紹介プレゼン資料.pptx"
    prs.save(ppt_out)
    print("Rebuilt 7_自己紹介プレゼン資料.pptx in Gamma Widescreen Dark Slate style successfully!")

if __name__ == "__main__":
    rebuild_self_intro()
