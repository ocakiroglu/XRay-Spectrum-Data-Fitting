import customtkinter as ctk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import os
import tkinter as tk # Still need this for tk.StringVar, tk.TOP, etc.

# --- Gaussian Model Functions (1-10 peaks) ---

def one_gaussian_function(x, center, width, height, y0):
    return height * np.exp(-(x - center) ** 2 / (2 * width ** 2)) + y0

def two_gaussian_function(x, center1, width1, height1, center2, width2, height2, y0):
    return (height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) +
            height2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) + y0)

def three_gaussian_function(x, center1, width1, height1, center2, width2, height2, center3, width3, height3, y0):
    return (height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) +
            height2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) +
            height3 * np.exp(-(x - center3) ** 2 / (2 * width3 ** 2)) + y0)

def four_gaussian_function(x, center1, width1, height1, center2, width2, height2, center3, width3, height3, center4, width4, height4, y0):
    return (height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) +
            height2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) +
            height3 * np.exp(-(x - center3) ** 2 / (2 * width3 ** 2)) +
            height4 * np.exp(-(x - center4) ** 2 / (2 * width4 ** 2)) + y0)

def five_gaussian_function(x, center1, width1, height1, center2, width2, height2, center3, width3, height3, center4, width4, height4, center5, width5, height5, y0):
    return (height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) +
            height2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) +
            height3 * np.exp(-(x - center3) ** 2 / (2 * width3 ** 2)) +
            height4 * np.exp(-(x - center4) ** 2 / (2 * width4 ** 2)) +
            height5 * np.exp(-(x - center5) ** 2 / (2 * width5 ** 2)) + y0)

def six_gaussian_function(x, center1, width1, height1, center2, width2, height2, center3, width3, height3, center4, width4, height4, center5, width5, height5, center6, width6, height6, y0):
    return (height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) +
            height2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) +
            height3 * np.exp(-(x - center3) ** 2 / (2 * width3 ** 2)) +
            height4 * np.exp(-(x - center4) ** 2 / (2 * width4 ** 2)) +
            height5 * np.exp(-(x - center5) ** 2 / (2 * width5 ** 2)) +
            height6 * np.exp(-(x - center6) ** 2 / (2 * width6 ** 2)) + y0)

def seven_gaussian_function(x, center1, width1, height1, center2, width2, height2, center3, width3, height3, center4, width4, height4, center5, width5, height5, center6, width6, height6, center7, width7, height7, y0):
    return (height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) +
            height2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) +
            height3 * np.exp(-(x - center3) ** 2 / (2 * width3 ** 2)) +
            height4 * np.exp(-(x - center4) ** 2 / (2 * width4 ** 2)) +
            height5 * np.exp(-(x - center5) ** 2 / (2 * width5 ** 2)) +
            height6 * np.exp(-(x - center6) ** 2 / (2 * width6 ** 2)) +
            height7 * np.exp(-(x - center7) ** 2 / (2 * width7 ** 2)) + y0)

def eight_gaussian_function(x, center1, width1, height1, center2, width2, height2, center3, width3, height3, center4, width4, height4, center5, width5, height5, center6, width6, height6, center7, width7, height7, center8, width8, height8, y0):
    return (height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) +
            height2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) +
            height3 * np.exp(-(x - center3) ** 2 / (2 * width3 ** 2)) +
            height4 * np.exp(-(x - center4) ** 2 / (2 * width4 ** 2)) +
            height5 * np.exp(-(x - center5) ** 2 / (2 * width5 ** 2)) +
            height6 * np.exp(-(x - center6) ** 2 / (2 * width6 ** 2)) +
            height7 * np.exp(-(x - center7) ** 2 / (2 * width7 ** 2)) +
            height8 * np.exp(-(x - center8) ** 2 / (2 * width8 ** 2)) + y0)

def nine_gaussian_function(x, center1, width1, height1, center2, width2, height2, center3, width3, height3, center4, width4, height4, center5, width5, height5, center6, width6, height6, center7, width7, height7, center8, width8, height8, center9, width9, height9, y0):
    return (height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) +
            height2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) +
            height3 * np.exp(-(x - center3) ** 2 / (2 * width3 ** 2)) +
            height4 * np.exp(-(x - center4) ** 2 / (2 * width4 ** 2)) +
            height5 * np.exp(-(x - center5) ** 2 / (2 * width5 ** 2)) +
            height6 * np.exp(-(x - center6) ** 2 / (2 * width6 ** 2)) +
            height7 * np.exp(-(x - center7) ** 2 / (2 * width7 ** 2)) +
            height8 * np.exp(-(x - center8) ** 2 / (2 * width8 ** 2)) +
            height9 * np.exp(-(x - center9) ** 2 / (2 * width9 ** 2)) + y0)

def ten_gaussian_function(x, center1, width1, height1, center2, width2, height2, center3, width3, height3, center4, width4, height4, center5, width5, height5, center6, width6, height6, center7, width7, height7, center8, width8, height8, center9, width9, height9, center10, width10, height10, y0):
    return (height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) +
            height2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) +
            height3 * np.exp(-(x - center3) ** 2 / (2 * width3 ** 2)) +
            height4 * np.exp(-(x - center4) ** 2 / (2 * width4 ** 2)) +
            height5 * np.exp(-(x - center5) ** 2 / (2 * width5 ** 2)) +
            height6 * np.exp(-(x - center6) ** 2 / (2 * width6 ** 2)) +
            height7 * np.exp(-(x - center7) ** 2 / (2 * width7 ** 2)) +
            height8 * np.exp(-(x - center8) ** 2 / (2 * width8 ** 2)) +
            height9 * np.exp(-(x - center9) ** 2 / (2 * width9 ** 2)) +
            height10 * np.exp(-(x - center10) ** 2 / (2 * width10 ** 2)) + y0)


# Dictionary to map peak count to function
FIT_FUNCTIONS = {
    1: one_gaussian_function,
    2: two_gaussian_function,
    3: three_gaussian_function,
    4: four_gaussian_function,
    5: five_gaussian_function,
    6: six_gaussian_function,
    7: seven_gaussian_function,
    8: eight_gaussian_function,
    9: nine_gaussian_function,
    10: ten_gaussian_function,
}


# --- Main GUI Application Class ---

class GaussianFitGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XRay Spectrum Fitter (CustomTkinter)")
        self.root.geometry("1200x850")

        # --- Data variables ---
        self.filename = ""
        self.xdata_full = None
        self.ydata_full = None
        self.xdata = None
        self.ydata = None
        self.popt = None # Stores parameters from auto-fit
        self.last_line = None # Stores the composite fit line
        self.last_filled = [] # Stores the individual peak fills
        
        # --- Manual fit variables ---
        self.manual_popt = None # Stores parameters from manual sliders
        self.manual_sliders = [] # Stores slider widgets
        self.manual_fit_window = None # Reference to the popup window

        # --- Tkinter control variables (Unchanged) ---
        self.filename_var = tk.StringVar(value="No file loaded.")
        self.x_type_var = tk.StringVar(value="Wavelength")
        self.range_min_var = tk.StringVar(value="0")
        self.range_max_var = tk.StringVar(value="500")
        self.peak_label_var = tk.StringVar(value="Number of Peaks: 0")

        # --- Create main frames ---
        self.control_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=(10, 15), pady=(10, 5))

        self.plot_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.results_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.results_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(5, 0))

        self.results_frame2 = ctk.CTkFrame(self.root, fg_color="transparent")
        self.results_frame2.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 10))

        # --- Populate controls ---
        self._create_controls()

        # --- Create plot canvas ---
        self._create_plot_canvas()

    def _create_controls(self):
        # --- File Loading ---
        file_frame = ctk.CTkFrame(self.control_frame)
        file_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        ctk.CTkButton(file_frame, text="Open File", command=self.load_file).pack(side=tk.LEFT, padx=0)
        ctk.CTkLabel(file_frame, textvariable=self.filename_var, width=60).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # --- Settings ---
        settings_frame = ctk.CTkFrame(self.control_frame)
        settings_frame.pack(side=tk.LEFT, padx=0, pady=5)

        ctk.CTkLabel(settings_frame, text="X-Data Type:").pack(side=tk.LEFT, padx=(5, 5))
        ctk.CTkRadioButton(settings_frame, text="Wavelength", variable=self.x_type_var, value="Wavelength", radiobutton_width=14, radiobutton_height=14,
                            command=self.update_plot).pack(side=tk.LEFT)
        ctk.CTkRadioButton(settings_frame, text="Channel", variable=self.x_type_var, value="Channel", radiobutton_width=14, radiobutton_height=14,
                            command=self.update_plot).pack(side=tk.LEFT, padx=(0, 0))

        ctk.CTkLabel(settings_frame, text="Fit Range:").pack(side=tk.LEFT, padx=(10, 5))
        
        self.range_min_entry = ctk.CTkEntry(settings_frame, textvariable=self.range_min_var, width=100)
        self.range_min_entry.pack(side=tk.LEFT)
        self.range_min_entry.bind("<Return>", self.update_plot)
        
        ctk.CTkLabel(settings_frame, text="to").pack(side=tk.LEFT, padx=(4, 4))
        
        self.range_max_entry = ctk.CTkEntry(settings_frame, textvariable=self.range_max_var, width=100)
        self.range_max_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.range_max_entry.bind("<Return>", self.update_plot)
        
        ctk.CTkButton(settings_frame, text="Apply Range", command=self.update_plot, width=100).pack(side=tk.LEFT, padx=0)


        # --- Fit Controls & Save ---
        fit_frame1 = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        fit_frame1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        ctk.CTkLabel(fit_frame1, text="Auto Peak Height:").pack(side=tk.LEFT, padx=5)
        
        self.height_slider = ctk.CTkSlider(fit_frame1, from_=0, to=1000, orientation="horizontal", width=500, command=self.update_plot)
        self.height_slider.set(700)
        self.height_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ctk.CTkLabel(fit_frame1, textvariable=self.peak_label_var, width=110).pack(side=tk.LEFT, padx=(5, 20))

        fit_frame2 = ctk.CTkFrame(self.results_frame2, fg_color="transparent")
        fit_frame2.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5, pady=5)

        ctk.CTkButton(fit_frame2, text="Manual", command=self.manual_fit).pack(side=tk.RIGHT)
        ctk.CTkButton(fit_frame2, text="Save Results", command=self.save_fit).pack(side=tk.RIGHT, padx=5)
        ctk.CTkButton(fit_frame2, text="Show Results", command=self.show_fit_results).pack(side=tk.RIGHT, padx=5)

    def _create_plot_canvas(self):
        self.fig = Figure(figsize=(15, 6), label="Gaussian Fit on Spectrum")
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(visible=True, which='both', axis='both', linestyle='--', linewidth=0.5, alpha=0.7)
        self.ax.set_xlabel("Load data to begin", fontsize=14)
        self.ax.set_ylabel("Counts", fontsize=14)
        self.fig.subplots_adjust(left=0.055, right=0.99, top=0.96, bottom=0.09)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
        
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=0)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=0)

    def load_file(self):
        self.filename = filedialog.askopenfilename(
            title="Select a spectrum file",
            filetypes=(("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if not self.filename:
            return
        
        self.filename_var.set(os.path.basename(self.filename))

        try:
            with open(self.filename, 'r') as f:
                first_line = f.readline()
                header = first_line.strip().replace(',', '').replace(';', '').replace('\t', '').replace('  ', '')
                if any(char.isalpha() for char in header):
                    skip_header = 1
                else:
                    skip_header = 0

            last_exc = None
            for delim in [',', ';', '\t', None]:
                try:
                    data = np.loadtxt(self.filename, delimiter=delim, skiprows=skip_header, unpack=True)
                    break
                except Exception as e:
                    last_exc = e
            else:
                raise ValueError("Could not read the file with common delimiters or whitespace.") from last_exc

            if isinstance(data, np.ndarray) and data.ndim == 1:
                data = np.atleast_2d(data)

            self.x_channel_full = data[0, :]
            self.ydata_full = data[1, :]
            self.x_energy_full = data[-1, :] 

            max_y = np.max(self.ydata_full)
            self.height_slider.configure(to=max_y)
            self.height_slider.set(max_y / 10) 
            
            self.range_min_var.set(str(np.min(self.x_energy_full if self.x_type_var.get() == "Wavelength" else self.x_channel_full)))
            self.range_max_var.set(str(np.max(self.x_energy_full if self.x_type_var.get() == "Wavelength" else self.x_channel_full)))

            plt.rcParams['savefig.directory'] = os.path.dirname(self.filename)
            self.fig.set_label(f"{os.path.basename(self.filename).rsplit('.', 1)[0]}_gaussian_fit_results")

            self.update_plot() 

        except Exception as e:
            messagebox.showerror("File Load Error", f"Failed to load file: {e}")
            self.filename_var.set("Failed to load file.")

    def _assign_data(self):
        self.ydata = self.ydata_full 
        
        if self.x_type_var.get() == "Channel":
            self.xdata = self.x_channel_full
            self.ax.set_xlabel("Channel", fontsize=14)
        else:
            self.xdata = self.x_energy_full
            self.ax.set_xlabel("Wavelength (nm)", fontsize=14)

    def get_peaks(self, y_data, height, distance=50):
        peak_indices, _ = find_peaks(y_data, height=height, distance=distance)
        
        num_peaks = len(peak_indices)
        if num_peaks == 0:
            self.peak_label_var.set(f'Number of Peaks: {num_peaks}')
            return None

        self.peak_label_var.set(f'Number of Peaks: {num_peaks}')
        return peak_indices

    def _plot_fit_on_ax(self, x_data, popt):
        if self.last_line:
            for line in self.last_line:
                line.remove()
        for fill in self.last_filled:
            fill.remove()
        
        self.last_line = None
        self.last_filled = []

        try:
            num_peaks = (len(popt) - 1) // 3
            if num_peaks not in FIT_FUNCTIONS:
                print(f"Cannot plot fit for {num_peaks} peaks.")
                return

            fit_func = FIT_FUNCTIONS[num_peaks]
            fit_y = fit_func(x_data, *popt)
            
            line = self.ax.plot(x_data, fit_y, label='Composite Fit', color='darkred', alpha=0.7)
            self.last_line = line 
            
            baseline = popt[-1]
            colors = ['red', 'orange', 'yellow', 'green', 'blue', 
                      'purple', 'cyan', 'magenta', 'lime', 'brown']
            
            peak_params_list = []
            for i in range(num_peaks):
                peak_params_list.append({
                    'center': popt[i*3],
                    'width': popt[i*3 + 1],
                    'height': popt[i*3 + 2],
                    'color': colors[i % len(colors)],
                    'label': f'Peak {i+1}'
                })

            sorted_peaks = sorted(peak_params_list, key=lambda p: p['height'], reverse=True)

            for peak in sorted_peaks:
                gaussian_i = one_gaussian_function(x_data, 
                                                   peak['center'], 
                                                   peak['width'], 
                                                   peak['height'], 
                                                   baseline)
                filled = self.ax.fill_between(x_data, 
                                              gaussian_i, 
                                              baseline, 
                                              where=(gaussian_i > baseline), 
                                              color=peak['color'], 
                                              alpha=0.3, 
                                              label=peak['label'])
                self.last_filled.append(filled)
        
        except Exception as e:
            print(f"Error during manual plot: {e}")
            pass

    def set_gaussian_fit(self, x_short_data, y_short_data, peak_indices):
        self.popt = None 
        
        num_peaks = len(peak_indices)
        fit_func = FIT_FUNCTIONS.get(num_peaks)

        if fit_func is None:
            self.ax.set_title("Auto Gaussian Fit supports up to 10 peaks only.", fontsize=12, color='red')
            self._plot_fit_on_ax(x_short_data, np.array([])) 
            return

        initial_guess = []
        for i in peak_indices:
            initial_guess.extend([x_short_data[i], 10, y_short_data[i]])
        initial_guess.append(np.min(y_short_data)) # y0

        try:
            self.popt, _ = curve_fit(fit_func, x_short_data, y_short_data, p0=initial_guess, bounds=(0, np.inf), maxfev=10000)
            self._plot_fit_on_ax(x_short_data, self.popt)
            self.ax.set_title("") 
        except RuntimeError:
            self.ax.set_title(f"Gaussian fit failed for {num_peaks} peaks.", fontsize=12, color='red')
            self.popt = None
            self._plot_fit_on_ax(x_short_data, np.array([]))
            
    def update_plot(self, event=None):
        if self.ydata_full is None:
            return

        if self.manual_fit_window:
            self.manual_fit_window.destroy()
            self.manual_fit_window = None

        try:
            xmin = float(self.range_min_var.get())
            xmax = float(self.range_max_var.get())
            height = self.height_slider.get()
        except ValueError:
            messagebox.showerror("Input Error", "Fit range values must be numbers.")
            return

        self.ax.clear() 
        self.last_line = None
        self.last_filled = []
        self._assign_data()

        self.ax.plot(self.xdata, self.ydata, label='Spectrum', color='darkblue', linestyle='', marker='.', markersize=5)

        indices = np.where((self.xdata >= xmin) & (self.xdata <= xmax))
        x_short_data = self.xdata[indices]
        y_short_data = self.ydata[indices]
        
        if len(x_short_data) == 0:
            self.ax.set_title("No data in the specified fit range.", fontsize=12, color='red')
            self.canvas.draw()
            return

        peak_indices = self.get_peaks(y_short_data, height=height, distance=50)
        
        if peak_indices is not None:
            max_peak_index_in_short = peak_indices[np.argmax(y_short_data[peak_indices])]
            peak_x = x_short_data[max_peak_index_in_short]
            peak_y = y_short_data[max_peak_index_in_short]
            
            label = f'Peak at x={peak_x:.2f}'
            self.ax.axvline(x=peak_x, color="gray", linestyle='--', alpha=0.7, label=label)
            self.ax.annotate(label, xy=(peak_x, peak_y), 
                             xytext=(peak_x + (xmax - xmin) * 0.05, peak_y),
                             fontsize=10, color='black')
            
            self.set_gaussian_fit(x_short_data, y_short_data, peak_indices)
        else:
            self.popt = None
            self._plot_fit_on_ax(x_short_data, np.array([]))

        
        self.ax.set_ylabel("Counts", fontsize=14)
        self.ax.set_xlim([np.min(self.xdata), np.max(self.xdata)])
        self.ax.set_ylim([self.ax.get_ylim()[0], np.max(self.ydata)*1.1])
        self.ax.grid(visible=True, which='both', axis='both', linestyle='--', linewidth=0.5, alpha=0.7)
        self.ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, labelsize=12)
        self.ax.legend()
        self.canvas.draw()

    def _generate_fit_results_string(self):
        popt_to_show = self.manual_popt if self.manual_popt is not None else self.popt
        
        if popt_to_show is None:
            return None

        num_peaks = (len(popt_to_show) - 1) // 3
        if num_peaks == 0:
            return "No fit parameters available."
            
        results_lines = []
        results_lines.append(f'Source File: {self.filename}\n')
        if self.manual_popt is not None:
             results_lines.append(f'Fit Type: MANUAL\n')
        else:
             results_lines.append(f'Fit Type: AUTO\n')
        results_lines.append(f'Number of Peaks Fitted: {num_peaks}\n')

        # (Blocks for 1-5 peaks are unchanged)
        if num_peaks == 1:
            results_lines.append('Fitting Function: One Gaussian\n\n')
            results_lines.append('Parameters: center, width, height, baseline (y0)\n')
            results_lines.append("Gaussian Fit Formula y(x) = height * np.exp(-(x - center) ** 2 / (2 * width ** 2)) + y0\n\n")
        elif num_peaks == 2:
            results_lines.append('Fitting Function: Two Gaussians\n\n')
            results_lines.append('Parameters:\t center1, width1, height1, \n'
                                 '\t\t center2, width2, height2, \n'
                                 '\t\t baseline (y0)\n')
            results_lines.append("Gaussian Fit Formula \t y(x) = height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) + \n"
                                 "\t\t\t\theight2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) + y0\n\n")
        elif num_peaks == 3:
            results_lines.append('Fitting Function: Three Gaussians\n\n')
            results_lines.append('Parameters:\t center1, width1, height1, \n'
                                 '\t\t center2, width2, height2, \n'
                                 '\t\t center3, width3, height3, \n'
                                 '\t\t baseline (y0)\n')
            results_lines.append("Gaussian Fit Formula \t y(x) = height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) + \n"
                                 "\t\t\t\theight2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) + \n"
                                 "\t\t\t\theight3 * np.exp(-(x - center3) ** 2 / (2 * width3 ** 2)) + y0\n\n")
        elif num_peaks == 4:
            results_lines.append('Fitting Function: Four Gaussians\n\n')
            results_lines.append('Parameters:\t center1, width1, height1, \n'
                                 '\t\t center2, width2, height2, \n'
                                 '\t\t center3, width3, height3, \n'
                                 '\t\t center4, width4, height4, \n'
                                 '\t\t baseline (y0)\n')
            results_lines.append("Gaussian Fit Formula \t y(x) = height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) + \n"
                                 "\t\t\t\theight2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) + \n"
                                 "\t\t\t\theight3 * np.exp(-(x - center3) ** 2 / (2 * width3 ** 2)) + \n"
                                 "\t\t\t\theight4 * np.exp(-(x - center4) ** 2 / (2 * width4 ** 2)) + y0\n\n")
        elif num_peaks == 5:
            results_lines.append('Fitting Function: Five Gaussians\n\n')
            results_lines.append('Parameters:\t center1, width1, height1, \n'
                                 '\t\t center2, width2, height2, \n'
                                 '\t\t center3, width3, height3, \n'
                                 '\t\t center4, width4, height4, \n'
                                 '\t\t center5, width5, height5, \n'
                                 '\t\t baseline (y0)\n')
            results_lines.append("Gaussian Fit Formula \t y(x) = height1 * np.exp(-(x - center1) ** 2 / (2 * width1 ** 2)) + \n"
                                 "\t\t\t\theight2 * np.exp(-(x - center2) ** 2 / (2 * width2 ** 2)) + \n"
                                 "\t\t\t\theight3 * np.exp(-(x - center3) ** 2 / (2 * width3 ** 2)) + \n"
                                 "\t\t\t\theight4 * np.exp(-(x - center4) ** 2 / (2 * width4 ** 2)) + \n"
                                 "\t\t\t\theight5 * np.exp(-(x - center5) ** 2 / (2 * width5 ** 2)) + y0\n\n")

        # (Blocks for 6-10 peaks are unchanged)
        elif num_peaks == 6:
            results_lines.append('Fitting Function: Six Gaussians\n\n')
            results_lines.append('Parameters:\t center1, width1, height1, \n'
                                 '\t\t center2, width2, height2, \n'
                                 '\t\t center3, width3, height3, \n'
                                 '\t\t center4, width4, height4, \n'
                                 '\t\t center5, width5, height5, \n'
                                 '\t\t center6, width6, height6, \n'
                                 '\t\t baseline (y0)\n')
            results_lines.append("Gaussian Fit Formula \t y(x) = ... (6 terms) ... + y0\n\n") 
        elif num_peaks == 7:
            results_lines.append('Fitting Function: Seven Gaussians\n\n')
            results_lines.append('Parameters:\t ... (all 7 peaks) ... \n'
                                 '\t\t baseline (y0)\n')
            results_lines.append("Gaussian Fit Formula \t y(x) = ... (7 terms) ... + y0\n\n")
        elif num_peaks == 8:
            results_lines.append('Fitting Function: Eight Gaussians\n\n')
            results_lines.append('Parameters:\t ... (all 8 peaks) ... \n'
                                 '\t\t baseline (y0)\n')
            results_lines.append("Gaussian Fit Formula \t y(x) = ... (8 terms) ... + y0\n\n")
        elif num_peaks == 9:
            results_lines.append('Fitting Function: Nine Gaussians\n\n')
            results_lines.append('Parameters:\t ... (all 9 peaks) ... \n'
                                 '\t\t baseline (y0)\n')
            results_lines.append("Gaussian Fit Formula \t y(x) = ... (9 terms) ... + y0\n\n")
        elif num_peaks == 10:
            results_lines.append('Fitting Function: Ten Gaussians\n\n')
            results_lines.append('Parameters:\t ... (all 10 peaks) ... \n'
                                 '\t\t baseline (y0)\n')
            results_lines.append("Gaussian Fit Formula \t y(x) = ... (10 terms) ... + y0\n\n")
        
        results_lines.append("--- Fit Results ---\n")
        for i in range(num_peaks):
            gaussian_fit_text = (f'Peak {i+1}: Center = {popt_to_show[i*3]:.4f}, Width = {popt_to_show[i*3+1]:.4f}, ')
            results_lines.append(gaussian_fit_text + f'Height = {popt_to_show[i*3+2]:.4f}\n')
        results_lines.append(f'Baseline (y0) = {popt_to_show[-1]:.4f}\n')
        
        return "".join(results_lines)


    def show_fit_results(self, event=None):
        results_text = self._generate_fit_results_string()
        
        if results_text is None:
            messagebox.showwarning("Show Results Error", "No fit parameters to show. Please perform a fit first.")
            return

        popup = ctk.CTkToplevel(self.root)
        popup.title("Fit Results")
        
        popup_width = 850
        popup_height = 650
        main_window_x = self.root.winfo_x()
        main_window_y = self.root.winfo_y()
        main_window_width = self.root.winfo_width()
        main_window_height = self.root.winfo_height()
        popup_x = main_window_x + (main_window_width // 2) - (popup_width // 2)
        popup_y = main_window_y + (main_window_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")
        
        popup.transient(self.root)
        popup.grab_set()

        text_frame = ctk.CTkFrame(popup)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        text_widget = ctk.CTkTextbox(text_frame, wrap="word", font=("Courier", 11))
        text_widget.pack(fill=tk.BOTH, expand=True)

        text_widget.insert("1.0", results_text)
        text_widget.configure(state="disabled")

        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 10))
        
        ctk.CTkButton(button_frame, text="Close", command=popup.destroy).pack()

        self.root.wait_window(popup)


    def save_fit(self, event=None):
        if self.popt is None and self.manual_popt is None:
            messagebox.showwarning("Save Error", "No fit parameters to save. Please perform a fit first.")
            return
            
        if not self.filename:
            messagebox.showwarning("Save Error", "Please load a file first.")
            return

        try:
            default_name = os.path.basename(self.filename.rsplit('.', 1)[0] + '_gaussian_fit_results.txt')
            initial_dir = os.path.dirname(self.filename)

            filename_save = filedialog.asksaveasfilename(
                initialfile=default_name,
                initialdir=initial_dir,
                title="Save Fit Results",
                defaultextension=".txt",
                filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
            )

            if not filename_save:
                return

            results_to_save = self._generate_fit_results_string()
            
            with open(filename_save, 'w') as f:
                f.write(results_to_save)
            
            messagebox.showinfo("Save Success", f"Fit results saved to:\n{filename_save}")
        
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file: {e}")

    def manual_fit(self):
        if self.popt is None:
            messagebox.showwarning("Manual Fit Error", "Please run an automatic fit first to get initial parameters.")
            return
            
        if self.manual_fit_window and self.manual_fit_window.winfo_exists():
            self.manual_fit_window.lift()
            return

        self.manual_popt = np.copy(self.popt)
        self.manual_sliders = []
        num_peaks = (len(self.manual_popt) - 1) // 3

        try:
            xmin = float(self.range_min_var.get())
            xmax = float(self.range_max_var.get())
            ymin = 0
            ymax = np.max(self.ydata_full) * 1.1
            y_avg = np.mean(self.ydata_full)
        except Exception:
            messagebox.showerror("Error", "Could not read data ranges.")
            return

        self.manual_fit_window = ctk.CTkToplevel(self.root)
        self.manual_fit_window.title("Manual Fit Control")
        self.manual_fit_window.geometry("500x700")
        
        self.manual_fit_window.protocol("WM_DELETE_WINDOW", self._on_manual_window_close)

        scroll_frame = ctk.CTkScrollableFrame(self.manual_fit_window, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        param_names = ["Center", "Width", "Height"]

        for i in range(num_peaks):
            ctk.CTkLabel(scroll_frame, text=f"--- Peak {i+1} ---", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 2), fill="x")
            
            ranges = [
                (xmin, xmax),                   # Center
                (0, (xmax - xmin) / 2),         # Width
                (ymin, ymax)                    # Height
            ]

            frame = ctk.CTkFrame(scroll_frame)
            frame.pack(fill="x", pady=0)
            for j in range(3): # Center, Width, Height
                param_index = i * 3 + j
                param_name = param_names[j]

                frame_sub = ctk.CTkFrame(frame, fg_color="transparent")
                frame_sub.pack(fill="x", pady=(5, 5))
                label = ctk.CTkLabel(frame_sub, text=f"{param_name}: {self.manual_popt[param_index]:.2f}", width=120)
                label.pack(side="left", padx=5)

                slider = ctk.CTkSlider(frame_sub,
                                       from_=ranges[j][0],
                                       to=ranges[j][1],
                                       command=self._on_manual_slider_change)
                slider.set(self.manual_popt[param_index])
                slider.pack(side="left", fill="x", expand=True, padx=5)
                
                self.manual_sliders.append((slider, label, param_name, param_index))

        ctk.CTkLabel(scroll_frame, text="--- Baseline ---", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 2), fill="x")
        param_index = -1
        param_name = "Baseline (y0)"
        
        frame = ctk.CTkFrame(scroll_frame)
        frame.pack(fill="x", pady=2)
        
        label = ctk.CTkLabel(frame, text=f"{param_name}: {self.manual_popt[param_index]:.2f}", width=120)
        label.pack(side="left", padx=5)
        
        slider = ctk.CTkSlider(frame, 
                               from_=ymin, 
                               to=y_avg, 
                               command=self._on_manual_slider_change)
        slider.set(self.manual_popt[param_index])
        slider.pack(side="left", fill="x", expand=True, padx=5)
        
        self.manual_sliders.append((slider, label, param_name, param_index))
        
        # --- MODIFIED: Added Reset Button ---
        ctk.CTkButton(self.manual_fit_window, 
                      text="Reset to Auto-Fit", 
                      command=self._reset_manual_fit,
                      fg_color="red", hover_color="#C00000").pack(pady=(10, 5), padx=10, fill="x")

        # Modified pady to (5, 10)
        ctk.CTkButton(self.manual_fit_window, 
                      text="Set as Final Fit (for Saving)", 
                      command=self._commit_manual_fit).pack(pady=(5, 10), padx=10, fill="x")

    # --- ADDED: New method to reset sliders ---
    def _reset_manual_fit(self):
        """
        Resets the manual_popt and sliders back to the
        original auto-fit (self.popt) values.
        """
        if self.popt is None or not self.manual_sliders:
            return
            
        # 1. Reset the manual parameters array
        self.manual_popt = np.copy(self.popt)
        
        # 2. Update all sliders and labels
        for slider, label, name, index in self.manual_sliders:
            val = self.manual_popt[index]
            slider.set(val)
            label.configure(text=f"{name}: {val:.2f}")
            
        # 3. Redraw the plot with the reset parameters
        self._update_plot_manual()


    def _on_manual_window_close(self):
        if self.manual_fit_window:
            self.manual_fit_window.destroy()
        self.manual_fit_window = None
        
        # Commit changes on close
        if self.manual_popt is not None:
            self.popt = np.copy(self.manual_popt)


    def _on_manual_slider_change(self, slider_value):
        if self.manual_popt is None:
            return

        for slider, label, name, index in self.manual_sliders:
            val = slider.get()
            self.manual_popt[index] = val
            label.configure(text=f"{name}: {val:.2f}")

        self._update_plot_manual()

    def _update_plot_manual(self):
        if self.manual_popt is None or self.xdata is None:
            return
            
        try:
            xmin = float(self.range_min_var.get())
            xmax = float(self.range_max_var.get())
        except ValueError:
            return 

        indices = np.where((self.xdata >= xmin) & (self.xdata <= xmax))
        x_short_data = self.xdata[indices]
        
        if len(x_short_data) == 0:
            return

        self._plot_fit_on_ax(x_short_data, self.manual_popt)
        
        self.ax.legend()
        self.canvas.draw()
        
    def _commit_manual_fit(self):
        if self.manual_popt is not None:
            self.popt = np.copy(self.manual_popt)
            messagebox.showinfo("Fit Saved", "Manual fit parameters are now set as the final fit. 'Save Results' will save these values.", 
                                parent=self.manual_fit_window)


# --- Run the application ---
if __name__ == "__main__":
    ctk.set_appearance_mode("System") 
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    app = GaussianFitGUI(root)
    root.mainloop()