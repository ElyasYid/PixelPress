import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import compression
from threading import Thread
import tkinter.ttk as ttk

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

    def showtip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tip_window, text=self.text, background="#ffffe0", relief=tk.SOLID, borderwidth=1, font=("Helvetica", 8))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

def create_tooltip(widget, text):
    tool_tip = ToolTip(widget, text)
    def enter(event):
        tool_tip.showtip()
    def leave(event):
        tool_tip.hide_tip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def compress_image():
    input_path = filedialog.askopenfilename()
    if not input_path:
        messagebox.showwarning("Input Error", "No input file selected.")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=f".{format_var.get().lower()}",
                                               filetypes=[(format_var.get(), f"*.{format_var.get().lower()}")])
    if not output_path:
        messagebox.showwarning("Output Error", "No output file selected.")
        return

    format_choice = format_var.get()
    quality = int(quality_scale.get())
    tiff_compression = tiff_compression_var.get()

    if not os.path.isfile(input_path):
        messagebox.showerror("File Error", "Input file does not exist.")
        return

    if quality < 0 or quality > 100:
        messagebox.showerror("Quality Error", "Quality must be between 0 and 100.")
        return

    progress_bar.start()
    compress_button.config(state=tk.DISABLED)

    def compress():
        try:
            if format_choice == "JPEG":
                compression.compress_jpeg(input_path, output_path, quality)
            elif format_choice == "PNG":
                compression.compress_png(input_path, output_path, quality // 10)  # PNG compression level is 0-9
            elif format_choice == "GIF":
                compression.compress_gif(input_path, output_path, quality)
            elif format_choice == "WEBP":
                compression.compress_webp(input_path, output_path, quality)
            elif format_choice == "BMP":
                compression.compress_bmp(input_path, output_path, quality)
            elif format_choice == "TIFF":
                compression.compress_tiff(input_path, output_path, compression=tiff_compression)
            messagebox.showinfo("Success", f"Image compressed and saved as {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compress image: {e}")
        finally:
            progress_bar.stop()
            compress_button.config(state=tk.NORMAL)

    Thread(target=compress).start()

# Create the main window
root = tk.Tk()
root.title("PixelPress")
root.configure(bg="lightblue")

# Set the icon
icon_path = 'pp.ico'  # Replace with your icon file path
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    print(f"Icon file '{icon_path}' not found. Skipping icon setup.")

# Create a Canvas widget to act as the background
canvas = tk.Canvas(root, bg="lightblue")
canvas.pack(fill=tk.BOTH, expand=True)

# Create and place widgets inside the Canvas
frame = tk.Frame(canvas, bg="lightblue")
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

label_format = tk.Label(frame, text="Choose Format:", bg="lightblue")
label_format.grid(row=0, column=0, padx=10, pady=10, sticky="w")
format_var = tk.StringVar(value="JPEG")
format_options = ["JPEG", "PNG", "GIF", "WEBP", "BMP", "TIFF"]
format_menu = ttk.Combobox(frame, textvariable=format_var, values=format_options)
format_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

label_quality = tk.Label(frame, text="Quality:", bg="lightblue")
label_quality.grid(row=1, column=0, padx=10, pady=10, sticky="w")
quality_scale = tk.Scale(frame, from_=0, to_=100, orient=tk.HORIZONTAL)
quality_scale.set(85)
quality_scale.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

label_tiff = tk.Label(frame, text="TIFF Compression:", bg="lightblue")
label_tiff.grid(row=2, column=0, padx=10, pady=10, sticky="w")
tiff_compression_var = tk.StringVar(value="tiff_lzw")
tiff_compression_menu = ttk.Combobox(frame, textvariable=tiff_compression_var, values=["tiff_lzw", "tiff_jpeg", "tiff_adobe_deflate"])
tiff_compression_menu.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

compress_button = tk.Button(frame, text="Compress Image", command=compress_image, bg="lightblue")
compress_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

progress_bar = ttk.Progressbar(frame, mode='indeterminate')
progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Configure column and row weights for responsiveness
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=2)
frame.rowconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)
frame.rowconfigure(2, weight=1)
frame.rowconfigure(3, weight=1)
frame.rowconfigure(4, weight=1)

# Add tooltips
create_tooltip(format_menu, "Select the image format you want to compress to.")
create_tooltip(quality_scale, "Set the quality/compression level (0-100).")
create_tooltip(tiff_compression_menu, "Select the compression method for TIFF images.")

# Run the application
root.mainloop()
