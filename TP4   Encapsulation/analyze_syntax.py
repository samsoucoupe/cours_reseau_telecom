from read_frames import read_frames
from unhexlify_frames import unhexlify_frames


def analyze_syntax(filename):
    """Syntax analysis of the filename file"""
    frames = read_frames(filename)
    unhexlify_frames(frames)
    return frames
