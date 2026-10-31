# Run from the terminal with: streamlit run app.py

import math

import streamlit as st
from sectors import SectorsError, get_company_overview

st.set_page_config(page_title="Investment Goal Calculator", page_icon="📈")

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
        --page: #0b1020;
        --surface: #121a2b;
        --surface-raised: #182338;
        --text: #eef4ff;
        --muted: #a7b3c9;
        --accent: #55d6be;
    }
    html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
        background-color: var(--page);
        color: var(--text);
    }
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 92% 0%, rgba(32, 99, 112, 0.28) 0, transparent 34rem),
            radial-gradient(ellipse at 4% 28%, rgba(71, 58, 135, 0.16) 0, transparent 30rem),
            var(--page);
    }
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: transparent;
    }
    [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
        color: var(--text);
    }
    [data-testid="stMainBlockContainer"] p,
    [data-testid="stMainBlockContainer"] label,
    [data-testid="stMainBlockContainer"] h1,
    [data-testid="stMainBlockContainer"] h2,
    [data-testid="stMainBlockContainer"] h3 {
        color: var(--text);
    }
    [data-testid="stMainBlockContainer"] [data-testid="stCaptionContainer"],
    [data-testid="stMainBlockContainer"] [data-testid="stCaptionContainer"] p {
        color: var(--muted);
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(18, 26, 43, 0.82);
        border-color: #29364d;
        border-radius: 18px;
    }
    [data-testid="stMainBlockContainer"] {
        max-width: 760px;
        padding: 2rem 1.15rem 3rem;
    }
    h1, h2, h3 { letter-spacing: -0.035em; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #087e78, #16a995);
        border: 0;
        border-radius: 20px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 12px 30px rgba(8, 126, 120, 0.2);
    }
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        color: white;
    }
    [data-testid="stMetricLabel"] p {
        color: rgba(255, 255, 255, 0.84);
        font-size: 0.95rem;
    }
    [data-testid="stMetricValue"] {
        font-size: clamp(1.7rem, 7vw, 2.7rem);
        overflow-wrap: anywhere;
    }
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: rgba(255, 255, 255, 0.9);
    }
    [data-testid="stTabs"] button {
        min-height: 3rem;
        font-weight: 650;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--accent);
    }
    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background-color: var(--accent);
    }
    [data-testid="stNumberInput"] [data-baseweb="input"] > div,
    [data-testid="stTextInput"] [data-baseweb="input"] > div,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background-color: var(--surface-raised) !important;
        border-color: #35445e !important;
        border-radius: 12px;
    }
    [data-testid="stSelectbox"] [role="group"],
    [data-testid="stNumberInput"] [role="group"],
    [data-testid="stTextInput"] [role="group"] {
        background-color: var(--surface-raised) !important;
        border: 1px solid #35445e !important;
        border-radius: 12px;
    }
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input,
    [data-testid="stSelectbox"] [role="combobox"] {
        background-color: transparent !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text);
    }
    [data-testid="stSelectbox"] button {
        color: var(--muted) !important;
    }
    [data-testid="stSelectbox"] [data-baseweb="select"] svg {
        fill: var(--muted);
    }
    [data-baseweb="popover"] [role="listbox"] {
        background-color: var(--surface-raised);
    }
    [data-baseweb="popover"] [role="option"] {
        color: var(--text);
    }
    [data-baseweb="popover"] [role="option"]:hover {
        background-color: #25344d;
    }
    [data-testid="stNumberInput"] input {
        min-height: 2.9rem;
        border-radius: 12px;
    }
    [data-testid="stAlert"] {
        background: #152b32;
        border: 1px solid #28565a;
        border-radius: 14px;
        color: var(--text);
    }
    [data-testid="stAlert"] p {
        color: var(--text);
    }
    [data-testid="stExpander"] {
        background: rgba(18, 26, 43, 0.82);
        border-color: #29364d;
        border-radius: 14px;
    }
    @media (max-width: 480px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1.25rem 0.85rem 2rem;
        }
        [data-testid="stMetric"] {
            padding: 1.1rem;
            border-radius: 16px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div role="img" aria-label="Colorful illustration of savings growing over time"
         style="display:flex;align-items:center;justify-content:space-between;
         gap:1rem;padding:1.15rem 1.35rem;margin:0 0 1.1rem;
             border-radius:22px;background:linear-gradient(115deg,#18213a,#143536);
             border:1px solid #2a4054;">
          <div>
            <div style="font-size:.78rem;font-weight:750;letter-spacing:.08em;
                        text-transform:uppercase;color:#72e0ce;">YOUR MONEY, YOUR GOAL</div>
            <div style="font-size:clamp(1.15rem,4vw,1.55rem);font-weight:750;
                        color:#eef4ff;margin-top:.25rem;">Small steps add up.</div>
            <div style="font-size:.9rem;color:#b1bfd4;margin-top:.2rem;">
              Make a plan that feels right for you.
            </div>
          </div>
      <svg width="104" height="82" viewBox="0 0 104 82" fill="none"
           xmlns="http://www.w3.org/2000/svg" aria-hidden="true"
           style="flex:none;max-width:30%;">
        <rect x="4" y="6" width="96" height="70" rx="20" fill="#20324a"/>
        <path d="M19 58h66" stroke="#38516a" stroke-width="2" stroke-linecap="round"/>
        <path d="M22 51l17-14 13 8 23-22" stroke="#55d6be" stroke-width="4"
              stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M65 23h10v10" stroke="#55d6be" stroke-width="4"
              stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="23" cy="61" r="5" fill="#FFB648"/>
        <circle cx="37" cy="61" r="5" fill="#FFB648"/>
        <circle cx="51" cy="61" r="5" fill="#FFB648"/>
      </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("Investment Goal Calculator")
st.write("See how your savings could grow and what they could buy in an IDX stock.")


def format_rupiah(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")


@st.cache_data(ttl=300)
def get_cached_company_overview(ticker):
    return get_company_overview(ticker)


market_tickers = ["BBCA", "BBRI", "BMRI", "TLKM", "ASII"]
market_performance = []
market_errors = []

for market_ticker in market_tickers:
    try:
        market_company = get_cached_company_overview(market_ticker)
    except SectorsError as error:
        message = str(error)
        if message not in market_errors:
            market_errors.append(message)
        continue

    daily_change = market_company.get("daily_close_change")
    if isinstance(daily_change, (int, float)) and math.isfinite(daily_change):
        industry = market_company.get("sub_sector") or market_company.get("sector") or "Other"
        market_performance.append((market_ticker, industry, daily_change * 100))

with st.container(border=True):
    st.subheader("🌈  Stock performance by industry")
    st.caption(
        "Average daily change for the available stocks in each industry among five "
        "selected IDX companies. This small snapshot is not the complete market or a recommendation."
    )
    for message in market_errors:
        st.warning(message)

    if market_performance:
        industry_returns = {}
        industry_tickers = {}
        for market_ticker, industry, daily_change in market_performance:
            industry_returns.setdefault(industry, []).append(daily_change)
            industry_tickers.setdefault(industry, []).append(market_ticker)

        industries = sorted(industry_returns)
        averages = {
            industry: sum(industry_returns[industry]) / len(industry_returns[industry])
            for industry in industries
        }
        industry_columns = [f"{industry} average" for industry in industries]
        chart_data = {
            "Industry": industries,
            **{
                column: [
                    averages[industry] if industry == industries[index] else None
                    for index, industry in enumerate(industries)
                ]
                for industry, column in zip(industries, industry_columns)
            },
        }
        palette = ["#55D6BE", "#F6BD60", "#8B9CF6", "#F28482", "#A9DEF9", "#CDB4DB"]
        st.bar_chart(
            chart_data,
            x="Industry",
            y=industry_columns,
            color=palette[: len(industries)],
            x_label="Industry",
            y_label="Average daily change (%)",
            sort=False,
        )
        for industry in industries:
            stocks = ", ".join(industry_tickers[industry])
            st.caption(f"**{industry}** · {stocks} · {averages[industry]:+.2f}%")
    elif not market_errors:
        st.info("Industry performance data is not available for these tickers right now.")


ticker = st.selectbox(
    "🔎  Choose an IDX ticker",
    options=[
        "ADRO",
        "AMMN",
        "ANTM",
        "ASII",
        "BBCA",
        "BBNI",
        "BBRI",
        "BMRI",
        "BRPT",
        "CPIN",
        "GOTO",
        "ICBP",
        "INDF",
        "ISAT",
        "KLBF",
        "MDKA",
        "MEDC",
        "PGAS",
        "PTBA",
        "SMGR",
        "TINS",
        "TLKM",
        "TPIA",
        "UNTR",
        "UNVR",
    ],
    index=4,
)
st.caption("This is a curated selection, not the complete list of IDX stocks.")
company = None
try:
    company = get_cached_company_overview(ticker)
except SectorsError as error:
    st.warning(str(error))

if company:
    st.subheader(company.get("company_name") or ticker)
    sector = company.get("sector") or "Not available"
    sub_sector = company.get("sub_sector") or "Not available"
    last_close_price = company.get("last_close_price")
    if isinstance(last_close_price, (int, float)) and math.isfinite(last_close_price):
        st.caption(
            f"Sector: {sector} · Sub-sector: {sub_sector} · "
            f"Last close: {format_rupiah(last_close_price)}"
        )
    else:
        st.caption(f"Sector: {sector} · Sub-sector: {sub_sector} · Last close: Not available")

calculator_tab, guide_tab = st.tabs(["🧮  Calculator", "💡  How it works"])

with calculator_tab:
    with st.container(border=True):
        st.subheader("Set your plan")
        monthly_saving = st.number_input(
            "💸  Monthly saving (Rp)",
            min_value=0,
            value=1_000_000,
            step=100_000,
            help="How much you plan to save at the end of each month.",
        )
        years = st.number_input(
            "🗓️  Number of years",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
        )
        annual_return_percent = st.number_input(
            "📈  Expected yearly return (%)",
            min_value=-100.0,
            max_value=100.0,
            value=8.0,
            step=0.5,
            help="An estimate for this example, not a promise of future returns.",
        )

    monthly_return = (1 + annual_return_percent / 100) ** (1 / 12) - 1
    balance = 0.0
    yearly_totals = [balance]

    for month in range(1, int(years) * 12 + 1):
        balance *= 1 + monthly_return
        balance += monthly_saving
        if month % 12 == 0:
            yearly_totals.append(balance)

    st.subheader("Your estimated result")
    st.metric("✨  Estimated final amount", format_rupiah(balance))

    if company:
        last_close_price = company.get("last_close_price")
        if (
            isinstance(last_close_price, (int, float))
            and math.isfinite(last_close_price)
            and last_close_price > 0
        ):
            lot_price = last_close_price * 100
            lots = math.floor(monthly_saving / lot_price)
            leftover = monthly_saving - lots * lot_price
            st.info(
                f"Your monthly saving buys **{lots:,} lots** of this stock, "
                f"with **{format_rupiah(leftover)}** left over."
            )
        else:
            st.warning("The stock's last close price is unavailable, so the lot estimate cannot be calculated.")

    with st.container(border=True):
        st.subheader("📈  Your savings growth projection")
        st.line_chart(
            {
                "Year": list(range(int(years) + 1)),
                "Estimated total (Rp)": yearly_totals,
            },
            x="Year",
            y="Estimated total (Rp)",
            x_label="Years",
            y_label="Estimated total (Rp)",
        )

    st.caption("For learning only. Actual results vary; this is not investment advice.")

with guide_tab:
    with st.container(border=True):
        st.subheader("A simple estimate")
        st.write(
            "Your saving is added at the end of every month. The existing balance "
            "grows a little each month using the yearly return you entered."
        )
        st.write(
            "The chart shows the estimated balance at the end of each year. "
            "Changing any number updates the estimate."
        )
        st.info(
            "Returns are uncertain. This calculator is for learning and is not "
            "investment advice."
        )

if company:
    with st.expander("🔎 Raw company data"):
        st.json(company)
