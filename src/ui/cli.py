from downloader import Downloader
from converter import Converter

class CLI:
    def __init__(self):
        self.downloader = Downloader()
        self.converter = Converter()

    def run(self):
        while True:
            print("\nMSDownloader CLI")
            print("1. Download video")
            print("2. Convert video to MP4")
            print("3. Quit")
            choice = input("Enter your choice (1-3): ")

            if choice == '1':
                self.download_video()
            elif choice == '2':
                self.convert_video()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def download_video(self):
        url = input("Enter the URL of the video: ")
        platform = input("Enter the platform (YouTube, VoirDrama, Papstream): ")
        quality = input("Enter the quality (Best, 1080p, 720p, 480p): ")
        
        print("Downloading...")
        title = self.downloader.download(url, platform, quality)
        if title:
            print(f"Successfully downloaded: {title}")
        else:
            print("Download failed.")

    def convert_video(self):
        input_file = input("Enter the path of the input video file: ")
        output_file = input("Enter the path for the output MP4 file: ")
        
        print("Converting...")
        if self.converter.convert_to_mp4(input_file, output_file):
            print("Conversion completed successfully.")
        else:
            print("Conversion failed.")
