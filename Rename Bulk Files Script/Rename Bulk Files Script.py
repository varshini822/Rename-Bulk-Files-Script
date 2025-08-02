import os
import tkinter as tk
from tkinter import filedialog, messagebox

class BulkRenamerApp:
    def __init__(self, root):
        self.root = root
        root.title("📝 Bulk File Renamer")
        root.geometry("540x520")
        root.resizable(False, False)
        root.configure(bg="#eaf6ff")

        # Title
        tk.Label(root, text="📁 Bulk File Renamer", font=("Helvetica", 18, "bold"), bg="#eaf6ff").pack(pady=10)

        # Folder selection
        frame1 = tk.Frame(root, bg="#eaf6ff")
        frame1.pack(pady=5)
        self.folder_path = tk.StringVar()
        tk.Entry(frame1, textvariable=self.folder_path, width=45).pack(side=tk.LEFT, padx=5)
        tk.Button(frame1, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)

        # Base name
        tk.Label(root, text="📝 Base Filename:", bg="#eaf6ff").pack(pady=(15, 0))
        self.base_name = tk.Entry(root, width=30)
        self.base_name.pack()

        # Extension filter
        tk.Label(root, text="📄 Filter by Extension (e.g., .txt):", bg="#eaf6ff").pack(pady=(15, 0))
        self.extension_entry = tk.Entry(root, width=20)
        self.extension_entry.pack()

        # Start Number
        tk.Label(root, text="🔢 Start Number (optional):", bg="#eaf6ff").pack(pady=(15, 0))
        self.start_number = tk.Entry(root, width=10)
        self.start_number.insert(0, "1")
        self.start_number.pack()

        # Preview label
        tk.Label(root, text="🔍 Preview Renamed Files:", bg="#eaf6ff").pack(pady=(15, 0))
        self.preview = tk.Text(root, height=8, width=63, state=tk.DISABLED)
        self.preview.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(root, bg="#eaf6ff")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Preview", command=self.preview_files, bg="#0275d8", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Rename", command=self.rename_files, bg="#5cb85c", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_preview, bg="#f0ad4e", fg="white", width=10).pack(side=tk.LEFT, padx=5)

        # Status message
        self.status_label = tk.Label(root, text="", fg="blue", bg="#eaf6ff", font=("Helvetica", 10, "italic"))
        self.status_label.pack(pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def clear_preview(self):
        self.preview.configure(state=tk.NORMAL)
        self.preview.delete(1.0, tk.END)
        self.preview.configure(state=tk.DISABLED)
        self.status_label.config(text="Preview cleared.")

    def preview_files(self):
        self.preview.configure(state=tk.NORMAL)
        self.preview.delete(1.0, tk.END)

        folder = self.folder_path.get()
        base = self.base_name.get().strip()
        extension = self.extension_entry.get().strip()
        start = self.start_number.get().strip()

        if not folder or not base:
            messagebox.showwarning("Input Error", "Please provide a folder and base filename.")
            return

        try:
            start_num = int(start) if start.isdigit() else 1
            files = os.listdir(folder)
            count = 0

            for filename in files:
                full_path = os.path.join(folder, filename)
                if os.path.isfile(full_path):
                    ext = os.path.splitext(filename)[1]
                    if extension and ext.lower() != extension.lower():
                        continue
                    new_name = f"{base}_{start_num + count}{ext}"
                    self.preview.insert(tk.END, f"{filename} ➜ {new_name}\n")
                    count += 1

            self.preview.configure(state=tk.DISABLED)

            if count == 0:
                self.status_label.config(text="No matching files found.")
            else:
                self.status_label.config(text=f"{count} file(s) ready to rename.")
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {e}")

    def rename_files(self):
        folder = self.folder_path.get()
        base = self.base_name.get().strip()
        extension = self.extension_entry.get().strip()
        start = self.start_number.get().strip()

        if not folder or not base:
            messagebox.showwarning("Input Error", "Please provide a folder and base filename.")
            return

        try:
            start_num = int(start) if start.isdigit() else 1
            files = os.listdir(folder)
            count = 0

            for filename in files:
                full_path = os.path.join(folder, filename)
                if os.path.isfile(full_path):
                    ext = os.path.splitext(filename)[1]
                    if extension and ext.lower() != extension.lower():
                        continue
                    new_name = f"{base}_{start_num + count}{ext}"
                    os.rename(full_path, os.path.join(folder, new_name))
                    count += 1

            self.status_label.config(text=f"✅ Successfully renamed {count} files.")
            self.preview.configure(state=tk.NORMAL)
            self.preview.insert(tk.END, "\n✅ Rename complete.\n")
            self.preview.configure(state=tk.DISABLED)
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {e}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BulkRenamerApp(root)
    root.mainloop()
