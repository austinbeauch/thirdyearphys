import cv2
import numpy as np
from matplotlib import pyplot as plt
# pylint: disable=maybe-no-member

cap = cv2.VideoCapture('austin.avi')
framerate = cap.get(cv2.CAP_PROP_FPS)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
real_height = 1.89e3 
mm_per_pixel = real_height / frame_height
thresh = 10
distance_thresh = 20

def main():
  drop_count = 0
  drops = []
  while(cap.isOpened()):
    ret, raw = cap.read()
    original = raw.copy()
    count = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

    if not ret:
      break
    blur = cv2.blur(cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY), (5, 5))

    processed = cv2.threshold(blur, thresh, 255, cv2.THRESH_BINARY)[1]
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
      for drop in drops:
        dist = distance(x, y, drop)
        if dist < distance_thresh:  # same drop as previous frame
          is_new = False
          drop.predicted_frames = 0
          drop.update(x, y, count)
          continue

      if is_new:
        new_drop = Drop(drop_count, x, y, count)
        drop_count += 1
        drops.append(new_drop)

    # predicting/removing drops
    seen = []
    for drop in drops:
      if not drop.seen:
        drop.predict(count)
      if drop.predicted_frames <= 10:
        seen.append(drop)
    drops = seen
    
    # drawing information on frame
    for drop in drops:
      text = "%i: %0.2f" % (drop.id, drop.vel * mm_per_pixel)  # convert to mm/sec
      color = (255, 255, 255) 
      if drop.predicted_frames != 0:
        color = (0, 0, 255) 
      raw = cv2.putText(raw, text, (int(drop.x+10), int(drop.y+10)), cv2.FONT_HERSHEY_SIMPLEX , 0.5, color, 1, cv2.LINE_AA) 
    
    show(original, raw, blur, processed)

    ### FOR PRODUCING THE VELOCITIES FIGURE FOR THE REPORT. OCCLUDNIG HAPPENS JUST AFTER ###
    if count >= 850: break
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  
  cap.release()
  cv2.destroyAllWindows()
 
  for drop in drops:
    if drop.id == 0:

      plt.plot(drop._vel)

      # hardcoded the intervals because I'm not getting paid to actually make this thing legit (yet)
      for low, high in [(0, 95) , (105,430) , (450,630), (653, 745), (755, 845)]:
        m, b = fit(drop._frames, drop._vel, low, high)
        line = m*np.array(drop._frames[low:high]) + b
        plt.plot(drop._frames[low:high], line, label=f"{round(np.mean(drop._vel[low:high]),3)} mm/s")

      plt.title(f"Drop {drop.id}")
      plt.xlabel("Frame")
      plt.ylabel("Velocity")
      plt.legend()
      plt.show()

def fit(x, y, i1, i2, deg=1):
  m, b = np.polyfit(x[i1:i2], y[i1:i2], deg)
  return m, b


def distance(x, y, d2):
  return np.sqrt((x - d2.x)**2 + (y-d2.y)**2)

class Drop:
  def __init__(self, id, x, y, frame):
    self.id = id
    self._x = [x]
    self._y = [y]
    self._vel = []
    self._frames = [frame]
    self.seen = True
    self.predicted_frames = 0

  def __str__(self):
    return f"Drop {self.id}, ({self.x}, {self.y}, {self.vel})"

  def update(self, new_x, new_y, frame):
    self._x.append(new_x)
    self._y.append(new_y)
    self._frames.append(frame)

    velocity = (self._y[-2] - self._y[-1]) / framerate  # update velocity in pix/sec
    self._vel.append(velocity) 
    self.seen = True

  def predict(self, frame):
    predicted_y = self.y - (self.vel * framerate)
    self.update(self.x, predicted_y, frame)
    self.predicted_frames += 1

  @property
  def vel(self):
    return self._vel[-1] if len(self._vel) > 0 else 0
  @property
  def x(self):
    return self._x[-1]
  
  @property
  def y(self):
    return self._y[-1]

def show(*imgs):
  for i, image in enumerate(imgs):
    cv2.imshow(str(i), image)

if __name__ == "__main__":
  main()