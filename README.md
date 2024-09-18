### Pdf_dealer

完全处理不能读取只能ocr的pdf文档

### Hope

1. 各个模块分开

### 流程

1. pdf==>md
```启动了
nohup python z_utils/magic_pdf_server.py > magic_pdf_server.log &
nohup python z_utils/ocr_latex_server.py > ocr_latex_server.log &
```

### Env

```shell
vi .env
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

### Emoji

```
🤝🫶😊📌👉🙋‍♂️📋📘📕📙
🤖💡✨🔥🎉🚀🔧🎯💻📚🎨🎵🍀🌟
1️⃣2️⃣
🤔🤯😎🚀🤗💭📖📊📈💡🎯💪📅📝✅🎁🔍🧠🔗🎶📂📎💬🎓🔑🔒🛠️🛡️🔄💥🧲
🔬⚙️🌐📊📅🖥️📈🎮📱🎙️🖼️🌍🔑✨🎯🎨📷🎶📋🧱🏗️🏅🥇🔔🎉🍀🔋🔑🍀🧑‍💻
🤩🎧🎯🤟🍕🌮🍣🍜🦄🐉🌈🚁✈️🛶🚀🛸🪐🏔️🏖️🏜️🏕️🏝️🏰🗽🎢🎡🎠🛒📅🖊️🖍️
🖋🗂️📌📎💼🔋🛠️🧪🔬💻🖥️📱🔍💡🎓📝✏️🛡️🔗🔒🔑✨🚨🚥🚦🏗️🎉
🎁🎨🎵🎶📸🎥🖼️🔑🍀🧩🏆🎮🕹️🎯🚗🛵🚤⛴️🚲🚜🤖💻📊📈📂🔬🧬🥳
```