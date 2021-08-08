# orange
神経衰弱のオンラインゲーム<br>
a～rのアルファベットのカードを2枚ずつ用意し，同じアルファベットのカードめくった場合，カードを獲得できる<br>
フレームワークはDjango，サーバはPythonAnywhereを使用<br>
acount：ユーザー名<br>
entry：ログインしているユーザーの人数<br>
turn：1，2の場合，操作できる。3，100の場合，loadボタンをクリックし，相手にターンを渡す<br>
      0：操作できない，1：1枚目のカードを選択できる，2：2枚目のカードを選択できる<br>
      3：カードのアルファベットが間違っている，100：合っている<br>
enemy：ユーザー名：ユーザーの対戦相手<br>
get：獲得したカードのアルファベット<br>

https://user-images.githubusercontent.com/76951687/128636240-6a59e18a-937e-49ce-9cbc-08e401829dce.mov

同時に複数の対戦可能（撮影は同時にできませんでしたが，同じ時間帯に対戦しています）<br>

https://user-images.githubusercontent.com/76951687/124150621-afa5e300-dacc-11eb-9026-f7457f8ecae2.mp4

https://user-images.githubusercontent.com/76951687/124150880-f267bb00-dacc-11eb-89ba-c918d88b7536.mp4

https://user-images.githubusercontent.com/76951687/124151025-15926a80-dacd-11eb-8372-0e57c96c8bbf.mp4
