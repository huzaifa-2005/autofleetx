from django.core.management.base import BaseCommand
import cloudinary
import cloudinary.uploader
from main_app.models import Car
from django.conf import settings

class Command(BaseCommand):
    help = 'Test Cloudinary configuration and show current image URLs'

    def handle(self, *args, **options):
        # Test 1: Check Cloudinary configuration
        self.stdout.write("🔧 Testing Cloudinary configuration...")
        try:
            result = cloudinary.api.ping()
            self.stdout.write(self.style.SUCCESS(f"✅ Cloudinary connected: {result}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Cloudinary connection failed: {e}"))
            return

        # Test 2: Check current car image URLs
        self.stdout.write("\n📸 Current car image URLs:")
        cars_with_images = Car.objects.filter(image__isnull=False).exclude(image='')
        
        for car in cars_with_images:
            self.stdout.write(f"Car: {car.name}")
            self.stdout.write(f"Image field: {car.image}")
            self.stdout.write(f"Image URL: {car.image.url}")
            self.stdout.write("---")

        # Test 3: Check storage backend
        self.stdout.write(f"\n⚙️ Current DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        
        # Test 4: Test upload
        self.stdout.write("\n🚀 Testing image upload to Cloudinary...")
        try:
            # Create a simple test image upload
            test_result = cloudinary.uploader.upload(
                "https://via.placeholder.com/150x150.png?text=Test",
                folder="car_images",
                public_id="test_upload"
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Test upload successful: {test_result['url']}"))
            
            # Clean up test image
            cloudinary.uploader.destroy("car_images/test_upload")
            self.stdout.write("🧹 Test image cleaned up")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Test upload failed: {e}"))