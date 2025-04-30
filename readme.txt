

# 元の Excel から 1列目(0), 3列目(2), 5列目(4)を抽出し、
# 抽出後の “売上” 列(1) と “コード”列(2) に欠損がある行を除外して
# output.csv に出力する

[UNIX]
excel_extract.exe input.xlsx output.csv \
  -i 0 2 4 \
  -n 日付 売上 コード \
  -d 1 2

[DOS]
excel_extract.exe pj.xlsx output.csv ^
  -i 1 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 ^
  -n pj company person class 1月 2月 3月 4月 5月 6月 7月 8月 9月 10月 11月 12月 ^
  -d 0 1 2 3


[PowerShell] 
excel_extract.exe .\pj.xlsx output.csv `
  -i 1 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 `
  -n pj company person class 1月 2月 3月 4月 5月 6月 7月 8月 9月 10月 11月 12月 `
  -d 0 1 2 3
