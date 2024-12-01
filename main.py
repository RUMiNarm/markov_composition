import re
from collections import Counter


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
    N-gramを生成する
    """
    ngrams = [tuple(notes[i : i + n]) for i in range(len(notes) - n + 1)]
    return ngrams


def analyze_ngrams(ngrams, top_k=None):
    """
    N-gramの頻度を集計し、上位top_k個を返す
    """
    ngram_counts = Counter(ngrams)
    if top_k:
        return ngram_counts.most_common(top_k)
    return ngram_counts.most_common()


def main():
    file_path = input("メロディのテキストファイルのパスを入力してください: ")
    n = int(input("Nの値を入力してください (例: 2): "))
    top_k = input(
        "注目する上位の音数を指定してください (例: 5, すべて表示する場合はEnter): "
    )
    top_k = int(top_k) if top_k.isdigit() else None

    # メロディの読み込みと音符分割
    notes = parse_melody(file_path)
    print(f"\n音符のリスト: {notes}")

    # N-gramの生成
    ngrams = generate_ngrams(notes, n)
    print(f"\nN-gramのリスト: {ngrams}")

    # N-gramの頻度分析
    ngram_counts = analyze_ngrams(ngrams, top_k)

    # 結果を表示
    print("\nN-gram頻度ランキング:")
    for ngram, count in ngram_counts:
        print(f"{ngram}: {count}回")


if __name__ == "__main__":
    main()
