import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider, Button
import math

plt.style.use('dark_background')
# Tắt toolbar TRƯỚC khi tạo figure
plt.rcParams['toolbar'] = 'None'

class SimplePrismSimulator:
    def __init__(self):
        # Tham số vật lý
        self.n1 = 1.0  # Không khí
        self.n2 = 1.5  # Lăng kính
        self.theta1 = 45  # Góc tới (độ)
        self.prism_angle = 60  # Góc lăng kính
        
        # Màu sắc cho tán sắc
        self.colors = ['#8A2BE2', '#4169E1', '#00BFFF', '#00FF00', '#FFFF00', '#FFA500', '#FF0000']
        self.wavelengths = ['380nm', '450nm', '485nm', '510nm', '570nm', '590nm', '650nm']
        self.n_colors = [1.532, 1.528, 1.525, 1.522, 1.520, 1.518, 1.515]
        
        # Trạng thái hiển thị
        self.show_dispersion = False
        self.show_angles = True
        self.show_normals = False
        
        self.setup_figure()
        self.create_widgets()
        self.setup_zoom()
        self.update_plot()
        
    def setup_figure(self):
        """Thiết lập figure và axes"""
        self.fig = plt.figure(figsize=(14, 10), facecolor='#1a1a2e')
        self.fig.suptitle('MO PHONG LANG KINH CHINH XAC', 
                         fontsize=16, fontweight='bold', color='white', y=0.95)
        
        # Layout
        gs = self.fig.add_gridspec(2, 2, height_ratios=[3, 1], width_ratios=[3, 1], 
                                  hspace=0.3, wspace=0.2)
        
        # Axes chính
        self.ax_main = self.fig.add_subplot(gs[0, 0])
        self.ax_main.set_facecolor('#16213e')
        
        # Panel thông tin
        self.ax_info = self.fig.add_subplot(gs[0, 1])
        self.ax_info.set_facecolor('#1a1a2e')
        self.ax_info.axis('off')
        
        # Controls
        self.ax_controls = self.fig.add_subplot(gs[1, :])
        self.ax_controls.axis('off')
        
    def create_widgets(self):
        """Tạo widgets điều khiển"""
        # Slider parameters
        slider_height = 0.03
        slider_width = 0.25
        left_margin = 0.1
        bottom_start = 0.25
        spacing = 0.05
        
        # Slider n1 (chỉ số khúc xạ môi trường)
        ax_n1 = plt.axes([left_margin, bottom_start, slider_width, slider_height])
        self.slider_n1 = Slider(ax_n1, 'n₁ (không khí)', 0.8, 1.5, 
                               valinit=self.n1, valfmt='%.2f')
        
        # Slider n2 (chỉ số khúc xạ lăng kính)
        ax_n2 = plt.axes([left_margin, bottom_start - spacing, slider_width, slider_height])
        self.slider_n2 = Slider(ax_n2, 'n₂ (lăng kính)', 1.0, 2.5, 
                               valinit=self.n2, valfmt='%.2f')
        
        # Slider góc tới
        ax_theta = plt.axes([left_margin, bottom_start - 2*spacing, slider_width, slider_height])
        self.slider_theta = Slider(ax_theta, 'Góc tới θ₁ (°)', 0, 85, 
                                  valinit=self.theta1, valfmt='%.1f°')
        
        # Slider góc lăng kính
        ax_prism = plt.axes([left_margin, bottom_start - 3*spacing, slider_width, slider_height])
        self.slider_prism_angle = Slider(ax_prism, 'Góc lăng kính A (°)', 30, 90, 
                                        valinit=self.prism_angle, valfmt='%.1f°')
        
        # 3 nút điều khiển
        button_width = 0.08
        button_height = 0.04
        button_left = left_margin + slider_width + 0.05
        
        # Nút Reset
        ax_reset = plt.axes([button_left, bottom_start, button_width, button_height])
        self.btn_reset = Button(ax_reset, 'Reset', color='lightcoral')
        
        # Nút Tán sắc
        ax_dispersion = plt.axes([button_left, bottom_start - spacing, button_width, button_height])
        self.btn_dispersion = Button(ax_dispersion, 'Tán sắc', color='lightblue')
        
        # Nút Bình thường
        ax_normal = plt.axes([button_left, bottom_start - 2*spacing, button_width, button_height])
        self.btn_normal = Button(ax_normal, 'Bình thường', color='lightgreen')
        
        # Nút Chụp ảnh
        ax_screenshot = plt.axes([button_left, bottom_start - 3*spacing, button_width, button_height])
        self.btn_screenshot = Button(ax_screenshot, 'Chụp ảnh', color='lightyellow')
        
        # Connect events
        self.slider_n1.on_changed(self.update_plot)
        self.slider_n2.on_changed(self.update_plot)
        self.slider_theta.on_changed(self.update_plot)
        self.slider_prism_angle.on_changed(self.update_plot)
        self.btn_reset.on_clicked(self.reset_values)
        self.btn_dispersion.on_clicked(self.toggle_dispersion)
        self.btn_normal.on_clicked(self.set_normal_mode)
        self.btn_screenshot.on_clicked(self.take_screenshot)
        
    def snell_law(self, n1, n2, theta1):
        """Định luật Snell"""
        if theta1 == 0:
            return 0
        
        theta1_rad = math.radians(abs(theta1))
        sin_theta2 = (n1 / n2) * math.sin(theta1_rad)
        
        if abs(sin_theta2) > 1:
            return None  # Phản xạ toàn phần
            
        theta2_rad = math.asin(sin_theta2)
        theta2 = math.degrees(theta2_rad)
        
        # Giữ dấu
        return theta2 if theta1 >= 0 else -theta2
    
    def calculate_prism_ray(self, n_medium):
        """Tính toán tia sáng qua lăng kính"""
        n1 = self.slider_n1.val
        n2 = n_medium  
        theta1 = self.slider_theta.val
        A = self.slider_prism_angle.val
        
        # Bước 1: Khúc xạ tại mặt vào
        r1 = self.snell_law(n1, n2, theta1)
        if r1 is None:
            return {"error": "Phản xạ toàn phần tại mặt vào"}
        
        # Bước 2: Góc tới tại mặt ra
        r2 = A - r1
        if r2 < 0:
            return {"error": "Tia không đến mặt ra"}
        
        # Bước 3: Khúc xạ tại mặt ra
        theta2 = self.snell_law(n2, n1, r2)
        if theta2 is None:
            return {"error": "Phản xạ toàn phần tại mặt ra"}
        
        # Bước 4: Tính góc lệch
        delta = theta1 + theta2 - A
        
        return {
            "theta1": theta1,    # Góc tới
            "r1": r1,           # Góc khúc xạ tại mặt vào
            "r2": r2,           # Góc tới tại mặt ra
            "theta2": theta2,   # Góc ra
            "delta": delta      # Góc lệch
        }
    
    def draw_prism(self):
        """Vẽ lăng kính tam giác đều"""
        A_rad = math.radians(self.prism_angle)
        
        # Tọa độ lăng kính (tam giác cân với đỉnh ở trên)
        height = 1.5
        base_half = height * math.tan(A_rad / 2)
        
        # 3 đỉnh lăng kính
        vertices = [
            [-base_half, 0],      # Trái dưới
            [base_half, 0],       # Phải dưới
            [0, height]           # Đỉnh trên
        ]
        
        # Vẽ lăng kính
        prism = patches.Polygon(vertices, closed=True, 
                              facecolor='lightblue', alpha=0.3,
                              edgecolor='cyan', linewidth=3)
        self.ax_main.add_patch(prism)
        
        # Vẽ viền
        vertices_closed = vertices + [vertices[0]]
        x_coords = [v[0] for v in vertices_closed]
        y_coords = [v[1] for v in vertices_closed]
        self.ax_main.plot(x_coords, y_coords, 'cyan', linewidth=3, label='Lăng kính')
        
        return vertices
    
    def draw_single_ray(self):
        """Vẽ tia sáng đơn màu"""
        result = self.calculate_prism_ray(self.slider_n2.val)
        
        if "error" in result:
            # Hiển thị lỗi
            self.ax_main.text(0, -0.5, result["error"], 
                            ha='center', fontsize=12, color='red', fontweight='bold',
                            bbox=dict(boxstyle="round", facecolor="yellow", alpha=0.8))
            return
        
        # Tính toán tọa độ các điểm
        A_rad = math.radians(self.prism_angle)
        height = 1.5
        base_half = height * math.tan(A_rad / 2)
        
        # Điểm va chạm tại mặt trái (đơn giản hóa)
        impact_x = -base_half/2
        impact_y = height * (1 - abs(impact_x)/base_half)  # Tỷ lệ với chiều cao
        
        # Điểm ra tại mặt phải
        exit_x = base_half/2
        exit_y = height * (1 - abs(exit_x)/base_half)
        
        # 1. Tia tới
        theta1_rad = math.radians(result["theta1"])
        start_x = impact_x - 2.0  # Điểm bắt đầu
        start_y = impact_y - 2.0 * math.tan(theta1_rad)  # Tính từ góc tới
        
        self.ax_main.plot([start_x, impact_x], [start_y, impact_y], 
                         'red', linewidth=3, label='Tia tới', alpha=0.9)
        
        # 2. Tia trong lăng kính
        self.ax_main.plot([impact_x, exit_x], [impact_y, exit_y], 
                         'orange', linewidth=3, label='Tia trong lăng kính', alpha=0.9)
        
        # 3. Tia ra
        theta2_rad = math.radians(result["theta2"])
        end_x = exit_x + 2.0
        end_y = exit_y + 2.0 * math.tan(theta2_rad)
        
        self.ax_main.plot([exit_x, end_x], [exit_y, end_y], 
                         'lime', linewidth=3, label='Tia ra', alpha=0.9)
        
        # Hiển thị thông tin góc
        if self.show_angles:
            # Góc tới
            self.ax_main.text(impact_x-0.3, impact_y+0.15, 
                            f'θ₁={result["theta1"]:.1f}°', 
                            color='red', fontsize=10, fontweight='bold')
            
            # Góc khúc xạ trong lăng kính
            self.ax_main.text(impact_x+0.1, impact_y-0.15, 
                            f'r₁={result["r1"]:.1f}°', 
                            color='orange', fontsize=10, fontweight='bold')
            
            # Góc tới tại mặt ra
            self.ax_main.text(exit_x-0.2, exit_y-0.15, 
                            f'r₂={result["r2"]:.1f}°', 
                            color='orange', fontsize=9, fontweight='bold')
            
            # Góc ra
            self.ax_main.text(exit_x+0.15, exit_y+0.1, 
                            f'θ₂={result["theta2"]:.1f}°', 
                            color='lime', fontsize=10, fontweight='bold')
        
        # Hiển thị góc lệch
        self.ax_main.text(1.2, -1.0, f'Góc lệch δ = {result["delta"]:.1f}°', 
                        color='yellow', fontsize=12, fontweight='bold',
                        bbox=dict(boxstyle="round", facecolor="blue", alpha=0.7))
    
    def draw_dispersed_rays(self):
        """Vẽ tia sáng tán sắc"""
        # Tia tới trắng (chung cho tất cả màu)
        basic_result = self.calculate_prism_ray(self.slider_n2.val)
        
        if "error" not in basic_result:
            # Vẽ tia tới trắng
            A_rad = math.radians(self.prism_angle)
            height = 1.5
            base_half = height * math.tan(A_rad / 2)
            
            impact_x = -base_half/2
            impact_y = height * (1 - abs(impact_x)/base_half)
            
            theta1_rad = math.radians(basic_result["theta1"])
            start_x = impact_x - 2.0
            start_y = impact_y - 2.0 * math.tan(theta1_rad)
            
            self.ax_main.plot([start_x, impact_x], [start_y, impact_y], 
                             'white', linewidth=4, label='Tia tới (trắng)', alpha=0.8)
        
        # Vẽ từng màu tán sắc
        for i, (color, n_color, wavelength) in enumerate(zip(self.colors, self.n_colors, self.wavelengths)):
            result = self.calculate_prism_ray(n_color)
            
            if "error" not in result:
                A_rad = math.radians(self.prism_angle)
                height = 1.5
                base_half = height * math.tan(A_rad / 2)
                
                impact_x = -base_half/2
                impact_y = height * (1 - abs(impact_x)/base_half)
                exit_x = base_half/2
                exit_y = height * (1 - abs(exit_x)/base_half)
                
                # Tia trong lăng kính
                self.ax_main.plot([impact_x, exit_x], [impact_y, exit_y], 
                                 color=color, linewidth=2, alpha=0.6)
                
                # Tia ra với góc khác nhau do tán sắc
                theta2_rad = math.radians(result["theta2"])
                end_x = exit_x + 2.5
                end_y = exit_y + 2.5 * math.tan(theta2_rad)
                
                self.ax_main.plot([exit_x, end_x], [exit_y, end_y], 
                                 color=color, linewidth=3, alpha=0.9,
                                 label=f'{wavelength} (δ={result["delta"]:.1f}°)')
        
        # Chú thích tán sắc
        self.ax_main.text(0, 2.2, 'TAN SAC ANH SANG', 
                        ha='center', fontsize=12, color='white', fontweight='bold',
                        bbox=dict(boxstyle="round", facecolor="purple", alpha=0.7))
    
    def draw_info_panel(self):
        """Vẽ panel thông tin bên phải"""
        self.ax_info.clear()
        self.ax_info.set_xlim(0, 1)
        self.ax_info.set_ylim(0, 1)
        self.ax_info.axis('off')
        
        # Thông số hiện tại
        info_text = f"""
THAM SO:
n1 = {self.slider_n1.val:.2f}
n2 = {self.slider_n2.val:.2f}
theta1 = {self.slider_theta.val:.1f} do
A = {self.slider_prism_angle.val:.1f} do

DINH LUAT SNELL:
n1 x sin(theta1) = n2 x sin(theta2)

TAN SAC:
Chi so khuc xa phu thuoc
buoc song anh sang
-> Tach thanh cac mau

PHAN XA TOAN PHAN:
Xay ra khi:
sin(theta) > n2/n1
        """
        
        self.ax_info.text(0.05, 0.95, info_text, transform=self.ax_info.transAxes,
                         fontsize=10, color='white', verticalalignment='top',
                         bbox=dict(boxstyle="round,pad=0.5", facecolor="navy", alpha=0.8))
    
    def update_plot(self, val=None):
        """Cập nhật toàn bộ đồ thị"""
        # Lấy giá trị từ slider để cập nhật biến trạng thái
        self.prism_angle = self.slider_prism_angle.val
        
        # Xóa và thiết lập lại axes chính
        self.ax_main.clear()
        self.ax_main.set_xlim(-3, 4)
        self.ax_main.set_ylim(-1.5, 2.5)
        self.ax_main.set_aspect('equal')
        self.ax_main.grid(True, alpha=0.3)
        self.ax_main.set_facecolor('#16213e')
        
        # Vẽ các thành phần
        self.draw_prism()
        
        if self.show_dispersion:
            self.draw_dispersed_rays()
        else:
            self.draw_single_ray()
        
        self.draw_info_panel()
        
        # Labels
        self.ax_main.set_xlabel('X (đơn vị tùy ý)', color='white')
        self.ax_main.set_ylabel('Y (đơn vị tùy ý)', color='white')
        
        # Legend
        if not self.show_dispersion:
            self.ax_main.legend(loc='upper right', framealpha=0.8, fontsize=9)
        
        plt.draw()
    
    def setup_zoom(self):
        """Thiết lập zoom và pan với chuột"""
        def zoom_factory(ax, base_scale=2.):
            def zoom_fun(event):
                if event.inaxes != ax:
                    return
                    
                cur_xlim = ax.get_xlim()
                cur_ylim = ax.get_ylim()
                
                xdata = event.xdata
                ydata = event.ydata
                
                if event.button == 'up':
                    scale_factor = 1 / base_scale
                elif event.button == 'down':
                    scale_factor = base_scale
                else:
                    return
                
                new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
                new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
                
                relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
                rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])
                
                ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
                ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
                ax.figure.canvas.draw()
            
            fig = ax.get_figure()
            fig.canvas.mpl_connect('scroll_event', zoom_fun)
            return zoom_fun
        
        def pan_factory(ax):
            """Thêm chức năng kéo để dịch chuyển mượt mà"""
            # Lưu trạng thái
            pan_factory.is_pressed = False
            pan_factory.press_data = None
            
            def on_press(event):
                if event.inaxes != ax or event.button != 1:  # Chỉ chuột trái
                    return
                    
                pan_factory.is_pressed = True
                pan_factory.press_data = {
                    'x': event.xdata,
                    'y': event.ydata,
                    'xlim': ax.get_xlim(),
                    'ylim': ax.get_ylim()
                }
                # Thay đổi cursor khi kéo
                ax.figure.canvas.get_tk_widget().configure(cursor="fleur")

            def on_motion(event):
                if not pan_factory.is_pressed or pan_factory.press_data is None:
                    return
                if event.inaxes != ax:
                    return

                # Tính độ dịch chuyển
                dx = event.xdata - pan_factory.press_data['x']
                dy = event.ydata - pan_factory.press_data['y']
                
                # Cập nhật giới hạn axes (mượt hơn)
                xlim = pan_factory.press_data['xlim']
                ylim = pan_factory.press_data['ylim']
                
                ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
                ax.set_ylim(ylim[0] - dy, ylim[1] - dy)
                
                # Sử dụng draw_idle thay vì draw để giảm lag
                ax.figure.canvas.draw_idle()

            def on_release(event):
                if pan_factory.is_pressed:
                    pan_factory.is_pressed = False
                    pan_factory.press_data = None
                    # Trở lại cursor bình thường
                    try:
                        ax.figure.canvas.get_tk_widget().configure(cursor="")
                    except:
                        pass  # Ignore nếu không phải tkinter backend
                    ax.figure.canvas.draw()

            # Kết nối events
            fig = ax.get_figure()
            fig.canvas.mpl_connect('button_press_event', on_press)
            fig.canvas.mpl_connect('motion_notify_event', on_motion)
            fig.canvas.mpl_connect('button_release_event', on_release)
            
        zoom_factory(self.ax_main)
        pan_factory(self.ax_main)
    
    def reset_values(self, event):
        """Reset về giá trị mặc định"""
        self.slider_n1.reset()
        self.slider_n2.reset()
        self.slider_theta.reset()
        self.slider_prism_angle.reset()
        self.show_dispersion = False
        self.update_plot()
    
    def toggle_dispersion(self, event):
        """Bật chế độ tán sắc"""
        self.show_dispersion = True
        self.update_plot()
    
    def set_normal_mode(self, event):
        """Bật chế độ bình thường (tia đơn màu)"""
        self.show_dispersion = False
        self.update_plot()
    
    def take_screenshot(self, event):
        """Chụp ảnh với dialog chọn vị trí lưu"""
        try:
            import tkinter as tk
            from tkinter import filedialog
            import datetime
            
            # Tạo root window và đưa lên trên cùng
            root = tk.Tk()
            root.withdraw()  # Ẩn window chính
            root.lift()      # Đưa lên trên
            root.attributes('-topmost', True)  # Luôn ở trên cùng
            
            # Tạo tên file mặc định
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"prism_simulation_{timestamp}"
            
            # Mở dialog lưu file
            filename = filedialog.asksaveasfilename(
                parent=root,
                defaultextension=".png",
                initialfile=default_name,  # Sửa từ initialfilename thành initialfile
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("SVG files", "*.svg"),
                    ("PDF files", "*.pdf"),
                    ("All files", "*.*")
                ],
                title="Chon vi tri luu anh mo phong lang kinh"
            )
            
            if filename:  # Nếu người dùng chọn vị trí lưu
                self.fig.savefig(filename, dpi=300, bbox_inches='tight', 
                                facecolor=self.fig.get_facecolor(), edgecolor='none')
                print(f"Da luu anh: {filename}")
            else:
                print("Da huy luu anh")
                
            
        except Exception as e:
            print(f"Loi dialog: {e}")
            # Fallback - lưu trực tiếp
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"prism_simulation_{timestamp}.png"
            self.fig.savefig(filename, dpi=300, bbox_inches='tight', 
                            facecolor=self.fig.get_facecolor(), edgecolor='none')
            print(f"Da luu anh: {filename} (trong thu muc hien tai)")
    
    def run(self):
        """Chạy ứng dụng"""
        plt.show()

def main():
    
    try:
        app = SimplePrismSimulator()
        app.run()
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()