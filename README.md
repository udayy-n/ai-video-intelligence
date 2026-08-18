# 🎥 AI Video Intelligence Platform

An AI-powered system that automatically analyzes YouTube videos and generates structured reports using Automatic Speech Recognition (ASR) and Generative AI.

## 📌 Project Overview

The AI Video Intelligence Platform is designed to reduce the time required to understand long-form video content such as lectures, meetings, interviews, tutorials, webinars, and educational videos.

The system accepts a YouTube URL, extracts the audio, converts speech into text using OpenAI Whisper, and analyzes the generated transcript using Google's Gemini 2.5 Flash Large Language Model.

The final output is a structured AI-generated report containing summaries, important topics, key insights, action items, frequently asked questions, and a conclusion.

---

## 🎯 Problem Statement

Long-form video content contains valuable information but requires significant time and effort to consume. Manually watching lengthy lectures, meetings, interviews, and tutorials to identify important information is inefficient.

The proposed system automates this process by converting video content into text and using Generative AI to extract meaningful and structured information.

---

## 🎯 Objectives

- Extract audio automatically from YouTube videos.
- Convert speech into text using Whisper ASR.
- Analyze transcripts using Gemini 2.5 Flash.
- Generate structured AI reports.
- Extract key topics and insights.
- Identify action items.
- Generate frequently asked questions.
- Display YouTube video metadata.
- Provide an interactive Streamlit interface.
- Generate downloadable PDF reports.
- Maintain analysis history using SQLite.

---

## ⚙️ System Architecture

```text
                    YouTube URL
                         │
                         ▼
                    ┌─────────┐
                    │  yt-dlp │
                    └────┬────┘
                         │
                         ▼
                    Audio Extraction
                         │
                         ▼
                  ┌─────────────┐
                  │ Whisper ASR │
                  └──────┬──────┘
                         │
                         ▼
                     Transcript
                         │
                         ▼
              ┌────────────────────┐
              │  Gemini 2.5 Flash  │
              │       LLM          │
              └─────────┬──────────┘
                        │
                        ▼
                Structured Report
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        Streamlit UI          PDF Export
              │
              ▼
        SQLite History
        