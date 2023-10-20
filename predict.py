import torch
import matplotlib.pyplot as plt
from modules import VQVAE, PixelCNN
from dataset import get_image_slices

# This function visualizes original vs reconstructed images.
def visualize_reconstructions(originals, reconstructions, num_samples=3):
    # Loop through the number of samples specified.
    for i in range(num_samples):
        # Create a subplot for the original and reconstructed images.
        fig, axs = plt.subplots(1, 2)

        # Display the original image.
        axs[0].imshow(originals[i, 0].detach().numpy(), cmap='gray')
        axs[0].set_title("Original")

        # Display the reconstructed image.
        axs[1].imshow(reconstructions[i, 0].detach().numpy(), cmap='gray')
        axs[1].set_title("Reconstruction")

        # Remove axis ticks and labels.
        plt.show()

# This function visualizes generated samples.
def visualize_samples(samples, num_samples=3):
    # Loop through the number of samples specified.
    for i in range(num_samples):
        # Display the generated image.
        plt.imshow(samples[i, 0].detach().cpu().numpy(), cmap='gray')
        plt.title("Generated Sample")
        plt.show()

# This function visualizes images generated using PixelCNN.
def visualize_pixelcnn_generation_batch(pixelcnn, batch_size, img_size=(1, 128, 128)):
    # Create a batch of empty images.
    samples = torch.zeros(batch_size, *img_size).to(device)

    # Generate images pixel by pixel.
    for i in range(img_size[1]):
        for j in range(img_size[2]):
            out = pixelcnn(samples)
            probs = F.softmax(out[:, :, i, j], dim=1)
            for b in range(batch_size):
                samples[b, :, i, j] = torch.multinomial(probs[b], 1).float() / 255.0

    # Display the generated images.
    for b in range(batch_size):
        plt.imshow(samples[b, 0].cpu().detach().numpy(), cmap='gray')
        plt.title(f"PixelCNN Generated Sample {b+1}")
        plt.show()

# This function compares an original image with one generated by PixelCNN.
def compare_original_and_generated(original, pixelcnn, img_size=(1, 128, 128)):
    # Generate an image using PixelCNN.
    generated = torch.zeros(img_size).to(device)
    for i in range(img_size[1]):
        for j in range(img_size[2]):
            out = pixelcnn(generated)
            probs = F.softmax(out[:, :, i, j], dim=1)
            generated[:, :, i, j] = torch.multinomial(probs, 1).float() / 255.0

    # Create a subplot for the original and PixelCNN generated images.
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # Display the original image.
    axs[0].imshow(original[0, 0].cpu().detach().numpy(), cmap='gray')
    axs[0].set_title("Original")

    # Display the PixelCNN generated image.
    axs[1].imshow(generated[0, 0].cpu().detach().numpy(), cmap='gray')
    axs[1].set_title("PixelCNN Generated")

    # Remove axis ticks and labels.
    plt.show()