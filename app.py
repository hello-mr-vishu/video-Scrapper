import os
from pytube import YouTube
from pytube.exceptions import PytubeError

def download_youtube_video(url, output_path="downloads"):
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Initialize YouTube object
        yt = YouTube(url)
        
        print(f"Video Title: {yt.title}")
        print("Available MP4 streams:")
        streams = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc()
        
        if not streams:
            print("No suitable MP4 streams found.")
            return
        
        # Display available streams
        for i, stream in enumerate(streams, 1):
            print(f"{i}. Resolution: {stream.resolution}, FPS: {stream.fps}, Size: ~{stream.filesize_mb:.2f} MB")
        
        # Let user choose a stream
        choice = input("Enter stream number to download (or '1' for highest resolution): ") or "1"
        try:
            choice = int(choice) - 1
            if 0 <= choice < len(streams):
                selected_stream = streams[choice]
            else:
                print("Invalid choice, selecting highest resolution.")
                selected_stream = streams[0]
        except ValueError:
            print("Invalid input, selecting highest resolution.")
            selected_stream = streams[0]
        
        print(f"Downloading: {yt.title} ({selected_stream.resolution})")
        selected_stream.download(output_path=output_path)
        print(f"Download completed! Video saved to {output_path}/{yt.title}.mp4")
        
    except PytubeError as e:
        print(f"YouTube error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    while True:
        url = input("Enter YouTube video URL (or 'q' to quit): ")
        if url.lower() == 'q':
            print("Exiting program.")
            break
        if not url.startswith(('https://www.youtube.com', 'https://youtu.be')):
            print("Invalid YouTube URL. Please try again.")
            continue
        download_youtube_video(url)

if __name__ == "__main__":
    main()