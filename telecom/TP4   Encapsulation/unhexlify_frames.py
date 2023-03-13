import binascii


def unhexlify_frames(frames):
    """frames: list of frames"""
    for i, frame in enumerate(frames):
        frames[i] = binascii.unhexlify(frame)
