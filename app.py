from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-string"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        answers = {f"Q{i}": request.form.get(f"Q{i}") for i in range(1, 10)}
        q1, q2, q3 = answers["Q1"], answers["Q2"], answers["Q3"]
        q4, q5, q6 = answers["Q4"], answers["Q5"], answers["Q6"]
        q7, q8, q9 = answers["Q7"], answers["Q8"], answers["Q9"]

        # --- メイン判定 ---
        main_result = "積立安定型（インデックスメイン）"

        if q6 == "1倍以下" and q5 == "10%以下":
            main_result = "貯蓄優先型"
        elif q4 == "損をする覚悟もある" and q2 == "1年以内" and q3 == "1日1時間以上":
            main_result = "アクティブチャレンジ型（短期トレード型）"
        elif (q7 == "ある" or q8 == "ある") and q3 == "できるだけ手間かけたくない":
            main_result = "ステーキング運用型（仮想通貨積立・ステーキング）"
        elif (
            q2 in ["3〜9年", "10年以上"]
            and q3 in ["1日1時間以上", "週に数時間"]
            and q4 in ["一時的に下がるのは我慢できる", "損をする覚悟もある"]
        ):
            main_result = "株式アクティブ型（中期〜長期の個別株投資）"
        elif q4 == "損をする覚悟もある" and q7 == "ある" and q3 in ["1日1時間以上", "週に数時間"]:
            main_result = "ハイリスクハイリターン型（仮想通貨トレード型）"
        elif (
            q8 == "ある"
            and q3 in ["1日1時間以上", "週に数時間"]
            and q4 in ["一時的に下がるのは我慢できる", "損をする覚悟もある"]
        ):
            main_result = "テクノロジー志向型（仮想通貨プロジェクト投資・新興市場）"
        elif q9 == "50代以上" and not (
            q1 == "一攫千金" or q4 == "損をする覚悟もある" or q3 == "1日1時間以上"
        ):
            main_result = "積立型（50代以上特別判定）"
        elif main_result == "積立安定型（インデックスメイン）" and q3 in ["1日1時間以上", "週に数時間"]:
            main_result = "積立応用型（高配当株など）"

        # --- サブ判定 ---
        if main_result == "貯蓄優先型":
            sub_result = "積立安定型（インデックスメイン）"
        elif main_result == "アクティブチャレンジ型（短期トレード型）":
            sub_result = "ハイリスクハイリターン型（仮想通貨トレード型）"
        elif main_result == "ステーキング運用型（仮想通貨積立・ステーキング）":
            sub_result = "積立安定型（インデックスメイン）"
        elif main_result == "株式アクティブ型（中期〜長期の個別株投資）":
            sub_result = "積立応用型（高配当株など）"
        elif main_result == "ハイリスクハイリターン型（仮想通貨トレード型）":
            sub_result = "アクティブチャレンジ型（短期トレード型）"
        elif main_result == "テクノロジー志向型（仮想通貨プロジェクト投資・新興市場）":
            sub_result = (
                "ステーキング運用型（仮想通貨積立・ステーキング）"
                if q3 == "できるだけ手間かけたくない"
                else "ハイリスクハイリターン型（仮想通貨トレード型）"
            )
        elif main_result == "積立型（50代以上特別判定）":
            sub_result = (
                "積立安定型（インデックスメイン）" if q3 == "できるだけ手間かけたくない" else "積立応用型（高配当株など）"
            )
        elif main_result == "積立応用型（高配当株など）":
            sub_result = "積立安定型（インデックスメイン）"
        else:
            sub_result = "積立安定型（インデックスメイン）"

        session["main_result"] = main_result
        session["sub_result"] = sub_result

        return redirect(url_for("result_main"))

    return render_template("index.html")


@app.route("/result")
def result_main():
    main_result = session.get("main_result")
    sub_result = session.get("sub_result")
    if not main_result:
        return redirect(url_for("index"))

    descriptions = {
        "貯蓄優先型": "リスクを抑えて安全に資産を増やすタイプです。",
        "積立安定型（インデックスメイン）": "長期でコツコツ投資し、安定的なリターンを目指します。",
        "アクティブチャレンジ型（短期トレード型）": "短期的な利益を狙うチャレンジ型の投資家です。",
        "ステーキング運用型（仮想通貨積立・ステーキング）": "仮想通貨を積立てつつ、ステーキングで利息を得る運用型です。",
        "株式アクティブ型（中期〜長期の個別株投資）": "中長期で個別株を分析して投資するタイプです。",
        "ハイリスクハイリターン型（仮想通貨トレード型）": "高リスクだが大きなリターンを狙う投資型です。",
        "テクノロジー志向型（仮想通貨プロジェクト投資・新興市場）": "新技術や新興市場に積極的に投資するタイプです。",
        "積立型（50代以上特別判定）": "年齢に合わせて無理のない積立型投資です。",
        "積立応用型（高配当株など）": "高配当株や応用投資でリスク分散を図るタイプです。",
    }

    main_desc = descriptions.get(main_result, "")
    sub_desc = descriptions.get(sub_result, "")

    return render_template(
        "result_main.html",
        main_result=main_result,
        sub_result=sub_result,
        main_desc=main_desc,
        sub_desc=sub_desc,
    )


@app.route("/result/books")
def result_books():
    main_result = session.get("main_result")
    sub_result = session.get("sub_result")
    if not main_result:
        return redirect(url_for("index"))
    return render_template(
        "result_books.html", main_result=main_result, sub_result=sub_result
    )


@app.route("/result/start")
def result_start():
    main_result = session.get("main_result")
    sub_result = session.get("sub_result")
    if not main_result:
        return redirect(url_for("index"))
    return render_template(
        "result_start.html", main_result=main_result, sub_result=sub_result
    )


@app.route("/result/learning")
def result_learning():
    main_result = session.get("main_result")
    sub_result = session.get("sub_result")
    if not main_result:
        return redirect(url_for("index"))
    return render_template(
        "result_learning.html", main_result=main_result, sub_result=sub_result
    )


if __name__ == "__main__":
    app.run(debug=True)
