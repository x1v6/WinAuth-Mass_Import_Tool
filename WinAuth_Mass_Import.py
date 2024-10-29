import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext

def create_winauth_txt(entries, file_name):
    """Creates a WinAuth-compatible .txt file with the provided entries."""
    try:
        with open(file_name, "w") as file:
            for secret, label in entries:
                if not secret or not label:
                    raise ValueError("Secret or Label cannot be empty.")
                uri = f"otpauth://totp/{label.replace(' ', '+')}?secret={secret}&digits=6&icon=WinAuth"
                file.write(uri + "\n")

        messagebox.showinfo("Success", f"WinAuth .txt file '{file_name}' created successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create .txt file: {e}")

def browse_file():
    """Opens a file dialog for the user to select where to save the file."""
    file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    return file_name if file_name else None

def on_generate_click():
    """Handles the Generate button click event."""
    secrets = entry_secrets.get("1.0", tk.END).strip().splitlines()
    labels = entry_labels.get("1.0", tk.END).strip().splitlines()

    secrets = [secret for secret in secrets if secret.strip()]
    labels = [label for label in labels if label.strip()]

    if not secrets or not labels:
        messagebox.showwarning("Input Error", "Please provide both Secret Codes and Labels.")
        return

    if len(secrets) != len(labels):
        messagebox.showwarning("Input Error", "Number of Secret Codes and Labels must match.")
        return

    entries = list(zip(secrets, labels))
    file_name = browse_file()
    if file_name:
        create_winauth_txt(entries, file_name)

def toggle_dark_mode():
    """Toggles between light and dark mode."""
    global dark_mode
    dark_mode = not dark_mode
    toggle_button.config(text="☀️" if dark_mode else "🌙")
    apply_theme()

def apply_theme():
    """Applies the selected theme (light or dark) to the GUI."""
    bg_color = "#2E2E2E" if dark_mode else "#FFFFFF"
    fg_color = "#FFFFFF" if dark_mode else "#000000"
    entry_bg_color = "#555555" if dark_mode else "#FFFFFF"
    button_bg_color = "#666666" if dark_mode else "#F0F0F0"

    root.config(bg=bg_color)

    # Apply colors to all widgets
    label_secrets.config(bg=bg_color, fg=fg_color)
    label_labels.config(bg=bg_color, fg=fg_color)
    toggle_button.config(bg=button_bg_color, fg=fg_color)

    entry_secrets.config(bg=entry_bg_color, fg=fg_color)
    entry_labels.config(bg=entry_bg_color, fg=fg_color)

    generate_button.config(bg=button_bg_color, fg=fg_color)
    version_label.config(bg=bg_color, fg=fg_color)

# Set up the GUI
root = tk.Tk()
root.title("WinAuth .txt Generator v. 1.18")

# Set a fixed window size to fit the layout better
root.geometry("480x440")  # Width adjusted to minimize empty space
root.resizable(False, False)

dark_mode = False  # Initialize dark mode flag

# Secret Codes Entry
label_secrets = tk.Label(root, text="Secret Codes (one per line):")
label_secrets.grid(row=1, column=0, padx=10, pady=(20, 5), sticky='nw')  # Added space above

entry_secrets = scrolledtext.ScrolledText(root, width=45, height=8)  # Width adjusted
entry_secrets.grid(row=2, column=0, padx=10, pady=5, columnspan=2, sticky='nsew')

# Labels Entry
label_labels = tk.Label(root, text="Labels (one per line):")
label_labels.grid(row=3, column=0, padx=10, pady=10, sticky='nw')

entry_labels = scrolledtext.ScrolledText(root, width=45, height=8)  # Width adjusted
entry_labels.grid(row=4, column=0, padx=10, pady=5, columnspan=2, sticky='nsew')

# Generate Button (aligned with the text box above)
generate_button = tk.Button(root, text="Generate .txt", command=on_generate_click)
generate_button.grid(row=5, column=0, padx=10, pady=10, sticky='w')  # Aligning left side of the text box

# Dark Mode Toggle (aligned to the right side of the text box)
toggle_button = tk.Button(root, text="🌙", command=toggle_dark_mode, width=3)
toggle_button.grid(row=5, column=1, padx=10, pady=10, sticky='e')  # Aligning right next to Generate button

# Version label at the bottom-right corner
version_label = tk.Label(root, text="v. 1.18", anchor="se")
version_label.grid(row=6, column=1, padx=10, pady=(0, 10), sticky='se')  # Positioned at the bottom right

# Apply initial theme
apply_theme()

# Start the GUI main loop
root.mainloop()
