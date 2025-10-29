import os
import re
import sys
import shutil
import logging
import unicodedata
from pathlib import Path
from tkinter import Tk, Label, Entry, Button, Frame, Listbox, END, StringVar, messagebox, PhotoImage
from tkinter import ttk
from logging.handlers import RotatingFileHandler

# --- Dependencias de conversión ---
import img2pdf                    # Imágenes → PDF (jpg/png)
from pypdf import PdfReader, PdfWriter  # Merge PDFs

# Office -> PDF (Windows + MS Office)
try:
    import win32com.client as win32  # pywin32
    HAS_WIN32 = True
except Exception:
    HAS_WIN32 = False


# =============================
# Configuración general
# =============================
APP_VERSION = "v1.2.1"
INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")
TEMP_DIR = Path("temp")
LOG_DIR = Path("logs")
ASSETS_DIR = Path("assets")  # coloca aquí tus imágenes
LOGO_EMPRESA = ASSETS_DIR / "logo_empresa.png"   # <-- agrega tus imágenes si quieres
LOGO_CAMPANA = ASSETS_DIR / "logo_campana.png"   # <-- agrega tus imágenes si quieres
LOGO_EXPANSION = ASSETS_DIR / "Expansión.png"   # Logo de Expansión

# Extensiones de archivos soportadas por categoría
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
WORD_EXTS = {".doc", ".docx"}
EXCEL_EXTS = {".xls", ".xlsx"}
PDF_EXTS = {".pdf"}

ALLOWED_EXTS = IMAGE_EXTS | WORD_EXTS | EXCEL_EXTS | PDF_EXTS
INVALID_FS_CHARS = r'<>:"/\\|?*'  # Windows

# Archivos que se deben excluir del procesamiento
EXCLUDED_FILES = {"README.md", "readme.md", "README.txt", "readme.txt"}

# Constantes para formatos de exportación Office
WD_FORMAT_PDF = 17  # Word PDF export format
XL_TYPE_PDF = 0     # Excel PDF export format


# =============================
# Logging
# =============================
LOG_DIR.mkdir(parents=True, exist_ok=True)
logger = logging.getLogger("consolidador")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_DIR / "app.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(fmt)
logger.addHandler(handler)


# =============================
# Utilidades
# =============================
def resource_path(relative: Path) -> str:
    """Compat con PyInstaller --onefile: devuelve la ruta real del recurso empaquetado."""
    try:
        base_path = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    except Exception:
        base_path = Path(".")
    return str(base_path / relative)


def ensure_dirs():
    for d in (INPUT_DIR, OUTPUT_DIR, TEMP_DIR, ASSETS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def sanitize_component(s: str) -> str:
    """Limpia nombre: quita inválidos, colapsa espacios y normaliza acentos a ASCII."""
    s = s.strip()
    s = "".join("_" if c in INVALID_FS_CHARS else c for c in s)
    s = re.sub(r"\s+", " ", s)
    # Normaliza tildes/acentos para minimizar problemas en FS o con otros sistemas
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return s


def final_pdf_name(ident: str, cliente: str, reembolso: str) -> str:
    ident = sanitize_component(ident)
    cliente = sanitize_component(cliente)
    reembolso = sanitize_component(reembolso)
    base = f"{ident}_{cliente}_{reembolso}".strip("_ ").replace(" ", "_")
    return base + ".pdf"


def get_supported_extensions_display() -> str:
    """
    Retorna una cadena legible con las extensiones soportadas agrupadas por tipo.
    """
    return (f"PDF: {', '.join(sorted(PDF_EXTS))} | "
            f"Word: {', '.join(sorted(WORD_EXTS))} | "
            f"Excel: {', '.join(sorted(EXCEL_EXTS))} | "
            f"Imágenes: {', '.join(sorted(IMAGE_EXTS))}")


def list_input_files() -> list[Path]:
    if not INPUT_DIR.exists():
        return []
    files = []
    for f in INPUT_DIR.iterdir():
        if (f.is_file() and 
            f.suffix.lower() in ALLOWED_EXTS and 
            f.name not in EXCLUDED_FILES):
            files.append(f)
    files.sort(key=lambda p: p.name.lower())  # orden alfabético
    return files


# =============================
# Conversión a PDF por tipo
# =============================
def convert_image_to_pdf(src: Path, dst_pdf: Path):
    """Convierte JPG/PNG/TIF a PDF. Usa Pillow para TIFF multipágina; img2pdf para el resto."""
    dst_pdf.parent.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower()

    if ext in (".tif", ".tiff"):
        from PIL import Image  # import local: solo si hace falta
        frames = []
        im = Image.open(src)
        try:
            while True:
                frames.append(im.convert("RGB").copy())
                im.seek(im.tell() + 1)
        except EOFError:
            pass
        if not frames:
            raise RuntimeError(f"TIFF sin frames: {src.name}")
        frames[0].save(dst_pdf, save_all=True, append_images=frames[1:])
        logger.info(f"TIFF multipágina -> {dst_pdf.name}")
    else:
        with open(dst_pdf, "wb") as f_out:
            f_out.write(img2pdf.convert(str(src)))
        logger.info(f"Imagen convertida -> {dst_pdf.name}")


def convert_word_to_pdf(src: Path, dst_pdf: Path):
    """
    Convierte documentos Word (.doc/.docx) a PDF usando Microsoft Word vía COM.
    
    Args:
        src: Ruta del archivo Word de origen
        dst_pdf: Ruta donde guardar el PDF convertido
        
    Raises:
        RuntimeError: Si no está disponible win32com o MS Office
    """
    if not HAS_WIN32:
        raise RuntimeError("Conversión de documentos Word requiere Windows + pywin32 + MS Office.")
    
    word = None
    try:
        logger.info(f"Iniciando conversión Word -> PDF: {src.name}")
        word = win32.DispatchEx("Word.Application")
        word.Visible = False
        
        # Asegurar ruta absoluta para MS Word
        src_absolute = src.resolve()
        dst_absolute = dst_pdf.resolve()
        
        logger.debug(f"Ruta absoluta origen: {src_absolute}")
        logger.debug(f"Ruta absoluta destino: {dst_absolute}")
        
        # Abrir documento (funciona tanto para .doc como .docx)
        doc = word.Documents.Open(str(src_absolute))
        
        # Exportar como PDF usando ruta absoluta
        doc.ExportAsFixedFormat(str(dst_absolute), WD_FORMAT_PDF)
        doc.Close(False)
        
        logger.info(f"Word -> PDF completado: {dst_pdf.name}")
        
    except Exception as e:
        logger.error(f"Error convirtiendo {src.name}: {e}")
        raise
    finally:
        if word:
            try:
                word.Quit()
            except Exception as e:
                logger.warning(f"Error cerrando Word: {e}")


def convert_excel_to_pdf(src: Path, dst_pdf: Path):
    """
    Convierte documentos Excel (.xls/.xlsx) a PDF usando Microsoft Excel vía COM.
    
    Args:
        src: Ruta del archivo Excel de origen
        dst_pdf: Ruta donde guardar el PDF convertido
        
    Raises:
        RuntimeError: Si no está disponible win32com o MS Office
    """
    if not HAS_WIN32:
        raise RuntimeError("Conversión de documentos Excel requiere Windows + pywin32 + MS Office.")
    
    excel = None
    try:
        logger.info(f"Iniciando conversión Excel -> PDF: {src.name}")
        excel = win32.DispatchEx("Excel.Application")
        excel.Visible = False
        
        # Asegurar ruta absoluta para MS Excel
        src_absolute = src.resolve()
        dst_absolute = dst_pdf.resolve()
        
        logger.debug(f"Ruta absoluta origen: {src_absolute}")
        logger.debug(f"Ruta absoluta destino: {dst_absolute}")
        
        # Abrir libro (funciona tanto para .xls como .xlsx)
        wb = excel.Workbooks.Open(str(src_absolute))
        
        # Exportar como PDF usando ruta absoluta
        wb.ExportAsFixedFormat(XL_TYPE_PDF, str(dst_absolute))
        wb.Close(False)
        
        logger.info(f"Excel -> PDF completado: {dst_pdf.name}")
        
    except Exception as e:
        logger.error(f"Error convirtiendo {src.name}: {e}")
        raise
    finally:
        if excel:
            try:
                excel.Quit()
            except Exception as e:
                logger.warning(f"Error cerrando Excel: {e}")


def copy_pdf(src: Path, dst_pdf: Path):
    dst_pdf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst_pdf)
    logger.info(f"PDF copiado: {dst_pdf.name}")


def convert_to_pdf(src: Path) -> Path | None:
    """
    Convierte un archivo permitido a PDF y devuelve la ruta del PDF temporal.
    
    Args:
        src: Ruta del archivo a convertir
        
    Returns:
        Path del PDF temporal creado, o None si la conversión falla
    """
    try:
        dst = TEMP_DIR / (src.stem + ".pdf")
        ext = src.suffix.lower()
        
        logger.info(f"Iniciando conversión: {src.name} ({ext})")
        
        if ext in IMAGE_EXTS:
            convert_image_to_pdf(src, dst)
        elif ext in PDF_EXTS:
            copy_pdf(src, dst)
        elif ext in WORD_EXTS:
            convert_word_to_pdf(src, dst)
        elif ext in EXCEL_EXTS:
            convert_excel_to_pdf(src, dst)
        else:
            raise RuntimeError(f"Extensión no soportada: {ext}")
            
        logger.info(f"Conversión exitosa: {src.name} -> {dst.name}")
        return dst
        
    except Exception as e:
        logger.exception(f"Error convirtiendo {src.name}: {e}")
        return None


# =============================
# Unión de PDFs
# =============================
def merge_pdfs(pdf_paths: list[Path], out_path: Path):
    writer = PdfWriter()
    for p in pdf_paths:
        try:
            reader = PdfReader(str(p))
            for page in reader.pages:
                writer.add_page(page)
        except Exception as e:
            logger.exception(f"Error leyendo {p.name}: {e}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        writer.write(f)
    logger.info(f"PDF final creado: {out_path.name}")


# =============================
# Interfaz (Tkinter)
# =============================
class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Consolidador de Archivos a PDF")
        self.geometry("760x560")
        self.resizable(False, False)

        ensure_dirs()

        # Header con branding
        header = Frame(self)
        header.pack(fill="x", pady=8, padx=16)

        # Título a la izquierda
        title_frame = Frame(header)
        title_frame.pack(side="left")
        Label(title_frame, text="Consolidador de Archivos a PDF", 
              font=("Segoe UI", 12, "bold")).pack(anchor="w")
        Label(title_frame, text=f"Versión {APP_VERSION}", 
              font=("Segoe UI", 9)).pack(anchor="w")

        # Logo de Expansión a la derecha
        logo_frame = Frame(header)
        logo_frame.pack(side="right")
        try:
            if LOGO_EXPANSION.exists():
                self.logo_expansion = PhotoImage(file=resource_path(LOGO_EXPANSION))
                Label(logo_frame, image=self.logo_expansion).pack()
        except Exception as e:
            logger.warning(f"No se pudo cargar logo de Expansión: {e}")

        # Logos adicionales (empresa y campaña) en la parte inferior del header
        branding = Frame(self)
        branding.pack(pady=4)
        try:
            if LOGO_EMPRESA.exists():
                self.logo_emp = PhotoImage(file=resource_path(LOGO_EMPRESA))
                Label(branding, image=self.logo_emp).pack(side="left", padx=8)
            if LOGO_CAMPANA.exists():
                self.logo_camp = PhotoImage(file=resource_path(LOGO_CAMPANA))
                Label(branding, image=self.logo_camp).pack(side="left", padx=8)
        except Exception as e:
            logger.warning(f"No se pudieron cargar logos adicionales: {e}")

        form = Frame(self)
        form.pack(pady=10, fill="x", padx=16)

        self.var_ident = StringVar()
        self.var_cliente = StringVar()
        self.var_reembolso = StringVar()

        Label(form, text="Número de identificación *").grid(row=0, column=0, sticky="w")
        Entry(form, textvariable=self.var_ident, width=40).grid(row=0, column=1, padx=8, pady=4)

        Label(form, text="Nombre del cliente *").grid(row=1, column=0, sticky="w")
        Entry(form, textvariable=self.var_cliente, width=40).grid(row=1, column=1, padx=8, pady=4)

        Label(form, text="Número de reembolso *").grid(row=2, column=0, sticky="w")
        Entry(form, textvariable=self.var_reembolso, width=40).grid(row=2, column=1, padx=8, pady=4)

        # Lista de archivos
        files_frame = Frame(self)
        files_frame.pack(pady=6, fill="both", expand=True, padx=16)
        Label(files_frame, text=f"Carpeta de entrada: {INPUT_DIR.resolve()}", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        Label(files_frame, text=f"Formatos soportados: {get_supported_extensions_display()}", 
              font=("Segoe UI", 8), fg="gray").pack(anchor="w", pady=(0, 5))

        self.listbox = Listbox(files_frame, height=12, width=100)
        self.listbox.pack(side="left", fill="both", expand=True)

        btns = Frame(files_frame)
        btns.pack(side="left", padx=8)
        Button(btns, text="Actualizar", command=self.reload_files).pack(fill="x", pady=2)
        Button(btns, text="Abrir INPUT", command=lambda: self.open_folder(INPUT_DIR)).pack(fill="x", pady=2)
        Button(btns, text="Abrir OUTPUT", command=lambda: self.open_folder(OUTPUT_DIR)).pack(fill="x", pady=2)

        # Progreso y acciones
        bottom = Frame(self)
        bottom.pack(pady=8)
        self.progress = ttk.Progressbar(bottom, length=500, mode="determinate")
        self.progress.pack(pady=4)
        self.btn_convert = Button(bottom, text="Convertir y Consolidar",
                                  command=self.run_process, width=30)
        self.btn_convert.pack(pady=6)

        # Leyenda PI
        Label(
            self,
            text="© 2025 La Ascensión S.A.  Todos los derechos reservados - Uso interno. Prohibida su reproducción sin autorización.",
            font=("Segoe UI", 8)
        ).pack(pady=4)

        self.reload_files()

    def reload_files(self):
        self.listbox.delete(0, END)
        files = list_input_files()
        if not files:
            self.listbox.insert(END, "(No hay documentos en la carpeta data/input)")
            self.btn_convert.configure(state="disabled")
        else:
            for f in files:
                self.listbox.insert(END, f.name)
            self.btn_convert.configure(state="normal")

    def open_folder(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                os.system(f"open \"{path}\"")
            else:
                os.system(f"xdg-open \"{path}\"")
        except Exception as e:
            messagebox.showwarning("Aviso", f"No se pudo abrir la carpeta:\n{e}")

    def validate_form(self) -> tuple[bool, str]:
        ident = self.var_ident.get().strip()
        cliente = self.var_cliente.get().strip()
        rem = self.var_reembolso.get().strip()
        if not ident or not cliente or not rem:
            return False, "Todos los campos marcados con * son obligatorios."

        invalid_char_pat = re.compile(f"[{re.escape(INVALID_FS_CHARS)}]")
        if any(invalid_char_pat.search(x) for x in (ident, cliente, rem)):
            return False, f"Los campos no deben contener ninguno de estos caracteres: {INVALID_FS_CHARS}"
        return True, ""

    def run_process(self):
        # Deshabilitar botón para evitar doble clic mientras procesa
        self.btn_convert.configure(state="disabled")

        ok, msg = self.validate_form()
        if not ok:
            messagebox.showerror("Validación", msg)
            # re-habilita si hay archivos para reintentar
            if list_input_files():
                self.btn_convert.configure(state="normal")
            return

        files = list_input_files()
        if not files:
            messagebox.showwarning("Sin archivos", f"No hay archivos con formatos admitidos en {INPUT_DIR}.")
            return  # seguirá deshabilitado si no hay archivos (correcto)

        # limpiar y preparar temporales
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR, ignore_errors=True)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)

        # conversión
        self.progress["value"] = 0
        self.progress["maximum"] = len(files)

        converted: list[Path] = []
        for idx, f in enumerate(files, 1):
            self.progress["value"] = idx - 1
            self.progress.update()
            pdf = convert_to_pdf(f)
            if pdf:
                converted.append(pdf)

        self.progress["value"] = len(files)
        self.progress.update()

        if not converted:
            messagebox.showerror("Error", "No se pudo convertir ninguno de los archivos. Revise el log.")
            # re-habilita si aún hay archivos (para reintentar)
            if list_input_files():
                self.btn_convert.configure(state="normal")
            return

        # unión
        out_name = final_pdf_name(self.var_ident.get(), self.var_cliente.get(), self.var_reembolso.get())
        out_path = OUTPUT_DIR / out_name
        try:
            merge_pdfs(converted, out_path)
        except Exception as e:
            logger.exception(f"Error uniendo PDFs: {e}")
            messagebox.showerror(
                "Error",
                "Falló la unión de PDFs.\n"
                "Verifica que el archivo de salida no esté abierto y vuelve a intentarlo."
            )
            # re-habilita si hay archivos para reintentar
            if list_input_files():
                self.btn_convert.configure(state="normal")
            return
        finally:
            # limpiar temporales
            shutil.rmtree(TEMP_DIR, ignore_errors=True)

        logger.info(f"Proceso completo -> {out_path}")
        messagebox.showinfo("Listo", f"PDF consolidado creado:\n{out_path.resolve()}")

        # Abrir salida y limpiar formulario + carpeta ARCHIVOS
        self.open_folder(OUTPUT_DIR)
        self.clear_form_and_input()

        # Tras limpiar data/input, el botón quedará deshabilitado por reload_files().
        # Si hubiera archivos (p. ej., el usuario ya colocó nuevos), se habilitará.
        if list_input_files():
            self.btn_convert.configure(state="normal")

    def clear_form_and_input(self):
        """Limpia los 3 campos del formulario y elimina el contenido de data/input."""
        try:
            # Limpiar campos del formulario
            self.var_ident.set("")
            self.var_cliente.set("")
            self.var_reembolso.set("")

            # Vaciar carpeta data/input (manteniendo la carpeta)
            if INPUT_DIR.exists():
                for path in INPUT_DIR.iterdir():
                    try:
                        if path.is_file() or path.is_symlink():
                            path.unlink()
                        elif path.is_dir():
                            shutil.rmtree(path)
                    except Exception as e:
                        logger.exception(f"Error eliminando '{path}': {e}")

            # Refrescar la lista de archivos en la UI (y estado del botón)
            self.reload_files()

        except Exception as e:
            logger.exception(f"Error al limpiar formulario/carpeta: {e}")
            messagebox.showwarning(
                "Aviso",
                f"Se creó el PDF, pero no se pudo limpiar completamente ARCHIVOS:\n{e}"
            )


if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        logger.exception(f"Fallo crítico: {e}")
        raise
