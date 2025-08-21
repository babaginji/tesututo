from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-string"  # Render用に必ず安全な値へ

# 診断タイプごとの説明文
TYPE_DESCRIPTIONS = {
    "貯蓄優先型": "リスクを抑え、まずは貯蓄を優先する投資タイプです。安全性重視で少しずつ資産を増やすことを目指します。",
    "積立安定型（インデックスメイン）": "インデックス投資を中心に、長期で安定した資産形成を目指すタイプです。",
    "積立応用型（高配当株など）": "高配当株などを組み合わせ、安定と収益性のバランスを追求するタイプです。",
    "アクティブチャレンジ型（短期トレード型）": "短期売買でリターンを狙う、積極的な投資タイプです。リスクを取れる人向け。",
    "ステーキング運用型（仮想通貨積立・ステーキング）": "仮想通貨の積立やステーキングで資産を増やすタイプです。自動運用も可能。",
    "株式アクティブ型（中期〜長期の個別株投資）": "個別株を中期〜長期で運用するタイプです。企業分析や市場動向の学習が必要。",
    "ハイリスクハイリターン型（仮想通貨トレード型）": "大きなリターンを狙う反面、損失リスクも高い投資タイプです。",
    "テクノロジー志向型（仮想通貨プロジェクト投資・新興市場）": "新しい技術やプロジェクトに投資するタイプです。知識習得が重要。",
    "積立型（50代以上特別判定）": "50代以上向けのリスク控えめの積立型です。安全運用を重視します。",
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        answers = {f"Q{i}": request.form.get(f"Q{i}") for i in range(1, 10)}
        q1, q2, q3 = answers["Q1"], answers["Q2"], answers["Q3"]
        q4, q5, q6 = answers["Q4"], answers["Q5"], answers["Q6"]
        q7, q8, q9 = answers["Q7"], answers["Q8"], answers["Q9"]

        # --- メイン判定 ---
        main_result = "積立安定型（インデックスメイン）"  # デフォルト

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
    return render_template(
        "result_main.html", main_result=main_result, sub_result=sub_result
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
