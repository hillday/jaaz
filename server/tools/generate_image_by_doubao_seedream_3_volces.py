from typing import Annotated
from pydantic import BaseModel, Field
from langchain_core.tools import tool, InjectedToolCallId  # type: ignore
from langchain_core.runnables import RunnableConfig
from tools.utils.image_generation_core import generate_image_with_provider


class GenerateImageByDoubaoSeedream3InputSchema(BaseModel):
    prompt: str = Field(
        description="必填项。图像生成的提示词。如果你想要编辑图像，请在提示词中描述你想要编辑的内容。"
    )
    aspect_ratio: str = Field(
        description="必填项。图像的宽高比，仅允许以下值：1:1、16:9、4:3、3:4、9:16。根据提示词选择最合适的宽高比。海报的最佳比例是3:4。"
    )
    tool_call_id: Annotated[str, InjectedToolCallId]


@tool("generate_image_by_doubao_seedream_3_volces",
      description="使用文生图的方式，通过豆包Seedream 3模型生成图像。该模型不支持输入图片作为参考或编辑。使用该模型通过豆包的高级AI生成高质量图像。支持多个提供者并自动降级。",
      args_schema=GenerateImageByDoubaoSeedream3InputSchema)
async def generate_image_by_doubao_seedream_3_volces(
    prompt: str,
    aspect_ratio: str,
    config: RunnableConfig,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> str:
    """
    通过提供者框架使用豆包Seedream 3模型生成图像
    """
    ctx = config.get('configurable', {})
    canvas_id = ctx.get('canvas_id', '')
    session_id = ctx.get('session_id', '')

    return await generate_image_with_provider(
        canvas_id=canvas_id,
        session_id=session_id,
        provider='volces',
        model="volces/doubao-seedream-3-0-t2i-250415",
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        input_images=None,
    )


# Export the tool for easy import
__all__ = ["generate_image_by_doubao_seedream_3_volces"]
