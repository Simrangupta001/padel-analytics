import numpy as np

ZONE_DEADBAND = 0.08

def calculate_angle(a, b, c):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (
        np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6
    )

    angle = np.degrees(
        np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    )

    return float(angle)

def wrist_speed(curr_kp, prev_kp):

    if prev_kp is None:
        return 0.0

    rw_c = curr_kp[10] if curr_kp[10][0] > 0 else curr_kp[9]
    rw_p = prev_kp[10] if prev_kp[10][0] > 0 else prev_kp[9]

    return float(
        np.linalg.norm(np.array(rw_c) - np.array(rw_p))
    )

def assign_zone_label(cx, cy, frame_w, frame_h, last_label):

    mid_x = frame_w / 2
    mid_y = frame_h / 2

    if (
        abs(cx - mid_x) < frame_w * ZONE_DEADBAND
        or abs(cy - mid_y) < frame_h * ZONE_DEADBAND
    ) and last_label:
        return last_label

    side = "Left" if cx < mid_x else "Right"
    depth = "Back" if cy < mid_y else "Front"

    return f"{side}-{depth}"

def nearest_zone(cx, cy, frame_w, frame_h):

    side = "Left" if cx < frame_w / 2 else "Right"
    depth = "Back" if cy < frame_h / 2 else "Front"

    return f"{side}-{depth}"