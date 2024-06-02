# face_recognition_model.py
import face_recognition

def load_and_encode_image(image_path):
    """Loads and encodes a known face image."""
    known_image = face_recognition.load_image_file(image_path)
    known_encoding = face_recognition.face_encodings(known_image)[0]
    return known_encoding

