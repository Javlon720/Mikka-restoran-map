from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import os

def create_card(slide, left, top, width, height, bg_color, border_color=None):
    """Creates a rounded rectangle shape to serve as a card for text content."""
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background() # No border
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

ppt_path = "/Users/macbook-projavlon/Desktop/JDU_bitiruv/cowork/Mikka_Presentation.pptx"
img_dir = "/Users/macbook-projavlon/Desktop/JDU_bitiruv/cowork"

def rebuild_cowork_presentation():
    prs = Presentation()
    
    # Set to 16:9 Widescreen standard sizes
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Color palette (Gamma Slate Dark style)
    bg_color = RGBColor(15, 23, 42)       # Slate-900 (Deep dark slate background)
    card_color = RGBColor(30, 41, 59)     # Slate-800 (Slightly lighter card background)
    text_white = RGBColor(241, 245, 249)  # Slate-100 (Bright text)
    text_gray = RGBColor(148, 163, 184)   # Slate-400 (Muted description)
    accent_indigo = RGBColor(99, 102, 241) # Indigo-500 (Primary accent)
    accent_amber = RGBColor(245, 158, 11)  # Amber-500 (Secondary accent)
    
    blank_layout = prs.slide_layouts[6]
    
    # ----------------------------------------------------
    # SLIDE 1: Title (表紙)
    # ----------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    slide1.background.fill.solid()
    slide1.background.fill.fore_color.rgb = bg_color
    
    # Left accent design block
    accent_bar = slide1.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.2), Inches(0.15), Inches(3.0)
    )
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = accent_indigo
    accent_bar.line.fill.background()
    
    txBox = slide1.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.5), Inches(3.0))
    tf = txBox.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "飲食店口コミサイト「Mikka」"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.name = 'MS Gothic'
    p1.font.color.rgb = text_white
    p1.space_after = Pt(12)
    
    p2 = tf.add_paragraph()
    p2.text = "プロジェクト概要と技術構成"
    p2.font.size = Pt(22)
    p2.font.name = 'MS Gothic'
    p2.font.color.rgb = accent_amber
    p2.space_after = Pt(20)
    
    p3 = tf.add_paragraph()
    p3.text = "アブドゥラエフ・ジャブロン (Abdullayev Javlon)\nJapan Digital University (JDU) / ソフトウェアエンジニアリング"
    p3.font.size = Pt(14)
    p3.font.name = 'MS Gothic'
    p3.font.color.rgb = text_gray
    
    # ----------------------------------------------------
    # SLIDE 2: Purpose (目的)
    # ----------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    slide2.background.fill.solid()
    slide2.background.fill.fore_color.rgb = bg_color
    
    # Slide Title
    add_clean_textbox(slide2, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), "1. プロジェクトの目的", 28, accent_indigo, bold=True)
    
    # Layout 2 Columns using cards
    # Column 1 Card (Goal)
    create_card(slide2, Inches(1.0), Inches(1.5), Inches(5.4), Inches(5.0), card_color)
    tf1 = add_clean_textbox(slide2, Inches(1.3), Inches(1.8), Inches(4.8), Inches(4.4), "■ 開発の目的と価値", 20, text_white, bold=True)
    bullets_p1 = [
        "",
        "・誰でも使いやすい飲食店共有プラットフォーム",
        "  地域のレストラン情報を多言語で共有し、",
        "  簡単に美味しい店を見つけられるシステムです。",
        "",
        "・言葉の壁を越える価値",
        "  観光客や日本からの滞在者が、自分の言語で",
        "  口コミを読んだり書いたりできる環境を作ります。",
        "",
        "・直感的なマップ連携",
        "  行きたいお店を地図から視覚的に探せます。"
    ]
    for b in bullets_p1:
        p = tf1.add_paragraph()
        p.text = b
        p.font.size = Pt(13) if b.startswith("  ") else Pt(14)
        p.font.color.rgb = text_gray if b.startswith("  ") else text_white
        p.font.name = 'MS Gothic'
        
    # Column 2 Card (Target / Design)
    create_card(slide2, Inches(6.9), Inches(1.5), Inches(5.4), Inches(5.0), card_color)
    tf2 = add_clean_textbox(slide2, Inches(7.2), Inches(1.8), Inches(4.8), Inches(4.4), "■ ターゲットとUX方針", 20, text_white, bold=True)
    bullets_p2 = [
        "",
        "・幅広いターゲットユーザー",
        "  地元のウズベキスタン人から、日本人の駐在員、",
        "  さらに海外からの観光客までをカバーします。",
        "",
        "・モダンで魅力的なUIデザイン",
        "  半透明のGlassmorphismデザインを取り入れ、",
        "  使うのが楽しくなるWeb画面を目指しました。",
        "",
        "・アクセシビリティの配慮",
        "  フォントの大きさや色のコントラストを調整し、",
        "  読みやすさを追求しました。"
    ]
    for b in bullets_p2:
        p = tf2.add_paragraph()
        p.text = b
        p.font.size = Pt(13) if b.startswith("  ") else Pt(14)
        p.font.color.rgb = text_gray if b.startswith("  ") else text_white
        p.font.name = 'MS Gothic'
        
    # ----------------------------------------------------
    # SLIDE 3: Features (主な機能)
    # ----------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    slide3.background.fill.solid()
    slide3.background.fill.fore_color.rgb = bg_color
    add_clean_textbox(slide3, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), "2. 主な機能", 28, accent_indigo, bold=True)
    
    # 3 Column layout cards
    col_width = Inches(3.5)
    gap = Inches(0.4)
    features = [
        ("ユーザー認証 ＆ 評価", "• セキュアなログインと登録\n• 5段階の星評価と詳細コメント\n• 口コミ時の画像アップロード"),
        ("多言語 ＆ マップ連携", "• 4言語対応 (日・ウズ・英・露)\n• Leaflet.jsを用いた動的地図\n• 地図と店舗カードの双方向連動"),
        ("Mikka AI Assistant", "• Gemini APIによるチャット機能\n• 最新店舗データを用いた推薦\n• クイックリプライによる簡単入力")
    ]
    
    for i, (title, desc) in enumerate(features):
        left = Inches(1.0) + i * (col_width + gap)
        create_card(slide3, left, Inches(1.8), col_width, Inches(4.5), card_color)
        
        # Circle badge for number
        badge = slide3.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.3), Inches(2.1), Inches(0.6), Inches(0.6))
        badge.fill.solid()
        badge.fill.fore_color.rgb = accent_indigo
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.paragraphs[0].text = str(i+1)
        tf_b.paragraphs[0].font.size = Pt(16)
        tf_b.paragraphs[0].font.bold = True
        tf_b.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        tf = add_clean_textbox(slide3, left + Inches(0.3), Inches(2.9), col_width - Inches(0.6), Inches(3.2), title, 18, text_white, bold=True)
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(13)
        p.font.color.rgb = text_gray
        p.font.name = 'MS Gothic'
        p.space_before = Pt(12)
        
    # ----------------------------------------------------
    # SLIDE 4: Architecture (システム構成)
    # ----------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    slide4.background.fill.solid()
    slide4.background.fill.fore_color.rgb = bg_color
    add_clean_textbox(slide4, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), "3. システム構成 (モノレポ)", 28, accent_indigo, bold=True)
    
    # 2x2 Grid of small cards
    card_w = Inches(5.4)
    card_h = Inches(2.2)
    components = [
        (Inches(1.0), Inches(1.5), "フロントエンド", "HTML5 / CSS3 / Vanilla JavaScript\nフレームワークを使わないことで、ページの表示速度を大幅に高めています。", accent_indigo),
        (Inches(6.9), Inches(1.5), "バックエンド", "TypeScript / Fastify / Clean Architecture\nTypeScriptで堅牢に、Fastifyで超高速なAPIサーバーを実現しました。", accent_indigo),
        (Inches(1.0), Inches(4.1), "データベース", "PostgreSQL\n頑丈なリレーショナルデータ構造により、ユーザー情報や店舗、レビューを安全に管理します。", accent_amber),
        (Inches(6.9), Inches(4.1), "リポジトリ構成", "NPM Workspaces によるモノレポ\nフロントエンドとバックエンドのコードを一体管理し、スムーズに開発を行いました。", accent_amber)
    ]
    
    for left, top, title, desc, col in components:
        create_card(slide4, left, top, card_w, card_h, card_color)
        
        # Color bar on the left of each card
        bar = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + Inches(0.2), top + Inches(0.3), Inches(0.08), Inches(1.6))
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()
        
        tf = add_clean_textbox(slide4, left + Inches(0.4), top + Inches(0.3), card_w - Inches(0.6), card_h - Inches(0.6), title, 18, text_white, bold=True)
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = text_gray
        p.font.name = 'MS Gothic'
        p.space_before = Pt(8)
        
    # ----------------------------------------------------
    # SLIDE 5: Security (認証とセキュリティ)
    # ----------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    slide5.background.fill.solid()
    slide5.background.fill.fore_color.rgb = bg_color
    add_clean_textbox(slide5, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), "4. 認証とセキュリティ", 28, accent_indigo, bold=True)
    
    create_card(slide5, Inches(1.0), Inches(1.5), Inches(11.3), Inches(5.0), card_color)
    tf = add_clean_textbox(slide5, Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.4), "■ 安全なWebシステムを守る3大要素", 20, text_white, bold=True)
    
    sec_points = [
        ("", "", ""),
        ("1. パスワードの高度なハッシュ化", "・ユーザーのパスワードは `bcryptjs` を使い、解読不可能な状態でDBに保存されます。", "これにより、万が一データベースが漏えいしても元のパスワードは安全です。"),
        ("2. JWT (JSON Web Token) によるセッション管理", "・ログインの成功時にセキュアなJWTトークンを発行します。", "認証情報を安全にクライアント側に引き渡す仕組みです。"),
        ("3. HTTP-Only Cookie でのトークン保存", "・発行したトークンはブラウザの『HTTP-Only属性付きクッキー』に保存されます。", "JavaScriptからトークンを読み取れないため、XSS（クロスサイトスクリプティング）攻撃を防ぎます。")
    ]
    
    for title, desc1, desc2 in sec_points:
        if not title:
            continue
        p = tf.add_paragraph()
        p.text = f"★ {title}"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = accent_amber
        p.space_before = Pt(8)
        
        p = tf.add_paragraph()
        p.text = f"  {desc1} ({desc2})"
        p.font.size = Pt(12)
        p.font.color.rgb = text_gray
        p.font.name = 'MS Gothic'
        
    # ----------------------------------------------------
    # SLIDE 6: UI Design (操作性とビジュアル)
    # ----------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    slide6.background.fill.solid()
    slide6.background.fill.fore_color.rgb = bg_color
    add_clean_textbox(slide6, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), "5. ビジュアルデザインと操作性", 28, accent_indigo, bold=True)
    
    create_card(slide6, Inches(1.0), Inches(1.5), Inches(11.3), Inches(5.0), card_color)
    tf = add_clean_textbox(slide6, Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.4), "■ 高級感のあるデザインテーマと心地よいUI", 20, text_white, bold=True)
    
    design_points = [
        ("", ""),
        ("・一貫したデザインテーマ", "インディゴ（深みのある紫）とアンバー（暖かい琥珀色）を組み合わせたモダンなダークグラデーション。"),
        ("・完全なレスポンシブ対応", "PC、タブレット、スマートフォンの画面に完璧に適応し、どのサイズでも見やすく崩れません。"),
        ("・心地よいマイクロアニメーションとモーダル効果", "ボタンのホバーエフェクトやスムーズに浮かび上がるモーダルウィンドウなど、操作を楽しくする工夫を凝らしました。"),
        ("・文字の見やすさへの配慮（アクセシビリティ）", "テキストと背景色のコントラスト比を適切に保ち、誰もが疲れずに情報を読み取れるデザインにしています。")
    ]
    for title, desc in design_points:
        if not title:
            continue
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = text_white
        p.space_before = Pt(8)
        
        p = tf.add_paragraph()
        p.text = f"  {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = text_gray
        p.font.name = 'MS Gothic'

    # ----------------------------------------------------
    # SLIDE 7: Demo 1 (メイン画面)
    # ----------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    slide7.background.fill.solid()
    slide7.background.fill.fore_color.rgb = bg_color
    add_clean_textbox(slide7, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), "機能紹介①：メイン画面 ＆ マップ機能", 28, accent_indigo, bold=True)
    
    # Left side Image (Slate bordered)
    img_path = os.path.join(img_dir, "screenshot_main.png")
    if os.path.exists(img_path):
        slide7.shapes.add_picture(img_path, Inches(1.0), Inches(1.5), width=Inches(5.8), height=Inches(3.6))
        
    create_card(slide7, Inches(7.2), Inches(1.5), Inches(5.1), Inches(5.0), card_color)
    tf = add_clean_textbox(slide7, Inches(7.5), Inches(1.8), Inches(4.5), Inches(4.4), "【機能特徴】", 18, text_white, bold=True)
    bullets_p7 = [
        "",
        "・Leaflet.js地図連携",
        "  データベース内の店舗を動的に地図へマッピングします。",
        "",
        "・カードと地図ピンの連動",
        "  左のレストランカードをクリックすると地図のピンがポップアップし、詳細を表示します。",
        "",
        "・テキスト検索機能",
        "  店舗名や住所で即座に絞り込めます。"
    ]
    for b in bullets_p7:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(12) if b.startswith("  ") else Pt(13)
        p.font.color.rgb = text_gray if b.startswith("  ") else text_white
        p.font.name = 'MS Gothic'
        
    # ----------------------------------------------------
    # SLIDE 8: Demo 2 (多言語・ログイン)
    # ----------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    slide8.background.fill.solid()
    slide8.background.fill.fore_color.rgb = bg_color
    add_clean_textbox(slide8, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), "機能紹介②：多言語対応(i18n) ＆ ユーザー認証", 28, accent_indigo, bold=True)
    
    img_path = os.path.join(img_dir, "screenshot_login.png")
    if os.path.exists(img_path):
        slide8.shapes.add_picture(img_path, Inches(1.0), Inches(1.5), width=Inches(5.8), height=Inches(3.6))
        
    create_card(slide8, Inches(7.2), Inches(1.5), Inches(5.1), Inches(5.0), card_color)
    tf = add_clean_textbox(slide8, Inches(7.5), Inches(1.8), Inches(4.5), Inches(4.4), "【機能特徴】", 18, text_white, bold=True)
    bullets_p8 = [
        "",
        "・自作の動的翻訳モジュール",
        "  日本語、英語、ウズベク語、ロシア語の4言語がリロードなしで切り替わります。",
        "",
        "・直感的なログイン画面",
        "  モーダル設計で、ページの切り替えをなくしスムーズなUXを実現しました。",
        "",
        "・Googleソーシャルログイン",
        "  Google認証を使い、ワンタップでログインが可能です。"
    ]
    for b in bullets_p8:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(12) if b.startswith("  ") else Pt(13)
        p.font.color.rgb = text_gray if b.startswith("  ") else text_white
        p.font.name = 'MS Gothic'
        
    # ----------------------------------------------------
    # SLIDE 9: Demo 3 (管理者機能)
    # ----------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    slide9.background.fill.solid()
    slide9.background.fill.fore_color.rgb = bg_color
    add_clean_textbox(slide9, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), "機能紹介③：管理者機能（店舗情報管理）", 28, accent_indigo, bold=True)
    
    img_path = os.path.join(img_dir, "screenshot_add.png")
    if os.path.exists(img_path):
        slide9.shapes.add_picture(img_path, Inches(1.0), Inches(1.5), width=Inches(5.8), height=Inches(3.6))
        
    create_card(slide9, Inches(7.2), Inches(1.5), Inches(5.1), Inches(5.0), card_color)
    tf = add_clean_textbox(slide9, Inches(7.5), Inches(1.8), Inches(4.5), Inches(4.4), "【機能特徴】", 18, text_white, bold=True)
    bullets_p9 = [
        "",
        "・権限に応じたUI表示制限",
        "  管理者(admin)アカウントでのログイン時のみ、追加・編集ボタンが表示されます。",
        "",
        "・ドラッグによる位置指定",
        "  登録用のマップ上でピンを動かすだけで、自動的に緯度と経度が計算されます。",
        "",
        "・画像ファイルアップロード",
        "  店舗写真を指定して、サーバー上にアップロード・静的配信させます。"
    ]
    for b in bullets_p9:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(12) if b.startswith("  ") else Pt(13)
        p.font.color.rgb = text_gray if b.startswith("  ") else text_white
        p.font.name = 'MS Gothic'
        
    # ----------------------------------------------------
    # SLIDE 10: Demo 4 (AIチャットボット)
    # ----------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    slide10.background.fill.solid()
    slide10.background.fill.fore_color.rgb = bg_color
    add_clean_textbox(slide10, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), "機能紹介④：Mikka AI Assistant（Gemini）", 28, accent_indigo, bold=True)
    
    img_path = os.path.join(img_dir, "screenshot_chat.png")
    if os.path.exists(img_path):
        slide10.shapes.add_picture(img_path, Inches(1.0), Inches(1.5), width=Inches(5.8), height=Inches(3.6))
        
    create_card(slide10, Inches(7.2), Inches(1.5), Inches(5.1), Inches(5.0), card_color)
    tf = add_clean_textbox(slide10, Inches(7.5), Inches(1.8), Inches(4.5), Inches(4.4), "【機能特徴】", 18, text_white, bold=True)
    bullets_p10 = [
        "",
        "・Gemini APIとのチャット機能",
        "  画面右下のウィジェットから、いつでもチャットを開始できます。",
        "",
        "・実在する店舗の推薦 (RAG)",
        "  データベース内の店舗リストをAIプロンプトへ動的に挿入し、嘘の回答を防ぎます。",
        "",
        "・タップ式クイックリプライ",
        "  入力の手間を減らすための簡単な選択用ボタンを装備しています。"
    ]
    for b in bullets_p10:
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(12) if b.startswith("  ") else Pt(13)
        p.font.color.rgb = text_gray if b.startswith("  ") else text_white
        p.font.name = 'MS Gothic'
        
    # ====================================================
    # 全10スライドへ N3レベル・ます形のスピーカーノートを流し込む
    # ====================================================
    presentation_notes = [
        "【発表原稿（スライド1）】[N3レベル・ます形]\n"
        "はじめまして。アブドゥラエフ・ジャブロンと申します。\n"
        "本日は、私がコワーク授業で開発した飲食店情報口コミサイト『Mikka（ミッカ）』について発表します。\n"
        "どうぞよろしくお願いいたします。",
        
        "【発表原稿（スライド2）】[N3レベル・ます形]\n"
        "まず、プロジェクトの目的について説明します。\n"
        "このサイトは、地域のレストラン情報を共有して、色々な国の言葉で口コミを投稿できるプラットフォームです。\n"
        "地元の人から、日本を訪れる外国人観光客まで幅広く対応して、言葉の壁を越えてお店を探せるように作りました。\n"
        "デザインは、誰でも直感的に操作できるモダンで美しい画面を意識して設計しました。",
        
        "【発表原稿（スライド3）】[N3レベル・ます形]\n"
        "次に、主な機能について説明します。\n"
        "システムには、ユーザー登録とログイン、日本語・ウズベク語・ロシア語・英語の多言語切り替え機能、Leafletを使用したインタラクティブな地図表示機能があります。\n"
        "ユーザーは星評価、コメント、画像を使って口コミを投稿でき、管理者は店舗の登録や編集を行えます。\n"
        "さらに、Gemini APIを使ったAIチャットアシスタントも搭載しています。",
        
        "【発表原稿（スライド4）】[N3レベル・ます形]\n"
        "システムの技術構成についてです。\n"
        "開発効率を高めるため、フロントエンドとバックエンドを1つのリポジトリで管理する『モノレポ』を採用しました。\n"
        "フロントエンドはHTML5、CSS3、およびVanilla JavaScriptを使い、軽くて速く動くようにしました。\n"
        "バックエンドはTypeScriptとFastifyフレームワークを使い、クリーンアーキテクチャで設計しました。\n"
        "データベースはPostgreSQLを使用しています。",
        
        "【発表原稿（スライド5）】[N3レベル・ます形]\n"
        "セキュリティについてです。\n"
        "ユーザーのパスワードは、bcryptjsを使ってハッシュ化し、安全に保存しています。\n"
        "ログイン後のセッション管理にはJWT（JSON Web Token）を使い、ブラウザのHTTP-Only Cookieに保存しています。\n"
        "これにより、外部からの不正アクセスやセキュリティ上の攻撃からユーザーの情報を保護します。",
        
        "【発表原稿（スライド6）】[N3レベル・ます形]\n"
        "デザインと操作性についての工夫です。\n"
        "インディゴ（紫）とアンバー（琥珀色）を基調とした、モダンなダークテーマとGlassmorphicデザインを採用しました。\n"
        "スマートフォン、タブレット、PCなど、どの画面でもきれいに表示されるレスポンシブ対応です。\n"
        "また、ボタンのアニメーションなど、使いやすさを高める工夫も行いました。",
        
        "【発表原稿（スライド7）】[N3レベル・ます形]\n"
        "ここからは実際の画面です。\n"
        "メイン画面では、Leaflet.js地図APIを使って、登録された飲食店を地図上に表示します。\n"
        "リストの店舗をクリックすると、地図のピンがポップアップします。\n"
        "店舗名やジャンル（Uzbek, Japanese等）で素早く検索することも可能です。",
        
        "【発表原稿（スライド8）】[N3レベル・ます形]\n"
        "こちらは多言語切り替えとログイン画面です。\n"
        "地球儀のボタンから、日本語・ウズベク語・ロシア語・英語をリロードなしで瞬時に言語を切り替えることができます。\n"
        "また、Googleアカウントを使った簡単なソーシャルログインも実装しました。",
        
        "【発表原稿（スライド9）】[N3レベル・ます形]\n"
        "こちらは管理者用の店舗追加・編集画面です。\n"
        "管理者だけが新しい店舗を登録できます。\n"
        "地図の上でピンをドラッグするだけで、緯度と経度が自動で入力される便利なUIを作りました。\n"
        "画像のアップロード機能も付いています。",
        
        "【発表原稿（スライド10）】[N3レベル・ます形]\n"
        "最後に、AIアシスタント機能です。\n"
        "右下のチャットボタンから、Gemini APIを使ったチャットボット『Mikka AI』が起動します。\n"
        "データベース内の最新店舗データをAIに渡して回答を生成させることで、AIが嘘の情報を言うのを防ぎ、実在するおすすめ店を正しく紹介することができます。\n\n"
        "以上で、私の発表を終わります。ありがとうございました。"
    ]
    
    for i, slide in enumerate(prs.slides):
        if i < len(presentation_notes):
            slide.notes_slide.notes_text_frame.text = presentation_notes[i]
            
    prs.save(ppt_path)
    print("Rebuilt Mikka_Presentation.pptx in Gamma Widescreen Dark Slate style successfully!")

if __name__ == "__main__":
    rebuild_cowork_presentation()
