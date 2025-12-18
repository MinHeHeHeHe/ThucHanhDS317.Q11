import streamlit as st
import textwrap
import streamlit.components.v1 as components
from modules.theme_system import get_theme_colors


def show(theme="Dark"):
    colors = get_theme_colors(theme)

    # auto text color theo theme
    is_dark = str(theme).lower() == "dark"
    td_text = "#E9EEF6" if is_dark else "#111827"
    td_muted = "#B9C2CF" if is_dark else "#374151"
    td_border = "rgba(255,255,255,0.14)" if is_dark else "rgba(0,0,0,0.12)"
    wrap_bg = "rgba(255,255,255,0.04)" if is_dark else "rgba(0,0,0,0.03)"

    # Inject CSS for normal Markdown (outside iframe)
    st.markdown(
        """
        <style>
            div[data-testid="stMarkdownContainer"] p,
            div[data-testid="stMarkdownContainer"] li {
                font-size: 18px !important;
                line-height: 1.6 !important;
            }
            div[data-testid="stMarkdownContainer"] h3 {
                font-size: 24px !important;
                margin-top: 1.5rem !important;
            }
            div[data-testid="stMarkdownContainer"] strong {
                font-weight: 700 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # DATA (9 models)
    # =========================
    models = [
        {
            "model": "RandomForest",
            "params": [
                "n_estimators: 500",
                "min_samples_split: 10",
                "min_samples_leaf: 4",
                "max_depth: 20",
                "bootstrap: False",
            ],
            "tests": [
                {"acc": 0.8776, "prec": 0.9419, "rec": 0.9181, "f1": 0.9299, "auc": 0.8987},
                {"acc": 0.8754, "prec": 0.9132, "rec": 0.9492, "f1": 0.9309, "auc": 0.8792},
                {"acc": 0.8752, "prec": 0.9124, "rec": 0.9499, "f1": 0.9308, "auc": 0.8948},
                {"acc": 0.9021, "prec": 0.9409, "rec": 0.9488, "f1": 0.9448, "auc": 0.9490},
                {"acc": 0.9364, "prec": 0.9872, "rec": 0.9402, "f1": 0.9631, "auc": 0.9835},
            ],
            "avg": {"acc": 0.8933, "prec": 0.7320, "rec": 0.7340, "f1": 0.7320, "auc": 0.9210},
        },
        {
            "model": "XGBoost",
            "params": [
                "learning_rate: 0.05",
                "max_depth: 8",
                "min_child_weight: 1",
                "n_estimators: 500",
                "subsample: 0.8",
                "scaler: RobustScaler()",
            ],
            "tests": [
                {"acc": 0.8819, "prec": 0.6974, "rec": 0.6081, "f1": 0.6333, "auc": 0.8087},
                {"acc": 0.8764, "prec": 0.6814, "rec": 0.6198, "f1": 0.6408, "auc": 0.8148},
                {"acc": 0.8755, "prec": 0.6862, "rec": 0.6464, "f1": 0.6625, "auc": 0.8663},
                {"acc": 0.9234, "prec": 0.8071, "rec": 0.8491, "f1": 0.8261, "auc": 0.9630},
                {"acc": 0.9352, "prec": 0.8240, "rec": 0.9286, "f1": 0.8652, "auc": 0.9844},
            ],
            "avg": {"acc": 0.8985, "prec": 0.7400, "rec": 0.7320, "f1": 0.7260, "auc": 0.8874},
        },
        {
            "model": "ANN-LSTM",
            "params": [],
            "tests": [
                {"acc": 0.7988, "prec": 0.9542, "rec": 0.8111, "f1": 0.8769, "auc": 0.8590},
                {"acc": 0.8472, "prec": 0.9496, "rec": 0.8733, "f1": 0.9099, "auc": 0.8823},
                {"acc": 0.8725, "prec": 0.9650, "rec": 0.8878, "f1": 0.9248, "auc": 0.9276},
                {"acc": 0.9006, "prec": 0.9800, "rec": 0.9060, "f1": 0.9416, "auc": 0.9612},
                {"acc": 0.9034, "prec": 0.9893, "rec": 0.9004, "f1": 0.9428, "auc": 0.9747},
            ],
            "avg": {"acc": 0.8645, "prec": 0.7140, "rec": 0.8260, "f1": 0.7480, "auc": 0.9210},
        },
        {
            "model": "Linear SVM",
            "params": [
                "C: 1",
                "class_weight: balanced",
            ],
            "tests": [
                {"acc": 0.5809, "prec": 0.9520, "rec": 0.5535, "f1": 0.7000, "auc": 0.7241},
                {"acc": 0.3164, "prec": 0.9620, "rec": 0.2354, "f1": 0.3783, "auc": 0.6769},
                {"acc": 0.4482, "prec": 0.9260, "rec": 0.4080, "f1": 0.5664, "auc": 0.6657},
                {"acc": 0.6291, "prec": 0.9441, "rec": 0.6166, "f1": 0.7460, "auc": 0.7170},
                {"acc": 0.7468, "prec": 0.9587, "rec": 0.7455, "f1": 0.8387, "auc": 0.8287},
            ],
            "avg": {"acc": 0.5443, "prec": 0.5680, "rec": 0.6500, "f1": 0.4720, "auc": 0.7225},
        },
        {
            "model": "LightGBM",
            "params": [
                "learning_rate: 0.05",
                "max_depth: -1",
                "n_estimators: 200",
                "num_leaves: 63",
            ],
            "tests": [
                {"acc": 0.8583, "prec": 0.9113, "rec": 0.9302, "f1": 0.9206, "auc": 0.8069},
                {"acc": 0.8603, "prec": 0.9137, "rec": 0.9296, "f1": 0.9216, "auc": 0.8097},
                {"acc": 0.8661, "prec": 0.9224, "rec": 0.9263, "f1": 0.9244, "auc": 0.8839},
                {"acc": 0.9089, "prec": 0.9552, "rec": 0.9409, "f1": 0.9480, "auc": 0.9467},
                {"acc": 0.9309, "prec": 0.9898, "rec": 0.9314, "f1": 0.9597, "auc": 0.9842},
            ],
            "avg": {"acc": 0.8849, "prec": 0.7120, "rec": 0.7300, "f1": 0.7180, "auc": 0.8863},
        },
        {
            "model": "LSTM",
            "params": [],
            "tests": [
                {"acc": 0.8764, "prec": 0.8863, "rec": 0.9867, "f1": 0.9338, "auc": 0.6060},
                {"acc": 0.8821, "prec": 0.8934, "rec": 0.9839, "f1": 0.9365, "auc": 0.6776},
                {"acc": 0.9034, "prec": 0.9279, "rec": 0.9657, "f1": 0.9464, "auc": 0.8149},
                {"acc": 0.9174, "prec": 0.9559, "rec": 0.9503, "f1": 0.9531, "auc": 0.9075},
                {"acc": 0.8883, "prec": 0.9713, "rec": 0.9001, "f1": 0.9343, "auc": 0.9333},
            ],
            "avg": {"acc": 0.8935, "prec": 0.7180, "rec": 0.6840, "f1": 0.6740, "auc": 0.7879},
        },
        {
            "model": "CatBoost",
            "params": [
                "depth: 6",
                "learning_rate: 0.05",
            ],
            "tests": [
                {"acc": 0.8946, "prec": 0.8970, "rec": 0.9950, "f1": 0.9435, "auc": 0.8196},
                {"acc": 0.8902, "prec": 0.8925, "rec": 0.9956, "f1": 0.9412, "auc": 0.7708},
                {"acc": 0.8907, "prec": 0.8926, "rec": 0.9960, "f1": 0.9415, "auc": 0.8275},
                {"acc": 0.9239, "prec": 0.9226, "rec": 0.9975, "f1": 0.9586, "auc": 0.9642},
                {"acc": 0.9548, "prec": 0.9572, "rec": 0.9933, "f1": 0.9749, "auc": 0.9753},
            ],
            "avg": {"acc": 0.9108, "prec": 0.8710, "rec": 0.6326, "f1": 0.6621, "auc": 0.8715},
        },
        {
            "model": "KNN",
            "params": [],
            "tests": [
                {"acc": 0.8942, "prec": 0.9072, "rec": 0.9806, "f1": 0.9424, "auc": 0.8358},
                {"acc": 0.8957, "prec": 0.9010, "rec": 0.9908, "f1": 0.9437, "auc": 0.7803},
                {"acc": 0.9044, "prec": 0.9071, "rec": 0.9936, "f1": 0.9484, "auc": 0.8357},
                {"acc": 0.9222, "prec": 0.9271, "rec": 0.9898, "f1": 0.9574, "auc": 0.9315},
                {"acc": 0.9378, "prec": 0.9514, "rec": 0.9796, "f1": 0.9653, "auc": 0.9522},
            ],
            "avg": {"acc": 0.9109, "prec": 0.8396, "rec": 0.6610, "f1": 0.6994, "auc": 0.8671},
        },
        {
            "model": "TabNet",
            "params": [],
            "tests": [
                {"acc": 0.8881, "prec": 0.9306, "rec": 0.9437, "f1": 0.9371, "auc": 0.8812},
                {"acc": 0.8978, "prec": 0.9195, "rec": 0.9692, "f1": 0.9437, "auc": 0.8788},
                {"acc": 0.9238, "prec": 0.9420, "rec": 0.9737, "f1": 0.9576, "auc": 0.9261},
                {"acc": 0.9376, "prec": 0.9479, "rec": 0.9834, "f1": 0.9653, "auc": 0.9423},
                {"acc": 0.9540, "prec": 0.9627, "rec": 0.9861, "f1": 0.9743, "auc": 0.9735},
            ],
            "avg": {"acc": 0.9203, "prec": 0.8258, "rec": 0.7528, "f1": 0.7817, "auc": 0.9204},
        },
    ]

    def fmt(x: float) -> str:
        return f"{x:.4f}"

    def build_row(m):
        params_html = "<br>".join(m["params"])

        test_cells = []
        for t in m["tests"]:
            test_cells.extend([
                f"<td class='metric'>{fmt(t['acc'])}</td>",
                f"<td class='metric'>{fmt(t['prec'])}</td>",
                f"<td class='metric'>{fmt(t['rec'])}</td>",
                f"<td class='metric'>{fmt(t['f1'])}</td>",
                f"<td class='metric'>{fmt(t['auc'])}</td>",
            ])

        avg = m["avg"]
        avg_cells = [
            f"<td class='metric avg'><b>{fmt(avg['acc'])}</b></td>",
            f"<td class='metric avg'><b>{fmt(avg['prec'])}</b></td>",
            f"<td class='metric avg'><b>{fmt(avg['rec'])}</b></td>",
            f"<td class='metric avg'><b>{fmt(avg['f1'])}</b></td>",
            f"<td class='metric avg'><b>{fmt(avg['auc'])}</b></td>",
        ]

        return f"""
        <tr>
            <td class="model">{m['model']}</td>
            <td class="params">{params_html}</td>
            {''.join(test_cells)}
            {''.join(avg_cells)}
        </tr>
        """

    rows_html = "\n".join(build_row(m) for m in models)

    # ✅ header dòng 1 có 7 nhóm: Test1..Test5 + Avg => 6 nhóm * 5 chỉ số
    html_table = textwrap.dedent(f"""
    <style>
        :root {{
            --head1: 50px; /* fallback */
        }}

        .table-wrap {{
            overflow: auto;
            /* max-height removed to show full table */
            width: 100%;
            padding: 12px;
            background: {wrap_bg};
            border-radius: 10px;
            border: 1px solid {td_border};
        }}

        table.result-table {{
            border-collapse: collapse;   /* ✅ không hở */
            border-spacing: 0;           /* ✅ không hở */
            min-width: 3400px;
            width: 100%;
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: {td_text};
        }}

        th, td {{
            border: 1px solid {td_border};
        }}

        th {{
            background: #0b5ed7;
            color: #fff;
            padding: 10px 12px;
            text-align: center;
            white-space: nowrap;
            line-height: 1.1;
            vertical-align: middle;
        }}

        td {{
            padding: 10px 12px;
            color: {td_text};
            text-align: center;
            white-space: nowrap;
            vertical-align: middle;
        }}

        /* ✅ Sticky header */
        thead th {{
            position: sticky;
        }}

        /* Dòng 1 sticky */
        thead tr:nth-child(1) th {{
            top: 0;
            z-index: 6;
        }}

        /* Dòng 2 sticky */
        thead tr:nth-child(2) th {{
            top: var(--head1);
            z-index: 7;
            background: #0a55c3;
            font-weight: 700;
        }}

        /* ✅ Quan trọng: 2 ô rowspan phải stick top=0 xuyên suốt, tránh bị “kéo xuống” gây lệch */
        th.rowspan2 {{
            top: 0 !important;
            z-index: 8 !important;
        }}

        .model {{
            font-weight: 800;
            background: rgba(11,94,215,0.18);
            min-width: 160px;
        }}

        .params {{
            font-family: Consolas, monospace;
            background: rgba(255,255,255,0.05);
            min-width: 260px;
            color: {td_muted};
            font-size: 13px;
            text-align: left;
            white-space: normal;
            line-height: 1.35;
        }}

        .avg-head {{
            background: #125bd6 !important;
        }}

        .metric {{
            min-width: 120px;
        }}

        td.avg {{
            background: rgba(18, 91, 214, 0.10);
        }}
    </style>

    <div class="table-wrap" id="wrap">
      <table class="result-table" id="rt">
        <thead>
          <tr>
            <th rowspan="2" class="rowspan2">Mô hình</th>
            <th rowspan="2" class="rowspan2">Tham số tốt nhất</th>

            <th colspan="5">Test 1</th>
            <th colspan="5">Test 2</th>
            <th colspan="5">Test 3</th>
            <th colspan="5">Test 4</th>
            <th colspan="5">Test 5</th>

            <th colspan="5" class="avg-head">Trung bình chỉ số</th>
          </tr>

          <tr>
            <!-- Test 1 -->
            <th class="metric">Accuracy</th><th class="metric">Precision</th><th class="metric">Recall</th><th class="metric">F1-Score</th><th class="metric">ROC-AUC</th>
            <!-- Test 2 -->
            <th class="metric">Accuracy</th><th class="metric">Precision</th><th class="metric">Recall</th><th class="metric">F1-Score</th><th class="metric">ROC-AUC</th>
            <!-- Test 3 -->
            <th class="metric">Accuracy</th><th class="metric">Precision</th><th class="metric">Recall</th><th class="metric">F1-Score</th><th class="metric">ROC-AUC</th>
            <!-- Test 4 -->
            <th class="metric">Accuracy</th><th class="metric">Precision</th><th class="metric">Recall</th><th class="metric">F1-Score</th><th class="metric">ROC-AUC</th>
            <!-- Test 5 -->
            <th class="metric">Accuracy</th><th class="metric">Precision</th><th class="metric">Recall</th><th class="metric">F1-Score</th><th class="metric">ROC-AUC</th>
            <!-- Avg -->
            <th class="metric avg-head">Accuracy</th><th class="metric avg-head">Precision</th><th class="metric avg-head">Recall</th><th class="metric avg-head">F1-Score</th><th class="metric avg-head">ROC-AUC</th>
          </tr>
        </thead>

        <tbody>
          {rows_html}
        </tbody>
      </table>
    </div>

    <script>
      // ✅ Tự đo đúng chiều cao header dòng 1 để top dòng 2 không lệch
      const rt = document.getElementById("rt");
      const firstRow = rt.querySelector("thead tr:nth-child(1)");
      const h = firstRow.getBoundingClientRect().height;
      rt.style.setProperty("--head1", h + "px");
    </script>
    """)

    components.html(html_table, height=800, scrolling=False)

    # phần dưới giữ nguyên
    st.markdown("### Model Categories")
    c1, c2, c3 = st.columns(3)
    c1.markdown("**Traditional ML**\n- CHƯA BỔ SUNG")
    c2.markdown("**Boosting**\n- CHƯA BỔ SUNG")
    c3.markdown("**Deep Learning**\n- CHƯA BỔ SUNG")
