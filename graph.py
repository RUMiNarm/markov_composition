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


def prepare_heatmap_data(data):
    """
    遷移確率データと出現回数をヒートマップ用のデータに整形
    """
    probabilities = data["transition_probabilities"]
    prefix_counts = data["prefix_counts"]

    # 全ての音符を列として設定
    all_next_notes = set()
    for transitions in probabilities.values():
        all_next_notes.update(transitions.keys())

    # 音階順にソート
    sorted_next_notes = sorted(
        all_next_notes,
        key=lambda x: NOTE_ORDER.index(x) if x in NOTE_ORDER else len(NOTE_ORDER),
    )

    # Y軸（遷移元）を出現回数順にソート
    sorted_prefixes = sorted(
        prefix_counts.keys(), key=lambda x: prefix_counts[x], reverse=True
    )

    # データフレームを作成
    heatmap_data = pd.DataFrame(
        0, index=sorted_prefixes, columns=sorted_next_notes, dtype=float
    )

    for prefix, transitions in probabilities.items():
        for next_note, prob in transitions.items():
            heatmap_data.loc[prefix, next_note] = prob

    return heatmap_data, prefix_counts


def plot_heatmap(heatmap_data, prefix_counts, title, output_file):
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
    # Y軸ラベルに出現回数を追加
    plt.yticks(
        ticks=range(len(heatmap_data.index)),
        labels=[f"{prefix} ({prefix_counts[prefix]})" for prefix in heatmap_data.index],
        rotation=0,
    )
    plt.title(title, fontsize=16)
    plt.xlabel("次の音符", fontsize=12)
    plt.ylabel("遷移元（出現回数）", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    # 画像として保存
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"ヒートマップを保存しました: {output_file}")


def main():
    json_file = "transition_probabilities.json"  # 入力JSONファイル名
    data = load_json(json_file)

    # ヒートマップを作成
    heatmap_data, prefix_counts = prepare_heatmap_data(data)
    plot_heatmap(
        heatmap_data, prefix_counts, "遷移確率ヒートマップ", "heatmap_sorted.png"
    )


if __name__ == "__main__":
    main()
