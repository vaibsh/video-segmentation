import json
import base64
import streamlit.components.v1 as components

from frontend.timeline import build_segments


def render_segmented_video(video_path, results):

    # ========================================================
    # VIDEO BASE64
    # ========================================================

    with open(video_path, "rb") as f:
        video_base64 = base64.b64encode(f.read()).decode()

    segments = build_segments(results)

    segments_json = json.dumps(segments)
    segments_json = segments_json.replace("</", "<\\/")

    html_code = f"""
    <style>

    .container {{
        width: 720px;
        margin: auto;
        font-family: Arial;
    }}

    video {{
        width: 100%;
        max-height: 380px;
        border-radius: 12px;
        background: black;
    }}

    /* =========================
       TIMELINE BASE
    ========================== */

    .timeline {{
        display: flex;
        height: 18px;
        margin-top: 12px;
        border-radius: 10px;
        overflow: hidden;
        background: #222;
        box-shadow: inset 0 0 6px rgba(0,0,0,0.5);
    }}


   .segment {{
        height: 100%;
        transition: all 0.25s ease;

        /* slightly more dimmed */
        opacity: 0.42;

        /* mild desaturation only */
        filter: saturate(0.7);

        transform: scaleY(1);
    }}

    /* =========================
       ACTIVE SEGMENT (🔥 MAIN CHANGE)
    ========================== */

    .segment.active {{
        opacity: 1 !important;

        /* stronger presence */
        filter: saturate(1.3) brightness(1.1) !important;

        transform: scaleY(1.6);

        /* richer glow (layered feel) */
        box-shadow:
            0 0 8px rgba(0, 255, 140, 0.8),
            0 0 16px rgba(0, 255, 140, 0.4);

        z-index: 10;
    }}

    /* =========================
       META PANEL
    ========================== */

    .meta {{
        margin-top: 16px;
        padding: 14px;
        border-radius: 12px;
        background: #111;
        color: white;
    }}

    .title {{
        font-size: 20px;
        font-weight: bold;
        color: #00ff99;
    }}

    .frames {{
        font-size: 13px;
        color: #aaa;
        margin-top: 6px;
    }}

    .about {{
        margin-top: 10px;
        font-size: 14px;
        line-height: 1.5;
        color: #ddd;
    }}

    </style>

    <div class="container">

        <video id="videoPlayer" controls autoplay>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>

        <div class="timeline" id="timeline"></div>

        <div class="meta">
            <div class="title" id="activity">Loading...</div>
            <div class="frames" id="frames"></div>
            <div class="about" id="about"></div>
        </div>

    </div>

    <script>

    const segments = JSON.parse('{segments_json}');

    const video = document.getElementById("videoPlayer");
    const timeline = document.getElementById("timeline");

    const activityEl = document.getElementById("activity");
    const framesEl = document.getElementById("frames");
    const aboutEl = document.getElementById("about");

    const colors = [
        "#00ff88",
        "#00c2ff",
        "#ffcc00",
        "#ff4d6d",
        "#a855f7"
    ];

    const totalDuration = segments[segments.length - 1].end_sec;

    // ========================================================
    // BUILD TIMELINE
    // ========================================================

    segments.forEach((seg, i) => {{

        const d = document.createElement("div");
        d.className = "segment";

        const width = ((seg.end_sec - seg.start_sec) / totalDuration) * 100;

        d.style.width = width + "%";
        d.style.background = colors[i % colors.length];

        d.id = "seg-" + i;

        timeline.appendChild(d);
    }});

    function update() {{

        const t = video.currentTime;

        let idx = 0;

        for (let i = 0; i < segments.length; i++) {{
            if (t >= segments[i].start_sec && t <= segments[i].end_sec) {{
                idx = i;
                break;
            }}
        }}

        const s = segments[idx];

        // =========================
        // TEXT UPDATE
        // =========================

        activityEl.innerText = s.activity;
        framesEl.innerText = `Frames: ${{s.start_frame}} → ${{s.end_frame}}`;
        aboutEl.innerText = s.about;

        // =========================
        // RESET ALL
        // =========================

        for (let i = 0; i < segments.length; i++) {{
            const el = document.getElementById("seg-" + i);
            if (el) el.classList.remove("active");
        }}

        // =========================
        // HIGHLIGHT ACTIVE
        // =========================

        const active = document.getElementById("seg-" + idx);
        if (active) active.classList.add("active");
    }}

    video.addEventListener("timeupdate", update);
    video.addEventListener("loadeddata", update);

    video.addEventListener("ended", () => {{
        video.currentTime = 0;
        video.play();
    }});

    </script>
    """

    components.html(
        html_code,
        height=720,
        scrolling=False
    )