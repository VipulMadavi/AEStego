import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def get_range(diff):
    ranges = [(0, 15, 1), (16, 31, 2), (32, 63, 3), (64, 127, 4), (128, 255, 5)]
    for (low, high, bits) in ranges:
        if low <= diff <= high:
            return bits
    return 1

def embed_data(image_path, secret_text, output_path):
    image = cv2.imread(image_path)
    secret_bin = ''.join(format(ord(char), '08b') for char in secret_text) + '1111111111111110'
    index = 0
    rows, cols, _ = image.shape
    
    for i in range(0, rows - 1, 2):
        for j in range(cols):
            for c in range(3):  # Process each RGB channel
                if index >= len(secret_bin):
                    break
                p1, p2 = int(image[i, j, c]), int(image[i + 1, j, c])
                diff = abs(p1 - p2)
                bit_capacity = get_range(diff)
                
                if index + bit_capacity > len(secret_bin):
                    break
                
                secret_bits = secret_bin[index:index + bit_capacity]
                secret_value = int(secret_bits, 2)
                index += bit_capacity
                
                new_diff = diff + (secret_value - (diff % (1 << bit_capacity)))
                
                if p1 > p2:
                    p2 = p1 - new_diff
                else:
                    p1 = p2 - new_diff
                
                image[i, j, c], image[i + 1, j, c] = np.clip(p1, 0, 255), np.clip(p2, 0, 255)
    
    cv2.imwrite(output_path, image)
    messagebox.showinfo("Success", f"Data hidden successfully in {output_path}")

def extract_data(image_path):
    image = cv2.imread(image_path)
    extracted_bin = ''
    rows, cols, _ = image.shape
    
    for i in range(0, rows - 1, 2):
        for j in range(cols):
            for c in range(3):
                p1, p2 = int(image[i, j, c]), int(image[i + 1, j, c])
                diff = abs(p1 - p2)
                bit_capacity = get_range(diff)
                extracted_bin += format(diff % (1 << bit_capacity), f'0{bit_capacity}b')
    
    extracted_text = ''
    for i in range(0, len(extracted_bin), 8):
        byte = extracted_bin[i:i + 8]
        if byte == '1111111111111110':
            break
        extracted_text += chr(int(byte, 2))
    
    messagebox.showinfo("Extracted Data", extracted_text)

def select_image(embed=True):
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.bmp")])
    if file_path:
        if embed:
            text = simpledialog.askstring("Input", "Enter secret text:")
            if text:
                save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
                if save_path:
                    embed_data(file_path, text, save_path)
        else:
            extract_data(file_path)

def create_gui():
    root = tk.Tk()
    root.title("AEStego")
    root.geometry("400x300")  # Increased window size
    
    tk.Label(root, text="AEStego", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(root, text="PVD based Steganography", font=("Arial", 10)).pack(pady=5)
    
    tk.Button(root, text="Hide Data", font=("Arial", 12), command=lambda: select_image(True)).pack(pady=10)
    tk.Button(root, text="Extract Data", font=("Arial", 12), command=lambda: select_image(False)).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
