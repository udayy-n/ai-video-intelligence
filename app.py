import streamlit as st
import os
import re

from datetime import datetime

from modules.downloader import download_audio
from modules.transcriber import transcribe_audio
from modules.report_generator import generate_report
from modules.video_info import get_video_info
from modules.cache import (
    cache_exists,
    save_cache,
    load_cache,
    get_video_id
)
from modules.database import (
    save_report,
    get_recent_reports,
    get_report_by_url
)
from modules.pdf_generator import generate_pdf


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Video Intelligence",
    layout="wide"
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("AI Video Intelligence")

st.sidebar.markdown("---")

st.sidebar.info(
    "Analyze YouTube videos and generate professional AI reports."
)

# -----------------------------------
# RECENT REPORTS
# -----------------------------------

st.sidebar.markdown("---")

st.sidebar.subheader("📚 Recent Reports")

try:

    recent_reports = get_recent_reports()

    for item in recent_reports:

        st.sidebar.write(
            f"• {item[0]}"
        )

except Exception:

    st.sidebar.write(
        "No reports yet"
    )

# -----------------------------------
# HEADER
# -----------------------------------

st.title(
    "🎥 AI Video Intelligence Platform"
)

st.caption(
    "AI-Powered YouTube Video Report Generator"
)

# -----------------------------------
# INPUT
# -----------------------------------

youtube_url = st.text_input(
    "Enter YouTube URL"
)

# -----------------------------------
# BUTTON
# -----------------------------------

if st.button("Generate Report"):

    if not youtube_url:

        st.warning(
            "Please enter a YouTube URL"
        )

    else:

        try:

            progress = st.progress(0)

            # -----------------------------------
            # VIDEO INFO
            # -----------------------------------

            with st.spinner(
                "Fetching Video Metadata..."
            ):

                video_info = get_video_info(
                    youtube_url
                )

            progress.progress(10)

            # -----------------------------------
            # DATABASE CHECK
            # -----------------------------------

            video_id = get_video_id(
                youtube_url
            )

            existing_report = get_report_by_url(
                video_id
            )

            if existing_report:

                report_path = existing_report[0]

                if os.path.exists(
                    report_path
                ):

                    with open(
                        report_path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        cached_report = f.read()

                    st.success(
                        "✅ Report Loaded From Database"
                    )

                    st.image(
                        video_info["thumbnail"],
                        use_container_width=True
                    )

                    st.markdown(
                        cached_report
                    )

                    st.stop()

            # -----------------------------------
            # DOWNLOAD AUDIO
            # -----------------------------------

            with st.spinner(
                "Downloading Audio..."
            ):

                audio_file = download_audio(
                    youtube_url
                )

            progress.progress(30)

            # -----------------------------------
            # TRANSCRIBE / CACHE
            # -----------------------------------

            with st.spinner(
                "Generating Transcript..."
            ):

                if cache_exists(
                    youtube_url
                ):

                    transcript = load_cache(
                        youtube_url
                    )

                else:

                    transcript = transcribe_audio(
                        audio_file
                    )

                    save_cache(
                        youtube_url,
                        transcript
                    )

            progress.progress(60)

            # -----------------------------------
            # SAVE TRANSCRIPT
            # -----------------------------------

            os.makedirs(
                "transcripts",
                exist_ok=True
            )

            with open(
                "transcripts/transcript.txt",
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    transcript
                )

            # -----------------------------------
            # REPORT GENERATION
            # -----------------------------------

            with st.spinner(
                "Generating AI Report..."
            ):

                report = generate_report(
                    transcript
                )

            progress.progress(80)

            # -----------------------------------
            # SAVE REPORT
            # -----------------------------------

            os.makedirs(
                "reports",
                exist_ok=True
            )

            safe_title = re.sub(
                r"[^a-zA-Z0-9]",
                "_",
                video_info["title"]
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            report_path = (
                f"reports/{safe_title}_{timestamp}.md"
            )

            with open(
                report_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    report
                )

            # -----------------------------------
            # PDF GENERATION
            # -----------------------------------

            os.makedirs(
                "exports",
                exist_ok=True
            )

            pdf_path = generate_pdf(
                report
            )

            progress.progress(90)

            # -----------------------------------
            # SAVE DATABASE
            # -----------------------------------

            save_report(
                video_info["title"],
                video_id,
                report_path
            )

            progress.progress(100)

            st.success(
                "✅ Analysis Completed Successfully"
            )

            # -----------------------------------
            # THUMBNAIL
            # -----------------------------------

            st.image(
                video_info["thumbnail"],
                use_container_width=True
            )

            # -----------------------------------
            # VIDEO DETAILS
            # -----------------------------------

            duration = video_info.get(
                "duration",
                0
            )

            minutes = duration // 60
            seconds = duration % 60

            colA, colB = st.columns(2)

            with colA:

                st.info(
                    f"📺 Title: {video_info['title']}"
                )

                st.info(
                    f"🎬 Channel: {video_info['channel']}"
                )

            with colB:

                st.info(
                    f"👁 Views: {video_info['views']:,}"
                    if video_info.get("views")
                    else "👁 Views: N/A"
                )

                st.info(
                    f"⏱ Duration: {minutes}m {seconds}s"
                )

            # -----------------------------------
            # METRICS
            # -----------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Transcript Words",
                    len(
                        transcript.split()
                    )
                )

            with col2:

                st.metric(
                    "Report Words",
                    len(
                        report.split()
                    )
                )

            with col3:

                st.metric(
                    "Status",
                    "Complete"
                )

            # -----------------------------------
            # DOWNLOAD PDF
            # -----------------------------------

            with open(
                pdf_path,
                "rb"
            ) as pdf_file:

                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_file,
                    file_name="AI_Report.pdf",
                    mime="application/pdf"
                )

            # -----------------------------------
            # TABS
            # -----------------------------------

            tab1, tab2 = st.tabs(
                [
                    "📑 AI Report",
                    "📝 Transcript"
                ]
            )

            with tab1:

                st.markdown(
                    report
                )

            with tab2:

                st.write(
                    transcript
                )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )
