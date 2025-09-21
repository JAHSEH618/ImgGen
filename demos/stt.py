import logging
from pathlib import Path
from typing import Optional, Union, List, Dict, Any
from contextlib import contextmanager
from openai import OpenAI
import json
from datetime import datetime


class AudioProcessor:
    """
    高级音频转文字处理器，支持转录和翻译功能
    """
    
    SUPPORTED_FORMATS = {
        '.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm'
    }
    
    SUPPORTED_LANGUAGES = {
        'zh': '中文', 'en': '英语', 'es': '西班牙语', 'fr': '法语', 
        'de': '德语', 'it': '意大利语', 'pt': '葡萄牙语', 'ru': '俄语',
        'ja': '日语', 'ko': '韩语', 'ar': '阿拉伯语', 'hi': '印地语'
    }
    
    def __init__(self, api_key: Optional[str] = None, log_level: str = "INFO"):
        """
        初始化音频处理器
        
        Args:
            api_key: OpenAI API密钥，如果为None则从环境变量获取
            log_level: 日志级别
        """
        self.setup_logging(log_level)
        self.client = OpenAI(api_key="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")
        self.logger = logging.getLogger(__name__)
        
    def setup_logging(self, level: str) -> None:
        """设置日志配置"""
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('stt_processing.log')
            ]
        )
    
    @contextmanager
    def open_audio_file(self, file_path: Union[str, Path]):
        """安全打开音频文件的上下文管理器"""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"音频文件不存在: {file_path}")
        
        if file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"不支持的音频格式: {file_path.suffix}")
        
        audio_file = None
        try:
            audio_file = open(file_path, "rb")
            yield audio_file
        finally:
            if audio_file:
                audio_file.close()
    
    def validate_file_size(self, file_path: Union[str, Path], max_size_mb: int = 25) -> bool:
        """验证文件大小是否符合OpenAI限制"""
        file_size = Path(file_path).stat().st_size / (1024 * 1024)  # MB
        if file_size > max_size_mb:
            self.logger.warning(f"文件大小 {file_size:.2f}MB 超过限制 {max_size_mb}MB")
            return False
        return True
    
    def transcribe(
        self, 
        file_path: Union[str, Path], 
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        temperature: float = 0,
        response_format: str = "json"
    ) -> Dict[str, Any]:
        """
        转录音频文件为文字（保持原语言）
        
        Args:
            file_path: 音频文件路径
            language: 音频语言代码（如'zh', 'en'），None为自动检测
            prompt: 提示词，用于改善转录质量
            temperature: 采样温度 (0-1)
            response_format: 响应格式 ('json', 'text', 'srt', 'verbose_json', 'vtt')
            
        Returns:
            转录结果字典
        """
        file_path = Path(file_path)
        
        if not self.validate_file_size(file_path):
            raise ValueError("文件大小超过限制")
        
        self.logger.info(f"开始转录文件: {file_path.name}")
        
        try:
            with self.open_audio_file(file_path) as audio_file:
                kwargs = {
                    "model": "whisper-1",
                    "file": audio_file,
                    "response_format": response_format,
                    "temperature": temperature
                }
                
                if language:
                    kwargs["language"] = language
                if prompt:
                    kwargs["prompt"] = prompt
                
                response = self.client.audio.transcriptions.create(**kwargs)
                
                result = {
                    "type": "transcription",
                    "file_name": file_path.name,
                    "language": language or "auto-detected",
                    "timestamp": datetime.now().isoformat(),
                    "response": response if response_format == "json" else {"text": response}
                }
                
                self.logger.info(f"转录完成: {file_path.name}")
                return result
                
        except Exception as e:
            self.logger.error(f"转录失败 {file_path.name}: {str(e)}")
            raise
    
    def translate(
        self, 
        file_path: Union[str, Path],
        prompt: Optional[str] = None,
        temperature: float = 0,
        response_format: str = "json"
    ) -> Dict[str, Any]:
        """
        翻译音频文件为英文
        
        Args:
            file_path: 音频文件路径
            prompt: 提示词
            temperature: 采样温度 (0-1)
            response_format: 响应格式
            
        Returns:
            翻译结果字典
        """
        file_path = Path(file_path)
        
        if not self.validate_file_size(file_path):
            raise ValueError("文件大小超过限制")
        
        self.logger.info(f"开始翻译文件: {file_path.name}")
        
        try:
            with self.open_audio_file(file_path) as audio_file:
                kwargs = {
                    "model": "whisper-1",
                    "file": audio_file,
                    "response_format": response_format,
                    "temperature": temperature
                }
                
                if prompt:
                    kwargs["prompt"] = prompt
                
                response = self.client.audio.translations.create(**kwargs)
                
                result = {
                    "type": "translation",
                    "file_name": file_path.name,
                    "target_language": "en",
                    "timestamp": datetime.now().isoformat(),
                    "response": response if response_format == "json" else {"text": response}
                }
                
                self.logger.info(f"翻译完成: {file_path.name}")
                return result
                
        except Exception as e:
            self.logger.error(f"翻译失败 {file_path.name}: {str(e)}")
            raise
    
    def batch_process(
        self, 
        input_folder: Union[str, Path],
        output_folder: Optional[Union[str, Path]] = None,
        operation: str = "transcribe",
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        批量处理音频文件
        
        Args:
            input_folder: 输入文件夹路径
            output_folder: 输出文件夹路径（可选）
            operation: 操作类型 ('transcribe' 或 'translate')
            **kwargs: 传递给处理函数的额外参数
            
        Returns:
            处理结果列表
        """
        input_path = Path(input_folder)
        if not input_path.exists():
            raise FileNotFoundError(f"输入文件夹不存在: {input_folder}")
        
        # 查找所有支持的音频文件
        audio_files = []
        for ext in self.SUPPORTED_FORMATS:
            audio_files.extend(input_path.glob(f"*{ext}"))
            audio_files.extend(input_path.glob(f"*{ext.upper()}"))
        
        if not audio_files:
            self.logger.warning("未找到支持的音频文件")
            return []
        
        self.logger.info(f"找到 {len(audio_files)} 个音频文件，开始批量{operation}...")
        
        results = []
        success_count = 0
        
        for audio_file in audio_files:
            try:
                if operation == "transcribe":
                    result = self.transcribe(audio_file, **kwargs)
                elif operation == "translate":
                    result = self.translate(audio_file, **kwargs)
                else:
                    raise ValueError(f"不支持的操作: {operation}")
                
                results.append(result)
                success_count += 1
                
                # 保存结果到文件
                if output_folder:
                    self.save_result(result, output_folder)
                    
            except Exception as e:
                error_result = {
                    "type": f"{operation}_error",
                    "file_name": audio_file.name,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                results.append(error_result)
                self.logger.error(f"处理文件失败 {audio_file.name}: {str(e)}")
        
        self.logger.info(f"批量处理完成: {success_count}/{len(audio_files)} 个文件处理成功")
        return results
    
    def save_result(self, result: Dict[str, Any], output_folder: Union[str, Path]) -> None:
        """保存处理结果到文件"""
        output_path = Path(output_folder)
        output_path.mkdir(exist_ok=True)
        
        file_name = Path(result["file_name"]).stem
        output_file = output_path / f"{file_name}_{result['type']}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    def get_audio_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """获取音频文件信息"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        stat = file_path.stat()
        return {
            "file_name": file_path.name,
            "file_size_mb": stat.st_size / (1024 * 1024),
            "format": file_path.suffix.lower(),
            "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "supported": file_path.suffix.lower() in self.SUPPORTED_FORMATS
        }


def main():
    """主函数示例"""
    processor = AudioProcessor()
    
    # 示例音频文件路径
    audio_file = "/Users/okonma/Desktop/output_ffmpeg.mp3"
    
    try:
        # 检查文件信息
        print("=== 音频文件信息 ===")
        info = processor.get_audio_info(audio_file)
        print(json.dumps(info, ensure_ascii=False, indent=2))
        
        # 转录音频（保持原语言）
        print("\n=== 转录音频 ===")
        transcription = processor.transcribe(
            audio_file,
            language="zh",  # 指定中文
            response_format="json"
        )
        print(f"转录结果: {transcription['response']['text']}")
        
        # 翻译音频为英文
        print("\n=== 翻译音频 ===")
        translation = processor.translate(
            audio_file,
            response_format="json"
        )
        print(f"翻译结果: {translation['response']['text']}")
        
    except FileNotFoundError:
        print(f"文件不存在: {audio_file}")
        print("请修改 audio_file 变量为有效的音频文件路径")
    except Exception as e:
        print(f"处理失败: {str(e)}")


if __name__ == "__main__":
    main()