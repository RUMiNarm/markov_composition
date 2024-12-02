import json
import os
import re
from collections import Counter, defaultdict


# 指定されたフォルダ内のすべてのテキストファイルを読み込む
def read_all_files(folder_path):
    melodies = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                melody = file.read().strip()
                melodies.append(melody)
    return melodies


def parse_melody(melody):
    # 正規表現で音符を定義
    pattern = r"(＃ファ|＃ド|＃レ|＃ミ|＃ソ|＃ラ|＃シ|♭ファ|♭ド|♭レ|♭ミ|♭ソ|♭ラ|♭シ|ファ|ド|レ|ミ|ソ|ラ|シ)"
    # 正規表現で定義した音符をテキストから抽出
    notes = re.findall(pattern, melody)
    return notes


# N個の音符を元に次の音符のタプル(リスト)を作成
def generate_ngrams_from_all(melodies, n):
    ngrams = []
    for melody in melodies:
        notes = parse_melody(melody)
        ngrams.extend(
            [(tuple(notes[i : i + n]), notes[i + n]) for i in range(len(notes) - n)]
        )
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
        ",".join(prefix): {note: prob for note, prob in next_notes.items()}
        for prefix, next_notes in probabilities.items()
    }
    return probabilities


# データをJSONファイルに保存する
def save_to_json(data, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    folder_path = "children_songs"
    n = int(input("N："))

    # メロディの読み込みと音符分割
    melodies = read_all_files(folder_path)
    print(f"\n音符のリスト: {melodies}")

    # N-gramの生成
    ngrams = generate_ngrams_from_all(melodies, n)
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
