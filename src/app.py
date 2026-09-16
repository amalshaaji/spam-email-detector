import sys
from pathlib import Path
import re

import pandas as pd
import streamlit as st

# Ensure modular imports work
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from email_classifier.inferance import (
    get_top_spam_words,
    load_model,
    predict_email_details,
)

# Page configuration
st.set_page_config(
    page_title="CertiMail AI™ Enterprise | Email Spam & Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject High-Aesthetic & Highlighted Input Styling
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0f172a;
    }

    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #eef4ff 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
        border-right: 1px solid #dfe7f5;
    }

    div[data-testid="stSidebarNavLink"] {
        border-radius: 10px;
        margin: 4px 8px;
    }

    /* Premium top navigation */
    .top-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.96), rgba(241,245,249,0.94));
        border: 1px solid rgba(148, 163, 184, 0.28);
        border-radius: 20px;
        padding: 30px 38px;
        margin-bottom: 28px;
        box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .brand-title {
        font-size: 34px;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        letter-spacing: -0.8px;
        line-height: 1.2;
    }

    .brand-subtitle {
        color: #475569;
        font-size: 17px;
        font-weight: 500;
        margin-top: 8px;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: #f0fdf4;
        border: 1.5px solid #bbf7d0;
        color: #15803d;
        padding: 10px 20px;
        border-radius: 24px;
        font-size: 16px;
        font-weight: 700;
    }

    .status-dot {
        width: 11px;
        height: 11px;
        background-color: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 10px #22c55e;
    }

    /* =========================================================
       ✨ ULTRA-AESTHETIC HIGHLIGHTED INPUT BOX STYLING 
       ========================================================= */
    .input-wrapper-card {
        background: linear-gradient(180deg, #ffffff 0%, #f8faff 100%);
        border: 2px solid #4f46e5;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 16px 36px rgba(79, 70, 229, 0.18), 0 4px 10px rgba(15, 23, 42, 0.06);
        position: relative;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }

    .input-wrapper-card:hover {
        box-shadow: 0 18px 42px rgba(79, 70, 229, 0.22), 0 6px 14px rgba(15, 23, 42, 0.08);
    }

    .input-header-label {
        font-size: 16px;
        font-weight: 700;
        color: #1e1b4b;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
    }

    .input-badge {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: #ffffff;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Highlighted Textarea Element Overrides */
    div[data-baseweb="textarea"] {
        border: 2px solid #a5b4fc !important;
        border-radius: 16px !important;
        background: linear-gradient(180deg, #ffffff 0%, #f8faff 100%) !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.08), inset 0 2px 8px rgba(15, 23, 42, 0.03) !important;
        transition: all 0.25s ease-in-out !important;
    }

    div[data-baseweb="textarea"]:focus-within {
        border-color: #4f46e5 !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 5px rgba(79, 70, 229, 0.14), inset 0 2px 8px rgba(15, 23, 42, 0.02) !important;
    }

    textarea {
        color: #0f172a !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
    }

    /* KPI Cards */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 4px;
    }

    /* Threat Status Banners */
    .banner-spam {
        background: #fef2f2;
        border-left: 5px solid #ef4444;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.08);
    }

    .banner-ham {
        background: #f0fdf4;
        border-left: 5px solid #10b981;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.08);
    }

    .banner-suspicious {
        background: #fffbeb;
        border-left: 5px solid #f59e0b;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.08);
    }

    .banner-title {
        font-size: 20px;
        font-weight: 800;
        margin: 0;
    }

    .banner-desc {
        font-size: 14px;
        margin-top: 6px;
        color: #475569;
    }

    /* Feature Chips */
    .chip-danger {
        display: inline-flex;
        align-items: center;
        background: #fee2e2;
        border: 1px solid #fca5a5;
        color: #991b1b;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        margin: 4px;
    }

    .chip-success {
        display: inline-flex;
        align-items: center;
        background: #dcfce7;
        border: 1px solid #86efac;
        color: #166534;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        margin: 4px;
    }

    .doc-inspector {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 18px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        line-height: 1.8;
        color: #1e293b;
        max-height: 320px;
        overflow-y: auto;
    }

    .hl-spam-word {
        background: #fca5a5;
        color: #7f1d1d;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
    }

    .hl-ham-word {
        background: #86efac;
        color: #14532d;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
    }

    div.stButton > button {
        border-radius: 12px !important;
        border: 1.5px solid rgba(99, 102, 241, 0.3) !important;
        background: linear-gradient(180deg, #ffffff 0%, #eef2ff 100%) !important;
        color: #1e293b !important;
        font-weight: 700 !important;
        letter-spacing: 0.1px !important;
        padding: 0.7rem 1.2rem !important;
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.10) !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover {
        border-color: rgba(79, 70, 229, 0.7) !important;
        box-shadow: 0 12px 24px rgba(79, 70, 229, 0.16) !important;
        transform: translateY(-1px);
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        border: none !important;
        color: #ffffff !important;
        box-shadow: 0 12px 28px rgba(79, 70, 229, 0.28) !important;
    }

    .stTabs [role="tablist"] {
        background: rgba(255,255,255,0.64);
        border: 1px solid rgba(148,163,184,0.22);
        border-radius: 12px;
        padding: 6px;
        gap: 8px;
    }

    .stTabs [role="tab"] {
        border-radius: 10px;
        padding: 0.55rem 0.9rem;
        font-weight: 600;
        color: #475569;
    }

    .stTabs [role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
        color: #312e81;
        box-shadow: inset 0 0 0 1px rgba(99,102,241,0.18);
    }
</style>
""",
    unsafe_allow_html=True,
)

# Preset Email Repositories (Safe & Suspicious Email Examples)
DEFAULT_SAFE_SAMPLE = """Subject: Q4 Security Audit & System Architecture Review

Hi Team,

Hope everyone is having a productive week.

Please find attached the final draft for our Q4 Security Audit report and infrastructure updates. We have successfully completed the routine penetration testing and verified all firewall rules.

Key highlights:
1. Zero critical vulnerabilities detected in production clusters.
2. Routine SSL certificate renewals scheduled for next Tuesday at 02:00 UTC.
3. Updated API rate-limiting rules are now active across all edge proxies.

Let's schedule a brief 20-minute sync on Thursday at 2:00 PM EST to review the deployment roadmap.

Best regards,
Security Engineering Team
CertiMail AI™ Security Studio"""

SCENARIOS = {
    "✨ Security Audit & System Update (Safe)": DEFAULT_SAFE_SAMPLE,
    "🚨 Phishing Alert (Bank Suspensions)": (
        "URGENT ACCOUNT NOTICE: Your online banking access has been temporarily locked due to suspicious login attempts. "
        "Please visit http://secure-bank-login-verify.com immediately to update your password and security questions. "
        "Failure to verify within 24 hours will result in permanent account closure."
    ),
    "🎁 Lottery & Prize Claim Scam": (
        "CONGRATULATIONS! You have been randomly chosen as the grand prize winner of $100,000 cash and a brand new Tesla! "
        "Click here now to claim your cash payout. No deposit required. Instant transfer guaranteed!"
    ),
    "💰 Crypto Investment Fraud": (
        "Special opportunity! Automated crypto trading bot generates $1,500 daily profits with zero risk! "
        "Click the link below to start your free trial and receive $250 bonus trading capital today."
    ),
    "💼 Corporate Meeting Sync (Safe)": (
        "Hi Alex,\n\nHope you're having a good week. Could you please review the attached PDF draft for the Q4 product launch? "
        "Let's schedule a brief 20-minute call on Thursday at 2:00 PM EST to align on key milestones.\n\nBest regards,\nDavid"
    ),
}

# Sidebar Navigation & Settings
with st.sidebar:
    st.markdown("### 🛡️ **CertiMail AI™**")
    st.caption("Enterprise Email Security Platform v1.0")
    st.markdown("---")

    st.markdown("##### 📌 Test Scenarios")
    selected_scenario = st.selectbox(
        "Load Pre-configured Scenario:",
        ["-- Select Scenario --"] + list(SCENARIOS.keys()),
    )

    st.markdown("---")
    st.markdown("##### ⚙️ Model Parameters")
    threshold_slider = st.slider(
        "Spam Cutoff Threshold (%)",
        min_value=10,
        max_value=90,
        value=50,
        step=5,
        help="Probability threshold above which an email is flagged as Spam.",
    )
    threshold = threshold_slider / 100.0

    st.markdown("---")
    st.markdown("##### 🔍 System Metadata")
    st.caption(
        "• Model: Logistic Regression\n• Vocabulary: 3,000 Tokens\n• Environment: Production"
    )

# Top Header Bar
st.markdown(
    """
<div class="top-header">
    <div>
        <div class="brand-title">🛡️ CertiMail AI™ Enterprise Security Studio</div>
        <div class="brand-subtitle">Automated NLP Email Spam Classification, Phishing Detection & Threat Analytics</div>
    </div>
    <div class="status-badge">
        <div class="status-dot"></div> System Operational
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# System Executive Metrics Row
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-label">Dataset Sample Size</div>
            <div class="kpi-value">5,172</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_m2:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-label">Vocabulary Features</div>
            <div class="kpi-value">3,000</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_m3:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-label">Model Architecture</div>
            <div class="kpi-value" style="font-size: 18px; margin-top: 8px;">Logistic Regression</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_m4:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-label">Avg Inference Time</div>
            <div class="kpi-value">&lt; 5 ms</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Dashboard Tabs
tab_eval, tab_compare, tab_batch, tab_analytics = st.tabs(
    [
        "📊 Threat Analyzer",
        "⚖️ Comparative Diff Analysis",
        "📂 Batch Processing",
        "📈 Model Feature Intelligence",
    ]
)

# TAB 1: Threat Analyzer
with tab_eval:
    c_left, c_right = st.columns([1.15, 0.85])

    with c_left:
        st.markdown(
            """
            <div class="input-header-label">
                <span>📝 Email Content Analysis</span>
                <span class="input-badge">Active Engine</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        default_val = ""
        if selected_scenario != "-- Select Scenario --" and selected_scenario in SCENARIOS:
            default_val = SCENARIOS[selected_scenario]

        if "email_text" not in st.session_state:
            st.session_state.email_text = default_val
        if "run_analysis" not in st.session_state:
            st.session_state.run_analysis = False

        if (
            selected_scenario != "-- Select Scenario --"
            and selected_scenario in SCENARIOS
            and st.session_state.get("last_selected_scenario") != selected_scenario
        ):
            st.session_state.email_text = SCENARIOS[selected_scenario]
            st.session_state.last_selected_scenario = selected_scenario
            st.session_state.run_analysis = True

        email_text_input = st.text_area(
            "Raw Email Text (Subject & Body):",
            key="email_text",
            height=300,
            placeholder="Paste raw email text here to run instant classification...",
        )

        def _clear_email_input():
            st.session_state.email_text = ""
            st.session_state.last_selected_scenario = "-- Select Scenario --"
            st.session_state.run_analysis = False

        def _trigger_analysis():
            st.session_state.run_analysis = True

        b1, b2 = st.columns([1.5, 1])
        with b1:
            st.button(
                "⚡ Analyze Threat Level",
                type="primary",
                width="stretch",
                on_click=_trigger_analysis,
            )
        with b2:
            st.button(
                "🗑️ Clear",
                width="stretch",
                on_click=_clear_email_input,
            )


    with c_right:
        st.markdown("#### 🎯 Classification Verdict")

        if email_text_input.strip():
            details = predict_email_details(email_text_input)
            prob_spam = details["prob_spam"]
            prob_ham = details["prob_ham"]
            is_spam = prob_spam >= threshold

            # Executive Banner Display
            if prob_spam >= 0.70:
                st.markdown(
                    f"""
                    <div class="banner-spam">
                        <div class="banner-title" style="color: #991b1b;">🚨 HIGH RISK SPAM / PHISHING DETECTED</div>
                        <div class="banner-desc">Spam Probability: <strong>{prob_spam * 100:.1f}%</strong> — High probability of malicious intent or promo spam.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif prob_spam >= 0.40:
                st.markdown(
                    f"""
                    <div class="banner-suspicious">
                        <div class="banner-title" style="color: #92400e;">⚠️ SUSPICIOUS EMAIL SIGNALS</div>
                        <div class="banner-desc">Spam Risk Score: <strong>{prob_spam * 100:.1f}%</strong> — Contains potential threat indicators requiring review.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="banner-ham">
                        <div class="banner-title" style="color: #166534;">✅ SAFE / LEGITIMATE EMAIL (HAM)</div>
                        <div class="banner-desc">Safety Confidence: <strong>{prob_ham * 100:.1f}%</strong> — No major spam or phishing signatures identified.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Metric Progress Bars
            st.markdown("##### 📈 Risk Probability Distribution")
            st.write(
                f"**Spam Probability:** `{prob_spam * 100:.1f}%` &nbsp;|&nbsp; **Safe Probability:** `{prob_ham * 100:.1f}%`"
            )
            st.progress(min(prob_spam, 1.0))

            v1, v2 = st.columns(2)
            v1.metric("Words Scanned", details["total_words"])
            v2.metric("Vocabulary Matches", len(details["word_contributions"]))

        else:
            st.info(
                "👈 Enter email text on the left panel or select a pre-configured scenario from the sidebar to view evaluation metrics."
            )

    # Lower Breakdown Section
    if email_text_input.strip():
        st.markdown("---")
        col_kw, col_doc = st.columns([1, 1])

        with col_kw:
            st.markdown("#### 🔍 Extracted Feature Influences")
            contributions = details["word_contributions"]

            if contributions:
                spam_words = [c for c in contributions if c["impact"] > 0.02]
                ham_words = [c for c in contributions if c["impact"] < -0.02]

                if spam_words:
                    st.markdown("**🚨 Spam Indicators:**")
                    chips_html = "".join(
                        [
                            f'<span class="chip-danger">⚠️ {c["word"]} (+{c["impact"]:.2f})</span>'
                            for c in spam_words[:8]
                        ]
                    )
                    st.markdown(chips_html, unsafe_allow_html=True)

                if ham_words:
                    st.markdown("**✅ Safe Indicators:**")
                    chips_html = "".join(
                        [
                            f'<span class="chip-success">✔️ {c["word"]} ({c["impact"]:.2f})</span>'
                            for c in ham_words[:8]
                        ]
                    )
                    st.markdown(chips_html, unsafe_allow_html=True)

                st.markdown("##### Feature Impact Breakdown")
                df_c = pd.DataFrame(contributions)
                df_c["Category"] = df_c["impact"].apply(
                    lambda x: "Spam Signal" if x > 0 else "Safe Signal"
                )
                st.dataframe(
                    df_c[["word", "count", "impact", "Category"]],
                    width="stretch",
                    height=210,
                )
            else:
                st.write("No vocabulary features matched in this input.")

        with col_doc:
            st.markdown("#### 🖍️ Text Token Highlighter")
            st.caption(
                "Highlighted terms indicate model feature coefficients (Red = Spam bias, Green = Safe bias)."
            )

            words_in_text = re.findall(
                r"\b\w+\b|\s+|[^\w\s]", email_text_input
            )
            contrib_map = {
                c["word"].lower(): c["impact"]
                for c in details["word_contributions"]
            }

            tokens_rendered = []
            for token in words_in_text:
                lower_t = token.lower()
                if lower_t in contrib_map:
                    impact = contrib_map[lower_t]
                    if impact > 0.05:
                        tokens_rendered.append(
                            f'<span class="hl-spam-word">{token}</span>'
                        )
                    elif impact < -0.05:
                        tokens_rendered.append(
                            f'<span class="hl-ham-word">{token}</span>'
                        )
                    else:
                        tokens_rendered.append(token)
                else:
                    tokens_rendered.append(token)

            st.markdown(
                f'<div class="doc-inspector">{"".join(tokens_rendered)}</div>',
                unsafe_allow_html=True,
            )

# TAB 2: Comparative Diff Analysis
with tab_compare:
    st.markdown("#### ⚖️ Comparative Text Analysis (A/B Testing)")
    st.caption(
        "Evaluate two email text variations side-by-side to understand how word changes affect classification scores."
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("##### Variation A")
        val_a = st.text_area(
            "Variation A Text:",
            value=SCENARIOS["🚨 Phishing Alert (Bank Suspensions)"],
            height=200,
            key="var_a_input",
        )
        if val_a.strip():
            res_a = predict_email_details(val_a)
            st.metric(
                "Spam Probability Score",
                f"{res_a['prob_spam'] * 100:.1f}%",
                delta="SPAM" if res_a["prob_spam"] >= threshold else "HAM",
                delta_color="inverse",
            )
            st.progress(min(res_a["prob_spam"], 1.0))

    with col_b:
        st.markdown("##### Variation B")
        val_b = st.text_area(
            "Variation B Text:",
            value=DEFAULT_SAFE_SAMPLE,
            height=200,
            key="var_b_input",
        )
        if val_b.strip():
            res_b = predict_email_details(val_b)
            st.metric(
                "Spam Probability Score",
                f"{res_b['prob_spam'] * 100:.1f}%",
                delta="SPAM" if res_b["prob_spam"] >= threshold else "HAM",
                delta_color="inverse",
            )
            st.progress(min(res_b["prob_spam"], 1.0))

# TAB 3: Batch Processing
with tab_batch:
    st.markdown("#### 📂 Enterprise Batch CSV Processing")
    st.caption(
        "Upload a dataset containing email contents to execute bulk predictions and export structured CSV reports."
    )

    uploaded_file = st.file_uploader(
        "Select CSV File:", type=["csv"], help="CSV must contain email content text column."
    )

    if uploaded_file is not None:
        try:
            df_file = pd.read_csv(uploaded_file)
            target_col = df_file.columns[0]
            for c in df_file.columns:
                if c.lower() in ["text", "email", "body", "content", "message"]:
                    target_col = c
                    break

            st.success(
                f"Loaded dataset containing **{len(df_file)}** records. Using target column `{target_col}`"
            )

            if st.button("🚀 Process Batch Predictions", type="primary"):
                results = []
                for val in df_file[target_col].astype(str):
                    pred = predict_email_details(val)
                    results.append(
                        {
                            "Text Snippet": val[:90] + "..."
                            if len(val) > 90
                            else val,
                            "Classification": "SPAM"
                            if pred["prob_spam"] >= threshold
                            else "HAM",
                            "Spam Probability (%)": round(
                                pred["prob_spam"] * 100, 2
                            ),
                            "Safe Probability (%)": round(
                                pred["prob_ham"] * 100, 2
                            ),
                        }
                    )

                df_results = pd.DataFrame(results)
                st.dataframe(df_results, width="stretch")

                csv_bytes = df_results.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Export Batch Results CSV",
                    data=csv_bytes,
                    file_name="email_predictions_export.csv",
                    mime="text/csv",
                )
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")

# TAB 4: Model Intelligence
with tab_analytics:
    st.markdown("#### 📈 Model Vocabulary Intelligence & Feature Coefficients")
    st.caption(
        "Statistical feature weights derived from Logistic Regression training on 5,172 email samples."
    )

    top_spam, top_ham = get_top_spam_words(25)

    if top_spam is not None:
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("##### 🚨 Top 25 Spam Indicators")
            st.bar_chart(
                data=top_spam.set_index("word")["coefficient"], color="#ef4444"
            )
            st.dataframe(top_spam, width="stretch")

        with c2:
            st.markdown("##### ✅ Top 25 Safe Indicators")
            top_ham["abs_weight"] = top_ham["coefficient"].abs()
            st.bar_chart(
                data=top_ham.set_index("word")["abs_weight"], color="#10b981"
            )
            st.dataframe(top_ham, width="stretch")

# Footer
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #94a3b8; font-size: 13px; padding-bottom: 20px;">
    CertiMail AI™ Enterprise Security Platform • Scikit-Learn NLP Machine Learning Engine
</div>
""",
    unsafe_allow_html=True,
)
