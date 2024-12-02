import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 日本語対応フォントを設定
plt.rcParams["font.family"] = "MS Gothic"  # 環境に応じて適切な日本語フォントを指定

# 音階順のリスト
NOTE_ORDER = [
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


def load_json(file_name):
    """
    JSONファイルを読み込む
    """
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)


def prepare_heatmap_data(data, position):
    """
    遷移確率データをヒートマップ用のデータに整形
    """
    transition_data = data[position]

    # 全ての音符を行・列として設定
    all_notes = set()
    for current, transitions in transition_data.items():
        all_notes.add(current)
        all_notes.update(transitions.keys())

    # 音階順にソート
    sorted_notes = sorted(
        all_notes,
        key=lambda x: NOTE_ORDER.index(x) if x in NOTE_ORDER else len(NOTE_ORDER),
    )

    # データフレームを作成
    heatmap_data = pd.DataFrame(
        0, index=sorted_notes, columns=sorted_notes, dtype=float
    )

    for current, transitions in transition_data.items():
        for next_note, prob in transitions.items():
            heatmap_data.loc[current, next_note] = prob

    return heatmap_data


def plot_heatmap(heatmap_data, title, output_file):
    """
    ヒートマップをプロットして保存
    """
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        heatmap_data,
        annot=True,  # 確率値を表示
        fmt=".2f",  # 小数点以下2桁でフォーマット
        cmap="Blues",  # カラーマップ
        cbar=True,  # カラーバーを表示
        linewidths=0.5,  # セルの境界線を設定
    )
    plt.title(title, fontsize=16)
    plt.xlabel("次の音符", fontsize=12)
    plt.ylabel("現在の音符", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    # 画像として保存
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"ヒートマップを保存しました: {output_file}")


def main():
    json_file = "markov_chain.json"  # 入力JSONファイル名
    data = load_json(json_file)

    # 各位置のヒートマップを作成
    for position, title in zip(
        ["start", "middle", "end"],
        ["小節の最初の遷移確率", "小節の途中の遷移確率", "小節の最後の遷移確率"],
    ):
        heatmap_data = prepare_heatmap_data(data, position)
        output_file = f"heatmap_{position}.png"
        plot_heatmap(heatmap_data, title, output_file)


if __name__ == "__main__":
    main()
