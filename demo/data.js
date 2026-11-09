window.CHARA_MATCH_DATA = {
  segments: ["ライト層","実利志向層","トレンド層","プレミアム層","情報発信層"],
  groups: [
    {id:"healing",name:"癒し・親しみ型",description:"安心感・親しみやすさを軸に日常接点を作りやすいタイプ。"},
    {id:"daily",name:"日常・ファミリー型",description:"生活シーンに馴染みやすく幅広い層へ届きやすいタイプ。"},
    {id:"trend",name:"トレンド・話題型",description:"新商品・SNS・話題化との相性が高いタイプ。"},
    {id:"culture",name:"知的・カルチャー型",description:"学習・比較検討・世界観訴求と相性が高いタイプ。"},
    {id:"entertainment",name:"ゲーム・エンタメ型",description:"熱量・イベント・ファンダム文脈に強いタイプ。"}
  ],
  products: [
    {id:"p1",category:"食品・スイーツ",name:"ギフトチョコ",price:"〜1,500円",audience:"20代〜30代",keywords:["ご褒美","ギフト","甘い","写真映え"],segments:[18,21,24,19,18],scores:{healing:92,daily:77,trend:84,culture:61,entertainment:69}},
    {id:"p2",category:"飲料",name:"デイリーティー",price:"〜500円",audience:"30代〜50代",keywords:["日常","リフレッシュ","仕事中","手軽"],segments:[24,28,18,13,17],scores:{healing:79,daily:94,trend:63,culture:74,entertainment:57}},
    {id:"p3",category:"美容・ヘルスケア",name:"セルフケアミスト",price:"1,500〜3,000円",audience:"20代〜40代",keywords:["美容","セルフケア","携帯","香り"],segments:[14,17,27,23,19],scores:{healing:82,daily:66,trend:91,culture:73,entertainment:68}},
    {id:"p4",category:"日用品",name:"デスク収納アイテム",price:"1,000〜2,000円",audience:"20代〜40代",keywords:["整理","デスク","仕事","シンプル"],segments:[19,27,21,18,15],scores:{healing:67,daily:88,trend:64,culture:86,entertainment:60}},
    {id:"p5",category:"デジタルサービス",name:"学習サブスクリプション",price:"月額1,000〜2,000円",audience:"10代後半〜30代",keywords:["学習","継続","アプリ","スキル"],segments:[13,20,22,18,27],scores:{healing:60,daily:68,trend:79,culture:95,entertainment:75}}
  ],
  characters: [
    {id:"c1",name:"Synthetic Character A",group:"healing",compatibility:94,expansion:78,unexpected:11,reliability:"High",segments:[24,18,18,20,20]},
    {id:"c2",name:"Synthetic Character B",group:"healing",compatibility:91,expansion:71,unexpected:8,reliability:"High",segments:[27,19,16,17,21]},
    {id:"c3",name:"Synthetic Character C",group:"daily",compatibility:88,expansion:61,unexpected:5,reliability:"High",segments:[23,28,17,14,18]},
    {id:"c4",name:"Synthetic Character D",group:"trend",compatibility:73,expansion:93,unexpected:16,reliability:"Medium",segments:[12,14,32,18,24]},
    {id:"c5",name:"Synthetic Character E",group:"culture",compatibility:84,expansion:82,unexpected:9,reliability:"High",segments:[13,21,20,24,22]},
    {id:"c6",name:"Synthetic Character F",group:"entertainment",compatibility:70,expansion:88,unexpected:14,reliability:"Medium",segments:[13,16,26,17,28]},
    {id:"c7",name:"Synthetic Character G",group:"daily",compatibility:86,expansion:67,unexpected:4,reliability:"High",segments:[25,27,18,13,17]},
    {id:"c8",name:"Synthetic Character H",group:"trend",compatibility:79,expansion:89,unexpected:13,reliability:"Medium",segments:[10,14,28,27,21]},
    {id:"c9",name:"Synthetic Character I",group:"culture",compatibility:89,expansion:74,unexpected:7,reliability:"High",segments:[12,24,20,25,19]},
    {id:"c10",name:"Synthetic Character J",group:"entertainment",compatibility:76,expansion:91,unexpected:15,reliability:"Medium",segments:[14,15,27,16,28]}
  ],
  adjustments: {
    p1:{c1:[3,4],c2:[2,1],c4:[1,5],c8:[0,3]},
    p2:{c3:[4,1],c7:[5,2],c1:[1,-1],c9:[2,0]},
    p3:{c4:[4,3],c8:[3,5],c1:[1,2],c5:[0,2]},
    p4:{c7:[4,1],c9:[4,2],c3:[2,0],c5:[3,1]},
    p5:{c5:[5,3],c9:[4,2],c10:[1,4],c6:[0,3]}
  }
};
