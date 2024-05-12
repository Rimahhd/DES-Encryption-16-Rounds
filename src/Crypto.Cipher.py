import tkinter as tk
from tkinter import messagebox
from pyDes import des, PAD_PKCS5

# DES Tables and Constants
X1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

X2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

Rotations = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

ExpantionTable = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

S_BOX = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]

    
    ]# S2 to S8 follow the same structure and must be defined

PTable = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
           2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

InitialPermutation = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
                       62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
                       57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
                       61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

FinalPermutation = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
                     38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
                     36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
                     34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

# Helper Functions
def hex_to_bin(hex_str):
    " Convert Hexadecimal to Binary "
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)

def bin_to_hex(bin_str):
    " Convert Binary to Hexadecimal "
    return f"{int(bin_str, 2):X}"

def permute(input_bin, permutation_table):
    " Permute input binary string based on a permutation table "
    return ''.join(input_bin[i - 1] for i in permutation_table)

def rotate_left(input_bin, shifts):
    " Perform left circular shift "
    return input_bin[shifts:] + input_bin[:shifts]

def xor(bin1, bin2):
    " XOR two binary strings "
    return ''.join('1' if b1 != b2 else '0' for b1, b2 in zip(bin1, bin2))


def substitute(input_expanded):
    " Substitute using S-boxes defined elsewhere in the code "
    pieces = (input_expanded[i:i + 6] for i in range(0, len(input_expanded), 6))
    result = ''
    for i, piece in enumerate(pieces):
        row = int(piece[0] + piece[5], 2)
        col = int(piece[1:5], 2)
        result += f"{S_BOX[i][row][col]:04b}"
    return result

def des_round(input_half, key):
    " Perform one round of DES encryption "
    expanded = permute(input_half, ExpantionTable)
    xored = xor(expanded, key)
    substituted = substitute(xored)
    permuted = permute(substituted, PTable)
    return permuted

def main():
    def encrypt():
      # User inputs
      plaintext = plaintext_entry.get()
      key = key_entry.get()
      # Validate input lengths
      if len(plaintext) != 16 or len(key) != 16:
          messagebox.showerror("Error", "Message and key should be 16 bytes (32 characters).")
          return
    
      # Generate round keys
      round_keys_output = ""
      key_bin = hex_to_bin(key)
      key_pc1 = permute(key_bin, X1)
      left, right = key_pc1[:28], key_pc1[28:]
      round_keys = []
      round_keys_output += "Key Schedule:\n"
      for i in range(16):
            left = rotate_left(left, Rotations[i])
            right = rotate_left(right, Rotations[i])
            round_key = permute(left + right, X2)
            round_keys.append(round_key)
            round_keys_output += f" Round {i+1}: Left = {bin_to_hex(left)} ({left}), Right = {bin_to_hex(right)} ({right})\n"
        
      # Perform DES encryption
      message_bin = hex_to_bin(plaintext)
      permuted = permute(message_bin, InitialPermutation)
      left, right = permuted[:32], permuted[32:]
      message_output = "Message Processing:\n"
      for i, key in enumerate(round_keys):
            new_right = xor(des_round(right, key), left)
            left, right = right, new_right
            message_output += f" Round {i+1}: Left = {bin_to_hex(left)} ({left}), Right = {bin_to_hex(right)} ({right})\n"
        
      final_permuted = permute(right + left, FinalPermutation)
      encrypted_message = bin_to_hex(final_permuted)
        
      # Display results in the GUI text box
      text_output.insert(tk.END, round_keys_output + "\n" + message_output + f"\n Encrypted Output: {encrypted_message}\n")


    root = tk.Tk()
    root.title("DES Encryption RIMAHHD")
    root.geometry("950x1000")

    # Create input fields
    plaintext_label = tk.Label(root, text="Enter your message to encrypt:")
    plaintext_label.grid(row=0, column=0, padx=5, pady=5)
    plaintext_entry = tk.Entry(root, width=30)
    plaintext_entry.grid(row=0, column=1, padx=5, pady=5)

    key_label = tk.Label(root, text="Enter the encryption key:")
    key_label.grid(row=1, column=0, padx=5, pady=5)
    key_entry = tk.Entry(root, width=30)
    key_entry.grid(row=1, column=1, padx=5, pady=5)

    # Create encrypt button
    encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
    encrypt_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    # Create output text box
    text_output = tk.Text(root, width=115, height=40)
    text_output.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    root.mainloop()

# Execute the main function
if __name__ == "__main__":
    main()
