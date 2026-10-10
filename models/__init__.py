"""
RECOM.ai - Recommender Engines Module
Contains MovieRecommender, ProductRecommender, and CourseRecommender.
"""

from .movie_rec import MovieRecommender
from .product_rec import ProductRecommender
from .course_rec import CourseRecommender
from .chatbot import ChatbotEngine

__all__ = ["MovieRecommender", "ProductRecommender", "CourseRecommender", "ChatbotEngine"]
