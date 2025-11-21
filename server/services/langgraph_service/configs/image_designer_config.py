from typing import List

from models.tool_model import ToolInfoJson
from .base_config import BaseAgentConfig, HandoffConfig

class ImageDesignerAgentConfig(BaseAgentConfig):
    """图像设计智能体 - 专门负责图像生成
    """

    def __init__(self, tool_list: List[ToolInfoJson], system_prompt: str = "") -> None:
        batch_generation_prompt = """

批量生成规则:
- 如果用户需要生成超过10张图片: 每次最多生成10张，分批次完成
- 完成一个批次后再开始下一个批次
- 20张图片的示例: 批次1 (1-10) → "批次1完成!" → 批次2 (11-20) → "全部20张图片完成!"

"""

        error_handling_prompt = """

错误处理说明:
当图片生成失败时，你必须:
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

        full_system_prompt = "你必须始终使用中文回答用户的问题，包括思考过程、步骤和所有回复内容。\n\n" + system_prompt + \
            batch_generation_prompt + error_handling_prompt

        # 图像设计智能体不需要切换到其他智能体
        handoffs: List[HandoffConfig] = [
            {
                'agent_name': 'video_designer',
                'description': """
                        Transfer user to the video_designer. If user wants to generate video, transfer to video_designer.
                        """
            }
        ]

        super().__init__(
            name='image_designer',
            tools=tool_list,
            system_prompt=full_system_prompt,
            handoffs=handoffs
        )
