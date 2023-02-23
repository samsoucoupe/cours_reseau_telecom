from analyze_semantics import analyze_semantics
from analyze_syntax import analyze_syntax

if __name__ == "__main__":
    frames = analyze_syntax("XXX.txt")
    for frame in frames:
        analyze_semantics(frame)
