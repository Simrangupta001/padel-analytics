from utils.helpers import calculate_angle

def get_arm_keypoints(kp):

    rs = kp[6]
    re = kp[8]
    rw = kp[10]

    if rs[0] > 0 or rs[1] > 0:
        return rs, re, rw

    ls = kp[5]
    le = kp[7]
    lw = kp[9]

    if ls[0] > 0 or ls[1] > 0:
        return ls, le, lw

    return None

def classify_shot(kp, is_rally_active):

    arm = get_arm_keypoints(kp)

    if arm is None:
        return None, is_rally_active

    rs, re, rw = arm

    arm_raised = rw[1] < rs[1]

    angle = calculate_angle(rs, re, rw)

    if arm_raised:

        if not is_rally_active:
            return "SERVE", True

        elif angle < 90:
            return "SMASH", True

    if angle > 150:
        return "FOREHAND", is_rally_active

    return "BACKHAND", is_rally_active

def classify_direction(kp, cx, frame_w):

    arm = get_arm_keypoints(kp)

    if arm is None:
        return "unknown"

    rs, re, rw = arm

    head_y = kp[0][1]

    if rw[1] < head_y - 20 and rw[1] < rs[1]:
        return "lob"

    if rw[0] > 0 and abs(rw[0] - cx) > frame_w * 0.05:

        if rw[0] < cx:
            return "cross-court"

        return "down-the-line"

    return "unknown"