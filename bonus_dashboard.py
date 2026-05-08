# =============================================================================
# Padel Analytics — Bonus Task Dashboard (CLEAN VERSION)
# =============================================================================

import pandas as pd
import os

INPUT_CSV = "/Users/simrankumarigupta/padel-analytics/outputs/shot_results2.csv"
OUTPUT_HTML = "outputs/padel9_report.html"

SHOT_COLORS = {
    "FOREHAND": "#2ecc71",
    "BACKHAND": "#e67e22",
    "SMASH": "#e74c3c",
    "SERVE": "#9b59b6",
}


# ─────────────────────────────────────────────────────────────
# ANALYTICS
# ─────────────────────────────────────────────────────────────

def analyse_shots(df):

    shot_df = df[~df["shot"].isin(["BOUNCE", "SUMMARY"])].copy()
    bounce_df = df[df["shot"] == "BOUNCE"].copy()

    total_shots = len(shot_df)
    total_bounces = len(bounce_df)

    shot_totals = shot_df["shot"].value_counts().to_dict()

    fh_bh = {}

    for player in shot_df["player"].unique():

        pdf = shot_df[shot_df["player"] == player]

        fh = len(pdf[pdf["shot"] == "FOREHAND"])
        bh = len(pdf[pdf["shot"] == "BACKHAND"])

        fh_bh[player] = {
            "forehand": fh,
            "backhand": bh,
            "fh_ratio": round(fh / (fh + bh) * 100, 1) if (fh + bh) > 0 else 0,
        }

    timeline = {}

    if "timestamp_sec" in shot_df.columns:

        shot_df["window"] = (
            pd.to_numeric(shot_df["timestamp_sec"], errors="coerce") // 5 * 5
        ).astype("Int64")

        timeline = shot_df.groupby("window")["shot"].count().to_dict()

    return {
        "total_shots": total_shots,
        "total_bounces": total_bounces,
        "shot_totals": shot_totals,
        "fh_bh": fh_bh,
        "timeline": timeline,
    }


# ─────────────────────────────────────────────────────────────
# CONSOLE OUTPUT
# ─────────────────────────────────────────────────────────────

def print_analytics(stats):

    print("\n" + "=" * 50)
    print("PADEL ANALYTICS SUMMARY")
    print("=" * 50)

    print(f"\nTotal shots: {stats['total_shots']}")
    print(f"Total bounces: {stats['total_bounces']}")

    print("\nShot breakdown:")

    for shot, count in stats["shot_totals"].items():
        print(f"{shot:<12}: {count}")

    print("\nPlayer stats:")

    for player, d in stats["fh_bh"].items():
        print(
            f"{player:<12} FH={d['forehand']} BH={d['backhand']} FH%={d['fh_ratio']}"
        )


# ─────────────────────────────────────────────────────────────
# HTML REPORT (WITH LINE GRAPH ONLY)
# ─────────────────────────────────────────────────────────────

def produce_html_report(stats, output_html):

    player_rows = ""

    for player, d in stats["fh_bh"].items():

        total = d["forehand"] + d["backhand"]

        player_rows += f"""
        <tr>
            <td>{player}</td>
            <td>{d['forehand']}</td>
            <td>{d['backhand']}</td>
            <td>{d['fh_ratio']}%</td>
            <td>{total}</td>
        </tr>
        """

    # ─── LINE GRAPH DATA ─────────────────────────────
    tl_labels = [str(int(k)) + "s" for k in sorted(stats["timeline"].keys())]
    tl_values = [stats["timeline"][k] for k in sorted(stats["timeline"].keys())]

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Padel Analytics Report</title>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>

        <style>
            body {{
                font-family: Arial;
                padding: 30px;
                background: #f5f5f5;
            }}

            .card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th, td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}

            .chart-box {{
                width: 100%;
                height: 250px;
            }}
        </style>

    </head>

    <body>

        <div class="card">
            <h1>Padel Analytics Report</h1>
            <p>Total Shots: {stats['total_shots']}</p>
            <p>Total Bounces: {stats['total_bounces']}</p>
        </div>

        <!-- LINE GRAPH ONLY -->
        <div class="card">
            <h2>Shot Activity Over Time</h2>
            <div class="chart-box">
                <canvas id="timelineChart"></canvas>
            </div>
        </div>

        <div class="card">
            <h2>Shot Counts</h2>
            <ul>
                <li>Forehand: {stats['shot_totals'].get('FOREHAND',0)}</li>
                <li>Backhand: {stats['shot_totals'].get('BACKHAND',0)}</li>
                <li>Smash: {stats['shot_totals'].get('SMASH',0)}</li>
                <li>Serve: {stats['shot_totals'].get('SERVE',0)}</li>
            </ul>
        </div>

        <div class="card">
            <h2>Player Statistics</h2>
            <table>
                <tr>
                    <th>Player</th>
                    <th>Forehand</th>
                    <th>Backhand</th>
                    <th>FH%</th>
                    <th>Total</th>
                </tr>
                {player_rows}
            </table>
        </div>

        <script>
            new Chart(document.getElementById('timelineChart'), {{
                type: 'line',
                data: {{
                    labels: {tl_labels},
                    datasets: [{{
                        label: 'Shots per 5s',
                        data: {tl_values},
                        borderColor: '#2980b9',
                        backgroundColor: 'rgba(41,128,185,0.2)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 3
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }}
                    }}
                }}
            }});
        </script>

    </body>
    </html>
    """

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML report saved: {output_html}")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():

    if not os.path.exists(INPUT_CSV):
        print("CSV file not found")
        return

    df = pd.read_csv(INPUT_CSV)

    print(f"Loaded {len(df)} rows")

    stats = analyse_shots(df)

    print_analytics(stats)

    produce_html_report(stats, OUTPUT_HTML)

    print("\nBonus dashboard completed (NO VIDEO MODE)")


if __name__ == "__main__":
    main()