import cv2
from argparse import ArgumentParser
import glob
from PIL import Image
import os

FRAME_FOLDER = os.path.join(os.path.dirname(__file__), 'frames')

def cleanup():
    print("cleaning up...")
    if os.path.exists(FRAME_FOLDER):
        for file in os.listdir(FRAME_FOLDER):
            os.remove(os.join(FRAME_FOLDER, file))
    print("done")

def make_gif(name):
    print("making GIF...")
    images = glob.glob(f"{FRAME_FOLDER}/*.jpg")
    images.sort()
    frames = [Image.open(image) for image in images]
    frame_one = frames[0]
    frame_one.save(name, format="GIF", append_images=frames,
                   save_all=True, duration=50, loop=0)
    print("done")

def convert_mp4_to_jpgs(path):
    print("extracting images from video...")
    if not os.path.exists(FRAME_FOLDER):
        os.mkdir(FRAME_FOLDER)
    video_capture = cv2.VideoCapture(path)
    still_reading, image = video_capture.read()
    frame_count = 0
    while still_reading:
        cv2.imwrite(os.path.join(FRAME_FOLDER, f"{frame_count:03d}.jpg"), image)
        
        # read next image
        still_reading, image = video_capture.read()
        frame_count += 1
    print("Done")

if __name__ == "__main__":
    parser = ArgumentParser(description="Convert an MP4 file to a GIF")
    parser.add_argument('path', metavar='PATH', help="Path to the video to convert", type=str)
    parser.add_argument('--output', "-o", help="Name of the GIF to produce. If not provided, the input file name is used.", type=str)
    args = parser.parse_args()
    convert_mp4_to_jpgs(args.path)
    mp4_dir = os.sep.join(args.path.split(os.sep)[0:-1])
    gif_name = ".".join(args.path.split(os.sep)[-1].split(".")[0:-1]) + ".gif"
    if args.output is not None:
        gif_name = args.output
    make_gif(os.path.join(mp4_dir, gif_name))
    cleanup()
