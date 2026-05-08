from collections import deque

BALL_TRAIL_LEN = 20
BOUNCE_GROUND_FRAC = 0.70

class BallTracker:

    def __init__(self):

        self.trail = deque(maxlen=BALL_TRAIL_LEN)

        self.prev_cy = None
        self.prev_dy = 0

    def update(self, cx, cy, frame_id, frame_h):

        if cx is None:

            self.trail.append(None)

            return False

        self.trail.append((cx, cy))

        is_bounce = False

        if self.prev_cy is not None:

            dy = cy - self.prev_cy

            if (
                self.prev_dy > 2
                and dy < -2
                and cy > frame_h * BOUNCE_GROUND_FRAC
            ):
                is_bounce = True

            self.prev_dy = dy

        self.prev_cy = cy

        return is_bounce