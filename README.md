# FUTU_Stop_Loss
A stock stop loss python program using FUTU API

###General Usage
    Please read 使用说明.pdf, chinese only.
    (p.s. 一般人会用富途来买股票的肯定也看得懂中文的吧）
    
###Develper
    Source codes are inside SourceCode folder, modify them as you like.


###Main Function
1. When a stock loss reach ¥n (RMB), program sold that stock for stop loss.
2. When the entire account loss/earn ¥n (RMB), Automatic clearance, and no more transactions can be made on the day.
3. All accounts are automatically sold before the noon closing (12:00) and before the afternoon closing (16:00). Account become an empty position.
4. This program only handle selling, no buying operation
