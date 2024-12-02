import json

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 日本語対応フォントを設定
matplotlib.rcParams["font.family"] = "MS Gothic"  # 使用可能な日本語フォントに置き換える


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
    """
    rows = []
    columns = set()
    for prefix, transitions in data.items():
        columns.update(transitions.keys())  # 次の音符を列名に追加

    # 次の音符を列に統一
    columns = sorted(list(columns))
    heatmap_data = pd.DataFrame(0, index=data.keys(), columns=columns, dtype=float)

    # ヒートマップ用のデータを埋める
    for prefix, transitions in data.items():
        for note, prob in transitions.items():
            heatmap_data.loc[prefix, note] = prob

    return heatmap_data


def plot_and_save_heatmap(heatmap_data, output_file):
    """
    ヒートマップを描画して画像として保存
    """
    # 行と列の数に基づいてキャンバスサイズを調整
    num_rows, num_cols = heatmap_data.shape
    fig_width = max(10, num_cols * 0.5)  # 列数に応じて幅を調整
    fig_height = max(10, num_rows * 0.5)  # 行数に応じて高さを調整

    plt.figure(figsize=(fig_width, fig_height))
    sns.heatmap(
        heatmap_data,
        annot=True,  # 確率値を表示
        fmt=".2f",  # 小数点以下2桁でフォーマット
        cmap="Blues",  # カラーマップ
        cbar=True,  # カラーバーを表示
        linewidths=0.5,  # セルの境界線を設定
    )
    plt.title("遷移確率ヒートマップ", fontsize=16)
    plt.xlabel("次の音符", fontsize=12)
    plt.ylabel("現在の音符（N音）", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()

    # 画像として保存
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"ヒートマップを画像として保存しました: {output_file}")

    plt.close()


def main():
    file_name = "chain.json"  # JSONファイル名
    output_file = "heatmap_large.png"  # 出力画像ファイル名
    data = load_json(file_name)  # JSONファイルを読み込み
    heatmap_data = prepare_heatmap_data(data)  # ヒートマップ用データに整形
    plot_and_save_heatmap(heatmap_data, output_file)  # ヒートマップをプロットして保存


if __name__ == "__main__":
    main()
