from pptx import Presentation
import os

ppt_path = "/Users/macbook-projavlon/Desktop/JDU_bitiruv/employability/7_自己紹介プレゼン資料.pptx"

def main():
    if not os.path.exists(ppt_path):
        print("7_自己紹介プレゼン資料.pptx not found.")
        return

    prs = Presentation(ppt_path)
    
    # 4枚のスライドに対応する発表台本（スピーカーノート）を定義
    self_intro_notes = [
        # Slide 1 (自己紹介タイトル)
        "【発表原稿（スライド1）】※制限時間：目安 30秒〜45秒\n"
        "はじめまして。アブドゥラエフ・ジャブロンと申します。本日はよろしくお願いいたします。\n"
        "私は現在、ウズベキスタン世界言語大学でコンピュータ言語学を専攻する傍ら、JDU（Japan Digital University）でコンピュータ工学を学び、日本市場やグローバル企業で即戦力として活躍できるソフトウェアエンジニアを目指しています。\n"
        "また、産業能率大学でビジネスリテラシーも学びました。\n"
        "本日は、私の強みについて2点、紹介させていただきます。",
        
        # Slide 2 (強み1：Web開発)
        "【発表原稿（スライド2）】※制限時間：目安 60秒\n"
        "私の強みの1つ目は、『フルスタックなWeb開発力とクリーンなコードへのこだわり』です。\n"
        "私はJavaScriptやNode.js、PostgreSQLを用いたWeb開発を得意としています。\n"
        "最近のコワーク活動では、飲食店口コミサイト『Mikka（ミッカ）』というシステムをゼロから構築しました。\n"
        "このアプリは、地図上での位置情報連携や多言語対応に加え、Google Gemini APIを組み込んだAIチャットボットがおすすめの飲食店をレコメンドする機能を持っています。\n"
        "バックエンドには『クリーンアーキテクチャ』を採用し、変化に強くメンテナンスしやすいシステムを意識して設計しました。",
        
        # Slide 3 (強み2：日本語・デザイン)
        "【発表原稿（スライド3）】※制限時間：目安 60秒\n"
        "強みの2つ目は、『多文化な環境での高いコミュニケーション力と日本語能力』です。\n"
        "私の日本語レベルは最高レベルのC2、JLPT N2相当であり、日本人のパートナーと直接ビジネスのやり取りを行うことができます。\n"
        "実際、JDUではグラフィックデザイナーとして、日本向けに輸出されるTシャツのプリントデザインを1,000件以上制作し、プロジェクトを成功に導きました。\n"
        "また、他校で日本語教師として20名以上の学生に日本語を教えた経験もあり、難しい概念を分かりやすく伝えるスキルを持っています。",
        
        # Slide 4 (目標)
        "【発表原稿（スライド4）】※制限時間：目安 30秒〜45秒\n"
        "最後に、私の将来の目標についてです。\n"
        "私は将来、この『技術力』『デザイン・表現力』、そして『日本語力』を掛け合わせ、日本とウズベキスタン、あるいは世界を繋ぐブリッジシステムエンジニアとして、社会に価値あるシステムを提供したいと考えています。\n"
        "本日は、私のこれまでの開発実績や自己PRについてお伝えできることを楽しみにしております。\n"
        "ご清聴ありがとうございました。どうぞよろしくお願いいたします。"
    ]
    
    # スピーカーノートの設定
    for i, slide in enumerate(prs.slides):
        if i < len(self_intro_notes):
            notes_slide = slide.notes_slide
            text_frame = notes_slide.notes_text_frame
            text_frame.text = self_intro_notes[i]
            print(f"Added self-intro notes to Slide {i+1}")
            
    prs.save(ppt_path)
    print("Successfully updated presenter notes for self-introduction slides!")

if __name__ == "__main__":
    main()
