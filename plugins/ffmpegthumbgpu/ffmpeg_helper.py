import json
import subprocess
import logging

from app.utils.system import SystemUtils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FfmpegHelper:

    @staticmethod
    def get_thumb(video_path: str, image_path: str, frames: str = None):
        if not frames:
            frames = "00:03:01"
        if not video_path or not image_path:
            logger.error("Video path or image path is not provided")
            return False

        cmd = f'ffmpeg -hwaccel cuda -i "{video_path}" -ss {frames} -vframes 1 -f image2 "{image_path}"'
        logger.info(f"Executing command: {cmd}")
        try:
            result = SystemUtils.execute(cmd)
            if result:
                return True
        except Exception as e:
            logger.error(f"Failed to execute ffmpeg command: {e}")
        return False

    @staticmethod
    def extract_wav(video_path: str, audio_path: str, audio_index: str = None):
        if not video_path or not audio_path:
            logger.error("Video path or audio path is not provided")
            return False

        try:
            if audio_index:
                command = [
                    'ffmpeg', '-hwaccel', 'cuda', "-hide_banner", "-loglevel", "warning", '-y', '-i', video_path,
                    '-map', f'0:a:{audio_index}',
                    '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', audio_path
                ]
            else:
                command = [
                    'ffmpeg', '-hwaccel', 'cuda', "-hide_banner", "-loglevel", "warning", '-y', '-i', video_path,
                    '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', audio_path
                ]

            logger.info(f"Executing command: {' '.join(command)}")
            ret = subprocess.run(command).returncode
            if ret == 0:
                return True
            logger.error(f"FFmpeg command failed with return code {ret}")
        except Exception as e:
            logger.error(f"Failed to execute ffmpeg command: {e}")
        return False

    @staticmethod
    def get_metadata(video_path: str):
        if not video_path:
            logger.error("Video path is not provided")
            return None

        try:
            command = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_path
            ]
            logger.info(f"Executing command: {' '.join(command)}")
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return json.loads(result.stdout.decode("utf-8"))
            logger.error(f"ffprobe command failed with return code {result.returncode}")
        except Exception as e:
            logger.error(f"Failed to execute ffprobe command: {e}")
        return None

    @staticmethod
    def extract_subtitle(video_path: str, subtitle_path: str, subtitle_index: str = None):
        if not video_path or not subtitle_path:
            logger.error("Video path or subtitle path is not provided")
            return False

        try:
            if subtitle_index:
                command = [
                    'ffmpeg', '-hwaccel', 'cuda', "-hide_banner", "-loglevel", "warning", '-y', '-i', video_path,
                    '-map', f'0:s:{subtitle_index}',
                    subtitle_path
                ]
            else:
                command = [
                    'ffmpeg', '-hwaccel', 'cuda', "-hide_banner", "-loglevel", "warning", '-y', '-i', video_path,
                    subtitle_path
                ]
            logger.info(f"Executing command: {' '.join(command)}")
            ret = subprocess.run(command).returncode
            if ret == 0:
                return True
            logger.error(f"FFmpeg command failed with return code {ret}")
        except Exception as e:
            logger.error(f"Failed to execute ffmpeg command: {e}")
        return False
