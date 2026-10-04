"""
Modul penyesuaian ke belakang (Backward Compatibility Wrapper).
Menyalurkan panggilan fungsi ke Model: RecommendationModel.
"""

from config import DB_CONFIG, SKINTONE_ORDER
from models.recommendation_model import RecommendationModel


def check_connection():
    return RecommendationModel.check_connection()


def get_recommendations(undertone, skintone):
    return RecommendationModel.get_foundation_recommendation(undertone, skintone)


def get_lipstick_recommendations(undertone, skintone):
    return RecommendationModel.get_lipstick_recommendation(undertone, skintone)