from typing import Annotated
from pydantic import BaseModel, Field
from langchain_core.tools import tool, InjectedToolCallId  # type: ignore
from langchain_core.runnables import RunnableConfig
from .video_generation import generate_video_with_provider
from .utils.image_utils import process_input_image


class GenerateVideoBySeedanceV1LiteInputI2VSchema(BaseModel):
    prompt: str = Field(
        description="必填项。视频生成的提示词。描述你想要在视频中看到的内容。"
    )
    resolution: str = Field(
        default="480p",
        description="可选。视频的分辨率。如果用户没有明确指定，使用480p。允许的值：480p、720p。"
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
        description="可选。用作参考、第一帧或最后一帧的图片。按顺序传入图片ID列表，例如：['im_jurheut7.png']。"
    )
    camera_fixed: bool = Field(
        default=True,
        description="可选。是否保持相机固定（无相机移动）。"
    )
    tool_call_id: Annotated[str, InjectedToolCallId]


class GenerateVideoBySeedanceV1LiteInputT2VSchema(BaseModel):
    prompt: str = Field(
        description="Required. The prompt for video generation. Describe what you want to see in the video."
    )
    resolution: str = Field(
        default="480p",
        description="Optional. The resolution of the video. Use 480p if not explicitly specified by user. Allowed values: 480p, 720p."
    )
    duration: int = Field(
        default=5,
        description="Optional. The duration of the video in seconds. Use 5 by default. Allowed values: 5, 10."
    )
    aspect_ratio: str = Field(
        default="16:9",
        description="Optional. The aspect ratio of the video. Allowed values: 1:1, 16:9, 4:3, 21:9"
    )
    camera_fixed: bool = Field(
        default=True,
        description="Optional. Whether to keep the camera fixed (no camera movement)."
    )
    tool_call_id: Annotated[str, InjectedToolCallId]


@tool("generate_video_by_seedance_v1_lite_i2v",
      description="使用Seedance V1 Lite模型生成高质量视频。支持图生视频/首尾帧视频生成。",
      args_schema=GenerateVideoBySeedanceV1LiteInputI2VSchema)
async def generate_video_by_seedance_v1_lite_i2v(
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
    if input_images is None:
        raise ValueError(
            "图生视频生成必须提供输入图片。")

    # Process input images if provided (only use the first one)
    processed_input_images = None
    if len(input_images) > 1:
        # first-last-frame-to-video
        first_image = input_images[0]
        last_frame = input_images[-1]
        processed_first_image = await process_input_image(first_image)
        processed_last_frame = await process_input_image(last_frame)
        if processed_first_image and processed_last_frame:
            processed_input_images = [
                processed_first_image, processed_last_frame]
            print(
                f"正在使用输入图片进行视频生成：{first_image}，{last_frame}")
        else:
            raise ValueError(
                f"处理输入图片失败：{first_image}。请检查图片是否存在且有效。")
    else:
        # image-to-video
        processed_image = await process_input_image(input_images[0])
        if processed_image:
            processed_input_images = [processed_image]
            print(f"正在使用输入图片进行视频生成：{input_images[0]}")
        else:
            raise ValueError(
                f"处理输入图片失败：{input_images[0]}。请检查图片是否存在且有效。")

    return await generate_video_with_provider(
        prompt=prompt,
        resolution=resolution,
        duration=duration,
        aspect_ratio=aspect_ratio,
        model="doubao-seedance-1-0-lite-i2v-250428",
        tool_call_id=tool_call_id,
        config=config,
        input_images=processed_input_images,
        camera_fixed=camera_fixed,
    )


@tool("generate_video_by_seedance_v1_lite_t2v",
      description="使用Seedance V1 Lite模型生成高质量视频。支持文生视频生成。",
      args_schema=GenerateVideoBySeedanceV1LiteInputT2VSchema)
async def generate_video_by_seedance_v1_lite_t2v(
    prompt: str,
    config: RunnableConfig,
    tool_call_id: Annotated[str, InjectedToolCallId],
    resolution: str = "480p",
    duration: int = 5,
    aspect_ratio: str = "16:9",
    camera_fixed: bool = True,
) -> str:
    """
    通过配置的提供者使用Seedance V1模型生成视频
    """

    return await generate_video_with_provider(
        prompt=prompt,
        resolution=resolution,
        duration=duration,
        aspect_ratio=aspect_ratio,
        model="doubao-seedance-1-0-lite-t2v-250428",
        tool_call_id=tool_call_id,
        config=config,
        camera_fixed=camera_fixed,
    )


# Export the tool for easy import
__all__ = ["generate_video_by_seedance_v1_lite_i2v",
           "generate_video_by_seedance_v1_lite_t2v"]
