"""
Create placeholder character images for the login screen.
This will create simple placeholder images so the layout works immediately.
You can replace these with your actual character images later.
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  PIL/Pillow not available. Install it with: pip install Pillow")

def create_placeholder_image(width: int, height: int, text: str, bg_color: tuple, output_path: str):
    """Create a simple placeholder image"""
    if not PIL_AVAILABLE:
        print(f"❌ Cannot create image - PIL not available")
        return False
    
    try:
        # Create image with gradient-like background
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Add a simple character representation
        # Draw a circle for head
        head_size = min(width, height) // 3
        head_x = width // 2
        head_y = height // 3
        draw.ellipse(
            [head_x - head_size//2, head_y - head_size//2, 
             head_x + head_size//2, head_y + head_size//2],
            fill=(255, 255, 255, 200),
            outline=(200, 200, 200),
            width=3
        )
        
        # Draw body (rectangle)
        body_width = head_size
        body_height = head_size * 1.5
        body_x = head_x - body_width // 2
        body_y = head_y + head_size // 2
        draw.rectangle(
            [body_x, body_y, body_x + body_width, body_y + body_height],
            fill=(255, 255, 255, 200),
            outline=(200, 200, 200),
            width=3
        )
        
        # Add text label
        try:
            # Try to use a nice font
            font_size = 40
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        text_y = body_y + body_height + 30
        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (width - text_width) // 2
            draw.text((text_x, text_y), text, fill=(100, 100, 100), font=font)
        else:
            draw.text((width//2 - 50, text_y), text, fill=(100, 100, 100))
        
        # Save as PNG
        img.save(output_path, 'PNG')
        print(f"✅ Created placeholder: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating image: {e}")
        return False

def main():
    """Create placeholder character images"""
    print("=" * 60)
    print("Creating Placeholder Character Images")
    print("=" * 60)
    
    # Setup directory
    images_dir = Path("app/assets/images")
    images_dir.mkdir(parents=True, exist_ok=True)
    
    left_path = images_dir / "left_character.png"
    right_path = images_dir / "right_character.png"
    
    # Check if images already exist
    if left_path.exists() and right_path.exists():
        print(f"\n✅ Images already exist!")
        print(f"   Left: {left_path}")
        print(f"   Right: {right_path}")
        response = input("\nDo you want to overwrite them? (y/n): ").strip().lower()
        if response != 'y':
            print("Skipping image creation.")
            return
    
    if not PIL_AVAILABLE:
        print("\n❌ PIL/Pillow is required to create placeholder images.")
        print("   Install it with: pip install Pillow")
        print("\n📝 Manual Instructions:")
        print(f"   1. Save your male character image as: {left_path}")
        print(f"   2. Save your female character image as: {right_path}")
        return
    
    print("\nCreating placeholder images...")
    
    # Create left character (male) - blue gradient background
    create_placeholder_image(
        700, 1000,
        "Male Character",
        (135, 206, 250),  # Light blue
        str(left_path)
    )
    
    # Create right character (female) - pink gradient background
    create_placeholder_image(
        700, 1000,
        "Female Character",
        (255, 182, 193),  # Light pink
        str(right_path)
    )
    
    print("\n" + "=" * 60)
    print("✅ Placeholder images created!")
    print("=" * 60)
    print(f"\n📁 Images saved to:")
    print(f"   - {left_path}")
    print(f"   - {right_path}")
    print("\n💡 Next Steps:")
    print("   1. Replace these placeholder images with your actual character images")
    print("   2. Keep the same filenames: 'left_character.png' and 'right_character.png'")
    print("   3. Restart your app to see the new images on the login screen")
    print("\n✨ The login screen layout will work immediately with these placeholders!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

