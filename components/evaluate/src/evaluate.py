import argparse
import json
import logging
import os
from pathlib import Path
from datetime import datetime, timezone


def configure_logger() -> logging.Logger:
    logger = logging.getLogger("evaluate")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s"))
        logger.addHandler(handler)
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(level)
    return logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-message-path", required=True, help="Path to input JSON file with a 'message' field")
    parser.add_argument("--append-text", default=" - evaluated", help="Text to append to message")
    parser.add_argument("--output-path", required=True, help="Where to write updated JSON file")
    args = parser.parse_args()

    logger = configure_logger()

    input_path = Path(args.input_message_path)
    output_path = Path(args.output_path)

    # Prefer a writable location for artifacts (OpenShift/KFP pods often run with random UID)
    artifacts_dir = Path(os.getenv("ARTIFACTS_DIR", "/tmp/artifacts"))
    try:
        artifacts_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        # Fallback to /tmp if a custom path was set but not writable
        artifacts_dir = Path("/tmp/artifacts")
        artifacts_dir.mkdir(parents=True, exist_ok=True)
    evaluated_copy_path = artifacts_dir / "evaluated_message.json"

    if not input_path.exists():
        logger.error(f"Input message file not found: {input_path}")
        raise SystemExit(2)

    with input_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    original = str(payload.get("message", ""))
    payload["message"] = f"{original}{args.append_text}"
    payload["evaluated_at"] = datetime.now(timezone.utc).isoformat()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    with evaluated_copy_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    logger.info(f"Loaded: {input_path}")
    logger.info(f"Wrote updated JSON: {output_path}")
    logger.info(f"Wrote evaluated artifact copy: {evaluated_copy_path}")
    logger.info(f"New message: {payload['message']}")


if __name__ == "__main__":
    main()


