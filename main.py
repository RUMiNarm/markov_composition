import json
import os
import re
from collections import defaultdict

FOLDER_PATH = "children_songs"  # メロディが保存されているフォルダ

# 音符リスト
NOTES = [
    "ド",
    "レ",
    "ミ",
    "ファ",
    "ソ",
    "ラ",
    "シ",
    "＃ド",
    "＃レ",
    "＃ミ",
    "＃ファ",
    "＃ソ",
    "＃ラ",
    "＃シ",
    "♭ド",
    "♭レ",
    "♭ミ",
    "♭ファ",
    "♭ソ",
    "♭ラ",
    "♭シ",
]

# 正規表現で音符を抽出
NOTE_PATTERN = re.compile("|".join(re.escape(note) for note in NOTES))


# フォルダ内のすべてのテキストファイルからメロディを読み込み
def load_all_melodies(folder_path):
    melodies = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                # 正規表現で音符を分割し、小節単位でリストを作成
                melodies.extend(
                    [NOTE_PATTERN.findall(line.strip()) for line in f.readlines()]
                )
    return melodies


# 遷移確率と遷移元の出現回数を計算
def build_transition_probabilities_with_counts(melody_data, n):
    transitions = defaultdict(lambda: defaultdict(int))
    prefix_counts = defaultdict(int)

    for measure in melody_data:
        if len(measure) < n + 1:
            continue  # 音符が少なすぎる小節はスキップ

        # 各小節内での遷移を記録
        for i in range(len(measure) - n):
            prefix = tuple(measure[i : i + n])  # 遷移元の長さをnに設定
            next_note = measure[i + n]
            transitions[prefix][next_note] += 1
            prefix_counts[prefix] += 1

    # 確率を計算
    probabilities = {}
    for prefix, next_notes in transitions.items():
        total = sum(next_notes.values())
        probabilities[prefix] = {
            next_note: count / total for next_note, count in next_notes.items()
        }

    # JSONに保存可能な形式に変換
    prefix_counts_json = {
        ",".join(prefix): count for prefix, count in prefix_counts.items()
    }
    probabilities_json = {
        ",".join(prefix): {next_note: prob for next_note, prob in next_notes.items()}
        for prefix, next_notes in probabilities.items()
    }

    return prefix_counts_json, probabilities_json


if __name__ == "__main__":
    # フォルダ内のすべてのテキストファイルからメロディを読み込む
    melody_data = load_all_melodies(FOLDER_PATH)

    # 遷移元の長さを指定（任意の数字を設定可能）
    n = int(input("遷移元の音符数を指定してください (例: 2): "))

    # 遷移確率と遷移元の出現回数を計算
    prefix_counts, transition_probabilities = (
        build_transition_probabilities_with_counts(melody_data, n)
    )

    # データを統合してJSONファイルに保存
    result = {
        "prefix_counts": prefix_counts,
        "transition_probabilities": transition_probabilities,
    }
    with open("transition_probabilities.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
