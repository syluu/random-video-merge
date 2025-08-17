import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import random
from moviepy import VideoFileClip, concatenate_videoclips
import threading
from pathlib import Path

class VideoMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Video Merger - Công cụ nối video ngẫu nhiên")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.selected_folder = tk.StringVar()
        self.target_duration = tk.DoubleVar(value=25.0)
        self.aspect_ratio = tk.StringVar(value="16:9")
        self.output_path = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Sẵn sàng")
        
        # Bind events to reset progress
        self.selected_folder.trace('w', self.reset_progress)
        self.target_duration.trace('w', self.reset_progress)
        self.aspect_ratio.trace('w', self.reset_progress)
        self.output_path.trace('w', self.reset_progress)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Random Video Merger", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Folder selection
        ttk.Label(main_frame, text="Thư mục chứa video:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.selected_folder, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Chọn thư mục", command=self.select_folder).grid(row=1, column=2, pady=5)
        
        # Duration and aspect ratio settings
        settings_frame = ttk.LabelFrame(main_frame, text="Cài đặt video", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        settings_frame.columnconfigure(1, weight=1)
        settings_frame.columnconfigure(3, weight=1)
        
        # Duration setting
        ttk.Label(settings_frame, text="Thời lượng (giây):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(settings_frame, textvariable=self.target_duration, width=10).grid(row=0, column=1, sticky=tk.W, padx=(5, 20))
        
        # Aspect ratio setting
        ttk.Label(settings_frame, text="Tỷ lệ khung hình:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        aspect_combo = ttk.Combobox(settings_frame, textvariable=self.aspect_ratio, width=12, state="readonly")
        aspect_combo['values'] = ('16:9 (Ngang)', '9:16 (Dọc)', '4:3 (Vuông)', '1:1 (Vuông)')
        aspect_combo.grid(row=0, column=3, sticky=tk.W, padx=(5, 0))
        aspect_combo.set('16:9 (Ngang)')  # Default value
        
        # Output path
        ttk.Label(main_frame, text="File đầu ra:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Chọn vị trí", command=self.select_output).grid(row=3, column=2, pady=5)
        
        # Process button
        self.process_button = ttk.Button(main_frame, text="Bắt đầu nối video", 
                                        command=self.start_processing, style="Accent.TButton")
        self.process_button.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Progress bar
        ttk.Label(main_frame, text="Tiến trình:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        
        # Status
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Info text
        info_text = tk.Text(main_frame, height=8, width=70, wrap=tk.WORD)
        info_text.grid(row=7, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(7, weight=1)
        
        # Scrollbar for info text
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=info_text.yview)
        scrollbar.grid(row=7, column=3, sticky=(tk.N, tk.S), pady=10)
        info_text.configure(yscrollcommand=scrollbar.set)
        
        self.info_text = info_text
        
        # Insert initial info
        info_content = """Hướng dẫn sử dụng:

1. Chọn thư mục chứa các file video (.mp4, .avi, .mov, .mkv)
2. Thiết lập thời lượng mong muốn cho video cuối
3. Chọn tỷ lệ khung hình (16:9 ngang, 9:16 dọc, 4:3 hoặc 1:1 vuông)
4. Chọn vị trí và tên file đầu ra
5. Nhấn "Bắt đầu nối video" để thực hiện

Lưu ý:
- Tool sẽ trộn ngẫu nhiên và chọn video tuần tự
- Video sẽ được cắt để đạt đúng thời lượng mong muốn
- Tất cả video sẽ được chuẩn hóa theo tỷ lệ khung hình đã chọn
- Không có video nào xuất hiện liền nhau
- Đảm bảo có đủ dung lượng ổ cứng cho file đầu ra"""
        
        self.info_text.insert(tk.END, info_content)
        self.info_text.config(state=tk.DISABLED)
        
    def reset_progress(self, *args):
        """Reset progress bar when config changes"""
        self.progress_var.set(0)
        self.status_var.set("Sẵn sàng")
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="Chọn thư mục chứa video")
        if folder:
            self.selected_folder.set(folder)
            self.log_message(f"Đã chọn thư mục: {folder}")
            self.scan_videos()
    
    def select_output(self):
        output_file = filedialog.asksaveasfilename(
            title="Chọn vị trí lưu file",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if output_file:
            self.output_path.set(output_file)
            self.log_message(f"File đầu ra: {output_file}")
    
    def scan_videos(self):
        folder = self.selected_folder.get()
        if not folder:
            return
            
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
        video_files = []
        
        try:
            for file_path in Path(folder).iterdir():
                if file_path.is_file() and file_path.suffix.lower() in video_extensions:
                    video_files.append(file_path)
            
            self.log_message(f"Tìm thấy {len(video_files)} file video trong thư mục")
            
            if len(video_files) == 0:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy file video nào trong thư mục đã chọn!")
                
        except Exception as e:
            self.log_message(f"Lỗi khi quét thư mục: {str(e)}")
    
    def log_message(self, message):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, f"\n{message}")
        self.info_text.see(tk.END)
        self.info_text.config(state=tk.DISABLED)
        self.root.update()
    
    def start_processing(self):
        # Validate inputs
        if not self.selected_folder.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục chứa video!")
            return
            
        if not self.output_path.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn vị trí lưu file đầu ra!")
            return
            
        if self.target_duration.get() <= 0:
            messagebox.showerror("Lỗi", "Thời lượng phải lớn hơn 0!")
            return
        
        # Disable button and start processing in thread
        self.process_button.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_var.set("Đang xử lý...")
        
        thread = threading.Thread(target=self.process_videos)
        thread.daemon = True
        thread.start()
    
    def process_videos(self):
        try:
            folder = self.selected_folder.get()
            target_dur = self.target_duration.get()
            output_file = self.output_path.get()
            
            # Get all video files
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
            video_files = []
            
            for file_path in Path(folder).iterdir():
                if file_path.is_file() and file_path.suffix.lower() in video_extensions:
                    video_files.append(str(file_path))
            
            if not video_files:
                raise Exception("Không tìm thấy file video nào!")
            
            self.log_message(f"Bắt đầu xử lý {len(video_files)} file video...")
            self.progress_var.set(10)
            
            # Shuffle videos randomly and select sequentially until target duration
            self.log_message("Đang trộn ngẫu nhiên danh sách video...")
            random.shuffle(video_files)
            
            selected_videos = []
            total_duration = 0
            last_selected = None
            
            self.log_message(f"Chọn video để đạt thời lượng {target_dur}s...")
            
            # Continue selecting videos until we reach exact target duration
            attempts = 0
            max_attempts = len(video_files) * 3  # Allow multiple passes through video list
            
            while total_duration < target_dur and attempts < max_attempts:
                video_added_this_round = False
                
                for video_file in video_files:
                    attempts += 1
                    
                    # Skip if same as last selected to avoid consecutive
                    if video_file == last_selected:
                        continue
                        
                    try:
                        # Get video duration
                        temp_clip = VideoFileClip(video_file)
                        video_duration = temp_clip.duration
                        temp_clip.close()
                        
                        # Calculate how much we need
                        remaining_duration = target_dur - total_duration
                        
                        if remaining_duration <= 0:
                            break
                        
                        # Use this video (will trim if needed)
                        use_duration = min(video_duration, remaining_duration)
                        selected_videos.append({
                            'file': video_file, 
                            'full_duration': video_duration,
                            'use_duration': use_duration
                        })
                        total_duration += use_duration
                        last_selected = video_file
                        video_added_this_round = True
                        
                        self.log_message(f"Đã chọn: {Path(video_file).name} - Sử dụng {use_duration:.1f}s/{video_duration:.1f}s (Tổng: {total_duration:.1f}s/{target_dur}s)")
                        
                        if total_duration >= target_dur:
                            break
                            
                    except Exception as e:
                        self.log_message(f"Lỗi khi đọc video {Path(video_file).name}: {str(e)}")
                        continue
                
                # If we completed the target duration, break out of while loop
                if total_duration >= target_dur:
                    break
                    
                # If no video was added this round, we might be stuck
                if not video_added_this_round:
                    self.log_message("Không thể thêm video nào nữa, cho phép tái sử dụng video...")
                    last_selected = None  # Reset to allow reusing videos
            
            if not selected_videos:
                raise Exception("Không thể chọn video nào!")
            
            if total_duration < target_dur:
                self.log_message(f"Cảnh báo: Chỉ đạt được {total_duration:.1f}s/{target_dur}s - Thiếu {target_dur - total_duration:.1f}s")
            elif total_duration > target_dur:
                self.log_message(f"Lưu ý: Video cuối sẽ được cắt để đạt đúng {target_dur}s")
            
            self.log_message(f"Hoàn thành chọn video: {len(selected_videos)} video - Thời lượng thực tế: {total_duration:.1f}s")
            self.log_message(f"Mục tiêu: {target_dur}s - Chêng lệch: {abs(target_dur - total_duration):.1f}s")
            self.progress_var.set(30)
            
            # Load and normalize videos
            self.log_message("Đang tải và chuẩn hóa video...")
            clips = []
            target_fps = None
            target_size = None
            
            # Determine target fps and size based on aspect ratio selection
            aspect_ratio_text = self.aspect_ratio.get()
            target_fps = 30.0  # Standard fps
            
            # Parse aspect ratio and set target size
            if '16:9' in aspect_ratio_text:
                target_size = (1920, 1080)  # Full HD landscape
                self.log_message("Chuẩn hóa theo tỷ lệ 16:9 (Ngang) - 1920x1080")
            elif '9:16' in aspect_ratio_text:
                target_size = (1080, 1920)  # Full HD portrait
                self.log_message("Chuẩn hóa theo tỷ lệ 9:16 (Dọc) - 1080x1920")
            elif '4:3' in aspect_ratio_text:
                target_size = (1440, 1080)  # 4:3 aspect ratio
                self.log_message("Chuẩn hóa theo tỷ lệ 4:3 (Vuông) - 1440x1080")
            elif '1:1' in aspect_ratio_text:
                target_size = (1080, 1080)  # Square
                self.log_message("Chuẩn hóa theo tỷ lệ 1:1 (Vuông) - 1080x1080")
            else:
                target_size = (1920, 1080)  # Default to 16:9
                self.log_message("Sử dụng mặc định 16:9 - 1920x1080")
            
            self.log_message(f"Chuẩn hóa video theo: {target_size[0]}x{target_size[1]} @ {target_fps}fps")
            
            # Load and process clips with exact trimming and fallback replacement
            clips = []
            actual_total_duration = 0
            
            # Create a list of unused videos for fallback
            used_files = [v['file'] for v in selected_videos]
            unused_videos = [f for f in video_files if f not in used_files]
            
            for i, video_info in enumerate(selected_videos):
                clip_loaded = False
                attempts = 0
                max_fallback_attempts = 3
                current_video_info = video_info
                
                while not clip_loaded and attempts < max_fallback_attempts:
                    try:
                        clip = VideoFileClip(current_video_info['file'])
                        
                        # Trim clip to exact duration needed
                        if current_video_info['use_duration'] < current_video_info['full_duration']:
                            clip = clip.subclipped(0, current_video_info['use_duration'])
                            self.log_message(f"Cắt video: {Path(current_video_info['file']).name} -> {current_video_info['use_duration']:.1f}s")
                        
                        # Normalize fps and size using correct MoviePy methods
                        if clip.fps != target_fps:
                            clip = clip.with_fps(target_fps)
                        
                        # Resize with proper aspect ratio handling
                        if clip.size != target_size:
                            # Resize and center crop to maintain aspect ratio
                            clip = clip.resized(target_size).with_position('center')
                        
                        clips.append(clip)
                        actual_total_duration += clip.duration
                        clip_loaded = True
                        
                        progress = 30 + (i + 1) / len(selected_videos) * 40
                        self.progress_var.set(progress)
                        self.log_message(f"Đã chuẩn hóa: {Path(current_video_info['file']).name}")
                        
                    except Exception as e:
                        attempts += 1
                        self.log_message(f"Lỗi khi tải video {Path(current_video_info['file']).name}: {str(e)}")
                        
                        # Try to find a replacement video
                        if unused_videos and attempts < max_fallback_attempts:
                            replacement_file = unused_videos.pop(0)
                            
                            try:
                                # Get replacement video duration
                                temp_clip = VideoFileClip(replacement_file)
                                replacement_duration = temp_clip.duration
                                temp_clip.close()
                                
                                # Calculate how much we need for replacement
                                needed_duration = current_video_info['use_duration']
                                use_duration = min(replacement_duration, needed_duration)
                                
                                current_video_info = {
                                    'file': replacement_file,
                                    'full_duration': replacement_duration,
                                    'use_duration': use_duration
                                }
                                
                                self.log_message(f"Thay thế bằng video: {Path(replacement_file).name} - Sử dụng {use_duration:.1f}s/{replacement_duration:.1f}s")
                                
                            except Exception as replacement_error:
                                self.log_message(f"Lỗi khi thử video thay thế {Path(replacement_file).name}: {str(replacement_error)}")
                                continue
                        else:
                            self.log_message(f"Không thể tìm video thay thế cho {Path(current_video_info['file']).name}")
                            break
                
                if not clip_loaded:
                    self.log_message(f"Bỏ qua video {Path(video_info['file']).name} sau {attempts} lần thử")
            
            if not clips:
                raise Exception("Không thể tải video nào!")
            
            self.progress_var.set(70)
            self.log_message("Đang ghép video...")
            
            # Concatenate clips with method='compose'
            final_video = concatenate_videoclips(clips, method='compose')
            
            self.progress_var.set(80)
            self.log_message("Đang xuất video...")
            
            # Write final video with optimized settings
            final_video.write_videofile(
                output_file,
                codec='libx264',
                audio_codec='aac',
                fps=target_fps,
                preset='medium',
                ffmpeg_params=['-crf', '23'],
                logger=None
            )
            
            # Clean up
            for clip in clips:
                clip.close()
            final_video.close()
            
            self.progress_var.set(100)
            self.status_var.set("Hoàn thành!")
            # Check if we need to add more videos to reach target duration
            if actual_total_duration < target_dur:
                shortage = target_dur - actual_total_duration
                self.log_message(f"Thiếu {shortage:.1f}s, tìm thêm video...")
                
                # Try to add more videos from unused list
                for unused_file in unused_videos:
                    if actual_total_duration >= target_dur:
                        break
                        
                    try:
                        temp_clip = VideoFileClip(unused_file)
                        unused_duration = temp_clip.duration
                        temp_clip.close()
                        
                        remaining_needed = target_dur - actual_total_duration
                        use_duration = min(unused_duration, remaining_needed)
                        
                        # Load and process the additional video
                        clip = VideoFileClip(unused_file)
                        if use_duration < unused_duration:
                            clip = clip.subclipped(0, use_duration)
                            self.log_message(f"Thêm và cắt video: {Path(unused_file).name} -> {use_duration:.1f}s")
                        else:
                            self.log_message(f"Thêm video: {Path(unused_file).name} -> {use_duration:.1f}s")
                        
                        # Normalize fps and size using correct MoviePy methods
                        if clip.fps != target_fps:
                            clip = clip.with_fps(target_fps)
                        if clip.size != target_size:
                            # Resize and center crop to maintain aspect ratio
                            clip = clip.resized(target_size).with_position('center')
                        
                        clips.append(clip)
                        actual_total_duration += clip.duration
                        
                    except Exception as e:
                        self.log_message(f"Lỗi khi thêm video {Path(unused_file).name}: {str(e)}")
                        continue
            
            # Calculate actual final duration
            actual_duration = actual_total_duration
            
            self.log_message(f"Đã tạo video thành công: {output_file}")
            self.log_message(f"Thời lượng cuối: {actual_duration:.1f}s")
            self.log_message(f"Số video đã ghép: {len(clips)} video")
            
            messagebox.showinfo("Thành công", f"Video đã được tạo thành công!\nFile: {output_file}\nThời lượng: {actual_duration:.1f}s\nSố video: {len(clips)}")
            
        except Exception as e:
            self.progress_var.set(0)  # Reset progress on error
            self.status_var.set("Có lỗi xảy ra!")
            self.log_message(f"Lỗi: {str(e)}")
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra:\n{str(e)}")
        
        finally:
            self.process_button.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = VideoMergerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
