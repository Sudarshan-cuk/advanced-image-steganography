import cv2
import numpy as np
from metrics_and_noise import add_gaussian_noise, compute_psnr, compute_ber, bytes_to_bits
from lsb_core import embed_lsb, extract_lsb
import csv
import matplotlib.pyplot as plt

def main():
    # Use any PNG/JPG in folder as cover
    cover_path = "sample.png"  # Download any image and rename
    cover = cv2.imread(cover_path)
    if cover is None:
        print("Put 'sample.png' in folder first")
        return

    message = "Test message for noise analysis"
    payload = message.encode("utf-8")
    
    stego = embed_lsb(cover, payload)
    psnr_embed = compute_psnr(cover, stego)
    print(f"PSNR (cover→stego): {psnr_embed:.2f} dB")

    sigmas = [0.0, 0.005, 0.01, 0.02, 0.05]
    results = []
    orig_bits = bytes_to_bits(payload)

    for sigma in sigmas:
        noisy = add_gaussian_noise(stego, sigma)
        recovered = extract_lsb(noisy, len(payload))
        
        if len(recovered) == len(payload):
            rec_bits = bytes_to_bits(recovered)
            ber = compute_ber(orig_bits, rec_bits)
        else:
            ber = 1.0

        psnr_noise = compute_psnr(stego, noisy)
        results.append((sigma, psnr_noise, ber))
        print(f"σ={sigma}: PSNR={psnr_noise:.1f}dB, BER={ber:.4f}")

    # Save CSV for report
    with open("noise_results.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["sigma", "PSNR_dB", "BER"])
        for r in results:
            writer.writerow(r)
    
    # Create and save a simple plot (PSNR and BER vs sigma)
    sigmas = [r[0] for r in results]
    psnrs = [r[1] for r in results]
    bers = [r[2] for r in results]

    fig, ax1 = plt.subplots(figsize=(7, 4))
    ax1.plot(sigmas, psnrs, marker='o', color='tab:blue', label='PSNR (dB)')
    ax1.set_xlabel('sigma')
    ax1.set_ylabel('PSNR (dB)', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.plot(sigmas, bers, marker='s', linestyle='--', color='tab:red', label='BER')
    ax2.set_ylabel('BER', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title('Noise analysis: PSNR and BER vs sigma')
    fig.tight_layout()
    out_png = "noise_analysis.png"
    fig.savefig(out_png, dpi=150)
    plt.close(fig)

    print(f"✅ Created noise_results.csv and {out_png}")

if __name__ == "__main__":
    main()
