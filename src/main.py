import sys

def main():
    args = sys.argv[1:]
    file = args[0]
    with open(file, "r") as f:
        content = f.read()


if __name__ == "__main__":
    main()
