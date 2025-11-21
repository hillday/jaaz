from typing import Annotated
from pydantic import BaseModel, Field
from langchain_core.tools import tool, InjectedToolCallId  # type: ignore
from langchain_core.runnables import RunnableConfig
from tools.video_generation.video_generation_core import generate_video_with_provider
from .utils.image_utils import process_input_image


class GenerateVideoBySeedanceV1InputSchema(BaseModel):
    prompt: str = Field(
        description="必填项。视频生成的提示词。描述你想要在视频中看到的内容。"
    )
    resolution: str = Field(
        default="480p",
        description="可选。视频的分辨率。如果用户没有明确指定，使用480p。允许的值：480p、1080p。"
    )
    duration: int = Field(
        default=5,
        description="可选。视频的时长（秒）。默认使用5秒。允许的值：5、10。"
    )
    aspect_ratio: str = Field(
        default="16:9",
        description="可选。视频的宽高比。允许的值：1:1、16:9、4:3、21:9"
    )
    input_images: list[str] | None = Field(
        default=None,
        description="可选。用作参考或第一帧的图片。在此处传入图片ID列表，例如：['im_jurheut7.png']。"
    )
    camera_fixed: bool = Field(
        default=True,
        description="可选。是否保持相机固定（无相机移动）。"
    )
    tool_call_id: Annotated[str, InjectedToolCallId]


@tool("generate_video_by_seedance_v1_pro_volces",
      description="使用Seedance V1模型生成高质量视频。支持多个提供者和文生图/图生视频生成。",
      args_schema=GenerateVideoBySeedanceV1InputSchema)
async def generate_video_by_seedance_v1_pro_volces(
    prompt: str,
    config: RunnableConfig,
    tool_call_id: Annotated[str, InjectedToolCallId],
    resolution: str = "480p",
    duration: int = 5,
    aspect_ratio: str = "16:9",
    input_images: list[str] | None = None,
    camera_fixed: bool = True,
) -> str:
    """
    通过配置的提供者使用Seedance V1模型生成视频
    """

    # Process input images if provided (only use the first one)
    processed_input_images = None
    if input_images and len(input_images) > 0:
        # Only process the first image
        first_image = input_images[0]
        processed_image = await process_input_image(first_image)
        if processed_image:
            processed_input_images = [processed_image]
            print(f"正在使用输入图片进行视频生成：{first_image}")
        else:
            raise ValueError(
                f"处理输入图片失败：{first_image}。请检查图片是否存在且有效。")

    return await generate_video_with_provider(
        prompt=prompt,
        resolution=resolution,
        duration=duration,
        aspect_ratio=aspect_ratio,
        model="doubao-seedance-1-0-pro-250528",
        tool_call_id=tool_call_id,
        config=config,
        input_images=processed_input_images,
        camera_fixed=camera_fixed,
    )


# Export the tool for easy import
__all__ = ["generate_video_by_seedance_v1_pro_volces"]
