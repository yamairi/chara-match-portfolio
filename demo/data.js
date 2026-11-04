const DEMO_DATA = {

  products: [

    {
      id: "product01",

      category: "食品・スイーツ",

      name: "Premium Cocoa Bites",

      price: "〜1,000円",

      target: "20代〜30代",

      keywords: [
        "ご褒美",
        "ギフト",
        "プレミアム",
        "SNS"
      ],

      description:
        "自分へのご褒美や小さなギフト需要を想定した架空のプレミアムスイーツ商品です。",

      customerSegments: [
        18,
        21,
        26,
        17,
        18
      ],


      types: [

        {
          name: "癒し・親しみ型",
          score: 92,
          compatibility: 88,
          expansion: 81
        },

        {
          name: "トレンド発信型",
          score: 84,
          compatibility: 78,
          expansion: 88
        },

        {
          name: "日常・ファミリー型",
          score: 78,
          compatibility: 82,
          expansion: 63
        },

        {
          name: "知的・カルチャー型",
          score: 70,
          compatibility: 68,
          expansion: 70
        },

        {
          name: "ゲーム・エンタメ型",
          score: 64,
          compatibility: 61,
          expansion: 69
        }

      ],


      characters: [

        {
          name: "Synthetic Character A",

          type: "癒し・親しみ型",

          score: 94,

          compatibility: 91,

          expansion: 84,

          unexpected: 72,

          reliability: "High",

          supporterSegments: [
            14,
            18,
            24,
            17,
            27
          ],

          tags: [
            "ご褒美需要",
            "SNS接点",
            "プレミアム層"
          ],

          reason:
            "現在顧客との親和性が高い一方、Segment Eにも相対的に支持者が多く、既存顧客強化と新しい顧客接点の両方を検討しやすい候補です。"
        },


        {
          name: "Synthetic Character B",

          type: "トレンド発信型",

          score: 91,

          compatibility: 80,

          expansion: 92,

          unexpected: 79,

          reliability: "High",

          supporterSegments: [
            10,
            15,
            24,
            16,
            35
          ],

          tags: [
            "話題化",
            "若年接点",
            "新市場開拓"
          ],

          reason:
            "Compatibilityは最上位ではありませんが、Segment Eへの広がりが大きく、認知拡大や話題化を目的とする施策仮説に向く候補です。"
        },


        {
          name: "Synthetic Character C",

          type: "日常・ファミリー型",

          score: 87,

          compatibility: 89,

          expansion: 67,

          unexpected: 61,

          reliability: "Medium",

          supporterSegments: [
            18,
            25,
            25,
            19,
            13
          ],

          tags: [
            "既存顧客強化",
            "日常接点",
            "安心感"
          ],

          reason:
            "現在の購買者構成と近く、既存顧客への自然な接点強化を重視する施策に向く候補です。"
        }

      ]
    },



    {
      id: "product02",

      category: "飲料",

      name: "Urban Tea Spark",

      price: "〜500円",

      target: "20代〜40代",

      keywords: [
        "爽快",
        "都会的",
        "持ち歩き",
        "軽やか"
      ],

      description:
        "仕事や外出時の気分転換を想定した架空のティードリンクです。",

      customerSegments: [
        15,
        20,
        28,
        22,
        15
      ],


      types: [

        {
          name: "知的・カルチャー型",
          score: 89,
          compatibility: 88,
          expansion: 79
        },

        {
          name: "トレンド発信型",
          score: 86,
          compatibility: 76,
          expansion: 90
        },

        {
          name: "癒し・親しみ型",
          score: 79,
          compatibility: 83,
          expansion: 68
        },

        {
          name: "ゲーム・エンタメ型",
          score: 72,
          compatibility: 69,
          expansion: 76
        },

        {
          name: "日常・ファミリー型",
          score: 68,
          compatibility: 75,
          expansion: 57
        }

      ],


      characters: [

        {
          name: "Synthetic Character D",

          type: "知的・カルチャー型",

          score: 92,

          compatibility: 90,

          expansion: 82,

          unexpected: 70,

          reliability: "High",

          supporterSegments: [
            12,
            18,
            31,
            21,
            18
          ],

          tags: [
            "知的イメージ",
            "都市生活",
            "王道"
          ],

          reason:
            "現在の商品購入者と支持者構成が近く、ブランドイメージを大きく変えずにコラボしやすい候補です。"
        },


        {
          name: "Synthetic Character E",

          type: "トレンド発信型",

          score: 89,

          compatibility: 78,

          expansion: 93,

          unexpected: 81,

          reliability: "High",

          supporterSegments: [
            8,
            14,
            25,
            24,
            29
          ],

          tags: [
            "トレンド",
            "SNS",
            "新市場"
          ],

          reason:
            "Segment Eへの支持が相対的に高く、新しいブランド接点や話題化を狙う場合に検討しやすい候補です。"
        },


        {
          name: "Synthetic Character F",

          type: "癒し・親しみ型",

          score: 83,

          compatibility: 85,

          expansion: 70,

          unexpected: 64,

          reliability: "Medium",

          supporterSegments: [
            17,
            21,
            27,
            19,
            16
          ],

          tags: [
            "親しみ",
            "日常",
            "安定"
          ],

          reason:
            "現在顧客との差が比較的小さく、日常的で親しみやすいコミュニケーションに向く候補です。"
        }

      ]

    },



    {
      id: "product03",

      category: "デジタルサービス",

      name: "Focus Note Plus",

      price: "月額〜1,000円",

      target: "20代〜40代",

      keywords: [
        "学習",
        "仕事",
        "効率",
        "記録"
      ],

      description:
        "学習・仕事のタスク整理を想定した架空のデジタルノートサービスです。",

      customerSegments: [
        10,
        17,
        31,
        24,
        18
      ],


      types: [

        {
          name: "知的・カルチャー型",
          score: 95,
          compatibility: 93,
          expansion: 84
        },

        {
          name: "ゲーム・エンタメ型",
          score: 83,
          compatibility: 76,
          expansion: 88
        },

        {
          name: "トレンド発信型",
          score: 80,
          compatibility: 71,
          expansion: 90
        },

        {
          name: "日常・ファミリー型",
          score: 68,
          compatibility: 70,
          expansion: 62
        },

        {
          name: "癒し・親しみ型",
          score: 63,
          compatibility: 65,
          expansion: 58
        }

      ],


      characters: [

        {
          name: "Synthetic Character G",

          type: "知的・カルチャー型",

          score: 96,

          compatibility: 95,

          expansion: 84,

          unexpected: 77,

          reliability: "High",

          supporterSegments: [
            8,
            14,
            35,
            25,
            18
          ],

          tags: [
            "学習",
            "知的",
            "高親和性"
          ],

          reason:
            "現在の商品利用者と支持者構成が近く、学習や仕事という利用文脈に自然に接続しやすい候補です。"
        },


        {
          name: "Synthetic Character H",

          type: "ゲーム・エンタメ型",

          score: 89,

          compatibility: 78,

          expansion: 92,

          unexpected: 82,

          reliability: "High",

          supporterSegments: [
            9,
            12,
            27,
            31,
            21
          ],

          tags: [
            "若年",
            "デジタル",
            "新市場"
          ],

          reason:
            "Segment Dへの支持が強く、現在顧客との接点を保ちながら新しい利用層へ広げる余地があります。"
        },


        {
          name: "Synthetic Character I",

          type: "トレンド発信型",

          score: 86,

          compatibility: 72,

          expansion: 94,

          unexpected: 85,

          reliability: "Medium",

          supporterSegments: [
            7,
            10,
            24,
            26,
            33
          ],

          tags: [
            "SNS",
            "話題化",
            "挑戦"
          ],

          reason:
            "既存顧客との一致より新しい顧客接点が特徴で、話題化やブランド拡張を目的とした探索的候補です。"
        }

      ]

    }

  ]

};
