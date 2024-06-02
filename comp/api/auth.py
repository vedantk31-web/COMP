# auth.py
import face_recognition
import os
import pickle
import cv2

def register_user(image_path, user_name):
    """Registers a user by encoding their face and saving it."""
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    
    os.makedirs("registered_users", exist_ok=True)
    with open(f"registered_users/{user_name}.pkl", "wb") as f:
        pickle.dump(face_encoding, f)

def load_known_faces():
    """Loads known face encodings from the registered users directory."""
    known_face_encodings = []
    known_face_names = []
    for file in os.listdir("registered_users"):
        if file.endswith(".pkl"):
            with open(f"registered_users/{file}", "rb") as f:
                face_encoding = pickle.load(f)
                known_face_encodings.append(face_encoding)
                known_face_names.append(file.split(".")[0])
    return known_face_encodings, known_face_names

def verify_face(unknown_image_path):
    """Verifies a face against registered users."""
    known_face_encodings, known_face_names = load_known_faces()
    unknown_image = face_recognition.load_image_file(unknown_image_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    results = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
    
    if True in results:
        return known_face_names[results.index(True)]
    else:
        return None

def authenticate_user(video_source=0):
    """Authenticates a user using their face via webcam."""
    known_face_encodings, known_face_names = load_known_faces()

    video_capture = cv2.VideoCapture(video_source)
    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                video_capture.release()
                cv2.destroyAllWindows()
                return name

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return None
