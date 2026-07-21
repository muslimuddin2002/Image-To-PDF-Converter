import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from PIL import Image
import os


class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.root.geometry("500x600")

        self.image_paths = []
        self.output_pdf_name = tk.StringVar()

        self.initialize_ui()

    def initialize_ui(self):
        title = tk.Label(
            self.root,
            text="Image to PDF Converter",
            font=("Helvetica", 16, "bold")
        )
        title.pack(pady=10)

        select_btn = tk.Button(
            self.root,
            text="Select Images",
            command=self.select_images,
            width=20
        )
        select_btn.pack(pady=10)

        self.selected_images_listbox = tk.Listbox(
            self.root,
            width=60,
            height=15
        )
        self.selected_images_listbox.pack(padx=10, pady=10)

        tk.Label(
            self.root,
            text="Enter Output PDF Name"
        ).pack()

        tk.Entry(
            self.root,
            textvariable=self.output_pdf_name,
            width=40,
            justify="center"
        ).pack(pady=5)

        convert_btn = tk.Button(
            self.root,
            text="Convert to PDF",
            command=self.convert_images_to_pdf,
            width=20
        )
        convert_btn.pack(pady=20)

    def select_images(self):
        paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.webp")
            ]
        )

        if not paths:
            return

        # আগের ছবি মুছে নতুনগুলো রাখবে
        self.image_paths = list(paths)

        self.selected_images_listbox.delete(0, tk.END)

        for path in self.image_paths:
            self.selected_images_listbox.insert(
                tk.END,
                os.path.basename(path)
            )

    def convert_images_to_pdf(self):
        if not self.image_paths:
            messagebox.showwarning(
                "Warning",
                "Please select images first."
            )
            return

        pdf_name = self.output_pdf_name.get().strip()

        if pdf_name == "":
            pdf_name = "output"

        output_pdf = pdf_name + ".pdf"

        pdf = canvas.Canvas(output_pdf, pagesize=(612, 792))

        for image_path in self.image_paths:

            img = Image.open(image_path)

            width, height = img.size

            available_width = 540
            available_height = 720

            scale = min(
                available_width / width,
                available_height / height
            )

            new_width = width * scale
            new_height = height * scale

            x = (612 - new_width) / 2
            y = (792 - new_height) / 2

            pdf.drawInlineImage(
                img,
                x,
                y,
                width=new_width,
                height=new_height
            )

            pdf.showPage()

        pdf.save()

        messagebox.showinfo(
            "Success",
            f"PDF saved successfully!\n\n{output_pdf}"
        )


def main():
    root = tk.Tk()
    ImageToPDFConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()