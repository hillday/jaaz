from typing import List
from .base_config import BaseAgentConfig, HandoffConfig


class PlannerAgentConfig(BaseAgentConfig):
    """规划智能体 - 负责制定执行计划
    """

    def __init__(self) -> None:
        system_prompt = """
            你必须始终使用中文回答用户的问题，包括思考过程、步骤和所有回复内容。

            你是一名专业规划师，你的工作是为用户的请求制定详细的执行计划。你可以使用提供的工具来完成用户的请求。

            当你制定计划时，需要考虑以下几点：
            1. 计划应详细具体，包括完成任务所需的所有步骤。
            2. 计划应切实可行，考虑到可用的工具和资源。
            3. 计划应清晰易懂，每个步骤都以简洁明了的方式描述。

            你可以按照以下步骤制定计划：
            1. 分析用户的请求，了解目标和要求。
            2. 将任务分解为更小的、可管理的步骤。
            3. 确定步骤的顺序和它们之间的任何依赖关系。
            4. 确定每个步骤所需的任何工具或资源。
            5. 以清晰有序的方式编写计划，必要时使用标题和项目符号。

            重要提示：你不得直接使用任何工具。你只需要制定计划。计划的执行将由其他智能体处理。

            当你完成计划后，必须以编号列表的形式编写执行计划，使用中文。"""

        handoffs: List[HandoffConfig] = [
            {
                'agent_name': 'image_video_creator',
                'description': """
                        Transfer user to the image_video_creator. About this agent: Specialize in generating images and videos from text prompt or input images.
                        """
            }
        ]

        super().__init__(
            name='planner',
            tools=[{'id': 'write_plan', 'provider': 'system'}],
            system_prompt=system_prompt,
            handoffs=handoffs
        )
