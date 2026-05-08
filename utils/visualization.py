import cv2

COLOR_TRAIL = (0, 200, 255)

SHOT_COLORS = {
    "FOREHAND": (0, 200, 0),
    "BACKHAND": (255, 140, 0),
    "SMASH": (0, 0, 220),
    "SERVE": (255, 0, 200),
}

def draw_court_overlay(frame):

    h, w = frame.shape[:2]

    cv2.line(
        frame,
        (w // 2, 0),
        (w // 2, h),
        (180, 180, 180),
        1
    )

    cv2.line(
        frame,
        (0, h // 2),
        (w, h // 2),
        (180, 180, 180),
        1
    )

def draw_ball_trail(frame, trail):

    pts = list(trail)

    for i in range(1, len(pts)):

        if pts[i - 1] is None or pts[i] is None:
            continue

        alpha = i / len(pts)

        thickness = max(1, int(4 * alpha))

        color = tuple(int(c * alpha) for c in COLOR_TRAIL)

        cv2.line(
            frame,
            pts[i - 1],
            pts[i],
            color,
            thickness
        )

def draw_dashboard(frame, shot_counts, ball_events, frame_id, fps):

    h, w = frame.shape[:2]

    panel_w = 200
    panel_h = 140

    x0 = w - panel_w - 10
    y0 = 10

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (x0, y0),
        (x0 + panel_w, y0 + panel_h),
        (20, 20, 20),
        -1
    )

    cv2.addWeighted(
        overlay,
        0.55,
        frame,
        0.45,
        0,
        frame
    )

    cv2.putText(
        frame,
        "Live Analytics",
        (x0 + 6, y0 + 18),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (220, 220, 220),
        1
    )

    labels = ["FOREHAND", "BACKHAND", "SMASH", "SERVE"]

    for i, lbl in enumerate(labels):

        color = SHOT_COLORS.get(lbl, (160, 160, 160))

        cv2.putText(
            frame,
            f"{lbl}: {shot_counts.get(lbl, 0)}",
            (x0 + 6, y0 + 38 + i * 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            color,
            1
        )

    cv2.putText(
        frame,
        f"Bounces: {ball_events['bounce']}",
        (x0 + 6, y0 + 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (0, 0, 255),
        1
    )

    cv2.putText(
        frame,
        f"T={frame_id/fps:.1f}s",
        (x0 + 6, y0 + 135),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (180, 180, 180),
        1
    )