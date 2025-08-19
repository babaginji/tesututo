from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        answers = {}
        for i in range(1, 10):
            answers[f"Q{i}"] = request.form.get(f"Q{i}")

        # --- 診断ロジック ---
        q1, q2, q3 = answers["Q1"], answers["Q2"], answers["Q3"]
        q4, q5, q6 = answers["Q4"], answers["Q5"], answers["Q6"]
        q7, q8, q9 = answers["Q7"], answers["Q8"], answers["Q9"]

        result = "積立安定型（インデックスメイン）"  # デフォルト

        if q6 == "1倍以下" and q5 == "10%以下":
            result = "貯蓄優先型"
        elif q4 == "損をする覚悟もある" and q2 == "1年以内" and q3 == "1日1時間以上":
            result = "アクティブチャレンジ型（短期トレード型）"
        elif (q7 == "ある" or q8 == "ある") and q3 == "できるだけ手間かけたくない":
            result = "ステーキング運用型（仮想通貨積立・ステーキング）"
        elif (
            (q2 in ["3〜9年", "10年以上"])
            and (q3 in ["1日1時間以上", "週に数時間"])
            and (q4 in ["一時的に下がるのは我慢できる", "損をする覚悟もある"])
        ):
            result = "株式アクティブ型（中期〜長期の個別株投資）"
        elif q4 == "損をする覚悟もある" and q7 == "ある" and q3 in ["1日1時間以上", "週に数時間"]:
            result = "ハイリスクハイリターン型（仮想通貨トレード型）"
        elif (
            q8 == "ある"
            and q3 in ["1日1時間以上", "週に数時間"]
            and q4 in ["一時的に下がるのは我慢できる", "損をする覚悟もある"]
        ):
            result = "テクノロジー志向型（仮想通貨プロジェクト投資・新興市場）"
        elif q9 == "50代以上" and not (
            q1 == "一攫千金" or q4 == "損をする覚悟もある" or q3 == "1日1時間以上"
        ):
            result = "積立型（50代以上特別判定）"
        elif result == "積立安定型（インデックスメイン）" and q3 in ["1日1時間以上", "週に数時間"]:
            result = "積立応用型（高配当株など）"

        return render_template("result.html", result=result)

    # GET のときは通常ページ表示
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
