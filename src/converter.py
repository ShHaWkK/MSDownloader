import ffmpeg

class Converter:
    def __init__(self):
        pass

    def convert_to_mp4(self, input_file, output_file):
        try:
            stream = ffmpeg.input(input_file)
            stream = ffmpeg.output(stream, output_file, vcodec='libx264', acodec='aac')
            ffmpeg.run(stream)
            return True
        except ffmpeg.Error as e:
            print(f"An error occurred during conversion: {str(e)}")
            return False
