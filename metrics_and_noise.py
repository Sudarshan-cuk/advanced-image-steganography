import numpy as np

def calculate_bit_error_rate(original_bits, bits_recovered):
    """
    Calculates the Bit Error Rate (BER) between original and recovered bits.

    Args:
        original_bits (np.array): The original message bits.
        bits_recovered (np.array): The bits recovered from the stego image.

    Returns:
        float: The Bit Error Rate.
    """
    # Ensure bits_recovered is treated as a binary array (0 or 1)
    br = bits_recovered.astype(np.uint8) & 1

    # Assuming original_bits also needs to be binary
    orig_b = original_bits.astype(np.uint8) & 1

    # Calculate the number of differing bits
    diff_bits = np.sum(br != orig_b)

    # Calculate BER
    total_bits = br.size
    if total_bits == 0:
        return 0.0 # Avoid division by zero
    ber = diff_bits / total_bits
    return ber

# You can add more metric functions here as needed.

def bytes_to_bits(data: bytes) -> np.ndarray:
    """Convert a bytes object to a 1-D numpy array of bits (0/1).

    Bits are returned in big-endian order per byte (msb first), which
    matches `np.unpackbits` default behavior.
    """
    if not isinstance(data, (bytes, bytearray)):
        # allow already-bit arrays to pass through
        arr = np.asarray(data, dtype=np.uint8)
        if arr.ndim == 1 and arr.dtype == np.uint8 and arr.size in (0,):
            return np.array([], dtype=np.uint8)
        return arr

    if len(data) == 0:
        return np.array([], dtype=np.uint8)

    a = np.frombuffer(data, dtype=np.uint8)
    bits = np.unpackbits(a)
    return bits.astype(np.uint8)


def bits_to_bytes(bits) -> bytes:
    """Convert an array-like of bits (0/1) to a bytes object.

    Expects the number of bits to be a multiple of 8. Returns the
    corresponding bytes (big-endian per byte).
    """
    b = np.asarray(bits, dtype=np.uint8).ravel() & 1
    if b.size == 0:
        return b""
    if b.size % 8 != 0:
        raise ValueError("Number of bits must be a multiple of 8 to convert to bytes")
    packed = np.packbits(b)
    return packed.tobytes()


def compute_psnr(img1, img2) -> float:
    """Compute PSNR (dB) between two images.

    Works for grayscale or color images. Input images are expected to be
    uint8 arrays or numeric arrays with values in [0,255].
    """
    a = np.asarray(img1).astype(np.float64)
    b = np.asarray(img2).astype(np.float64)
    if a.shape != b.shape:
        raise ValueError("Input images must have the same shape for PSNR")
    mse = np.mean((a - b) ** 2)
    if mse == 0:
        return float("inf")
    PIXEL_MAX = 255.0
    psnr = 10 * np.log10((PIXEL_MAX ** 2) / mse)
    return psnr


def add_gaussian_noise(image, sigma: float):
    """Add Gaussian noise to an image.

    `sigma` is the standard deviation of the noise in the [0,1] range when
    the image is normalized to [0,1]. Typical usage in the repo uses small
    sigma like 0.005, 0.01, etc.
    """
    img = np.asarray(image)
    # Work on float in [0,1]
    if np.issubdtype(img.dtype, np.floating):
        f = img.astype(np.float64)
        # If image already in [0,1], keep; otherwise assume 0-255 and scale
        if f.max() > 1.0:
            f = f / 255.0
    else:
        f = img.astype(np.float64) / 255.0

    noise = np.random.normal(loc=0.0, scale=sigma, size=f.shape)
    noisy = f + noise
    noisy = np.clip(noisy, 0.0, 1.0)
    noisy_uint8 = (noisy * 255.0).round().astype(np.uint8)
    return noisy_uint8


def compute_ber(original_bits, recovered_bits) -> float:
    """Compute Bit Error Rate (BER) between two bit arrays.

    Accepts lists/arrays of 0/1 or bytes (bytes will be converted via
    `bytes_to_bits`). Returns a float between 0 and 1.
    """
    # Convert bytes to bits if necessary
    if isinstance(original_bits, (bytes, bytearray)):
        orig = bytes_to_bits(original_bits)
    else:
        orig = np.asarray(original_bits).astype(np.uint8)

    if isinstance(recovered_bits, (bytes, bytearray)):
        rec = bytes_to_bits(recovered_bits)
    else:
        rec = np.asarray(recovered_bits).astype(np.uint8)

    # If lengths differ, define BER=1.0 (caller in script uses this behaviour)
    if orig.size != rec.size:
        return 1.0

    # Ensure binary
    orig = orig & 1
    rec = rec & 1
    diff = np.sum(orig != rec)
    if orig.size == 0:
        return 0.0
    return float(diff) / float(orig.size)
