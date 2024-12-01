import json
import re
from collections import Counter, defaultdict


def parse_melody(file_path):
    # ファイルからメロディを読み込み、音符ごとに分割する
    with open(file_path, "r", encoding="utf-8") as file:
        melody = file.read().strip()

    # 正規表現で音符を定義
    pattern = r"(＃[ドレミファソラシ]|♭[ドレミファソラシ]|ド|レ|ミ|ファ|ソ|ラ|シ)"
    # 正規表現で定義した音符をテキストから抽出
    notes = re.findall(pattern, melody)
    return notes


# N個の音符を元に次の音符のタプル(リスト)を作成
def generate_ngrams(notes, n):
    ngrams = [(tuple(notes[i : i + n]), notes[i + n]) for i in range(len(notes) - n)]
    return ngrams


# N個の音符を元に次の音符の遷移確率を計算
def calculate_transition_probabilities(ngrams):
    # 音符の辞書を作成
    transitions = defaultdict(Counter)

    # prefix=N個の音符の組み合わせ, next_note=次の音
    for prefix, next_note in ngrams:
        # 出現回数をカウント
        transitions[prefix][next_note] += 1

    probabilities = {}
    # prefixごとの遷移確率を計算, counter=次の音符のカウント
    for prefix, counter in transitions.items():
        # total=次に来る音符の総出現数
        total = sum(counter.values())
        # 辞書形式で格納
        probabilities[prefix] = {note: count / total for note, count in counter.items()}

    # タプルのキーをJSON形式に文字列に変換
    probabilities = {
        ",".join(prefix): transitions for prefix, transitions in probabilities.items()
    }
    return probabilities


# データをJSONファイルに保存する
def save_to_json(data, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    file_path = "children_songs\Osakanatengoku.txt"
    n = int(input("N："))

    # メロディの読み込みと音符分割
    notes = parse_melody(file_path)
    print(f"\n音符のリスト: {notes}")

    # N-gramの生成
    ngrams = generate_ngrams(notes, n)
    print(f"\nN-gramのリスト: {ngrams}")

    # 遷移確率の計算
    probabilities = calculate_transition_probabilities(ngrams)

    # 遷移確率をJSONファイルに保存
    save_to_json(probabilities, "chain.json")

    # 遷移確率の結果を表示
    print("\n遷移確率:")
    for prefix, transitions in probabilities.items():
        print(f"{prefix}:")
        for note, prob in transitions.items():
            print(f"  {note}: {prob:.2f}")


if __name__ == "__main__":
    main()
