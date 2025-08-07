# main_app/management/commands/test_cloudinary.py

from django.core.management.base import BaseCommand
from django.conf import settings
import cloudinary
import cloudinary.uploader
import cloudinary.api

class Command(BaseCommand):
    help = 'Test Cloudinary connection and configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Testing Cloudinary connection...'))
        
        try:
            # Test 1: Check configuration
            self.stdout.write('1. Checking Cloudinary configuration...')
            self.stdout.write(f'   Cloud Name: {cloudinary.config().cloud_name}')
            self.stdout.write(f'   API Key: {cloudinary.config().api_key[:8]}...')  # Only show first 8 chars
            self.stdout.write(f'   Secure: {cloudinary.config().secure}')
            
            # Test 2: Ping Cloudinary
            self.stdout.write('2. Testing connection to Cloudinary...')
            result = cloudinary.api.ping()
            self.stdout.write(self.style.SUCCESS(f'   ✓ Connection successful: {result}'))
            
            # Test 3: Check storage backend
            self.stdout.write('3. Checking Django storage configuration...')
            from django.core.files.storage import default_storage
            self.stdout.write(f'   Default storage: {default_storage.__class__.__name__}')
            
            # Test 4: Test upload (small test image)
            self.stdout.write('4. Testing image upload...')
            test_result = cloudinary.uploader.upload(
                "https://via.placeholder.com/150x150/ff0000/ffffff?text=TEST",
                public_id="django_test_upload",
                folder="test_uploads"
            )
            self.stdout.write(self.style.SUCCESS(f'   ✓ Upload successful!'))
            self.stdout.write(f'   Test image URL: {test_result.get("url")}')
            
            # Test 5: Clean up test upload
            self.stdout.write('5. Cleaning up test upload...')
            cloudinary.uploader.destroy("test_uploads/django_test_upload")
            self.stdout.write(self.style.SUCCESS('   ✓ Cleanup completed'))
            
            self.stdout.write(self.style.SUCCESS('\n🎉 ALL TESTS PASSED! Cloudinary is working correctly.'))
            
        except cloudinary.exceptions.Error as e:
            self.stdout.write(self.style.ERROR(f'❌ Cloudinary API Error: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ General Error: {str(e)}'))
            self.stdout.write('Check your environment variables and internet connection.')