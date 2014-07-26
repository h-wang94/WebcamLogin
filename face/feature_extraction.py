import cv2
import sys
import numpy as np

class FaceClassification:
  def __init__(self):
    self.face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
    self.nose_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_mcs_nose.xml")
    self.eye_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_eye.xml")
    self.usage_str = "Press <enter> to take picture."

  def take_picture(self):
    cap = cv2.VideoCapture(0)
    print self.usage_str
    while (cap.isOpened()):
      ret, frame = cap.read()
      if not ret:
        print "Camera error, quitting."
        break
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5)
      try:
        x, y, w, h = faces[0]
      except IndexError as e:
        continue
      frame_copy = frame.copy()
      cv2.rectangle(frame_copy, (x, y), (x + w, y + h), color=(255, 0, 0), thickness=2)
      cv2.imshow(self.usage_str, frame_copy)
      if cv2.waitKey(1) & 0xFF == ord("\n"):
        face = frame[y:y+h, x:x+w]
        face = cv2.resize(face, dsize=(200, 200), fx=0, fy=0)
        cap.release()
        cv2.destroyAllWindows()
        return face

  def predict(self, face):
    data = np.array([cv2.imread("images/harrison_face.png", cv2.IMREAD_GRAYSCALE),
                     cv2.imread("images/rohan_face.png", cv2.IMREAD_GRAYSCALE),
                     cv2.imread("images/heath_face.png", cv2.IMREAD_GRAYSCALE)])
    labels = np.array(range(len(data)))
    cv2.imshow("face", face)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    model1 = cv2.createEigenFaceRecognizer()
    model1.train(data, labels)
    pred1, conf1 = model1.predict(face)
    model2 = cv2.createFisherFaceRecognizer()
    model2.train(data, labels)
    pred2, conf2 = model2.predict(face)
    print pred1, pred2, conf1, conf2
    import IPython; IPython.embed()

  def register(self, img, name):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = self.face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)
    try:
      x, y, w, h = faces[0]
    except IndexError as e:
      print "Could not detect a face"
      return
    face = img[y:y+h, x:x+w]
    face = cv2.resize(face, dsize=(200, 200), fx=0, fy=0)
    cv2.imwrite("images/" + name + ".png", face)
    
if __name__ == "__main__":
  fc = FaceClassification()
  fc.predict(fc.take_picture())
  # FeatureExtraction().extract_face()
