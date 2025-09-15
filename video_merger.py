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
        self.root.title("Video Tool - Công cụ xử lý video")
        self.root.geometry("650x550")
        self.root.resizable(True, True)
        
        # Variables for merge feature
        self.selected_folder = tk.StringVar()
        self.target_duration = tk.DoubleVar(value=25.0)
        self.aspect_ratio = tk.StringVar(value="16:9")
        self.output_path = tk.StringVar()
        
        # Variables for split feature
        self.split_input_files = []  # List to store multiple files
        self.split_display_text = tk.StringVar()  # For displaying selected files
        self.split_output_folder = tk.StringVar()
        self.split_duration = tk.DoubleVar(value=5.0)
        
        # Common variables
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Sẵn sàng")
        
        # Bind events to reset progress
        self.selected_folder.trace('w', self.reset_progress)
        self.target_duration.trace('w', self.reset_progress)
        self.aspect_ratio.trace('w', self.reset_progress)
        self.output_path.trace('w', self.reset_progress)
        self.split_display_text.trace('w', self.reset_progress)
        self.split_output_folder.trace('w', self.reset_progress)
        self.split_duration.trace('w', self.reset_progress)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Video Tool - Công cụ xử lý video", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Merge tab
        self.merge_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.merge_frame, text="Gộp Video")
        self.setup_merge_tab()
        
        # Split tab
        self.split_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.split_frame, text="Tách Video")
        self.setup_split_tab()
        
        # Progress and status (common to both tabs)
        progress_frame = ttk.Frame(main_frame, padding="10")
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        progress_frame.columnconfigure(1, weight=1)
        
        # Progress bar
        ttk.Label(progress_frame, text="Tiến trình:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        
        # Status
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)
    
    def setup_merge_tab(self):
        # Configure grid weights
        self.merge_frame.columnconfigure(1, weight=1)
        
        # Folder selection
        ttk.Label(self.merge_frame, text="Thư mục chứa video:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.merge_frame, textvariable=self.selected_folder, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(self.merge_frame, text="Chọn thư mục", command=self.select_folder).grid(row=0, column=2, pady=5)
        
        # Duration and aspect ratio settings
        settings_frame = ttk.LabelFrame(self.merge_frame, text="Cài đặt video", padding="10")
        settings_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
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
        ttk.Label(self.merge_frame, text="File đầu ra:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.merge_frame, textvariable=self.output_path, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(self.merge_frame, text="Chọn vị trí", command=self.select_output).grid(row=2, column=2, pady=5)
        
        # Process button
        self.merge_button = ttk.Button(self.merge_frame, text="Bắt đầu nối video", 
                                       command=self.start_merge_processing, style="Accent.TButton")
        self.merge_button.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Info text
        info_text = tk.Text(self.merge_frame, height=6, width=70, wrap=tk.WORD)
        info_text.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.merge_frame.rowconfigure(4, weight=1)
        
        # Scrollbar for info text
        scrollbar = ttk.Scrollbar(self.merge_frame, orient=tk.VERTICAL, command=info_text.yview)
        scrollbar.grid(row=4, column=3, sticky=(tk.N, tk.S), pady=10)
        info_text.configure(yscrollcommand=scrollbar.set)
        
        self.merge_info_text = info_text
        
        # Insert initial info
        info_content = """Hướng dẫn gộp video:

1. Chọn thư mục chứa các file video (.mp4, .avi, .mov, .mkv)
2. Thiết lập thời lượng mong muốn cho video cuối
3. Chọn tỷ lệ khung hình (16:9 ngang, 9:16 dọc, 4:3 hoặc 1:1 vuông)
4. Chọn vị trí và tên file đầu ra
5. Nhấn "Bắt đầu nối video" để thực hiện

Lưu ý:
- Tool sẽ trộn ngẫu nhiên và chọn video tuần tự
- Video sẽ được cắt để đạt đúng thời lượng mong muốn
- Tất cả video sẽ được chuẩn hóa theo tỷ lệ khung hình đã chọn"""
        
        self.merge_info_text.insert(tk.END, info_content)
        self.merge_info_text.config(state=tk.DISABLED)
    
    def setup_split_tab(self):
        # Configure grid weights
        self.split_frame.columnconfigure(1, weight=1)
        
        # Input files selection
        ttk.Label(self.split_frame, text="Chọn video cần tách:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.split_frame, textvariable=self.split_display_text, width=50, state="readonly").grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        
        # Buttons for file selection
        button_frame = ttk.Frame(self.split_frame)
        button_frame.grid(row=0, column=2, padx=(5, 0), pady=5)
        
        ttk.Button(button_frame, text="Chọn video", command=self.select_split_input).grid(row=0, column=0, pady=(0, 2))
        ttk.Button(button_frame, text="Xóa tất cả", command=self.clear_split_input).grid(row=1, column=0)
        
        # Output folder selection
        ttk.Label(self.split_frame, text="Thư mục lưu video tách:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.split_frame, textvariable=self.split_output_folder, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(self.split_frame, text="Chọn thư mục", command=self.select_split_output).grid(row=1, column=2, pady=5)
        
        # Split duration setting
        duration_frame = ttk.LabelFrame(self.split_frame, text="Cài đặt tách video", padding="10")
        duration_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(duration_frame, text="Thời lượng mỗi đoạn (giây):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(duration_frame, textvariable=self.split_duration, width=10).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Process button
        self.split_button = ttk.Button(self.split_frame, text="Bắt đầu tách video", 
                                       command=self.start_split_processing, style="Accent.TButton")
        self.split_button.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Info text
        split_info_text = tk.Text(self.split_frame, height=6, width=70, wrap=tk.WORD)
        split_info_text.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.split_frame.rowconfigure(4, weight=1)
        
        # Scrollbar for info text
        split_scrollbar = ttk.Scrollbar(self.split_frame, orient=tk.VERTICAL, command=split_info_text.yview)
        split_scrollbar.grid(row=4, column=3, sticky=(tk.N, tk.S), pady=10)
        split_info_text.configure(yscrollcommand=split_scrollbar.set)
        
        self.split_info_text = split_info_text
        
        # Insert initial info
        split_info_content = """Hướng dẫn tách video:

1. Chọn video cần tách (.mp4, .avi, .mov, .mkv) - có thể chọn nhiều file
2. Chọn thư mục để lưu các video được tách
3. Thiết lập thời lượng cho mỗi đoạn video (ví dụ: 5 giây)
4. Nhấn "Bắt đầu tách video" để thực hiện

Tính năng mới:
- ✨ Hỗ trợ tách nhiều video cùng lúc
- Có thể chọn thêm video sau khi đã chọn trước đó
- Nút "Xóa tất cả" để bỏ chọn tất cả video

Lưu ý:
- Mỗi video sẽ được tách thành các đoạn riêng biệt
- Tên file: tên_video_001.mp4, tên_video_002.mp4, ..."""
        
        self.split_info_text.insert(tk.END, split_info_content)
        self.split_info_text.config(state=tk.DISABLED)
        
        # Initialize display
        self.update_split_display()
        
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
            self.log_merge_message(f"File đầu ra: {output_file}")
    
    def select_split_input(self):
        input_files = filedialog.askopenfilenames(
            title="Chọn video cần tách (có thể chọn nhiều file)",
            filetypes=[
                ("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv;*.flv;*.webm"),
                ("MP4 files", "*.mp4"),
                ("AVI files", "*.avi"),
                ("MOV files", "*.mov"),
                ("MKV files", "*.mkv"),
                ("All files", "*.*")
            ]
        )
        if input_files:
            # Add new files to existing list (avoid duplicates)
            for file in input_files:
                if file not in self.split_input_files:
                    self.split_input_files.append(file)
            
            self.update_split_display()
            self.log_split_message(f"Đã chọn {len(input_files)} video mới")
            self.log_split_message(f"Tổng cộng: {len(self.split_input_files)} video")
            
            # Show info for each new video
            for input_file in input_files:
                if input_file not in self.split_input_files[:-len(input_files)]:  # Only new files
                    try:
                        temp_clip = VideoFileClip(input_file)
                        duration = temp_clip.duration
                        temp_clip.close()
                        filename = Path(input_file).name
                        self.log_split_message(f"- {filename}: {duration:.1f} giây")
                    except Exception as e:
                        filename = Path(input_file).name
                        self.log_split_message(f"- {filename}: Lỗi đọc video - {str(e)}")
    
    def clear_split_input(self):
        self.split_input_files.clear()
        self.update_split_display()
        self.log_split_message("Đã xóa tất cả video đã chọn")
    
    def update_split_display(self):
        if not self.split_input_files:
            self.split_display_text.set("Chưa chọn video nào")
        elif len(self.split_input_files) == 1:
            filename = Path(self.split_input_files[0]).name
            self.split_display_text.set(f"1 video: {filename}")
        else:
            self.split_display_text.set(f"{len(self.split_input_files)} video được chọn")
    
    def select_split_output(self):
        output_folder = filedialog.askdirectory(title="Chọn thư mục lưu video tách")
        if output_folder:
            self.split_output_folder.set(output_folder)
            self.log_split_message(f"Thư mục đầu ra: {output_folder}")
    
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
        # Legacy method - log to merge tab by default
        self.log_merge_message(message)
    
    def log_merge_message(self, message):
        self.merge_info_text.config(state=tk.NORMAL)
        self.merge_info_text.insert(tk.END, f"\n{message}")
        self.merge_info_text.see(tk.END)
        self.merge_info_text.config(state=tk.DISABLED)
        self.root.update()
    
    def log_split_message(self, message):
        self.split_info_text.config(state=tk.NORMAL)
        self.split_info_text.insert(tk.END, f"\n{message}")
        self.split_info_text.see(tk.END)
        self.split_info_text.config(state=tk.DISABLED)
        self.root.update()
    
    def start_merge_processing(self):
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
        self.merge_button.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_var.set("Đang xử lý...")
        
        thread = threading.Thread(target=self.process_videos)
        thread.daemon = True
        thread.start()
    
    def start_split_processing(self):
        # Validate inputs
        if not self.split_input_files:
            messagebox.showerror("Lỗi", "Vui lòng chọn ít nhất một video cần tách!")
            return
            
        if not self.split_output_folder.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục lưu video tách!")
            return
            
        if self.split_duration.get() <= 0:
            messagebox.showerror("Lỗi", "Thời lượng mỗi đoạn phải lớn hơn 0!")
            return
        
        # Disable button and start processing in thread
        self.split_button.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_var.set("Đang tách video...")
        
        thread = threading.Thread(target=self.split_video)
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
            self.merge_button.config(state=tk.NORMAL)
    
    def split_video(self):
        try:
            input_files = self.split_input_files.copy()
            output_folder = self.split_output_folder.get()
            segment_duration = self.split_duration.get()
            
            self.log_split_message(f"Bắt đầu tách {len(input_files)} video")
            self.log_split_message(f"Thời lượng mỗi đoạn: {segment_duration} giây")
            self.progress_var.set(5)
            
            total_segments_created = 0
            total_videos_processed = 0
            
            # Process each video file
            for video_index, input_file in enumerate(input_files):
                try:
                    filename = Path(input_file).name
                    self.log_split_message(f"\n=== Xử lý video {video_index + 1}/{len(input_files)}: {filename} ===")
                    
                    # Get video info first
                    temp_clip = VideoFileClip(input_file)
                    total_duration = temp_clip.duration
                    fps = temp_clip.fps
                    temp_clip.close()
                    
                    self.log_split_message(f"Thời lượng video: {total_duration:.1f} giây")
                    
                    # Calculate number of segments for this video
                    num_segments = int(total_duration / segment_duration)
                    if total_duration % segment_duration > 0:
                        num_segments += 1  # Add one more for the remainder
                    
                    self.log_split_message(f"Sẽ tách thành {num_segments} đoạn video")
                    
                    # Get base filename without extension
                    base_filename = Path(input_file).stem
                    
                    # Split the video into segments - load fresh clip for each segment
                    for i in range(num_segments):
                        start_time = i * segment_duration
                        end_time = min((i + 1) * segment_duration, total_duration)
                        
                        # Create output filename with zero-padded numbering
                        output_filename = f"{base_filename}_{i+1:03d}.mp4"
                        output_path = Path(output_folder) / output_filename
                        
                        self.log_split_message(f"Đang tạo đoạn {i+1}/{num_segments}: {output_filename} ({end_time-start_time:.1f}s)")
                        
                        segment = None
                        fresh_clip = None
                        try:
                            # Load a fresh clip for each segment to avoid ffmpeg corruption
                            fresh_clip = VideoFileClip(input_file)
                            segment = fresh_clip.subclipped(start_time, end_time)
                            
                            # Write the segment with basic parameters
                            segment.write_videofile(
                                str(output_path),
                                codec='libx264',
                                audio_codec='aac',
                                fps=fps,
                                preset='medium',
                                ffmpeg_params=['-crf', '23'],
                                logger=None
                            )
                            
                            self.log_split_message(f"Hoàn thành: {output_filename}")
                            total_segments_created += 1
                            
                        except Exception as segment_error:
                            self.log_split_message(f"Lỗi khi tạo {output_filename}: {str(segment_error)}")
                            # Try alternative approach with minimal parameters
                            try:
                                if segment:
                                    segment.close()
                                if fresh_clip:
                                    fresh_clip.close()
                                fresh_clip = VideoFileClip(input_file)
                                segment = fresh_clip.subclipped(start_time, end_time)
                                segment.write_videofile(
                                    str(output_path),
                                    logger=None
                                )
                                self.log_split_message(f"Hoàn thành (phương pháp thay thế): {output_filename}")
                                total_segments_created += 1
                            except Exception as fallback_error:
                                self.log_split_message(f"Không thể tạo {output_filename}: {str(fallback_error)}")
                                continue
                        
                        finally:
                            # Clean up
                            try:
                                if segment:
                                    segment.close()
                                if fresh_clip:
                                    fresh_clip.close()
                            except:
                                pass
                        
                        # Update progress based on overall completion
                        overall_progress = 5 + ((video_index * 100 + ((i + 1) / num_segments) * 100) / len(input_files)) * 0.9
                        self.progress_var.set(overall_progress)
                    
                    total_videos_processed += 1
                    self.log_split_message(f"Hoàn thành video: {filename}")
                    
                except Exception as video_error:
                    filename = Path(input_file).name
                    self.log_split_message(f"Lỗi khi xử lý video {filename}: {str(video_error)}")
                    continue
            
            self.progress_var.set(100)
            self.status_var.set("Hoàn thành!")
            self.log_split_message(f"\n=== KẾT QUẢ ===")
            self.log_split_message(f"Đã xử lý: {total_videos_processed}/{len(input_files)} video")
            self.log_split_message(f"Tổng số đoạn được tạo: {total_segments_created}")
            self.log_split_message(f"Các file được lưu trong: {output_folder}")
            
            messagebox.showinfo("Thành công", 
                              f"Tách video hoàn thành!\n"
                              f"Đã xử lý: {total_videos_processed}/{len(input_files)} video\n"
                              f"Tổng số đoạn: {total_segments_created}\n"
                              f"Thư mục: {output_folder}")
            
        except Exception as e:
            self.progress_var.set(0)
            self.status_var.set("Có lỗi xảy ra!")
            self.log_split_message(f"Lỗi: {str(e)}")
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi tách video:\n{str(e)}")
        
        finally:
            self.split_button.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = VideoMergerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
