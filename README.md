### Pdf_dealer

完全处理不能读取只能ocr的pdf文档

### Hope

1. 各个模块分开

### 流程

1. pdf==>picsA
2. picsA==>picsB(旋转图片为阅读方向)
3. picsB==>ansA:txt+picsC+table(OCR识别图片提取 标准文字+表格图片+纯图片+表格)
4. ansA==>entityA(提取实体)
5. entityA==>show_data(实体展示)

### Env

```shell
conda create -n pdf_dealer python=3.11 -y
conda activate pdf_dealer
pip install -r requirements.txt
```

### Test

```shell
# 翻译文档

```

### Prompt

```
工厂模式
```
