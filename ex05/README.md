# 第5回
## 負けるな！こうかとん（ex05/fight_kokaton.py）
### ゲーム概要
- ex05/fight_kokaton.pyを実行すると，1600x900のスクリーンに草原が描画され，こうかとんを移動させ飛び回る爆弾から逃げるゲーム
- こうかとんが爆弾と接触するとゲームオーバーで終了する
### 操作方法
- 矢印キーでこうかとんを上下左右に移動する
### 追加機能
- 爆弾を複数個にする
- 爆弾以外にも、こうかとん強化アイテムが飛び回る機能
- こうかとん強化アイテムである白い●に当たると、こうかとんが戦闘モードになる。以後爆弾に接触すると倒す（消す）ことができる
- テキスト生成クラスを実装、クラス内のblit関数で表示させることができる
- 着弾するとこうかとん画像が切り替わる
### 今回の追加機能
- こうかとんが敵を全員倒すとGEMECLEARが表示される
- GAMECLEAR時、クリアにかかった時間を表示する機能
- こうかとんの戦闘モードが一定時間で解除される
### ToDo（実装しようと思ったけど時間がなかった）
- [ ] 効果音の実施
- [ ] 強化アイテムを円ではなく、画像に
### メモ