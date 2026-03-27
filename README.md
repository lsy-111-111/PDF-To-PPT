# PDF to PPT Convertor

## Optional SAM 2 image refinement

The editable-image conversion flow can now optionally refine its OCR-based text
mask with [Meta's SAM 2](https://github.com/facebookresearch/sam2) before
inpainting. Existing behavior is unchanged by default.

To enable it for image-editable conversions:

1. Install SAM 2 and its runtime dependencies in the same Python environment
   used by the backend.
2. Set these environment variables before starting the server:
   - `PDF_TO_PPT_USE_SAM2=true`
   - `SAM2_CONFIG_PATH=<path to a SAM2 config>`
   - `SAM2_CHECKPOINT_PATH=<path to a SAM2 checkpoint>`

`SAM2_OVERLAP_THRESHOLD` can also be set to tune how aggressively SAM 2 masks
are merged with the existing OCR text mask. If SAM 2 is unavailable or
misconfigured, the backend automatically falls back to the existing OCR-only
masking flow.
