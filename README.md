# SigmaGO
## Description
這是受到AlphaGO、ZeelaGO、GNUGO等著名圍棋機器人啟發，開發的圍棋機器人。以沒有池化層(Pooling)的捲積神經網路(CNN)為主體，以[GymGO](https://github.com/aigagror/GymGo)為輔助，判斷此步是否合法。而訓練資料則是使用了超過34572個Sgf(Smartgameformat)檔案，並加以旋轉、翻轉、平移以製造出更多的變化。
