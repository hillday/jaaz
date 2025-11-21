from typing import List
from models.tool_model import ToolInfoJson
from .base_config import BaseAgentConfig, HandoffConfig


class VideoDesignerAgentConfig(BaseAgentConfig):
    """视频设计智能体 - 专门负责视频生成
    """

    def __init__(self, tool_list: List[ToolInfoJson]) -> None:
        video_generation_prompt = """
你是一名视频设计师，负责根据用户请求生成视频。你可以根据文本提示和图片生成视频。

视频生成规则:
- 根据用户提示生成高质量视频
- 使用详细的电影化描述以获得更好的结果
- 考虑宽高比、时长和分辨率要求
- 提供清晰的视频生成进度反馈
- 如果用户提供了图片，尽可能将其用作第一帧

"""

        error_handling_prompt = """

错误处理说明:
当视频生成失败时，你必须:
1. 确认失败并向用户解释具体原因
2. 如果错误提到"敏感内容"或"标记内容"，建议用户:
   - 使用更合适、敏感度更低的描述
   - 避免潜在的争议、暴力或不当内容
   - 尝试用更中性的语言重新表述
3. 如果是API错误(HTTP 500等)，建议:
   - 稍后再试
   - 在提示词中使用不同的措辞
   - 检查服务是否暂时不可用
4. 始终提供有用的替代方案建议
5. 保持支持和专业的语气

重要提示: 永远不要忽略工具错误。始终对失败的工具调用做出回应，为用户提供有用的指导。
"""

        full_system_prompt = "你必须始终使用中文回答用户的问题，包括思考过程、步骤和所有回复内容。\n\n" + video_generation_prompt + error_handling_prompt

        # 视频设计智能体不需要切换到其他智能体
        handoffs: List[HandoffConfig] = [
            {
                'agent_name': 'image_designer',
                'description': """
                        Transfer user to the image_designer. About this agent: Specialize in generating images.
                        """
            },
        ]

        super().__init__(
            name='video_designer',
            tools=tool_list,
            system_prompt=full_system_prompt,
            handoffs=handoffs
        )
