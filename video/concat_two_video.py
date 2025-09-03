from moviepy.editor import VideoFileClip, clips_array

# 读取视频
clip1 = VideoFileClip(r"E:\myJobTwo\project\onnxruntime_yolo_c\cmake-build-debug-visual-studio\t2..mp4")
clip2 = VideoFileClip(r"E:\myJobTwo\project\onnxruntime_yolo_c\cmake-build-debug-visual-studio\output.mp4")

# 确保两个视频宽度一致，如果不一致则调整
if clip1.w != clip2.w:
    clip2 = clip2.resize(width=clip1.w)

# 上下拼接
final_clip = clips_array([[clip1], [clip2]])

# 输出视频
final_clip.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
