from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os
import fitz  # PyMuPDF

translations = {
    "en": {
        "merge_pdfs": "Enter the PDF file names to merge (comma-separated): ",
        "output_file": "Enter the output file name: ",
        "merge_success": "Files merged successfully into: ",
        "split_pdf": "Enter the PDF file name: ",
        "start_page": "Enter the start page number (starts from 0): ",
        "end_page": "Enter the end page number: ",
        "split_success": "File split successfully into: ",
        "extract_text": "Enter the PDF file name: ",
        "text_from_page": "--- Text from page ",
        "encrypt_pdf": "Enter the PDF file name: ",
        "password": "Enter the password: ",
        "encrypt_success": "File encrypted successfully: ",
        "decrypt_pdf": "Enter the encrypted PDF file name: ",
        "decrypt_success": "File decrypted successfully: ",
        "incorrect_password": "Incorrect password!",
        "rotate_pdf": "Enter the PDF file name: ",
        "rotation_angle": "Enter the rotation angle (90, 180, 270): ",
        "rotate_success": "Pages rotated successfully in: ",
        "add_watermark": "Enter the PDF file name: ",
        "watermark_file": "Enter the watermark PDF file name: ",
        "watermark_success": "Watermark added successfully to: ",
        "compress_pdf": "Enter the PDF file name: ",
        "compress_success": "PDF compressed successfully: ",
        "extract_images": "Enter the PDF file name: ",
        "output_folder": "Enter the output folder: ",
        "extract_images_success": "Images extracted successfully to: ",
        "add_metadata": "Enter the PDF file name: ",
        "title": "Enter the title: ",
        "author": "Enter the author: ",
        "subject": "Enter the subject: ",
        "metadata_success": "Metadata added successfully to: ",
        "remove_metadata": "Enter the PDF file name: ",
        "remove_metadata_success": "Metadata removed successfully from: ",
        "rearrange_pages": "Enter the PDF file name: ",
        "page_order": "Enter the new page order (comma-separated): ",
        "rearrange_success": "Pages rearranged successfully in: ",
        "extract_pages": "Enter the PDF file name: ",
        "page_numbers": "Enter the page numbers to extract (comma-separated): ",
        "extract_pages_success": "Pages extracted successfully to: ",
        "error_occurred": "An error occurred: ",
        "function_menu": "\n--- Function Menu ---",
        "merge_files": "1. Merge PDF files",
        "split_file": "2. Split PDF file",
        "extract_text_from_pdf": "3. Extract text from PDF",
        "encrypt_file": "4. Encrypt PDF file",
        "decrypt_file": "5. Decrypt PDF file",
        "rotate_pages": "6. Rotate PDF pages",
        "add_watermark_to_pdf": "7. Add watermark to PDF",
        "compress_file": "8. Compress PDF file",
        "extract_images_from_pdf": "9. Extract images from PDF",
        "add_metadata_to_pdf": "10. Add metadata to PDF",
        "remove_metadata_from_pdf": "11. Remove metadata from PDF",
        "rearrange_pdf_pages": "12. Rearrange PDF pages",
        "extract_specific_pages": "13. Extract specific pages from PDF",
        "exit": "16. Exit",
        "enter_function_number": "Enter the function number: ",
        "invalid_choice": "Invalid choice. Please try again.",
        "goodbye": "Goodbye!"
    },
    "fr": {
        "merge_pdfs": "Entrez les noms des fichiers PDF à fusionner (séparés par des virgules) : ",
        "output_file": "Entrez le nom du fichier de sortie : ",
        "merge_success": "Fichiers fusionnés avec succès dans : ",
        "split_pdf": "Entrez le nom du fichier PDF : ",
        "start_page": "Entrez le numéro de la page de début (commence à 0) : ",
        "end_page": "Entrez le numéro de la page de fin : ",
        "split_success": "Fichier divisé avec succès dans : ",
        "extract_text": "Entrez le nom du fichier PDF : ",
        "text_from_page": "--- Texte de la page ",
        "encrypt_pdf": "Entrez le nom du fichier PDF : ",
        "password": "Entrez le mot de passe : ",
        "encrypt_success": "Fichier crypté avec succès : ",
        "decrypt_pdf": "Entrez le nom du fichier PDF crypté : ",
        "decrypt_success": "Fichier décrypté avec succès : ",
        "incorrect_password": "Mot de passe incorrect !",
        "rotate_pdf": "Entrez le nom du fichier PDF : ",
        "rotation_angle": "Entrez l'angle de rotation (90, 180, 270) : ",
        "rotate_success": "Pages tournées avec succès dans : ",
        "add_watermark": "Entrez le nom du fichier PDF : ",
        "watermark_file": "Entrez le nom du fichier PDF de filigrane : ",
        "watermark_success": "Filigrane ajouté avec succès à : ",
        "compress_pdf": "Entrez le nom du fichier PDF : ",
        "compress_success": "PDF compressé avec succès : ",
        "extract_images": "Entrez le nom du fichier PDF : ",
        "output_folder": "Entrez le dossier de sortie : ",
        "extract_images_success": "Images extraites avec succès dans : ",
        "add_metadata": "Entrez le nom du fichier PDF : ",
        "title": "Entrez le titre : ",
        "author": "Entrez l'auteur : ",
        "subject": "Entrez le sujet : ",
        "metadata_success": "Métadonnées ajoutées avec succès à : ",
        "remove_metadata": "Entrez le nom du fichier PDF : ",
        "remove_metadata_success": "Métadonnées supprimées avec succès de : ",
        "rearrange_pages": "Entrez le nom du fichier PDF : ",
        "page_order": "Entrez le nouvel ordre des pages (séparés par des virgules) : ",
        "rearrange_success": "Pages réorganisées avec succès dans : ",
        "extract_pages": "Entrez le nom du fichier PDF : ",
        "page_numbers": "Entrez les numéros de pages à extraire (séparés par des virgules) : ",
        "extract_pages_success": "Pages extraites avec succès dans : ",
        "error_occurred": "Une erreur s'est produite : ",
        "function_menu": "\n--- Menu des fonctions ---",
        "merge_files": "1. Fusionner des fichiers PDF",
        "split_file": "2. Diviser un fichier PDF",
        "extract_text_from_pdf": "3. Extraire du texte d'un PDF",
        "encrypt_file": "4. Crypter un fichier PDF",
        "decrypt_file": "5. Décrypter un fichier PDF",
        "rotate_pages": "6. Tourner les pages d'un PDF",
        "add_watermark_to_pdf": "7. Ajouter un filigrane à un PDF",
        "compress_file": "8. Compresser un fichier PDF",
        "extract_images_from_pdf": "9. Extraire des images d'un PDF",
        "add_metadata_to_pdf": "10. Ajouter des métadonnées à un PDF",
        "remove_metadata_from_pdf": "11. Supprimer les métadonnées d'un PDF",
        "rearrange_pdf_pages": "12. Réorganiser les pages d'un PDF",
        "extract_specific_pages": "13. Extraire des pages spécifiques d'un PDF",
        "exit": "16. Quitter",
        "enter_function_number": "Entrez le numéro de la fonction : ",
        "invalid_choice": "Choix invalide. Veuillez réessayer.",
        "goodbye": "Au revoir !"
    },
        "ar": {
        "merge_pdfs": "أدخل أسماء ملفات PDF للفصل (مفصولة بفواصل): ",
        "output_file": "أدخل اسم الملف الناتج: ",
        "merge_success": "تم دمج الملفات بنجاح في: ",
        "split_pdf": "أدخل اسم ملف PDF: ",
        "start_page": "أدخل رقم الصفحة الأولى (يبدأ من 0): ",
        "end_page": "أدخل رقم الصفحة الأخيرة: ",
        "split_success": "تم تقسيم الملف إلى: ",
        "extract_text": "أدخل اسم ملف PDF: ",
        "text_from_page": "--- نص الصفحة ",
        "encrypt_pdf": "أدخل اسم ملف PDF: ",
        "password": "أدخل كلمة المرور: ",
        "encrypt_success": "تم تشفير الملف: ",
        "decrypt_pdf": "أدخل اسم ملف PDF المشفر: ",
        "decrypt_success": "تم فك تشفير الملف: ",
        "incorrect_password": "كلمة المرور غير صحيحة!",
        "rotate_pdf": "أدخل اسم ملف PDF: ",
        "rotation_angle": "أدخل زاوية الدوران (90، 180، 270): ",
        "rotate_success": "تم تدوير الصفحات بنجاح في: ",
        "add_watermark": "أدخل اسم ملف PDF: ",
        "watermark_file": "أدخل اسم ملف PDF العلامة المائية: ",
        "watermark_success": "تمت إضافة العلامة المائية بنجاح إلى: ",
        "compress_pdf": "أدخل اسم ملف PDF: ",
        "compress_success": "تم ضغط ملف PDF بنجاح: ",
        "extract_images": "أدخل اسم ملف PDF: ",
        "output_folder": "أدخل المجلد الناتج: ",
        "extract_images_success": "تم استخراج الصور بنجاح إلى: ",
        "add_metadata": "أدخل اسم ملف PDF: ",
        "title": "أدخل العنوان: ",
        "author": "أدخل المؤلف: ",
        "subject": "أدخل الموضوع: ",
        "metadata_success": "تمت إضافة البيانات الوصفية بنجاح إلى: ",
        "remove_metadata": "أدخل اسم ملف PDF: ",
        "remove_metadata_success": "تمت إزالة البيانات الوصفية بنجاح من: ",
        "rearrange_pages": "أدخل اسم ملف PDF: ",
        "page_order": "أدخل ترتيب الصفحات الجديد (مفصولة بفواصل): ",
        "rearrange_success": "تمت إعادة ترتيب الصفحات بنجاح في: ",
        "extract_pages": "أدخل اسم ملف PDF: ",
        "page_numbers": "أدخل أرقام الصفحات لاستخراجها (مفصولة بفواصل): ",
        "extract_pages_success": "تم استخراج الصفحات بنجاح إلى: ",
        "error_occurred": "حدث خطأ: ",
         "function_menu": "\n--- قائمة الوظائف ---",
        "merge_files": "1. دمج ملفات PDF",
        "split_file": "2. تقسيم ملف PDF",
        "extract_text_from_pdf": "3. استخراج النصوص من PDF",
        "encrypt_file": "4. تشفير ملف PDF",
        "decrypt_file": "5. فك تشفير ملف PDF",
        "rotate_pages": "6. تدوير صفحات PDF",
        "add_watermark_to_pdf": "7. إضافة علامة مائية إلى PDF",
         "compress_file": "8. ضغط ملف PDF",
        "extract_images_from_pdf": "9. استخراج الصور من PDF",
        "add_metadata_to_pdf": "10. إضافة بيانات وصفية إلى PDF",
        "remove_metadata_from_pdf": "11. إزالة البيانات الوصفية من PDF",
         "rearrange_pdf_pages": "12. إعادة ترتيب صفحات PDF",
        "extract_specific_pages": "13. استخراج صفحات محددة من PDF",
        "exit": "16. خروج",
        "enter_function_number": "أدخل رقم الوظيفة: ",
        "invalid_choice": "اختيار غير صحيح. حاول مرة أخرى.",
         "goodbye": "وداعًا!"
    }
}



def get_translation(lang, key):
    return translations[lang].get(key, key)

def get_static_input_files():
    return ["1.pdf", "2.pdf"]


def merge_pdfs(lang):
    print("mergeing 1.pdf and 2.pdf file from the server !")
    pdf_list = get_static_input_files()
    output_file = "output_file" + ".pdf"
    merger = PdfMerger()
    try:
        for pdf in pdf_list:
            pdf = pdf.strip()
            if pdf:
                merger.append(pdf)
        merger.write(output_file)
        print(get_translation(lang, "merge_success") + output_file)
    except Exception as e:
        print(get_translation(lang, "error_occurred") + str(e))
    finally:
        merger.close()


def split_pdf(lang):
    print("spliting 1.pdf file from the server !")
    input_file = get_static_input_files()[0]
    try:
        start = int(input(get_translation(lang, "start_page")))
        end = int(input(get_translation(lang, "end_page")))
        output_file = "output_file" + ".pdf"
        reader = PdfReader(input_file)
        writer = PdfWriter()
        for page in range(start, end):
            writer.add_page(reader.pages[page])
        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)
        print(get_translation(lang, "split_success") + output_file)
    except Exception as e:
        print(get_translation(lang, "error_occurred") + str(e))


def extract_text(lang):
    print("extract text from 1.pdf file from the server !")
    input_file = get_static_input_files()[0]
    output_file = "output_file" + ".txt"
    reader = PdfReader(input_file)
    try:
        with open(output_file, "w", encoding="utf-8") as txt_file:
            for page_num, page in enumerate(reader.pages):
                txt_file.write(get_translation(lang, "text_from_page") + str(page_num + 1) + " ---\n")
                txt_file.write(page.extract_text() + "\n")
        print(get_translation(lang, "extract_pages_success") + output_file)
    except Exception as e:
        print(get_translation(lang, "error_occurred") + str(e))


def encrypt_pdf(lang):
    print("encrypting 1.pdf file from the server !")
    input_file = get_static_input_files()[0]
    password = input(get_translation(lang, "password"))
    output_file = "output_file" + ".pdf"
    reader = PdfReader(input_file)
    writer = PdfWriter()
    try:
        writer.append(reader)
        writer.encrypt(password)
        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)
        print(get_translation(lang, "encrypt_success") + output_file)
    except Exception as e:
        print(get_translation(lang, "error_occurred") + str(e))


def decrypt_pdf(lang):
    print("decrypting 1.pdf file from the server !")
    input_file = get_static_input_files()[0]
    password = input(get_translation(lang, "password"))
    output_file = "output_file" + ".pdf"
    reader = PdfReader(input_file)
    writer = PdfWriter()
    try:
        if reader.decrypt(password):
            writer.append(reader)
            with open(output_file, "wb") as output_pdf:
                writer.write(output_pdf)
            print(get_translation(lang, "decrypt_success") + output_file)
        else:
            print(get_translation(lang, "incorrect_password"))
    except Exception as e:
        print(get_translation(lang, "error_occurred") + str(e))


def rotate_pdf(lang):
    print("rotateing 1.pdf file from the server !")
    input_file = get_static_input_files()[0]
    rotation = int(input(get_translation(lang, "rotation_angle")))
    output_file = "output_file" + ".pdf"
    reader = PdfReader(input_file)
    writer = PdfWriter()
    try:
        for page in reader.pages:
            page.rotate(rotation)
            writer.add_page(page)
        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)
        print(get_translation(lang, "rotate_success") + output_file)
    except Exception as e:
        print(get_translation(lang, "error_occurred") + str(e))


def add_watermark(lang):
    print("adding watermark to 1.pdf file from the server !")
    input_file = get_static_input_files()[0]
    print("adding watermark to 2.pdf file from the server !")
    watermark_file = get_static_input_files()[1]
    output_file = "output_file" + ".pdf"
    reader = PdfReader(input_file)
    watermark = PdfReader(watermark_file)
    writer = PdfWriter()
    try:
        watermark_page = watermark.pages[0]
        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)
        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)
        print(get_translation(lang, "watermark_success") + output_file)
    except Exception as e:
        print(get_translation(lang, "error_occurred") + str(e))


def compress_pdf(lang):
    print("compressing 1.pdf file from the server !")
    input_file = get_static_input_files()[0]
    output_file = "output_file" + ".pdf"
    reader = PdfReader(input_file)
    writer = PdfWriter()
    try:
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata(reader.metadata)
        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)
        print(get_translation(lang, "compress_success") + output_file)
    except Exception as e:
        print(get_translation(lang, "error_occurred") + str(e))


def extract_images(lang):
    print("Extracting images from 1.pdf file from the server!")
    input_file = get_static_input_files()[0]
    output_folder = "images_1_pdf"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_document = fitz.open(input_file)
    
    try:
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            images = page.get_images(full=True)

            for img_index, img in enumerate(images):
                xref = img[0]
                image = pdf_document.extract_image(xref)
                image_data = image["image"]
                image_filename = f"{output_folder}/image_{page_num + 1}_{img_index + 1}.jpg"
                
                with open(image_filename, "wb") as img_file:
                    img_file.write(image_data)
                
        print(get_translation(lang, "extract_images_success") + output_folder)
    except Exception as e:
        print(get_translation(lang, "error_occurred") + str(e))
    finally:
        pdf_document.close()


def add_metadata(lang):
    print("adding metadata to 1.pdf file from the server !")
    input_file = get_static_input_files()[0]
    output_file = "output_file" + ".pdf"
    title = input(get_translation(lang, "title"))
    author = input(get_translation(lang, "author"))
    subject = input(get_translation(lang, "subject"))
    reader = PdfReader(input_file)
    writer = PdfWriter()
    try:
        writer.append(reader)
        writer.add_metadata({
            "/Title": title,
            "/Author": author,
            "/Subject": subject
        })
        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)
        print(get_translation(lang, "metadata_success") + output_file)
    except Exception as e:
        print(get_translation(lang, "error_occurred") + str(e))

def view_metadata(lang):
    try:
        reader = PdfReader("output_file.pdf")
        metadata = reader.metadata
        print("Metadata for file:", "output_file.pdf")
        print("Title:", metadata.get("/Title", "No Title"))
        print("Author:", metadata.get("/Author", "No Author"))
        print("Subject:", metadata.get("/Subject", "No Subject"))
    except Exception as e:
        print(f"Error occurred while reading metadata: {str(e)}")

def remove_metadata(lang):
    print("removing metadata from 1.pdf file from the server !")
    input_file = get_static_input_files()[0]
    output_file = "output_file" + ".pdf"
    reader = PdfReader(input_file)
    writer = PdfWriter()
    try:
        writer.append(reader)
        writer.add_metadata({})
        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)
        print(get_translation(lang, "remove_metadata_success") + output_file)
    except Exception as e:
         print(get_translation(lang, "error_occurred") + str(e))


def rearrange_pages(lang):
    print("rearranging pages of 1.pdf file from the server !")
    input_file = get_static_input_files()[0]
    output_file = "output_file" + ".pdf"
    page_order = input(get_translation(lang, "page_order")).split(',')
    reader = PdfReader(input_file)
    writer = PdfWriter()
    try:
        for page_num in page_order:
            writer.add_page(reader.pages[int(page_num.strip())])
        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)
        print(get_translation(lang, "rearrange_success") + output_file)
    except Exception as e:
        print(get_translation(lang, "error_occurred") + str(e))


def extract_pages(lang):
    print("extracting pages of 1.pdf file from the server !")
    input_file = get_static_input_files()[0]
    output_file = "output_file" + ".pdf"
    page_numbers = input(get_translation(lang, "page_numbers")).split(',')
    reader = PdfReader(input_file)
    writer = PdfWriter()
    try:
        for page_num in page_numbers:
            writer.add_page(reader.pages[int(page_num.strip())])
        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)
        print(get_translation(lang, "extract_pages_success") + output_file)
    except Exception as e:
        print(get_translation(lang, "error_occurred") + str(e))

def main():
    lang = input("Choose language (en/fr/ar): ").strip().lower()
    if lang not in translations:
        print("Invalid language choice. Defaulting to English.")
        lang = "en"

    while True:
        print(get_translation(lang, "function_menu"))
        print(get_translation(lang, "merge_files"))
        print(get_translation(lang, "split_file"))
        print(get_translation(lang, "extract_text_from_pdf"))
        print(get_translation(lang, "encrypt_file"))
        print(get_translation(lang, "decrypt_file"))
        print(get_translation(lang, "rotate_pages"))
        print(get_translation(lang, "add_watermark_to_pdf"))
        print(get_translation(lang, "compress_file"))
        print(get_translation(lang, "extract_images_from_pdf"))
        print(get_translation(lang, "add_metadata_to_pdf"))
        print(get_translation(lang, "remove_metadata_from_pdf"))
        print(get_translation(lang, "rearrange_pdf_pages"))
        print(get_translation(lang, "extract_specific_pages"))
        print("14. View metadata")
        print("15. View Simalrity")
        print(get_translation(lang, "exit"))
        choice = input(get_translation(lang, "enter_function_number"))

        if choice == "1":
            merge_pdfs(lang)
        elif choice == "2":
            split_pdf(lang)
        elif choice == "3":
            extract_text(lang)
        elif choice == "4":
            encrypt_pdf(lang)
        elif choice == "5":
            decrypt_pdf(lang)
        elif choice == "6":
            rotate_pdf(lang)
        elif choice == "7":
            add_watermark(lang)
        elif choice == "8":
             compress_pdf(lang)
        elif choice == "9":
            extract_images(lang)
        elif choice == "10":
            add_metadata(lang)
        elif choice == "11":
            remove_metadata(lang)
        elif choice == "12":
            rearrange_pages(lang)
        elif choice == "13":
            extract_pages(lang)
        elif choice == "14":
            view_metadata(lang)
        elif choice == "15":
            import similarity_project.app as app
            app.print_results()
        elif choice == "16":
            print(get_translation(lang, "goodbye"))
            break

        else:
            print(get_translation(lang, "invalid_choice"))

if __name__ == "__main__":
    main()


