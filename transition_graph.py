import json

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# 日本語対応フォントを設定
matplotlib.rcParams["font.family"] = "MS Gothic"  # 使用可能な日本語フォントに置き換える

# 音階順のリスト（比較用）
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
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def prepare_heatmap_data(data):
    """
    遷移確率データをヒートマップ用のデータに整形
    遷移元を出現回数順に並べる
    """
    # 遷移元の出現回数を取得（タプルを適切に結合）
    prefix_counts = {
        ",".join(k.strip("()").split(", ")): v for k, v in data["prefix_counts"].items()
    }
    transition_probabilities = {
        ",".join(k.strip("()").split(", ")): v
        for k, v in data["transition_probabilities"].items()
    }

    # 遷移元を出現回数順に並べる
    sorted_prefixes = sorted(
        prefix_counts.keys(), key=lambda x: prefix_counts[x], reverse=True
    )

    # 全ての次の音符を列として設定
    all_next_notes = set()
    for transitions in transition_probabilities.values():
        all_next_notes.update(transitions.keys())

    # 音階順で並べる
    sorted_next_notes = sorted(
        all_next_notes,
        key=lambda x: NOTE_ORDER.index(x) if x in NOTE_ORDER else len(NOTE_ORDER),
    )

    # ヒートマップデータフレームを作成
    heatmap_data = pd.DataFrame(
        0, index=sorted_prefixes, columns=sorted_next_notes, dtype=float
    )

    for prefix, transitions in transition_probabilities.items():
        if prefix in heatmap_data.index:
            for next_note, prob in transitions.items():
                heatmap_data.loc[prefix, next_note] = prob

    return heatmap_data, prefix_counts


def plot_and_save_heatmap_in_chunks(
    heatmap_data, prefix_counts, output_file_base, max_rows=1000
):
    """
    ヒートマップを最大行数で分割して保存
    """
    num_rows, num_cols = heatmap_data.shape
    chunks = [heatmap_data.iloc[i : i + max_rows] for i in range(0, num_rows, max_rows)]

    for i, chunk in enumerate(chunks):
        output_file = f"{output_file_base}_part{i + 1}.png"
        fig_width = max(10, num_cols * 0.5)
        fig_height = max(10, len(chunk) * 0.5)

        plt.figure(figsize=(fig_width, fig_height))
        sns.heatmap(
            chunk,
            annot=False,  # 必要ならTrueにする
            fmt=".2f",
            cmap="Blues",
            cbar=True,
            linewidths=0.5,
        )
        plt.yticks(
            ticks=np.arange(len(chunk.index)) + 0.5,
            labels=[f"{prefix} ({prefix_counts[prefix]})" for prefix in chunk.index],
            rotation=0,
        )
        plt.title("遷移確率ヒートマップ", fontsize=16)
        plt.xlabel("次の音符", fontsize=12)
        plt.ylabel("遷移元（出現回数）", fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()

        # 保存
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        print(f"ヒートマップを画像として保存しました: {output_file}")

        plt.close()


def main():
    file_name = "chain.json"  # JSONファイル名
    output_file_base = "heatmap_sorted"  # 出力画像ファイル名のベース
    max_rows = 1000  # 一度に描画する最大行数

    # JSONデータを読み込み
    data = load_json(file_name)

    # ヒートマップデータを準備
    heatmap_data, prefix_counts = prepare_heatmap_data(data)

    # ヒートマップを分割して描画＆保存
    plot_and_save_heatmap_in_chunks(
        heatmap_data, prefix_counts, output_file_base, max_rows
    )


if __name__ == "__main__":
    main()
