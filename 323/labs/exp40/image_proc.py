import numpy as np
import cv2

# pylint: disable=maybe-no-member

cap = cv2.VideoCapture('austin.avi')
framerate = cap.get(cv2.CAP_PROP_FPS)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
real_height = 1.89  #mm
mm_per_pixel = real_height / frame_height
thresh = 10
distance_thresh = 10

window_name = 'Image'

font = cv2.FONT_HERSHEY_SIMPLEX 
org = (50, 50) 
fontScale = 0.5
color = (255, 0, 0) 
thickness = 1

def main():
  drop_count = 0
  drops = []
  while(cap.isOpened()):
    ret, raw = cap.read()
    blur = cv2.blur(raw, (5, 5))
    if not ret:
      break
    processed = cv2.threshold(cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY), thresh, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    new_drops = []
    for c in contours:
        (x, y), radius = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(raw, center, radius, (0,0,255), 1)
        new_drops.append((x, y))

    for drop in drops:
      drop.seen = False

    # decide if the drop is the same or not
    for x, y in new_drops:
      is_new = True
      for old_drop in drops:
        dist = distance(x, y, old_drop)
        if dist < distance_thresh:  # same drop as previos frame
          is_new = False
          old_drop.update(x, y)
          continue

      if is_new:
        new_drop = Drop(drop_count, x, y)
        drop_count += 1
        drops.append(new_drop)

    seen = []
    for drop in drops:
      if drop.seen:
        seen.append(drop)
    drops = seen
    
    for drop in drops:
      raw = cv2.putText(raw, f"{drop.id}:{round(drop.vel, 5)}", (int(drop.x())+10, int(drop.y())+10), font, fontScale, color, thickness, cv2.LINE_AA) 
    
    show(raw, blur, processed)
    if cv2.waitKey(30) & 0xFF == ord('q'):
      break
  
  cap.release()
  cv2.destroyAllWindows()

def distance(x, y, d2):
  return np.sqrt((x- d2.x())**2 + (y-d2.y())**2)

class Drop:
  def __init__(self, id, x, y):
    self.id = id
    self._x = [x]
    self._y = [y]
    self.vel = 0
    self.seen = True

  def update(self, new_x, new_y):
    self._x.append(new_x)
    self._y.append(new_y)
    self.velocity()
    self.seen = True

  def velocity(self):
    self.vel = (self.y(-2) - self.y(-1)) * mm_per_pixel / framerate

  def x(self, idx=-1):
    return self._x[idx]

  def y(self, idx=-1):
    return self._y[idx]

def show(*imgs):
  for i, image in enumerate(imgs):
    cv2.imshow(str(i), image)

if __name__ == "__main__":
  main()