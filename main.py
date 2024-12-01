import re
from collections import Counter, defaultdict


def parse_melody(file_path):
    """
    ファイルからメロディを読み込み、音符ごとに分割する
    """
    with open(file_path, "r", encoding="utf-8") as file:
        melody = file.read().strip()
    # 正規表現で音符を抽出する
    pattern = r"(＃[ドレミファソラシ]|ド|レ|ミ|ファ|ソ|ラ|シ)"
    notes = re.findall(pattern, melody)
    return notes


def generate_ngrams(notes, n):
    """
    N個の音符を元に次の音符を求めるためのデータを生成
    """
    ngrams = [(tuple(notes[i : i + n]), notes[i + n]) for i in range(len(notes) - n)]
    return ngrams


def calculate_transition_probabilities(ngrams):
    """
    N個の音符を元に次の音符の遷移確率を計算する
    """
    transitions = defaultdict(Counter)

    for prefix, next_note in ngrams:
        transitions[prefix][next_note] += 1

    probabilities = {}
    for prefix, counter in transitions.items():
        total = sum(counter.values())
        probabilities[prefix] = {note: count / total for note, count in counter.items()}

    return probabilities


def main():
    file_path = input("メロディのテキストファイルのパスを入力してください: ")
    n = int(input("Nの値を入力してください (例: 3): "))

    # メロディの読み込みと音符分割
    notes = parse_melody(file_path)
    print(f"\n音符のリスト: {notes}")

    # N-gramの生成 (N個の音符を元に次の音符を求める)
    ngrams = generate_ngrams(notes, n)
    print(f"\nN-gramのリスト: {ngrams}")

    # 遷移確率の計算
    probabilities = calculate_transition_probabilities(ngrams)

    # 遷移確率の結果を表示
    print("\n遷移確率:")
    for prefix, transitions in probabilities.items():
        print(f"{prefix}:")
        for note, prob in transitions.items():
            print(f"  {note}: {prob:.2f}")


if __name__ == "__main__":
    main()
