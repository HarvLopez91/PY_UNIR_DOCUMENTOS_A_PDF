#!/usr/bin/env python3
"""
Script para convertir LogoLApng-1920w.webp a icon.ico para usar como icono de aplicación
"""
from PIL import Image
from pathlib import Path

def crear_icono():
    """Convierte el logo de La Ascensión a formato .ico para icono de aplicación"""
    
    assets_dir = Path("assets")
    logo_path = assets_dir / "LogoLApng-1920w.webp"
    icon_path = assets_dir / "icon.ico"
    
    if not logo_path.exists():
        print(f"❌ Error: No se encuentra {logo_path}")
        return False
    
    try:
        # Cargar la imagen webp
        img = Image.open(logo_path)
        print(f"📂 Cargando imagen: {img.size[0]}x{img.size[1]} px")
        
        # Convertir a RGBA para mantener transparencia
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Crear icono con múltiples tamaños para mejor compatibilidad
        sizes = [16, 32, 48, 64, 128, 256]
        icon_images = []
        
        for size in sizes:
            # Redimensionar manteniendo proporciones
            img_resized = img.resize((size, size), Image.Resampling.LANCZOS)
            icon_images.append(img_resized)
            print(f"✅ Creado tamaño: {size}x{size}")
        
        # Guardar como .ico con múltiples tamaños
        icon_images[0].save(
            icon_path,
            format='ICO',
            sizes=[(img.size[0], img.size[1]) for img in icon_images],
            append_images=icon_images[1:]
        )
        
        print(f"🎯 Icono creado exitosamente: {icon_path}")
        print(f"📏 Tamaños incluidos: {', '.join(f'{s}x{s}' for s in sizes)}")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear icono: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Generador de Icono - PDF Consolidator")
    print("=" * 50)
    
    if crear_icono():
        print("\n✅ Proceso completado exitosamente")
    else:
        print("\n❌ Error en el proceso")