import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from tkinter import filedialog, messagebox
from main import ToolTip, create_tooltip, compress_image
import compression

class TestMain(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()

    def tearDown(self):
        self.root.destroy()

    def test_ToolTip_showtip(self):
        widget = tk.Text(self.root)
        tip = ToolTip(widget, "Test Tip")
        tip.showtip()
        self.assertTrue(tip.tip_window is not None)

    def test_ToolTip_hide_tip(self):
        widget = tk.Text(self.root)
        tip = ToolTip(widget, "Test Tip")
        tip.showtip()
        tip.hide_tip()
        self.assertTrue(tip.tip_window is None)

    def test_create_tooltip(self):
        widget = tk.Text(self.root)
        create_tooltip(widget, "Test Tip")
        # Simulate enter and leave events to trigger tooltip display and hide
        widget.event_generate('<Enter>')
        widget.event_generate('<Leave>')

    @patch('main.os.path.exists')
    @patch('main.messagebox.showinfo')
    @patch('main.compression.compress_jpeg')
    def test_compress_image(self, mock_compress_jpeg, mock_showinfo, mock_exists):
        mock_exists.return_value = True
        filedialog.askopenfilename = MagicMock(return_value="test_input.jpg")
        filedialog.asksaveasfilename = MagicMock(return_value="test_output.jpg")
        format_var = tk.StringVar(value="JPEG")
        quality_scale = tk.Scale(self.root, from_=0, to_=100, orient=tk.HORIZONTAL)
        quality_scale.set(85)
        tiff_compression_var = tk.StringVar(value="tiff_lzw")

        compress_image(quality_scale)

        mock_showinfo.assert_called_once_with("Success", "Image compressed and saved as test_output.jpg")
        mock_compress_jpeg.assert_called_once_with("test_input.jpg", "test_output.jpg", 85)

    @patch('main.messagebox.showwarning')
    def test_compress_image_no_input_file(self, mock_showwarning):
        filedialog.askopenfilename = MagicMock(return_value="")
        format_var = tk.StringVar(value="JPEG")
        quality_scale = tk.Scale(self.root, from_=0, to_=100, orient=tk.HORIZONTAL)
        quality_scale.set(85)
        tiff_compression_var = tk.StringVar(value="tiff_lzw")

        compress_image(quality_scale)

        mock_showwarning.assert_called_once_with("Input Error", "No input file selected.")

    @patch('main.messagebox.showwarning')
    def test_compress_image_no_output_file(self, mock_showwarning):
        filedialog.askopenfilename = MagicMock(return_value="test_input.jpg")
        filedialog.asksaveasfilename = MagicMock(return_value="")
        format_var = tk.StringVar(value="JPEG")
        quality_scale = tk.Scale(self.root, from_=0, to_=100, orient=tk.HORIZONTAL)
        quality_scale.set(85)
        tiff_compression_var = tk.StringVar(value="tiff_lzw")

        compress_image(quality_scale)

        mock_showwarning.assert_called_once_with("Output Error", "No output file selected.")

    @patch('main.os.path.isfile')
    @patch('main.messagebox.showerror')
    def test_compress_image_invalid_input_file(self, mock_showerror, mock_isfile):
        mock_isfile.return_value = False
        filedialog.askopenfilename = MagicMock(return_value="invalid_input.jpg")
        format_var = tk.StringVar(value="JPEG")
        quality_scale = tk.Scale(self.root, from_=0, to_=100, orient=tk.HORIZONTAL)
        quality_scale.set(85)
        tiff_compression_var = tk.StringVar(value="tiff_lzw")

        compress_image(quality_scale)

        mock_showerror.assert_called_once_with("File Error", "Input file does not exist.")

    @patch('main.messagebox.showerror')
    def test_compress_image_invalid_quality(self, mock_showerror):
        filedialog.askopenfilename = MagicMock(return_value="test_input.jpg")
        filedialog.asksaveasfilename = MagicMock(return_value="test_output.jpg")
        format_var = tk.StringVar(value="JPEG")
        quality_scale = tk.Scale(self.root, from_=0, to_=100, orient=tk.HORIZONTAL)
        quality_scale.set(150)
        tiff_compression_var = tk.StringVar(value="tiff_lzw")

        compress_image(quality_scale)

        mock_showerror.assert_called_once_with("Quality Error", "Quality must be between 0 and 100.")

    @patch('main.compression.compress_jpeg', side_effect=Exception("Test Exception"))
    @patch('main.messagebox.showerror')
    def test_compress_image_exception_handling(self, mock_showerror, mock_compress_jpeg):
        filedialog.askopenfilename = MagicMock(return_value="test_input.jpg")
        filedialog.asksaveasfilename = MagicMock(return_value="test_output.jpg")
        format_var = tk.StringVar(value="JPEG")
        quality_scale = tk.Scale(self.root, from_=0, to_=100, orient=tk.HORIZONTAL)
        quality_scale.set(85)
        tiff_compression_var = tk.StringVar(value="tiff_lzw")

        compress_image(quality_scale)

        mock_showerror.assert_called_once_with("Error", "Failed to compress image: Test Exception")

if __name__ == '__main__':
    unittest.main()
