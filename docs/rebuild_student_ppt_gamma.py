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
    
    # Colors (Slate Dark style)
    bg_color = RGBColor(15, 23, 42)
    card_color = RGBColor(30, 41, 59)
    text_white = RGBColor(241, 245, 249)
    text_gray = RGBColor(148, 163, 184)
    accent_indigo = RGBColor(99, 102, 241)
    accent_amber = RGBColor(245, 158, 11)
    
    blank_layout = prs.slide_layouts[6]
    
    # 18枚のスライドデータを定義 (元のスライドから抽出したテキスト)
    slides_data = [
        # Slide 1
        {
            "title": "INTRODUCTION",
            "subtitle": "自己紹介 (Self-Introduction)",
            "content": [
                "氏名: ジャブロン・アブドゥラエフ",
                "所属: Japan Digital University (JDU) / コンピューター工学科"
            ],
            "note": "【発表原稿（スライド1）】[N3・ます形]\n"
                    "はじめまして。アブドゥラエフ・ジャブロンと申します。本日は私の自己紹介をさせていただきます。\n"
                    "どうぞよろしくお願いいたします。"
        },
        # Slide 2
        {
            "title": "INTRODUCTION",
            "subtitle": "本日の目的",
            "content": [
                "• 面接で自然に自己紹介ができるようになること",
                "• 相手に自分のことを正しく伝えること",
                "• 30秒〜45秒で話す練習をすること"
            ],
            "note": "【発表原稿（スライド2）】[N3・ます形]\n"
                    "本日の目的は、面接で自然に自己紹介ができるようになること、そして相手に自分のことを正しく伝えることです。\n"
                    "30秒から45秒程度で簡潔に話せるように練習を重ねてきました。"
        },
        # Slide 3
        {
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
            "title": "自己紹介②",
            "subtitle": "大学で学んでいること",
            "content": [
                "• プログラミング（複数の言語を学習中）",
                "• データベースの基礎と設計",
                "• ネットワークの仕組み",
                "• Web開発とバックエンド開発の基本"
            ],
            "note": "【発表原稿（スライド4）】[N3・ます形]\n"
                    "大学では、複数のプログラミング言語の学習、データベースの基礎と設計、ネットワークの仕組み、そしてWeb開発とバックエンド開発の基本について学んできました。"
        },
        # Slide 5
        {
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
            "title": "学ぶときに大切にしていること",
            "subtitle": "探究心と協調性",
            "content": [
                "• 分からないことをそのままにせず、必ず理解するまで調べる",
                "• チームで活動するときは、コミュニケーションと協力を大切にする"
            ],
            "note": "【発表原稿（スライド16）】[N3・ます形]\n"
                    "学ぶときに大切にしていることは、疑問点を放置せず最後まで調べること、そしてチームで活動する際はコミュニケーションを取り、協力し合うことです。"
        },
        # Slide 17
        {
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
        
        # Background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = bg_color
        
        # 1. Slide Title (Accent color Indigo)
        add_clean_textbox(slide, Inches(1.0), Inches(0.5), Inches(11.3), Inches(0.8), data["title"], 28, accent_indigo, bold=True)
        
        # 2. Card layout for content
        create_card(slide, Inches(1.0), Inches(1.5), Inches(11.3), Inches(5.0), card_color)
        
        # 3. Add Subtitle inside the card
        tf = add_clean_textbox(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.4), data["subtitle"], 20, accent_amber, bold=True)
        
        # 4. Add Bullet points inside the card
        for bullet in data["content"]:
            p = tf.add_paragraph()
            p.text = bullet
            p.font.size = Pt(15)
            p.font.name = 'MS Gothic'
            p.font.color.rgb = text_white
            p.space_before = Pt(10)
            if bullet.strip().startswith("•"):
                p.font.bold = False
            else:
                p.font.bold = True
                
        # 5. Add N3-polite Speaker Notes
        slide.notes_slide.notes_text_frame.text = data["note"]
        
    # Save the file
    ppt_out = "/Users/macbook-projavlon/Desktop/JDU_bitiruv/employability/7_自己紹介プレゼン資料.pptx"
    prs.save(ppt_out)
    print("Rebuilt student resume PPTX into 18 modern widescreen Gamma slides successfully!")

if __name__ == "__main__":
    main()
