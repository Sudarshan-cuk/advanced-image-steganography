import numpy as np
from metrics_and_noise import bytes_to_bits, bits_to_bytes

def embed_lsb(cover_img, payload):
    """Embed payload bits into LSBs of cover_img"""
    h, w = cover_img.shape[:2]
    channels = 1 if cover_img.ndim == 2 else cover_img.shape[2]
    capacity = h * w * channels

    payload_bits = bytes_to_bits(payload)
    if payload_bits.size > capacity:
        raise ValueError(f"Payload too large: {payload_bits.size} > {capacity}")

    flat = cover_img.flatten()
    flat = flat & 0xFE  # Clear LSB
    flat[:payload_bits.size] |= payload_bits
    return flat.reshape(cover_img.shape)

def extract_lsb(stego_img, num_bytes):
    """Extract num_bytes from LSBs of stego_img"""
    num_bits = num_bytes * 8
    flat = stego_img.flatten()
    bits = flat[:num_bits] & 1
    return bits_to_bytes(bits)
