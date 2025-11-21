from typing import Annotated
from pydantic import BaseModel, Field
from langchain_core.tools import tool, InjectedToolCallId  # type: ignore
from langchain_core.runnables import RunnableConfig
from tools.utils.image_generation_core import generate_image_with_provider


class EditImageByDoubaoSeedream3InputSchema(BaseModel):
    prompt: str = Field(
        description="必填项。图像编辑的提示词。请在提示词中描述你想要编辑的内容。"
    )
    image: list[str] = Field(
        description="必填项。用于图像生成的图片。在此处传入图片ID列表（仅支持1张图片。如果你想要生成多张图片，请调用其他工具），例如['im_hfuiut78.png']。适用于以下图像编辑场景：编辑图像的特定部分、移除特定对象、保持场景中的视觉元素（角色/对象一致性）、参考图片风格生成新内容（风格迁移）等。"
    )
    tool_call_id: Annotated[str, InjectedToolCallId]


@tool(
    "edit_image_by_doubao_seededit_3_volces",
    description="使用文本提示词和图片，通过豆包Seedream 3模型编辑图像。使用该模型通过豆包的高级AI进行高质量的图像修改。",
    args_schema=EditImageByDoubaoSeedream3InputSchema,
)
async def edit_image_by_doubao_seededit_3_volces(
    prompt: str,
    image: list[str],
    config: RunnableConfig,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> str:
    """
    通过提供者框架使用豆包Seedream 3模型编辑图像
    """
    ctx = config.get("configurable", {})
    canvas_id = ctx.get("canvas_id", "")
    session_id = ctx.get("session_id", "")

    return await generate_image_with_provider(
        canvas_id=canvas_id,
        session_id=session_id,
        provider="volces",
        model="doubao-seededit-3-0-i2i-250628",
        prompt=prompt,
        input_images=image,
    )


# Export the tool for easy import
__all__ = ["edit_image_by_doubao_seededit_3_volces"]
