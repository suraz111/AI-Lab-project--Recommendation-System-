"""
RECOM.ai — Multi-Domain Recommendation Portal 🔮
Architecture:
1. High-Contrast Stark Brutalist Authentication Gateway (Login / Sign Up / Demo Access).
2. High-Contrast Stark Portal Interface (Accessible only after successful authentication).
3. Domains: Movies (Bollywood, Tollywood, Hollywood, Nepali Cinema), Products E-Commerce (INR ₹), and Career Pathways.
"""

import os
import base64
import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
import html

from models import MovieRecommender, ProductRecommender, CourseRecommender
import database as db
from evaluation import evaluate_models
from components import habit_auth

# Page Configuration
st.set_page_config(
    page_title="RECOM.ai — Intelligence Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stark High-Contrast Brutalist Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Core Palette: Paper and Signal (#FDFBF7 Warm Paper Canvas, #FFFFFF Cards, #000000 Borders & Ink) */
    .stApp {
        background-color: #FDFBF7 !important;
        color: #000000 !important;
    }

    /* Header background transparency while preserving sidebar controls */
    header[data-testid="stHeader"],
    div[data-testid="stHeader"],
    .stAppHeader {
        background: transparent !important;
        background-color: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }

    /* Ensure sidebar collapse & expand buttons remain visible and clickable */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="stSidebarHeader"] button {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
    }

    .main, section.main, .stMain {
        padding-top: 0px !important;
        margin-top: 0px !important;
    }

    /* Main Container Padding - Placed cleanly at the top of the browser window */
    .main .block-container,
    div[data-testid="stMainBlockContainer"],
    [data-testid="block-container"],
    .block-container {
        padding-top: 1.2rem !important;
        margin-top: 0rem !important;
        max-width: 1240px !important;
    }

    /* Top Header Logout Button Accent */
    div[class*="st-key-top_logout_btn"] button {
        background: linear-gradient(135deg, #E11D48 0%, #991B1B 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        box-shadow: 3.5px 3.5px 0px #000000 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        padding: 0.5rem 0.5rem !important;
        min-height: auto !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }

    div[class*="st-key-top_logout_btn"] button * {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    div[class*="st-key-top_logout_btn"] button:hover {
        background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%) !important;
        transform: translate(-1px, -1px) !important;
        box-shadow: 4.5px 4.5px 0px #000000 !important;
    }

    /* Top Header Recom.AI Clickable Banner & Overlay Button */
    .recom-banner-box {
        display: flex;
        align-items: center;
        gap: 12px;
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
        border: 2.5px solid #000000;
        box-shadow: 4px 4px 0px #000000;
        padding: 0 18px;
        height: 52px;
        box-sizing: border-box;
        cursor: pointer;
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
        white-space: nowrap;
        overflow: hidden;
    }

    div[class*="st-key-top_banner_home_btn"] {
        margin-top: -52px !important;
        height: 52px !important;
        position: relative !important;
        z-index: 10 !important;
        margin-bottom: 1.2rem !important;
    }

    div[class*="st-key-top_banner_home_btn"] button {
        width: 100% !important;
        height: 52px !important;
        min-height: 52px !important;
        max-height: 52px !important;
        opacity: 0 !important;
        cursor: pointer !important;
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    div[class*="st-key-top_banner_home_btn"] button:focus,
    div[class*="st-key-top_banner_home_btn"] button:active {
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }

    /* Interactive Hover Effect for RECOM.AI Banner when button or banner is hovered */
    div[data-testid="stColumn"]:has(div[class*="st-key-top_banner_home_btn"] button:hover) .recom-banner-box,
    .recom-banner-box:hover {
        transform: translate(-1.5px, -1.5px);
        box-shadow: 6px 6px 0px #FF2E93 !important;
        border-color: #FF2E93 !important;
    }

    /* Top Header Portal Navigation Bar */
    .portal-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.95rem 1.6rem;
        background: #FFFFFF !important;
        border: 2.5px solid #000000 !important;
        box-shadow: 4px 4px 0px #000000 !important;
        border-radius: 0px;
        margin-bottom: 1.6rem;
    }

    .portal-brand {
        font-size: 1.25rem;
        font-weight: 800;
        color: #000000 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .portal-user-tag {
        font-size: 0.82rem;
        font-weight: 800;
        color: #FFFFFF !important;
        background: #000000 !important;
        padding: 0.35rem 0.85rem;
        border-radius: 0px;
        border: 2px solid #000000;
        text-transform: uppercase;
        box-shadow: 2.5px 2.5px 0px #000000;
        letter-spacing: 0.04em;
    }

    /* Minimalist Stark Cards */
    .min-card {
        background-color: #FFFFFF !important;
        border: 2.5px solid #000000 !important;
        box-shadow: 5px 5px 0px #000000 !important;
        border-radius: 0px !important;
        padding: 1.25rem !important;
        margin-bottom: 1.1rem !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    .min-card:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 7px 7px 0px #000000 !important;
    }

    .item-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #000000 !important;
        margin: 0 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.02em !important;
    }

    /* High-Contrast Tags */
    .tag-neutral {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        border-radius: 0px;
        background: #FFFFFF;
        color: #000000;
        border: 1.5px solid #000000;
        margin-right: 0.35rem;
        margin-bottom: 0.3rem;
    }

    .tag-accent {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        border-radius: 0px;
        background: #000000;
        color: #FFFFFF;
        border: 1.5px solid #000000;
        margin-right: 0.35rem;
        margin-bottom: 0.3rem;
    }

    .tag-match {
        float: right;
        font-size: 0.82rem;
        font-weight: 800;
        color: #FFFFFF;
        background: #000000;
        padding: 0.25rem 0.65rem;
        border-radius: 0px;
        border: 2px solid #000000;
        box-shadow: 2.5px 2.5px 0px #000000;
        letter-spacing: 0.03em;
    }

    /* Explanation Box */
    .reason-box {
        background: #FAFAFA;
        border: 2px solid #000000;
        border-left: 6px solid #000000;
        padding: 0.65rem 0.85rem;
        margin-top: 0.75rem;
        border-radius: 0px;
        font-size: 0.84rem;
        font-weight: 500;
        color: #000000;
        line-height: 1.45;
    }

    /* =========================================================================
       VELVET & BRASS THEATRE THEME (MOVIES & CINEMA DOMAIN)
       ========================================================================= */
    .cinema-marquis {
        background: linear-gradient(135deg, #7A0C24 0%, #4D0717 100%);
        border: 2.5px solid #C5A059;
        box-shadow: 4px 4px 0px #1A050B;
        padding: 14px 20px;
        margin-bottom: 1.3rem;
    }

    .cinema-domain-badge {
        background: #C5A059 !important;
        color: #1A050B !important;
        font-weight: 900 !important;
        font-size: 0.68rem !important;
        padding: 4px 10px !important;
        border: 1.5px solid #1A050B !important;
        box-shadow: 2px 2px 0px #1A050B !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        display: inline-block !important;
    }

    .cinema-brass-pill {
        background: #FAF6EE !important;
        color: #7A0C24 !important;
        border: 1.5px solid #C5A059 !important;
        font-weight: 800 !important;
        font-size: 0.72rem !important;
        padding: 0.2rem 0.6rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
        display: inline-block !important;
        margin-right: 0.35rem !important;
        margin-bottom: 0.3rem !important;
    }

    .cinema-card {
        background-color: #FFFFFF !important;
        border: 2px solid #7A0C24 !important;
        border-top: 5px solid #C5A059 !important;
        box-shadow: 4px 4px 0px #1A050B !important;
        border-radius: 0px !important;
        padding: 1.15rem 1.25rem !important;
        margin-bottom: 0.65rem !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    .cinema-card:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0px #C5A059 !important;
    }

    /* Velvet & Brass: Movie Card Poster Layout */
    .cinema-card-body {
        display: flex !important;
        flex-direction: row !important;
        gap: 1.25rem !important;
        align-items: stretch !important;
    }

    .cinema-poster-frame {
        flex-shrink: 0 !important;
        width: 120px !important;
        height: 180px !important;
        aspect-ratio: 2 / 3 !important;
        background: linear-gradient(135deg, #7A0C24 0%, #3B0511 100%) !important;
        border: 2px solid #1A050B !important;
        box-shadow: 3px 3px 0px #C5A059 !important;
        overflow: hidden !important;
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .cinema-poster-img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        object-position: center !important;
        display: block !important;
        transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .cinema-card:hover .cinema-poster-img {
        transform: scale(1.05) !important;
    }

    .cinema-info-col {
        flex-grow: 1 !important;
        min-width: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
    }

    @media (max-width: 680px) {
        .cinema-card-body {
            flex-direction: column !important;
            align-items: center !important;
            text-align: center !important;
        }
        .cinema-poster-frame {
            width: 140px !important;
            height: 210px !important;
            margin-bottom: 0.75rem !important;
        }
        .cinema-info-col {
            width: 100% !important;
        }
    }

    .tag-cinema-industry {
        display: inline-block;
        padding: 0.2rem 0.65rem;
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        background: #7A0C24;
        color: #FAF5E8;
        border: 1.5px solid #1A050B;
        margin-right: 0.35rem;
        margin-bottom: 0.3rem;
    }

    .tag-cinema-genre {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        background: #FAF6EE;
        color: #1A050B;
        border: 1.5px solid #1A050B;
        margin-right: 0.35rem;
        margin-bottom: 0.3rem;
    }

    .tag-cinema-match {
        float: right;
        font-size: 0.82rem;
        font-weight: 900;
        color: #1A050B;
        background: #C5A059;
        padding: 0.25rem 0.7rem;
        border-radius: 0px;
        border: 1.5px solid #1A050B;
        box-shadow: 2px 2px 0px #1A050B;
        letter-spacing: 0.04em;
    }

    .cinema-reason-box {
        background: #FAF6EE;
        border: 1.5px solid #1A050B;
        border-left: 5px solid #7A0C24;
        padding: 0.7rem 0.9rem;
        margin-top: 0.75rem;
        font-size: 0.84rem;
        font-weight: 500;
        color: #1A050B;
        line-height: 1.45;
    }

    .cinema-buy-btn {
        display: inline-block !important;
        width: 100% !important;
        text-align: center !important;
        background: linear-gradient(135deg, #7A0C24 0%, #540919 100%) !important;
        color: #FAF5E8 !important;
        border: 2px solid #C5A059 !important;
        padding: 0.4rem 0.65rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.78rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        text-decoration: none !important;
        box-shadow: 3px 3px 0px #1A050B !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }

    .cinema-buy-btn:hover {
        background: #C5A059 !important;
        color: #1A050B !important;
        border-color: #1A050B !important;
        box-shadow: 4px 4px 0px #1A050B !important;
    }

    /* Velvet & Brass: Active Cinema Industry Filter Buttons */
    div[class*="st-key-btn_cat_"] button[kind="primary"],
    div[class*="st-key-btn_cat_"] button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #7A0C24 0%, #540919 100%) !important;
        color: #FAF5E8 !important;
        border: 2px solid #C5A059 !important;
        box-shadow: 3.5px 3.5px 0px #1A050B !important;
        font-weight: 800 !important;
    }

    div[class*="st-key-btn_cat_"] button[kind="primary"] * {
        color: #FAF5E8 !important;
        font-weight: 800 !important;
    }

    div[class*="st-key-btn_cat_"] button[kind="secondary"],
    div[class*="st-key-btn_cat_"] button[data-testid="stBaseButton-secondary"] {
        background: #FFFFFF !important;
        color: #1A050B !important;
        border: 2px solid #1A050B !important;
        box-shadow: 2px 2px 0px #1A050B !important;
        font-weight: 700 !important;
    }

    div[class*="st-key-btn_cat_"] button[kind="secondary"]:hover {
        background: #FAF6EE !important;
        color: #7A0C24 !important;
        border-color: #C5A059 !important;
    }

    /* Velvet & Brass: Cinema Card Action Buttons */
    div[class*="st-key-s_m_"] button,
    div[class*="st-key-l_m_"] button {
        background: #FFFFFF !important;
        color: #1A050B !important;
        border: 2px solid #1A050B !important;
        box-shadow: 2px 2px 0px #1A050B !important;
        font-weight: 800 !important;
        font-size: 0.78rem !important;
        padding: 0.35rem 0.5rem !important;
    }

    div[class*="st-key-s_m_"] button:hover,
    div[class*="st-key-l_m_"] button:hover {
        background: #FAF6EE !important;
        border-color: #C5A059 !important;
        color: #7A0C24 !important;
    }

    /* Velvet & Brass: Cinema Filter Box Office Console & Widgets */
    div[class*="st-key-sb_movie_industry"] label,
    div[class*="st-key-m_genres"] label,
    div[class*="st-key-input_movie_query"] label,
    div[class*="st-key-m_s"] label,
    div[class*="st-key-m_alpha"] label {
        color: #7A0C24 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.82rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    /* Velvet Multiselect Chips / Tags in Cinema Tab */
    div[class*="st-key-m_genres"] div[data-baseweb="tag"],
    div[class*="st-key-m_genres"] span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #7A0C24 0%, #5A0819 100%) !important;
        color: #FAF5E8 !important;
        border: 1.5px solid #C5A059 !important;
        border-radius: 0px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.74rem !important;
        letter-spacing: 0.03em !important;
        padding: 2px 6px !important;
        box-shadow: 1.5px 1.5px 0px #1A050B !important;
    }

    div[class*="st-key-m_genres"] div[data-baseweb="tag"] span,
    div[class*="st-key-m_genres"] div[data-baseweb="tag"] div {
        color: #FAF5E8 !important;
    }

    div[class*="st-key-m_genres"] div[data-baseweb="tag"] svg {
        fill: #FAF5E8 !important;
        color: #FAF5E8 !important;
    }

    /* Cinema Inputs and Selects border focus */
    div[class*="st-key-sb_movie_industry"] [data-baseweb="select"] > div,
    div[class*="st-key-m_genres"] [data-baseweb="select"] > div,
    div[class*="st-key-input_movie_query"] input {
        background-color: #FFFFFF !important;
        border: 2px solid #1A050B !important;
        border-radius: 0px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        color: #1A050B !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }

    div[class*="st-key-sb_movie_industry"] [data-baseweb="select"] > div:focus-within,
    div[class*="st-key-m_genres"] [data-baseweb="select"] > div:focus-within,
    div[class*="st-key-input_movie_query"] input:focus {
        border-color: #7A0C24 !important;
        box-shadow: 2.5px 2.5px 0px #C5A059 !important;
    }

    /* Velvet Sliders Track and Thumb */
    div[class*="st-key-m_s"] [data-baseweb="slider"] div[role="slider"],
    div[class*="st-key-m_alpha"] [data-baseweb="slider"] div[role="slider"] {
        background-color: #FAF5E8 !important;
        border: 2.5px solid #7A0C24 !important;
        box-shadow: 2px 2px 0px #C5A059 !important;
    }

    div[class*="st-key-m_s"] [data-testid="stThumbValue"],
    div[class*="st-key-m_alpha"] [data-testid="stThumbValue"] {
        color: #7A0C24 !important;
        font-weight: 900 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Cinema Reset Button */
    div[class*="st-key-btn_reset_m_filters"] {
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
    }

    div[class*="st-key-btn_reset_m_filters"] button {
        background: #FAF6EE !important;
        color: #7A0C24 !important;
        border: 2px solid #7A0C24 !important;
        box-shadow: 2.5px 2.5px 0px #1A050B !important;
        font-weight: 800 !important;
        font-size: 0.76rem !important;
        letter-spacing: 0.03em !important;
        text-transform: uppercase !important;
        padding: 0.4rem 0.4rem !important;
        margin-top: 0.5rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
        white-space: normal !important;
        overflow: hidden !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
    }

    div[class*="st-key-btn_reset_m_filters"] button div[data-testid="stMarkdownContainer"],
    div[class*="st-key-btn_reset_m_filters"] button div,
    div[class*="st-key-btn_reset_m_filters"] button p,
    div[class*="st-key-btn_reset_m_filters"] button span {
        white-space: normal !important;
        overflow: hidden !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        line-height: 1.2 !important;
        margin: 0 !important;
    }

    div[class*="st-key-btn_reset_m_filters"] button:hover {
        background: #7A0C24 !important;
        color: #FAF5E8 !important;
        border-color: #1A050B !important;
        box-shadow: 3.5px 3.5px 0px #C5A059 !important;
    }

    div[class*="st-key-btn_reset_m_filters"] button:hover * {
        color: #FAF5E8 !important;
    }

    /* Quick Keyword Chips in Cinema Filter */
    div[class*="st-key-mchip_"] {
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
    }

    div[class*="st-key-mchip_"] button {
        background: #FAF6EE !important;
        color: #1A050B !important;
        border: 1.5px solid #C5A059 !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        padding: 0.25rem 0.2rem !important;
        border-radius: 0px !important;
        box-shadow: 2px 2px 0px #1A050B !important;
        letter-spacing: 0.01em !important;
        min-height: 32px !important;
        height: auto !important;
        line-height: 1.15 !important;
        white-space: normal !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }

    div[class*="st-key-mchip_"] button div[data-testid="stMarkdownContainer"],
    div[class*="st-key-mchip_"] button div,
    div[class*="st-key-mchip_"] button p,
    div[class*="st-key-mchip_"] button span {
        white-space: normal !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.01em !important;
        line-height: 1.15 !important;
        text-align: center !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }

    div[class*="st-key-mchip_"] button:hover {
        background: #7A0C24 !important;
        color: #FAF5E8 !important;
        border-color: #1A050B !important;
        box-shadow: 3px 3px 0px #C5A059 !important;
    }

    div[class*="st-key-mchip_"] button:hover * {
        color: #FAF5E8 !important;
    }

    /* =========================================================================
       CHARCOAL SLATE GRAPHITE & BALANCING TEAL (PRODUCTS & LIFESTYLE DOMAIN)
       Deep charcoal canvas provides supreme contrast and luxury polish
       ========================================================================= */
    .product-marquis {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        border: 2.5px solid #000000 !important;
        box-shadow: 4px 4px 0px #000000 !important;
        padding: 14px 20px !important;
        margin-bottom: 1.3rem !important;
    }

    .product-domain-badge {
        background: #0D9488 !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 0.68rem !important;
        padding: 4px 10px !important;
        border: 1.5px solid #000000 !important;
        box-shadow: 2px 2px 0px #000000 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        display: inline-block !important;
    }

    .product-card {
        background: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-top: 5px solid #1E293B !important;
        box-shadow: 4px 4px 0px #000000 !important;
        border-radius: 0px !important;
        padding: 1.15rem 1.35rem !important;
        margin-bottom: 0.65rem !important;
        position: relative !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    .product-card:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0px #0D9488 !important;
    }

    /* Product Card: Image + Info two-column poster layout */
    .product-card-body {
        display: flex !important;
        flex-direction: row !important;
        gap: 1.25rem !important;
        align-items: stretch !important;
    }

    .product-img-frame {
        flex-shrink: 0 !important;
        width: 120px !important;
        height: 180px !important;
        aspect-ratio: 2 / 3 !important;
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        border: 2px solid #000000 !important;
        box-shadow: 3px 3px 0px #0D9488 !important;
        overflow: hidden !important;
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
    }

    .product-img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        object-position: center !important;
        display: block !important;
        transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .product-card:hover .product-img {
        transform: scale(1.05) !important;
    }

    .product-img-placeholder {
        font-size: 2.2rem !important;
        line-height: 1 !important;
        color: #94A3B8 !important;
        text-align: center !important;
    }

    .product-info-col {
        flex-grow: 1 !important;
        min-width: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
    }

    @media (max-width: 680px) {
        .product-card-body {
            flex-direction: column !important;
            align-items: center !important;
            text-align: center !important;
        }
        .product-img-frame {
            width: 140px !important;
            height: 210px !important;
            margin-bottom: 0.75rem !important;
        }
        .product-info-col { width: 100% !important; }
    }

    .product-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.15rem !important;
        letter-spacing: -0.02em !important;
        line-height: 1.25 !important;
        margin-top: 0.2rem !important;
    }

    .product-title a {
        color: #000000 !important;
        text-decoration: underline !important;
        text-decoration-color: #1E293B !important;
        text-decoration-thickness: 2px !important;
        transition: color 0.15s ease, text-decoration-color 0.15s ease !important;
    }

    .product-title a:hover {
        color: #0D9488 !important;
        text-decoration-color: #0D9488 !important;
    }

    .tag-product-match {
        float: right;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        background: #1E293B !important;
        padding: 0.25rem 0.7rem !important;
        border-radius: 0px !important;
        border: 1.5px solid #000000 !important;
        box-shadow: 2px 2px 0px #000000 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
    }

    .tag-product-brand {
        display: inline-block !important;
        padding: 0.2rem 0.65rem !important;
        font-size: 0.72rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
        background: #F1F5F9 !important;
        color: #1E293B !important;
        border: 1.5px solid #94A3B8 !important;
        margin-right: 0.35rem !important;
        margin-bottom: 0.3rem !important;
    }

    .tag-product-cat {
        display: inline-block !important;
        padding: 0.2rem 0.6rem !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
        background: #FFFFFF !important;
        color: #475569 !important;
        border: 1.5px solid #CBD5E1 !important;
        margin-right: 0.35rem !important;
        margin-bottom: 0.3rem !important;
    }

    .tag-product-price {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 900 !important;
        color: #0F172A !important;
        letter-spacing: -0.01em !important;
        margin-left: 0.4rem !important;
    }

    .product-reason-box {
        background: #F8FAFC !important;
        border: 1.5px solid #000000 !important;
        border-left: 5px solid #1E293B !important;
        padding: 0.7rem 0.9rem !important;
        margin-top: 0.75rem !important;
        font-size: 0.84rem !important;
        font-weight: 500 !important;
        color: #1E293B !important;
        line-height: 1.45 !important;
    }

    /* Balancing Teal Buy Button */
    .product-buy-btn {
        display: inline-block !important;
        width: 100% !important;
        text-align: center !important;
        background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        padding: 0.45rem 0.75rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        text-decoration: none !important;
        box-shadow: 3px 3px 0px #000000 !important;
        transition: all 0.2s ease !important;
        box-sizing: border-box !important;
    }

    .product-buy-btn:hover {
        background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%) !important;
        color: #FFFFFF !important;
        transform: translate(-1px, -1px) !important;
        box-shadow: 4px 4px 0px #000000 !important;
    }

    /* Product Category Selection Bar (btn_pcat_) — Anti-Truncation & Sharp Styling */
    div[class*="st-key-btn_pcat_"] {
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
    }

    div[class*="st-key-btn_pcat_"] button {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.70rem !important;
        letter-spacing: 0.01em !important;
        text-transform: uppercase !important;
        transition: all 0.15s ease !important;
        padding: 0.35rem 0.2rem !important;
        border-radius: 0px !important;
        min-height: 38px !important;
        height: auto !important;
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: normal !important;
        overflow: hidden !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
    }

    div[class*="st-key-btn_pcat_"] button div[data-testid="stMarkdownContainer"],
    div[class*="st-key-btn_pcat_"] button div,
    div[class*="st-key-btn_pcat_"] button p,
    div[class*="st-key-btn_pcat_"] button span {
        white-space: normal !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        font-size: 0.70rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.01em !important;
        line-height: 1.15 !important;
        text-align: center !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }

    div[class*="st-key-btn_pcat_"] button[kind="primary"] {
        background: #1E293B !important;
        color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        box-shadow: 3.5px 3.5px 0px #000000 !important;
        font-weight: 900 !important;
    }

    div[class*="st-key-btn_pcat_"] button[kind="primary"] *,
    div[class*="st-key-btn_pcat_"] button[kind="primary"] p,
    div[class*="st-key-btn_pcat_"] button[kind="primary"] span {
        color: #FFFFFF !important;
    }

    div[class*="st-key-btn_pcat_"] button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #1E293B !important;
        border: 2px solid #000000 !important;
        box-shadow: 2px 2px 0px #000000 !important;
        font-weight: 700 !important;
    }

    div[class*="st-key-btn_pcat_"] button[kind="secondary"]:hover {
        background: #F1F5F9 !important;
        color: #0D9488 !important;
        border-color: #000000 !important;
        box-shadow: 3px 3px 0px #0D9488 !important;
    }

    /* Product Action Buttons (Save & Like) */
    div[class*="st-key-s_p_"] button,
    div[class*="st-key-l_p_"] button {
        background: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        box-shadow: 2px 2px 0px #000000 !important;
        font-weight: 800 !important;
        font-size: 0.78rem !important;
        padding: 0.35rem 0.5rem !important;
    }

    div[class*="st-key-s_p_"] button:hover,
    div[class*="st-key-l_p_"] button:hover {
        background: #F1F5F9 !important;
        border-color: #000000 !important;
        color: #0D9488 !important;
        box-shadow: 3px 3px 0px #0D9488 !important;
    }

    /* Product Filter Inputs & Sliders */
    div[class*="st-key-sb_product_category"] label,
    div[class*="st-key-sb_product_brand"] label,
    div[class*="st-key-input_product_query"] label,
    div[class*="st-key-p_budget"] label,
    div[class*="st-key-p_s"] label {
        color: #1E293B !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.82rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    div[class*="st-key-input_product_query"] input,
    div[class*="st-key-sb_product_category"] [data-baseweb="select"] > div,
    div[class*="st-key-sb_product_brand"] [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        color: #000000 !important;
        box-sizing: border-box !important;
        max-width: 100% !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }

    div[class*="st-key-input_product_query"] input:focus,
    div[class*="st-key-sb_product_category"] [data-baseweb="select"] > div:focus-within,
    div[class*="st-key-sb_product_brand"] [data-baseweb="select"] > div:focus-within {
        border-color: #0D9488 !important;
        box-shadow: 2.5px 2.5px 0px #0D9488 !important;
    }

    div[class*="st-key-p_budget"] [data-baseweb="slider"] div[role="slider"],
    div[class*="st-key-p_s"] [data-baseweb="slider"] div[role="slider"] {
        background-color: #FFFFFF !important;
        border: 2.5px solid #0D9488 !important;
        box-shadow: 2px 2px 0px #000000 !important;
    }

    div[class*="st-key-p_budget"] [data-testid="stThumbValue"],
    div[class*="st-key-p_s"] [data-testid="stThumbValue"] {
        color: #0D9488 !important;
        font-weight: 900 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Product Reset Button */
    div[class*="st-key-btn_reset_p_filters"] {
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
    }

    div[class*="st-key-btn_reset_p_filters"] button {
        background: #F1F5F9 !important;
        color: #1E293B !important;
        border: 2px solid #000000 !important;
        box-shadow: 2.5px 2.5px 0px #000000 !important;
        font-weight: 800 !important;
        font-size: 0.76rem !important;
        letter-spacing: 0.03em !important;
        text-transform: uppercase !important;
        padding: 0.4rem 0.4rem !important;
        margin-top: 0.5rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
        white-space: normal !important;
        overflow: hidden !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
    }

    div[class*="st-key-btn_reset_p_filters"] button div[data-testid="stMarkdownContainer"],
    div[class*="st-key-btn_reset_p_filters"] button div,
    div[class*="st-key-btn_reset_p_filters"] button p,
    div[class*="st-key-btn_reset_p_filters"] button span {
        white-space: normal !important;
        overflow: hidden !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        line-height: 1.2 !important;
        margin: 0 !important;
    }

    div[class*="st-key-btn_reset_p_filters"] button:hover {
        background: #1E293B !important;
        color: #FFFFFF !important;
        border-color: #000000 !important;
        box-shadow: 3.5px 3.5px 0px #0D9488 !important;
    }

    div[class*="st-key-btn_reset_p_filters"] button:hover * {
        color: #FFFFFF !important;
    }

    /* Quick Feature Chips in Product Filter */
    div[class*="st-key-pchip_"] {
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
    }

    div[class*="st-key-pchip_"] button {
        background: #FFFFFF !important;
        color: #1E293B !important;
        border: 1.5px solid #94A3B8 !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        padding: 0.25rem 0.2rem !important;
        border-radius: 0px !important;
        box-shadow: 2px 2px 0px #000000 !important;
        letter-spacing: 0.01em !important;
        min-height: 32px !important;
        height: auto !important;
        line-height: 1.15 !important;
        white-space: normal !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }

    div[class*="st-key-pchip_"] button div[data-testid="stMarkdownContainer"],
    div[class*="st-key-pchip_"] button div,
    div[class*="st-key-pchip_"] button p,
    div[class*="st-key-pchip_"] button span {
        white-space: normal !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.01em !important;
        line-height: 1.15 !important;
        text-align: center !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }

    div[class*="st-key-pchip_"] button:hover {
        background: #1E293B !important;
        color: #FFFFFF !important;
        border-color: #000000 !important;
        box-shadow: 3px 3px 0px #0D9488 !important;
    }

    div[class*="st-key-pchip_"] button:hover * {
        color: #FFFFFF !important;
    }

    /* =========================================================================
       EMERALD GREEN & SUNBEAM YELLOW (CAREER PATHWAYS & SKILLS DOMAIN)
       Emerald Green stands for growth, momentum, and progress.
       Sunbeam Yellow works like a highlighter pen to spotlight acquired skills,
       the learning path strip, and the Enroll button.
       Brutalist structure with deep green borders and hard shadows.
       ========================================================================= */
    .career-marquis {
        background: linear-gradient(135deg, #064E3B 0%, #022C22 100%) !important;
        border: 2.5px solid #064E3B !important;
        box-shadow: 4px 4px 0px #064E3B !important;
        padding: 14px 20px !important;
        margin-bottom: 1.3rem !important;
    }

    .career-domain-badge {
        background: #FACC15 !important;
        color: #022C22 !important;
        font-weight: 900 !important;
        font-size: 0.68rem !important;
        padding: 4px 10px !important;
        border: 1.5px solid #064E3B !important;
        box-shadow: 2px 2px 0px #064E3B !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        display: inline-block !important;
    }

    .career-card {
        background: #FFFFFF !important;
        border: 2px solid #064E3B !important;
        border-top: 5px solid #059669 !important;
        box-shadow: 4px 4px 0px #064E3B !important;
        border-radius: 0px !important;
        padding: 1.25rem 1.45rem !important;
        margin-bottom: 0.95rem !important;
        position: relative !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    .career-card:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0px #FACC15 !important;
    }

    /* Emerald & Sunbeam Yellow: Career Card Poster Layout */
    .career-card-body {
        display: flex !important;
        flex-direction: row !important;
        gap: 1.25rem !important;
        align-items: stretch !important;
    }

    .career-poster-frame {
        flex-shrink: 0 !important;
        width: 120px !important;
        height: 180px !important;
        aspect-ratio: 2 / 3 !important;
        background: linear-gradient(135deg, #064E3B 0%, #022C22 100%) !important;
        border: 2px solid #064E3B !important;
        box-shadow: 3px 3px 0px #FACC15 !important;
        overflow: hidden !important;
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .career-poster-img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        object-position: center !important;
        display: block !important;
        transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .career-card:hover .career-poster-img {
        transform: scale(1.05) !important;
    }

    .career-info-col {
        flex-grow: 1 !important;
        min-width: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
    }

    @media (max-width: 680px) {
        .career-card-body {
            flex-direction: column !important;
            align-items: center !important;
            text-align: center !important;
        }
        .career-poster-frame {
            width: 140px !important;
            height: 210px !important;
            margin-bottom: 0.75rem !important;
        }
        .career-info-col { width: 100% !important; }
    }

    .tag-career-match {
        background: #064E3B !important;
        color: #FFFFFF !important;
        border: 1.5px solid #022C22 !important;
        font-weight: 900 !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.05em !important;
        padding: 3px 8px !important;
        text-transform: uppercase !important;
        box-shadow: 2px 2px 0px #022C22 !important;
        display: inline-block !important;
    }

    .tag-career-org {
        background: #022C22 !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 0.72rem !important;
        padding: 2px 8px !important;
        border: 1.5px solid #064E3B !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
        display: inline-block !important;
    }

    .tag-career-level {
        background: #ECFDF5 !important;
        color: #064E3B !important;
        font-weight: 800 !important;
        font-size: 0.72rem !important;
        padding: 2px 8px !important;
        border: 1.5px solid #059669 !important;
        text-transform: uppercase !important;
        display: inline-block !important;
    }

    .tag-career-duration {
        background: #F4FBF7 !important;
        color: #065F46 !important;
        font-weight: 800 !important;
        font-size: 0.72rem !important;
        padding: 2px 8px !important;
        border: 1.5px solid #059669 !important;
        display: inline-block !important;
    }

    /* Sunbeam Yellow Highlighter Skill Badge (Marks acquired / matching skills) */
    .skill-highlighter {
        background: #FDE047 !important;
        color: #022C22 !important;
        border: 1.5px solid #064E3B !important;
        font-weight: 900 !important;
        font-size: 0.72rem !important;
        padding: 3px 8px !important;
        display: inline-block !important;
        margin-right: 5px !important;
        margin-bottom: 5px !important;
        box-shadow: 2px 2px 0px #064E3B !important;
        letter-spacing: 0.02em !important;
    }

    .skill-curriculum {
        background: #ECFDF5 !important;
        color: #065F46 !important;
        border: 1.5px solid #059669 !important;
        font-weight: 700 !important;
        font-size: 0.72rem !important;
        padding: 2px 7px !important;
        display: inline-block !important;
        margin-right: 5px !important;
        margin-bottom: 5px !important;
    }

    /* Learning Path Strip marked in Sunbeam Yellow */
    .career-path-strip {
        background: #FEF9C3 !important;
        border: 1.5px solid #064E3B !important;
        box-shadow: 2.5px 2.5px 0px #064E3B !important;
        padding: 6px 12px !important;
        margin-top: 0.75rem !important;
        margin-bottom: 0.6rem !important;
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        gap: 6px !important;
    }

    .career-path-label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 900 !important;
        font-size: 0.68rem !important;
        color: #022C22 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        background: #FACC15 !important;
        padding: 2px 6px !important;
        border: 1px solid #064E3B !important;
    }

    .career-path-step {
        font-size: 0.72rem !important;
        font-weight: 800 !important;
        color: #022C22 !important;
    }

    .career-path-arrow {
        color: #059669 !important;
        font-weight: 900 !important;
        font-size: 0.75rem !important;
    }

    .career-reason-box {
        background: #F0FDF4 !important;
        border: 1.5px solid #064E3B !important;
        border-left: 5px solid #059669 !important;
        padding: 8px 12px !important;
        font-size: 0.78rem !important;
        color: #064E3B !important;
        line-height: 1.5 !important;
        font-weight: 600 !important;
    }

    /* Sunbeam Yellow Highlighter Enroll Button */
    .career-enroll-btn {
        display: inline-block !important;
        width: 100% !important;
        text-align: center !important;
        background: linear-gradient(135deg, #FDE047 0%, #FACC15 100%) !important;
        color: #022C22 !important;
        border: 2px solid #064E3B !important;
        padding: 0.45rem 0.75rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        text-decoration: none !important;
        box-shadow: 3.5px 3.5px 0px #064E3B !important;
        transition: all 0.2s ease !important;
        box-sizing: border-box !important;
    }

    .career-enroll-btn:hover {
        background: #064E3B !important;
        color: #FACC15 !important;
        transform: translate(-1px, -1px) !important;
        box-shadow: 4.5px 4.5px 0px #022C22 !important;
    }

    /* Domain Selector Bar for Careers (btn_cdom_) */
    div[class*="st-key-btn_cdom_"] {
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
    }

    div[class*="st-key-btn_cdom_"] button {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.70rem !important;
        letter-spacing: 0.01em !important;
        text-transform: uppercase !important;
        transition: all 0.15s ease !important;
        padding: 0.35rem 0.2rem !important;
        border-radius: 0px !important;
        min-height: 38px !important;
        height: auto !important;
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: normal !important;
        overflow: hidden !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
    }

    div[class*="st-key-btn_cdom_"] button div[data-testid="stMarkdownContainer"],
    div[class*="st-key-btn_cdom_"] button div,
    div[class*="st-key-btn_cdom_"] button p,
    div[class*="st-key-btn_cdom_"] button span {
        white-space: normal !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        font-size: 0.70rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.01em !important;
        line-height: 1.15 !important;
        text-align: center !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }

    div[class*="st-key-btn_cdom_"] button[kind="primary"] {
        background: #064E3B !important;
        color: #FFFFFF !important;
        border: 2px solid #064E3B !important;
        box-shadow: 3.5px 3.5px 0px #FACC15 !important;
        font-weight: 900 !important;
    }

    div[class*="st-key-btn_cdom_"] button[kind="primary"] *,
    div[class*="st-key-btn_cdom_"] button[kind="primary"] p,
    div[class*="st-key-btn_cdom_"] button[kind="primary"] span {
        color: #FFFFFF !important;
    }

    div[class*="st-key-btn_cdom_"] button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #064E3B !important;
        border: 2px solid #064E3B !important;
        box-shadow: 2px 2px 0px #064E3B !important;
        font-weight: 700 !important;
    }

    div[class*="st-key-btn_cdom_"] button[kind="secondary"]:hover {
        background: #ECFDF5 !important;
        color: #047857 !important;
        border-color: #064E3B !important;
        box-shadow: 3px 3px 0px #FACC15 !important;
    }

    /* In-Demand Skill Chips in Career Filter (cchip_) */
    div[class*="st-key-cchip_"] {
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
    }

    div[class*="st-key-cchip_"] button {
        background: #FFFFFF !important;
        color: #064E3B !important;
        border: 1.5px solid #059669 !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        padding: 0.25rem 0.2rem !important;
        border-radius: 0px !important;
        box-shadow: 2px 2px 0px #064E3B !important;
        letter-spacing: 0.01em !important;
        min-height: 32px !important;
        height: auto !important;
        line-height: 1.15 !important;
        white-space: normal !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }

    div[class*="st-key-cchip_"] button div[data-testid="stMarkdownContainer"],
    div[class*="st-key-cchip_"] button div,
    div[class*="st-key-cchip_"] button p,
    div[class*="st-key-cchip_"] button span {
        white-space: normal !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.01em !important;
        line-height: 1.15 !important;
        text-align: center !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin: 0 !important;
    }

    div[class*="st-key-cchip_"] button:hover {
        background: #064E3B !important;
        color: #FACC15 !important;
        border-color: #064E3B !important;
        box-shadow: 3px 3px 0px #FACC15 !important;
    }

    div[class*="st-key-cchip_"] button:hover * {
        color: #FACC15 !important;
    }

    /* Career Domain Widgets and Sliders */
    div[class*="st-key-sb_course_domain"] label,
    div[class*="st-key-sb_course_level"] label,
    div[class*="st-key-input_course_query"] label,
    div[class*="st-key-c_s"] label,
    div[class*="st-key-c_alpha"] label {
        color: #064E3B !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.82rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    div[class*="st-key-input_course_query"] input,
    div[class*="st-key-sb_course_domain"] [data-baseweb="select"] > div,
    div[class*="st-key-sb_course_level"] [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 2px solid #064E3B !important;
        border-radius: 0px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        color: #022C22 !important;
        box-sizing: border-box !important;
        max-width: 100% !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }

    div[class*="st-key-input_course_query"] input:focus,
    div[class*="st-key-sb_course_domain"] [data-baseweb="select"] > div:focus-within,
    div[class*="st-key-sb_course_level"] [data-baseweb="select"] > div:focus-within {
        border-color: #059669 !important;
        box-shadow: 2.5px 2.5px 0px #FACC15 !important;
    }

    div[class*="st-key-c_s"] [data-baseweb="slider"] div[role="slider"],
    div[class*="st-key-c_alpha"] [data-baseweb="slider"] div[role="slider"] {
        background-color: #FFFFFF !important;
        border: 2.5px solid #059669 !important;
        box-shadow: 2px 2px 0px #064E3B !important;
    }

    div[class*="st-key-c_s"] [data-testid="stThumbValue"],
    div[class*="st-key-c_alpha"] [data-testid="stThumbValue"] {
        color: #059669 !important;
        font-weight: 900 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Career Action Buttons (Save & Like) */
    div[class*="st-key-s_c_"] button,
    div[class*="st-key-l_c_"] button {
        background: #FFFFFF !important;
        color: #064E3B !important;
        border: 2px solid #064E3B !important;
        box-shadow: 2px 2px 0px #064E3B !important;
        font-weight: 800 !important;
        font-size: 0.78rem !important;
        padding: 0.35rem 0.5rem !important;
    }

    div[class*="st-key-s_c_"] button:hover,
    div[class*="st-key-l_c_"] button:hover {
        background: #ECFDF5 !important;
        border-color: #064E3B !important;
        color: #059669 !important;
        box-shadow: 3px 3px 0px #FACC15 !important;
    }

    /* Course Reset Button */
    div[class*="st-key-btn_reset_c_filters"] {
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
    }

    div[class*="st-key-btn_reset_c_filters"] button {
        background: #F1F5F9 !important;
        color: #064E3B !important;
        border: 2px solid #064E3B !important;
        box-shadow: 2.5px 2.5px 0px #064E3B !important;
        font-weight: 800 !important;
        font-size: 0.76rem !important;
        letter-spacing: 0.03em !important;
        text-transform: uppercase !important;
        padding: 0.4rem 0.4rem !important;
        margin-top: 0.5rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
        white-space: normal !important;
        overflow: hidden !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
    }

    div[class*="st-key-btn_reset_c_filters"] button div[data-testid="stMarkdownContainer"],
    div[class*="st-key-btn_reset_c_filters"] button div,
    div[class*="st-key-btn_reset_c_filters"] button p,
    div[class*="st-key-btn_reset_c_filters"] button span {
        white-space: normal !important;
        overflow: hidden !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        line-height: 1.2 !important;
        margin: 0 !important;
    }

    div[class*="st-key-btn_reset_c_filters"] button:hover {
        background: #064E3B !important;
        color: #FACC15 !important;
        border-color: #064E3B !important;
        box-shadow: 3.5px 3.5px 0px #FACC15 !important;
    }

    div[class*="st-key-btn_reset_c_filters"] button:hover * {
        color: #FACC15 !important;
    }

    /* =========================================================================
       OVERVIEW DOMAIN EXPLORATION BUTTONS (PALETTE HARMONIZED)
       ========================================================================= */
    /* Movies & Cinema Explore Buttons (Velvet Crimson & Antique Brass) */
    div[class*="st-key-btn_ov_cinema"] button {
        background: linear-gradient(135deg, #7A0C24 0%, #4D0717 100%) !important;
        color: #FAF5E8 !important;
        border: 2px solid #C5A059 !important;
        box-shadow: 3.5px 3.5px 0px #1A050B !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease !important;
    }

    div[class*="st-key-btn_ov_cinema"] button * {
        color: #FAF5E8 !important;
    }

    div[class*="st-key-btn_ov_cinema"] button:hover {
        background: #C5A059 !important;
        color: #1A050B !important;
        border-color: #1A050B !important;
        box-shadow: 4.5px 4.5px 0px #7A0C24 !important;
        transform: translate(-1px, -1px) !important;
    }

    div[class*="st-key-btn_ov_cinema"] button:hover * {
        color: #1A050B !important;
    }

    /* Products & Lifestyle Explore Buttons (Charcoal Slate & Balancing Teal) */
    div[class*="st-key-btn_ov_brands"] button,
    div[class*="st-key-btn_ov_watches"] button,
    div[class*="st-key-btn_ov_fragrance"] button {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important;
        color: #F8FAFC !important;
        border: 2px solid #0D9488 !important;
        box-shadow: 3.5px 3.5px 0px #0F172A !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease !important;
    }

    div[class*="st-key-btn_ov_brands"] button *,
    div[class*="st-key-btn_ov_watches"] button *,
    div[class*="st-key-btn_ov_fragrance"] button * {
        color: #F8FAFC !important;
    }

    div[class*="st-key-btn_ov_brands"] button:hover,
    div[class*="st-key-btn_ov_watches"] button:hover,
    div[class*="st-key-btn_ov_fragrance"] button:hover {
        background: #0D9488 !important;
        color: #FFFFFF !important;
        border-color: #0F172A !important;
        box-shadow: 4.5px 4.5px 0px #F97316 !important;
        transform: translate(-1px, -1px) !important;
    }

    div[class*="st-key-btn_ov_brands"] button:hover *,
    div[class*="st-key-btn_ov_watches"] button:hover *,
    div[class*="st-key-btn_ov_fragrance"] button:hover * {
        color: #FFFFFF !important;
    }

    /* Career Pathways Explore Buttons (Emerald Green & Sunbeam Yellow) */
    div[class*="st-key-btn_ov_courses"] button {
        background: linear-gradient(135deg, #064E3B 0%, #022C22 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #064E3B !important;
        box-shadow: 3.5px 3.5px 0px #FACC15 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 900 !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease !important;
    }

    div[class*="st-key-btn_ov_courses"] button * {
        color: #FFFFFF !important;
    }

    div[class*="st-key-btn_ov_courses"] button:hover {
        background: #FACC15 !important;
        color: #022C22 !important;
        border-color: #064E3B !important;
        box-shadow: 4.5px 4.5px 0px #064E3B !important;
        transform: translate(-1px, -1px) !important;
    }

    div[class*="st-key-btn_ov_courses"] button:hover * {
        color: #022C22 !important;
    }

    /* =========================================================================
       HIGH-CONTRAST STARK NAVIGATION TAB BAR (REACT-ARIA & BASEWEB COMPATIBLE)
       ========================================================================= */
    div[data-testid="stTabs"],
    .stTabs {
        width: 100% !important;
        margin-top: 1.2rem !important;
        margin-bottom: 1.5rem !important;
    }

    div[data-testid="stTabs"] [role="tablist"],
    div[data-testid="stTabs"] .react-aria-TabList,
    .stTabs [role="tablist"],
    .stTabs .react-aria-TabList,
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.75rem !important;
        background: #FFFFFF !important;
        padding: 0.75rem 1rem !important;
        border-radius: 0px !important;
        border: 2.5px solid #000000 !important;
        box-shadow: 5px 5px 0px #000000 !important;
        align-items: center !important;
        position: relative !important;
        margin-bottom: 1.6rem !important;
    }

    /* Hide standard react-aria and baseweb underline indicators */
    div[data-testid="stTabs"] .react-aria-SelectionIndicator,
    .react-aria-SelectionIndicator,
    div[data-testid="stTabs"] [role="tablist"]::after,
    .stTabs [data-baseweb="tab-highlight-container"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
        height: 0px !important;
        visibility: hidden !important;
    }

    /* ALL Tabs: Base styling */
    div[data-testid="stTab"],
    button[data-testid="stTab"],
    div[role="tab"],
    button[role="tab"],
    .react-aria-Tab,
    .stTabs [data-baseweb="tab"] {
        border-radius: 0px !important;
        padding: 0.65rem 1.25rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        height: auto !important;
        min-height: 44px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        opacity: 1 !important;
        visibility: visible !important;
        outline: none !important;
    }

    /* UNSELECTED / DEFAULT TABS:
       Light background (#F4F4F6), crisp solid black border (2.5px solid #000000),
       2px offset brutalist shadow, and FORCED SOLID BOLD BLACK TEXT (#000000) */
    div[data-testid="stTab"]:not([data-selected]),
    button[data-testid="stTab"]:not([data-selected]),
    div[data-testid="stTab"][aria-selected="false"],
    button[data-testid="stTab"][aria-selected="false"],
    div[role="tab"]:not([aria-selected="true"]),
    button[role="tab"]:not([aria-selected="true"]),
    .react-aria-Tab:not([data-selected]),
    .stTabs [data-baseweb="tab"]:not([aria-selected="true"]) {
        background-color: #F4F4F6 !important;
        border: 2.5px solid #000000 !important;
        box-shadow: 2px 2px 0px #000000 !important;
        color: #000000 !important;
    }

    /* Force all text in default unselected tabs to be BOLDER SOLID BLACK (#000000) */
    div[data-testid="stTab"]:not([data-selected]) *,
    button[data-testid="stTab"]:not([data-selected]) *,
    div[data-testid="stTab"][aria-selected="false"] *,
    button[data-testid="stTab"][aria-selected="false"] *,
    div[role="tab"]:not([aria-selected="true"]) *,
    button[role="tab"]:not([aria-selected="true"]) *,
    .react-aria-Tab:not([data-selected]) *,
    .stTabs [data-baseweb="tab"]:not([aria-selected="true"]) *,
    div[data-testid="stTab"] p,
    div[data-testid="stTab"] span,
    button[data-testid="stTab"] p,
    button[data-testid="stTab"] span,
    div[role="tab"] p,
    div[role="tab"] span,
    .react-aria-Tab p,
    .react-aria-Tab span {
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 900 !important;
        font-size: 0.88rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        -webkit-text-stroke: 0.3px #000000 !important;
        opacity: 1 !important;
    }

    /* Tab Hover State */
    div[data-testid="stTab"]:hover,
    button[data-testid="stTab"]:hover,
    div[role="tab"]:hover,
    button[role="tab"]:hover,
    .react-aria-Tab:hover,
    .react-aria-Tab[data-hovered],
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #E2E8F0 !important;
        border: 2.5px solid #000000 !important;
        transform: translateY(-2px) !important;
        box-shadow: 4px 4px 0px #000000 !important;
    }

    div[data-testid="stTab"]:hover *,
    button[data-testid="stTab"]:hover *,
    div[role="tab"]:hover *,
    button[role="tab"]:hover *,
    .react-aria-Tab:hover *,
    .stTabs [data-baseweb="tab"]:hover * {
        color: #000000 !important;
        font-weight: 900 !important;
        letter-spacing: 0.06em !important;
    }

    /* SELECTED ACTIVE TAB: Highlighted Badge with 3.5px Solid Black Border, 5px Shadow & Ultra-Bold Black Text */
    div[data-testid="stTab"][data-selected],
    div[data-testid="stTab"][aria-selected="true"],
    button[data-testid="stTab"][data-selected],
    button[data-testid="stTab"][aria-selected="true"],
    div[role="tab"][aria-selected="true"],
    button[role="tab"][aria-selected="true"],
    .react-aria-Tab[data-selected],
    .stTabs [aria-selected="true"],
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #FFFFFF !important;
        border: 3.5px solid #000000 !important;
        transform: translateY(-3px) !important;
        box-shadow: 5px 5px 0px #000000 !important;
        opacity: 1 !important;
    }

    div[data-testid="stTab"][data-selected] *,
    div[data-testid="stTab"][aria-selected="true"] *,
    button[data-testid="stTab"][data-selected] *,
    button[data-testid="stTab"][aria-selected="true"] *,
    div[role="tab"][aria-selected="true"] *,
    button[role="tab"][aria-selected="true"] *,
    .react-aria-Tab[data-selected] *,
    .stTabs [aria-selected="true"] *,
    .stTabs [data-baseweb="tab"][aria-selected="true"] * {
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 900 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        -webkit-text-stroke: 0.4px #000000 !important;
    }

    /* Streamlit Buttons Global Styling */
    .stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        box-shadow: 3px 3px 0px #000000 !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        box-shadow: 4px 4px 0px #000000 !important;
    }

    .stButton > button:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 1px 1px 0px #000000 !important;
    }

    /* Direct Action Buy Button Styling */
    .buy-btn {
        display: inline-block !important;
        width: 100% !important;
        text-align: center !important;
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        padding: 0.35rem 0.6rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        text-decoration: none !important;
        box-shadow: 3px 3px 0px #000000 !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }

    .buy-btn:hover {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        box-shadow: 4px 4px 0px #000000 !important;
    }

    .buy-btn:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 1px 1px 0px #000000 !important;
    }

    /* =========================================================================
       FILTER SECTION SUBTITLES & WIDGET LABELS (FORCED DEFAULT BOLD BLACK #000000)
       ========================================================================= */
    label[data-testid="stWidgetLabel"],
    label[data-testid="stWidgetLabel"] *,
    label[data-testid="stWidgetLabel"] p,
    label[data-testid="stWidgetLabel"] span,
    .stSelectbox label,
    .stSelectbox label *,
    .stSelectbox label p,
    .stSelectbox label span,
    .stSlider label,
    .stSlider label *,
    .stSlider label p,
    .stSlider label span,
    .stTextInput label,
    .stTextInput label *,
    .stTextInput label p,
    .stTextInput label span,
    .stMultiSelect label,
    .stMultiSelect label *,
    .stMultiSelect label p,
    .stMultiSelect label span,
    div[data-testid="stSlider"] [data-testid="stWidgetLabel"] p,
    div[data-testid="stSlider"] [data-testid="stWidgetLabel"] span {
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.82rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
        opacity: 1 !important;
        visibility: visible !important;
        white-space: normal !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        line-height: 1.25 !important;
    }

    /* Slider values & numbers - contained strictly */
    div[data-testid="stSlider"] [data-testid="stThumbValue"],
    div[data-testid="stSlider"] div[role="slider"] {
        color: #000000 !important;
        font-weight: 800 !important;
    }

    div[data-testid="stSlider"] [data-testid="stTickBarMin"],
    div[data-testid="stSlider"] [data-testid="stTickBarMax"] {
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.01em !important;
    }

    /* Form Inputs, Selectboxes, and MultiSelects - Single Outer Border Only */
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div,
    div[data-baseweb="select"] > div,
    div[data-testid="stTextInput"] input,
    .stTextInput input {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        opacity: 1 !important;
        box-sizing: border-box !important;
        max-width: 100% !important;
    }

    /* Prevent accidental double borders on wrapper divs */
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stSelectbox"] [data-baseweb="select"],
    div[data-testid="stMultiSelect"] > div,
    div[data-testid="stMultiSelect"] [data-baseweb="select"] {
        border: none !important;
        background: transparent !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stSelectbox"] [role="combobox"],
    div[data-testid="stMultiSelect"] [role="combobox"] {
        border: none !important;
        background: transparent !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        max-width: 100% !important;
    }

    /* Selected value text inside Selectbox: contain text and prevent spilling outside box */
    div[data-testid="stSelectbox"] [data-baseweb="select"] [aria-selected="true"],
    div[data-testid="stSelectbox"] [data-baseweb="select"] span,
    div[data-testid="stSelectbox"] [data-baseweb="select"] p,
    div[data-testid="stSelectbox"] [data-baseweb="select"] div {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        color: #000000 !important;
        font-weight: 700 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Multiselect Tags: strictly contained inside selectbox without leaking */
    div[data-testid="stMultiSelect"] div[data-baseweb="tag"],
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
        max-width: calc(100% - 6px) !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    div[data-testid="stMultiSelect"] div[data-baseweb="tag"] span {
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        max-width: calc(100% - 16px) !important;
    }

    /* Selectbox dropdown virtual popover options */
    div[data-testid="stSelectboxVirtualDropdown"] li,
    div[data-testid="stSelectboxVirtualDropdown"] span,
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] span {
        color: #000000 !important;
        font-weight: 700 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    .stTextInput input:focus {
        box-shadow: 2px 2px 0px #000000 !important;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 2.5px solid #000000 !important;
        box-shadow: 4px 4px 0px #000000 !important;
        border-radius: 0px !important;
        padding: 0.85rem !important;
    }

    div[data-testid="stMetricLabel"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        color: #000000 !important;
    }

    div[data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        color: #000000 !important;
    }

    /* High-Contrast Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FDFBF7 !important;
        border-right: 3px solid #000000 !important;
        box-shadow: 5px 0px 0px #000000 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] p,
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] div,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] label {
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Preserve Material Symbols font for collapse arrow & icons (fixes keyboard_double_arrow text bug) */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapsedControl"] button,
    button[data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarHeader"] button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        cursor: pointer !important;
    }

    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapsedControl"] span,
    [data-testid="stSidebarHeader"] span,
    span[data-testid="stIconMaterial"],
    .material-symbols-rounded {
        font-family: 'Material Symbols Rounded' !important;
        font-weight: 400 !important;
        font-style: normal !important;
        font-feature-settings: 'liga' !important;
        -webkit-font-feature-settings: 'liga' !important;
        font-size: 1.45rem !important;
        color: #000000 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        line-height: 1 !important;
    }

    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover {
        background-color: #E2E8F0 !important;
        border-radius: 4px !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] strong,
    section[data-testid="stSidebar"] label {
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.03em !important;
    }

    section[data-testid="stSidebar"] .stCaption p,
    section[data-testid="stSidebar"] .stCaption span {
        color: #333333 !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] svg,
    section[data-testid="stSidebar"] button svg path {
        fill: #000000 !important;
        stroke: #000000 !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        font-weight: 800 !important;
        padding: 0.2rem 0.5rem !important;
        min-height: auto !important;
    }

    section[data-testid="stSidebar"] .stButton > button * {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover * {
        color: #000000 !important;
    }

    /* Sidebar Saved Items: Red Delete Cross Button */
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button {
        background-color: #FFF1F2 !important;
        border: 2px solid #EF4444 !important;
        box-shadow: 2px 2px 0px #DC2626 !important;
        transition: all 0.15s ease-in-out !important;
    }

    section[data-testid="stSidebar"] div[class*="st-key-del_"] button *,
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button p,
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button span {
        color: #DC2626 !important;
        font-weight: 900 !important;
        font-size: 1.15rem !important;
        line-height: 1 !important;
        -webkit-text-stroke: 0.6px #DC2626 !important;
    }

    section[data-testid="stSidebar"] div[class*="st-key-del_"] button:hover {
        background-color: #DC2626 !important;
        border-color: #991B1B !important;
        box-shadow: 2px 2px 0px #7F1D1D !important;
        transform: translate(-1px, -1px) !important;
    }

    section[data-testid="stSidebar"] div[class*="st-key-del_"] button:hover *,
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button:hover p,
    section[data-testid="stSidebar"] div[class*="st-key-del_"] button:hover span {
        color: #FFFFFF !important;
        -webkit-text-stroke: 0.6px #FFFFFF !important;
    }

    section[data-testid="stSidebar"] div[class*="st-key-del_"] button svg path {
        fill: #DC2626 !important;
        stroke: #DC2626 !important;
    }

    section[data-testid="stSidebar"] div[class*="st-key-del_"] button:hover svg path {
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }

    /* =========================================================================
       LOGIN GATEWAY MINIMAL POSTER CARDS (CLEAR ARTWORK SHOWCASE)
       ========================================================================= */
    .login-feature-card {
        background: #FFFFFF !important;
        border: 2.5px solid #000000 !important;
        box-shadow: 4px 4px 0px #000000 !important;
        margin-bottom: 1.15rem !important;
        overflow: hidden !important;
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .login-feature-card:hover {
        transform: translate(-3px, -3px) !important;
        box-shadow: 7px 7px 0px #000000 !important;
    }

    .login-card-img-wrapper {
        position: relative !important;
        width: 100% !important;
        height: 340px !important;
        overflow: hidden !important;
        border-bottom: 2.5px solid #000000 !important;
        background: #000000 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .login-card-img {
        width: 100% !important;
        height: 100% !important;
        object-fit: contain !important;
        object-position: center center !important;
        display: block !important;
        filter: contrast(1.04) saturate(1.04) !important;
        transition: transform 0.35s ease !important;
    }

    .login-feature-card:hover .login-card-img {
        transform: scale(1.04) !important;
    }

    .login-card-footer {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding: 0.65rem 0.85rem !important;
        background: #FFFFFF !important;
    }

    .login-card-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 800 !important;
        color: #000000 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        line-height: 1 !important;
    }

    .login-card-badge {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.62rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.08em !important;
        background: #000000 !important;
        color: #FFFFFF !important;
        padding: 3px 7px !important;
        border: 1.5px solid #000000 !important;
        text-transform: uppercase !important;
        white-space: nowrap !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Database
db.init_db()

# Safe Comprehensive Filter Reset Callback for All 3 Domains
def reset_all_domain_filters():
    """
    Reset all filters, categories, search queries, sliders, and focused items
    across all 3 domains (Cinema, Products, Careers) to default 'All' state.
    Ensures no categories are pre-selected without explicit user input.
    """
    # Portal Tab & Overview Hub
    st.session_state["portal_tabs"] = "🏠 Overview"
    st.session_state["overview_domain_selectbox"] = "🏠 Overview Hub — (Select a Domain below)"
    st.session_state.focused_saved_item = None

    # Domain 1: 🎬 Movies & Cinema
    st.session_state["selected_movie_industry"] = "All"
    st.session_state["sb_movie_industry"] = "All"
    st.session_state["m_genres"] = []
    st.session_state["input_movie_query"] = ""
    st.session_state["m_s"] = 5
    st.session_state["m_alpha"] = 0.6

    # Domain 2: 🛍️ Products & Lifestyle
    st.session_state["selected_product_category"] = "All"
    st.session_state["sb_product_category"] = "All"
    st.session_state["sb_product_brand"] = "All"
    st.session_state["input_product_query"] = ""
    st.session_state["p_budget"] = 14995
    st.session_state["p_s"] = 5

    # Domain 3: 🎓 Career Pathways & Skills
    st.session_state["selected_course_domain"] = "All"
    st.session_state["sb_course_domain"] = "All"
    st.session_state["sb_course_level"] = "All"
    st.session_state["input_course_query"] = ""
    st.session_state["c_s"] = 5

# Session State Initialization
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "auth_error" not in st.session_state:
    st.session_state.auth_error = None
if "auth_success" not in st.session_state:
    st.session_state.auth_success = None

# Ensure all 3 domains default to clean "All" state on fresh session initialization
if "portal_tabs" not in st.session_state:
    reset_all_domain_filters()

# Defensive defaults for all individual domain state keys
if "selected_movie_industry" not in st.session_state:
    st.session_state["selected_movie_industry"] = "All"
if "sb_movie_industry" not in st.session_state:
    st.session_state["sb_movie_industry"] = "All"
if "m_genres" not in st.session_state:
    st.session_state["m_genres"] = []
if "input_movie_query" not in st.session_state:
    st.session_state["input_movie_query"] = ""
if "m_s" not in st.session_state:
    st.session_state["m_s"] = 5
if "m_alpha" not in st.session_state:
    st.session_state["m_alpha"] = 0.6

if "selected_product_category" not in st.session_state:
    st.session_state["selected_product_category"] = "All"
if "sb_product_category" not in st.session_state:
    st.session_state["sb_product_category"] = "All"
if "sb_product_brand" not in st.session_state:
    st.session_state["sb_product_brand"] = "All"
if "input_product_query" not in st.session_state:
    st.session_state["input_product_query"] = ""
if "p_budget" not in st.session_state:
    st.session_state["p_budget"] = 14995
if "p_s" not in st.session_state:
    st.session_state["p_s"] = 5

if "selected_course_domain" not in st.session_state:
    st.session_state["selected_course_domain"] = "All"
if "sb_course_domain" not in st.session_state:
    st.session_state["sb_course_domain"] = "All"
if "sb_course_level" not in st.session_state:
    st.session_state["sb_course_level"] = "All"
if "input_course_query" not in st.session_state:
    st.session_state["input_course_query"] = ""
if "c_s" not in st.session_state:
    st.session_state["c_s"] = 5

if "overview_domain_selectbox" not in st.session_state:
    st.session_state["overview_domain_selectbox"] = "🏠 Overview Hub — (Select a Domain below)"
if "focused_saved_item" not in st.session_state:
    st.session_state.focused_saved_item = None

TAB_OPTIONS = [
    "🏠 Overview",
    "🎬 Movies & Cinema",
    "🛍️ Products",
    "🎓 Courses & Skills",
    "📊 Model Benchmarks"
]

CATEGORY_TAB_MAP = {
    "Movie": "🎬 Movies & Cinema",
    "movie": "🎬 Movies & Cinema",
    "Movies": "🎬 Movies & Cinema",
    "Product": "🛍️ Products",
    "product": "🛍️ Products",
    "Products": "🛍️ Products",
    "Course": "🎓 Courses & Skills",
    "course": "🎓 Courses & Skills",
    "Courses": "🎓 Courses & Skills",
}

# Model Loader (Auto-invalidates cache when clean CSV files or model codes are updated)
@st.cache_resource
def get_engines_v4(movies_mtime, products_mtime, courses_mtime, models_mtime):
    import importlib
    import models.movie_rec
    import models.product_rec
    import models.course_rec
    importlib.reload(models.movie_rec)
    importlib.reload(models.product_rec)
    importlib.reload(models.course_rec)
    m = models.movie_rec.MovieRecommender()
    p = models.product_rec.ProductRecommender()
    c = models.course_rec.CourseRecommender()
    return m, p, c

@st.cache_data
def get_login_card_images():
    img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "login_cards")
    cards = {}
    for name in ["movies_cinema.jpg", "lifestyle_brands.jpg", "career_skills.jpg", "entertainment_ai.jpg"]:
        p = os.path.join(img_dir, name)
        if os.path.exists(p):
            with open(p, "rb") as f:
                cards[name] = base64.b64encode(f.read()).decode("utf-8")
        else:
            cards[name] = ""
    return cards

# =========================================================================
# STATE 1: STARK HIGH-CONTRAST AUTHENTICATION GATEWAY
# =========================================================================
if st.session_state.user_id is None:
    card_imgs = get_login_card_images()

    # High-contrast site branding header on login page
    st.markdown("""
        <div style="text-align: center; margin-top: 0.2rem; margin-bottom: 1.4rem;">
            <div style="display: inline-flex; align-items: center; gap: 10px; background: #000000; color: #FFFFFF; padding: 8px 24px; border: 2.5px solid #000000; box-shadow: 4px 4px 0px #000000;">
                <span style="font-size: 1.15rem;">⚡</span>
                <span style="font-weight: 900; font-size: 1.25rem; letter-spacing: 0.12em; color: #FFFFFF;">RECOM.ai</span>
                <span style="background: #FFFFFF; color: #000000; font-size: 0.65rem; font-weight: 800; padding: 2px 7px; letter-spacing: 0.08em; margin-left: 4px;">PORTAL</span>
            </div>
            <div style="font-size: 0.74rem; font-weight: 800; letter-spacing: 0.15em; color: #333333; margin-top: 0.5rem; text-transform: uppercase;">
                CROSS-DOMAIN MULTI-PERSPECTIVE INTELLIGENCE PLATFORM
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 1.4, 1], gap="medium")

    with col_left:
        # Card 1: Movies & Cinema
        st.markdown(f"""
            <div class="login-feature-card">
                <div class="login-card-img-wrapper">
                    <img src="data:image/jpeg;base64,{card_imgs['movies_cinema.jpg']}" alt="Movies & Cinema" class="login-card-img" />
                </div>
                <div class="login-card-footer">
                    <span class="login-card-title">🎬 MOVIES & CINEMA</span>
                    <span class="login-card-badge">DOMAIN 01</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Card 2: Lifestyle & Products
        st.markdown(f"""
            <div class="login-feature-card">
                <div class="login-card-img-wrapper">
                    <img src="data:image/jpeg;base64,{card_imgs['lifestyle_brands.jpg']}" alt="Products" class="login-card-img" />
                </div>
                <div class="login-card-footer">
                    <span class="login-card-title">🛍️ PRODUCTS</span>
                    <span class="login-card-badge">DOMAIN 02</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_center:
        auth_action = habit_auth(
            key="habit_tracker_auth",
            error=st.session_state.auth_error,
            success=st.session_state.auth_success
        )

    with col_right:
        # Card 3: Career & Skills
        st.markdown(f"""
            <div class="login-feature-card">
                <div class="login-card-img-wrapper">
                    <img src="data:image/jpeg;base64,{card_imgs['career_skills.jpg']}" alt="Career & Skills" class="login-card-img" />
                </div>
                <div class="login-card-footer">
                    <span class="login-card-title">🎓 CAREER & SKILLS</span>
                    <span class="login-card-badge">DOMAIN 03</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Card 4: AI & Entertainment
        st.markdown(f"""
            <div class="login-feature-card">
                <div class="login-card-img-wrapper">
                    <img src="data:image/jpeg;base64,{card_imgs['entertainment_ai.jpg']}" alt="AI & Entertainment" class="login-card-img" />
                </div>
                <div class="login-card-footer">
                    <span class="login-card-title">⚡ AI & ENTERTAINMENT</span>
                    <span class="login-card-badge">CORE AI</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    if auth_action:
        action_type = auth_action.get("action")
        username = auth_action.get("username", "").strip()
        password = auth_action.get("password", "")

        if action_type == "login":
            uid, msg = db.login_user(username, password)
            if uid:
                st.session_state.user_id = uid
                st.session_state.username = username
                st.session_state.auth_error = None
                st.session_state.auth_success = None
                reset_all_domain_filters()
                st.rerun()
            else:
                st.session_state.auth_error = msg
                st.session_state.auth_success = None
                st.rerun()

        elif action_type == "signup":
            uid, msg = db.register_user(username, password)
            if uid:
                st.session_state.user_id = uid
                st.session_state.username = username
                st.session_state.auth_error = None
                st.session_state.auth_success = f"Account created! Welcome, {username}!"
                reset_all_domain_filters()
                st.rerun()
            else:
                st.session_state.auth_error = msg
                st.session_state.auth_success = None
                st.rerun()

        elif action_type == "demo":
            demo_uid, _ = db.login_user("demo_user", "demo123")
            if not demo_uid:
                demo_uid, _ = db.register_user("demo_user", "demo123")
            st.session_state.user_id = demo_uid
            st.session_state.username = "demo_user"
            st.session_state.auth_error = None
            st.session_state.auth_success = None
            reset_all_domain_filters()
            st.rerun()

    st.stop()  # Stop execution here if not logged in

# =========================================================================
# STATE 2: AUTHENTICATED PORTAL & LANDING EXPERIENCE
# =========================================================================
m_csv = "data/cleaned/movies_clean.csv"
p_csv = "data/cleaned/products_clean.csv"
c_csv = "data/cleaned/courses_clean.csv"
m_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "movie_rec.py")
p_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "product_rec.py")
c_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "course_rec.py")
models_mtime = (
    (os.path.getmtime(m_py) if os.path.exists(m_py) else 0) +
    (os.path.getmtime(p_py) if os.path.exists(p_py) else 0) +
    (os.path.getmtime(c_py) if os.path.exists(c_py) else 0)
)
movie_engine, product_engine, course_engine = get_engines_v4(
    os.path.getmtime(m_csv) if os.path.exists(m_csv) else 0,
    os.path.getmtime(p_csv) if os.path.exists(p_csv) else 0,
    os.path.getmtime(c_csv) if os.path.exists(c_csv) else 0,
    models_mtime,
)

def resolve_product_image(product_id: int, name: str, brand: str, category: str, price_inr: int = 1999, rating: float = 4.5) -> tuple:
    """Bulletproof resolver that invokes product_engine.get_image, ProductRecommender.get_image, or fallback poster."""
    if hasattr(product_engine, "get_image"):
        try:
            return product_engine.get_image(product_id, name, brand, category, price_inr, rating)
        except Exception:
            pass
    try:
        import models.product_rec
        return models.product_rec.get_product_poster(product_id, name, brand, category, price_inr, rating)
    except Exception:
        return ("", "")

# Safe Tab Switching Callback (Runs before widgets are instantiated on rerun)
def set_active_tab(tab_name, industry=None, category=None, domain=None):
    st.session_state["portal_tabs"] = tab_name
    st.session_state["overview_domain_selectbox"] = "🏠 Overview Hub — (Select a Domain below)"
    if tab_name == "🏠 Overview":
        st.session_state.focused_saved_item = None
    if industry:
        st.session_state["selected_movie_industry"] = industry
        st.session_state["sb_movie_industry"] = industry
    if category:
        st.session_state["selected_product_category"] = category
        st.session_state["sb_product_category"] = category
    if domain:
        st.session_state["selected_course_domain"] = domain
        st.session_state["sb_course_domain"] = domain

# Top Header Navigation Bar (Placed at the very top edge with vibrant color palette)
header_col1, header_col2 = st.columns([2.5, 1.5], gap="small")
with header_col1:
    st.markdown('''
        <div class="recom-banner-box" title="⚡ Recom.AI — Click to jump to Overview Hub">
            <span style="font-weight:900; font-size:1.35rem; letter-spacing:0.08em; background:linear-gradient(90deg, #FF2E93 0%, #FF8A00 50%, #FFD600 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-family:'Space Grotesk';">⚡ RECOM.AI</span>
            <span style="background:linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%); color:#FFFFFF; font-size:0.65rem; font-weight:800; padding:3px 9px; letter-spacing:0.06em; text-transform:uppercase; border:1.5px solid #000000; box-shadow:2px 2px 0px #000000;">PORTAL</span>
            <span style="color:#94A3B8; font-size:0.75rem; font-weight:800; text-transform:uppercase; letter-spacing:0.05em;">• MULTI-DOMAIN INTELLIGENCE ENGINE</span>
        </div>
    ''', unsafe_allow_html=True)
    if st.button("⚡ RECOM.AI (Go to Overview)", key="top_banner_home_btn", help="⚡ Click to return to Overview page", on_click=set_active_tab, args=("🏠 Overview",)):
        st.session_state["portal_tabs"] = "🏠 Overview"
        st.session_state["overview_domain_selectbox"] = "🏠 Overview Hub — (Select a Domain below)"
        st.session_state.focused_saved_item = None
        st.rerun()

with header_col2:
    u_col1, u_col2 = st.columns([1.3, 1], gap="small")
    with u_col1:
        st.markdown(f'''
            <div style="background:linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%); color:#FFFFFF; border:2.5px solid #000000; box-shadow:3.5px 3.5px 0px #000000; padding:9.5px 12px; text-align:center; font-weight:800; font-size:0.8rem; font-family:'Space Grotesk'; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:1.2rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                👤 @{st.session_state.username}
            </div>
        ''', unsafe_allow_html=True)
    with u_col2:
        if st.button("LOG OUT", key="top_logout_btn", width="stretch"):
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.auth_error = None
            st.session_state.auth_success = None
            reset_all_domain_filters()
            st.rerun()

# Explicit Spacing Gap Between Top Header Banner and Tab Navigation Bar
st.markdown('<div style="margin-bottom: 1.8rem;"></div>', unsafe_allow_html=True)

# Sidebar: Saved Bookmarks Drawer
with st.sidebar:
    st.markdown("<h3 style='font-family:\"Space Grotesk\"; text-transform:uppercase; font-size:1.15rem; font-weight:800; margin-bottom:0.3rem;'>🔖 Saved Items</h3>", unsafe_allow_html=True)
    st.caption("Click any saved item to jump directly to its navigation tab.")

    user_bookmarks = db.get_bookmarks(st.session_state.user_id)
    if user_bookmarks:
        for idx, b in enumerate(user_bookmarks):
            b_id = b.get('id', idx)
            cat = b['category']
            item_id = b['item_id']
            title = b['title']
            extra = b.get("extra_info") or {}
            url = extra.get("url")
            target_tab = CATEGORY_TAB_MAP.get(cat, "🏠 Overview")
            icon = "🎬" if cat.lower() in ["movie", "movies"] else "🛍️" if cat.lower() in ["product", "products"] else "🎓"

            st.markdown(f"""
            <div style="background:#FFFFFF; border:2px solid #000000; box-shadow:3px 3px 0px #000000; padding:8px 10px; margin-bottom:5px;">
                <div style="font-size:0.65rem; font-weight:800; color:#555555; text-transform:uppercase; letter-spacing:0.05em;">{icon} {cat}</div>
                <div style="font-size:0.85rem; font-weight:800; color:#000000; margin:3px 0 2px 0; line-height:1.25;">{title}</div>
            </div>
            """, unsafe_allow_html=True)

            nav_col, del_col = st.columns([3.5, 1.2])
            with nav_col:
                if st.button(f"Go to {cat} ➔", key=f"nav_bm_{b_id}_{item_id}_{idx}", width="stretch"):
                    st.session_state["portal_tabs"] = target_tab
                    st.session_state.focused_saved_item = {
                        "category": cat,
                        "id": item_id,
                        "title": title,
                        "url": url
                    }
                    if cat.lower() in ["movie", "movies"]:
                        st.session_state["input_movie_query"] = title
                    elif cat.lower() in ["product", "products"]:
                        st.session_state["input_product_query"] = title
                    elif cat.lower() in ["course", "courses"]:
                        st.session_state["input_course_query"] = title
                    st.rerun()
            with del_col:
                if st.button("✕", key=f"del_bm_{b_id}_{item_id}_{idx}", help="Remove from saved items", width="stretch"):
                    db.remove_bookmark(st.session_state.user_id, cat, item_id)
                    if st.session_state.get("focused_saved_item") and st.session_state.focused_saved_item.get("id") == item_id:
                        st.session_state.focused_saved_item = None
                    st.rerun()

            if url:
                st.markdown(f'<div style="text-align:right; margin-bottom:8px; font-size:0.72rem;"><a href="{url}" target="_blank" style="color:#000000; font-weight:700; text-decoration:underline;">External Link ↗</a></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="margin-bottom:8px;"></div>', unsafe_allow_html=True)
    else:
        st.caption("No saved items yet. Click 🔖 on any card to save it here.")

# (Note: set_active_tab callback defined above for top header navigation)

# Dropdown Domain Select Callback (Runs before widgets are instantiated on rerun)
def on_overview_domain_select():
    selected = st.session_state.get("overview_domain_selectbox")
    if selected and selected != "🏠 Overview Hub — (Select a Domain below)":
        st.session_state["portal_tabs"] = selected
        st.session_state["overview_domain_selectbox"] = "🏠 Overview Hub — (Select a Domain below)"

# Safe Callbacks for Movies & Cinema Domain (Run before widgets instantiate)
def clear_movie_focus():
    st.session_state.focused_saved_item = None
    st.session_state["input_movie_query"] = ""

def set_cinema_industry(ind):
    st.session_state["selected_movie_industry"] = ind
    st.session_state["sb_movie_industry"] = ind
    st.session_state["input_movie_query"] = ""

def on_cinema_industry_change():
    st.session_state["selected_movie_industry"] = st.session_state.get("sb_movie_industry", "All")

def set_movie_query_theme(theme_text):
    st.session_state["input_movie_query"] = theme_text

def reset_cinema_filters():
    st.session_state["sb_movie_industry"] = "All"
    st.session_state["selected_movie_industry"] = "All"
    st.session_state["m_genres"] = []
    st.session_state["input_movie_query"] = ""
    st.session_state["m_s"] = 5
    st.session_state["m_alpha"] = 0.6

# Safe Callbacks for Products & Lifestyle Domain (Run before widgets instantiate)
def clear_product_focus():
    st.session_state.focused_saved_item = None
    st.session_state["input_product_query"] = ""

def set_product_category(cat):
    st.session_state["selected_product_category"] = cat
    st.session_state["sb_product_category"] = cat
    st.session_state["input_product_query"] = ""

def on_product_category_change():
    st.session_state["selected_product_category"] = st.session_state.get("sb_product_category", "All")

def set_product_query_feature(feat_text):
    st.session_state["input_product_query"] = feat_text

def reset_product_filters(max_p):
    st.session_state["sb_product_category"] = "All"
    st.session_state["selected_product_category"] = "All"
    st.session_state["sb_product_brand"] = "All"
    st.session_state["input_product_query"] = ""
    st.session_state["p_budget"] = max_p
    st.session_state["p_s"] = 5

# Safe Callbacks for Career Pathways & Skills Domain (Run before widgets instantiate)
def clear_course_focus():
    st.session_state.focused_saved_item = None
    st.session_state["input_course_query"] = ""

def set_course_domain(dom):
    st.session_state["selected_course_domain"] = dom
    st.session_state["sb_course_domain"] = dom
    st.session_state["input_course_query"] = ""

def on_course_domain_change():
    st.session_state["selected_course_domain"] = st.session_state.get("sb_course_domain", "All")

def set_course_query_skill(skill_text):
    st.session_state["input_course_query"] = skill_text

def reset_course_filters():
    st.session_state["sb_course_domain"] = "All"
    st.session_state["selected_course_domain"] = "All"
    st.session_state["sb_course_level"] = "All"
    st.session_state["input_course_query"] = ""
    st.session_state["c_s"] = 5

# Always ensure overview selectbox is reset to the default Overview option when navigating away
if st.session_state.get("portal_tabs") != "🏠 Overview":
    st.session_state["overview_domain_selectbox"] = "🏠 Overview Hub — (Select a Domain below)"

# Conditionally hide top navigation bar when on Overview page
if st.session_state.get("portal_tabs", "🏠 Overview") == "🏠 Overview":
    st.markdown("""
    <style>
        div[data-testid="stTabs"] [role="tablist"],
        .stTabs [role="tablist"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Main Minimalist Tabs
tabs = st.tabs(TAB_OPTIONS, key="portal_tabs", on_change="rerun")

# -------------------------------------------------------------------------
# TAB 0: OVERVIEW
# -------------------------------------------------------------------------
with tabs[0]:
    user_display = (st.session_state.get("username") or "Explorer").strip().upper()
    st.markdown('<div style="display:flex;height:8px;margin-bottom:1rem"><span style="flex:1;background:#B3123B"></span><span style="flex:1;background:#FF8A00"></span><span style="flex:1;background:#059669"></span></div>', unsafe_allow_html=True)
    st.markdown(f'''
        <h2 style='font-family:"Space Grotesk"; text-transform:uppercase; font-size:1.85rem; font-weight:800; margin-bottom:0.2rem; letter-spacing:0.02em;'>
            WELCOME BACK, <span style="background:linear-gradient(90deg, #B3123B 0%, #FF8A00 50%, #059669 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">{user_display}</span> 👋
        </h2>
    ''', unsafe_allow_html=True)
    st.markdown("<p style='color:#555555; font-size:0.9rem; font-weight:600; text-transform:uppercase; margin-bottom:1.2rem;'>Select a domain below or use the navigation tabs to generate personalized recommendations.</p>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SELECT DOMAIN DROPDOWN SELECTOR INSIDE OVERVIEW
    # ---------------------------------------------------------
    st.markdown("<div style='font-family:\"Space Grotesk\"; text-transform:uppercase; font-size:0.85rem; font-weight:800; color:#000000; letter-spacing:0.08em; margin-bottom:0.4rem;'>📌 SELECT A DOMAIN TO EXPLORE</div>", unsafe_allow_html=True)
    
    st.selectbox(
        "Select Domain",
        options=["🏠 Overview Hub — (Select a Domain below)"] + TAB_OPTIONS[1:],
        index=0,
        key="overview_domain_selectbox",
        on_change=on_overview_domain_select,
        label_visibility="collapsed"
    )

    st.markdown("<div style='margin-bottom:1.6rem;'></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # VERTICAL DOMAIN CARDS (SCROLL DOWN SEQUENCE)
    # ---------------------------------------------------------
    st.markdown("<div style='font-family:\"Space Grotesk\"; text-transform:uppercase; font-size:0.85rem; font-weight:800; color:#555555; letter-spacing:0.08em; margin-bottom:0.8rem;'>EXPLORE RECOMMENDATION DOMAINS</div>", unsafe_allow_html=True)

    # Vertical Card 1: Cinema Hub (Domain 01: Velvet Crimson #7A0C24 & Antique Brass #C5A059)
    overview_cinema_img = get_login_card_images().get("movies_cinema.jpg", "")
    st.markdown(f"""
    <div class="cinema-card" style="padding:1.25rem 1.45rem !important; margin-bottom:0.8rem;">
        <div class="cinema-card-body">
            <div class="cinema-poster-frame">
                <img src="data:image/jpeg;base64,{overview_cinema_img}" 
                     class="cinema-poster-img" 
                     alt="Cinema & Theatre Hub" />
            </div>
            <div class="cinema-info-col">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <span style="font-size:0.75rem; color:#7A0C24; text-transform:uppercase; font-weight:800; letter-spacing:0.06em;">🎬 DOMAIN 01</span>
                        <span class="cinema-domain-badge">🏛️ CINEMA & THEATRE</span>
                    </div>
                    <div style="font-size:1.35rem; font-weight:900; color:#7A0C24; text-transform:uppercase; font-family:'Space Grotesk'; margin:0.15rem 0 0.35rem 0;">Cinema & Theatre Hub</div>
                    <p style="font-size:0.88rem; color:#333333; line-height:1.55; margin-bottom:0.6rem;">
                        Explore Bollywood, Tollywood, Hollywood, and Nepali cinema films with multi-genre filters, content-based TF-IDF plot search, and IMDb score weighting.
                    </p>
                    <div style="margin-bottom:0.2rem; display:flex; flex-wrap:wrap; gap:5px;">
                        <span class="tag-cinema-industry">Bollywood</span>
                        <span class="tag-cinema-industry">Tollywood</span>
                        <span class="tag-cinema-industry">Hollywood</span>
                        <span class="tag-cinema-industry">Nepali Cinema</span>
                        <span class="cinema-brass-pill">TF-IDF Plot Match</span>
                        <span class="cinema-brass-pill">23 Curated Genres</span>
                        <span class="cinema-brass-pill">IMDb Weighted</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    c_btn1, c_btn2 = st.columns([1, 1])
    with c_btn1:
        st.button("Explore All Movies ➔", key="btn_ov_cinema", width="stretch", on_click=set_active_tab, args=("🎬 Movies & Cinema", "All"))
    with c_btn2:
        st.button("🏔️ Explore Nepali Cinema ➔", key="btn_ov_cinema_nepali", width="stretch", on_click=set_active_tab, args=("🎬 Movies & Cinema", "Nepali Cinema"))

    st.markdown("<div style='margin-bottom:1.6rem;'></div>", unsafe_allow_html=True)

    # Vertical Card 2: Products E-Commerce & Lifestyle (Domain 02: Slate #0F172A & Teal #0D9488)
    overview_product_img = get_login_card_images().get("lifestyle_brands.jpg", "")
    st.markdown(f"""
    <div class="product-card" style="padding:1.25rem 1.45rem !important; margin-bottom:0.8rem; border-top:5px solid #0D9488 !important; border-color:#0F172A !important;">
        <div class="product-card-body">
            <div class="product-img-frame">
                <img src="data:image/jpeg;base64,{overview_product_img}" 
                     class="product-img" 
                     alt="Products & Lifestyle Store" />
            </div>
            <div class="product-info-col">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <span style="font-size:0.75rem; color:#0D9488; text-transform:uppercase; font-weight:800; letter-spacing:0.06em;">🛍️ DOMAIN 02</span>
                        <span class="product-domain-badge">PRODUCTS & LIFESTYLE</span>
                    </div>
                    <div style="font-size:1.35rem; font-weight:900; color:#0F172A; text-transform:uppercase; font-family:'Space Grotesk'; margin:0.15rem 0 0.35rem 0;">Products & Lifestyle Store</div>
                    <p style="font-size:0.88rem; color:#333333; line-height:1.55; margin-bottom:0.6rem;">
                        Discover curated audio, iconic watches (Titan, HMT, Fastrack, Sonata), luxury fragrances (Titan Skinn, Bella Vita, Forest Essentials, Phool), wearables, and electronics with real-time INR (₹) budget filters.
                    </p>
                    <div style="margin-bottom:0.2rem; display:flex; flex-wrap:wrap; gap:5px;">
                        <span class="tag-product-price">₹ INR Pricing</span>
                        <span class="tag-product-cat">⌚ Watches</span>
                        <span class="tag-product-cat">🌸 Fragrance</span>
                        <span class="tag-product-brand">Titan</span>
                        <span class="tag-product-brand">HMT</span>
                        <span class="tag-product-brand">Titan Skinn</span>
                        <span class="tag-product-brand">boAt</span>
                        <span class="tag-product-brand">Noise</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    b_col1, b_col2, b_col3 = st.columns([1, 1, 1])
    with b_col1:
        st.button("Explore All Products ➔", key="btn_ov_brands", width="stretch", on_click=set_active_tab, args=("🛍️ Products", None, "All"))
    with b_col2:
        st.button("⌚ Explore Watches ➔", key="btn_ov_watches", width="stretch", on_click=set_active_tab, args=("🛍️ Products", None, "Watches"))
    with b_col3:
        st.button("🌸 Explore Fragrances ➔", key="btn_ov_fragrance", width="stretch", on_click=set_active_tab, args=("🛍️ Products", None, "Fragrance"))

    st.markdown("<div style='margin-bottom:1.6rem;'></div>", unsafe_allow_html=True)

    # Vertical Card 3: Career & Skills (Domain 03: Emerald Green #064E3B & Sunbeam Yellow #FACC15)
    overview_career_img = get_login_card_images().get("career_skills.jpg", "")
    st.markdown(f"""
    <div class="career-card" style="padding:1.25rem 1.45rem !important; margin-bottom:0.8rem;">
        <div class="career-card-body">
            <div class="career-poster-frame">
                <img src="data:image/jpeg;base64,{overview_career_img}" 
                     class="career-poster-img" 
                     alt="Career & Skill Pathways" />
            </div>
            <div class="career-info-col">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <span style="font-size:0.75rem; color:#064E3B; text-transform:uppercase; font-weight:800; letter-spacing:0.06em;">🎓 DOMAIN 03</span>
                        <span class="career-domain-badge">CAREER EDUCATION</span>
                    </div>
                    <div style="font-size:1.35rem; font-weight:900; color:#064E3B; text-transform:uppercase; font-family:'Space Grotesk'; margin:0.15rem 0 0.35rem 0;">Career & Skill Pathways</div>
                    <p style="font-size:0.88rem; color:#333333; line-height:1.55; margin-bottom:0.6rem;">
                        Match job goals to industry certifications and university pathways from Stanford, Google, Meta, and Harvard in AI, Data Science, and Software Engineering.
                    </p>
                    <div style="margin-bottom:0.2rem; display:flex; flex-wrap:wrap; gap:5px;">
                        <span class="skill-highlighter">Stanford</span>
                        <span class="skill-highlighter">Google</span>
                        <span class="skill-highlighter">Meta</span>
                        <span class="skill-curriculum">Machine Learning</span>
                        <span class="skill-curriculum">Full Stack</span>
                        <span class="skill-curriculum">Skill Match</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Explore Pathways ➔", key="btn_ov_courses", width="stretch", on_click=set_active_tab, args=("🎓 Courses & Skills", None, None, "All"))

    st.markdown("<hr style='border:none; border-top:2.5px solid #000000; margin:2.2rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-family:\"Space Grotesk\"; text-transform:uppercase; font-size:1.2rem; font-weight:700; color:#000000; margin-bottom:0.3rem;'>Curated Recommendations</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555555; font-size:0.85rem; font-weight:600; text-transform:uppercase; margin-bottom:1.2rem;'>Top-rated picks across all domains, stacked for quick exploration.</p>", unsafe_allow_html=True)

    # Vertical Recommendation 1: RRR (Velvet Crimson & Antique Brass Theatre Card)
    rrr_p, rrr_fb = movie_engine.get_poster(91001, "RRR (2022)", "Tollywood", 4.6)
    st.markdown(f"""
    <div class="cinema-card" style="margin-bottom:1.2rem;">
        <div class="cinema-card-body">
            <div class="cinema-poster-frame">
                <img src="{rrr_p}" 
                     class="cinema-poster-img" 
                     loading="lazy" 
                     referrerpolicy="no-referrer" 
                     onerror="this.onerror=null; this.src='{rrr_fb}';" 
                     alt="RRR (2022)" />
            </div>
            <div class="cinema-info-col">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px;">
                        <div>
                            <div style="font-size:0.72rem; color:#7A0C24; text-transform:uppercase; font-weight:800; letter-spacing:0.05em; margin-bottom:0.2rem;">🎬 CINEMA PICK</div>
                            <div class="item-title" style="margin-bottom:0.25rem;">
                                <a href="https://www.google.com/search?q=RRR+2022+movie+watch+online" target="_blank" style="color:#7A0C24; text-decoration:none; font-family:'Space Grotesk'; font-weight:800; font-size:1.12rem;">RRR (2022) <span style="font-size:0.85rem; color:#C5A059;">↗</span></a>
                            </div>
                        </div>
                        <span class="tag-cinema-match">98.5% MATCH</span>
                    </div>
                    <div style="margin-top:0.35rem; display:flex; flex-wrap:wrap; align-items:center; gap:6px;">
                        <span class="tag-cinema-industry">Tollywood</span>
                        <span class="tag-cinema-genre">Action</span>
                        <span class="tag-cinema-genre">Drama</span>
                        <span style="font-size:0.85rem; color:#C5A059; margin-left:0.3rem; font-weight:900;">★ 4.6</span>
                        <span style="font-size:0.75rem; color:#666666;">(Top Community Narrative)</span>
                    </div>
                    <p style="color:#333333; font-size:0.84rem; margin:0.4rem 0 0 0; line-height:1.45;">High community rating & iconic Telugu period action narrative with groundbreaking visual spectacle.</p>
                </div>
                <div class="cinema-reason-box" style="margin-top:0.6rem;">High community rating & iconic Telugu period action narrative with groundbreaking visual spectacle.</div>
                <div style="margin-top:0.8rem; max-width:280px;"><a href="https://www.google.com/search?q=RRR+2022+movie+watch+online" target="_blank" class="cinema-buy-btn">🎬 Watch Online ↗</a></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Vertical Recommendation 1B: Nepali Cinema (Loot) (Velvet Crimson & Antique Brass Theatre Card)
    loot_p, loot_fb = movie_engine.get_poster(200001, "Loot (2012)", "Nepali Cinema", 4.8)
    st.markdown(f"""
    <div class="cinema-card" style="margin-bottom:1.2rem;">
        <div class="cinema-card-body">
            <div class="cinema-poster-frame">
                <img src="{loot_p}" 
                     class="cinema-poster-img" 
                     loading="lazy" 
                     referrerpolicy="no-referrer" 
                     onerror="this.onerror=null; this.src='{loot_fb}';" 
                     alt="Loot (2012)" />
            </div>
            <div class="cinema-info-col">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px;">
                        <div>
                            <div style="font-size:0.72rem; color:#7A0C24; text-transform:uppercase; font-weight:800; letter-spacing:0.05em; margin-bottom:0.2rem;">🏔️ NEPALI CINEMA PICK</div>
                            <div class="item-title" style="margin-bottom:0.25rem;">
                                <a href="https://www.google.com/search?q=Loot+2012+nepali+movie+watch+online" target="_blank" style="color:#7A0C24; text-decoration:none; font-family:'Space Grotesk'; font-weight:800; font-size:1.12rem;">Loot (2012) <span style="font-size:0.85rem; color:#C5A059;">↗</span></a>
                            </div>
                        </div>
                        <span class="tag-cinema-match">98.2% MATCH</span>
                    </div>
                    <div style="margin-top:0.35rem; display:flex; flex-wrap:wrap; align-items:center; gap:6px;">
                        <span class="tag-cinema-industry">Nepali Cinema</span>
                        <span class="tag-cinema-genre">Action</span>
                        <span class="tag-cinema-genre">Crime</span>
                        <span class="tag-cinema-genre">Thriller</span>
                        <span style="font-size:0.85rem; color:#C5A059; margin-left:0.3rem; font-weight:900;">★ 4.8</span>
                        <span style="font-size:0.75rem; color:#666666;">(Revolution of Modern Nepali Cinema)</span>
                    </div>
                    <p style="color:#333333; font-size:0.84rem; margin:0.4rem 0 0 0; line-height:1.45;">Cult classic Kathmandu underworld bank heist thriller that redefined contemporary Nepali cinema with iconic performances and realistic pacing.</p>
                </div>
                <div class="cinema-reason-box" style="margin-top:0.6rem;">Cult classic Kathmandu underworld bank heist thriller that redefined contemporary Nepali cinema with iconic performances and realistic pacing.</div>
                <div style="margin-top:0.8rem; max-width:280px;"><a href="https://www.google.com/search?q=Loot+2012+nepali+movie+watch+online" target="_blank" class="cinema-buy-btn">🎬 Watch Online ↗</a></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Vertical Recommendation 2: boAt Nirvana Ion
    p102_img, p102_fb = resolve_product_image(102, "boAt Nirvana Ion ANC Headphones", "boAt", "Audio", 2499, 4.8)
    st.markdown(f"""
    <div class="product-card" style="margin-bottom:1.2rem;">
        <div class="product-card-body">
            <a href="https://www.boat-lifestyle.com/products/nirvana-ion" target="_blank" class="product-img-frame" title="boAt Nirvana Ion ANC">
                <img src="{p102_img}" class="product-img" onerror="this.onerror=null; this.src='{p102_fb}';" alt="boAt Nirvana Ion ANC" />
            </a>
            <div class="product-info-col">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px;">
                        <div>
                            <div style="font-size:0.72rem; color:#4B5563; text-transform:uppercase; font-weight:800; letter-spacing:0.05em; margin-bottom:0.2rem;">🎧 AUDIO PICK</div>
                            <div class="product-title" style="margin-bottom:0.25rem;"><a href="https://www.boat-lifestyle.com/products/nirvana-ion" target="_blank">boAt Nirvana Ion ANC ↗</a></div>
                        </div>
                        <span class="tag-product-match">96.8% MATCH</span>
                    </div>
                    <div style="margin:0.35rem 0 0.45rem 0; display:flex; flex-wrap:wrap; align-items:center; gap:6px;">
                        <span class="tag-product-brand">boAt</span>
                        <span class="tag-product-cat">Audio</span>
                        <span class="tag-product-price">₹2,499</span>
                        <span style="font-size:0.85rem; color:#0D9488; font-weight:800; margin-left:0.2rem;">★ 4.8</span>
                    </div>
                    <p style="color:#333333; font-size:0.84rem; margin:0.4rem 0 0 0; line-height:1.45;">Top active noise cancellation wireless earbuds with 120-hour playback and dual EQ modes from boAt.</p>
                </div>
                <div style="margin-top:0.8rem; max-width:280px;"><a href="https://www.boat-lifestyle.com/products/nirvana-ion" target="_blank" class="product-buy-btn">🛒 Buy Now ↗</a></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Vertical Recommendation 2B: Titan Watch Pick
    p122_img, p122_fb = resolve_product_image(122, "Titan Octane Mechanical Automatic Watch", "Titan", "Watches", 12495, 4.8)
    st.markdown(f"""
    <div class="product-card" style="margin-bottom:1.2rem;">
        <div class="product-card-body">
            <a href="https://www.titan.co.in/shop/watches" target="_blank" class="product-img-frame" title="Titan Octane Automatic">
                <img src="{p122_img}" class="product-img" onerror="this.onerror=null; this.src='{p122_fb}';" alt="Titan Octane Automatic" />
            </a>
            <div class="product-info-col">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px;">
                        <div>
                            <div style="font-size:0.72rem; color:#4B5563; text-transform:uppercase; font-weight:800; letter-spacing:0.05em; margin-bottom:0.2rem;">⌚ WATCH PICK</div>
                            <div class="product-title" style="margin-bottom:0.25rem;"><a href="https://www.titan.co.in/shop/watches" target="_blank">Titan Octane Mechanical Automatic Watch ↗</a></div>
                        </div>
                        <span class="tag-product-match">97.4% MATCH</span>
                    </div>
                    <div style="margin:0.35rem 0 0.45rem 0; display:flex; flex-wrap:wrap; align-items:center; gap:6px;">
                        <span class="tag-product-brand">Titan</span>
                        <span class="tag-product-cat">Watches</span>
                        <span class="tag-product-price">₹12,495</span>
                        <span style="font-size:0.85rem; color:#0D9488; font-weight:800; margin-left:0.2rem;">★ 4.8</span>
                    </div>
                    <p style="color:#333333; font-size:0.84rem; margin:0.4rem 0 0 0; line-height:1.45;">Exquisite automatic mechanical watch by Tata Titan featuring skeleton dial displaying inner mechanical gear movements.</p>
                </div>
                <div style="margin-top:0.8rem; max-width:280px;"><a href="https://www.titan.co.in/shop/watches" target="_blank" class="product-buy-btn">🛒 Buy Now ↗</a></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Vertical Recommendation 2C: Fragrance Pick
    p132_img, p132_fb = resolve_product_image(132, "Titan Skinn Raw Eau De Parfum (100ml)", "Titan Skinn", "Fragrance", 2495, 4.9)
    st.markdown(f"""
    <div class="product-card" style="margin-bottom:1.2rem;">
        <div class="product-card-body">
            <a href="https://www.skinn.in/product/skinn-raw-perfume-for-men-100ml" target="_blank" class="product-img-frame" title="Titan Skinn Raw EDP">
                <img src="{p132_img}" class="product-img" onerror="this.onerror=null; this.src='{p132_fb}';" alt="Titan Skinn Raw EDP" />
            </a>
            <div class="product-info-col">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px;">
                        <div>
                            <div style="font-size:0.72rem; color:#4B5563; text-transform:uppercase; font-weight:800; letter-spacing:0.05em; margin-bottom:0.2rem;">🌸 FRAGRANCE PICK</div>
                            <div class="product-title" style="margin-bottom:0.25rem;"><a href="https://www.skinn.in/product/skinn-raw-perfume-for-men-100ml" target="_blank">Titan Skinn Raw Eau De Parfum (100ml) ↗</a></div>
                        </div>
                        <span class="tag-product-match">96.5% MATCH</span>
                    </div>
                    <div style="margin:0.35rem 0 0.45rem 0; display:flex; flex-wrap:wrap; align-items:center; gap:6px;">
                        <span class="tag-product-brand">Titan Skinn</span>
                        <span class="tag-product-cat">Fragrance</span>
                        <span class="tag-product-price">₹2,495</span>
                        <span style="font-size:0.85rem; color:#0D9488; font-weight:800; margin-left:0.2rem;">★ 4.9</span>
                    </div>
                    <p style="color:#333333; font-size:0.84rem; margin:0.4rem 0 0 0; line-height:1.45;">French-crafted luxury Eau De Parfum for India blending fresh citrus bergamot, watery watermelon, and Indonesian patchouli.</p>
                </div>
                <div style="margin-top:0.8rem; max-width:280px;"><a href="https://www.skinn.in/product/skinn-raw-perfume-for-men-100ml" target="_blank" class="product-buy-btn">🛒 Buy Now ↗</a></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Vertical Recommendation 3: ML Specialization (Emerald Green & Sunbeam Yellow 2-column layout)
    st.markdown(f"""
    <div class="career-card" style="margin-bottom:1.2rem;">
        <div class="career-card-body">
            <div class="career-poster-frame">
                <img src="data:image/jpeg;base64,{overview_career_img}" 
                     class="career-poster-img" 
                     alt="Machine Learning Specialization" />
            </div>
            <div class="career-info-col">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px;">
                        <div>
                            <div style="font-size:0.72rem; color:#064E3B; text-transform:uppercase; font-weight:800; letter-spacing:0.05em; margin-bottom:0.2rem;">🎓 CAREER PICK</div>
                            <div class="item-title" style="margin-bottom:0.25rem;">
                                <a href="https://coursera.org/specializations/machine-learning-introduction" target="_blank" style="color:#064E3B; text-decoration:none; font-family:'Space Grotesk'; font-weight:800; font-size:1.12rem;">Machine Learning Specialization <span style="font-size:0.85rem; color:#064E3B;">↗</span></a>
                            </div>
                        </div>
                        <span class="tag-career-match" style="margin:0;">99.1% MATCH</span>
                    </div>
                    <div style="margin:0.35rem 0 0.45rem 0; display:flex; flex-wrap:wrap; align-items:center; gap:6px;">
                        <span class="tag-career-org">Stanford</span>
                        <span class="tag-career-level">Beginner</span>
                        <span class="tag-career-duration">⏱️ 60 Hours</span>
                        <span style="font-size:0.85rem; color:#064E3B; margin-left:0.3rem; font-weight:800;">★ 4.9</span>
                    </div>
                    <div style="margin-top:0.35rem; margin-bottom:0.5rem; display:flex; flex-wrap:wrap; gap:5px;">
                        <span class="skill-highlighter">Machine Learning</span>
                        <span class="skill-highlighter">Python</span>
                        <span class="skill-curriculum">Supervised Learning</span>
                        <span class="skill-curriculum">Neural Networks</span>
                    </div>
                    <div class="career-path-strip">
                        <span class="career-path-label">⚡ LEARNING PATHWAY</span>
                        <span class="career-path-step">01 Foundation</span>
                        <span class="career-path-arrow">➔</span>
                        <span class="career-path-step">02 Applied Labs</span>
                        <span class="career-path-arrow">➔</span>
                        <span class="career-path-step" style="background:#FDE047; color:#022C22; padding:1px 6px; border:1px solid #064E3B; font-weight:900;">03 Capstone & Credential</span>
                    </div>
                    <p style="color:#333333; font-size:0.84rem; margin:0.4rem 0 0 0; line-height:1.45;">Fundamental ML certification taught by Andrew Ng covering supervised learning, neural networks, and decision trees.</p>
                </div>
                <div class="career-reason-box" style="margin-top:0.6rem;">Fundamental ML certification taught by Andrew Ng covering supervised learning, neural networks, and decision trees.</div>
                <div style="margin-top:0.8rem; max-width:280px;"><a href="https://coursera.org/specializations/machine-learning-introduction" target="_blank" class="career-enroll-btn">🎓 Enroll Now ↗</a></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------------
# TAB 1: MOVIES & CINEMA (VELVET & BRASS THEATRE THEME)
# -------------------------------------------------------------------------
with tabs[1]:
    # Velvet and Brass Theatre Marquis Header
    st.markdown("""
    <div class="cinema-marquis">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.5rem;">🎭</span>
                <div>
                    <div style="font-family:'Space Grotesk'; font-size:1.35rem; font-weight:900; color:#FAF5E8; text-transform:uppercase; letter-spacing:0.06em; line-height:1.15;">
                        THEATRE & CINEMA REPERTOIRE
                    </div>
                    <div style="font-size:0.75rem; font-weight:800; color:#C5A059; text-transform:uppercase; letter-spacing:0.1em; margin-top:3px;">
                        VELVET ARCHIVE • CURATED WORLD & SOUTH ASIAN CINEMA
                    </div>
                </div>
            </div>
            <div>
                <span style="background:#C5A059; color:#1A050B; font-weight:900; font-size:0.68rem; padding:4px 10px; border:1.5px solid #1A050B; box-shadow:2px 2px 0px #1A050B; text-transform:uppercase; letter-spacing:0.06em;">
                    🏛️ DOMAIN 01: CINEMA
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    focused = st.session_state.get("focused_saved_item")
    if focused and focused.get("category", "").lower() in ["movie", "movies"]:
        f_top1, f_top2 = st.columns([4, 1.2])
        with f_top1:
            f_poster = ""
            f_fallback = ""
            f_id = focused.get("id")
            if f_id:
                try:
                    f_poster, f_fallback = movie_engine.get_poster(int(f_id), focused.get("title", ""), "Cinema", 4.5)
                except Exception:
                    pass
            poster_thumb_html = f'<div style="width:44px; height:64px; flex-shrink:0; border:1.5px solid #C5A059; overflow:hidden; box-shadow:2px 2px 0px #1A050B; background:#1A050B;"><img src="{f_poster or f_fallback}" style="width:100%; height:100%; object-fit:cover;" onerror="this.onerror=null; this.src=\'{f_fallback}\';" /></div>' if (f_poster or f_fallback) else ''

            st.markdown(f"""
            <div style="background:linear-gradient(135deg, #7A0C24 0%, #4D0717 100%); border:2.5px solid #C5A059; box-shadow:4px 4px 0px #1A050B; padding:10px 16px; margin-bottom:1.1rem; display:flex; justify-content:space-between; align-items:center; gap:12px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    {poster_thumb_html}
                    <div>
                        <span style="background:#C5A059; color:#1A050B; font-size:0.65rem; font-weight:900; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1px solid #1A050B;">📌 SAVED MOVIE IN FOCUS</span>
                        <div style="font-weight:900; font-size:1.05rem; color:#FAF5E8; text-transform:uppercase; font-family:'Space Grotesk'; margin-top:4px;">{focused['title']}</div>
                    </div>
                </div>
                <div>
                    <a href="{focused.get('url', '#')}" target="_blank" class="cinema-buy-btn" style="padding:6px 14px; font-size:0.75rem;">🎬 Watch Online ↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with f_top2:
            st.button("Clear Focus ✕", key="clr_focus_m", width="stretch", on_click=clear_movie_focus)

    # Quick Industry / Category Bar
    st.markdown("<div style='font-size:0.8rem; font-weight:800; font-family:\"Space Grotesk\"; color:#7A0C24; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;'>🎭 SELECT MOVIE INDUSTRY / CATEGORY</div>", unsafe_allow_html=True)
    all_industries = movie_engine.get_industries()
    
    current_ind = st.session_state.get("selected_movie_industry", "All")
    if current_ind not in all_industries:
        current_ind = "All"
        st.session_state["selected_movie_industry"] = "All"

    cat_cols = st.columns(len(all_industries))
    for idx, ind in enumerate(all_industries):
        with cat_cols[idx]:
            if ind == "Nepali Cinema":
                btn_label = "🏔️ Nepali Cinema"
            elif ind == "Bollywood":
                btn_label = "🎬 Bollywood"
            elif ind == "Tollywood":
                btn_label = "🌟 Tollywood"
            elif ind == "Hollywood":
                btn_label = "🎥 Hollywood"
            else:
                btn_label = "🌐 All Movies"
            
            is_active = (current_ind == ind)
            btn_type = "primary" if is_active else "secondary"
            st.button(btn_label, key=f"btn_cat_{ind}", width="stretch", type=btn_type, on_click=set_cinema_industry, args=(ind,))

    st.markdown("<div style='margin-bottom:1.1rem;'></div>", unsafe_allow_html=True)

    f_col, r_col = st.columns([1.15, 2.35])

    with f_col:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #7A0C24 0%, #4D0717 100%); border:2px solid #C5A059; box-shadow:3px 3px 0px #1A050B; padding:10px 14px; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; box-sizing:border-box; overflow:hidden;">
            <div>
                <span style="background:#C5A059; color:#1A050B; font-size:0.62rem; font-weight:900; padding:2px 7px; text-transform:uppercase; letter-spacing:0.08em; border:1px solid #1A050B; margin-right:6px;">THEATRE</span>
                <span style="font-family:'Space Grotesk'; font-weight:900; font-size:0.9rem; color:#FAF5E8; text-transform:uppercase; letter-spacing:0.06em;">CURATION CONSOLE</span>
            </div>
            <span style="font-size:0.85rem; color:#C5A059;">🎛️</span>
        </div>
        """, unsafe_allow_html=True)

        chosen_industry = st.selectbox(
            "🎭 Cinema Industry",
            all_industries,
            key="sb_movie_industry",
            on_change=on_cinema_industry_change
        )
        st.session_state["selected_movie_industry"] = chosen_industry

        chosen_genres = st.multiselect(
            "🎬 Filter by Genre(s)",
            movie_engine.get_genres(),
            key="m_genres"
        )

        movie_query = st.text_input(
            "🔍 Plot Keywords / Themes",
            placeholder="e.g. heist, kathmandu, revenge, sci-fi...",
            key="input_movie_query"
        )

        # Quick keyword chips for instant discovery - 6 curated themes
        if chosen_industry == "Nepali Cinema":
            quick_chips = ["Kathmandu", "Loot", "Mustang", "Berlinale", "Pashupati", "White Sun"]
        elif chosen_industry == "Bollywood":
            quick_chips = ["Underworld", "Romance", "Mafia", "Revenge", "Heist", "Dacoit"]
        elif chosen_industry == "Tollywood":
            quick_chips = ["Revenge", "Action", "Mythology", "Family", "Hero", "Empire"]
        elif chosen_industry == "Hollywood":
            quick_chips = ["Space", "Heist", "Mafia", "Sci-Fi", "Detective", "Thriller"]
        else:
            quick_chips = ["Kathmandu", "Heist", "Underworld", "Space", "Revenge", "Romance"]

        st.markdown("<div style='font-size:0.68rem; font-weight:800; color:#7A0C24; text-transform:uppercase; letter-spacing:0.04em; margin-top:-0.3rem; margin-bottom:0.35rem;'>⚡ Quick Themes:</div>", unsafe_allow_html=True)
        for row_start in range(0, len(quick_chips), 2):
            row_items = quick_chips[row_start : row_start + 2]
            row_cols = st.columns(2)
            for c_offset, chip in enumerate(row_items):
                with row_cols[c_offset]:
                    st.button(
                        chip,
                        key=f"mchip_{chosen_industry}_{row_start + c_offset}",
                        width="stretch",
                        on_click=set_movie_query_theme,
                        args=(chip,)
                    )

        st.markdown("<div style='margin-bottom:0.8rem;'></div>", unsafe_allow_html=True)

        top_n_m = st.slider("🎞️ Recommendations Count", min_value=3, max_value=12, key="m_s")

        alpha_m = st.slider("⚖️ Algorithm Tuning (Plot vs Rating)", min_value=0.0, max_value=1.0, step=0.05, key="m_alpha")
        st.markdown(f"""
        <div style="background:#FAF6EE; border:1.5px solid #1A050B; border-left:4px solid #C5A059; padding:5px 9px; margin-top:-0.35rem; margin-bottom:0.85rem; font-size:0.72rem; color:#1A050B; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:4px; box-sizing:border-box; overflow:hidden;">
            <span>📖 <strong>Plot:</strong> {int(round(alpha_m*100))}%</span>
            <span style="color:#C5A059; font-weight:900;">•</span>
            <span>⭐ <strong>Critic:</strong> {int(round((1-alpha_m)*100))}%</span>
        </div>
        """, unsafe_allow_html=True)

        # Reset button if any filter is active
        has_active_filters = (
            chosen_industry != "All" or 
            len(chosen_genres) > 0 or 
            bool(movie_query and movie_query.strip()) or 
            alpha_m != 0.6 or 
            top_n_m != 5
        )
        if has_active_filters:
            st.button("↺ Reset Filters", key="btn_reset_m_filters", width="stretch", on_click=reset_cinema_filters)

    with r_col:
        if chosen_industry == "Nepali Cinema":
            st.markdown("""
            <div style="background:linear-gradient(135deg, #6B0F24 0%, #4A0817 100%); border:2.5px solid #C5A059; box-shadow:4px 4px 0px #1A050B; padding:14px 20px; margin-bottom:1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="background:#C5A059; color:#1A050B; font-size:0.68rem; font-weight:900; padding:3px 9px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1px solid #1A050B;">🏔️ SPOTLIGHT</span>
                        <span style="font-weight:900; font-size:1.05rem; color:#FAF5E8; text-transform:uppercase; font-family:'Space Grotesk';">Curated Nepali Masterpieces & Cult Classics</span>
                    </div>
                    <span style="font-size:0.75rem; font-weight:900; color:#1A050B; background:#C5A059; border:1.5px solid #1A050B; padding:2px 9px;">18 Titles</span>
                </div>
                <div style="font-size:0.84rem; color:#E8D8B8; margin-top:8px; line-height:1.55;">
                    Featuring Kathmandu underworld heists (<em>Loot</em>), Mustang romances (<em>Kabaddi</em>), Pashupatinath realism (<em>Pashupati Prasad</em>), to Berlinale & Venice festival selections (<em>Shambhala</em>, <em>Kalo Pothi</em>, <em>White Sun</em>).
                </div>
            </div>
            """, unsafe_allow_html=True)

        recs = movie_engine.recommend(
            selected_genres=chosen_genres,
            industry=chosen_industry,
            query_text=movie_query,
            top_n=top_n_m,
            alpha=alpha_m
        )

        if not recs:
            st.markdown(f"""
            <div style="background:#FAF6EE; border:2px dashed #7A0C24; padding:2rem; text-align:center; margin-top:0.8rem; box-shadow:3px 3px 0px #1A050B;">
                <div style="font-size:2rem; margin-bottom:0.4rem;">🎭</div>
                <div style="font-family:'Space Grotesk'; font-size:1.05rem; font-weight:900; color:#7A0C24; text-transform:uppercase; letter-spacing:0.04em;">No Matches Found in Curated Archive</div>
                <div style="font-size:0.85rem; color:#555555; margin-top:0.4rem; max-width:440px; margin-left:auto; margin-right:auto; line-height:1.5;">
                    No titles match your specific combination of genre filters and keywords in <strong>{chosen_industry}</strong>. Try clearing genres or adjusting the plot search query.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.9rem; padding-bottom:0.4rem; border-bottom:1.5px dashed #C5A059;">
                <div style="font-size:0.86rem; font-weight:800; font-family:'Space Grotesk'; text-transform:uppercase; color:#7A0C24; letter-spacing:0.04em;">
                    NOW SCREENING &bull; TOP {len(recs)} SELECTIONS IN {chosen_industry.upper()}
                </div>
                <div style="font-size:0.72rem; font-weight:800; background:#FAF6EE; color:#7A0C24; border:1px solid #C5A059; padding:2px 8px; letter-spacing:0.04em; text-transform:uppercase;">
                    HYBRID THEATRE ENGINE
                </div>
            </div>
            """, unsafe_allow_html=True)

        for m in recs:
            genres_html = " ".join([f'<span class="tag-cinema-genre">{g}</span>' for g in m["genres"][:4]])
            m_url = m.get("url") or f"https://www.google.com/search?q={urllib.parse.quote_plus(str(m.get('title', '')) + ' movie watch online')}"
            poster_src = m.get("poster_url") or m.get("fallback_poster") or ""
            fallback_src = m.get("fallback_poster") or ""
            if not str(poster_src).startswith("data:"):
                p_url, p_fb = movie_engine.get_poster(m['id'], m['title'], m.get('industry', 'Cinema'), m.get('rating', 4.5))
                poster_src = p_url if str(p_url).startswith("data:") else p_fb
            if not str(fallback_src).startswith("data:"):
                fallback_src = poster_src
            safe_title = html.escape(str(m.get('title', '')))

            st.markdown(f"""
            <div class="cinema-card">
                <div class="cinema-card-body">
                    <div class="cinema-poster-frame">
                        <img src="{poster_src}" 
                             class="cinema-poster-img" 
                             loading="lazy" 
                             referrerpolicy="no-referrer" 
                             onerror="this.onerror=null; this.src='{fallback_src}';" 
                             alt="{safe_title}" />
                    </div>
                    <div class="cinema-info-col">
                        <div>
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px;">
                                <div class="item-title" style="margin-bottom:0.25rem;">
                                    <a href="{m_url}" target="_blank" style="color:#7A0C24; text-decoration:none; font-family:'Space Grotesk'; font-weight:800; font-size:1.12rem;">{safe_title} <span style="font-size:0.85rem; color:#C5A059;">↗</span></a>
                                </div>
                                <span class="tag-cinema-match">{m['match_score']}% MATCH</span>
                            </div>
                            <div style="margin-top:0.35rem; display:flex; flex-wrap:wrap; align-items:center; gap:6px;">
                                <span class="tag-cinema-industry">{m['industry']}</span>
                                {genres_html}
                                <span style="font-size:0.85rem; color:#C5A059; margin-left:0.3rem; font-weight:900;">★ {m['rating']:.1f}</span>
                                <span style="font-size:0.75rem; color:#666666;">({m['rating_count']} ratings)</span>
                            </div>
                        </div>
                        <div class="cinema-reason-box" style="margin-top:0.6rem;">{m['explanation']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            b1, b2, _ = st.columns([1, 1.8, 4.2])
            with b1:
                if st.button("🔖 Save", key=f"s_m_{m['id']}"):
                    ok, msg = db.save_bookmark(st.session_state.user_id, "Movie", m['id'], m['title'], extra_info={"url": m_url, "poster_url": poster_src, "fallback_poster": fallback_src})
                    st.toast(msg)
            with b2:
                st.markdown(f'<a href="{m_url}" target="_blank" class="cinema-buy-btn">🎬 Watch Online ↗</a>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# TAB 2: PRODUCTS
# -------------------------------------------------------------------------
with tabs[2]:
    # Charcoal Slate & Balancing Teal Lifestyle & Products Marquee Header
    st.markdown("""
    <div class="product-marquis">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.5rem;">🛍️</span>
                <div>
                    <div style="font-family:'Space Grotesk'; font-size:1.35rem; font-weight:900; color:#FFFFFF; text-transform:uppercase; letter-spacing:0.06em; line-height:1.15;">
                        PRODUCTS & LIFESTYLE STORE
                    </div>
                    <div style="font-size:0.75rem; font-weight:800; color:#94A3B8; text-transform:uppercase; letter-spacing:0.08em; margin-top:3px;">
                        CURATED INDIAN BRANDS • HOROLOGY • APPAREL • AUDIO • TECH
                    </div>
                </div>
            </div>
            <div>
                <span class="product-domain-badge">
                    🏷️ DOMAIN 02: PRODUCTS
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    focused = st.session_state.get("focused_saved_item")
    if focused and focused.get("category", "").lower() in ["product", "products"]:
        f_top1, f_top2 = st.columns([4, 1.2])
        with f_top1:
            f_img = ""
            f_fallback = ""
            f_id = focused.get("id")
            if f_id:
                try:
                    f_img, f_fallback = resolve_product_image(int(f_id), focused.get("title", ""), "Product", "Products", 1999, 4.5)
                except Exception:
                    pass
            img_thumb_html = f'<div style="width:44px; height:64px; flex-shrink:0; border:1.5px solid #0D9488; overflow:hidden; box-shadow:2px 2px 0px #000000; background:#0F172A;"><img src="{f_img or f_fallback}" style="width:100%; height:100%; object-fit:cover;" onerror="this.onerror=null; this.src=\'{f_fallback}\';" /></div>' if (f_img or f_fallback) else ''

            st.markdown(f"""
            <div style="background:linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%); border:2.5px solid #000000; border-left:8px solid #0D9488; box-shadow:4px 4px 0px #000000; padding:10px 16px; margin-bottom:1.1rem; display:flex; justify-content:space-between; align-items:center; gap:12px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    {img_thumb_html}
                    <div>
                        <span style="background:#E5E7EB; color:#111827; font-size:0.65rem; font-weight:900; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1px solid #000000;">📌 SAVED PRODUCT IN FOCUS</span>
                        <div style="font-weight:900; font-size:1.05rem; color:#000000; text-transform:uppercase; font-family:'Space Grotesk'; margin-top:4px;">{focused['title']}</div>
                    </div>
                </div>
                <div>
                    <a href="{focused.get('url', '#')}" target="_blank" class="product-buy-btn" style="padding:6px 14px; font-size:0.75rem;">🛒 Buy Now ↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with f_top2:
            st.button("Clear Focus ✕", key="clr_focus_p", width="stretch", on_click=clear_product_focus)

    # Quick Product Category Bar
    st.markdown("<div style='font-size:0.8rem; font-weight:800; font-family:\"Space Grotesk\"; color:#4B5563; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;'>🛍️ SELECT PRODUCT CATEGORY</div>", unsafe_allow_html=True)
    all_categories = product_engine.get_categories()
    
    current_cat = st.session_state.get("selected_product_category", "All")
    if current_cat not in all_categories:
        current_cat = "All"
        st.session_state["selected_product_category"] = "All"

    featured_cats = ["All", "Watches", "Fragrance", "Audio", "Wearables", "Desk Setup"]
    cat_btn_cols = st.columns(len(featured_cats))
    for idx, c_name in enumerate(featured_cats):
        with cat_btn_cols[idx]:
            if c_name == "Watches":
                btn_txt = "⌚ Watches"
            elif c_name == "Fragrance":
                btn_txt = "🌸 Fragrance"
            elif c_name == "Audio":
                btn_txt = "🎧 Audio"
            elif c_name == "Wearables":
                btn_txt = "📱 Wearables"
            elif c_name == "Desk Setup":
                btn_txt = "🖥️ Desk Setup"
            else:
                btn_txt = "🌐 All Items"

            is_act = (current_cat == c_name)
            btn_style = "primary" if is_act else "secondary"
            st.button(btn_txt, key=f"btn_pcat_{c_name}", width="stretch", type=btn_style, on_click=set_product_category, args=(c_name,))

    st.markdown("<div style='margin-bottom:1.1rem;'></div>", unsafe_allow_html=True)

    p_f_col, p_r_col = st.columns([1.15, 2.35])

    with p_f_col:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border:2px solid #000000; box-shadow:3px 3px 0px #000000; padding:10px 14px; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; box-sizing:border-box; overflow:hidden;">
            <div>
                <div style="font-family:'Space Grotesk'; font-size:0.95rem; font-weight:900; color:#FFFFFF; text-transform:uppercase; letter-spacing:0.06em;">
                    🛍️ PRODUCT FILTERS
                </div>
                <div style="font-size:0.68rem; font-weight:800; color:#94A3B8; text-transform:uppercase; letter-spacing:0.08em;">
                    CURATION ENGINE
                </div>
            </div>
            <span style="background:#0D9488; color:#FFFFFF; font-size:0.62rem; font-weight:900; padding:3px 8px; border:1px solid #000000; text-transform:uppercase; letter-spacing:0.06em;">
                LIVE
            </span>
        </div>
        """, unsafe_allow_html=True)

        if "sb_product_category" not in st.session_state or st.session_state["sb_product_category"] not in all_categories:
            st.session_state["sb_product_category"] = current_cat

        chosen_cat = st.selectbox(
            "Category",
            all_categories,
            key="sb_product_category",
            on_change=on_product_category_change
        )
        st.session_state["selected_product_category"] = chosen_cat

        chosen_brand = st.selectbox("Brand", product_engine.get_brands(), key="sb_product_brand")
        min_p, max_p = product_engine.get_price_range()
        if "p_budget" not in st.session_state:
            st.session_state["p_budget"] = max_p
        budget = st.slider("Max Budget (₹ INR)", min_p, max_p, step=500, key="p_budget")
        category_placeholders = {
            "Audio": "e.g. noise cancelling, deep bass, 100H playtime, dolby...",
            "Wearables": "e.g. amoled display, bluetooth calling, rugged outdoor...",
            "Watches": "e.g. automatic mechanical, ceramic slim, devanagari, chronograph...",
            "Fragrance": "e.g. oud wood, citrus fresh, edp long lasting, body mist...",
            "Desk Setup": "e.g. 65W GaN, 20000mAh, adjustable laptop stand...",
            "Computer Accessories": "e.g. mechanical keyboard, red switches, silent mouse...",
            "Gaming": "e.g. wireless gamepad, dual rumble, optical gaming mouse...",
            "Smart Home": "e.g. RGB batten, BLDC fan, 360 security camera...",
        }
        p_ph = category_placeholders.get(chosen_cat, "e.g. ceramic slim, mechanical, oud, noise cancellation...")
        p_query = st.text_input("Feature Search", placeholder=p_ph, key="input_product_query")

        # Category-driven popular features (strictly max 4 per category, concise labels)
        category_features = {
            "Audio": ["Noise Cancel", "Deep Bass", "Dolby Audio", "100H Battery"],
            "Wearables": ["AMOLED Screen", "BT Calling", "Rugged Sport", "Heart & SpO2"],
            "Watches": ["Automatic", "Ceramic Slim", "Devanagari", "Chronograph"],
            "Fragrance": ["Oud Wood", "Citrus Fresh", "Long Lasting", "Body Mist"],
            "Desk Setup": ["65W GaN", "Powerbank", "Laptop Stand", "Fast Charge"],
            "Computer Accessories": ["Mechanical", "RGB Lighting", "Silent Click", "Tenkeyless"],
            "Gaming": ["Gamepad", "Dual Rumble", "Gaming Mouse", "Low Latency"],
            "Smart Home": ["RGB Sync", "BLDC Motor", "360 Camera", "Voice Control"],
        }
        feat_chips = category_features.get(chosen_cat, ["Noise Cancel", "AMOLED", "Automatic", "Oud Wood"])[:4]

        st.markdown("<div style='font-size:0.75rem; font-weight:800; font-family:\"Space Grotesk\"; color:#4B5563; text-transform:uppercase; letter-spacing:0.06em; margin-top:0.6rem; margin-bottom:0.35rem;'>⚡ POPULAR FEATURES</div>", unsafe_allow_html=True)
        fc_cols = st.columns(2)
        for i, f_txt in enumerate(feat_chips):
            with fc_cols[i % 2]:
                st.button(f_txt, key=f"pchip_{chosen_cat}_{i}", width="stretch", on_click=set_product_query_feature, args=(f_txt,))

        top_n_p = st.slider("Results", 3, 10, 5, key="p_s")

        st.button("↺ Reset Filters", key="btn_reset_p_filters", width="stretch", on_click=reset_product_filters, args=(max_p,))

    with p_r_col:
        if chosen_cat == "Watches":
            st.markdown("""
            <div style="background:#FFFDF9; border:2px solid #000000; border-left:6px solid #1E293B; box-shadow:4px 4px 0px #000000; padding:12px 18px; margin-bottom:1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="background:#1E293B; color:#FFFFFF; font-size:0.68rem; font-weight:800; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1.5px solid #000000;">⌚ WATCHES</span>
                        <span style="font-weight:900; font-size:1.05rem; color:#000000; text-transform:uppercase; font-family:'Space Grotesk';">Iconic Horology & Modern Smartwatches</span>
                    </div>
                    <span style="font-size:0.75rem; font-weight:800; color:#0F766E; background:#CCFBF1; border:1.5px solid #000000; padding:2px 8px;">11 Titles</span>
                </div>
                <div style="font-size:0.82rem; color:#444444; margin-top:6px; line-height:1.5;">
                    Featuring Tata Titan (Edge ceramic ultra-slim & Octane mechanical automatic), historic HMT (Kohinoor & Janata Devanagari Hindi dial), Fastrack chronographs & AMOLED smartwatches, and Sonata minimalist quartz.
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif chosen_cat == "Fragrance":
            st.markdown("""
            <div style="background:#FFFDF9; border:2px solid #000000; border-left:6px solid #1E293B; box-shadow:4px 4px 0px #000000; padding:12px 18px; margin-bottom:1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="background:#1E293B; color:#FFFFFF; font-size:0.68rem; font-weight:800; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1.5px solid #000000;">🌸 FRAGRANCES</span>
                        <span style="font-weight:900; font-size:1.05rem; color:#000000; text-transform:uppercase; font-family:'Space Grotesk';">Luxury Perfumes, Mists & Natural Attars</span>
                    </div>
                    <span style="font-size:0.75rem; font-weight:800; color:#0F766E; background:#CCFBF1; border:1.5px solid #000000; padding:2px 8px;">10 Titles</span>
                </div>
                <div style="font-size:0.82rem; color:#444444; margin-top:6px; line-height:1.5;">
                    Featuring French-crafted Titan Skinn (Raw & Celeste), Bella Vita Luxury (CEO Man & Honey Oud), Bombay Shaving Company (Mexico EDP), Forest Essentials pure Kashmiri Nargis mist, and Phool upcycled natural floral perfumes.
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif chosen_cat == "Audio":
            st.markdown("""
            <div style="background:#FFFDF9; border:2px solid #000000; border-left:6px solid #1E293B; box-shadow:4px 4px 0px #000000; padding:12px 18px; margin-bottom:1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="background:#1E293B; color:#FFFFFF; font-size:0.68rem; font-weight:800; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1.5px solid #000000;">🎧 AUDIO</span>
                        <span style="font-weight:900; font-size:1.05rem; color:#000000; text-transform:uppercase; font-family:'Space Grotesk';">High-Fidelity Audio & Wireless ANC</span>
                    </div>
                    <span style="font-size:0.75rem; font-weight:800; color:#0F766E; background:#CCFBF1; border:1.5px solid #000000; padding:2px 8px;">Premium Picks</span>
                </div>
                <div style="font-size:0.82rem; color:#444444; margin-top:6px; line-height:1.5;">
                    Featuring boAt Nirvana Ion ANC wireless earbuds with 120-hour playback, Noise Buds VS series, and Boult Audio high-definition acoustics designed for Indian bass preferences.
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif chosen_cat == "Wearables":
            st.markdown("""
            <div style="background:#FFFDF9; border:2px solid #000000; border-left:6px solid #1E293B; box-shadow:4px 4px 0px #000000; padding:12px 18px; margin-bottom:1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="background:#1E293B; color:#FFFFFF; font-size:0.68rem; font-weight:800; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1.5px solid #000000;">📱 WEARABLES</span>
                        <span style="font-weight:900; font-size:1.05rem; color:#000000; text-transform:uppercase; font-family:'Space Grotesk';">AMOLED Smartwatches & Fitness Trackers</span>
                    </div>
                    <span style="font-size:0.75rem; font-weight:800; color:#0F766E; background:#CCFBF1; border:1.5px solid #000000; padding:2px 8px;">Top Tech</span>
                </div>
                <div style="font-size:0.82rem; color:#444444; margin-top:6px; line-height:1.5;">
                    Equipped with Bluetooth calling, SpO2 monitoring, always-on AMOLED displays, and durable IP68 water resistance from Noise, Fire-Boltt, and Fastrack.
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif chosen_cat == "Desk Setup":
            st.markdown("""
            <div style="background:#FFFDF9; border:2px solid #000000; border-left:6px solid #1E293B; box-shadow:4px 4px 0px #000000; padding:12px 18px; margin-bottom:1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="background:#1E293B; color:#FFFFFF; font-size:0.68rem; font-weight:800; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1.5px solid #000000;">🖥️ DESK SETUP</span>
                        <span style="font-weight:900; font-size:1.05rem; color:#000000; text-transform:uppercase; font-family:'Space Grotesk';">Productivity Essentials & Minimalist Workspace</span>
                    </div>
                    <span style="font-size:0.75rem; font-weight:800; color:#0F766E; background:#CCFBF1; border:1.5px solid #000000; padding:2px 8px;">Curated</span>
                </div>
                <div style="font-size:0.82rem; color:#444444; margin-top:6px; line-height:1.5;">
                    Ergonomic laptop stands, vegan leather desk mats, wireless fast chargers, and cable organizers from DailyObjects and Portronics.
                </div>
            </div>
            """, unsafe_allow_html=True)

        p_recs = product_engine.recommend(
            category=chosen_cat,
            max_price_inr=budget,
            brand=chosen_brand,
            query_text=p_query,
            top_n=top_n_p
        )

        st.markdown(f"<div style='font-size:0.85rem; font-weight:800; text-transform:uppercase; color:#4B5563; letter-spacing:0.05em; margin-bottom:0.8rem;'>Showing Top {len(p_recs)} results in {chosen_cat}</div>", unsafe_allow_html=True)

        # ── Load individual product images as base64 data URIs ──
        _img_dir = os.path.join(os.path.dirname(__file__), "assets", "product_images")
        _dir_mtime = max([os.path.getmtime(os.path.join(_img_dir, f)) for f in os.listdir(_img_dir)]) if os.path.exists(_img_dir) and os.listdir(_img_dir) else 0

        @st.cache_data(show_spinner=False)
        def _load_all_product_images_v2(img_dir: str, cache_mtime: float) -> dict:
            result = {}
            if os.path.exists(img_dir):
                for fname in os.listdir(img_dir):
                    fpath = os.path.join(img_dir, fname)
                    if os.path.isfile(fpath) and os.path.getsize(fpath) > 100:
                        name_lower = fname.lower()
                        for ext in [".jpg", ".jpeg", ".png", ".webp"]:
                            if name_lower.endswith(ext):
                                base_key = fname[:-len(ext)]
                                mime = "image/png" if ext == ".png" else "image/jpeg"
                                try:
                                    with open(fpath, "rb") as f:
                                        data_uri = f"data:{mime};base64," + base64.b64encode(f.read()).decode()
                                    result[base_key] = data_uri
                                    clean_id = base_key.lstrip("p")
                                    if clean_id.isdigit():
                                        result[int(clean_id)] = data_uri
                                except Exception:
                                    pass
            return result

        _product_imgs = _load_all_product_images_v2(_img_dir, _dir_mtime)

        for p in p_recs:
            p_url = p.get("url") or f"https://www.amazon.in/s?k={urllib.parse.quote_plus(str(p.get('name', '')))}"
            safe_name = html.escape(str(p.get("name", "")))
            
            # Resolve individual real product image -> engine image -> SVG fallback
            poster_src = (
                _product_imgs.get(p["id"]) or 
                _product_imgs.get(f"p{p['id']}") or 
                _product_imgs.get(str(p["id"])) or 
                p.get("image_url", "")
            )
            fallback_src = p.get("fallback_image") or ""
            if not poster_src or not str(poster_src).startswith("data:"):
                p_img, p_fb = resolve_product_image(
                    product_id=p["id"],
                    name=p["name"],
                    brand=p["brand"],
                    category=p["category"],
                    price_inr=p["price_inr"],
                    rating=p["rating"]
                )
                poster_src = p_img if str(p_img).startswith("data:") else p_fb
                if not fallback_src:
                    fallback_src = p_fb

            if not fallback_src:
                fallback_src = poster_src

            st.markdown(f"""
            <div class="product-card">
                <div class="product-card-body">
                    <a href="{p_url}" target="_blank" class="product-img-frame" title="View {safe_name}">
                        <img src="{poster_src}" 
                             class="product-img" 
                             loading="lazy" 
                             referrerpolicy="no-referrer" 
                             onerror="this.onerror=null; this.src='{fallback_src}';" 
                             alt="{safe_name}" />
                    </a>
                    <div class="product-info-col">
                        <div>
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px;">
                                <div class="product-title" style="margin-bottom:0.25rem;">
                                    <a href="{p_url}" target="_blank">{safe_name} <span style="font-size:0.85rem; color:#0D9488;">↗</span></a>
                                </div>
                                <span class="tag-product-match">{p['match_score']}% MATCH</span>
                            </div>
                            <div style="margin-top:0.35rem; display:flex; flex-wrap:wrap; align-items:center; gap:6px;">
                                <span class="tag-product-brand">{p['brand']}</span>
                                <span class="tag-product-cat">{p['category']}</span>
                                <span class="tag-product-price">₹{p['price_inr']:,}</span>
                                <span style="font-size:0.88rem; color:#0D9488; font-weight:800; margin-left:0.2rem;">★ {p['rating']:.1f}</span>
                            </div>
                            <p style="color:#333333; font-size:0.84rem; margin:0.45rem 0 0 0; line-height:1.45;">{p['description']}</p>
                        </div>
                        <div class="product-reason-box" style="margin-top:0.6rem;">{p['explanation']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            pb1, pb2, _ = st.columns([1, 1.8, 4.2])
            with pb1:
                if st.button("🔖 Save", key=f"s_p_{p['id']}"):
                    ok, msg = db.save_bookmark(st.session_state.user_id, "Product", p['id'], p['name'], extra_info={"url": p_url, "image_url": poster_src, "fallback_image": fallback_src})
                    st.toast(msg)
            with pb2:
                st.markdown(f'<a href="{p_url}" target="_blank" class="product-buy-btn">🛒 Buy Now ↗</a>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# TAB 3: CAREER PATHWAYS & SKILLS (EMERALD GREEN & SUNBEAM YELLOW)
# -------------------------------------------------------------------------
with tabs[3]:
    # Emerald Green & Sunbeam Yellow Career & Skills Marquis Header
    st.markdown("""
    <div class="career-marquis">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.5rem;">🎓</span>
                <div>
                    <div style="font-family:'Space Grotesk'; font-size:1.35rem; font-weight:900; color:#FFFFFF; text-transform:uppercase; letter-spacing:0.06em; line-height:1.15;">
                        CAREER PATHWAYS & SKILLS
                    </div>
                    <div style="font-size:0.75rem; font-weight:800; color:#A7F3D0; text-transform:uppercase; letter-spacing:0.08em; margin-top:3px;">
                        GROWTH & PROGRESS ENGINE • STANFORD • GOOGLE • META • HARVARD
                    </div>
                </div>
            </div>
            <div>
                <span class="career-domain-badge">
                    ⚡ DOMAIN 03: CAREERS & SKILLS
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    focused = st.session_state.get("focused_saved_item")
    if focused and focused.get("category", "").lower() in ["course", "courses"]:
        f_top1, f_top2 = st.columns([4, 1.2])
        with f_top1:
            st.markdown(f"""
            <div style="background:#FFFFFF; border:2.5px solid #064E3B; border-left:8px solid #059669; box-shadow:4px 4px 0px #064E3B; padding:10px 16px; margin-bottom:1.1rem; display:flex; justify-content:space-between; align-items:center; gap:12px;">
                <div>
                    <span style="background:#064E3B; color:#FFFFFF; font-size:0.65rem; font-weight:900; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1px solid #022C22;">📌 SAVED COURSE IN FOCUS</span>
                    <div style="font-weight:900; font-size:1.05rem; color:#064E3B; text-transform:uppercase; font-family:'Space Grotesk'; margin-top:4px;">{focused['title']}</div>
                </div>
                <div>
                    <a href="{focused.get('url', '#')}" target="_blank" class="career-enroll-btn" style="padding:6px 14px; font-size:0.75rem; width:auto; display:inline-block;">🎓 Enroll Now ↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with f_top2:
            st.button("Clear Focus ✕", key="clr_focus_c", width="stretch", on_click=clear_course_focus)

    # Quick Career Domain Selector Bar (Emerald Green & Sunbeam Yellow)
    st.markdown("<div style='font-size:0.8rem; font-weight:800; font-family:\"Space Grotesk\"; color:#064E3B; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;'>🎓 SELECT CAREER DOMAIN</div>", unsafe_allow_html=True)
    all_domains = course_engine.get_categories()

    current_dom = st.session_state.get("selected_course_domain", "All")
    if current_dom not in all_domains:
        current_dom = "All"
        st.session_state["selected_course_domain"] = "All"

    featured_doms = ["All", "Artificial Intelligence", "Data Science", "Software Engineering", "Cloud Computing", "Cybersecurity", "Business & Management"]
    dom_btn_cols = st.columns(len(featured_doms))
    for idx, d_name in enumerate(featured_doms):
        with dom_btn_cols[idx]:
            if d_name == "Artificial Intelligence":
                btn_txt = "🤖 AI & ML"
            elif d_name == "Data Science":
                btn_txt = "📊 Data Science"
            elif d_name == "Software Engineering":
                btn_txt = "💻 Software"
            elif d_name == "Cloud Computing":
                btn_txt = "☁️ Cloud"
            elif d_name == "Cybersecurity":
                btn_txt = "🛡️ Security"
            elif d_name == "Business & Management":
                btn_txt = "📈 Business"
            else:
                btn_txt = "🌐 All Domains"

            is_act = (current_dom == d_name)
            btn_style = "primary" if is_act else "secondary"
            st.button(btn_txt, key=f"btn_cdom_{d_name}", width="stretch", type=btn_style, on_click=set_course_domain, args=(d_name,))

    st.markdown("<div style='margin-bottom:1.1rem;'></div>", unsafe_allow_html=True)

    c_f_col, c_r_col = st.columns([1.15, 2.35])

    with c_f_col:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #064E3B 0%, #022C22 100%); border:2px solid #064E3B; box-shadow:3px 3px 0px #064E3B; padding:10px 14px; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; box-sizing:border-box; overflow:hidden;">
            <div>
                <div style="font-family:'Space Grotesk'; font-size:0.95rem; font-weight:900; color:#FFFFFF; text-transform:uppercase; letter-spacing:0.06em;">
                    🎓 CAREER FILTERS
                </div>
                <div style="font-size:0.68rem; font-weight:800; color:#A7F3D0; text-transform:uppercase; letter-spacing:0.08em;">
                    PROGRESS & SKILLS ENGINE
                </div>
            </div>
            <span style="background:#FACC15; color:#022C22; font-size:0.62rem; font-weight:900; padding:3px 8px; border:1px solid #064E3B; text-transform:uppercase; letter-spacing:0.06em;">
                LIVE
            </span>
        </div>
        """, unsafe_allow_html=True)

        if "sb_course_domain" not in st.session_state or st.session_state["sb_course_domain"] not in all_domains:
            st.session_state["sb_course_domain"] = current_dom

        chosen_c_cat = st.selectbox(
            "Domain",
            all_domains,
            key="sb_course_domain",
            on_change=on_course_domain_change
        )
        st.session_state["selected_course_domain"] = chosen_c_cat

        chosen_lvl = st.selectbox("Level", course_engine.get_difficulty_levels(), key="sb_course_level")
        target_skills = st.text_input("Desired Skills", placeholder="e.g. Python, SQL, Neural Networks", key="input_course_query")

        # Contextual In-Demand Skill Chips (Max 4 popular features per domain)
        skill_presets = {
            "Artificial Intelligence": ["Python", "Machine Learning", "Neural Networks", "Deep Learning"],
            "Data Science": ["Python", "SQL", "Data Analysis", "Tableau"],
            "Software Engineering": ["Full Stack", "Data Structures", "Algorithms", "Web Dev"],
            "Cloud Computing": ["AWS", "Google Cloud", "DevOps", "Microservices"],
            "Cybersecurity": ["Network Security", "Cryptography", "Ethical Hacking", "InfoSec"],
            "Business & Management": ["Project Management", "Leadership", "Agile", "Strategy"],
        }
        active_presets = skill_presets.get(chosen_c_cat, ["Machine Learning", "Python", "Data Science", "Cloud Architecture"])

        st.markdown("<div style='font-size:0.75rem; font-weight:800; font-family:\"Space Grotesk\"; color:#064E3B; text-transform:uppercase; letter-spacing:0.05em; margin:0.6rem 0 0.35rem 0;'>⚡ IN-DEMAND SKILLS</div>", unsafe_allow_html=True)
        sc1, sc2 = st.columns(2)
        for s_i, s_name in enumerate(active_presets[:4]):
            target_col = sc1 if s_i % 2 == 0 else sc2
            with target_col:
                st.button(s_name, key=f"cchip_{s_i}_{s_name.replace(' ', '_')}", width="stretch", on_click=set_course_query_skill, args=(s_name,))

        st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)
        top_n_c = st.slider("Results", 3, 10, 5, key="c_s")

        has_active_c_filters = (
            chosen_c_cat != "All" or 
            chosen_lvl != "All" or 
            bool(target_skills and target_skills.strip()) or 
            top_n_c != 5
        )
        if has_active_c_filters:
            st.button("↺ Reset Career Filters", key="btn_reset_c_filters", width="stretch", on_click=reset_course_filters)

    with c_r_col:
        c_recs = course_engine.recommend(
            category=chosen_c_cat,
            difficulty=chosen_lvl,
            desired_skills=target_skills,
            top_n=top_n_c
        )

        st.markdown(f"<div style='font-size:0.85rem; font-weight:700; text-transform:uppercase; color:#064E3B; margin-bottom:0.8rem;'>Showing Top {len(c_recs)} career pathways</div>", unsafe_allow_html=True)

        for c in c_recs:
            # Highlight skills: matching query skills get Sunbeam Yellow highlighter .skill-highlighter;
            # if no query skills matched, first 2 core skills get .skill-highlighter, rest get .skill-curriculum
            target_tokens = [tok.lower().strip() for tok in (target_skills or "").split() if len(tok.strip()) > 1]
            skill_badges = []
            for s_idx, s in enumerate(c["skills"][:5]):
                s_lower = s.lower()
                is_match = any(t in s_lower for t in target_tokens) if target_tokens else (s_idx < 2)
                badge_class = "skill-highlighter" if is_match else "skill-curriculum"
                skill_badges.append(f'<span class="{badge_class}">{s}</span>')
            skills_html = "".join(skill_badges)

            c_url = c.get("url") or "https://coursera.org"
            st.markdown(f"""
            <div class="career-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                    <span class="tag-career-match">{c['match_score']}% MATCH</span>
                    <span style="font-size:0.75rem; color:#064E3B; text-transform:uppercase; font-weight:800; letter-spacing:0.05em;">🎓 {c['category']}</span>
                </div>
                <div class="item-title"><a href="{c_url}" target="_blank" style="color:#064E3B; text-decoration:underline;">{c['title']} ↗</a></div>
                <div style="margin:0.45rem 0 0.5rem 0; display:flex; flex-wrap:wrap; align-items:center; gap:6px;">
                    <span class="tag-career-org">{c['organization']}</span>
                    <span class="tag-career-level">{c['difficulty']}</span>
                    <span class="tag-career-duration">⏱️ {c['duration_hours']} Hours</span>
                    <span style="font-size:0.85rem; color:#064E3B; margin-left:0.3rem; font-weight:800;">★ {c['rating']:.1f}</span>
                </div>
                <div style="margin-top:0.4rem; margin-bottom:0.3rem;">{skills_html}</div>
                <div class="career-path-strip">
                    <span class="career-path-label">⚡ LEARNING PATHWAY</span>
                    <span class="career-path-step">01 Foundation</span>
                    <span class="career-path-arrow">➔</span>
                    <span class="career-path-step">02 Applied Labs</span>
                    <span class="career-path-arrow">➔</span>
                    <span class="career-path-step" style="background:#FDE047; color:#022C22; padding:1px 6px; border:1px solid #064E3B; font-weight:900;">03 Capstone & Credential</span>
                </div>
                <p style="color:#333333; font-size:0.84rem; margin:0.45rem 0 0 0; line-height:1.45;">{c['description']}</p>
                <div class="career-reason-box" style="margin-top:0.6rem;">{c['explanation']}</div>
            </div>
            """, unsafe_allow_html=True)

            cb1, cb2, _ = st.columns([1, 1.8, 4.2])
            with cb1:
                if st.button("🔖 Save", key=f"s_c_{c['id']}"):
                    ok, msg = db.save_bookmark(st.session_state.user_id, "Course", c['id'], c['title'], extra_info={"url": c_url})
                    st.toast(msg)
            with cb2:
                st.markdown(f'<a href="{c_url}" target="_blank" class="career-enroll-btn">🎓 Enroll Now ↗</a>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# TAB 4: BENCHMARKS
# -------------------------------------------------------------------------
with tabs[4]:
    st.markdown("<h3 style='font-family:\"Space Grotesk\"; text-transform:uppercase; font-size:1.2rem; font-weight:700; color:#000000; margin-bottom:0.2rem;'>Evaluation Metrics</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555555; font-size:0.85rem; font-weight:600; text-transform:uppercase;'>Computed on an 80/20 train/test user rating holdout split.</p>", unsafe_allow_html=True)

    eval_res = evaluate_models(k=5)
    summ = eval_res.get("summary", {})

    kp1, kp2, kp3, kp4 = st.columns(4)
    with kp1:
        st.metric("Holdout Ratings", f"{summ.get('test_size', 20164):,}")
    with kp2:
        st.metric("Baseline RMSE", summ.get("baseline_rmse", 1.05))
    with kp3:
        st.metric("Hybrid Precision@5", summ.get("hybrid_precision", 0.272))
    with kp4:
        st.metric("Hybrid Recall@5", summ.get("hybrid_recall", 0.161))

    st.markdown("<hr style='border:none; border-top:2.5px solid #000000; margin:1.5rem 0;'>", unsafe_allow_html=True)

    b_df = eval_res.get("benchmark_df", pd.DataFrame())
    if not b_df.empty:
        st.dataframe(b_df, width="stretch")
        st.markdown("<br>", unsafe_allow_html=True)
        st.bar_chart(b_df.set_index("Algorithm")[["Precision@5", "Recall@5"]])
