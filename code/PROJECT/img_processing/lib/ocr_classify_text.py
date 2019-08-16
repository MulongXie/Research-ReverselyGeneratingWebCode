import pytesseract as pyt
import cv2


def is_text(img, min_word_area, show=False):
    broad = img.copy()
    area_word = 0
    area_total = img.shape[0] * img.shape[1]

    try:
        # ocr text detection
        data = pyt.image_to_data(img).split('\n')
    except:
        print(img.shape)
        return -1
    word = []
    for d in data[1:]:
        d = d.split()
        if d[-1] != '-1':
            if d[-1] != '-' and d[-1] != '—' and int(d[-3]) < 40:
                word.append(d)
                t_l = (int(d[-6]), int(d[-5]))
                b_r = (int(d[-6]) + int(d[-4]), int(d[-5]) + int(d[-3]))

                area_word += int(d[-4]) * int(d[-3])
                cv2.rectangle(broad, t_l, b_r, (0,0,255), 1)

    if show:
        for d in word: print(d)
        print(area_word/area_total, img.shape[0], img.shape[1]/img.shape[0])
        cv2.imshow('a', broad)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # no text in this clip or relatively small text area
    if len(word) == 0 or area_word/area_total < min_word_area:
        return False
    return True
