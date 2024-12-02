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


# 遷移辞書を作成
def build_transition_probabilities(melody_data):
    transitions = defaultdict(lambda: defaultdict(int))

    for measure in melody_data:
        if len(measure) < 2:
            continue  # 音符が少なすぎる小節はスキップ

        # 各小節内での音符の遷移を記録
        for i in range(len(measure) - 1):
            transitions[measure[i]][measure[i + 1]] += 1

    # 確率を計算
    probabilities = {}
    for current, next_notes in transitions.items():
        total = sum(next_notes.values())
        probabilities[current] = {
            next_note: count / total for next_note, count in next_notes.items()
        }

    return probabilities


if __name__ == "__main__":
    # フォルダ内のすべてのテキストファイルからメロディを読み込む
    melody_data = load_all_melodies(FOLDER_PATH)

    # 遷移確率を計算
    transition_probabilities = build_transition_probabilities(melody_data)

    # JSONファイルに保存
    with open("transition_probabilities.json", "w", encoding="utf-8") as f:
        json.dump(transition_probabilities, f, ensure_ascii=False, indent=4)
