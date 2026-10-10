"""
RECOM.ai — Conversational AI Assistant Engine
Provides human-like, high-quality multi-domain recommendations (Movies, Products, Courses).
Supports Google Gemini (Free Tier) when an API key is available, and an intelligent
built-in conversational synthesis engine that works 100% out-of-the-box without requiring any user keys.
"""

import os
import re
import json
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """You are RECOM.ai's conversational intelligence concierge and multi-domain expert advisor.
You talk directly to users, answering their questions descriptively, comprehensively, and intelligently.

CORE RESPONSE BEHAVIOR & GUIDELINES:
1. TALK DIRECTLY TO THE USER & EXPLAIN DESCRIPTIVELY:
   - When the user asks a conceptual, philosophical, informational, or explanatory question (e.g., "is ai important", "what is machine learning", "how does a recommender work", "tell me about Christopher Nolan", "why is tech evolving so fast"):
     Directly talk to the user! Provide an articulate, multi-angle, descriptive, and comprehensive answer.
     DO NOT force catalog recommendations or course lists when the user didn't ask for them!
2. ONLY RECOMMEND WHEN EXPLICITLY ASKED:
   - Only suggest specific catalog items (movies, products, courses) when the user explicitly requests recommendations, suggestions, options, comparisons, or items to watch/buy/enroll in.
3. NEVER GIVE CANNED OR BOILERPLATE TEXT:
   - Do NOT output repetitive robotic disclaimers or rigid templates. Speak naturally, engagingly, and with high intellectual depth.
4. LOW TEMPERATURE & FACTUAL GROUNDING:
   - Maintain high factual rigor, structured reasoning, clear headings, and concise takeaways (Temperature: 0.2).
"""

_WEB_KNOWLEDGE_CACHE = {}

class ChatbotEngine:
    """Conversational Recommender Engine with built-in conversational intelligence & Gemini integration."""

    def __init__(self, movie_engine=None, product_engine=None, course_engine=None):
        self.movie_engine = movie_engine
        self.product_engine = product_engine
        self.course_engine = course_engine

    def resolve_api_key(self, custom_key: Optional[str] = None) -> Optional[str]:
        """Resolves the Gemini API key from explicit arg, env var, Streamlit session state, .env, or secrets."""
        if custom_key and custom_key.strip():
            return custom_key.strip()

        # Check explicit GEMINI_API_KEY environment variable first
        if os.environ.get("GEMINI_API_KEY") and os.environ.get("GEMINI_API_KEY").strip():
            return os.environ.get("GEMINI_API_KEY").strip()

        # Check local .env files next (so project .env takes precedence over stale OS environment)
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for env_path in [".env", os.path.join(root_dir, ".env")]:
            try:
                if os.path.exists(env_path):
                    with open(env_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith(("GEMINI_API_KEY=", "GOOGLE_API_KEY=")):
                                k = line.split("=", 1)[1].strip().strip('"').strip("'")
                                if k:
                                    return k
            except Exception:
                pass

        # Check .streamlit/secrets.toml
        for sec_path in [".streamlit/secrets.toml", os.path.join(root_dir, ".streamlit", "secrets.toml")]:
            try:
                if os.path.exists(sec_path):
                    with open(sec_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if any(line.startswith(p) for p in ["GEMINI_API_KEY", "GOOGLE_API_KEY"]) and "=" in line:
                                k = line.split("=", 1)[1].strip().strip('"').strip("'")
                                if k:
                                    return k
            except Exception:
                pass

        try:
            import streamlit as st
            if "gemini_api_key" in st.session_state and st.session_state["gemini_api_key"]:
                return st.session_state["gemini_api_key"].strip()
            if hasattr(st, "secrets"):
                for var in ["GEMINI_API_KEY", "GOOGLE_API_KEY"]:
                    if var in st.secrets and st.secrets[var]:
                        return st.secrets[var].strip()
        except Exception:
            pass

        # Check system GOOGLE_API_KEY if present
        if os.environ.get("GOOGLE_API_KEY") and os.environ.get("GOOGLE_API_KEY").strip():
            return os.environ.get("GOOGLE_API_KEY").strip()

        return None

    def fetch_live_web_knowledge(self, query: str) -> Optional[str]:
        """
        Fetches live open web knowledge using Wikipedia search and summary/extract APIs.
        Provides up-to-date real-world facts for questions, cinema, technologies, and concepts.
        """
        import urllib.request
        import urllib.parse
        import json

        q = query.strip()
        if q in _WEB_KNOWLEDGE_CACHE:
            return _WEB_KNOWLEDGE_CACHE[q]

        # Never query Wikipedia for bot identity, greetings, pleasantries, or chat
        q_lower = q.lower()
        conversational_phrases = [
            "who are", "who r", "who is recom", "what are you", "your name",
            "who made", "who created", "yourself", "who are ypu", "what is recom",
            "what can you do", "introduce yourself", "about you", "how are you",
            "how are u", "how r u", "how do you do", "how is it going", "hows it going",
            "how you doing", "what's up", "whats up", "sup", "hi", "hello", "hey",
            "good morning", "good evening", "good afternoon", "thank you", "thanks"
        ]
        if any(k in q_lower for k in conversational_phrases) and len(q_lower.split()) <= 8:
            _WEB_KNOWLEDGE_CACHE[q] = None
            return None

        search_topic = q
        # Clean conversational question prefixes for higher search relevance
        clean_q = re.sub(
            r'^(is|are|what is|what are|why is|why are|explain|tell me about|how does|how do|who is|who was|can you explain|difference between)\s+',
            '',
            q,
            flags=re.I
        ).strip().rstrip('?').strip()
        if clean_q:
            search_topic = clean_q

        if "2025" in q.lower() or "2026" in q.lower() or "upcoming" in q.lower():
            if "bollywood" in q.lower() or "hindi" in q.lower():
                search_topic = "List of Hindi films of 2025"
            elif "hollywood" in q.lower() or "english" in q.lower():
                search_topic = "List of American films of 2025"
            elif "tollywood" in q.lower() or "telugu" in q.lower() or "south" in q.lower():
                search_topic = "List of Indian films of 2025"

        headers = {"User-Agent": "RECOM_AI_Concierge/1.0 (contact@recom.ai)"}
        try:
            search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(search_topic)}&format=json"
            req = urllib.request.Request(search_url, headers=headers)
            with urllib.request.urlopen(req, timeout=2.0) as r:
                data = json.loads(r.read().decode("utf-8"))
                results = data.get("query", {}).get("search", [])
                if not results:
                    _WEB_KNOWLEDGE_CACHE[q] = None
                    return None
                best_title = results[0]["title"]

                # Relevance check: discard random acronyms (e.g. "who are ypu" matching "Yale Political Union")
                topic_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', search_topic.lower())) - {
                    "what", "which", "about", "tell", "from", "with", "this", "that", "does", "have", "been"
                }
                title_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', best_title.lower()))
                if topic_words and not (topic_words & title_words):
                    _WEB_KNOWLEDGE_CACHE[q] = None
                    return None

            # Query the rich full introductory extract for the best matching topic
            extract_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=1&explaintext=1&redirects=1&titles={urllib.parse.quote(best_title)}"
            req2 = urllib.request.Request(extract_url, headers=headers)
            with urllib.request.urlopen(req2, timeout=2.0) as r2:
                data2 = json.loads(r2.read().decode("utf-8"))
                pages = data2.get("query", {}).get("pages", {})
                for pid, p in pages.items():
                    if pid != "-1":
                        extract = p.get("extract", "").strip()
                        if extract and len(extract) > 40:
                            res_str = f"**{best_title}**\n\n{extract}"
                            _WEB_KNOWLEDGE_CACHE[q] = res_str
                            return res_str

            # Fallback to snippets if extract was empty
            snippets = []
            for item in results[:3]:
                title = item.get("title", "")
                raw_snip = item.get("snippet", "")
                clean_snip = re.sub(r'<[^>]+>', '', raw_snip).strip()
                if title and clean_snip and not title.lower().startswith("file:"):
                    snippets.append(f"• **{title}**: {clean_snip}...")
            if snippets:
                res_str = "\n\n".join(snippets)
                _WEB_KNOWLEDGE_CACHE[q] = res_str
                return res_str
        except Exception as e:
            logger.debug(f"Web knowledge fetch error: {e}")
            _WEB_KNOWLEDGE_CACHE[q] = None
            return None
        _WEB_KNOWLEDGE_CACHE[q] = None
        return None

    def search_movies(
        self,
        query: str = "",
        industry: str = "All",
        genres: List[str] = None,
        count: int = 3,
        sort_by_year: bool = False,
        min_year: Optional[int] = None,
        exclude_ids: Optional[set] = None
    ) -> List[Dict[str, Any]]:
        """Query movie recommender engine with temporal, genre filtering, and exclusion of seen items."""
        if not self.movie_engine:
            return []
        try:
            fetch_count = count + (len(exclude_ids) if exclude_ids else 0) + 4
            recs = self.movie_engine.recommend(
                selected_genres=genres or [],
                industry=industry,
                query_text=query,
                top_n=fetch_count,
                alpha=0.6,
                min_year=min_year,
                sort_by_year=sort_by_year
            )
            if exclude_ids:
                clean_recs = []
                for r in recs:
                    r_id = str(r.get("id", ""))
                    r_title = str(r.get("title", "")).lower().strip()
                    if r_id not in exclude_ids and r_title not in exclude_ids:
                        clean_recs.append(r)
                if len(clean_recs) >= count:
                    return clean_recs[:count]
                return (clean_recs + [r for r in recs if r not in clean_recs])[:count]
            return recs[:count]
        except Exception as e:
            logger.warning(f"Error querying movie engine: {e}")
            return []

    def search_products(
        self,
        query: str = "",
        category: str = "All",
        max_price: Optional[int] = None,
        brand: str = "All",
        count: int = 3,
        exclude_ids: Optional[set] = None
    ) -> List[Dict[str, Any]]:
        """Query product recommender engine with budget filtering and exclusion of seen items."""
        if not self.product_engine:
            return []
        try:
            fetch_count = count + (len(exclude_ids) if exclude_ids else 0) + 4
            recs = self.product_engine.recommend(
                category=category,
                max_price_inr=max_price,
                brand=brand,
                query_text=query,
                top_n=fetch_count,
                alpha=0.6
            )
            if exclude_ids:
                clean_recs = []
                for r in recs:
                    r_id = str(r.get("id", ""))
                    r_name = str(r.get("name", "")).lower().strip()
                    if r_id not in exclude_ids and r_name not in exclude_ids:
                        clean_recs.append(r)
                if len(clean_recs) >= count:
                    return clean_recs[:count]
                return (clean_recs + [r for r in recs if r not in clean_recs])[:count]
            return recs[:count]
        except Exception as e:
            logger.warning(f"Error querying product engine: {e}")
            return []

    def search_courses(
        self,
        query: str = "",
        domain: str = "All",
        difficulty: str = "All",
        count: int = 3,
        exclude_ids: Optional[set] = None
    ) -> List[Dict[str, Any]]:
        """Query course recommender engine with skill filtering and exclusion of seen items."""
        if not self.course_engine:
            return []
        try:
            fetch_count = count + (len(exclude_ids) if exclude_ids else 0) + 4
            recs = self.course_engine.recommend(
                category=domain,
                difficulty=difficulty,
                desired_skills=query,
                top_n=fetch_count,
                alpha=0.6
            )
            if exclude_ids:
                clean_recs = []
                for r in recs:
                    r_id = str(r.get("id", ""))
                    r_title = str(r.get("title", "")).lower().strip()
                    if r_id not in exclude_ids and r_title not in exclude_ids:
                        clean_recs.append(r)
                if len(clean_recs) >= count:
                    return clean_recs[:count]
                return (clean_recs + [r for r in recs if r not in clean_recs])[:count]
            return recs[:count]
        except Exception as e:
            logger.warning(f"Error querying course engine: {e}")
            return []

    def _extract_conversation_state(self, chat_history: Optional[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Analyzes multi-turn conversation history to extract active domain,
        established industry/category, previous constraints, and previously recommended items.
        """
        state = {
            "last_domain": None,
            "last_movie_industry": None,
            "last_movie_genres": [],
            "last_movie_year_filter": None,
            "last_product_category": None,
            "last_product_budget": None,
            "last_course_domain": None,
            "last_course_difficulty": None,
            "last_items": [],
            "seen_item_ids": set(),
            "turns_count": 0
        }
        if not chat_history:
            return state

        # Strip off trailing message if it's the current user query being processed
        history_msgs = list(chat_history)
        if history_msgs and history_msgs[-1].get("role") == "user":
            prior_msgs = history_msgs[:-1]
        else:
            prior_msgs = history_msgs

        if not prior_msgs:
            return state

        state["turns_count"] = len([m for m in prior_msgs if m.get("role") == "user"])

        # Scan backwards to get the most recent contextual states
        for m in reversed(prior_msgs):
            m_role = m.get("role")
            m_content = (m.get("content") or "").strip()
            m_items = m.get("items") or []

            # Track seen items to prevent repeating recommendations across turns
            for itm in m_items:
                if itm.get("id"):
                    state["seen_item_ids"].add(str(itm["id"]))
                if itm.get("title"):
                    state["seen_item_ids"].add(str(itm["title"]).lower().strip())
                if itm.get("name"):
                    state["seen_item_ids"].add(str(itm["name"]).lower().strip())

            if not state["last_items"] and m_items:
                state["last_items"] = list(m_items)
                types = [i.get("type") for i in m_items if i.get("type")]
                if types:
                    first_type = types[0]
                    if first_type == "Movie":
                        state["last_domain"] = state["last_domain"] or "Movies"
                        inds = [i.get("industry") for i in m_items if i.get("industry")]
                        if inds and not state["last_movie_industry"]:
                            state["last_movie_industry"] = inds[0]
                    elif first_type == "Product":
                        state["last_domain"] = state["last_domain"] or "Products"
                        cats = [i.get("category") for i in m_items if i.get("category")]
                        if cats and not state["last_product_category"]:
                            state["last_product_category"] = cats[0]
                    elif first_type == "Course":
                        state["last_domain"] = state["last_domain"] or "Courses"
                        cats = [i.get("category") for i in m_items if i.get("category")]
                        if cats and not state["last_course_domain"]:
                            state["last_course_domain"] = cats[0]

            # Also check user messages for explicit signals
            if m_role == "user" and m_content:
                u_text = m_content.lower()
                if any(w in u_text for w in ["bollywood", "hindi"]) and not state["last_movie_industry"]:
                    state["last_movie_industry"] = "Bollywood"
                    state["last_domain"] = state["last_domain"] or "Movies"
                elif any(w in u_text for w in ["tollywood", "telugu", "south"]) and not state["last_movie_industry"]:
                    state["last_movie_industry"] = "Tollywood"
                    state["last_domain"] = state["last_domain"] or "Movies"
                elif "nepali" in u_text and not state["last_movie_industry"]:
                    state["last_movie_industry"] = "Nepali Cinema"
                    state["last_domain"] = state["last_domain"] or "Movies"
                elif any(w in u_text for w in ["hollywood", "english"]) and not state["last_movie_industry"]:
                    state["last_movie_industry"] = "Hollywood"
                    state["last_domain"] = state["last_domain"] or "Movies"

                if any(w in u_text for w in ["2025", "2026", "new", "upcoming"]) and not state["last_movie_year_filter"]:
                    state["last_movie_year_filter"] = 2025

                if any(w in u_text for w in ["earbud", "headphone", "audio", "sound"]) and not state["last_product_category"]:
                    state["last_product_category"] = "Audio"
                    state["last_domain"] = state["last_domain"] or "Products"
                elif any(w in u_text for w in ["watch", "watches", "titan", "rolex", "casio"]) and not state["last_product_category"]:
                    state["last_product_category"] = "Watches"
                    state["last_domain"] = state["last_domain"] or "Products"

                b_m = re.search(r'(?:under|below|less than|max|₹|rs\.?)\s*(\d{3,6})', u_text)
                if b_m and not state["last_product_budget"]:
                    try:
                        state["last_product_budget"] = int(b_m.group(1))
                    except Exception:
                        pass

                if not state["last_movie_genres"]:
                    g_found = []
                    genre_map = {
                        "Comedy": ["comedy", "comedies", "funny", "humor"],
                        "Action": ["action"],
                        "Thriller": ["thriller", "suspense"],
                        "Horror": ["horror", "scary"],
                        "Romance": ["romance", "romantic", "love"],
                        "Sci-Fi": ["sci-fi", "science fiction", "scifi", "space"],
                        "Crime": ["crime", "dacoit", "heist", "mafia"],
                        "Drama": ["drama"],
                        "Adventure": ["adventure"],
                        "Animation": ["animation", "animated"]
                    }
                    for g_name, kws in genre_map.items():
                        if any(re.search(rf"\b{kw}\b", u_text) for kw in kws):
                            g_found.append(g_name)
                    if g_found:
                        state["last_movie_genres"] = g_found

                if any(w in u_text for w in ["ai", "machine learning", "deep learning"]) and not state["last_course_domain"]:
                    state["last_course_domain"] = "Artificial Intelligence"
                    state["last_domain"] = state["last_domain"] or "Courses"
                elif any(w in u_text for w in ["data science", "analytics"]) and not state["last_course_domain"]:
                    state["last_course_domain"] = "Data Science"
                    state["last_domain"] = state["last_domain"] or "Courses"

        return state

    def _detect_meta_question(self, text: str) -> Optional[str]:
        """Detects if the user is asking a question about the chatbot, algorithms, or past responses."""
        t = text.lower().strip()
        # Inquiring why same movies, why old movies, or why chatbot isn't answering
        if any(phrase in t for phrase in [
            "why the chatbot", "why is the chatbot", "why is it showing same",
            "showing same", "high rated movie all the time", "same high rated",
            "all the time", "answer the question of the user", "answer my question",
            "why old movies", "why not new", "why not giving", "not giving the result",
            "not showing new", "same movie", "same movies", "why always same"
        ]):
            return "why_old_same_movies"
        if any(phrase in t for phrase in [
            "depend on the data", "depend on dataset", "data from the web",
            "what about 2025", "answer using the data from the web", "latest information from the web",
            "not depend wholey", "not depend solely", "not depend on the data", "answer using the web"
        ]):
            return "web_and_2025_policy"
        if t.startswith(("why ", "how does ", "how do ", "what is ", "what are ", "explain ")):
            if any(w in t for w in ["your algorithm", "recommendation algorithm", "how recom works", "how do recommendations work", "how does your system work", "how does this app work"]):
                return "how_it_works"
            if any(w in t for w in ["inr", "rupee", "pricing", "cost of product"]):
                return "pricing_inr"
        return None

    def _is_explicit_recommendation_request(self, text: str) -> bool:
        """Determines if the user is explicitly asking for concrete recommendations or item suggestions."""
        t = text.lower().strip()
        rec_patterns = [
            r'\b(recommend|recommendation|recommendations|suggest|suggestion|suggestions)\b',
            r'\b(give me|show me|find me|list of|top \d+|best \d+|best of|give recommendations)\b',
            r'\b(what should i watch|which movie should i|what movies to watch|films to watch)\b',
            r'\b(buy|purchase|shop for|under \d+|below \d+|price under|budget under)\b',
            r'\b(which (course|product|movie|smartwatch|headphone|earbud) should i)\b',
            r'\b(courses? to learn|certifications? for|best courses?|top courses?)\b',
            r'\b(what are some good|any good (movies|courses|products|gadgets|headphones))\b'
        ]
        return any(re.search(pat, t) for pat in rec_patterns)

    def _is_conversational_or_conceptual_query(self, text: str) -> bool:
        """Determines if the user is asking an informative, conceptual, or conversational question."""
        t = text.lower().strip()
        if self._is_explicit_recommendation_request(t):
            return False

        # Explicit follow-up inquiries that should NOT be treated as conversational Wikipedia queries
        if any(p in t for p in [
            "what about", "how about", "what are some good", "which one", "which of these",
            "what should i", "tell me more about the first", "tell me more about the second",
            "show more", "give more", "different ones", "i like", "i prefer", "under "
        ]) or (
            any(ind in t for ind in ["bollywood", "hollywood", "tollywood", "nepali"]) and
            any(m in t for m in ["movie", "movies", "film", "films"])
        ) or any(p in t for p in ["product", "products", "gadget", "gadgets", "earbud", "earbuds", "headphone", "headphones", "smartwatch"]):
            return False

        question_starters = [
            r'^(is|are|was|were|do|does|did|can|could|will|would|should|may|might)\b',
            r'^(what|why|how|who|where|when)\b',
            r'^(tell me about|explain|describe|discuss|elaborate|give information on|what do you think about)\b'
        ]
        is_q_starter = any(re.search(pat, t) for pat in question_starters)
        ends_with_qmark = t.endswith("?")

        conceptual_terms = [
            "important", "importance", "future of", "impact", "difference between",
            "how does", "how do", "why is", "why are", "what is", "what are",
            "pros and cons", "advantages", "benefits", "meaning", "concept",
            "replace", "job market", "career advice", "worth it", "better than",
            "significance", "overview", "history of"
        ]
        has_conceptual = any(term in t for term in conceptual_terms)

        return is_q_starter or ends_with_qmark or has_conceptual

    def extract_intent_and_items(self, user_text: str, chat_history: Optional[List[Dict[str, Any]]] = None) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Extracts user intent, domain targets, and queries catalog items with multi-turn memory."""
        conv_state = self._extract_conversation_state(chat_history)
        text = user_text.lower()
        items = []
        meta = {
            "domains": [],
            "keywords": [],
            "budget": None,
            "is_greeting": False,
            "is_meta_question": False,
            "is_conversational": False,
            "meta_type": None,
            "movie_genres": [],
            "is_new_movie": False,
            "industry_label": "All",
            "is_followup": False,
            "is_item_inquiry": False,
            "referred_item": None,
            "inherited_industry": None,
            "inherited_domain": None,
            "conversation_context": conv_state
        }

        # 0. Check if user is referencing a specific item from the previous response
        if conv_state.get("last_items"):
            last_itms = conv_state["last_items"]
            matched_ref = None
            if re.search(r'\b(first|1st|number\s*1|#1)\b', text):
                matched_ref = last_itms[0]
            elif re.search(r'\b(second|2nd|number\s*2|#2)\b', text) and len(last_itms) >= 2:
                matched_ref = last_itms[1]
            elif re.search(r'\b(third|3rd|number\s*3|#3)\b', text) and len(last_itms) >= 3:
                matched_ref = last_itms[2]
            elif re.search(r'\b(last|final)\b', text):
                matched_ref = last_itms[-1]
            else:
                for cand in last_itms:
                    c_title = cand.get("title") or cand.get("name") or ""
                    clean_cand = re.sub(r'\s*\(\d{4}\)', '', c_title).strip().lower()
                    if clean_cand and len(clean_cand) >= 4 and clean_cand in text:
                        matched_ref = cand
                        break

            if matched_ref and any(k in text for k in [
                "tell me more", "about", "story", "plot", "details", "explain", "watch", "buy", "review",
                "rating", "price", "how is", "what is", "more info", "overview"
            ]):
                meta["is_item_inquiry"] = True
                meta["referred_item"] = matched_ref
                itype = matched_ref.get("type", "Item")
                meta["domains"].append(f"{itype}s")
                return [matched_ref], meta

        # Check for greeting, pleasantry, or bot identity question (e.g. "hi, how are you", "who are you")
        text_norm = re.sub(r'\b(ypu|yuo|yu|u)\b', 'you', text)
        text_norm = re.sub(r'\b(r)\b', 'are', text_norm)
        text_norm = re.sub(r'\b(ur)\b', 'your', text_norm)

        # 1. "How are you" / "How's it going" pleasantries
        if any(re.search(rf"\b{re.escape(p)}\b", text_norm) for p in [
            "how are you", "how are u", "how r u", "how do you do", "how is it going",
            "hows it going", "how you doing", "how have you been", "whats up", "what's up",
            "how are things"
        ]) and len(text.split()) <= 8:
            meta["is_greeting"] = True
            meta["greeting_type"] = "how_are_you"
            return items, meta

        # 2. General greetings and identity questions
        identity_patterns = [
            "who are you", "what are you", "what is your name", "who made you",
            "who created you", "what can you do", "help", "hi", "hello", "hey",
            "good morning", "good afternoon", "good evening", "namaste",
            "who is recom", "what is recom", "introduce yourself", "tell me about yourself",
            "about you", "what do you do", "nice to meet you"
        ]
        if any(re.search(rf"\b{re.escape(p)}\b", text_norm) for p in identity_patterns) and len(text.split()) <= 8:
            meta["is_greeting"] = True
            meta["greeting_type"] = "who_are_you"
            return items, meta

        # 3. Gratitude & pleasantry
        if any(re.search(rf"\b{re.escape(p)}\b", text_norm) for p in ["thank you", "thanks", "thank u", "thx", "appreciate it"]) and len(text.split()) <= 6:
            meta["is_thanks"] = True
            return items, meta

        # Check for meta-question or feedback
        meta_q = self._detect_meta_question(user_text)
        if meta_q == "why_old_same_movies":
            meta["is_meta_question"] = True
            meta["meta_type"] = "why_old_same_movies"
            meta["domains"].append("Movies")
            # Fetch the actual newest comedies from Bollywood and Hollywood
            b_items = self.search_movies(query="", industry="Bollywood", genres=["Comedy"], count=2, sort_by_year=True)
            h_items = self.search_movies(query="", industry="Hollywood", genres=["Comedy"], count=2, sort_by_year=True)
            for r in b_items + h_items:
                r["type"] = "Movie"
            items.extend(b_items + h_items)
            return items, meta
        elif meta_q == "how_it_works":
            meta["is_meta_question"] = True
            meta["meta_type"] = "how_it_works"
            return items, meta
        elif meta_q == "pricing_inr":
            meta["is_meta_question"] = True
            meta["meta_type"] = "pricing_inr"
            return items, meta
        elif meta_q == "web_and_2025_policy":
            meta["is_meta_question"] = True
            meta["meta_type"] = "web_and_2025_policy"
            meta["domains"].append("Movies")
            b_2025 = self.search_movies(query="", industry="Bollywood", count=2, sort_by_year=True, min_year=2025)
            h_2025 = self.search_movies(query="", industry="Hollywood", count=2, sort_by_year=True, min_year=2025)
            for r in b_2025 + h_2025:
                r["type"] = "Movie"
            items.extend(b_2025 + h_2025)
            meta["web_knowledge"] = self.fetch_live_web_knowledge("2025 in film")
            return items, meta

        # Check if user is asking an informational, conceptual, or conversational question
        if self._is_conversational_or_conceptual_query(user_text):
            meta["is_conversational"] = True
            meta["web_knowledge"] = self.fetch_live_web_knowledge(user_text)
            return [], meta

        # Define common transition & filler words regex to strip from search queries
        TRANSITION_STOPWORDS_PATTERN = (
            r'\b(now|then|further|furthermore|after|sometime|later|next|also|instead|rather|'
            r'shift|shifting|switch|switching|change|changing|move|moving|turn|tell|ask|asking|'
            r'what|how|about|can|could|would|you|me|i|give|show|suggest|recommend|find|'
            r'any|some|all|few|a|an|the|of|for|to|in|from|with|or|and|please|as|well|too|'
            r'respectively|respective|domain|convo|conversation|topic)\b'
        )

        last_domain = conv_state.get("last_domain")
        last_movie_industry = conv_state.get("last_movie_industry")
        last_product_category = conv_state.get("last_product_category")
        last_course_domain = conv_state.get("last_course_domain")

        # 1. Signal Detection Across Domains
        is_watch_product = bool(re.search(
            r'\b(watches|smartwatch|smartwatches|wrist\s*watch(es)?|titan|rolex|casio|fossil|hmt|noise)\b', text
        ))

        has_movie_explicit = bool(re.search(
            r'\b(movie|movies|cinema|film|films|bollywood|hollywood|tollywood|nepali|actor|actress|director|stream|binge)\b', text
        )) or bool(re.search(r'\b(to\s+watch|watch\s+(a\s+)?(movie|film|cinema|show))\b', text))

        has_product_explicit = bool(re.search(
            r'\b(product|products|prouduct|prouducts|gadget|gadgets|buy|shop|gear|headphone|headphones|earbud|earbuds|'
            r'earphone|earphones|audio|perfume|fragrance|scent|keyboard|mouse|wearable|wearables|smartwatch|smartwatches|'
            r'rupee|inr|₹|boat|noise|titan)\b', text
        )) or is_watch_product or bool(re.search(r'\b(under|below|less than)\s*\d{3,6}\b', text))

        has_course_explicit = bool(re.search(
            r'\b(course|courses|learn|study|certif|certification|certifications|career|roadmap|curriculum|syllabus|degree|bootcamp|training)\b', text
        ))

        has_tech_skill = bool(re.search(
            r'\b(python|machine\s*learning|ml|ai|artificial\s*intelligence|deep\s*learning|data\s*science|cloud|aws|azure|cybersecurity|full\s*stack|web\s*dev)\b', text
        ))

        has_genre_signal = bool(re.search(
            r'\b(action|thriller|comedy|comedies|romance|romantic|horror|drama|sci-fi|scifi|crime|heist|adventure|animation|animated)\b', text
        )) and not is_watch_product

        # 2. Determine Target Domains for Current Request
        target_domains = []
        if has_movie_explicit:
            target_domains.append("Movies")
        if has_product_explicit:
            target_domains.append("Products")
        if has_course_explicit:
            target_domains.append("Courses")

        # If user mentioned technical skills without explicit movie/product keywords
        if has_tech_skill and "Courses" not in target_domains and not has_movie_explicit and not has_product_explicit:
            target_domains.append("Courses")

        # If no explicit domain signal, determine from multi-turn context
        if not target_domains:
            if has_genre_signal and last_domain == "Movies":
                target_domains.append("Movies")
            elif has_tech_skill and last_domain == "Courses":
                target_domains.append("Courses")
            elif last_domain:
                # Continuation of last domain if query is a follow-up refinement
                target_domains.append(last_domain)
            elif has_genre_signal:
                target_domains.append("Movies")

        # 3. Detect Explicit Domain Shift
        is_domain_shift = False
        if last_domain and target_domains and last_domain not in target_domains:
            is_domain_shift = True
            shift_from_domain = last_domain
            shift_to_domain = target_domains[0]
            meta["is_shift"] = True
            meta["shift_type"] = "domain_shift"
            meta["shift_from"] = "Cinema" if shift_from_domain == "Movies" else shift_from_domain
            meta["shift_to"] = "Cinema" if shift_to_domain == "Movies" else ("Products & Tech" if shift_to_domain == "Products" else "Courses & Skills")

        # 4. Process Target Domain Recommendations

        # --- A. MOVIE DOMAIN ---
        if "Movies" in target_domains:
            is_new = bool(re.search(r'\b(new|latest|recent|current|modern|fresh|202[0-9]|201[8-9])\b', text)) or (conv_state.get("last_movie_year_filter") == 2025 and not is_domain_shift)
            meta["is_new_movie"] = is_new

            # Genre detection in current query
            detected_genres = []
            genre_map = {
                "Comedy": ["comedy", "comedies", "funny", "humor"],
                "Action": ["action"],
                "Thriller": ["thriller", "suspense"],
                "Horror": ["horror", "scary"],
                "Romance": ["romance", "romantic", "love"],
                "Sci-Fi": ["sci-fi", "science fiction", "scifi", "space"],
                "Crime": ["crime", "dacoit", "heist", "mafia"],
                "Drama": ["drama"],
                "Adventure": ["adventure"],
                "Animation": ["animation", "animated"]
            }
            for g_name, kws in genre_map.items():
                if any(re.search(rf"\b{kw}\b", text) for kw in kws):
                    detected_genres.append(g_name)

            # Industry detection in current query
            has_hollywood = "hollywood" in text or "english" in text
            has_bollywood = "bollywood" in text or "hindi" in text
            has_nepali = "nepali" in text
            has_tollywood = "tollywood" in text or "telugu" in text or "south" in text

            # Industry resolution & Industry Shift check
            industry = "All"
            is_industry_shift = False
            if has_hollywood and has_bollywood:
                meta["industry_label"] = "Hollywood & Bollywood"
                industry = "Hollywood & Bollywood"
            elif has_nepali:
                industry = "Nepali Cinema"
            elif has_bollywood:
                industry = "Bollywood"
            elif has_tollywood:
                industry = "Tollywood"
            elif has_hollywood:
                industry = "Hollywood"
            elif not is_domain_shift and last_movie_industry:
                industry = last_movie_industry
                meta["is_followup"] = True
                meta["inherited_industry"] = industry

            if (
                last_movie_industry
                and industry not in ["All", "Hollywood & Bollywood"]
                and industry != last_movie_industry
                and not is_domain_shift
            ):
                is_industry_shift = True
                meta["is_shift"] = True
                meta["shift_type"] = "industry_shift"
                meta["shift_from"] = f"{last_movie_industry} Cinema"
                meta["shift_to"] = f"{industry} Cinema"

            # In shifts, do NOT inherit old genres unless user explicitly mentioned them
            if not detected_genres and not is_industry_shift and not is_domain_shift and meta.get("is_followup"):
                detected_genres = conv_state.get("last_movie_genres") or []

            meta["movie_genres"] = detected_genres
            meta["industry_label"] = industry

            # Clean query: strip transition stopwords and cinema keywords
            clean_query = re.sub(TRANSITION_STOPWORDS_PATTERN, ' ', text, flags=re.I)
            clean_query = re.sub(
                r'\b(like|love|prefer|want|ones?|good|best|top|new|latest|recent|movies?|films?|cinema|to\s+watch|watch|hollywood|bollywood|tollywood|nepali|comedy|action|thriller|horror|romance|crime|drama|scifi|sci-fi|animated|animation)\b',
                ' ',
                clean_query,
                flags=re.I
            )
            clean_query = re.sub(r'\s+', ' ', clean_query).strip()

            is_2025 = bool(re.search(r'\b(2025|2026|upcoming|future)\b', text)) or (conv_state.get("last_movie_year_filter") == 2025 and not is_domain_shift and not any(k in text for k in ["classic", "old", "vintage", "90s"]))
            min_yr = 2025 if is_2025 else (2024 if is_new else None)

            if industry == "Hollywood & Bollywood":
                b_recs = self.search_movies(query=clean_query, industry="Bollywood", genres=detected_genres, count=2, sort_by_year=is_new, min_year=min_yr, exclude_ids=conv_state.get("seen_item_ids"))
                h_recs = self.search_movies(query=clean_query, industry="Hollywood", genres=detected_genres, count=2, sort_by_year=is_new, min_year=min_yr, exclude_ids=conv_state.get("seen_item_ids"))
                for r in b_recs + h_recs:
                    r["type"] = "Movie"
                items.extend(b_recs + h_recs)
            else:
                recs = self.search_movies(query=clean_query, industry=industry, genres=detected_genres, count=3, sort_by_year=is_new, min_year=min_yr, exclude_ids=conv_state.get("seen_item_ids"))
                for r in recs:
                    r["type"] = "Movie"
                items.extend(recs)

            if is_2025 or "web" in text or "internet" in text or "latest" in text:
                meta["web_knowledge"] = self.fetch_live_web_knowledge(user_text)

            meta["domains"].append("Movies")

        # --- B. PRODUCT DOMAIN ---
        if "Products" in target_domains:
            category = "All"
            is_cat_shift = False
            if any(w in text for w in ["headphone", "headphones", "earphone", "earphones", "audio", "earbud", "earbuds", "anc", "bass", "sound"]):
                category = "Audio"
            elif any(w in text for w in ["smartwatch", "smartwatches", "wearable", "wearables", "band"]):
                category = "Wearables"
            elif any(w in text for w in ["watch", "watches", "chronograph", "mechanical", "automatic", "titan", "rolex", "casio"]):
                category = "Watches"
            elif any(w in text for w in ["perfume", "fragrance", "scent", "oud", "edp", "cologne"]):
                category = "Fragrance"
            elif any(w in text for w in ["keyboard", "mouse", "desk", "charger", "stand"]):
                category = "Desk Setup"
            elif any(w in text for w in ["gaming", "gamepad"]):
                category = "Gaming"
            elif not is_domain_shift and last_product_category:
                category = last_product_category
                meta["is_followup"] = True

            if (
                last_product_category
                and category != "All"
                and category != last_product_category
                and not is_domain_shift
            ):
                is_cat_shift = True
                meta["is_shift"] = True
                meta["shift_type"] = "category_shift"
                meta["shift_from"] = f"{last_product_category}"
                meta["shift_to"] = f"{category}"

            budget = None
            budget_match = re.search(r'(?:under|below|less than|max|₹|rs\.?)\s*(\d{3,6})', text)
            if budget_match:
                try:
                    budget = int(budget_match.group(1))
                    meta["budget"] = budget
                except Exception:
                    pass
            elif not is_domain_shift and not is_cat_shift and conv_state.get("last_product_budget"):
                budget = conv_state["last_product_budget"]
                meta["budget"] = budget
                meta["is_followup"] = True

            clean_query = re.sub(TRANSITION_STOPWORDS_PATTERN, ' ', text, flags=re.I)
            clean_query = re.sub(
                r'\b(like|love|prefer|want|ones?|good|best|top|products?|prouducts?|gadgets?|items?|buy|shop|under|below|rupees?|rs|inr|\d+)\b',
                ' ',
                clean_query,
                flags=re.I
            )
            clean_query = re.sub(r'\s+', ' ', clean_query).strip()

            recs = self.search_products(query=clean_query, category=category, max_price=budget, count=3, exclude_ids=conv_state.get("seen_item_ids"))
            for r in recs:
                r["type"] = "Product"
            items.extend(recs)
            meta["domains"].append("Products")

        # --- C. COURSE DOMAIN ---
        if "Courses" in target_domains:
            domain = "All"
            if any(w in text for w in ["ai", "artificial intelligence", "deep learning"]):
                domain = "Artificial Intelligence"
            elif any(w in text for w in ["data science", "analytics", "sql"]):
                domain = "Data Science"
            elif any(w in text for w in ["cloud", "aws", "devops", "azure"]):
                domain = "Cloud Computing"
            elif any(w in text for w in ["cyber", "security", "hacking"]):
                domain = "Cybersecurity"
            elif any(w in text for w in ["business", "management", "project", "leadership"]):
                domain = "Business & Management"
            elif any(w in text for w in ["software", "engineering", "coding", "web", "full stack"]):
                domain = "Software Engineering"
            elif not is_domain_shift and last_course_domain:
                domain = last_course_domain
                meta["is_followup"] = True

            difficulty = "All"
            if "beginner" in text or "intro" in text or "start" in text:
                difficulty = "Beginner"
            elif "intermediate" in text:
                difficulty = "Intermediate"
            elif "advanced" in text or "expert" in text:
                difficulty = "Advanced"
            elif not is_domain_shift and conv_state.get("last_course_difficulty"):
                difficulty = conv_state["last_course_difficulty"]

            clean_query = re.sub(TRANSITION_STOPWORDS_PATTERN, ' ', text, flags=re.I)
            clean_query = re.sub(
                r'\b(like|love|prefer|want|ones?|good|best|top|courses?|certifications?|certif|cert|to\s+learn|learn|study|in)\b',
                ' ',
                clean_query,
                flags=re.I
            )
            clean_query = re.sub(r'\s+', ' ', clean_query).strip()

            recs = self.search_courses(query=clean_query, domain=domain, difficulty=difficulty, count=3, exclude_ids=conv_state.get("seen_item_ids"))
            for r in recs:
                r["type"] = "Course"
            items.extend(recs)
            meta["domains"].append("Courses")

        # If nothing specific was caught but user typed something, only search if explicit recommendation was asked
        if not items and not meta["is_greeting"] and len(text.strip()) > 2:
            if self._is_explicit_recommendation_request(text):
                m_res = self.search_movies(query=text, count=1, exclude_ids=conv_state.get("seen_item_ids"))
                p_res = self.search_products(query=text, count=1, exclude_ids=conv_state.get("seen_item_ids"))
                c_res = self.search_courses(query=text, count=1, exclude_ids=conv_state.get("seen_item_ids"))
                for r in m_res:
                    r["type"] = "Movie"
                for r in p_res:
                    r["type"] = "Product"
                for r in c_res:
                    r["type"] = "Course"
                items = m_res + p_res + c_res
            else:
                meta["is_conversational"] = True
                meta["web_knowledge"] = self.fetch_live_web_knowledge(user_text)

        return items, meta

    def generate_intelligent_response(
        self,
        user_text: str,
        items: List[Dict[str, Any]],
        meta: Dict[str, Any],
        chat_history: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Synthesizes an articulate, tailored recommendation and advisory response with conversational memory."""
        text_lower = user_text.lower().strip()

        # 0. Item Spotlight Breakdown (when user asked about a specific item from previous response)
        if meta.get("is_item_inquiry") and meta.get("referred_item"):
            ref_item = meta["referred_item"]
            itype = ref_item.get("type", "Item")
            if itype == "Movie":
                t = ref_item.get("title", "Film")
                ind = ref_item.get("industry", "Cinema")
                g = ", ".join(ref_item.get("genres", []))
                r = ref_item.get("rating", 4.5)
                exp = ref_item.get("explanation", "Outstanding cinematic storytelling.")
                return (
                    f"### 🎬 Spotlight Breakdown: **{t}**\n\n"
                    f"✨ **Here is the complete overview and perspective on {t} ({ind}):**\n\n"
                    f"• **Cinema Industry:** {ind}\n"
                    f"• **IMDb / Rating:** ★ {r:.1f} / 5.0\n"
                    f"• **Genres & Atmosphere:** {g}\n"
                    f"• **Curated Perspective:** {exp}\n\n"
                    f"**Why Watch:** This title represents a benchmark in {ind} cinema in the {g} space. You can click **🎬 Watch Online ↗** on the card below to jump directly to streaming availability!"
                )
            elif itype == "Product":
                n = ref_item.get("name", "Product")
                b = ref_item.get("brand", "Brand")
                cat = ref_item.get("category", "Products")
                p = ref_item.get("price_inr", 1999)
                r = ref_item.get("rating", 4.5)
                exp = ref_item.get("explanation", "Top-rated value and build quality.")
                return (
                    f"### 🛍️ Spec Spotlight: **{n}** by {b}\n\n"
                    f"✨ **Here are the key specs and buying advice for this {cat} pick:**\n\n"
                    f"• **Target Price:** ₹{p:,} INR\n"
                    f"• **Rating:** ★ {r:.1f} / 5.0\n"
                    f"• **Category:** {cat}\n"
                    f"• **Expert Evaluation:** {exp}\n\n"
                    f"Click **🛒 Buy Now ↗** below to check live merchant availability and warranty details!"
                )
            elif itype == "Course":
                t = ref_item.get("title", "Course")
                org = ref_item.get("organization", "Academy")
                diff = ref_item.get("difficulty", "All Levels")
                skills = ", ".join(ref_item.get("skills", [])[:5])
                exp = ref_item.get("explanation", "Comprehensive hands-on curriculum.")
                return (
                    f"### 🎓 Curriculum Spotlight: **{t}**\n\n"
                    f"✨ **Course Overview provided by {org}:**\n\n"
                    f"• **Offered by:** {org}\n"
                    f"• **Skill Level:** {diff}\n"
                    f"• **Core Competencies:** {skills}\n"
                    f"• **Curriculum Highlights:** {exp}\n\n"
                    f"Click **🎓 View Course ↗** below to view syllabus modules and enrollment credentials!"
                )

        if meta.get("is_thanks"):
            return (
                "✨ **You're very welcome!** 😊\n\n"
                "Always glad to help! Feel free to ask anytime if you want to explore more cinema releases, tech gadgets in ₹ INR, or career skill paths."
            )

        if meta.get("is_greeting"):
            if meta.get("greeting_type") == "how_are_you":
                return (
                    "👋 **Hello! I'm doing great, thank you for asking! 😊**\n\n"
                    "I am your **RECOM.ai Concierge**, running smoothly and ready to assist you across:\n\n"
                    "• 🎬 **Cinema & Blockbusters**: Latest 2024–2026 films in Bollywood, Hollywood, Tollywood, and Nepali cinema.\n"
                    "• 🛍️ **Tech & Products**: Noise-cancelling earbuds, smartwatches, Titan/HMT wristwatches, and desk setups in ₹ INR.\n"
                    "• 🎓 **Career & Skills**: Stanford AI/ML specializations, Data Science, Full-Stack, and deep learning roadmaps.\n\n"
                    "How are you doing today, and what would you like to explore?"
                )
            return (
                "🤖 **I am RECOM.ai Concierge!**\n\n"
                "I am your multi-domain conversational AI recommender and intelligent advisor. I specialize in:\n\n"
                "• 🎬 **Cinema & Film Discovery**: Bollywood, Hollywood, Tollywood, and Nepali cinema releases (including latest 2024–2026 films) with IMDb ratings, genres, and storyline matching.\n"
                "• 🛍️ **Smart Products & Workspace Gear**: Audio equipment, noise-cancelling earbuds, smartwatches, mechanical timepieces (Titan, HMT), and tech setups in ₹ INR.\n"
                "• 🎓 **Skill Roadmaps & Career Accelerators**: Top certifications, curricula, and career pathways in AI/ML, Data Science, Full-Stack, and Cloud technologies.\n\n"
                "You can ask me questions about any topic, explore 2025 movies, compare tech gadgets, or plan your career roadmap!"
            )

        # Conversational & Informative Query Synthesizer (Talk directly to user!)
        if meta.get("is_conversational"):
            # 1. Distinctions & Comparison: AI vs Machine Learning vs Deep Learning
            is_comparison_query = any(k in text_lower for k in [
                "difference", "differ", "compare", "comparison", "vs", "versus", "between",
                "hierarchy", "relationship", "how do they relate", "how does ai differ"
            ]) and any(k in text_lower for k in ["ai", "machine learning", "ml", "deep learning", "dl"])

            if is_comparison_query or ("machine learning" in text_lower and "deep learning" in text_lower):
                return (
                    "### 🧠 The Core Distinctions: AI vs. Machine Learning vs. Deep Learning\n\n"
                    "While often used interchangeably in marketing, **Artificial Intelligence**, **Machine Learning**, and **Deep Learning** form a precise **concentric hierarchy**:\n\n"
                    "```\n"
                    "┌─────────────────────────────────────────────────────────────┐\n"
                    "│  🌐 ARTIFICIAL INTELLIGENCE (Broad Discipline)              │\n"
                    "│   ┌─────────────────────────────────────────────────────┐   │\n"
                    "│   │  📊 MACHINE LEARNING (Statistical Learning)         │   │\n"
                    "│   │   ┌─────────────────────────────────────────────┐   │   │\n"
                    "│   │   │  ⚡ DEEP LEARNING (Multi-Layer Neural Nets)  │   │   │\n"
                    "│   │   └─────────────────────────────────────────────┘   │   │\n"
                    "│   └─────────────────────────────────────────────────────┘   │\n"
                    "└─────────────────────────────────────────────────────────────┘\n"
                    "```\n\n"
                    "#### 1. 🌐 Artificial Intelligence (The Broad Umbrella)\n"
                    "• **Definition**: The entire field of computer science dedicated to building computational systems that perform tasks requiring human-like intelligence (reasoning, perception, problem solving, planning).\n"
                    "• **Scope**: Encompasses both non-learning approaches (symbolic logic, expert systems, A* pathfinding search) and learning-based systems.\n\n"
                    "#### 2. 📊 Machine Learning (The Statistical Subfield)\n"
                    "• **Definition**: A subset of AI where systems learn mathematical mappings and decision boundaries directly from data rather than being explicitly rule-programmed.\n"
                    "• **Key Trait**: **Requires human feature engineering**. Data scientists manually extract relevant features (e.g., word frequencies, pixel histograms, financial ratios) before feeding them into algorithms like XGBoost, Random Forests, or SVMs.\n"
                    "• **Best For**: Structured tabular data, credit scoring, churn prediction, and low-latency classification.\n\n"
                    "#### 3. ⚡ Deep Learning (The Neural Network Revolution)\n"
                    "• **Definition**: A specialized branch of ML inspired by biological brain structures, utilizing **deep multi-layered Artificial Neural Networks** (ANNs, CNNs, Transformers).\n"
                    "• **Key Trait**: **Automated Representation Learning**. DL models discover and extract hierarchical features on their own directly from raw, unstructured data (raw pixels, audio waveforms, text tokens).\n"
                    "• **Best For**: Computer vision, natural language processing, LLMs (GPT, Gemini), autonomous driving, and speech synthesis.\n\n"
                    "#### ⚖️ Technical Comparison Matrix\n"
                    "| Dimension | Machine Learning (Traditional) | Deep Learning |\n"
                    "| :--- | :--- | :--- |\n"
                    "| **Feature Extraction** | Manually engineered by experts | Learned end-to-end automatically |\n"
                    "| **Data Volume** | Performs well on small-to-medium datasets | Requires massive scale to avoid overfitting |\n"
                    "| **Hardware Needs** | Standard multicore CPUs | High-throughput GPU / TPU accelerators |\n"
                    "| **Interpretability** | High (feature importance, decision trees) | 'Black-box' complex latent representations |\n"
                    "| **Training Duration** | Minutes to hours | Days to weeks across GPU clusters |\n\n"
                    "---\n"
                    "*Would you like to explore the mathematics behind backpropagation, dive into specific ML algorithms (like XGBoost), or discuss modern Transformer architectures?*"
                )

            # 2. Deep Learning Deep Dive
            if any(k in text_lower for k in ["deep learning", "neural network", "neural networks", "backpropagation", "cnn", "transformer", "transformers", "llm", "llms"]):
                return (
                    "### ⚡ Deep Learning: Multi-Layer Neural Architectures & Representation\n\n"
                    "**Deep Learning (DL)** is a paradigm of machine learning centered on stacking multiple layers of non-linear transformations to automatically discover representations from raw sensory data.\n\n"
                    "#### 1. How Deep Networks Learn (The Mechanics)\n"
                    "• **Artificial Neurons (Perceptrons)**: Compute a linear weighted combination of inputs plus bias ($z = \\sum w_i x_i + b$) passed through non-linear activation functions (ReLU, GELU, Sigmoid) to enable arbitrary function approximation.\n"
                    "• **Forward Pass & Loss Computation**: Data flows forward through successive latent layers to generate predictions, evaluated against ground truth via loss functions (e.g., Cross-Entropy, Mean Squared Error).\n"
                    "• **Backpropagation & Optimization**: By applying the calculus chain rule, the network calculates the partial derivative of the error with respect to every weight, updating parameters via gradient descent optimizers (AdamW, SGD) to minimize loss.\n\n"
                    "#### 2. Milestone Architectures\n"
                    "• **Transformers (Attention is All You Need)**: Multi-Head Self-Attention mechanisms compute contextual relationships between tokens globally in parallel, serving as the backbone for modern LLMs (GPT, Gemini) and Vision Transformers (ViT).\n"
                    "• **Convolutional Neural Networks (CNNs)**: Use localized kernel convolutions and spatial pooling for translation-invariant computer vision (ResNet, YOLO).\n"
                    "• **Generative Diffusion Models**: Score-based reverse diffusion processes generating high-fidelity visual and audio media.\n\n"
                    "#### 3. Why Deep Learning Rose to Dominance\n"
                    "The breakthrough was catalyzed by the simultaneous convergence of:\n"
                    "1. **Massive Datasets** (ImageNet, Common Crawl, web-scale corpora).\n"
                    "2. **Parallel GPU Hardware** (NVIDIA CUDA tensor cores accelerating matrix multiplications).\n"
                    "3. **Algorithmic Innovations** (Residual skip connections, layer normalization, dropout regularization).\n\n"
                    "---\n"
                    "*What aspect of deep learning would you like to explore next—attention mechanisms, loss landscapes, or fine-tuning techniques?*"
                )

            # 3. Machine Learning Deep Dive
            if any(k in text_lower for k in ["machine learning", "supervised learning", "unsupervised learning", "reinforcement learning", "regression", "clustering", "xgboost", "random forest"]):
                return (
                    "### 📊 Machine Learning: Paradigms, Lifecycle & Statistical Foundations\n\n"
                    "**Machine Learning (ML)** focuses on developing statistical algorithms that generalize from historical data to make accurate inferences on unseen observations without explicit programming.\n\n"
                    "#### 1. The Three Primary Learning Paradigms\n"
                    "• **Supervised Learning**: Model trains on labeled input-output pairs $(X, y)$.\n"
                    "  - *Classification*: Predicting discrete categories (churn prediction, disease diagnosis, spam detection).\n"
                    "  - *Regression*: Predicting continuous numerical quantities (house pricing, stock volatility, sales forecast).\n"
                    "• **Unsupervised Learning**: Discovers intrinsic latent structure, clusters, or manifold distributions without target labels.\n"
                    "  - *Clustering (K-Means, DBSCAN)*: Customer segmentation, anomaly detection.\n"
                    "  - *Dimensionality Reduction (PCA, t-SNE)*: Compression and data visualization.\n"
                    "• **Reinforcement Learning (RL)**: An autonomous agent learns an optimal behavioral policy $\\pi(a|s)$ via trial-and-error environmental interactions to maximize cumulative discounted rewards.\n\n"
                    "#### 2. The Core Machine Learning Workflow\n"
                    "1. **Exploratory Data Analysis (EDA)**: Inspecting distributions, collinearity, skewness, and outliers.\n"
                    "2. **Feature Engineering**: Imputing null values, encoding categoricals (One-Hot, Target Encoding), feature scaling (StandardScaler), and polynomial interactions.\n"
                    "3. **Managing Bias-Variance Tradeoff**: Preventing **overfitting** (high variance) using L1/L2 regularization (Lasso/Ridge), tree pruning, and k-fold cross-validation.\n"
                    "4. **Evaluation**: Assessing precision, recall, F1-score, ROC-AUC, or MAE/RMSE depending on business asymmetry.\n\n"
                    "---\n"
                    "*Would you like to discuss a specific algorithm, feature engineering pipeline, or practical implementation in Python?*"
                )

            # 4. Importance, Societal Impact & Future of AI
            if any(k in text_lower for k in ["important", "importance", "why ai", "future of ai", "impact of ai", "replace jobs", "why is ai"]):
                return (
                    "### 🤖 The Critical Importance & Societal Impact of AI\n\n"
                    "Yes, **Artificial Intelligence is profoundly important**—arguably the defining general-purpose technology of our era, on par with the discovery of electricity or the invention of the internet. It is transitioning from experimental research into foundational infrastructure across global industry, science, and everyday life.\n\n"
                    "Here is a comprehensive breakdown of why AI matters so critically today:\n\n"
                    "#### 1. ⚡ Cognitive Automation & Supercharged Productivity\n"
                    "• **Shifting Human Labor**: Rather than merely automating physical manual labor, modern AI automates complex cognitive friction—synthesizing legal briefs, writing boilerplate code, analyzing market data, and translating languages in real time.\n"
                    "• **Focus on High-Leverage Strategy**: By eliminating routine cognitive toil, professionals can focus on creative architecture, strategic direction, and human empathy.\n\n"
                    "#### 2. 🔬 Accelerating Scientific & Medical Breakthroughs\n"
                    "• **Genomics & Drug Discovery**: Breakthroughs like AlphaFold solved the 50-year protein-folding challenge, predicting 200M+ structures and shortening discovery timelines from decades to months.\n"
                    "• **Precision Diagnostics**: Deep learning models detect anomalies in oncology, radiology, and retinal imaging earlier and with greater consistency than manual screenings.\n"
                    "• **Materials Science & Climate**: Accelerating battery chemistry discovery and optimizing renewable energy grids.\n\n"
                    "#### 3. 🌐 Engine Behind Daily Digital Experiences\n"
                    "• **Recommender Systems**: Every streaming discovery, e-commerce suggestion, and personalized feed is driven by collaborative filtering and dense vector embeddings.\n"
                    "• **Autonomous Systems**: Powering robotics, smart supply chains, and precision agriculture.\n\n"
                    "#### 4. ⚖️ Ethical Alignment & Future Readiness\n"
                    "• Mastering AI literacy is now fundamental for professionals across all disciplines. Concurrently, addressing algorithmic bias, hallucination risks, and data sovereignty ensures technology serves human well-being responsibly.\n\n"
                    "---\n"
                    "*What specific dimension would you like to explore further—industry disruption, ethical challenges, or career pathways?*"
                )

            # Cinema & Filmmaking Conceptual Questions
            if any(k in text_lower for k in ["cinema", "film", "movie", "director", "nolan", "actor", "acting", "hollywood", "bollywood", "tollywood", "storytelling"]):
                web_ctx = f"\n\n**🌐 Live Context / Background:**\n{meta['web_knowledge']}\n" if meta.get("web_knowledge") else ""
                return (
                    f"### 🎬 Cinema & Visual Storytelling Analysis\n\n"
                    f"Cinema is a unique confluence of visual art, literature, music, and engineering that reflects societal consciousness across eras.\n\n"
                    f"• **Visual Narrative & Directorial Vision**: Great cinema is driven by thematic coherence, lighting, framing, and pacing. Auteur directors craft singular sensory experiences that transcend standard formulaic entertainment.\n"
                    f"• **Theatrical Evolution & Technological Craft**: Modern filmmaking is navigating a transformative shift—balancing practical in-camera craft (such as IMAX 70mm and physical practical effects) with cutting-edge digital post-production and virtual production volumes.\n"
                    f"• **Cultural Resonance**: Beyond entertainment, contemporary global cinema—from Hollywood epics to Bollywood narratives, Tollywood scale, and realist Nepali cinema—provides profound social commentary and emotional catharsis.{web_ctx}\n\n"
                    f"*What specific aspect of filmmaking, director's filmography, or cinema movement would you like to discuss?*"
                )

            # Tech, Hardware & Audio Conceptual Questions
            if any(k in text_lower for k in ["hardware", "gadget", "headphone", "earbud", "audio", "watch", "sensor", "anc", "oled", "battery"]):
                web_ctx = f"\n\n**🌐 Context Notes:**\n{meta['web_knowledge']}\n" if meta.get("web_knowledge") else ""
                return (
                    f"### ⚡ Modern Tech & Hardware Architecture\n\n"
                    f"Consumer electronics and wearable hardware are defined by the convergence of miniaturized silicon, precision mechanical engineering, and intelligent DSP (Digital Signal Processing).\n\n"
                    f"• **Acoustics & Active Noise Cancellation (ANC)**: Modern audio engineering pairs tuned dynamic/planar drivers with dual-microphone inverse phase anti-noise algorithms to isolate ambient disturbances without muddying soundstaging.\n"
                    f"• **Wearable Biosensors**: Smartwatches leverage photoplethysmography (PPG) optical sensors and micro-gyroscopes, interpreting real-time biometric metrics through embedded microcontrollers.\n"
                    f"• **Display & Power Efficiency**: Advances in LTPO OLED panels allow dynamic refresh rates from 1Hz to 120Hz, balancing visual fluidity with all-day battery endurance.{web_ctx}\n\n"
                    f"*Would you like a deeper technical breakdown of any particular gadget technology or architecture?*"
                )

            # General Knowledge & Web-Assisted Explanations
            if meta.get("web_knowledge"):
                return (
                    f"### 💡 Detailed Overview & Insights\n\n"
                    f"{meta['web_knowledge']}\n\n"
                    f"*I am here to converse and discuss this further with you. Feel free to ask follow-up questions!*"
                )

            return (
                f"### 💡 Insight & Discussion\n\n"
                f"Thank you for asking about **{user_text.strip()}**.\n\n"
                f"As an AI advisor, I look at questions through multiple lenses—practical utility, future trajectory, and real-world implications. "
                f"Whether exploring technology, arts, cinema, or career directions, understanding core principles is key to making informed decisions.\n\n"
                f"*Could you share more details about what specific angle or use case you are curious about? I'm happy to dive deep!*"
            )

        sections = []

        # 1. Career Guidance / Courses
        course_items = [i for i in items if i.get("type") == "Course"]
        if course_items:
            target_role = "Modern Technology Careers"
            if any(k in text_lower for k in ["data science", "data analyst", "analytics", "sql"]):
                target_role = "Data Science & Analytics"
                phases = (
                    "1. **Core Foundations**: Master Python (Pandas, NumPy) and Advanced SQL (Window functions, CTEs).\n"
                    "2. **Data Modeling & Stats**: Probability distributions, hypothesis testing, EDA, and Scikit-Learn algorithms.\n"
                    "3. **Applied Machine Learning & BI**: Tableau/PowerBI, feature engineering pipelines, and cloud warehouses (BigQuery/Snowflake).\n"
                    "4. **High-Impact Portfolio Projects**: Build an end-to-end customer churn or recommendation engine with interactive dashboards."
                )
            elif any(k in text_lower for k in ["ai", "machine learning", "ml", "artificial intelligence", "deep learning"]):
                target_role = "AI & Machine Learning Engineering"
                phases = (
                    "1. **Foundations**: Python, Linear Algebra, Multivariable Calculus, and Probability.\n"
                    "2. **Core ML & Deep Learning**: PyTorch/TensorFlow, CNNs, Transformers, and vector embeddings.\n"
                    "3. **LLMs & GenAI Systems**: Prompt engineering, RAG (Retrieval-Augmented Generation), vector DBs, and fine-tuning.\n"
                    "4. **Production MLOps**: Docker, FastAPI model serving, tracking with MLflow, and cloud deployments."
                )
            elif any(k in text_lower for k in ["cloud", "devops", "aws", "docker", "kubernetes"]):
                target_role = "Cloud Architecture & DevOps"
                phases = (
                    "1. **Systems & Scripting**: Linux internals, Bash scripting, and Git workflows.\n"
                    "2. **Cloud Infrastructure**: AWS/GCP compute, VPC networking, IAM policies, and Terraform (IaC).\n"
                    "3. **Containers & Orchestration**: Docker containerization and Kubernetes cluster management.\n"
                    "4. **CI/CD & Observability**: GitHub Actions, Prometheus/Grafana, and automated deployment pipelines."
                )
            elif any(k in text_lower for k in ["cyber", "security", "ethical hacking", "infosec"]):
                target_role = "Cybersecurity & Information Security"
                phases = (
                    "1. **Networking & Systems**: TCP/IP protocols, OSI model, Linux administration, and network analysis (Wireshark).\n"
                    "2. **Security Fundamentals**: Vulnerability scanning, cryptographic protocols, and threat modeling.\n"
                    "3. **Defensive/Offensive Tools**: SOC analysis, SIEM tooling, penetration testing (Burp Suite), and OWASP Top 10.\n"
                    "4. **Hands-on Proof**: TryHackMe/HackTheBox certifications and security incident post-mortems."
                )
            elif any(k in text_lower for k in ["web", "full stack", "frontend", "backend", "software"]):
                target_role = "Full-Stack Software Engineering"
                phases = (
                    "1. **Frontend Fundamentals**: HTML5, modern CSS, JavaScript (ES6+), and React/Next.js.\n"
                    "2. **Backend Engineering**: Node.js/FastAPI, RESTful APIs, relational databases (PostgreSQL), and authentication.\n"
                    "3. **System Architecture**: Caching (Redis), microservices, database indexing, and async task queues.\n"
                    "4. **Full-Stack Portfolio Project**: A complete production SaaS application with auth, database design, and automated testing."
                )
            else:
                phases = (
                    "1. **Prerequisite Fundamentals**: Solidify programming fundamentals and problem solving.\n"
                    "2. **Specialized Toolchain**: Master modern frameworks and production best practices.\n"
                    "3. **Real-World Portfolio**: Build 2-3 production-grade projects demonstrating real domain problem solving.\n"
                    "4. **Certifications & Networking**: Target industry credentials and contribute to open-source."
                )

            if meta.get("is_shift") and meta.get("shift_type") == "domain_shift":
                shift_from = meta.get("shift_from", "Previous Domain")
                career_sec = [
                    f"### 🎓 Switching Domain: Career & Learning Roadmaps",
                    f"✨ **Shifting context from {shift_from} to Career & Learning!**\n"
                    f"Here are curated curriculum tracks and certifications in **{target_role}**:\n\n{phases}"
                ]
            elif meta.get("is_followup"):
                career_sec = [
                    f"### 🎯 Strategic Career Pathway: **{target_role}**",
                    f"✨ **Got it! Continuing your learning roadmap in {target_role}:**\n\n{phases}"
                ]
            else:
                career_sec = [
                    f"### 🎯 Strategic Career Roadmap: **{target_role}**\n\n{phases}"
                ]

            career_sec.append("#### 🎓 Recommended Learning Tracks:")
            for c in course_items:
                skills_preview = ", ".join(c.get("skills", [])[:4])
                career_sec.append(
                    f"• **{c['title']}** — *{c['organization']}*\n"
                    f"  Rating: ★ {c['rating']:.1f}/5.0 • Level: {c['difficulty']} • Skills: {skills_preview}\n"
                    f"  *Key Takeaway:* {c.get('explanation', 'Provides hands-on mastery of fundamental and applied concepts.')}"
                )
            sections.append("\n\n".join(career_sec))

        # 2. Latest Movies & Cinema
        movie_items = [i for i in items if i.get("type") == "Movie"]
        if movie_items:
            ind_label = meta.get("industry_label", "Cinema")
            if meta.get("is_shift") and meta.get("shift_type") == "industry_shift":
                shift_from = meta.get("shift_from", "Previous Industry")
                shift_to = meta.get("shift_to", f"{ind_label} Cinema")
                movie_sec = [
                    f"### 🎬 Switching to {ind_label} Cinema",
                    f"✨ **Shifting context from {shift_from} to {shift_to}!**\n"
                    f"Here are premier {ind_label} cinematic releases to dive into:"
                ]
            elif meta.get("is_shift") and meta.get("shift_type") == "domain_shift":
                shift_from = meta.get("shift_from", "Previous Domain")
                movie_sec = [
                    f"### 🎬 Switching Domain: Cinema Discovery ({ind_label})",
                    f"✨ **Shifting context from {shift_from} to Film & Cinema!**\n"
                    f"Here are top-rated {ind_label} film recommendations:"
                ]
            elif meta.get("is_followup"):
                genres_active = meta.get("movie_genres", [])
                g_str = " & ".join(genres_active) if genres_active else "your preferences"
                movie_sec = [
                    f"### 🎬 Tailored Follow-Up: **{ind_label} ({g_str})**",
                    f"✨ **Got it! Continuing our {ind_label} cinema discussion:**\n"
                    f"Since you enjoy **{g_str}**, I've refined the catalog to highlight standout {ind_label} titles that match this exact energy and style:"
                ]
            else:
                movie_sec = [
                    f"### 🎬 Curated Cinema Highlights ({ind_label})"
                ]

            if meta.get("web_knowledge"):
                movie_sec.append(
                    f"**🌐 Real-Time Industry & 2025/2026 Releases Context:**\n{meta['web_knowledge']}"
                )
            movie_sec.append("#### 📽️ Top Recommendations:")
            for m in movie_items:
                g_txt = ", ".join(m.get("genres", []))
                yr_txt = f" ({m['year']})" if m.get("year") else ""
                movie_sec.append(
                    f"• **{m['title']}{yr_txt}** — *{m['industry']}*\n"
                    f"  Rating: ★ {m['rating']:.1f}/5.0 • Genres: {g_txt}\n"
                    f"  *Why Watch:* {m.get('explanation', 'Outstanding storytelling with strong artistic and entertainment value.')}"
                )
            sections.append("\n\n".join(movie_sec))

        # 3. Products & Tech Buyer Advice
        product_items = [i for i in items if i.get("type") == "Product"]
        if product_items:
            if meta.get("is_shift") and meta.get("shift_type") == "domain_shift":
                shift_from = meta.get("shift_from", "Previous Domain")
                prod_sec = [
                    f"### 🛍️ Switching Domain: Products & Tech Advisory",
                    f"✨ **Shifting context from {shift_from} to Products & Gear!**\n"
                    f"Here are top-tier curated recommendations from our catalog across audio, tech, and everyday essentials:"
                ]
            elif meta.get("is_shift") and meta.get("shift_type") == "category_shift":
                shift_from = meta.get("shift_from", "Previous Category")
                shift_to = meta.get("shift_to", "Products")
                prod_sec = [
                    f"### 🛍️ Switching Category: {shift_to}",
                    f"✨ **Shifting category from {shift_from} to {shift_to}!**\n"
                    f"Here are standout {shift_to} recommendations with verified ratings:"
                ]
            elif meta.get("is_followup"):
                b_note = f" (Refined for under ₹{meta['budget']:,} INR)" if meta.get("budget") else ""
                prod_sec = [
                    f"### 🛍️ Tailored Buyer's Guide{b_note}",
                    f"✨ **Got it! Building on our previous search:**\n"
                    f"Here are refined product recommendations tailored to your updated criteria:"
                ]
            else:
                prod_sec = [
                    "### 🛍️ Buyer's Guide & Spec Evaluation"
                ]

            if meta.get("budget"):
                prod_sec.append(f"*Target Price Range: Under ₹{meta['budget']:,} INR*")
            prod_sec.append("#### ⚡ Featured Selections:")
            for p in product_items:
                prod_sec.append(
                    f"• **{p['name']}** by **{p['brand']}**\n"
                    f"  Price: ₹{p['price_inr']:,} • Category: {p['category']} • Rating: ★ {p['rating']:.1f}/5.0\n"
                    f"  *Evaluation:* {p.get('explanation', 'Excellent price-to-performance ratio with reliable build quality.')}"
                )
            sections.append("\n\n".join(prod_sec))

        if not sections:
            if meta.get("web_knowledge"):
                return f"### 🌐 Live Information & Trends\n\n{meta['web_knowledge']}"
            return (
                "### ⚡ RECOM.ai Multi-Domain Advisory\n\n"
                "I can give you in-depth, personalized guidance across:\n"
                "- 🎬 **Latest Movies**: 2024–2026 releases in Bollywood, Hollywood, Tollywood, or Nepali cinema.\n"
                "- 🛍️ **Products & Tech**: Headphones, earbuds, smartwatches, luxury timepieces, and desk setups.\n"
                "- 🎓 **Career Roadmaps**: Detailed skill paths for AI/ML, Data Science, Web Dev, Cloud, and Cybersecurity.\n\n"
                "Please tell me what industry, role, or gadget category you'd like an in-depth breakdown for!"
            )

        return "\n\n---\n\n".join(sections)

    def _call_gemini_api(
        self,
        api_key: str,
        prompt: str,
        model_name: str = "gemini-3.5-flash",
        temperature: float = 0.2
    ) -> Optional[str]:
        """Calls Google Gemini API using gemini-3.5-flash with low temperature and fast fallback."""
        models_to_try = [model_name, "gemini-2.0-flash", "gemini-1.5-flash-latest"]
        seen = set()
        dedup_models = []
        for m in models_to_try:
            if m and m not in seen:
                seen.add(m)
                dedup_models.append(m)

        for target_model in dedup_models:
            # 1. Direct REST API (Fastest and supports all preview/flash models)
            try:
                import requests
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": temperature,
                        "topP": 0.85,
                        "topK": 40,
                        "maxOutputTokens": 1500
                    }
                }
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent?key={api_key}"
                r = requests.post(url, headers=headers, json=payload, timeout=4.5)
                if r.status_code == 200:
                    data = r.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        texts = [p.get("text", "") for p in parts if "text" in p and p.get("text")]
                        if texts:
                            return "\n\n".join(texts).strip()
                elif r.status_code == 429:
                    logger.warning("Gemini API quota exceeded (429). Fast fallback to built-in intelligence.")
                    break  # Key is rate-limited, retrying other models with same key will also 429
                elif r.status_code == 400 and ("API_KEY_INVALID" in r.text or "API key not valid" in r.text):
                    break
            except Exception as rest_err:
                logger.debug(f"REST call failed for {target_model}: {rest_err}")

            # 2. SDK Fallback (Only if REST had network glitch, not rate-limit)
            try:
                import warnings
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=FutureWarning)
                    import google.generativeai as genai
                genai.configure(api_key=api_key)
                gen_config = genai.types.GenerationConfig(
                    temperature=temperature,
                    top_p=0.85,
                    top_k=40,
                    max_output_tokens=1500,
                )
                model = genai.GenerativeModel(target_model, generation_config=gen_config)
                res = model.generate_content(prompt)
                if res and hasattr(res, "text") and res.text:
                    return res.text.strip()
            except Exception as sdk_err:
                err_str = str(sdk_err)
                logger.debug(f"SDK model {target_model} failed: {sdk_err}")
                if "429" in err_str or "quota" in err_str.lower() or "ResourceExhausted" in err_str:
                    break
                if "API_KEY_INVALID" in err_str or "API key not valid" in err_str:
                    break

        return None

    def generate_response(
        self,
        user_message: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        custom_api_key: Optional[str] = None,
        model_name: str = "gemini-3.5-flash",
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        """
        Generates a conversational response with multi-turn context awareness.
        If Gemini is available, uses it for dynamic response with low temperature.
        Always gracefully falls back to high-quality conversational response with zero errors shown.
        """
        api_key = self.resolve_api_key(custom_api_key)
        local_items, meta = self.extract_intent_and_items(user_message, chat_history=chat_history)

        # If API key is present, attempt Gemini inference
        if api_key:
            try:
                catalog_context = ""
                if local_items:
                    catalog_context = "\nMATCHING RECOM.AI CATALOG ITEMS:\n"
                    for itm in local_items[:5]:
                        itype = itm.get("type", "Item")
                        if itype == "Movie":
                            catalog_context += f"- [Movie] {itm['title']} ({itm['industry']}, Genres: {', '.join(itm.get('genres', []))}, Rating: {itm['rating']}/5.0). Plot: {itm.get('explanation')}\n"
                        elif itype == "Product":
                            catalog_context += f"- [Product] {itm['name']} (Brand: {itm['brand']}, Category: {itm['category']}, Price: ₹{itm['price_inr']}, Rating: {itm['rating']}/5.0). Details: {itm.get('explanation')}\n"
                        elif itype == "Course":
                            catalog_context += f"- [Course] {itm['title']} (Org: {itm['organization']}, Domain: {itm['category']}, Level: {itm['difficulty']}, Rating: {itm['rating']}/5.0). Skills: {', '.join(itm.get('skills', []))}\n"

                prompt_parts = [
                    f"SYSTEM:\n{SYSTEM_INSTRUCTION}\n",
                ]
                if catalog_context:
                    prompt_parts.append(catalog_context)

                if meta.get("is_conversational"):
                    prompt_parts.append(
                        "\nSPECIAL INSTRUCTION: The user is asking an informative, conversational, or conceptual question. "
                        "Talk directly to them with clear, structured, descriptive paragraphs. "
                        "DO NOT recommend specific products, courses, or movies unless they explicitly asked for them."
                    )

                if meta.get("web_knowledge"):
                    prompt_parts.append(
                        f"\nREAL-TIME OPEN WEB CONTEXT (FOR 2025/2026/LATEST INFORMATION):\n{meta['web_knowledge']}\n"
                        f"(You may freely combine this live web data with your broader knowledge to answer fully about 2025 and upcoming developments!).\n"
                    )

                if chat_history:
                    # Cleanly extract prior conversation turns
                    prior_msgs = [m for m in chat_history if not (m.get("role") == "user" and m.get("content") == user_message)]
                    if prior_msgs:
                        prompt_parts.append("\nPRIOR CONVERSATION HISTORY (Maintain Context & Continuity):")
                        for msg in prior_msgs[-6:]:
                            role = "User" if msg.get("role") == "user" else "Assistant"
                            content_text = str(msg.get("content", "")).strip()[:400]
                            prompt_parts.append(f"{role}: {content_text}")

                        if meta.get("is_shift"):
                            shift_from = meta.get("shift_from", "Previous Topic")
                            shift_to = meta.get("shift_to", "New Topic")
                            prompt_parts.append(
                                f"\n⚠️ CRITICAL DOMAIN / TOPIC SHIFT DIRECTIVE (DO NOT HALLUCINATE):\n"
                                f"The user has EXPLICITLY SWITCHED TOPICS from '{shift_from}' to '{shift_to}'.\n"
                                f"STRICT RULES FOR CONTEXT SWITCHING:\n"
                                f"1. COMPLETELY DISREGARD and CLEAR all previous conversational context regarding '{shift_from}'.\n"
                                f"2. DO NOT mention, blend, or cross-reference '{shift_from}' in your response (for example: if switching from Bollywood to Hollywood, discuss ONLY Hollywood; if switching from Movies to Products, discuss ONLY Products with ZERO cinema or movie references).\n"
                                f"3. DO NOT hallucinate connections, merchandise, or hybrid analogies between '{shift_from}' and '{shift_to}'.\n"
                                f"4. Acknowledge the shift cleanly and naturally (e.g., 'Switching gears to {shift_to}...') and focus 100% on '{shift_to}'.\n"
                                f"5. Recommend strictly the matching catalog items provided above."
                            )
                        elif meta.get("is_followup"):
                            prompt_parts.append(
                                "\nCONVERSATIONAL CONTINUITY INSTRUCTION:\n"
                                "The user is continuing a multi-turn conversation on the same topic. Maintain conversational context: "
                                "remember established preferences (e.g. Hindi/Bollywood cinema, specific budget in ₹, or domain). "
                                "When the user refines their criteria (such as adding 'action and comedy'), tailor your response within their established preference."
                            )

                prompt_parts.append(f"\nUser: {user_message}\nAssistant:")
                full_prompt = "\n".join(prompt_parts)

                gemini_text = self._call_gemini_api(api_key, full_prompt, model_name=model_name, temperature=temperature)
                if gemini_text:
                    return {
                        "text": gemini_text,
                        "items": local_items,
                        "source": "gemini"
                    }
            except Exception as e:
                logger.warning(f"Gemini processing exception: {e}")

        # Intelligent Built-in Conversational Engine (Zero raw error messages!)
        response_text = self.generate_intelligent_response(user_message, local_items, meta, chat_history=chat_history)
        return {
            "text": response_text,
            "items": local_items,
            "source": "recom_ai_engine"
        }
