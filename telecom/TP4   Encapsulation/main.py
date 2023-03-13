from analyze_semantics import analyze_semantics
from analyze_syntax import analyze_syntax

if __name__ == "__main__":
    frames = analyze_syntax("test.txt")
    for frame in frames:
        print(frame)
        analyze_semantics(frame)
