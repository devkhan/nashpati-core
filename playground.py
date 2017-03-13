from youtube_dl import YoutubeDL


def my_progress_hook(s):
    with open('progress.txt', 'a') as file:
        import json
        file.write(json.dumps(s))
        file.flush()

ytdl = YoutubeDL()

ytdl.add_progress_hook(my_progress_hook)

ytdl.extract_info('https://www.youtube.com/watch?v=4OctxxWGiNw')

# celery worker -A tasks.celery --loglevel=info
