import argparse
import io
import math
import os
from pathlib import Path

import cv2
import fitz
import keras_ocr
import numpy as np
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR / "pdf"
PPTX_DIR = BASE_DIR / "pptx"
TEMP_IMAGE_NAME = "text_free_image.jpg"


def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2) / 2)
    y_mid = int((y1 + y2) / 2)
    return (x_mid, y_mid)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_name")
    parser.add_argument("download_images")
    parser.add_argument("--use-sam2", action="store_true")
    return parser.parse_args()


def str_to_bool(value):
    return str(value).lower() == "true"


def prepare_image(img):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    elif img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img.astype("uint8")


def build_text_mask(prediction_groups, image_shape):
    mask = np.zeros(image_shape[:2], dtype="uint8")

    for box in prediction_groups[0]:
        x0, y0 = box[1][0]
        x1, y1 = box[1][1]
        x2, y2 = box[1][2]
        x3, y3 = box[1][3]

        x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
        x_mid1, y_mid1 = midpoint(x0, y0, x3, y3)

        thickness = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mid1), 255, thickness)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 10:
            cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return cv2.filter2D(mask, -1, sharpen_kernel)


def create_sam2_mask_generator():
    config_path = os.getenv("SAM2_CONFIG_PATH")
    checkpoint_path = os.getenv("SAM2_CHECKPOINT_PATH")
    if not config_path or not checkpoint_path:
        print(
            "SAM2 requested but SAM2_CONFIG_PATH or SAM2_CHECKPOINT_PATH is missing; using OCR-only masking."
        )
        return None

    try:
        import torch
        from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator
        from sam2.build_sam import build_sam2
    except Exception as error:
        print(f"SAM2 dependencies are unavailable; using OCR-only masking. {error}")
        return None

    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = build_sam2(
            config_file=config_path,
            ckpt_path=checkpoint_path,
            device=device,
        )
        return SAM2AutomaticMaskGenerator(model, output_mode="binary_mask")
    except Exception as error:
        print(f"SAM2 initialization failed; using OCR-only masking. {error}")
        return None


def refine_mask_with_sam2(img, mask, sam2_generator):
    if sam2_generator is None or not np.any(mask):
        return mask

    try:
        generated_masks = sam2_generator.generate(img)
    except Exception as error:
        print(f"SAM2 mask generation failed; using OCR-only masking. {error}")
        return mask

    refined_mask = mask.copy()
    base_mask = mask > 0
    overlap_threshold = float(os.getenv("SAM2_OVERLAP_THRESHOLD", "0.15"))

    for generated_mask in generated_masks:
        segmentation = generated_mask.get("segmentation")
        if segmentation is None:
            continue

        segment_pixels = segmentation.astype(bool)
        segment_area = np.count_nonzero(segment_pixels)
        if segment_area == 0:
            continue

        overlap_area = np.count_nonzero(segment_pixels & base_mask)
        if overlap_area / segment_area >= overlap_threshold:
            refined_mask[segment_pixels] = 255

    return refined_mask


def inpaint_text(img, pipeline, image_mode, output_path, sam2_generator=None):
    img = prepare_image(img)

    try:
        prediction_groups = pipeline.recognize([img])
    except ValueError as error:
        print(f"Error occurred: {error}")
        return None

    mask = build_text_mask(prediction_groups, img.shape)
    mask = refine_mask_with_sam2(img, mask, sam2_generator)
    result = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)

    if image_mode == "CMYK":
        result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)

    cv2.imwrite(str(output_path), result)
    return output_path


def process_pdf(dir_name, download_images, use_sam2):
    pptx_dir_path = PPTX_DIR / dir_name
    image_output_dir = pptx_dir_path / "images"
    pdf_path = PDF_DIR / f"{dir_name}.pdf"
    temp_image_path = pptx_dir_path / TEMP_IMAGE_NAME

    pipeline = keras_ocr.pipeline.Pipeline()
    sam2_generator = create_sam2_mask_generator() if use_sam2 else None

    doc = fitz.open(pdf_path)
    for page in doc:
        images = page.get_images()
        for item in images:
            xref = item[0]
            rect = page.get_image_rects(xref)[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            image_array = np.array(image)
            image_mode = image.mode
            inpaint_text(
                image_array,
                pipeline,
                image_mode,
                temp_image_path,
                sam2_generator=sam2_generator,
            )
            page.add_redact_annot(rect)
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)
            page.insert_image(rect, filename=str(temp_image_path))

    temp_pdf_path = PDF_DIR / f"{dir_name}_1.pdf"
    doc.save(temp_pdf_path)
    doc.close()

    os.remove(pdf_path)
    os.rename(temp_pdf_path, pdf_path)

    if download_images:
        image_output_dir.mkdir(parents=True, exist_ok=True)
        doc = fitz.open(pdf_path)
        counter = 1
        for page in doc:
            images = page.get_images()
            for item in images:
                xref = item[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                image.save(image_output_dir / f"{dir_name}_{counter}.jpg")
                counter += 1
        doc.close()

    if temp_image_path.exists():
        os.remove(temp_image_path)


def main():
    args = parse_args()
    process_pdf(
        dir_name=args.dir_name,
        download_images=str_to_bool(args.download_images),
        use_sam2=args.use_sam2,
    )


if __name__ == "__main__":
    main()
