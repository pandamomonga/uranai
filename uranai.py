import random
import re
from datetime import datetime
import json
import os

# PDFから抽出した波動コードのデータ
hadou_data = {
    "感情波動": {
        "45-672": "怒り",
        "135-489": "無関心・感情麻痺",
        "235-493": "幸福感の欠如",
        "335-883": "無表情な",
        "435-891": "癌に対する恐怖",
        "535-896": "虚偽・欺き",
        "645-055": "やきもち",
        "745-056": "消極性・否定的",
        "845-072": "偏見・ひがみ",
        "955-160": "心配・不安",
        "1055-168": "愚図",
        "1145-236": "倦怠・飽きっぽい",
        "1245-266": "苛立ち・いらいら",
        "1345-396": "不信 疑惑",
        "1445-408": "恐怖",
        "1545-487": "罪の意識",
        "1645-496": "妄想・強迫観念",
        "1745-593": "プレッシャー",
        "1845-604": "迷い",
        "1945-605": "懸念・神経質な",
        "2045-631": "忍耐心の欠如",
        "2145-648": "強いいらだち・せっかち",
        "2345-720": "良心の呵責",
        "2445-823": "疲労・だるさ",
        "2545-859": "抑鬱",
        "2645-921": "恨み",
        "2745-929": "深い悲しみ・悲嘆",
        "2845-953": "非常な恐怖",
        "2955-005": "死に対する恐怖",
        "3055-011": "絶望・自暴自棄",
        "3155-015": "短気",
        "3255-030": "寂しさ",
        "3355-038": "悲しみ",
        "3455-055": "気苦労",
        "3555-058": "不幸",
        "3655-093": "自制心を失う恐れ",
        "3755-102": "頑固・プライド",
        "3855-144": "パニック",
        "3955-216": "メランコリー・憂鬱",
        "4055-222": "ストレス",
        "4155-227": "意図・目論見",
        "4255-275": "抑圧",
        "4355-431": "ヒステリー",
        "4455-702": "はにかみ・内気",
        "4555-916": "自己憐憫",
        "4665-001": "無気力",
        "4765-007": "環境ストレス",
        "4875-315": "幻覚・妄想",
    },
    "毒素波動": {
        "145-410": "鉄沈着",
        "245-459": "炭素沈着",
        "345-679": "動物毒素",
        "445-684": "疲労毒素",
        "545-695": "カドミウム沈着",
        "645-858": "カルシウム沈着",
        "745-984": "ナトリウム沈着",
        "855-109": "原子灰",
        "955-160": "鉄欠乏",
        "1055-168": "ポリオ毒素",
        "1155-170": "放射線毒素",
        "1255-487": "臭毒素",
        "1355-860": "アルミニウム毒",
        "1455-973": "一般毒",
        "1565-474": "硫黄毒",
        "1665-029": "連鎖球菌発赤毒素",
        "1765-029": "ブドウ球菌毒素",
        "1865-031": "超短波放射線",
        "1965-241": "アルコール毒",
        "2065-242": "モルヒネ毒",
        "2165-243": "亜鉛毒",
        "2265-305": "キニーネ毒",
        "2365-432": "たばこ中毒",
        "2465-573": "コカイン毒",
        "2565-639": "ラジウム熱傷",
        "2665-674": "真鍮毒",
        "2765-707": "鉛毒",
        "2865-708": "細菌性毒",
        "2965-825": "鉄毒",
        "3065-874": "マグネシウム毒",
        "3175-182": "蛍光性毒",
        "3275-187": "カルシウム沈着",
        "3375-384": "レントゲン焼け",
        "3475-585": "銀毒",
        "3575-584": "ニコチン毒",
        "3685-051": "コバルト熱傷",
        "3785-058": "ヒ素",
        "3885-069": "水銀毒",
        "3985-074": "ナトリウム毒",
        "4085-118": "ヨウ素毒",
        "4185-149": "アヘン毒",
        "4285-178": "麻薬中毒",
        "4316-022": "リン中毒",
        "4486-358": "紫外線",
    },
    "ウィルス波動": {
        "135-492": "染色体",
        "245-193": "チミン (DNA)",
        "345-428": "エプスタインバーウィルス",
        "445-479": "アデノウィルス",
        "545-497": "アデノウィルス",
        "645-647": "A型肝炎ウィルス",
        "745-863": "インフルエンザウィルス・ロシア",
        "855-082": "コロナウィルス",
        "955-090": "サイトメガロウィルス",
        "1055-122": "エコーウィルス",
        "1155-126": "インフルエンザ",
        "1255-158": "ヘルペスウィルス",
        "1355-171": "レオウィルス",
        "1455-329": "肝炎",
        "1555-439": "パラインフルエンザウィルス",
        "1655-508": "コクサッキーウィルス",
        "1755-510": "エコーウィルス",
        "1855-585": "ワクチニアウィルス",
        "1955-731": "インフルエンザ・ロシア",
        "2065-010": "B型肝炎ウィルス",
        "2165-022": "灰白髄炎・ポリオ",
        "2265-121": "ウィルス",
        "2365-147": "タバコモザイクウィルス",
        "2475-054": "タンパク質",
        "2585-120": "インフルエンザ",
    }
}

# 波動に対するアドバイスと幸運アイテム
hadou_advice = {
    # 感情波動のアドバイス
    "怒り": {
        "advice": "深呼吸をして、心を落ち着けましょう。今日は冷静な判断が大切です。",
        "lucky_item": "ラベンダーの香り",
        "color": "青",
        "number": 7
    },
    "無関心・感情麻痺": {
        "advice": "新しいことに挑戦してみましょう。小さな刺激が心を動かします。",
        "lucky_item": "カラフルな花",
        "color": "オレンジ",
        "number": 3
    },
    "幸福感の欠如": {
        "advice": "小さな幸せを見つけてみましょう。感謝の気持ちが幸運を呼びます。",
        "lucky_item": "お気に入りの音楽",
        "color": "黄色",
        "number": 9
    },
    "心配・不安": {
        "advice": "今に集中しましょう。心配事の9割は起こりません。",
        "lucky_item": "アメジスト",
        "color": "紫",
        "number": 5
    },
    "ストレス": {
        "advice": "今日は自分へのご褒美を。リラックスタイムを大切に。",
        "lucky_item": "ハーブティー",
        "color": "緑",
        "number": 2
    },
    # 毒素波動のアドバイス
    "疲労毒素": {
        "advice": "休息が必要です。今日は早めに休んで体を労わりましょう。",
        "lucky_item": "温かいお風呂",
        "color": "白",
        "number": 8
    },
    "環境毒素": {
        "advice": "自然の中で過ごす時間を作りましょう。新鮮な空気が幸運を運びます。",
        "lucky_item": "観葉植物",
        "color": "深緑",
        "number": 4
    },
    # ウィルス波動のアドバイス
    "インフルエンザ": {
        "advice": "免疫力を高めましょう。ビタミンCとたっぷりの睡眠が味方です。",
        "lucky_item": "レモン",
        "color": "黄緑",
        "number": 6
    }
}

class HadouFortuneApp:
    def __init__(self):
        self.history_file = "fortune_history.json"
        self.load_history()
        
    def load_history(self):
        """占い履歴を読み込む"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        else:
            self.history = []
    
    def save_history(self, result):
        """占い結果を履歴に保存"""
        self.history.append(result)
        # 最新の10件のみ保存
        if len(self.history) > 10:
            self.history = self.history[-10:]
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def get_zodiac_sign(self, month, day):
        """誕生日から星座を判定"""
        zodiac_dates = [
            (1, 20, "山羊座"), (2, 19, "水瓶座"), (3, 21, "魚座"),
            (4, 20, "牡羊座"), (5, 21, "牡牛座"), (6, 21, "双子座"),
            (7, 23, "蟹座"), (8, 23, "獅子座"), (9, 23, "乙女座"),
            (10, 23, "天秤座"), (11, 22, "蠍座"), (12, 22, "射手座"),
            (12, 31, "山羊座")
        ]
        
        for end_month, end_day, sign in zodiac_dates:
            if month < end_month or (month == end_month and day <= end_day):
                return sign
        return "山羊座"
    
    def get_detailed_advice(self, hadou_name):
        """波動に基づいた詳細なアドバイスを取得"""
        # デフォルトのアドバイス
        default_advice = {
            "advice": "今日は新しい発見がありそうです。前向きに過ごしましょう。",
            "lucky_item": "クリスタル",
            "color": "虹色",
            "number": random.randint(1, 9)
        }
        
        # 完全一致を探す
        if hadou_name in hadou_advice:
            return hadou_advice[hadou_name]
        
        # 部分一致を探す
        for key in hadou_advice:
            if key in hadou_name or hadou_name in key:
                return hadou_advice[key]
        
        # カテゴリ別のデフォルトアドバイスを生成
        if "恐怖" in hadou_name:
            return {
                "advice": "勇気を持って一歩踏み出しましょう。恐れは幻想です。",
                "lucky_item": "お守り",
                "color": "赤",
                "number": 1
            }
        elif "毒" in hadou_name or "毒素" in hadou_name:
            return {
                "advice": "デトックスを心がけましょう。水分をたくさん摂って。",
                "lucky_item": "レモン水",
                "color": "透明",
                "number": 0
            }
        elif "ウィルス" in hadou_name:
            return {
                "advice": "健康第一。手洗いうがいを忘れずに。",
                "lucky_item": "マスク",
                "color": "白",
                "number": 8
            }
        
        return default_advice
    
    def calculate_compatibility(self, hadou_code):
        """波動コードから相性の良い人を計算"""
        code_numbers = [int(x) for x in re.findall(r'\d+', hadou_code)]
        total = sum(code_numbers) % 12
        
        compatibility_types = [
            "リーダータイプ", "サポータータイプ", "クリエイタータイプ",
            "アナリストタイプ", "コミュニケータータイプ", "ヒーラータイプ",
            "チャレンジャータイプ", "オーガナイザータイプ", "ビジョナリータイプ",
            "メンタータイプ", "イノベータータイプ", "ハーモナイザータイプ"
        ]
        
        return compatibility_types[total]
    
    def generate_biorhythm(self):
        """今日のバイオリズムを生成"""
        today = datetime.now()
        day_of_year = today.timetuple().tm_yday
        
        # 簡易的なバイオリズム計算
        physical = int(50 + 50 * random.random())
        emotional = int(50 + 50 * random.random())
        intellectual = int(50 + 50 * random.random())
        
        return {
            "physical": physical,
            "emotional": emotional,
            "intellectual": intellectual
        }
    
    def fortune_telling(self):
        """占いアプリのメイン機能"""
        print("\n" + "="*50)
        print("✨ 波動占いアプリ Premium ✨".center(50))
        print("="*50 + "\n")
        
        # 名前の入力
        name = input("あなたのお名前を教えてください: ")
        
        # 誕生日の入力（オプション）
        use_birthday = input("誕生日を使った詳細占いをしますか？ (y/n): ").lower()
        zodiac = None
        if use_birthday == 'y':
            try:
                month = int(input("生まれた月を入力してください (1-12): "))
                day = int(input("生まれた日を入力してください: "))
                zodiac = self.get_zodiac_sign(month, day)
            except ValueError:
                print("正しい数値を入力してください。")
        
        print("\n占いたいカテゴリを選んでください：")
        print("-" * 30)
        
        # カテゴリのリストを表示
        categories = list(hadou_data.keys())
        categories.append("全カテゴリからランダム")
        
        for i, category in enumerate(categories):
            print(f"{i + 1}: {category}")
        
        # ユーザーにカテゴリを選択させる
        while True:
            try:
                choice = int(input("\n番号を選択してください: "))
                if 1 <= choice <= len(categories):
                    if choice == len(categories):
                        # 全カテゴリからランダム
                        all_codes = {}
                        for cat_data in hadou_data.values():
                            all_codes.update(cat_data)
                        selected_category_name = "全カテゴリ"
                        selected_category_data = all_codes
                    else:
                        selected_category_name = categories[choice - 1]
                        selected_category_data = hadou_data[selected_category_name]
                    break
                else:
                    print("正しい番号を入力してください。")
            except ValueError:
                print("番号を数値で入力してください。")
        
        # 選択されたカテゴリからランダムに一つ選ぶ
        random_code = random.choice(list(selected_category_data.keys()))
        random_hadou = selected_category_data[random_code]
        
        # 詳細なアドバイスを取得
        advice_data = self.get_detailed_advice(random_hadou)
        
        # 相性の良いタイプを計算
        compatible_type = self.calculate_compatibility(random_code)
        
        # バイオリズムを生成
        biorhythm = self.generate_biorhythm()
        
        # 結果の表示
        print("\n" + "="*50)
        print("🔮 占い結果 🔮".center(50))
        print("="*50)
        print(f"\n{name}さんの今日の波動")
        print("-" * 30)
        print(f"波動: 【{random_hadou}】")
        print(f"波動コード: {random_code}")
        print(f"カテゴリ: {selected_category_name}")
        
        if zodiac:
            print(f"星座: {zodiac}")
        
        print("\n📍 今日のアドバイス")
        print("-" * 30)
        print(f"{advice_data['advice']}")
        
        print("\n🍀 ラッキーアイテム")
        print("-" * 30)
        print(f"アイテム: {advice_data['lucky_item']}")
        print(f"ラッキーカラー: {advice_data['color']}")
        print(f"ラッキーナンバー: {advice_data['number']}")
        
        print("\n💑 相性の良いタイプ")
        print("-" * 30)
        print(f"今日のあなたと相性が良いのは【{compatible_type}】の人です")
        
        print("\n📊 今日のバイオリズム")
        print("-" * 30)
        print(f"身体: {'▓' * (biorhythm['physical'] // 10)}{'░' * (10 - biorhythm['physical'] // 10)} {biorhythm['physical']}%")
        print(f"感情: {'▓' * (biorhythm['emotional'] // 10)}{'░' * (10 - biorhythm['emotional'] // 10)} {biorhythm['emotional']}%")
        print(f"知性: {'▓' * (biorhythm['intellectual'] // 10)}{'░' * (10 - biorhythm['intellectual'] // 10)} {biorhythm['intellectual']}%")
        
        # 総合運勢
        total_luck = (biorhythm['physical'] + biorhythm['emotional'] + biorhythm['intellectual']) // 3
        stars = "★" * (total_luck // 20) + "☆" * (5 - total_luck // 20)
        print(f"\n⭐ 総合運勢: {stars}")
        
        print("\n" + "="*50)
        print("素敵な一日をお過ごしください！✨")
        print("="*50)
        
        # 履歴に保存
        result = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "hadou": random_hadou,
            "code": random_code,
            "category": selected_category_name,
            "total_luck": total_luck
        }
        self.save_history(result)
        
        # 追加機能の提案
        self.additional_features()
    
    def additional_features(self):
        """追加機能メニュー"""
        print("\n追加機能:")
        print("1: 占い履歴を見る")
        print("2: もう一度占う")
        print("3: 終了")
        
        choice = input("\n選択してください (1-3): ")
        
        if choice == "1":
            self.show_history()
        elif choice == "2":
            self.fortune_telling()
        elif choice == "3":
            print("\nまたのご利用をお待ちしております！🌟")
        else:
            print("\n終了します。")
    
    def show_history(self):
        """占い履歴を表示"""
        if not self.history:
            print("\nまだ占い履歴がありません。")
        else:
            print("\n📜 占い履歴")
            print("="*50)
            for i, record in enumerate(self.history[-5:], 1):  # 最新5件を表示
                print(f"\n{i}. {record['date']}")
                print(f"   名前: {record['name']}")
                print(f"   波動: {record['hadou']} ({record['code']})")
                print(f"   総合運勢: {'★' * (record['total_luck'] // 20)}{'☆' * (5 - record['total_luck'] // 20)}")
        
        self.additional_features()


def main():
    app = HadouFortuneApp()
    app.fortune_telling()


if __name__ == "__main__":
    main()
