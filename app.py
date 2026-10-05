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

    .cinema-card {
        background-color: #FFFFFF !important;
        border: 2px solid #1A050B !important;
        border-top: 5px solid #7A0C24 !important;
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
    div[class*="st-key-btn_reset_m_filters"] button {
        background: #FAF6EE !important;
        color: #7A0C24 !important;
        border: 2px solid #7A0C24 !important;
        box-shadow: 2.5px 2.5px 0px #1A050B !important;
        font-weight: 800 !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        padding: 0.4rem 0.6rem !important;
        margin-top: 0.5rem !important;
        transition: all 0.2s ease !important;
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
    div[class*="st-key-mchip_"] button {
        background: #FAF6EE !important;
        color: #1A050B !important;
        border: 1.5px solid #C5A059 !important;
        font-size: 0.76rem !important;
        font-weight: 700 !important;
        padding: 0.3rem 0.5rem !important;
        border-radius: 0px !important;
        box-shadow: 2px 2px 0px #1A050B !important;
        letter-spacing: 0.02em !important;
        min-height: 32px !important;
        line-height: 1.25 !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div[class*="st-key-mchip_"] button *,
    div[class*="st-key-mchip_"] button p,
    div[class*="st-key-mchip_"] button span {
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
        word-break: keep-all !important;
        font-size: 0.76rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
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
       SAFFRON ORANGE & BALANCING TEAL (PRODUCTS & LIFESTYLE DOMAIN)
       Saffron orange drives shopping intent and warmth; Teal balances the CTA
       ========================================================================= */
    .product-marquis {
        background: linear-gradient(135deg, #FF7A00 0%, #E65100 100%) !important;
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
        border-top: 5px solid #FF7A00 !important;
        box-shadow: 4px 4px 0px #000000 !important;
        border-radius: 0px !important;
        padding: 1.15rem 1.35rem !important;
        margin-bottom: 0.65rem !important;
        position: relative !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    .product-card:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0px #FF7A00 !important;
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
        text-decoration-color: #FF7A00 !important;
        text-decoration-thickness: 2px !important;
        transition: color 0.15s ease, text-decoration-color 0.15s ease !important;
    }

    .product-title a:hover {
        color: #E65100 !important;
        text-decoration-color: #0D9488 !important;
    }

    .tag-product-match {
        float: right;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        background: linear-gradient(135deg, #FF7A00 0%, #E65100 100%) !important;
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
        background: #FFF3E0 !important;
        color: #D84315 !important;
        border: 1.5px solid #FF7A00 !important;
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
        background: #F3F4F6 !important;
        color: #1F2937 !important;
        border: 1.5px solid #000000 !important;
        margin-right: 0.35rem !important;
        margin-bottom: 0.3rem !important;
    }

    .tag-product-price {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 900 !important;
        color: #E65100 !important;
        letter-spacing: -0.01em !important;
        margin-left: 0.4rem !important;
    }

    .product-reason-box {
        background: #FFFDF9 !important;
        border: 1.5px solid #000000 !important;
        border-left: 5px solid #FF7A00 !important;
        padding: 0.7rem 0.9rem !important;
        margin-top: 0.75rem !important;
        font-size: 0.84rem !important;
        font-weight: 500 !important;
        color: #2D2319 !important;
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
        box-shadow: 4px 4px 0px #FF7A00 !important;
    }

    /* Product Category Selection Bar (btn_pcat_) */
    div[class*="st-key-btn_pcat_"] button {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.03em !important;
        text-transform: uppercase !important;
        transition: all 0.15s ease !important;
        padding: 0.4rem 0.6rem !important;
        border-radius: 0px !important;
    }

    div[class*="st-key-btn_pcat_"] button[kind="primary"] {
        background: linear-gradient(135deg, #FF7A00 0%, #E65100 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        box-shadow: 3.5px 3.5px 0px #000000 !important;
        font-weight: 900 !important;
    }

    div[class*="st-key-btn_pcat_"] button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        box-shadow: 2px 2px 0px #000000 !important;
        font-weight: 700 !important;
    }

    div[class*="st-key-btn_pcat_"] button[kind="secondary"]:hover {
        background: #FFF3E0 !important;
        color: #E65100 !important;
        border-color: #FF7A00 !important;
        box-shadow: 3px 3px 0px #000000 !important;
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
        background: #FFF3E0 !important;
        border-color: #FF7A00 !important;
        color: #E65100 !important;
        box-shadow: 3px 3px 0px #0D9488 !important;
    }

    /* Product Filter Inputs & Sliders */
    div[class*="st-key-sb_product_category"] label,
    div[class*="st-key-sb_product_brand"] label,
    div[class*="st-key-input_product_query"] label,
    div[class*="st-key-p_budget"] label,
    div[class*="st-key-p_s"] label {
        color: #E65100 !important;
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
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }

    div[class*="st-key-input_product_query"] input:focus,
    div[class*="st-key-sb_product_category"] [data-baseweb="select"] > div:focus-within,
    div[class*="st-key-sb_product_brand"] [data-baseweb="select"] > div:focus-within {
        border-color: #FF7A00 !important;
        box-shadow: 2.5px 2.5px 0px #0D9488 !important;
    }

    div[class*="st-key-p_budget"] [data-baseweb="slider"] div[role="slider"],
    div[class*="st-key-p_s"] [data-baseweb="slider"] div[role="slider"] {
        background-color: #FFFFFF !important;
        border: 2.5px solid #FF7A00 !important;
        box-shadow: 2px 2px 0px #0D9488 !important;
    }

    div[class*="st-key-p_budget"] [data-testid="stThumbValue"],
    div[class*="st-key-p_s"] [data-testid="stThumbValue"] {
        color: #E65100 !important;
        font-weight: 900 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Product Reset Button */
    div[class*="st-key-btn_reset_p_filters"] button {
        background: #FFF3E0 !important;
        color: #E65100 !important;
        border: 2px solid #FF7A00 !important;
        box-shadow: 2.5px 2.5px 0px #000000 !important;
        font-weight: 800 !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        padding: 0.4rem 0.6rem !important;
        margin-top: 0.5rem !important;
        transition: all 0.2s ease !important;
    }

    div[class*="st-key-btn_reset_p_filters"] button:hover {
        background: #FF7A00 !important;
        color: #FFFFFF !important;
        border-color: #000000 !important;
        box-shadow: 3.5px 3.5px 0px #0D9488 !important;
    }

    div[class*="st-key-btn_reset_p_filters"] button:hover * {
        color: #FFFFFF !important;
    }

    /* Quick Feature Chips in Product Filter */
    div[class*="st-key-pchip_"] button {
        background: #FFFDF9 !important;
        color: #000000 !important;
        border: 1.5px solid #FF7A00 !important;
        font-size: 0.76rem !important;
        font-weight: 700 !important;
        padding: 0.3rem 0.5rem !important;
        border-radius: 0px !important;
        box-shadow: 2px 2px 0px #000000 !important;
        letter-spacing: 0.02em !important;
        min-height: 32px !important;
        line-height: 1.25 !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div[class*="st-key-pchip_"] button *,
    div[class*="st-key-pchip_"] button p,
    div[class*="st-key-pchip_"] button span {
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
        word-break: keep-all !important;
        font-size: 0.76rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
    }

    div[class*="st-key-pchip_"] button:hover {
        background: #FF7A00 !important;
        color: #FFFFFF !important;
        border-color: #000000 !important;
        box-shadow: 3px 3px 0px #0D9488 !important;
    }

    div[class*="st-key-pchip_"] button:hover * {
        color: #FFFFFF !important;
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
    div[data-testid="stWidgetLabel"],
    div[data-testid="stWidgetLabel"] *,
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] span,
    div[data-testid="stWidgetLabel"] div,
    label[data-testid="stWidgetLabel"],
    label[data-testid="stWidgetLabel"] *,
    label[data-testid="stWidgetLabel"] p,
    label[data-testid="stWidgetLabel"] span,
    label,
    label *,
    label p,
    label span,
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
    div[data-testid="stSlider"] [data-testid="stWidgetLabel"] span,
    div[data-testid="stSlider"] [data-testid="stTickBarMin"],
    div[data-testid="stSlider"] [data-testid="stTickBarMax"] {
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.82rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        opacity: 1 !important;
        visibility: visible !important;
        -webkit-text-stroke: 0.25px #000000 !important;
    }

    /* Slider values & numbers */
    div[data-testid="stSlider"] [data-testid="stThumbValue"],
    div[data-testid="stSlider"] div[role="slider"] {
        color: #000000 !important;
        font-weight: 800 !important;
    }

    /* Form Inputs, Selectboxes, and MultiSelects */
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stSelectbox"] [role="combobox"],
    div[data-testid="stSelectbox"] [data-baseweb="select"],
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
    div[data-testid="stMultiSelect"] > div,
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
    }

    div[data-testid="stSelectbox"] [role="combobox"] *,
    div[data-testid="stSelectbox"] div[data-testid="stMarkdownContainer"] *,
    div[data-testid="stSelectbox"] span,
    div[data-testid="stSelectbox"] p,
    div[data-testid="stMultiSelect"] div,
    div[data-testid="stMultiSelect"] span,
    div[data-testid="stMultiSelect"] p {
        color: #000000 !important;
        font-weight: 700 !important;
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

# Session State Initialization
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "auth_error" not in st.session_state:
    st.session_state.auth_error = None
if "auth_success" not in st.session_state:
    st.session_state.auth_success = None
if "portal_tabs" not in st.session_state:
    st.session_state["portal_tabs"] = "🏠 Overview"
if "focused_saved_item" not in st.session_state:
    st.session_state.focused_saved_item = None
if "input_movie_query" not in st.session_state:
    st.session_state["input_movie_query"] = ""
if "selected_movie_industry" not in st.session_state:
    st.session_state["selected_movie_industry"] = "All"
if "sb_movie_industry" not in st.session_state:
    st.session_state["sb_movie_industry"] = "All"
if "m_genres" not in st.session_state:
    st.session_state["m_genres"] = []
if "m_s" not in st.session_state:
    st.session_state["m_s"] = 5
if "m_alpha" not in st.session_state:
    st.session_state["m_alpha"] = 0.6
if "input_product_query" not in st.session_state:
    st.session_state["input_product_query"] = ""
if "input_course_query" not in st.session_state:
    st.session_state["input_course_query"] = ""
if "overview_domain_selectbox" not in st.session_state:
    st.session_state["overview_domain_selectbox"] = "🏠 Overview Hub — (Select a Domain below)"

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
def get_engines_v3(movies_mtime, products_mtime, courses_mtime, code_mtime):
    import importlib
    import models.movie_rec
    import models.product_rec
    importlib.reload(models.movie_rec)
    importlib.reload(models.product_rec)
    m = models.movie_rec.MovieRecommender()
    p = models.product_rec.ProductRecommender()
    c = CourseRecommender()
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
                st.session_state["portal_tabs"] = "🏠 Overview"
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
                st.session_state["portal_tabs"] = "🏠 Overview"
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
            st.session_state["portal_tabs"] = "🏠 Overview"
            st.rerun()

    st.stop()  # Stop execution here if not logged in

# =========================================================================
# STATE 2: AUTHENTICATED PORTAL & LANDING EXPERIENCE
# =========================================================================
m_csv = "data/cleaned/movies_clean.csv"
p_csv = "data/cleaned/products_clean.csv"
c_csv = "data/cleaned/courses_clean.csv"
rec_code = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "movie_rec.py")
movie_engine, product_engine, course_engine = get_engines_v3(
    os.path.getmtime(m_csv) if os.path.exists(m_csv) else 0,
    os.path.getmtime(p_csv) if os.path.exists(p_csv) else 0,
    os.path.getmtime(c_csv) if os.path.exists(c_csv) else 0,
    os.path.getmtime(rec_code) if os.path.exists(rec_code) else 0,
)

# Top Header Navigation Bar (Placed at the very top edge with vibrant color palette)
header_col1, header_col2 = st.columns([2.5, 1.5], gap="small")
with header_col1:
    st.markdown('''
        <div style="display:flex; align-items:center; gap:12px; background:linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%); border:2.5px solid #000000; box-shadow:4px 4px 0px #000000; padding:10px 18px; margin-bottom:1.2rem;">
            <span style="font-weight:900; font-size:1.35rem; letter-spacing:0.08em; background:linear-gradient(90deg, #FF2E93 0%, #FF8A00 50%, #FFD600 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-family:'Space Grotesk';">⚡ RECOM.AI</span>
            <span style="background:linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%); color:#FFFFFF; font-size:0.65rem; font-weight:800; padding:3px 9px; letter-spacing:0.06em; text-transform:uppercase; border:1.5px solid #000000; box-shadow:2px 2px 0px #000000;">PORTAL</span>
            <span style="color:#94A3B8; font-size:0.75rem; font-weight:800; text-transform:uppercase; letter-spacing:0.05em;">• MULTI-DOMAIN INTELLIGENCE ENGINE</span>
        </div>
    ''', unsafe_allow_html=True)

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
            st.session_state["portal_tabs"] = "🏠 Overview"
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

# Safe Tab Switching Callback (Runs before widgets are instantiated on rerun)
def set_active_tab(tab_name, industry=None, category=None):
    st.session_state["portal_tabs"] = tab_name
    st.session_state["overview_domain_selectbox"] = "🏠 Overview Hub — (Select a Domain below)"
    if industry:
        st.session_state["selected_movie_industry"] = industry
        st.session_state["sb_movie_industry"] = industry
    if category:
        st.session_state["selected_product_category"] = category
        st.session_state["sb_product_category"] = category

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
    st.markdown('<div style="display:flex;height:8px;margin-bottom:1rem"><span style="flex:1;background:#B3123B"></span><span style="flex:1;background:#FF8A00"></span><span style="flex:1;background:#3B5BFF"></span></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='font-family:\"Space Grotesk\"; text-transform:uppercase; font-size:1.8rem; font-weight:700; margin-bottom:0.2rem;'>WELCOME BACK</h2>", unsafe_allow_html=True)
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

    # Vertical Card 1: Cinema Hub (Domain 01: Crimson #B3123B)
    st.markdown("""
    <div class="min-card" style="border-top:5px solid #B3123B !important; margin-bottom:0.8rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <span style="font-size:0.75rem; color:#B3123B; text-transform:uppercase; font-weight:800; letter-spacing:0.06em;">🎬 DOMAIN 01</span>
            <span style="background:#B3123B; color:#FFFFFF; font-size:0.72rem; font-weight:800; padding:3px 8px; text-transform:uppercase; border:1.5px solid #000000; margin:0;">CINEMA & ENTERTAINMENT</span>
        </div>
        <div style="font-size:1.35rem; font-weight:800; color:#000000; text-transform:uppercase; font-family:'Space Grotesk'; margin:0.2rem 0 0.4rem 0;">Cinema Hub</div>
        <p style="font-size:0.88rem; color:#333333; line-height:1.6; margin-bottom:0.6rem;">
            Explore Bollywood, Tollywood, Hollywood, and Nepali cinema films with multi-genre filters, content-based TF-IDF plot search, and IMDb score weighting.
        </p>
        <div style="margin-bottom:0.2rem;">
            <span class="tag-neutral">Bollywood</span>
            <span class="tag-neutral">Tollywood</span>
            <span class="tag-neutral">Hollywood</span>
            <span class="tag-neutral">Nepali Cinema</span>
            <span class="tag-neutral">TF-IDF Plot Match</span>
            <span class="tag-neutral">Genre Filters</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    c_btn1, c_btn2 = st.columns([1, 1])
    with c_btn1:
        st.button("Explore All Movies ➔", key="btn_ov_cinema", width="stretch", on_click=set_active_tab, args=("🎬 Movies & Cinema", "All"))
    with c_btn2:
        st.button("🏔️ Explore Nepali Cinema ➔", key="btn_ov_cinema_nepali", width="stretch", on_click=set_active_tab, args=("🎬 Movies & Cinema", "Nepali Cinema"))

    st.markdown("<div style='margin-bottom:1.6rem;'></div>", unsafe_allow_html=True)

    # Vertical Card 2: Products E-Commerce & Lifestyle (Domain 02: Saffron #FF8A00)
    st.markdown("""
    <div class="min-card" style="border-top:5px solid #FF8A00 !important; margin-bottom:0.8rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <span style="font-size:0.75rem; color:#FF8A00; text-transform:uppercase; font-weight:800; letter-spacing:0.06em;">🛍️ DOMAIN 02</span>
            <span style="background:#FF8A00; color:#FFFFFF; font-size:0.72rem; font-weight:800; padding:3px 8px; text-transform:uppercase; border:1.5px solid #000000; margin:0;">PRODUCTS & LIFESTYLE</span>
        </div>
        <div style="font-size:1.35rem; font-weight:800; color:#000000; text-transform:uppercase; font-family:'Space Grotesk'; margin:0.2rem 0 0.4rem 0;">Products Hub</div>
        <p style="font-size:0.88rem; color:#333333; line-height:1.6; margin-bottom:0.6rem;">
            Discover curated audio, iconic watches (Titan, HMT, Fastrack, Sonata), luxury fragrances (Titan Skinn, Bella Vita, Forest Essentials, Phool), wearables, and electronics with real-time INR (₹) budget filters.
        </p>
        <div style="margin-bottom:0.2rem;">
            <span class="tag-neutral">₹ INR Pricing</span>
            <span class="tag-neutral">⌚ Watches</span>
            <span class="tag-neutral">🌸 Fragrance</span>
            <span class="tag-neutral">Titan</span>
            <span class="tag-neutral">HMT</span>
            <span class="tag-neutral">Titan Skinn</span>
            <span class="tag-neutral">boAt</span>
            <span class="tag-neutral">Noise</span>
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

    # Vertical Card 3: Career & Skills (Domain 03: Blue #3B5BFF)
    st.markdown("""
    <div class="min-card" style="border-top:5px solid #3B5BFF !important; margin-bottom:0.8rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <span style="font-size:0.75rem; color:#3B5BFF; text-transform:uppercase; font-weight:800; letter-spacing:0.06em;">🎓 DOMAIN 03</span>
            <span style="background:#3B5BFF; color:#FFFFFF; font-size:0.72rem; font-weight:800; padding:3px 8px; text-transform:uppercase; border:1.5px solid #000000; margin:0;">CAREER EDUCATION</span>
        </div>
        <div style="font-size:1.35rem; font-weight:800; color:#000000; text-transform:uppercase; font-family:'Space Grotesk'; margin:0.2rem 0 0.4rem 0;">Career & Skill Pathways</div>
        <p style="font-size:0.88rem; color:#333333; line-height:1.6; margin-bottom:0.6rem;">
            Match job goals to industry certifications and university pathways from Stanford, Google, Meta, and Harvard in AI, Data Science, and Software Engineering.
        </p>
        <div style="margin-bottom:0.2rem;">
            <span class="tag-neutral">Stanford</span>
            <span class="tag-neutral">Google</span>
            <span class="tag-neutral">Meta</span>
            <span class="tag-neutral">Machine Learning</span>
            <span class="tag-neutral">Full Stack</span>
            <span class="tag-neutral">Skill Match</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Explore Pathways ➔", key="btn_ov_courses", width="stretch", on_click=set_active_tab, args=("🎓 Courses & Skills",))

    st.markdown("<hr style='border:none; border-top:2.5px solid #000000; margin:2.2rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-family:\"Space Grotesk\"; text-transform:uppercase; font-size:1.2rem; font-weight:700; color:#000000; margin-bottom:0.3rem;'>Curated Recommendations</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555555; font-size:0.85rem; font-weight:600; text-transform:uppercase; margin-bottom:1.2rem;'>Top-rated picks across all domains, stacked for quick exploration.</p>", unsafe_allow_html=True)

    # Vertical Recommendation 1: RRR
    st.markdown("""
    <div class="min-card" style="margin-bottom:1.2rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <span class="tag-match" style="margin:0;">98.5% MATCH</span>
            <span style="font-size:0.75rem; color:#555555; text-transform:uppercase; font-weight:800; letter-spacing:0.05em;">🎬 CINEMA PICK</span>
        </div>
        <div class="item-title"><a href="https://www.google.com/search?q=RRR+2022+movie+watch+online" target="_blank" style="color:#000000; text-decoration:underline;">RRR (2022) ↗</a></div>
        <div style="margin:0.4rem 0 0.5rem 0;">
            <span class="tag-accent">Tollywood</span>
            <span class="tag-neutral">Action</span>
            <span style="font-size:0.85rem; color:#000000; margin-left:0.4rem; font-weight:700;">★ 4.9</span>
            <span style="font-size:0.75rem; color:#666666; margin-left:0.2rem;">(Top Community Narrative)</span>
        </div>
        <div class="reason-box">High community rating & iconic Telugu period action narrative with groundbreaking visual spectacle.</div>
        <div style="margin-top:0.8rem; max-width:280px;"><a href="https://www.google.com/search?q=RRR+2022+movie+watch+online" target="_blank" class="buy-btn">🎬 Watch Online ↗</a></div>
    </div>
    """, unsafe_allow_html=True)

    # Vertical Recommendation 1B: Nepali Cinema (Loot)
    st.markdown("""
    <div class="min-card" style="margin-bottom:1.2rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <span class="tag-match" style="margin:0;">98.2% MATCH</span>
            <span style="font-size:0.75rem; color:#555555; text-transform:uppercase; font-weight:800; letter-spacing:0.05em;">🏔️ NEPALI CINEMA PICK</span>
        </div>
        <div class="item-title"><a href="https://www.google.com/search?q=Loot+2012+nepali+movie+watch+online" target="_blank" style="color:#000000; text-decoration:underline;">Loot (2012) ↗</a></div>
        <div style="margin:0.4rem 0 0.5rem 0;">
            <span class="tag-accent">Nepali Cinema</span>
            <span class="tag-neutral">Action</span>
            <span class="tag-neutral">Crime</span>
            <span class="tag-neutral">Thriller</span>
            <span style="font-size:0.85rem; color:#000000; margin-left:0.4rem; font-weight:700;">★ 4.8</span>
            <span style="font-size:0.75rem; color:#666666; margin-left:0.2rem;">(Revolution of Modern Nepali Cinema)</span>
        </div>
        <div class="reason-box">Cult classic Kathmandu underworld bank heist thriller that redefined contemporary Nepali cinema with iconic performances and realistic pacing.</div>
        <div style="margin-top:0.8rem; max-width:280px;"><a href="https://www.google.com/search?q=Loot+2012+nepali+movie+watch+online" target="_blank" class="buy-btn">🎬 Watch Online ↗</a></div>
    </div>
    """, unsafe_allow_html=True)

    # Vertical Recommendation 2: boAt Nirvana Ion
    st.markdown("""
    <div class="product-card" style="margin-bottom:1.2rem;">
        <span class="tag-product-match">96.8% MATCH</span>
        <div style="font-size:0.75rem; color:#E65100; text-transform:uppercase; font-weight:800; letter-spacing:0.05em; margin-bottom:0.2rem;">🎧 AUDIO PICK</div>
        <div class="product-title"><a href="https://www.boat-lifestyle.com/products/nirvana-ion" target="_blank">boAt Nirvana Ion ANC ↗</a></div>
        <div style="margin:0.4rem 0 0.5rem 0;">
            <span class="tag-product-brand">boAt</span>
            <span class="tag-product-cat">Audio</span>
            <span class="tag-product-price">₹2,499</span>
            <span style="font-size:0.85rem; color:#0D9488; margin-left:0.4rem; font-weight:800;">★ 4.8</span>
        </div>
        <div class="product-reason-box">Top active noise cancellation wireless earbuds with 120-hour playback and dual EQ modes from boAt.</div>
        <div style="margin-top:0.8rem; max-width:280px;"><a href="https://www.boat-lifestyle.com/products/nirvana-ion" target="_blank" class="product-buy-btn">🛒 Buy Now ↗</a></div>
    </div>
    """, unsafe_allow_html=True)

    # Vertical Recommendation 2B: Titan Watch Pick
    st.markdown("""
    <div class="product-card" style="margin-bottom:1.2rem;">
        <span class="tag-product-match">97.4% MATCH</span>
        <div style="font-size:0.75rem; color:#E65100; text-transform:uppercase; font-weight:800; letter-spacing:0.05em; margin-bottom:0.2rem;">⌚ WATCH PICK</div>
        <div class="product-title"><a href="https://www.titan.co.in/shop/watches" target="_blank">Titan Octane Mechanical Automatic Watch ↗</a></div>
        <div style="margin:0.4rem 0 0.5rem 0;">
            <span class="tag-product-brand">Titan</span>
            <span class="tag-product-cat">Watches</span>
            <span class="tag-product-price">₹12,495</span>
            <span style="font-size:0.85rem; color:#0D9488; margin-left:0.4rem; font-weight:800;">★ 4.8</span>
        </div>
        <div class="product-reason-box">Exquisite automatic mechanical watch by Tata Titan featuring skeleton dial displaying inner mechanical gear movements and stainless steel bracelet.</div>
        <div style="margin-top:0.8rem; max-width:280px;"><a href="https://www.titan.co.in/shop/watches" target="_blank" class="product-buy-btn">🛒 Buy Now ↗</a></div>
    </div>
    """, unsafe_allow_html=True)

    # Vertical Recommendation 2C: Fragrance Pick
    st.markdown("""
    <div class="product-card" style="margin-bottom:1.2rem;">
        <span class="tag-product-match">96.5% MATCH</span>
        <div style="font-size:0.75rem; color:#E65100; text-transform:uppercase; font-weight:800; letter-spacing:0.05em; margin-bottom:0.2rem;">🌸 FRAGRANCE PICK</div>
        <div class="product-title"><a href="https://www.skinn.in/product/skinn-raw-perfume-for-men-100ml" target="_blank">Titan Skinn Raw Eau De Parfum (100ml) ↗</a></div>
        <div style="margin:0.4rem 0 0.5rem 0;">
            <span class="tag-product-brand">Titan Skinn</span>
            <span class="tag-product-cat">Fragrance</span>
            <span class="tag-product-price">₹2,495</span>
            <span style="font-size:0.85rem; color:#0D9488; margin-left:0.4rem; font-weight:800;">★ 4.9</span>
        </div>
        <div class="product-reason-box">French-crafted luxury Eau De Parfum for India blending fresh citrus bergamot, watery watermelon, and earthy Indonesian patchouli.</div>
        <div style="margin-top:0.8rem; max-width:280px;"><a href="https://www.skinn.in/product/skinn-raw-perfume-for-men-100ml" target="_blank" class="product-buy-btn">🛒 Buy Now ↗</a></div>
    </div>
    """, unsafe_allow_html=True)

    # Vertical Recommendation 3: ML Specialization
    st.markdown("""
    <div class="min-card" style="margin-bottom:1.2rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <span class="tag-match" style="margin:0;">99.1% MATCH</span>
            <span style="font-size:0.75rem; color:#555555; text-transform:uppercase; font-weight:800; letter-spacing:0.05em;">🎓 CAREER PICK</span>
        </div>
        <div class="item-title"><a href="https://coursera.org/specializations/machine-learning-introduction" target="_blank" style="color:#000000; text-decoration:underline;">Machine Learning Specialization ↗</a></div>
        <div style="margin:0.4rem 0 0.5rem 0;">
            <span class="tag-accent">Stanford</span>
            <span class="tag-neutral">Beginner</span>
            <span style="font-size:0.85rem; color:#000000; margin-left:0.4rem; font-weight:700;">⏱️ 60 Hours</span>
            <span style="font-size:0.85rem; color:#000000; margin-left:0.4rem; font-weight:700;">★ 4.9</span>
        </div>
        <div class="reason-box">Fundamental ML certification taught by Andrew Ng covering supervised learning, neural networks, and decision trees.</div>
        <div style="margin-top:0.8rem; max-width:280px;"><a href="https://coursera.org/specializations/machine-learning-introduction" target="_blank" class="buy-btn">🎓 Enroll Now ↗</a></div>
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

    f_col, r_col = st.columns([1.1, 2.4])

    with f_col:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #7A0C24 0%, #4D0717 100%); border:2px solid #C5A059; box-shadow:3px 3px 0px #1A050B; padding:10px 14px; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
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
        <div style="background:#FAF6EE; border:1.5px solid #1A050B; border-left:4px solid #C5A059; padding:5px 9px; margin-top:-0.35rem; margin-bottom:0.85rem; font-size:0.72rem; color:#1A050B; display:flex; justify-content:space-between; align-items:center;">
            <span>📖 <strong>Plot Match:</strong> {int(round(alpha_m*100))}%</span>
            <span style="color:#C5A059; font-weight:900;">•</span>
            <span>⭐ <strong>Critic Score:</strong> {int(round((1-alpha_m)*100))}%</span>
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
            st.button("↺ Reset All Cinema Filters", key="btn_reset_m_filters", width="stretch", on_click=reset_cinema_filters)

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
                                    <a href="{m_url}" target="_blank" style="color:#1A050B; text-decoration:none; font-family:'Space Grotesk'; font-weight:800; font-size:1.12rem;">{safe_title} <span style="font-size:0.85rem; color:#7A0C24;">↗</span></a>
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

            b1, b2, b3, _ = st.columns([1, 1, 1.8, 3.2])
            with b1:
                if st.button("🔖 Save", key=f"s_m_{m['id']}"):
                    ok, msg = db.save_bookmark(st.session_state.user_id, "Movie", m['id'], m['title'], extra_info={"url": m_url, "poster_url": poster_src, "fallback_poster": fallback_src})
                    st.toast(msg)
            with b2:
                if st.button("👍 Like", key=f"l_m_{m['id']}"):
                    db.save_feedback(st.session_state.user_id, "Movie", m['id'], "like")
                    st.toast(f"Liked {m['title']}!")
            with b3:
                st.markdown(f'<a href="{m_url}" target="_blank" class="cinema-buy-btn">🎬 Watch Online ↗</a>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# TAB 2: PRODUCTS
# -------------------------------------------------------------------------
with tabs[2]:
    # Saffron & Balancing Teal Lifestyle & Products Marquee Header
    st.markdown("""
    <div class="product-marquis">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.5rem;">🛍️</span>
                <div>
                    <div style="font-family:'Space Grotesk'; font-size:1.35rem; font-weight:900; color:#FFFFFF; text-transform:uppercase; letter-spacing:0.06em; line-height:1.15;">
                        PRODUCTS & LIFESTYLE STORE
                    </div>
                    <div style="font-size:0.75rem; font-weight:800; color:#FFE8D6; text-transform:uppercase; letter-spacing:0.08em; margin-top:3px;">
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
            st.markdown(f"""
            <div style="background:linear-gradient(135deg, #FFF8F0 0%, #FFF3E0 100%); border:2.5px solid #000000; border-left:8px solid #FF7A00; box-shadow:4px 4px 0px #000000; padding:10px 16px; margin-bottom:1.1rem; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="background:#FF7A00; color:#FFFFFF; font-size:0.65rem; font-weight:900; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1px solid #000000;">📌 SAVED PRODUCT IN FOCUS</span>
                    <span style="font-weight:900; font-size:1.05rem; color:#000000; text-transform:uppercase; font-family:'Space Grotesk';">{focused['title']}</span>
                </div>
                <div>
                    <a href="{focused.get('url', '#')}" target="_blank" class="product-buy-btn" style="padding:6px 14px; font-size:0.75rem;">🛒 Buy Now ↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with f_top2:
            st.button("Clear Focus ✕", key="clr_focus_p", width="stretch", on_click=clear_product_focus)

    # Quick Product Category Bar
    st.markdown("<div style='font-size:0.8rem; font-weight:800; font-family:\"Space Grotesk\"; color:#E65100; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;'>🛍️ SELECT PRODUCT CATEGORY</div>", unsafe_allow_html=True)
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
                btn_txt = "🌐 All Products"

            is_act = (current_cat == c_name)
            btn_style = "primary" if is_act else "secondary"
            st.button(btn_txt, key=f"btn_pcat_{c_name}", width="stretch", type=btn_style, on_click=set_product_category, args=(c_name,))

    st.markdown("<div style='margin-bottom:1.1rem;'></div>", unsafe_allow_html=True)

    p_f_col, p_r_col = st.columns([1.1, 2.4])

    with p_f_col:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #FF7A00 0%, #E65100 100%); border:2px solid #000000; box-shadow:3px 3px 0px #000000; padding:10px 14px; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-family:'Space Grotesk'; font-size:0.95rem; font-weight:900; color:#FFFFFF; text-transform:uppercase; letter-spacing:0.06em;">
                    🛍️ PRODUCT FILTERS
                </div>
                <div style="font-size:0.68rem; font-weight:800; color:#FFE8D6; text-transform:uppercase; letter-spacing:0.08em;">
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
        p_query = st.text_input("Feature Search", placeholder="e.g. ceramic slim, mechanical, oud, noise cancellation", key="input_product_query")

        # Quick feature inspiration tags
        st.markdown("<div style='font-size:0.75rem; font-weight:800; font-family:\"Space Grotesk\"; color:#E65100; text-transform:uppercase; letter-spacing:0.06em; margin-top:0.6rem; margin-bottom:0.35rem;'>⚡ POPULAR FEATURES</div>", unsafe_allow_html=True)
        feat_chips = ["Ceramic Slim", "Automatic", "Oud Wood", "Noise Cancelling", "Ergonomic", "Waterproof"]
        fc_cols = st.columns(2)
        for i, f_txt in enumerate(feat_chips):
            with fc_cols[i % 2]:
                st.button(f_txt, key=f"pchip_{i}", width="stretch", on_click=set_product_query_feature, args=(f_txt,))

        top_n_p = st.slider("Results", 3, 10, 5, key="p_s")

        st.button("Reset Filters ↺", key="btn_reset_p_filters", width="stretch", on_click=reset_product_filters, args=(max_p,))

    with p_r_col:
        if chosen_cat == "Watches":
            st.markdown("""
            <div style="background:#FFFDF9; border:2px solid #000000; border-left:6px solid #FF7A00; box-shadow:4px 4px 0px #000000; padding:12px 18px; margin-bottom:1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="background:#FF7A00; color:#FFFFFF; font-size:0.68rem; font-weight:800; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1.5px solid #000000;">⌚ WATCHES</span>
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
            <div style="background:#FFFDF9; border:2px solid #000000; border-left:6px solid #FF7A00; box-shadow:4px 4px 0px #000000; padding:12px 18px; margin-bottom:1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="background:#FF7A00; color:#FFFFFF; font-size:0.68rem; font-weight:800; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1.5px solid #000000;">🌸 FRAGRANCES</span>
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
            <div style="background:#FFFDF9; border:2px solid #000000; border-left:6px solid #FF7A00; box-shadow:4px 4px 0px #000000; padding:12px 18px; margin-bottom:1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="background:#FF7A00; color:#FFFFFF; font-size:0.68rem; font-weight:800; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1.5px solid #000000;">🎧 AUDIO</span>
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
            <div style="background:#FFFDF9; border:2px solid #000000; border-left:6px solid #FF7A00; box-shadow:4px 4px 0px #000000; padding:12px 18px; margin-bottom:1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="background:#FF7A00; color:#FFFFFF; font-size:0.68rem; font-weight:800; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1.5px solid #000000;">📱 WEARABLES</span>
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
            <div style="background:#FFFDF9; border:2px solid #000000; border-left:6px solid #FF7A00; box-shadow:4px 4px 0px #000000; padding:12px 18px; margin-bottom:1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="background:#FF7A00; color:#FFFFFF; font-size:0.68rem; font-weight:800; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px; border:1.5px solid #000000;">🖥️ DESK SETUP</span>
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

        st.markdown(f"<div style='font-size:0.85rem; font-weight:800; text-transform:uppercase; color:#E65100; letter-spacing:0.05em; margin-bottom:0.8rem;'>Showing Top {len(p_recs)} results in {chosen_cat}</div>", unsafe_allow_html=True)

        for p in p_recs:
            p_url = p.get("url") or f"https://www.amazon.in/s?k={urllib.parse.quote_plus(str(p.get('name', '')))}"
            st.markdown(f"""
            <div class="product-card">
                <span class="tag-product-match">{p['match_score']}% MATCH</span>
                <div class="product-title"><a href="{p_url}" target="_blank">{p['name']} ↗</a></div>
                <div style="margin-top:0.45rem; display:flex; flex-wrap:wrap; align-items:center; gap:6px;">
                    <span class="tag-product-brand">{p['brand']}</span>
                    <span class="tag-product-cat">{p['category']}</span>
                    <span class="tag-product-price">₹{p['price_inr']:,}</span>
                    <span style="font-size:0.88rem; color:#0D9488; font-weight:800; margin-left:0.2rem;">★ {p['rating']:.1f}</span>
                </div>
                <p style="color:#333333; font-size:0.84rem; margin:0.45rem 0 0 0; line-height:1.45;">{p['description']}</p>
                <div class="product-reason-box">{p['explanation']}</div>
            </div>
            """, unsafe_allow_html=True)

            pb1, pb2, pb3, _ = st.columns([1, 1, 1.8, 3.2])
            with pb1:
                if st.button("🔖 Save", key=f"s_p_{p['id']}"):
                    ok, msg = db.save_bookmark(st.session_state.user_id, "Product", p['id'], p['name'], extra_info={"url": p_url})
                    st.toast(msg)
            with pb2:
                if st.button("👍 Like", key=f"l_p_{p['id']}"):
                    db.save_feedback(st.session_state.user_id, "Product", p['id'], "like")
                    st.toast(f"Liked {p['name']}!")
            with pb3:
                st.markdown(f'<a href="{p_url}" target="_blank" class="product-buy-btn">🛒 Buy Now ↗</a>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# TAB 3: COURSES
# -------------------------------------------------------------------------
with tabs[3]:
    focused = st.session_state.get("focused_saved_item")
    if focused and focused.get("category", "").lower() in ["course", "courses"]:
        f_top1, f_top2 = st.columns([4, 1.2])
        with f_top1:
            st.markdown(f"""
            <div style="background:#FFFFFF; border:2.5px solid #000000; box-shadow:4px 4px 0px #000000; padding:10px 16px; margin-bottom:1.1rem; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="background:#000000; color:#FFFFFF; font-size:0.65rem; font-weight:800; padding:3px 8px; text-transform:uppercase; letter-spacing:0.08em; margin-right:8px;">📌 SAVED COURSE IN FOCUS</span>
                    <span style="font-weight:900; font-size:1.05rem; color:#000000; text-transform:uppercase; font-family:'Space Grotesk';">{focused['title']}</span>
                </div>
                <div>
                    <a href="{focused.get('url', '#')}" target="_blank" class="buy-btn" style="padding:6px 14px; font-size:0.75rem;">🎓 Enroll Now ↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with f_top2:
            if st.button("Clear Focus ✕", key="clr_focus_c", width="stretch"):
                st.session_state.focused_saved_item = None
                st.session_state["input_course_query"] = ""
                st.rerun()

    c_f_col, c_r_col = st.columns([1, 2.5])

    with c_f_col:
        st.markdown("<div style='font-size:0.9rem; font-weight:700; font-family:\"Space Grotesk\"; color:#000000; text-transform:uppercase; margin-bottom:0.6rem;'>FILTERS</div>", unsafe_allow_html=True)
        chosen_c_cat = st.selectbox("Domain", course_engine.get_categories())
        chosen_lvl = st.selectbox("Level", course_engine.get_difficulty_levels())
        target_skills = st.text_input("Desired Skills", placeholder="e.g. Python, SQL, Machine Learning", key="input_course_query")
        top_n_c = st.slider("Results", 3, 10, 5, key="c_s")

    with c_r_col:
        c_recs = course_engine.recommend(
            category=chosen_c_cat,
            difficulty=chosen_lvl,
            desired_skills=target_skills,
            top_n=top_n_c
        )

        st.markdown(f"<div style='font-size:0.85rem; font-weight:700; text-transform:uppercase; color:#555555; margin-bottom:0.8rem;'>Showing Top {len(c_recs)} results</div>", unsafe_allow_html=True)

        for c in c_recs:
            skills_html = " ".join([f'<span class="tag-neutral">{s}</span>' for s in c["skills"][:4]])
            c_url = c.get("url") or "https://coursera.org"
            st.markdown(f"""
            <div class="min-card">
                <span class="tag-match">{c['match_score']}% MATCH</span>
                <div class="item-title"><a href="{c_url}" target="_blank" style="color:#000000; text-decoration:underline;">{c['title']} ↗</a></div>
                <div style="margin-top:0.4rem;">
                    <span class="tag-accent">{c['organization']}</span>
                    <span class="tag-neutral">{c['difficulty']}</span>
                    <span class="tag-neutral">{c['duration_hours']} Hours</span>
                    <span style="font-size:0.85rem; color:#000000; margin-left:0.4rem; font-weight:700;">★ {c['rating']:.1f}</span>
                </div>
                <div style="margin-top:0.35rem;">{skills_html}</div>
                <p style="color:#333333; font-size:0.84rem; margin:0.4rem 0 0 0;">{c['description']}</p>
                <div class="reason-box">{c['explanation']}</div>
            </div>
            """, unsafe_allow_html=True)

            cb1, cb2, cb3, _ = st.columns([1, 1, 1.8, 3.2])
            with cb1:
                if st.button("🔖 Save", key=f"s_c_{c['id']}"):
                    ok, msg = db.save_bookmark(st.session_state.user_id, "Course", c['id'], c['title'], extra_info={"url": c_url})
                    st.toast(msg)
            with cb2:
                if st.button("👍 Like", key=f"l_c_{c['id']}"):
                    db.save_feedback(st.session_state.user_id, "Course", c['id'], "like")
                    st.toast(f"Liked {c['title']}!")
            with cb3:
                st.markdown(f'<a href="{c_url}" target="_blank" class="buy-btn">🎓 Enroll Now ↗</a>', unsafe_allow_html=True)

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
