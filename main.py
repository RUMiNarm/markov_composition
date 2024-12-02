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
def build_markov_chain_by_position(melody_data):
    chains = {
        "start": defaultdict(lambda: defaultdict(int)),
        "middle": defaultdict(lambda: defaultdict(int)),
        "end": defaultdict(lambda: defaultdict(int)),
    }

    for measure in melody_data:
        if len(measure) < 2:
            continue  # 音符が少なすぎる小節はスキップ

        # 小節の最初の音符 -> 2つ目の音符
        chains["start"][measure[0]][measure[1]] += 1

        # 小節の途中の音符遷移
        for i in range(1, len(measure) - 1):
            chains["middle"][measure[i]][measure[i + 1]] += 1

        # 小節の最後の音符
        chains["end"][measure[-2]][measure[-1]] += 1

    # 確率を計算
    for chain in chains.values():
        for current, transitions in chain.items():
            total = sum(transitions.values())
            for next_note in transitions:
                transitions[next_note] /= total

    return chains


if __name__ == "__main__":
    # フォルダ内のすべてのテキストファイルからメロディを読み込む
    melody_data = load_all_melodies(FOLDER_PATH)

    # マルコフ連鎖を構築
    markov_chain = build_markov_chain_by_position(melody_data)

    # JSONファイルに保存
    with open("markov_chain.json", "w", encoding="utf-8") as f:
        json.dump(markov_chain, f, ensure_ascii=False, indent=4)
