from pytubefix import YouTube
from pytubefix.cli import on_progress
import subprocess, re, os

def url_read():
    url = []
    with open("url.txt") as f:
        for line in f:
            url.append(line.rstrip())
    return url

def conversion(input_file, output_file):
    path = r"C:\Users\pecks\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
    ffmpeg_cmd = [path, "-i", input_file, "-vn", "-acodec", "libmp3lame", "-ab", "192k", "-ar", "44100", "-y", output_file]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print("Conversion success")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def clean_filename(title):
    return re.sub(r'[\\/*?:"<>|]', "", title).strip()

def yt2mp3(url):
    yt = YouTube(url, on_progress_callback = on_progress)
    print(yt.title)
 
    ys = yt.streams.get_audio_only()

    name = clean_filename(yt.title)

    out_file = ys.download(output_path="Songs", filename = name +".m4a")
    conversion(out_file, f"Songs/{name}.mp3")

    m4a_file = os.path.join("Songs", name + ".m4a")
    if os.path.exists(m4a_file):
        os.remove(m4a_file)
        print(f"Deleted {m4a_file}")

url_list = url_read()
for item in url_list:
    preview = YouTube(item)
    name = clean_filename(preview.title)
    output_file = os.path.join("Songs", f"{name}.mp3")

    if os.path.exists(output_file):
        print(f"Skipping {output_file}")
        continue
    yt2mp3(item)