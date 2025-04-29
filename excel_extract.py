import pandas as pd
import sys
import argparse

def extract_excel_columns_to_csv_by_index(
    input_excel_path: str,
    output_csv_path: str,
    column_indices_to_extract: list[int],
    column_names_to_assign: list[str] | None = None,
    dropna_indices: list[int] | None = None
) -> None:
    """
    Excelファイルを読み込み、指定した列番号の列を抽出し、
    必要に応じて特定の列で欠損行を除外してCSVファイルに保存する関数。

    Args:
        input_excel_path (str): 入力Excelファイルのパス (.xlsx または .xls)。
        output_csv_path (str): 出力CSVファイルのパス。
        column_indices_to_extract (list[int]): 抽出したい列のインデックス（番号）のリスト (0始まり)。
        column_names_to_assign (list[str] | None): 抽出後の列に付けたい列名のリスト。None の場合は元の列名を使用。
        dropna_indices (list[int] | None): 抽出後の DataFrame の列位置 (0 始まり) で、欠損行を除外する列インデックスのリスト。
    """
    try:
        print(f"'{input_excel_path}' を読み込み中...")
        df = pd.read_excel(input_excel_path)
        print("読み込み完了。")

        num_columns = df.shape[1]
        invalid_indices = [i for i in column_indices_to_extract if i < 0 or i >= num_columns]
        if invalid_indices:
            print(f"エラー: 以下の指定された列番号が無効です: {invalid_indices}")
            print(f"有効な列番号の範囲は 0 から {num_columns-1} までです。")
            sys.exit(1)

        print(f"指定された列 {column_indices_to_extract} を抽出中...")
        df_selected = df.iloc[:, column_indices_to_extract]
        print("抽出完了。")

        # 列名の置き換え
        if column_names_to_assign:
            if len(column_names_to_assign) != len(column_indices_to_extract):
                print(f"エラー: 列名の数 ({len(column_names_to_assign)}) が列番号の数 ({len(column_indices_to_extract)}) と一致しません。")
                sys.exit(1)
            df_selected.columns = column_names_to_assign

        # 指定列で欠損値を含む行を除外
        if dropna_indices is not None:
            # dropna_indices は抽出後 DataFrame の列位置
            max_idx = len(df_selected.columns) - 1
            invalid_drop = [i for i in dropna_indices if i < 0 or i > max_idx]
            if invalid_drop:
                print(f"エラー: dropna 用の列番号が無効です: {invalid_drop}")
                print(f"抽出後の列位置の範囲は 0 から {max_idx} までです。")
                sys.exit(1)
            subset_cols = [df_selected.columns[i] for i in dropna_indices]
            before = len(df_selected)
            df_selected = df_selected.dropna(subset=subset_cols)
            after = len(df_selected)
            print(f"欠損行の除外: {before-after} 行を削除しました。（残り {after} 行）")

        print(f"'{output_csv_path}' にCSVとして保存中...")
        df_selected.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
        print("保存完了。")

    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません '{input_excel_path}'")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"エラー: ファイル '{input_excel_path}' は空、または有効なデータを含みません。")
        sys.exit(1)
    except Exception as e:
        print(f"予期せぬエラー: {e} ({type(e).__name__})")
        sys.exit(1)

if __name__ == "__main__":
    print("--- Excelデータ抽出プログラム (列番号指定) ---")

    parser = argparse.ArgumentParser(
        description='Excelファイルから指定列を抽出し、オプションで特定列の欠損値行を除外してCSVに出力します。'
    )
    parser.add_argument(
        'input_excel',
        help='入力元のExcelファイル (.xlsx または .xls)'
    )
    parser.add_argument(
        'output_csv',
        help='出力先のCSVファイル'
    )
    parser.add_argument(
        '--indices', '-i',
        metavar='INDEX',
        type=int,
        nargs='+',
        required=True,
        help='抽出したい列番号リスト (0始まり)。例: -i 0 2 4'
    )
    parser.add_argument(
        '--names', '-n',
        metavar='NAME',
        type=str,
        nargs='+',
        help='各列に対応する列名リスト。--indices と同数指定'
    )
    parser.add_argument(
        '--dropna', '-d',
        metavar='INDEX',
        type=int,
        nargs='+',
        help='抽出後の DataFrame 列位置 (0始まり) で、欠損値を含む行を除外する列番号リスト。例: -d 1 2'
    )

    args = parser.parse_args()

    extract_excel_columns_to_csv_by_index(
        args.input_excel,
        args.output_csv,
        args.indices,
        args.names,
        dropna_indices=args.dropna
    )

    print("------------------------------------------")
