# 学習する場合
via_to_png_script.pyを動かして学習データを生成、train.pyで学習する

### viaファイルからpng画像を切り出して保存する
```
python via_to_png.py\
  --json_filepath annotation_tool/sample_data/via_project_test.json\
  --jpg_filepath annotation_tool/sample_data/test.jpg
```

### viaファイルにアノテーションすべき領域を付与する
```
python update_via_region.py\
  --target_json_filepath via_project.json\
  --source_json_filepath annotation_tool/sample_data/via_project_test2.json\
  --output_dirpath tmp
```

### 教師データ生成

```
via_to_png_script.py
```
