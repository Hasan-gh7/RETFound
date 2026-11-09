"""Record a trusted person's completed modality review; does not detect a retina."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from retfound_platform.config import MAX_IMAGE_BYTES
from retfound_platform.datasets.manifests import write_json
from retfound_platform.inference.input_validation import REVIEWS, review_record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('--reviewer', required=True)
    parser.add_argument('--note', required=True)
    parser.add_argument('--confirm-color-fundus', action='store_true',
                        help='Attest that you personally inspected this exact image and confirmed color fundus modality')
    args = parser.parse_args()
    if not args.confirm_color_fundus:
        parser.error('A trusted person must inspect the image first, then supply --confirm-color-fundus. This command does not classify image modality.')
    try:
        with args.image.open('rb') as stream:
            payload = stream.read(MAX_IMAGE_BYTES + 1)
        if len(payload) > MAX_IMAGE_BYTES:
            raise ValueError('Image exceeds the review byte limit')
        record = review_record(payload, args.reviewer, args.note)
        output = REVIEWS / f'{record["image_sha256"]}.json'
        write_json(output, record)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Review not recorded: {exc}\n')
    print(f'Review recorded for SHA-256 {record["image_sha256"]}. Only these exact image bytes are approved.')
    print('New uploads will use this review immediately. No image was copied or model weights changed.')


if __name__ == '__main__':
    main()
