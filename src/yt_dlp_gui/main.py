import sys
import yt_dlp
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QLineEdit, QPushButton, QTextEdit,
                           QComboBox, QProgressBar, QLabel, QFileDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from pathlib import Path


class VideoDownloader(QThread):
    progress = pyqtSignal(dict)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, url, format_id, download_path):
        super().__init__()
        self.url = url
        self.format_id = format_id
        self.download_path = download_path
        self.is_cancelled = False

    def _progress_hook(self, d):
        if self.is_cancelled:
            raise Exception("다운로드가 취소되었습니다.")
        self.progress.emit(d)

    def run(self):
        try:
            ydl_opts = {
                'format': self.format_id,
                'outtmpl': str(Path(self.download_path) / '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            if not self.is_cancelled:
                self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def cancel_download(self):
        self.is_cancelled = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube 다운로더")
        self.setMinimumSize(800, 700)
        
        # 기본 다운로드 경로 설정
        self.download_path = str(Path.home() / "Downloads")
        
        # 메인 위젯과 레이아웃 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)  # 전체 여백 설정
        layout.setSpacing(15)  # 위젯 간 간격 설정
        
        # 스타일시트 설정
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                font-size: 14px;
                color: #333333;
            }
            QPushButton {
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                background-color: #4a9eff;
                color: white;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3d8ce8;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QTextEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                font-size: 13px;
                line-height: 1.4;
                color: #333333;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                font-size: 13px;
                color: #333333;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                text-align: center;
                font-size: 12px;
                height: 25px;
                color: #333333;
            }
            QProgressBar::chunk {
                background-color: #4a9eff;
                border-radius: 3px;
            }
            QLabel {
                font-size: 13px;
                color: #333333;
            }
        """)
        
        # URL 입력 레이아웃
        url_layout = QHBoxLayout()
        url_layout.setSpacing(10)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("YouTube URL을 입력하세요")
        self.fetch_btn = QPushButton("정보 가져오기")
        self.fetch_btn.setFixedWidth(120)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.fetch_btn)
        layout.addLayout(url_layout)
        
        # 정보 표시 영역
        info_label = QLabel("비디오 정보")
        info_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        layout.addWidget(info_label)
        
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setMinimumHeight(300)
        layout.addWidget(self.info_display)
        
        # 포맷 선택 영역
        format_layout = QHBoxLayout()
        format_layout.setSpacing(10)
        format_label = QLabel("포맷 선택:")
        self.format_combo = QComboBox()
        self.format_combo.setMinimumWidth(600)
        self.format_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.format_combo.view().setMinimumWidth(800)
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)
        
        # 다운로드 경로 표시 및 변경 버튼
        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)
        self.path_label = QLabel(f"저장 위치: {self.download_path}")
        self.path_label.setStyleSheet("color: #666666;")
        change_path_btn = QPushButton("위치 변경")
        change_path_btn.setFixedWidth(120)
        path_layout.addWidget(self.path_label, stretch=1)
        path_layout.addWidget(change_path_btn)
        layout.addLayout(path_layout)
        
        # 진행 상태 표시
        progress_label = QLabel("다운로드 진행 상태")
        progress_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        layout.addWidget(progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_bar)
        
        # 다운로드 버튼과 취소 버튼
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.download_btn = QPushButton("다운로드")
        self.download_btn.setFixedWidth(120)
        self.download_btn.setEnabled(False)
        self.cancel_btn = QPushButton("취소")
        self.cancel_btn.setFixedWidth(120)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4a4a;
            }
            QPushButton:hover {
                background-color: #e83d3d;
            }
        """)
        button_layout.addStretch()
        button_layout.addWidget(self.download_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        # 버튼 연결
        self.fetch_btn.clicked.connect(self.fetch_video_info)
        self.download_btn.clicked.connect(self.start_download)
        self.cancel_btn.clicked.connect(self.cancel_download)
        change_path_btn.clicked.connect(self.change_download_path)
        
        self.video_formats = []
        self.current_video_info = None
        self.downloader = None

    def fetch_video_info(self):
        url = self.url_input.text().strip()
        if not url:
            self.info_display.setText("URL을 입력해주세요.")
            return
        
        # UI 상태 업데이트 - 로딩 중
        self.fetch_btn.setEnabled(False)
        self.fetch_btn.setText("가져오는 중...")
        self.info_display.setText("비디오 정보를 가져오는 중입니다...\n잠시만 기다려주세요.")
        QApplication.processEvents()  # UI 업데이트
        
        try:
            with yt_dlp.YoutubeDL() as ydl:
                self.current_video_info = ydl.extract_info(url, download=False)
                
                # 비디오 정보 표시 텍스트 구성
                title = self.current_video_info.get('title', '제목 없음')
                channel = self.current_video_info.get('channel', '채널 정보 없음')
                channel_url = self.current_video_info.get('channel_url', '#')
                upload_date = self.current_video_info.get('upload_date', '')
                if upload_date:
                    upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
                
                duration = self.format_duration(self.current_video_info.get('duration', 0))
                view_count = self.format_number(self.current_video_info.get('view_count', 0))
                like_count = self.format_number(self.current_video_info.get('like_count', 0))
                comment_count = self.format_number(self.current_video_info.get('comment_count', 0))
                
                # 카테고리와 태그
                categories = self.current_video_info.get('categories', [])
                tags = self.current_video_info.get('tags', [])[:5]  # 처음 5개 태그만
                
                # 설명 (300자로 제한)
                description = self.current_video_info.get('description', '')
                if len(description) > 300:
                    description = description[:300] + "..."
                
                info_text = f"""제목: {title}
채널: {channel} ({channel_url})
업로드: {upload_date}
재생시간: {duration}

조회수: {view_count}
좋아요: {like_count}
댓글: {comment_count}

카테고리: {', '.join(categories) if categories else '없음'}
태그: {', '.join(tags) if tags else '없음'}

설명:
{description}
"""
                self.info_display.setText(info_text)
                
                # 포맷 정보 업데이트
                self.format_combo.clear()
                self.video_formats = []
                formats_with_info = []
                
                for f in self.current_video_info['formats']:
                    if f.get('vcodec', 'none') != 'none':
                        height = f.get('height', 0)
                        format_str = f"{height}p" if height else "??p"
                        
                        vcodec = f.get('vcodec', '').split('.')[0]
                        acodec = f.get('acodec', '').split('.')[0]
                        if vcodec and acodec != 'none':
                            format_str += f" ({vcodec}+{acodec})"
                        elif vcodec:
                            format_str += f" ({vcodec}, no audio)"
                        
                        fps = f.get('fps', 0)
                        if fps and fps > 30:
                            format_str += f" {fps}fps"
                        
                        format_str += f" - {f.get('ext', '???')}"
                        
                        if f.get('filesize'):
                            format_str += f" ({self.format_size(f['filesize'])})"
                        elif f.get('filesize_approx'):
                            format_str += f" (~{self.format_size(f['filesize_approx'])})"
                        
                        vbr = f.get('vbr', 0)
                        abr = f.get('abr', 0)
                        if vbr or abr:
                            br_info = []
                            if vbr:
                                br_info.append(f"v: {vbr}k")
                            if abr:
                                br_info.append(f"a: {abr}k")
                            format_str += f" [{'+'.join(br_info)}]"
                        
                        formats_with_info.append({
                            'height': height,
                            'fps': fps,
                            'format_str': format_str,
                            'format': f
                        })
                
                formats_with_info.sort(key=lambda x: (x['height'], x['fps']), reverse=True)
                
                for fmt in formats_with_info:
                    self.format_combo.addItem(fmt['format_str'])
                    self.video_formats.append(fmt['format'])
                
                self.download_btn.setEnabled(True)
                
        except Exception as e:
            self.info_display.setText(f"오류 발생: {str(e)}")
        finally:
            # UI 상태 복원
            self.fetch_btn.setEnabled(True)
            self.fetch_btn.setText("정보 가져오기")

    def format_number(self, num):
        """숫자를 읽기 쉬운 형태로 변환 (예: 1000 -> 1,000)"""
        return format(num, ',')

    def format_duration(self, seconds):
        """초 단위 시간을 시:분:초 형식으로 변환"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
        else:
            return f"{int(minutes):02d}:{int(seconds):02d}"

    def change_download_path(self):
        """다운로드 경로 변경"""
        new_path = QFileDialog.getExistingDirectory(
            self,
            "다운로드 위치 선택",
            self.download_path,
            QFileDialog.Option.ShowDirsOnly
        )
        if new_path:
            self.download_path = new_path
            self.path_label.setText(f"저장 위치: {self.download_path}")

    def start_download(self):
        """선택한 형식으로 다운로드 시작"""
        if not self.video_formats:
            return
            
        format_index = self.format_combo.currentIndex()
        if format_index < 0:
            return
            
        selected_format = self.video_formats[format_index]
        
        # 다운로드 시작
        self.downloader = VideoDownloader(
            self.url_input.text(),
            selected_format['format_id'],
            self.download_path
        )
        self.downloader.progress.connect(self.update_progress)
        self.downloader.finished.connect(self.download_finished)
        self.downloader.error.connect(self.download_error)
        
        # UI 상태 업데이트
        self.download_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat('준비 중...')
        
        # 다운로드 시작
        self.downloader.start()

    def cancel_download(self):
        if self.downloader and self.downloader.isRunning():
            self.downloader.cancel_download()
            self.cancel_btn.setEnabled(False)
            self.info_display.append("\n다운로드를 취소하는 중...")

    def update_progress(self, d):
        """다운로드 진행 상태 업데이트"""
        if d['status'] == 'downloading':
            # 다운로드 진행률 계산
            total = d.get('total_bytes')
            downloaded = d.get('downloaded_bytes', 0)
            
            if total is None:
                total = d.get('total_bytes_estimate', 0)
            
            if total > 0:
                # 진행률 계산 및 표시
                progress = (downloaded / total) * 100
                self.progress_bar.setValue(int(progress))
                
                # 다운로드 속도
                speed = d.get('speed', 0)
                if speed:
                    speed_str = self.format_size(speed) + '/s'
                else:
                    speed_str = '계산 중...'
                
                # ETA (예상 남은 시간)
                eta = d.get('eta', 0)
                if eta:
                    eta_str = self.format_duration(eta)
                else:
                    eta_str = '계산 중...'
                
                # 진행 상태 텍스트 업데이트
                status_text = f'{int(progress)}% ({self.format_size(downloaded)}/{self.format_size(total)}) {speed_str} ETA: {eta_str}'
                self.progress_bar.setFormat(status_text)
            else:
                self.progress_bar.setFormat(f'다운로드 중... {self.format_size(downloaded)} {self.format_size(speed)}/s')

    def format_size(self, bytes):
        """바이트 크기를 사람이 읽기 쉬운 형태로 변환"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024
        return f"{bytes:.1f} PB"

    def format_time(self, seconds):
        """초 단위 시간을 시:분:초 형식으로 변환"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
        else:
            return f"{int(minutes):02d}:{int(seconds):02d}"

    def download_finished(self):
        self.progress_bar.setValue(100)
        self.download_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.info_display.append("\n다운로드가 완료되었습니다!")

    def download_error(self, error_msg):
        self.download_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.info_display.append(f"\n오류 발생: {error_msg}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
