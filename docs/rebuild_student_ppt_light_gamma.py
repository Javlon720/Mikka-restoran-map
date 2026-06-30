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

def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Colors (Light Gamma Modern theme - Eye-catching colors)
    bg_color = RGBColor(255, 255, 255)       # Pure white background (ユーザーの要望)
    card_color = RGBColor(248, 250, 252)     # Slate-50 (Very light gray card background)
    border_color = RGBColor(226, 232, 240)   # Slate-200 (Subtle border for cards)
    
    text_dark = RGBColor(15, 23, 42)         # Slate-900 (Dark readable text)
    text_gray = RGBColor(71, 85, 105)        # Slate-600 (Muted subtext)
    
    # Eye-catching accent colors
    accent_blue = RGBColor(29, 78, 216)      # Blue-700 (Deep royal blue - highly professional)
    accent_teal = RGBColor(13, 148, 136)     # Teal-600 (Vibrant teal - attractive highlight)
    
    blank_layout = prs.slide_layouts[6]
    
    photo_path = '/Users/macbook-projavlon/Downloads/IMG_0844.JPG'
    has_photo = os.path.exists(photo_path)
    
    # 18枚のスライドデータを定義
    slides_data = [
        # Slide 1
        {
            "id": 1,
            "title": "INTRODUCTION",
            "subtitle": "自己紹介 (Self-Introduction)",
            "content": [
                "氏名: ジャブロン・アブドゥラエフ",
                "所属: Japan Digital University (JDU) / コンピューター工学科",
                "日付: 2026年6月30日"
            ],
            "note": "【発表原稿（スライド1）】[N3・ます形]\n"
                    "はじめまして。アブドゥラエフ・ジャブロンと申します。本日は私の自己紹介をさせていただきます。\n"
                    "どうぞよろしくお願いいたします。"
        },
        # Slide 2
        {
            "id": 2,
            "title": "INTRODUCTION",
            "subtitle": "本日の目的",
            "content": [
                "• 面接で自然に自己紹介ができるようになること",
                "• 相手に自分のことを正しく伝えること",
                "• 30秒〜45秒で話す練習をすること"
            ],
            "note": "【発表原稿（スライド2）】[N3・ます形]\n"
                    "本日の目的は、面接で自然に自己紹介ができるようになること、精度高く相手に自分のことを正しく伝えることです。\n"
                    "30秒から45秒程度で簡潔に話せるように練習を重ねてきました。"
        },
        # Slide 3
        {
            "id": 3,
            "title": "自己紹介①",
            "subtitle": "名前・年齢・所属",
            "content": [
                "• 名前: ジャブロン・アブドゥラエフ",
                "• 年齢: 23歳（2003年9月18日生まれ）",
                "• 所属: JDU大学 コンピューター工学科 5年生",
                "• 卒業予定: 2026年"
            ],
            "note": "【発表原稿（スライド3）】[N3・ます形]\n"
                    "私の名前はジャブロン・アブドゥラエフです。年齢は23歳で、2003年9月18日生まれです。\n"
                    "現在はJDU大学のコンピューター工学科の5年生で、2026年に卒業する予定です。"
        },
        # Slide 4
        {
            "id": 4,
            "title": "自己紹介②",
            "subtitle": "大学で学んでいること",
            "content": [
                "• プログラミング（複数の言語を学習中）",
                "• データベースの基礎と設計",
                "• ネットワークの仕組み",
                "• Web開発とバックエンド開発の基本"
            ],
            "note": "【発表原稿（スライド4）】[N3・ます形]\n"
                    "大学では、複数のプログラミング言語の学習、データベースの基礎と設計、ネットワークの仕組み、およびWeb開発とバックエンド開発の基本について学んできました。"
        },
        # Slide 5
        {
            "id": 5,
            "title": "興味のある分野",
            "subtitle": "バックエンド開発に特に興味がある",
            "content": [
                "• サーバーの仕組みやデータ処理の流れを理解したい",
                "• セキュリティについても学びたい",
                "• 実践的なスキルを身につけることが目標"
            ],
            "note": "【発表原稿（スライド5）】[N3・ます形]\n"
                    "私は特にバックエンド開発に興味があります。サーバーの仕組みやデータ処理の流れを理解し、セキュリティについても学びながら、実践的なスキルを身につけることが目標です。"
        },
        # Slide 6
        {
            "id": 6,
            "title": "ITを始めたきっかけ",
            "subtitle": "開発への情熱と社会貢献",
            "content": [
                "• 自分でアプリケーションやサービスを開発したいという想い",
                "• IT技術を使って問題を解決できることに魅力を感じた",
                "• 技術で社会に貢献したいと考えている",
                "• 新しいことを学ぶことが好き"
            ],
            "note": "【発表原稿（スライド6）】[N3・ます形]\n"
                    "自分でアプリケーションやサービスを一から開発したいと思ったことがきっかけです。\n"
                    "IT技術を使って身の回りの問題を解決できる点に強い魅力を感じ、技術で社会に貢献したいと考えています。"
        },
        # Slide 7
        {
            "id": 7,
            "title": "最近勉強していること",
            "subtitle": "セキュリティとデータベース",
            "content": [
                "• セキュリティについて（JWT認証など）",
                "• データベースの設計と活用方法",
                "• バックエンド技術の深い理解",
                "• 授業以外でも自分で調べて学習している"
            ],
            "note": "【発表原稿（スライド7）】[N3・ます形]\n"
                    "最近は、特にJWT認証などのセキュリティ技術や、データベースの設計方法について深く勉強しています。\n"
                    "大学の授業以外でも、自分で調べて学習を進めています。"
        },
        # Slide 8
        {
            "id": 8,
            "title": "大切にしていること",
            "subtitle": "継続的な学習とチームワーク",
            "content": [
                "• わからないことをそのままにせず、必ず理解するまで調べる",
                "• チームで活動するときはコミュニケーションを大切にしている",
                "• 相手の意見を聞き、協力することを重視している",
                "• 継続的に学習し、成長することを心がけている"
            ],
            "note": "【発表原稿（スライド8）】[N3・ます形]\n"
                    "私が大切にしていることは、分からないことをそのままにせず、必ず理解するまで調べることです。\n"
                    "また、チームで活動するときはコミュニケーションと協力を最も重視しています。"
        },
        # Slide 9
        {
            "id": 9,
            "title": "面接で伝えたい印象",
            "subtitle": "「前向きで努力を続ける人」",
            "content": [
                "• 新しいことを学ぶことが好きで、チャレンジ精神がある",
                "• 最後まであきらめずに取り組む姿勢を大切にしている",
                "• 相手と協力して、一緒に成長したいと考えている"
            ],
            "note": "【発表原稿（スライド9）】[N3・ます形]\n"
                    "面接官の皆様には、『前向きで努力を続ける人』という印象を持っていただきたいです。\n"
                    "新しいことを学ぶのが好きで、チャレンジ精神を持ち、最後まで諦めずに取り組みます。"
        },
        # Slide 10
        {
            "id": 10,
            "title": "まとめ",
            "subtitle": "感謝と今後の展望",
            "content": [
                "• 本日は自己紹介の時間をいただき、ありがとうございました",
                "• 皆様の前で自分のことをお話しできて、とても嬉しいです",
                "• これからも努力を続けて、成長していきたいと思っています"
            ],
            "note": "【発表原稿（スライド10）】[N3・ます形]\n"
                    "本日は自己紹介の時間をいただき、本当にありがとうございました。\n"
                    "皆様の前でお話しできて嬉しいです。これからも努力を続けて成長していきます。"
        },
        # Slide 11
        {
            "id": 11,
            "title": "プロフィール",
            "subtitle": "詳細な自己紹介",
            "content": [
                "• 名前: ジャブロンベク・アブドゥラエフ・シュフラトオグリ",
                "• 年齢: 22歳 (生年月日: 2003年9月18日)",
                "• 所属: Japan Digital University 5年生 (卒業予定)"
            ],
            "note": "【発表原稿（スライド11）】[N3・ます形]\n"
                    "私の本名はジャブロンベク・アブドゥラエフ・シュフラトオグリです。\n"
                    "22歳で、生年月日は2003年9月18日です。Japan Digital Universityの5年生です。"
        },
        # Slide 12
        {
            "id": 12,
            "title": "学習内容",
            "subtitle": "大学での主な専門分野",
            "content": [
                "• プログラミング言語",
                "• データベース設計",
                "• ネットワーク構築",
                "• Web開発とバックエンド基礎"
            ],
            "note": "【発表原稿（スライド12）】[N3・ます形]\n"
                    "大学で主に学習している内容は、プログラミング、データベース、ネットワーク、そしてWeb開発とバックエンドの基礎技術です。"
        },
        # Slide 13
        {
            "id": 13,
            "title": "興味分野",
            "subtitle": "特に関心のあるIT技術",
            "content": [
                "• バックエンド開発",
                "• サーバーの仕組み",
                "• データ処理の流れ"
            ],
            "note": "【発表原稿（スライド13）】[N3・ます形]\n"
                    "私の興味のある分野は、バックエンド開発、サーバーの仕組み、そして大量のデータ処理の流れについてです。"
        },
        # Slide 14
        {
            "id": 14,
            "title": "ITに興味を持ったきっかけ",
            "subtitle": "開発への興味と問題解決",
            "content": [
                "• 自分でサービスやアプリケーションを開発したい想い",
                "• IT技術を使って問題を解決できる点に魅力を感じた"
            ],
            "note": "【発表原稿（スライド14）】[N3・ます形]\n"
                    "自分で新しいサービスやアプリケーションを開発し、ITの力で社会の様々な問題を解決できることに魅力を感じたため、ITに興味を持ちました。"
        },
        # Slide 15
        {
            "id": 15,
            "title": "最近の学習",
            "subtitle": "自律的な技術学習",
            "content": [
                "• セキュリティについて (JWT)",
                "• データベースの設計・活用方法"
            ],
            "note": "【発表原稿（スライド15）】[N3・ます形]\n"
                    "最近は、JWTを使ったセキュリティや、より複雑なデータベースの設計・活用方法について自主的に学習を進めています。"
        },
        # Slide 16
        {
            "id": 16,
            "title": "学ぶときに大切にしていること",
            "subtitle": "探究心と協調性",
            "content": [
                "• 分からないことをそのままにせず、必ず理解するまで調べる",
                "• チームで活動するときは、コミュニケーションと協力を大切にする"
            ],
            "note": "【発表原稿（スライド16）】[N3・ます形]\n"
                    "学ぶときに大切にしていることは、疑問点を放置せず最後まで調べること、端的にチームで活動する際はコミュニケーションを取り、協力し合うことです。"
        },
        # Slide 17
        {
            "id": 17,
            "title": "面接で最初に知っていただきたい印象",
            "subtitle": "「前向きで努力を続ける人」",
            "content": [
                "• 新しいことを学ぶことが好き",
                "• 最後まであきらめずに取り組む姿勢を大切にしている"
            ],
            "note": "【発表原稿（スライド17）】[N3・ます形]\n"
                    "面接官の皆様に最初に知っていただきたい私の印象は、『前向きで努力を続ける人』です。\n"
                    "新しいことを学ぶ楽しさを知り、諦めずにやり遂げる姿勢を持っています。"
        },
        # Slide 18
        {
            "id": 18,
            "title": "ご清聴ありがとうございました",
            "subtitle": "Thank you for your time",
            "content": [
                "• お忙しい中、貴重なお時間をいただきありがとうございました",
                "• ジャブロンベク・アブドゥラエフ・シュフラトオグリ",
                "• Email: abdullayevjavlon720@gmail.com"
            ],
            "note": "【発表原稿（スライド18）】[N3・ます形]\n"
                    "お忙しい中、貴重なお時間をいただき本当にありがとうございました。メールアドレスは記載の通りです。\n"
                    "どうぞよろしくお願いいたします。"
        }
    ]

    for data in slides_data:
        slide = prs.slides.add_slide(blank_layout)
        
        # Background Solid Color
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = bg_color
        
        # 1. Slide Title (Polished deep blue, eye-catching color)
        add_clean_textbox(slide, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), data["title"], 28, accent_blue, bold=True)
        
        # Title Accent Line (Teal color)
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.2), Inches(3.0), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = accent_teal
        line.line.fill.background()
        
        # Layout depends on slide ID (Slides 1 and 11 get the profile photo on the right)
        is_profile_slide = data["id"] in [1, 11]
        
        if is_profile_slide and has_photo:
            # 2 Columns: Left side Card for text, Right side for Photo
            # Card
            create_card(slide, Inches(1.0), Inches(1.5), Inches(7.0), Inches(5.0), card_color, border_color)
            tf = add_clean_textbox(slide, Inches(1.4), Inches(1.8), Inches(6.2), Inches(4.4), data["subtitle"], 20, accent_teal, bold=True)
            
            for bullet in data["content"]:
                p = tf.add_paragraph()
                p.text = bullet
                p.font.size = Pt(14)
                p.font.name = 'MS Gothic'
                p.font.color.rgb = text_dark
                p.space_before = Pt(12)
                p.font.bold = not bullet.strip().startswith("•")
                
            # Photo (Right side)
            # Create a card border for photo first
            photo_card = create_card(slide, Inches(8.5), Inches(1.5), Inches(3.8), Inches(5.0), card_color, border_color)
            # Add image inside the card area
            slide.shapes.add_picture(photo_path, Inches(8.7), Inches(1.7), width=Inches(3.4), height=Inches(4.6))
        else:
            # Standard Slide: 1 Big Card for text
            create_card(slide, Inches(1.0), Inches(1.5), Inches(11.3), Inches(5.0), card_color, border_color)
            tf = add_clean_textbox(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.4), data["subtitle"], 20, accent_teal, bold=True)
            
            for bullet in data["content"]:
                p = tf.add_paragraph()
                p.text = bullet
                p.font.size = Pt(15)
                p.font.name = 'MS Gothic'
                p.font.color.rgb = text_dark
                p.space_before = Pt(12)
                p.font.bold = not bullet.strip().startswith("•")
                
        # 5. Add Speaker Notes
        slide.notes_slide.notes_text_frame.text = data["note"]
        
    # Save the file
    ppt_out = "/Users/macbook-projavlon/Desktop/JDU_bitiruv/employability/7_自己紹介プレゼン資料.pptx"
    prs.save(ppt_out)
    print("Rebuilt student resume PPTX into 18 modern light widescreen slides with photo successfully!")

if __name__ == "__main__":
    main()
