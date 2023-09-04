# MotionGenerator

# pyalterのインストール  
pyalterのソースもこのリポジトリに含めたので，ソースからインストールできます．　　
```terminal
cd pyalter
pip install -e pyalter  
```

# simulatorを起動  
ここからAlter Simulatorをダウンロードできます．(おそらく)　　
<https://drive.google.com/file/d/1GCROpRbKZ6dzvn_OGsFYrrjxS8ncEUGv/view?usp=sharing>  
その後，ダウンロードしたディレクトリに移動し，次のコマンドを実行.　　ダウンロードしたappファイルをアップルがリジェクトしないようにする呪文です．
```terminal
unzip Alter3Simulator.app.zip
xattr -rd com.apple.quarantine Alter3Simulator.app
open Alter3Simulator.app
```

# Motion Generation
Langchainとopenaiをインストールする必要があります．
```terminal
pip install openai
pip install langchain
```
コード汚いですが，とりあえず動きます．
### 生成には10分くらいかかります．
1. simulatorに接続 (IPとポートを確認)
2. action_inputに生成したい運動をかく.
3. 上から実行していってください．
4. 生成したコードはmotion_command.txtに保存されます．コピペしてsimulatorに流してください．
