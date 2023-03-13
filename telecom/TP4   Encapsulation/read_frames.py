def read_frames(filename):
    """
    This function creates a list of strings from the file containing frames.
    Each string in the returned list is a frame from the file.
    return: list of frames contained in the file
    """
    with open(filename) as file:
        frames = []  # List of frames
        frame = ""  # Current frame
        for line in file:
            line = line.rstrip("\n")  # Remove newline character
            line = line[5:53]  # Keep only interesting columns
            frame += line
            if not line:  # Trame separator
                # Store frame in frames
                frame = frame.replace(" ", "")  # Remove whitespace
                frames.append(frame)  # Add frame to the list
                frame = ""  # Reset frame
        # If there is a frame to save at the end of the file
        if frame:
            frame = frame.replace(" ", "")  # Remove whitespace
            frames.append(frame)  # Add frame to the list
    return frames
