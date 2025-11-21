from typing import Annotated, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool, InjectedToolCallId  # type: ignore
from langchain_core.runnables import RunnableConfig
from tools.utils.image_generation_core import generate_image_with_provider


class GenerateImageByDoubaoSeedream4InputSchema(BaseModel):
    prompt: str = Field(
        description="必填项。图像生成的提示词。请在提示词中描述你想要生成的内容。"
    )
    image: Optional[list[str]] = Field(
        description="可选。用于图像生成的图片（适用于图生图）。在此处传入图片ID列表（仅支持1张图片）。",
        default=None
    )
    tool_call_id: Annotated[str, InjectedToolCallId]


@tool(
    "generate_image_by_doubao_seedream_4_volces",
    description="使用文生图（或文生图+图片进行图生图）的方式，通过豆包Seedream 4.0模型生成图像。使用该模型通过豆包的高级AI生成高质量图像。",
    args_schema=GenerateImageByDoubaoSeedream4InputSchema,
)
async def generate_image_by_doubao_seedream_4_volces(
    prompt: str,
    image: Optional[list[str]] = None,
    config: RunnableConfig = None,
    tool_call_id: Annotated[str, InjectedToolCallId] = None,
) -> str:
    """
    通过提供者框架使用豆包Seedream 4.0模型生成图像
    """
    ctx = config.get("configurable", {}) if config else {}
    canvas_id = ctx.get("canvas_id", "")
    session_id = ctx.get("session_id", "")

    return await generate_image_with_provider(
        canvas_id=canvas_id,
        session_id=session_id,
        provider="volces",
        model="doubao-seedream-4-0-250828",
        prompt=prompt,
        input_images=image,
    )


# Export the tool for easy import
__all__ = ["generate_image_by_doubao_seedream_4_volces"]