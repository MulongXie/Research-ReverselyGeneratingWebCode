import cv2
import glob


label_paths = glob.glob('input/*.txt')

for label_path in label_paths:
    name = label_path.split('\\')[1][:-4]
    img_path = 'input/' + name + '.png'

    img = cv2.imread(img_path, 0)
    label = open(label_path, 'r')

    sentences = clip_sentence(img, label)
    words = clip_word(sentences, 1, os.path.join('output', name))
    break
