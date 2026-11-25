from components.render import show_html

_MARK = """
<svg width="36" height="36" viewBox="0 0 34 34" fill="none" aria-hidden="true">
    <circle cx="17" cy="17" r="15.2"
        stroke="#FFD76A" stroke-width="1.2"/>
    <path d="M6 19c3.2-.8 4.4-6.2 7.4-6.2
        2.6 0 3.2 7.4 6.2 7.4
        2.8 0 3.8-6.2 7.2-5.2"
        stroke="#FFFFFF" stroke-width="1.5"
        stroke-linecap="round"/>
    <circle cx="17" cy="16.2" r="2" fill="#FF9B45"/>
</svg>
"""


_ART = """
<svg viewBox="0 0 640 540"
     fill="none"
     xmlns="http://www.w3.org/2000/svg"
     aria-hidden="true">

<defs>
    <linearGradient id="roadGlow" x1="40" y1="80" x2="600" y2="460">
        <stop offset="0" stop-color="#FF9B45"/>
        <stop offset="0.5" stop-color="#FFD76A"/>
        <stop offset="1" stop-color="#FF354D"/>
    </linearGradient>

    <radialGradient id="junctionGlow">
        <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.9"/>
        <stop offset="0.35" stop-color="#FFD76A" stop-opacity="0.45"/>
        <stop offset="1" stop-color="#FFD76A" stop-opacity="0"/>
    </radialGradient>

    <filter id="trafficGlow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feMerge>
            <feMergeNode in="blur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>

    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="9"/>
    </filter>
</defs>

<!-- Subtle city grid -->
<g stroke="#AAB0BA" stroke-width="0.8" opacity="0.10">
    <path d="M30 85 H610"/>
    <path d="M30 165 H610"/>
    <path d="M30 245 H610"/>
    <path d="M30 325 H610"/>
    <path d="M30 405 H610"/>
    <path d="M30 485 H610"/>

    <path d="M80 35 V510"/>
    <path d="M160 35 V510"/>
    <path d="M240 35 V510"/>
    <path d="M320 35 V510"/>
    <path d="M400 35 V510"/>
    <path d="M480 35 V510"/>
    <path d="M560 35 V510"/>
</g>

<!-- Background road network -->
<g class="traffic-road">
    <path d="M35 390 C115 365 155 280 235 260
             S390 200 600 230"/>

    <path d="M60 455 C155 420 210 350 295 310
             S460 265 610 325"/>

    <path d="M190 45 C220 125 260 185 320 235
             S405 325 435 490"/>

    <path d="M435 45 C460 115 490 165 525 215
             S570 300 610 380"/>

    <path d="M35 185 C110 165 175 190 235 225
             S345 280 420 365"/>

    <path d="M95 510 C145 440 185 390 245 350
             S365 300 480 105"/>

    <path d="M30 285 C125 280 175 310 245 330
             S400 385 590 460"/>
</g>

<!-- Soft glow behind major routes -->
<g fill="none" filter="url(#softGlow)" opacity="0.16">
    <path d="M35 390 C115 365 155 280 235 260
             S390 200 600 230"
          stroke="#FFD76A" stroke-width="13"/>

    <path d="M60 455 C155 420 210 350 295 310
             S460 265 610 325"
          stroke="#FF354D" stroke-width="12"/>

    <path d="M190 45 C220 125 260 185 320 235
             S405 325 435 490"
          stroke="#FFFFFF" stroke-width="10"/>

    <path d="M95 510 C145 440 185 390 245 350
             S365 300 480 105"
          stroke="#FF6B9A" stroke-width="10"/>
</g>

<!-- Headlights: white traffic moving forward -->
<g>
    <path class="traffic-headlights"
          d="M35 390 C115 365 155 280 235 260
             S390 200 600 230"/>

    <path class="traffic-headlights"
          d="M190 45 C220 125 260 185 320 235
             S405 325 435 490"/>

    <path class="traffic-headlights"
          d="M30 285 C125 280 175 310 245 330
             S400 385 590 460"/>
</g>

<!-- Warm yellow and amber traffic -->
<g>
    <path class="traffic-amber"
          d="M60 455 C155 420 210 350 295 310
             S460 265 610 325"/>

    <path class="traffic-amber"
          d="M435 45 C460 115 490 165 525 215
             S570 300 610 380"/>
</g>

<!-- Red tail lights moving in the opposite direction -->
<g>
    <path class="traffic-taillights"
          d="M600 230 C390 200 310 220 235 260
             S115 365 35 390"/>

    <path class="traffic-taillights"
          d="M435 490 C405 325 370 275 320 235
             S220 125 190 45"/>

    <path class="traffic-taillights"
          d="M590 460 C400 385 315 350 245 330
             S125 280 30 285"/>
</g>

<!-- Pink tail-light streams -->
<g>
    <path class="traffic-pink"
          d="M610 325 C460 265 380 285 295 310
             S155 420 60 455"/>

    <path class="traffic-pink"
          d="M480 105 C365 300 305 320 245 350
             S145 440 95 510"/>
</g>

<!-- Junction glow -->
<g>
    <circle cx="235" cy="260" r="27" fill="url(#junctionGlow)"/>
    <circle cx="320" cy="235" r="31" fill="url(#junctionGlow)"/>
    <circle cx="295" cy="310" r="26" fill="url(#junctionGlow)"/>
    <circle cx="245" cy="330" r="22" fill="url(#junctionGlow)"/>
    <circle cx="525" cy="215" r="20" fill="url(#junctionGlow)"/>
</g>

<!-- Bright junction points -->
<g class="traffic-node">
    <circle cx="235" cy="260" r="3.2" fill="#FFFFFF"/>
    <circle cx="320" cy="235" r="4" fill="#FFD76A"/>
    <circle cx="295" cy="310" r="3.5" fill="#FFFFFF"/>
    <circle cx="245" cy="330" r="3" fill="#FF9B45"/>
    <circle cx="525" cy="215" r="3.2" fill="#FFFFFF"/>
    <circle cx="435" cy="490" r="3" fill="#FF354D"/>
    <circle cx="190" cy="45" r="2.8" fill="#FFD76A"/>
    <circle cx="480" cy="105" r="2.8" fill="#FF6B9A"/>
</g>

<!-- Small illuminated intersections -->
<g fill="#FFFFFF" opacity="0.8">
    <circle cx="115" cy="365" r="1.5"/>
    <circle cx="155" cy="420" r="1.5"/>
    <circle cx="390" cy="200" r="1.5"/>
    <circle cx="460" cy="265" r="1.5"/>
    <circle cx="405" cy="325" r="1.5"/>
    <circle cx="570" cy="300" r="1.5"/>
</g>

</svg>
"""

_ICONS = {
    "ridership": """
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#B8E6CF" stroke-width="1.4">
    <path d="M4 16c2.2-1 3.2-5 6-5s2.4 6 5 6 3.2-5 5-4" stroke-linecap="round"/>
    <circle cx="12" cy="12" r="8.2"/>
    </svg>
    """,
    "patterns": """
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#B8E6CF" stroke-width="1.4">
    <path d="M4 16l4-5 3 3 5-7 4 4" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M4 20h16" stroke-linecap="round"/>
    </svg>
    """,
    "map": """
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#B8E6CF" stroke-width="1.4">
    <path d="M12 21s6-5.2 6-10a6 6 0 1 0-12 0c0 4.8 6 10 6 10z"/>
    <circle cx="12" cy="11" r="1.6" fill="#B8E6CF" stroke="none"/>
    </svg>
    """,
    "decision": """
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#B8E6CF" stroke-width="1.4">
    <circle cx="6" cy="12" r="2"/><circle cx="18" cy="7" r="2"/><circle cx="18" cy="17" r="2"/>
    <path d="M8 12h6M14 12l4-4M14 12l4 4" stroke-linecap="round"/>
    </svg>
    """,
}


def render_landing(
    *, ridership: str, transfers: str, stations: str, boroughs: str, period: str
) -> None:

    show_html(
        f"""
        <div class="mp" id="top">

        <div class="mp-bg">
        <svg viewBox="0 0 1200 700" width="100%" height="100%" fill="none" aria-hidden="true">
        <g stroke="rgba(184,230,207,0.16)" stroke-width="1">
        <path d="M760 40c80 90 90 180 40 260s-40 170 30 250"/>
        <path d="M860 20c-20 120 40 180 20 280s-80 160-20 250"/>
        <path d="M980 80c-60 80-40 170 10 240s20 150-30 220"/>
        </g>
        </svg>
        </div>

        <nav class="mp-nav">
            <a class="mp-brand" href="#top" target="_self">
                {_MARK}
                <span>
                    <span class="mp-brand-name">ChronoTunnel</span>
                    <span class="mp-brand-sub">URBAN MOBILITY INTELLIGENCE</span>
                </span>
            </a>

            <div class="mp-nav-right">
                <a class="mp-textlink" href="#top" target="_self">Home</a>
                <a class="mp-textlink" href="#platform" target="_self">Explore</a>
                <a class="mp-textlink" href="#about" target="_self">About</a>
                <a class="mp-cta" href="?nav=dashboard" target="_self">Get Started</a>
            </div>
        </nav>

        <section class="hero-grid">
            <div class="hero-copy">
                <div class="kicker">NYC TRANSIT INTELLIGENCE | {period}</div>

                <h1>
    <span class="hero-title-red">Beyond the numbers.</span>
    <span class="hero-title-blue">Understand the movement.</span>
</h1>

                <p class="lede">
                    Explore the pulse of New York City's transit network.
                    Discover ridership patterns, uncover geographic insights
                    and understand how mobility changes across the city.
                </p>

                <div class="hero-actions">
                    <a class="btn-primary" href="?nav=dashboard" target="_self">
                        Explore ChronoTunnel
                    </a>
                    <a class="btn-ghost" href="#features" target="_self">
                        Discover the Platform
                    </a>
                </div>
            </div>

            <div class="hero-art">
                {_ART}

                <div class="glass-layer">
                    <div class="glass g-ridership">
                        <span>RIDERSHIP</span>
                        <strong>{ridership}</strong>
                    </div>

                    <div class="glass g-stations">
                        <span>STATION NETWORK</span>
                        <strong>{stations}</strong>
                    </div>

                    <div class="glass g-boroughs">
                        <span>BOROUGHS</span>
                        <strong>{boroughs}</strong>
                    </div>

                    <div class="glass g-years">
                        <span>TRANSIT PATTERNS</span>
                        <strong>{period}</strong>
                    </div>
                </div>
            </div>
        </section>

        <section class="feature-strip" id="features">
            <article class="feature">
                {_ICONS["ridership"]}
                <h3>Explore Ridership</h3>
                <p>Understand network-wide passenger activity.</p>
            </article>

            <article class="feature">
                {_ICONS["patterns"]}
                <h3>Discover Patterns</h3>
                <p>Explore temporal and hourly mobility trends.</p>
            </article>

            <article class="feature">
                {_ICONS["map"]}
                <h3>Map the Network</h3>
                <p>Investigate geographic ridership distribution.</p>
            </article>

            <article class="feature">
                {_ICONS["decision"]}
                <h3>Make Better Decisions</h3>
                <p>Examine statistical findings and mobility insights.</p>
            </article>
        </section>

        <section class="section" id="about">
            <div class="split">
                <div>
                    <div class="eyebrow">THE PLATFORM</div>

                    <h2>
                        A workspace for reading the city's recorded movement.
                    </h2>

                    <p class="intro">
                        ChronoTunnel organizes New York City transit ridership
                        from January 2020 through December 2024. It is a
                        historical intelligence product: annual change,
                        station rank, borough share, sampled hour-of-day,
                        and geography, with the study limits kept in view.
                    </p>
                </div>

                <div class="quiet-stats">
                    <div>
                        <strong>{ridership}</strong>
                        <span>
                            Recorded ridership, {period}.
                            Transfers are already included.
                        </span>
                    </div>

                    <div>
                        <strong>{transfers}</strong>
                        <span>
                            Recorded transfers, reported separately
                            and not added to ridership.
                        </span>
                    </div>

                    <div>
                        <strong>{stations}</strong>
                        <span>
                            Station identifiers across five boroughs
                            and three transit modes.
                        </span>
                    </div>
                </div>
            </div>
        </section>

        <section class="section" id="platform">
            <div class="eyebrow">ANALYTICAL CAPABILITIES</div>
            <h2>Six ways into the same network.</h2>

            <div class="cap-grid">

                <a class="cap-link" href="?nav=overview" target="_self">
                    <div class="cap">
                        <div class="idx">01</div>
                        <h3>Ridership overview</h3>
                        <p>
                            Annual trajectory, borough contribution,
                            mode mix, and the leading station complexes.
                        </p>
                    </div>
                </a>

                <a class="cap-link" href="?nav=temporal" target="_self">
                    <div class="cap">
                        <div class="idx">02</div>
                        <h3>Temporal analysis</h3>
                        <p>
                            Monthly change, seasonality, and the
                            Wednesday–Saturday hourly sample.
                        </p>
                    </div>
                </a>

                <a class="cap-link" href="?nav=stations" target="_self">
                    <div class="cap">
                        <div class="idx">03</div>
                        <h3>Station analysis</h3>
                        <p>
                            Search the network and compare complexes
                            without merging shared station identifiers.
                        </p>
                    </div>
                </a>

                <a class="cap-link" href="?nav=boroughs" target="_self">
                    <div class="cap">
                        <div class="idx">04</div>
                        <h3>Borough analysis</h3>
                        <p>
                            Ridership, transfers, station counts,
                            and average station totals side by side.
                        </p>
                    </div>
                </a>

                <a class="cap-link" href="?nav=geo" target="_self">
                    <div class="cap">
                        <div class="idx">05</div>
                        <h3>Geospatial analysis</h3>
                        <p>
                            Station maps, a ridership heatmap,
                            and ridership-weighted borough centroids.
                        </p>
                    </div>
                </a>

                <a class="cap-link" href="?nav=insights" target="_self">
                    <div class="cap">
                        <div class="idx">06</div>
                        <h3>Insights</h3>
                        <p>
                            Observed results, the paired statistical
                            comparison, recommendations, and limits.
                        </p>
                    </div>
                </a>

            </div>
        </section>

        <section class="section" id="coverage">
            <div class="eyebrow">DATASET COVERAGE</div>
            <h2>What the records contain.</h2>

            <div class="cover-grid">
                <article class="cover">
                    <div class="idx">MONTHLY</div>
                    <h3>Sixty complete months</h3>
                    <p>
                        Station-level monthly ridership from January 2020
                        through December 2024, used for trends, ranks,
                        and borough totals.
                    </p>
                </article>

                <article class="cover">
                    <div class="idx">HOURLY SAMPLE</div>
                    <h3>120 selected dates</h3>
                    <p>
                        One Wednesday and one Saturday in each month.
                        This is a sample for comparison, not a continuous
                        hourly series.
                    </p>
                </article>

                <article class="cover">
                    <div class="idx">GEOGRAPHY</div>
                    <h3>Representative coordinates</h3>
                    <p>
                        Map positions are ridership-weighted references.
                        They are not exact station entrance locations.
                    </p>
                </article>
            </div>
        </section>

        <section class="cta-band">
            <div>
                <h2>Enter the workspace.</h2>
                <p>
                    Move from the network overview into time, stations,
                    boroughs, maps, and the study's findings.
                </p>
            </div>

            <a class="btn-primary" href="?nav=dashboard" target="_self">
                Explore ChronoTunnel
            </a>
        </section>

        <footer class="mp-footer">
            <div>
                <strong>ChronoTunnel</strong><br>
                Urban Mobility Intelligence Platform<br>
                Turning Transit Data into Smarter Mobility Decisions.
            </div>

            <div>
                New York City transit records<br>
                {period}<br>
                Historical study. Not a live ridership feed.
            </div>
        </footer>

        </div>
        """
    )
