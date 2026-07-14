"""
Script to download and save character images for the login screen.
This script will help you get character images for the login screen.
"""

import os
import requests
from pathlib import Path

def download_image(url: str, save_path: str) -> bool:
    """Download an image from a URL and save it"""
    try:
        print(f"Downloading from: {url}")
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
        
        # Save the image
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Successfully saved to: {save_path}")
        return True
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        return False

def setup_images_directory():
    """Ensure the images directory exists"""
    images_dir = Path("app/assets/images")
    images_dir.mkdir(parents=True, exist_ok=True)
    return images_dir

def main():
    """Main function to download character images"""
    print("=" * 60)
    print("Character Images Downloader for Login Screen")
    print("=" * 60)
    
    images_dir = setup_images_directory()
    
    print("\n📋 Instructions:")
    print("1. You need to provide URLs for the character images")
    print("2. Or you can manually save images to:")
    print(f"   - {images_dir / 'left_character.png'}")
    print(f"   - {images_dir / 'right_character.png'}")
    print("\n💡 Tip: You can find free character images at:")
    print("   - https://www.flaticon.com/")
    print("   - https://www.freepik.com/")
    print("   - https://unsplash.com/")
    print("   - https://www.pexels.com/")
    
    # Option 1: Download from URLs if provided
    print("\n" + "=" * 60)
    print("Option 1: Download from URLs")
    print("=" * 60)
    
    left_url = input("\nEnter URL for left character (male) image (or press Enter to skip): ").strip()
    right_url = input("Enter URL for right character (female) image (or press Enter to skip): ").strip()
    
    if left_url:
        left_path = images_dir / "left_character.png"
        download_image(left_url, str(left_path))
    
    if right_url:
        right_path = images_dir / "right_character.png"
        download_image(right_url, str(right_path))
    
    # Check if images exist
    print("\n" + "=" * 60)
    print("Current Status:")
    print("=" * 60)
    
    left_path = images_dir / "left_character.png"
    right_path = images_dir / "right_character.png"
    
    if left_path.exists():
        print(f"✅ Left character image found: {left_path}")
    else:
        print(f"❌ Left character image missing: {left_path}")
        print("   Please add 'left_character.png' to this location")
    
    if right_path.exists():
        print(f"✅ Right character image found: {right_path}")
    else:
        print(f"❌ Right character image missing: {right_path}")
        print("   Please add 'right_character.png' to this location")
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. If images are missing, you can:")
    print("   - Run this script again with image URLs")
    print("   - Manually download and save images to the paths shown above")
    print("2. Once both images are in place, restart your app")
    print("3. The login screen will automatically display the images!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")

