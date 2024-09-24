import json
import subprocess
from app.utils.system import SystemUtils

class FfmpegHelper:

    @staticmethod
    def check_and_install_ffmpeg():
        """
        检查并安装支持GPU加速的FFmpeg
        """
        try:
            # 检查FFmpeg版本，并验证其是否支持GPU
            result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8')

            if 'enable-cuda' in output or 'enable-nvenc' in output:
                print("FFmpeg with GPU support is already installed.")
                return True
            else:
                print("FFmpeg does not support GPU. Installing FFmpeg with GPU support...")

                # 假设使用的是Linux系统，可以通过直接下载或从源编译来安装FFmpeg
                # 这里提供一个简化的安装命令示范（以Ubuntu为例）
                install_cmds = [
                    'sudo add-apt-repository -y ppa:savoury1/ffmpeg4',
                    'sudo apt-get update',
                    'sudo apt-get -y install ffmpeg'
                ]

                for cmd in install_cmds:
                    result = subprocess.run(cmd, shell=True)
                    if result.returncode != 0:
                        print(f"Failed to run command: {cmd}")
                        return False

                print("FFmpeg with GPU support installed successfully.")
                return True

        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    @staticmethod
    def get_thumb(video_path: str, image_path: str, frames: str = None):
        """
        使用ffmpeg从视频文件中截取缩略图
        """
        if not frames:
            frames = "00:03:01"
        if not video_path or not image_path:
            return False
        
        if not FfmpegHelper.check_and_install_ffmpeg():
            print("FFmpeg with GPU support is not available.")
            return False

        cmd = (
            'ffmpeg -hwaccel cuda -i "{video_path}" -ss {frames} '
            '-vframes 1 -f image2 "{image_path}"'
            ).format(
                video_path=video_path,
                frames=frames,
                image_path=image_path
            )
        result = SystemUtils.execute(cmd)
        if result:
            return True
        return False

    @staticmethod
    def extract_wav(video_path: str, audio_path: str, audio_index: str = None):
        """
        使用ffmpeg从视频文件中提取16000hz, 16-bit的wav格式音频
        """
        if not video_path or not audio_path:
            return False

        if not FfmpegHelper.check_and_install_ffmpeg():
            print("FFmpeg with GPU support is not available.")
            return False

        # 提取指定音频流
        if audio_index:
            command = [
                'ffmpeg', "-hide_banner", "-loglevel", "warning", '-y',
                '-hwaccel', 'cuda', '-i', video_path, 
                '-map', f'0:a:{audio_index}', 
                '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', 
                audio_path
            ]
        else:
            command = [
                'ffmpeg', "-hide_banner", "-loglevel", "warning", '-y',
                '-hwaccel', 'cuda', '-i', video_path, 
                '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', 
                audio_path
            ]

        ret = subprocess.run(command).returncode
        if ret == 0:
            return True
        return False

    @staticmethod
    def get_metadata(video_path: str):
        """
        获取视频元数据
        """
        if not video_path:
            return False

        try:
            command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_path]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return json.loads(result.stdout.decode("utf-8"))
        except Exception as e:
            print(e)
        return None

    @staticmethod
    def extract_subtitle(video_path: str, subtitle_path: str, subtitle_index: str = None):
        """
        从视频中提取字幕
        """
        if not video_path or not subtitle_path:
            return False

        if not FfmpegHelper.check_and_install_ffmpeg():
            print("FFmpeg with GPU support is not available.")
            return False

        if subtitle_index:
            command = [
                'ffmpeg', "-hide_banner", "-loglevel", "warning", '-y',
                '-hwaccel', 'cuda', '-i', video_path,
                '-map', f'0:s:{subtitle_index}',
                subtitle_path
            ]
        else:
            command = [
                'ffmpeg', "-hide_banner", "-loglevel", "warning", '-y',
                '-hwaccel', 'cuda', '-i', video_path, 
                subtitle_path
            ]
        ret = subprocess.run(command).returncode
        if ret == 0:
            return True
        return False
