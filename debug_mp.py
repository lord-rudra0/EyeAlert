try:
    import mediapipe
    print(f"MediaPipe location: {mediapipe.__file__}")
    import mediapipe.python.solutions as solutions
    print("Direct import of solutions successful")
    from mediapipe.python.solutions import face_mesh
    print("FaceMesh imported")
except ImportError as e:
    print(f"ImportError: {e}")
except AttributeError as e:
    print(f"AttributeError: {e}")
except Exception as e:
    print(f"Exception: {e}")
