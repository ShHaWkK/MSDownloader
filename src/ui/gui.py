import tkinter as tk
from tkinter import ttk, messagebox
from downloader import Downloader
import logging

logger = logging.getLogger(__name__)

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MSDownloader")
        self.downloader = Downloader()

        self.url_entry = ttk.Entry(self.root, width=50)
        self.url_entry.pack(pady=10)

        self.quality_var = tk.StringVar(value="best")
        self.quality_combo = ttk.Combobox(self.root, textvariable=self.quality_var)
        self.quality_combo['values'] = ('best', '1080p', '720p', '480p', '360p')
        self.quality_combo.pack(pady=5)

        self.download_button = ttk.Button(self.root, text="Download", command=self.download)
        self.download_button.pack(pady=5)

    def download(self):
        url = self.url_entry.get()
        quality = self.quality_var.get()
        
        logger.info(f"Attempting download - URL: {url}, Quality: {quality}")
        
        if url:
            title = self.downloader.download(url, quality=quality)
            if title:
                messagebox.showinfo("Success", f"Successfully downloaded: {title}")
            else:
                messagebox.showerror("Error", "Download failed.")
        else:
            messagebox.showwarning("Warning", "Please enter a URL.")

    def run(self):
        self.root.mainloop()
