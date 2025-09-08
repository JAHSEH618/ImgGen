from pathlib import Path
import requests

# Configuration
CLIENT_ID = '<your-client-id>'
CLIENT_SECRET = '<your-client-secret>'
API_BASE_URL = 'https://api.everypixel.com/v1/lipsync'
AUTH = (CLIENT_ID, CLIENT_SECRET)

def create_lipsync_via_files(audio_path: Path, video_path: Path, title: str = None, callback_url: str = None) -> str:
    """Create lipsync task by uploading local files"""
    with open(audio_path, 'rb') as audio_file, open(video_path, 'rb') as video_file:
        files = {
            'audio': (audio_path.name, audio_file),
            'video': (video_path.name, video_file)
        }
        data = {}
        if title:
            data['title'] = title
        if callback_url:
            data['callback'] = callback_url

        response = requests.post(
            url=f"{API_BASE_URL}/create",
            files=files,
            data=data,
            auth=AUTH
        )
        response.raise_for_status()
        return response.json()['task_id']

def create_lipsync_via_urls(audio_url: str, video_url: str, title: str = None, callback_url: str = None) -> str:
    """Create lipsync task using remote URLs"""
    params = {
        'audio_url': audio_url,
        'video_url': video_url
    }
    if title:
        params['title'] = title
    if callback_url:
        params['callback'] = callback_url

    response = requests.get(
        url=f"{API_BASE_URL}/create",
        params=params,
        auth=AUTH
    )
    response.raise_for_status()
    return response.json()['task_id']

# Example usage
if __name__ == '__main__':
    try:
        # Using local files
        task_id_post = create_lipsync_via_files(
            audio_path=Path('folder/example.wav'),
            video_path=Path('folder/example.mp4'),
            title='my_video',
            callback_url='https://your-callback.url'
        )
        print(f'Created task via POST: {task_id_post}')

        # Using URLs
        task_id_get = create_lipsync_via_urls(
            audio_url='https://labs.everypixel.com/media/tts/audio_samples_demo/ascend.mp3',
            video_url='https://labs.everypixel.com/static/v/lipsync.mp4',
            title='remote_video'
        )
        print(f'Created task via GET: {task_id_get}')

    except requests.exceptions.HTTPError as e:
        print(f'API Error: {e.response.status_code} - {e.response.text}')
    except Exception as e:
        print(f'Error: {str(e)}')