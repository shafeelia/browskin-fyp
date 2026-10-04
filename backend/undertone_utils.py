"""
Modul penyesuaian ke belakang (Backward Compatibility Wrapper).
Menyalurkan panggilan ke Model: UndertoneModel.
"""

from models.undertone_model import UndertoneModel

# Instance tunggal untuk panggilan modul lama
_default_model = UndertoneModel()


def classify_skintone(R, G, B):
    return UndertoneModel.classify_skintone(R, G, B)


def extract_features(image):
    return _default_model.extract_features(image)