# SigmaGO
## Description
這是受到AlphaGO、ZeelaGO、GNUGO等著名圍棋機器人啟發，開發的圍棋機器人。以沒有池化層(Pooling)的捲積神經網路(CNN)為主體，以[GymGO](https://github.com/aigagror/GymGo)為輔助，判斷此步是否合法。而訓練資料則是使用了超過34572個[Sgf(Smartgameformat)檔案](https://github.com/ymgaq/Pyaq)，並加以旋轉、翻轉、平移以製造出更多的變化。在訓練50000多次後，將當局棋勢丟入模型，產出81格中，每一格的機率，如下圖:![下載 (4)](https://github.com/tudohuang/SigmaGO/assets/88125758/78a80e12-458f-40ab-b07d-cefe9fc9f384)

接著再以[Softmax算法](https://zh.wikipedia.org/zh-tw/Softmax%E5%87%BD%E6%95%B0)取出最大值，將矩陣座標轉換成圍棋棋盤座標，以[GTP(Go Text Protocol)](https://www.gnu.org/software/gnugo/gnugo_19.html)輸出，使用以Electron打造的[Sabaki](https://github.com/SabakiHQ/Sabaki)，與人類、機器人進行對戰。

## How to use?
在整個Repository中，有三個重要的檔案，```requirments.txt```、```sigmago.py```、```eval/eval1.py```
- requirments.txt:
模組列表
```bash
pip install -r requirments.txt
```
- sigmago.py:
主體程式
```bash
python sigmago.py -m 模型位置
```
- eval1.py
評估: 使用GNUGO level n級;與sigmago下50×2(黑/白)場
```bash
python eval1.py n
```
## Connect with Sabaki:
### 第一步設定:
![](https://github.com/tudohuang/SigmaGO/assets/88125758/88ab7894-14f0-4508-bd32-3381cd91f05a)
### 第二步開始對奕;人vs機/機vs機
![124g](https://github.com/tudohuang/SigmaGO/assets/88125758/81c107ab-33c9-4e7b-b685-2432bde71313)

如果設定機vs機，按下F5可以開始兩者對奕;如果人(黑)vs機(白)，直接下一子，機器也會跟著動;如果機器持黑，右建引擎列表的該引擎(Generative mode)，就會落第一子，之後就會如上。

## 努力方向:
實作Value network以及演算法輔助Minimax/MCTS，以達到更高的水平。目前與GNUGO勝率:![](https://github.com/tudohuang/SigmaGO/assets/88125758/282761af-2b1a-4488-9df7-2d99c6619c48)
可以看到，在Level5之後，就失去了過半的勝率。如何提高勝率，是目前重要的課題。

## 目標:
希望可以參與2024年的TCGA(台灣電腦對局協會)所舉辦的電腦對局競賽，以增加經驗、拓增視野。

## License
本專案使用 [GPL3.0](https://github.com/tudohuang/SigmaGO/blob/main/LICENSE) License

## Reference
- Sabaki: https://github.com/SabakiHQ/Sabaki
- GTP/GNUGO: https://www.gnu.org
- 34572個sgf檔案: https://github.com/ymgaq/Pyaq
- 參考書籍: 深度學習與圍棋(簡中版本) https://www.tenlong.com.tw/products/9787115551467
