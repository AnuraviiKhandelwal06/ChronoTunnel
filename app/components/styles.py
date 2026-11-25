from components.render import show_html


def inject_landing_styles() -> None:
    show_html(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        :root {
            --mp-black: #050608;
            --mp-surface: #0D0E12;
            --mp-surface-2: #15171D;
            --mp-white: #F8FAFF;
            --mp-muted: #9297A2;
            --mp-border: rgba(255,255,255,0.10);
            --mp-headlight: #FFFFFF;
            --mp-yellow: #FF354D;
            --mp-amber: #FF9B45;
            --mp-red: #FF354D;
            --mp-pink: #FF6B9A;
            --mp-cyan: #00D9FF;
        }

        .stApp {
            background:
                radial-gradient(ellipse at 78% 18%, rgba(255,53,77,0.065), transparent 35%),
                radial-gradient(ellipse at 15% 45%, rgba(255,53,77,0.075), transparent 32%),
                radial-gradient(ellipse at 50% 100%, rgba(255,107,154,0.025), transparent 45%),
                var(--mp-black) !important;
            color: var(--mp-white);
            font-family: Outfit, sans-serif;
        }

        header[data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        #MainMenu,
        footer,
        [data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        .block-container {
            max-width: 1280px;
            padding: 0.4rem 1.5rem 3rem;
        }

        .stApp,
        .stApp p,
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp a,
        .stApp span,
        .stApp li {
            font-family: Outfit, sans-serif;
        }

        .mp {
            position: relative;
            color: var(--mp-white);
        }

        .mp-bg {
            position: absolute;
            inset: -40px -8vw auto -8vw;
            height: 850px;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
            opacity: 0.8;
        }

        .mp-bg::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, transparent 45%, var(--mp-black) 100%);
        }

        .mp > *:not(.mp-bg) {
            position: relative;
            z-index: 1;
        }

        .mp-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            padding: 23px 0 18px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }

        .mp-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            color: inherit !important;
            text-decoration: none !important;
        }

        .mp-brand svg {
            filter: drop-shadow(0 0 5px rgba(255,53,77,0.40))
                    drop-shadow(0 0 12px rgba(255,107,154,0.12));
        }

        .mp-brand-name {
            font-family: "Space Grotesk", sans-serif;
            font-size: 23px;
            font-weight: 700;
            letter-spacing: -0.06em;
            color: var(--mp-white);
            line-height: 1;
        }

        .mp-brand-sub {
            display: block;
            margin-top: 5px;
            color: var(--mp-muted);
            font-size: 9px;
            letter-spacing: 0.17em;
            font-weight: 600;
        }

        .mp-nav-right {
            display: flex;
            align-items: center;
            gap: 29px;
        }

        a.mp-textlink {
            color: #AEB8C3 !important;
            text-decoration: none !important;
            font-size: 13.5px;
            font-weight: 500;
            transition: color 160ms ease;
        }

        a.mp-textlink:hover {
            color: var(--mp-red) !important;
        }

        a.mp-cta,
        a.btn-primary {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(110deg, #FF354D 0%, #FF354D 80%, #FF6B9A 100%) !important;
            color: #FFFFFF !important;
            text-decoration: none !important;
            border: 1px solid #FF354D;
            border-radius: 7px;
            padding: 11px 19px;
            font-size: 13.5px;
            font-weight: 700;
            letter-spacing: 0.01em;
            transition: all 180ms ease;
            box-shadow: 0 0 20px rgba(255,53,77,0.20);
        }

        a.btn-primary {
            padding: 14px 23px;
        }

        a.mp-cta:hover,
        a.btn-primary:hover {
            background: linear-gradient(110deg, #FF5265 0%, #FF5265 80%, #FF8FB2 100%) !important;
            border-color: #FF5265;
            transform: translateY(-2px);
            box-shadow: 0 0 28px rgba(255,53,77,0.30);
        }

        a.btn-ghost {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: var(--mp-white) !important;
            text-decoration: none !important;
            border: 1px solid rgba(255,255,255,0.22);
            background: rgba(255,255,255,0.025) !important;
            border-radius: 7px;
            padding: 13px 21px;
            font-size: 13.5px;
            font-weight: 500;
            transition: all 180ms ease;
        }

        a.btn-ghost:hover {
            border-color: var(--mp-red);
            background: rgba(255,53,77,0.07) !important;
        }

        .hero-title-red {
            color: #FF354D;
            display: block;
        }

        .hero-title-blue {
            color: #7BA7FF;
            display: block;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.02fr) minmax(300px, 0.98fr);
            gap: 28px;
            align-items: center;
            padding: 76px 0 40px;
            min-height: 560px;
        }

        .kicker {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            color: var(--mp-red);
            font-family: "Space Grotesk", sans-serif;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.16em;
            margin-bottom: 23px;
        }

        .kicker::before {
            content: "";
            width: 23px;
            height: 2px;
            background: linear-gradient(90deg, #FF354D 0%, #FF354D 80%, #FF6B9A 100%);
            box-shadow: 0 0 10px rgba(255,53,77,0.55);
        }

        .hero-title {
            font-family: "Space Grotesk", sans-serif;
            font-weight: 700;
            font-size: clamp(46px, 5.4vw, 76px);
            line-height: 1.02;
            letter-spacing: -0.065em;
            color: var(--mp-white);
            margin: 0;
            text-wrap: balance;
        }

        .hero-title span {
            background: linear-gradient(100deg, #FF354D 0%, #FF354D 80%, #FF6B9A 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            -webkit-text-fill-color: transparent;
            text-shadow: none;
        }

        .hero-copy p.lede {
            max-width: 520px;
            margin: 23px 0 0;
            color: #AAB5C1;
            font-size: 16px;
            line-height: 1.8;
            font-weight: 300;
        }

        .hero-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 13px;
            margin-top: 32px;
        }

        .hero-art {
            position: relative;
            min-height: 510px;
        }

        .hero-art svg {
            width: 100%;
            height: auto;
            display: block;
            overflow: visible;
        }

        .hero-art svg .traffic-road {
            fill: none;
            stroke: rgba(255,255,255,0.10);
            stroke-width: 1.5;
        }

        .hero-art svg .traffic-headlights {
            fill: none;
            stroke: #FFFFFF;
            stroke-width: 2.2;
            stroke-linecap: round;
            stroke-dasharray: 2 22;
            filter: drop-shadow(0 0 3px #FFFFFF) drop-shadow(0 0 8px #FFD76A);
            animation: headlights-flow 2.2s linear infinite;
        }

        .hero-art svg .traffic-amber {
            fill: none;
            stroke: #FFD76A;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-dasharray: 2 28;
            filter: drop-shadow(0 0 7px #FF9B45);
            animation: headlights-flow 3s linear infinite;
        }

        .hero-art svg .traffic-taillights {
            fill: none;
            stroke: #FF354D;
            stroke-width: 2.5;
            stroke-linecap: round;
            stroke-dasharray: 3 19;
            filter: drop-shadow(0 0 4px #FF354D) drop-shadow(0 0 9px #FF6B9A);
            animation: taillights-flow 2.6s linear infinite;
        }

        .hero-art svg .traffic-pink {
            fill: none;
            stroke: #FF6B9A;
            stroke-width: 1.8;
            stroke-linecap: round;
            stroke-dasharray: 2 25;
            filter: drop-shadow(0 0 8px #FF6B9A);
            animation: taillights-flow 3.5s linear infinite;
        }

        @keyframes headlights-flow {
            from { stroke-dashoffset: 0; }
            to { stroke-dashoffset: -96; }
        }

        @keyframes taillights-flow {
            from { stroke-dashoffset: 0; }
            to { stroke-dashoffset: 96; }
        }

        .hero-art svg .traffic-node {
            filter: drop-shadow(0 0 4px #FFFFFF) drop-shadow(0 0 10px #FF9B45);
        }

        @media (prefers-reduced-motion: reduce) {
            .hero-art svg .traffic-headlights,
            .hero-art svg .traffic-amber,
            .hero-art svg .traffic-taillights,
            .hero-art svg .traffic-pink {
                animation: none !important;
            }
        }

        .glass {
            position: absolute;
            min-width: 150px;
            padding: 13px 15px 12px;
            border-radius: 9px;
            background: rgba(11,12,16,0.86);
            border: 1px solid rgba(255,53,77,0.20);
            backdrop-filter: blur(16px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.35);
        }

        .glass span {
            display: block;
            color: var(--mp-red);
            font-size: 9px;
            letter-spacing: 0.15em;
            font-weight: 700;
        }

        .glass strong {
            display: block;
            margin-top: 6px;
            font-family: "Space Grotesk", sans-serif;
            font-size: 27px;
            font-weight: 700;
            letter-spacing: -0.05em;
            color: var(--mp-white);
        }

        .g-ridership { top: 7%; left: 0; }
        .g-stations { top: 24%; right: 0; }
        .g-boroughs { bottom: 25%; left: 4%; }
        .g-years { bottom: 6%; right: 8%; }

        .feature-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 18px;
            margin-top: 18px;
            padding: 28px 0 12px;
            border-top: 1px solid var(--mp-border);
            border-bottom: 1px solid var(--mp-border);
        }

        .feature {
            padding: 12px 16px 20px;
            border-right: 1px solid rgba(255,255,255,0.07);
        }

        .feature:last-child { border-right: none; }

        .feature svg {
            display: block;
            filter: drop-shadow(0 0 5px rgba(255,53,77,0.30))
                    drop-shadow(0 0 8px rgba(255,107,154,0.12));
        }

        .feature h3 {
            margin: 14px 0 7px;
            font-family: "Space Grotesk", sans-serif;
            font-size: 15px;
            font-weight: 600;
            letter-spacing: -0.025em;
            color: var(--mp-white);
        }

        .feature p {
            margin: 0;
            color: var(--mp-muted);
            font-size: 13px;
            line-height: 1.65;
        }

        .section { padding: 88px 0 0; }

        .section .eyebrow {
            color: var(--mp-red);
            letter-spacing: 0.17em;
            font-size: 10px;
            font-weight: 700;
            margin-bottom: 14px;
        }

        .section h2 {
            font-family: "Space Grotesk", sans-serif;
            font-weight: 600;
            font-size: clamp(32px, 3.8vw, 49px);
            letter-spacing: -0.055em;
            line-height: 1.1;
            margin: 0 0 17px;
            color: var(--mp-white);
            max-width: 760px;
        }

        .section .intro {
            max-width: 690px;
            color: #AAB5C1;
            font-size: 15px;
            line-height: 1.8;
            margin: 0;
        }

        .split {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 50px;
            align-items: end;
        }

        .quiet-stats { display: grid; gap: 17px; }

        .quiet-stats div {
            border-top: 1px solid var(--mp-border);
            padding-top: 13px;
        }

        .quiet-stats strong {
            display: block;
            font-family: "Space Grotesk", sans-serif;
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.045em;
            color: var(--mp-white);
        }

        .quiet-stats span {
            color: var(--mp-muted);
            font-size: 12px;
            line-height: 1.5;
        }

        .cap-grid,
        .cover-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin-top: 34px;
        }

        .cap,
        .cover {
            height: 100%;
            box-sizing: border-box;
            border: 1px solid var(--mp-border);
            border-radius: 10px;
            padding: 23px 21px;
            background: linear-gradient(145deg, rgba(25,24,26,0.88), rgba(9,10,13,0.94));
            transition: all 200ms ease;
        }

        .cap:hover,
        .cover:hover {
            border-color: rgba(255,53,77,0.42);
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.25);
        }

        .cap .idx,
        .cover .idx {
            color: var(--mp-red);
            font-family: "Space Grotesk", sans-serif;
            font-size: 11px;
            letter-spacing: 0.13em;
            font-weight: 700;
        }

        .cap h3,
        .cover h3 {
            margin: 12px 0 8px;
            font-family: "Space Grotesk", sans-serif;
            font-size: 17px;
            font-weight: 600;
            letter-spacing: -0.025em;
            color: var(--mp-white);
        }

        .cap p,
        .cover p {
            margin: 0;
            color: var(--mp-muted);
            font-size: 13px;
            line-height: 1.7;
        }

        a.cap-link {
            color: var(--mp-white) !important;
            text-decoration: none !important;
            display: block;
            height: 100%;
        }

        a.cap-link:hover h3 { color: var(--mp-red); }

        .cta-band {
            margin-top: 88px;
            padding: 39px 38px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 24px;
            border-radius: 12px;
            background:
                radial-gradient(ellipse at 85% 50%, rgba(255,53,77,0.12), transparent 45%),
                radial-gradient(ellipse at 15% 50%, rgba(255,107,154,0.025), transparent 45%),
                linear-gradient(120deg, #171319, #090A0D);
            border: 1px solid rgba(255,53,77,0.22);
        }

        .cta-band h2 {
            font-family: "Space Grotesk", sans-serif;
            font-weight: 600;
            font-size: clamp(29px, 3vw, 41px);
            letter-spacing: -0.05em;
            margin: 0 0 9px;
            color: var(--mp-white);
        }

        .cta-band p {
            margin: 0;
            color: #AAB5C1;
            max-width: 520px;
            line-height: 1.7;
            font-size: 14px;
        }

        .mp-footer {
            display: flex;
            justify-content: space-between;
            gap: 24px;
            margin-top: 30px;
            padding: 25px 0 8px;
            border-top: 1px solid var(--mp-border);
            color: var(--mp-muted);
            font-size: 12px;
            line-height: 1.8;
        }

        .mp-footer strong {
            color: var(--mp-white);
            font-family: "Space Grotesk", sans-serif;
            font-size: 15px;
            font-weight: 700;
        }

        @media (max-width: 980px) {
            .hero-grid, .split { grid-template-columns: 1fr; }
            .cap-grid, .cover-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .feature-strip { grid-template-columns: 1fr 1fr; }
            .hero-art { min-height: 450px; }
            .mp-nav-right a.mp-textlink { display: none; }
            .cta-band { flex-direction: column; align-items: flex-start; }
        }

        @media (max-width: 680px) {
            .block-container { padding-left: 1rem; padding-right: 1rem; }
            .hero-grid { padding-top: 48px; }
            .feature-strip, .cap-grid, .cover-grid { grid-template-columns: 1fr; }
            .feature { border-right: none; border-bottom: 1px solid var(--mp-border); }
            .hero-title { font-size: 43px; }
            .glass { position: static; min-width: 0; }
            .glass-layer {
                position: static;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-top: 12px;
            }
            .hero-art { min-height: 0; }
            .mp-footer { flex-direction: column; }
            .cta-band { padding: 27px 22px; }
        }
        </style>
        """
    )


def inject_dashboard_styles() -> None:
    show_html(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded');

        /* =========================================
           GLOBAL DASHBOARD THEME
        ========================================= */

        .stApp {
            background: #08090D !important;
            color: #F5F6FA !important;
            font-family: 'DM Sans', sans-serif !important;
        }

        html, body, [class*="css"],
        .stApp, .stApp p, .stApp li,
        .stApp label, .stApp h1, .stApp h2, .stApp h3 {
            font-family: 'DM Sans', sans-serif !important;
        }

        header[data-testid="stHeader"] {
            background: rgba(8,9,13,0.94) !important;
            backdrop-filter: blur(10px);
        }

        #MainMenu,
        footer,
        [data-testid="stDecoration"],
        [data-testid="stToolbar"] {
            display: none !important;
        }

        [data-testid="stSidebarNav"] { display: none !important; }

        [data-testid="stSidebar"] {
            background: #0D0F15 !important;
            border-right: 1px solid rgba(255,255,255,0.08) !important;
        }

        [data-testid="stSidebar"] * {
            font-family: 'DM Sans', sans-serif !important;
        }

        [data-testid="stSidebar"] [data-testid="stIconMaterial"] {
            font-family: "Material Symbols Rounded" !important;
            font-weight: normal !important;
            font-style: normal !important;
            font-size: 1.25rem !important;
            line-height: 1 !important;
            letter-spacing: normal !important;
            text-transform: none !important;
            white-space: nowrap;
            direction: ltr;
            font-feature-settings: "liga";
            -webkit-font-feature-settings: "liga";
            -webkit-font-smoothing: antialiased;
            display: inline-block;
            overflow: hidden;
        }

        [data-testid="stSidebarContent"] { padding-top: 1.1rem; }

        [data-testid="stPageLink"] { margin: 0.08rem 0; }

        [data-testid="stPageLink"] a {
            width: 100%;
            border-radius: 8px;
            padding: 0.46rem 0.7rem !important;
            color: #B9C0CF !important;
            text-decoration: none !important;
            font-size: 0.92rem;
            font-weight: 450;
            gap: 0.55rem;
        }

        [data-testid="stPageLink"] a:hover,
        [data-testid="stPageLink"] a[aria-current="page"] {
            background: rgba(255,53,77,0.13) !important;
            color: #FF5368 !important;
        }

        [data-testid="stPageLink"] span { color: inherit !important; }

        .block-container {
            max-width: 1280px;
            padding-top: 4.6rem;
            padding-bottom: 2.6rem;
            overflow: visible;
            background: transparent !important;
        }

        [data-testid="stVerticalBlock"],
        [data-testid="stMarkdown"] {
            overflow: visible !important;
        }

        /* =========================================
           PAGE HEADINGS AND TEXT
        ========================================= */

        .mp-eyebrow {
            display: block;
            color: #FF5368 !important;
            font-size: 0.74rem;
            font-weight: 580;
            letter-spacing: 0.16em;
            line-height: 1.7;
            margin: 0 0 0.4rem;
            padding-top: 0.15rem;
            overflow: visible;
        }

        .mp-h1, .mp-welcome h1 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            letter-spacing: -0.045em !important;
            color: #F5F6FA !important;
            font-size: clamp(2rem, 3vw, 2.7rem);
            line-height: 1.08;
            margin: 0;
        }

        .mp-lede, .mp-welcome p {
            color: #A1A8B8 !important;
            font-size: 1.02rem;
            line-height: 1.65;
            max-width: 720px;
            margin: 0.7rem 0 0;
        }

        .mp-pagehead { margin-bottom: 1.15rem; overflow: visible; }

        .mp-section { margin: 1.15rem 0 0.35rem; }

        .mp-section h2 {
            margin: 0;
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 1.12rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: #F5F6FA !important;
        }

        .mp-caption {
            margin: 0.25rem 0 0;
            color: #A1A8B8 !important;
            font-size: 0.86rem;
            line-height: 1.5;
        }

        /* =========================================
           KPI CARDS
        ========================================= */

        .mp-kpi {
            background: #12151E !important;
            border: 1px solid rgba(255,255,255,0.09) !important;
            border-radius: 14px !important;
            padding: 0.95rem 1rem 0.9rem;
            min-height: 118px;
        }

        .mp-kpi-label {
            color: #A1A8B8 !important;
            font-size: 0.72rem;
            letter-spacing: 0.08em;
            font-weight: 560;
        }

        .mp-kpi-value {
            margin-top: 0.45rem;
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 1.85rem;
            font-weight: 600 !important;
            letter-spacing: -0.03em;
            color: #FF5368 !important;
            line-height: 1;
        }

        .mp-kpi-note {
            margin-top: 0.45rem;
            color: #A1A8B8 !important;
            font-size: 0.78rem;
            line-height: 1.4;
        }

        /* =========================================
           WELCOME AND PERIOD CARD
        ========================================= */

        .mp-welcome {
            display: flex;
            justify-content: space-between;
            gap: 24px;
            align-items: flex-end;
            margin-bottom: 1.1rem;
        }

        .mp-period {
            min-width: 180px;
            background: #171A25 !important;
            border: 1px solid rgba(123,167,255,0.2) !important;
            color: #F5F6FA;
            border-radius: 12px;
            padding: 0.9rem 1rem;
        }

        .mp-period span, .mp-period em {
            display: block;
            font-style: normal;
            color: #7BA7FF !important;
            font-size: 0.68rem;
            letter-spacing: 0.14em;
            font-weight: 560;
        }

        .mp-period strong {
            display: block;
            margin: 0.35rem 0 0.3rem;
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 1.45rem;
            font-weight: 600;
            color: #F5F6FA !important;
        }

        .mp-period small { color: #A1A8B8; font-size: 0.75rem; }

        /* =========================================
           FINDINGS AND RECOMMENDATIONS
        ========================================= */

        .mp-callout, .mp-finding {
            background: #12151E !important;
            border: 1px solid rgba(255,255,255,0.09) !important;
            border-radius: 12px;
            padding: 0.9rem 1rem 0.85rem;
            margin-bottom: 0.7rem;
        }

        .mp-callout p, .mp-finding p {
            margin: 0.35rem 0 0;
            color: #C1C7D3 !important;
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .mp-kicker {
            font-size: 0.68rem;
            letter-spacing: 0.14em;
            font-weight: 600;
            color: #FF5368 !important;
        }

        .mp-finding h3 {
            margin: 0.3rem 0 0;
            font-size: 1rem;
            letter-spacing: -0.02em;
            color: #F5F6FA !important;
        }

        .mp-observed { border-top: 2px solid #FF354D !important; }
        .mp-statistical { border-top: 2px solid #7BA7FF !important; }
        .mp-recommendation { border-top: 2px solid #FF6B9A !important; }
        .mp-limitation { border-top: 2px solid #65718A !important; }

        .mp-statgrid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
        }

        .mp-stat {
            background: #191D28 !important;
            border-radius: 10px;
            padding: 0.75rem 0.8rem;
        }

        .mp-stat span {
            display: block;
            color: #A1A8B8 !important;
            font-size: 0.72rem;
            letter-spacing: 0.04em;
        }

        .mp-stat strong {
            display: block;
            margin-top: 0.25rem;
            font-size: 1rem;
            color: #F5F6FA !important;
        }

        /* =========================================
           SIDEBAR BRAND AND FOOTER
        ========================================= */

        .side-brand {
            display: flex;
            gap: 10px;
            align-items: center;
            padding: 0.2rem 0.35rem 0.9rem;
        }

        .side-name {
            color: #F5F6FA;
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 1.25rem;
            letter-spacing: -0.03em;
            line-height: 1;
        }

        .side-sub {
            margin-top: 4px;
            color: #91B7A5;
            font-size: 0.62rem;
            letter-spacing: 0.14em;
        }

        .side-label {
            color: #91B7A5;
            font-size: 0.66rem;
            letter-spacing: 0.16em;
            font-weight: 580;
            padding: 0.35rem 0.75rem 0.45rem;
        }

        .side-note {
            margin-top: 1.3rem;
            padding: 0.85rem 0.75rem 0.2rem;
            border-top: 1px solid rgba(245,245,240,0.1);
        }

        .side-note p {
            color: #A2AEA7 !important;
            font-size: 0.78rem;
            line-height: 1.5;
            margin: 0.35rem 0 0;
        }

        .side-note strong {
            color: #F5F6FA;
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 1.05rem;
            font-weight: 600;
        }

        .mp-foot {
            margin-top: 1.6rem;
            color: #A1A8B8 !important;
            font-size: 0.78rem;
            border-top: 1px solid rgba(255,255,255,0.10);
            padding-top: 0.8rem;
        }

        /* =========================================
           FORM LABELS AND INPUTS
        ========================================= */

        div[data-testid="stSelectbox"] label,
        div[data-testid="stMultiSelect"] label,
        div[data-testid="stTextInput"] label,
        div[data-testid="stNumberInput"] label,
        div[data-testid="stDateInput"] label {
            color: #AEB6C7 !important;
            font-size: 0.72rem !important;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 580;
        }

        /* Text input controls */
        .stApp div[data-testid="stTextInput"] input,
        .stApp div[data-testid="stNumberInput"] input,
        .stApp div[data-testid="stDateInput"] input {
            background: #171B26 !important;
            color: #F5F6FA !important;
            -webkit-text-fill-color: #F5F6FA !important;
            border: 1px solid #343B4D !important;
            border-radius: 9px !important;
        }

        /* =========================================
           DARK SELECTBOX — CONTROL SURFACE
        ========================================= */

        .stApp div[data-testid="stSelectbox"] [data-baseweb="select"] {
            background-color: #171B26 !important;
            border-radius: 9px !important;
        }

        .stApp div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background-color: #171B26 !important;
            border: 1px solid #343B4D !important;
            border-radius: 9px !important;
            box-shadow: none !important;
        }

        .stApp div[data-testid="stSelectbox"] [data-baseweb="select"] [role="combobox"],
        .stApp div[data-testid="stSelectbox"] [data-baseweb="select"] [class*="singleValue"],
        .stApp div[data-testid="stSelectbox"] [data-baseweb="select"] [class*="placeholder"] {
            color: #F5F6FA !important;
            -webkit-text-fill-color: #F5F6FA !important;
        }

        .stApp div[data-testid="stSelectbox"] [data-baseweb="select"] input {
            color: #F5F6FA !important;
            -webkit-text-fill-color: #F5F6FA !important;
        }

        .stApp div[data-testid="stSelectbox"] [data-baseweb="select"] svg {
            fill: #A7B0C2 !important;
            color: #A7B0C2 !important;
        }

        /* Multiselect controls */
        .stApp div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
            background: #171B26 !important;
            border: 1px solid #343B4D !important;
            border-radius: 9px !important;
        }

        .stApp div[data-testid="stMultiSelect"] [data-baseweb="select"] span {
            color: #F5F6FA !important;
        }

        /* Dropdown popover surface */
        body [data-baseweb="popover"],
        body [data-baseweb="popover"] > div,
        body [data-baseweb="popover"] ul {
            background-color: #171B26 !important;
            border-color: #343B4D !important;
        }

        /* Dropdown options */
        body [data-baseweb="popover"] [role="option"],
        body [data-baseweb="popover"] [role="option"] * {
            background-color: transparent !important;
            color: #F5F6FA !important;
            -webkit-text-fill-color: #F5F6FA !important;
        }

        body [data-baseweb="popover"] [role="option"]:hover {
            background-color: #292E3C !important;
        }

        /* Focused selectbox */
        .stApp div[data-testid="stSelectbox"] [data-baseweb="select"]:focus-within > div {
            border-color: #FF5368 !important;
            box-shadow: 0 0 0 1px #FF5368 !important;
        }

        /* =========================================
           BUTTONS
        ========================================= */

        .stButton > button {
            background: #FF354D !important;
            color: #FFFFFF !important;
            border: 1px solid #FF354D !important;
            border-radius: 9px !important;
        }

        .stButton > button:hover {
            background: #E92D45 !important;
            border-color: #E92D45 !important;
        }

        /* =========================================
           EXPANDERS AND TABS
        ========================================= */

        [data-testid="stExpander"] {
            background: #12151E !important;
            border: 1px solid rgba(255,255,255,0.09) !important;
        }

        button[data-baseweb="tab"] {
            color: #A1A8B8 !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #FF5368 !important;
        }

        /* =========================================
           DATAFRAMES AND METRICS
        ========================================= */

        [data-testid="stDataFrame"] {
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 10px;
        }

        [data-testid="stMetric"] {
            background: #12151E !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 12px !important;
            padding: 16px 18px !important;
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] p,
        [data-testid="stMetricLabel"] div {
            color: #A7B0C2 !important;
            -webkit-text-fill-color: #A7B0C2 !important;
        }

        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] div {
            color: #F5F6FA !important;
            -webkit-text-fill-color: #F5F6FA !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
        }

        [data-testid="stMetricDelta"] {
            color: #B8E6CF !important;
            -webkit-text-fill-color: #B8E6CF !important;
        }

        [data-testid="stMetric"] svg {
            color: #A7B0C2 !important;
            fill: #A7B0C2 !important;
        }

        hr {
            border-color: rgba(255,255,255,0.10) !important;
        }

        /* =========================================
           RESPONSIVE LAYOUT
        ========================================= */

        @media (max-width: 900px) {
            .mp-welcome, .mp-statgrid { display: block; }
            .mp-period { margin-top: 0.9rem; }
            .mp-stat { margin-bottom: 8px; }
        }
        </style>
        """
    )
