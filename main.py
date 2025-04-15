import argparse
import sys
import os

os.environ["PYTHONIOENCODING"] = "utf-8"

ASCII_RANGE = range(0x20, 0x7F)  # Space (0x20) to Tilde (0x7E)
TAG_RANGE = range(0xE0020, 0xE007F)  # Unicode TAG SPACE to TAG TILDE
TAG_OFFSET = 0xE0000


def encode_ascii_to_unicode(text: str) -> str:
    result: list[str] = []
    for char in text:
        code_point = ord(char)
        if code_point in ASCII_RANGE:
            tag_code_point = code_point + TAG_OFFSET
            result.append(chr(tag_code_point))
        else:
            result.append(char)
    return "".join(result)


def decode_unicode_to_ascii(text: str) -> str:
    result: list[str] = []
    for char in text:
        code_point = ord(char)
        if code_point in TAG_RANGE:
            ascii_code_point = code_point - TAG_OFFSET
            result.append(chr(ascii_code_point))
        else:
            result.append(char)
    return "".join(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["encode", "decode"], help="Mode: encode or decode")
    parser.add_argument("text", nargs="*", help="Text to process (if not provided, reads from stdin)")
    parser.add_argument("-f", "--file", help="Input file to read from instead of command line")
    parser.add_argument("-o", "--output", help="Output file to write to instead of stdout")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                input_text = f.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.text:
        input_text = " ".join(args.text)
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    if args.mode == "encode":
        output_text = encode_ascii_to_unicode(input_text)
    else:
        output_text = decode_unicode_to_ascii(input_text)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_text)
        except Exception as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        sys.stdout.buffer.write(output_text.encode('utf-8'))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
