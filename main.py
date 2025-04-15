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
    subparsers = parser.add_subparsers(dest="command", help="Commands", required=True)

    def add_common_args(parser: argparse.ArgumentParser):
        parser.add_argument(
            "text", nargs="*", help="Text to process (if not provided, reads from stdin)"
        )
        parser.add_argument(
            "-f", "--file", help="Input file to read from instead of command line"
        )
        parser.add_argument(
            "-o", "--output", help="Output file to write to instead of stdout"
        )

    encode_parser = subparsers.add_parser("encode", help="Encode ASCII to invisible Unicode")
    add_common_args(encode_parser)

    decode_parser = subparsers.add_parser("decode", help="Decode invisible Unicode back to ASCII")
    add_common_args(decode_parser)

    args = parser.parse_args()

    input_text = ""
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

    if args.command == "encode":
        output_text = encode_ascii_to_unicode(input_text)
    elif args.command == "decode":
        output_text = decode_unicode_to_ascii(input_text)
    else:
        parser.print_help()
        sys.exit(1)

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
