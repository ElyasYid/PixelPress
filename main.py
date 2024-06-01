import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import compression
from threading import Thread
import tkinter.ttk as ttk

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None

    def showtip(self, text):
        if self.tipwindow or not text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def create_tooltip(widget, text):
    tool_tip = ToolTip(widget)
    def enter(event):
        tool_tip.showtip(text)
    def leave(event):
        tool_tip.hidetip()
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

# Create and place widgets
tk.Label(root, text="Choose Format:").grid(row=0, column=0, padx=10, pady=10)
format_var = tk.StringVar(value="JPEG")
format_options = ["JPEG", "PNG", "GIF", "WEBP", "BMP", "TIFF"]
format_menu = ttk.Combobox(root, textvariable=format_var, values=format_options)
format_menu.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Quality:").grid(row=1, column=0, padx=10, pady=10)
quality_scale = tk.Scale(root, from_=0, to_=100, orient=tk.HORIZONTAL)
quality_scale.set(85)
quality_scale.grid(row=1, column=1, padx=10, pady=10)

tiff_compression_var = tk.StringVar(value="tiff_lzw")
tk.Label(root, text="TIFF Compression:").grid(row=2, column=0, padx=10, pady=10)
tiff_compression_menu = ttk.Combobox(root, textvariable=tiff_compression_var, values=["tiff_lzw", "tiff_jpeg", "tiff_adobe_deflate"])
tiff_compression_menu.grid(row=2, column=1, padx=10, pady=10)

compress_button = tk.Button(root, text="Compress Image", command=compress_image)
compress_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Add tooltips
create_tooltip(format_menu, "Select the image format you want to compress to.")
create_tooltip(quality_scale, "Set the quality/compression level (0-100).")
create_tooltip(tiff_compression_menu, "Select the compression method for TIFF images.")

# Run the application
root.mainloop()
