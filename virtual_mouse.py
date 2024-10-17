import cv2
import mediapipe as mp
import pyautogui
import math

vid_cap = cv2.VideoCapture(0)

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
hands = mp_hand.Hands()


def damping_function(var, target, alpha=0.1):
    # Damping formula for both variables
    damped_var = (1 - alpha) * target + alpha * var
    return damped_var


def calculate_distance(pos1x, pos1y, pos1z, pos2x, pos2y, pos2z):
    return math.sqrt((pos2x - pos1x) ** 2 + (pos2y - pos1y) ** 2 + (pos2z - pos1z) ** 2)


while True:
    seccess, img = vid_cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    screen_hight, screen_width, c = img.shape

    if results.multi_hand_landmarks:
        # Hands were detected
        hand_lmks = results.multi_hand_landmarks[0]
        if hand_lmks.landmark[8] and hand_lmks.landmark[4]:
            mp_draw.draw_landmarks(img, hand_lmks, mp_hand.HAND_CONNECTIONS)

            px = int(hand_lmks.landmark[8].x * pyautogui.size().width)
            py = int(hand_lmks.landmark[8].y * pyautogui.size().height)

            cv2px = int(hand_lmks.landmark[8].x * screen_width)
            cv2py = int(hand_lmks.landmark[8].y * screen_hight)

            DAMPING = 0.69
            pyautogui.moveTo(damping_function(pyautogui.position(
            ).x, px, DAMPING), damping_function(pyautogui.position().y, py, DAMPING), 0)

            treshold = 0.065
            if calculate_distance(
                    hand_lmks.landmark[4].x, hand_lmks.landmark[4].y, hand_lmks.landmark[4].z, hand_lmks.landmark[8].x, hand_lmks.landmark[8].y, hand_lmks.landmark[8].z) < treshold:
                pyautogui.click()
                print("clicked")
                cv2.circle(
                    img, (cv2px, cv2py), 20, (243, 133, 23), cv2.FILLED)

    cv2.imshow("Image", img)
    # hit "q" in the keyboard to stop the script.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
