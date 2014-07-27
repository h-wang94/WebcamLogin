import cv2
import sys
import os
import numpy as np

IMAGE_DIR = "./images/"
MODEL_DIR = "./models/"

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
        cap.release()
        cv2.destroyAllWindows()
        return frame

  def predict(self, img):
    faces = self.face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)
    try:
      x, y, w, h = faces[0]
    except IndexError as e:
      print "No face detected!"
      return
    face = img[y:y+h, x:x+w]
    face = cv2.resize(face, dsize=(200, 200), fx=0, fy=0)
    model1 = cv2.createEigenFaceRecognizer(threshold=3000)
    model1.load(MODEL_DIR + "model1")
    pred1, conf1 = model1.predict(face)
    model2 = cv2.createFisherFaceRecognizer(threshold=3000)
    model2.load(MODEL_DIR + "model2")
    pred2, conf2 = model2.predict(face)
    with open(MODEL_DIR + "label_map", "r") as f:
      label_map = eval(f.readline())
    print "Eigen model 1 classification: %s, confidence: %f"%(label_map[pred1], conf1)
    print "Fisher model 2 classification: %s, confidence: %f"%(label_map[pred2], conf2)

  def train(self):
    data = []
    labels = []
    label_map = {}
    for i, filename in enumerate(os.listdir(IMAGE_DIR)):
      data.append(cv2.imread(IMAGE_DIR + filename, cv2.IMREAD_GRAYSCALE))
      labels.append(i)
      label_map[i] = filename
    data = np.asarray(data)
    labels = np.asarray(labels)
    model1 = cv2.createEigenFaceRecognizer(threshold=3000)
    model1.train(data, labels)
    model1.save(MODEL_DIR + "model1")
    model2 = cv2.createFisherFaceRecognizer(threshold=3000)
    model2.train(data, labels)
    model2.save(MODEL_DIR + "model2")
    with open(MODEL_DIR + "label_map", "w") as f:
      f.write(str(label_map))

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
  if len(sys.argv) != 2:
    print "Need option"
    sys.exit(1)
  fc = FaceClassification()
  if sys.argv[1] == "train":
    fc.train()
  elif sys.argv[1] == "predict":
    fc.predict(fc.take_picture())
  else:
    print "Invalid option"
    sys.exit(1)
