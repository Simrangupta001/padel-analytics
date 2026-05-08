from ultralytics import YOLO
import cv2
import pandas as pd
from collections import defaultdict

from utils.shot_classifier import classify_shot, classify_direction
from utils.visualization import (
    draw_court_overlay,
    draw_dashboard,
    draw_ball_trail
)
from utils.ball_tracker import BallTracker
from utils.helpers import (
    wrist_speed,
    assign_zone_label,
    nearest_zone
)

INPUT_VIDEO  = "/Users/simrankumarigupta/padel-analytics/input/input_vedio.mp4"
OUTPUT_VIDEO = "outputs/final001_output.mp4"
OUTPUT_CSV   = "outputs/shot_results001.csv"

DET_MODEL  = "yolov8m.pt"
POSE_MODEL = "yolov8m-pose.pt"

MAX_PLAYERS          = 4
CONF_PERSON          = 0.45
CONF_BALL            = 0.25
CONF_RACKET          = 0.30

SHOT_COOLDOWN_FRAMES = 12
RALLY_RESET_FRAMES   = 60
WRIST_VELOCITY_MIN   = 8.0

CLS_PERSON = 0
CLS_BALL   = 32
CLS_RACKET = 38

SHOT_COLORS = {
    "FOREHAND": (0, 200, 0),
    "BACKHAND": (255, 140, 0),
    "SMASH": (0, 0, 220),
    "SERVE": (255, 0, 200),
}

COLOR_PERSON = (200, 200, 200)
COLOR_BALL   = (0, 255, 255)
COLOR_RACKET = (255, 100, 0)

def main():

    print("Loading YOLO models...")

    det_model  = YOLO(DET_MODEL)
    pose_model = YOLO(POSE_MODEL)

    print("Models loaded successfully")

    cap = cv2.VideoCapture(INPUT_VIDEO)

    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {INPUT_VIDEO}")

    fps    = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    out = cv2.VideoWriter(
        OUTPUT_VIDEO,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    results_list = []

    frame_id = 0
    is_rally_active = False
    frames_since_shot = 0

    cooldown_remaining = defaultdict(int)
    prev_keypoints = {}
    last_zone_label = {}

    shot_counts = defaultdict(int)
    unique_players = set()

    ball_tracker = BallTracker()
    ball_events = {"bounce": 0}

    print("Processing video...")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_id += 1

        if frame_id % 100 == 0:
            print(f"Frame {frame_id}/{total}")

        draw_court_overlay(frame)

        frames_since_shot += 1

        if frames_since_shot > RALLY_RESET_FRAMES:
            is_rally_active = False

        for zone in list(cooldown_remaining):
            if cooldown_remaining[zone] > 0:
                cooldown_remaining[zone] -= 1

        det_results = det_model(frame, verbose=False)[0]

        boxes_all   = det_results.boxes.xyxy.cpu().numpy()
        classes_all = det_results.boxes.cls.cpu().numpy()
        confs_all   = det_results.boxes.conf.cpu().numpy()

        person_boxes = []
        ball_boxes = []
        racket_boxes = []

        for box, cls, conf in zip(boxes_all, classes_all, confs_all):

            cls = int(cls)

            if cls == CLS_PERSON and conf > CONF_PERSON:
                person_boxes.append((box, conf))

            elif cls == CLS_BALL and conf > CONF_BALL:
                ball_boxes.append(box)

            elif cls == CLS_RACKET and conf > CONF_RACKET:
                racket_boxes.append(box)

        ball_cx = None
        ball_cy = None

        if ball_boxes:

            best_ball = max(
                ball_boxes,
                key=lambda b: (b[2] - b[0]) * (b[3] - b[1])
            )

            bx1, by1, bx2, by2 = map(int, best_ball)

            ball_cx = (bx1 + bx2) // 2
            ball_cy = (by1 + by2) // 2

            cv2.circle(frame, (ball_cx, ball_cy), 8, COLOR_BALL, 2)

            cv2.putText(
                frame,
                "BALL",
                (bx1, by1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                COLOR_BALL,
                2
            )

        bounce = ball_tracker.update(ball_cx, ball_cy, frame_id, height)

        if bounce:

            ball_events["bounce"] += 1

            bounce_zone = nearest_zone(
                ball_cx,
                ball_cy,
                width,
                height
            )

            results_list.append({
                "frame": frame_id,
                "timestamp_sec": round(frame_id / fps, 2),
                "player": bounce_zone,
                "shot": "BOUNCE",
                "direction": "-"
            })

        draw_ball_trail(frame, ball_tracker.trail)

        for rbox in racket_boxes:

            rx1, ry1, rx2, ry2 = map(int, rbox)

            cv2.rectangle(
                frame,
                (rx1, ry1),
                (rx2, ry2),
                COLOR_RACKET,
                2
            )

            cv2.putText(
                frame,
                "RACKET",
                (rx1, ry1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                COLOR_RACKET,
                2
            )

        person_boxes.sort(key=lambda x: x[1], reverse=True)

        person_boxes = person_boxes[:MAX_PLAYERS]

        for box, _ in person_boxes:

            x1, y1, x2, y2 = map(int, box)

            crop = frame[y1:y2, x1:x2]

            if crop.size == 0:
                continue

            pose_result = pose_model(crop, verbose=False)[0]

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            centroid_key = (
                cx // max(1, width // 2),
                cy // max(1, height // 2)
            )

            last_lbl = last_zone_label.get(centroid_key)

            zone = assign_zone_label(
                cx,
                cy,
                width,
                height,
                last_lbl
            )

            last_zone_label[centroid_key] = zone

            shot = None
            direction = "unknown"

            if pose_result.keypoints is not None:

                kp_all = pose_result.keypoints.xy.cpu().numpy()

                if len(kp_all) > 0:

                    kp = kp_all[0]

                    speed = wrist_speed(
                        kp,
                        prev_keypoints.get(zone)
                    )

                    prev_keypoints[zone] = kp

                    if (
                        speed >= WRIST_VELOCITY_MIN
                        and cooldown_remaining[zone] == 0
                    ):

                        shot, is_rally_active = classify_shot(
                            kp,
                            is_rally_active
                        )

                        if shot is not None:

                            direction = classify_direction(
                                kp,
                                cx,
                                width
                            )

                            cooldown_remaining[zone] = SHOT_COOLDOWN_FRAMES

                            frames_since_shot = 0

                            shot_counts[shot] += 1

                            unique_players.add(zone)

                            results_list.append({
                                "frame": frame_id,
                                "timestamp_sec": round(frame_id / fps, 2),
                                "player": zone,
                                "shot": shot,
                                "direction": direction
                            })

                    for kx, ky in kp:

                        if kx > 0 and ky > 0:

                            cv2.circle(
                                frame,
                                (int(x1 + kx), int(y1 + ky)),
                                3,
                                (0, 255, 0),
                                -1
                            )

            color = SHOT_COLORS.get(shot, COLOR_PERSON)

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            label = zone if shot is None else f"{zone} | {shot}"

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )

            if direction != "unknown":

                cv2.putText(
                    frame,
                    direction,
                    (x1, y2 + 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45,
                    color,
                    1
                )

        draw_dashboard(
            frame,
            shot_counts,
            ball_events,
            frame_id,
            fps
        )

        out.write(frame)

    cap.release()
    out.release()

    df = pd.DataFrame(results_list)

    df.to_csv(OUTPUT_CSV, index=False)

    print("\nProcessing Complete")
    print(f"Output Video : {OUTPUT_VIDEO}")
    print(f"Output CSV   : {OUTPUT_CSV}")

    print("\nShot Counts:\n")

    if not df.empty:

        shot_df = df[df["shot"] != "BOUNCE"]

        pivot = shot_df.groupby(
            ["player", "shot"]
        ).size().unstack(fill_value=0)

        print(pivot)

if __name__ == "__main__":
    main()