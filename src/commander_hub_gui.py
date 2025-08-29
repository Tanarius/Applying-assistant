#!/usr/bin/env python3
"""
AI Job Hunt Commander Hub GUI - Integrated Automation Dashboard
=============================================================

Centralized GUI for complete job search automation ecosystem.
Integrates with all automation bots and provides real-time monitoring.

Author: Trey (Infrastructure Engineer → AI/Automation Specialist)
Phase: Layer 2 - Integrated Commander Architecture
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
import sys
import subprocess
import logging

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from commander_hub import CommanderHub
from progress_tracker import ProgressTracker, ProgressStage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommanderHubGUI:
    """
    Centralized GUI for AI Job Hunt Commander Hub
    
    Features:
    - Real-time automation monitoring
    - Ecosystem integration dashboard  
    - One-click automation controls
    - Performance metrics and analytics
    - Bot coordination interface
    """
    
    def __init__(self, root):
        self.root = root
        self.base_path = Path(__file__).parent.parent
        
        # Commander Hub core
        self.commander = CommanderHub()
        self.automation_running = False
        self.status_thread = None
        
        # UI State
        self.colors = self._get_color_scheme()
        self.status_vars = {}
        
        self.setup_window()
        self.create_interface()
        self.start_status_monitoring()
        
        logger.info("🚀 Commander Hub GUI initialized")
    
    def _get_color_scheme(self):
        """GitHub Dark theme color scheme for ecosystem consistency"""
        return {
            'bg_primary': '#0d1117',
            'bg_secondary': '#161b22', 
            'bg_tertiary': '#21262d',
            'purple_primary': '#8b5cf6',
            'purple_hover': '#7c3aed',
            'text_primary': '#c9d1d9',
            'text_secondary': '#8b949e',
            'text_tertiary': '#6e7681',
            'success': '#3fb950',
            'error': '#f85149',
            'border': '#30363d'
        }
    
    def setup_window(self):
        """Configure main window with professional styling"""
        self.root.title("🚀 AI Job Hunt Commander Hub - Integrated Automation Dashboard")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        self.root.configure(bg=self.colors['bg_primary'])
        self.root.resizable(True, True)
        
        # Center window
        self.center_window()
        
        # Apply dark title bar (Windows)
        self.root.after(100, self.apply_dark_title_bar)
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def apply_dark_title_bar(self):
        """Apply dark title bar styling (Windows)"""
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int))
        except:
            pass
    
    def create_interface(self):
        """Create main interface with tabs and sections"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_frame)
        
        # Tabbed interface
        self.create_tabbed_interface(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create header with title and quick stats"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = tk.Label(header_frame,
                              text="🚀 AI Job Hunt Commander Hub",
                              font=('Segoe UI', 24, 'bold'),
                              bg=self.colors['bg_primary'],
                              fg=self.colors['text_primary'])
        title_label.pack(side=tk.LEFT)
        
        # Quick stats panel
        stats_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        stats_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        self.create_quick_stats(stats_frame)
    
    def create_quick_stats(self, parent):
        """Create quick statistics display"""
        stats_title = tk.Label(parent,
                              text="📊 Today's Performance",
                              font=('Segoe UI', 12, 'bold'),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_primary'])
        stats_title.pack(padx=15, pady=(10, 5))
        
        # Stats variables
        self.status_vars['jobs_discovered'] = tk.StringVar(value="Jobs Discovered: 0")
        self.status_vars['apps_generated'] = tk.StringVar(value="Applications: 0")
        self.status_vars['quality_avg'] = tk.StringVar(value="Avg Quality: 0.0/10")
        self.status_vars['success_rate'] = tk.StringVar(value="Success Rate: 0%")
        
        # Stats labels
        for var_name, var in self.status_vars.items():
            label = tk.Label(parent,
                           textvariable=var,
                           font=('Segoe UI', 10),
                           bg=self.colors['bg_secondary'],
                           fg=self.colors['text_secondary'])
            label.pack(padx=15, pady=2)
        
        # Last update time
        self.status_vars['last_update'] = tk.StringVar(value="Updated: Never")
        update_label = tk.Label(parent,
                               textvariable=self.status_vars['last_update'],
                               font=('Segoe UI', 9),
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_tertiary'])
        update_label.pack(padx=15, pady=(2, 10))
    
    def create_tabbed_interface(self, parent):
        """Create tabbed interface for different functions"""
        # Create notebook
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure tab styles for dark theme
        style.configure('TNotebook', background=self.colors['bg_primary'])
        style.configure('TNotebook.Tab', 
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_secondary'],
                       padding=[15, 8])
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['bg_secondary'])],
                 foreground=[('selected', self.colors['text_primary'])])
        
        self.notebook = ttk.Notebook(parent, style='TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create tabs
        self.create_automation_tab()
        self.create_discovery_tab() 
        self.create_applications_tab()
        self.create_ecosystem_tab()
        self.create_analytics_tab()
    
    def create_automation_tab(self):
        """Main automation control tab"""
        automation_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(automation_frame, text="🤖 Automation Control")
        
        # Control panel
        control_panel = tk.LabelFrame(automation_frame,
                                     text="🎮 Commander Controls",
                                     font=('Segoe UI', 14, 'bold'),
                                     bg=self.colors['bg_secondary'],
                                     fg=self.colors['text_primary'],
                                     bd=1, relief='solid')
        control_panel.pack(fill=tk.X, padx=20, pady=20)
        
        # Automation status
        self.automation_status_var = tk.StringVar(value="🔴 Automation Stopped")
        status_label = tk.Label(control_panel,
                               textvariable=self.automation_status_var,
                               font=('Segoe UI', 16, 'bold'),
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['error'])
        status_label.pack(pady=20)
        
        # Control buttons
        button_frame = tk.Frame(control_panel, bg=self.colors['bg_secondary'])
        button_frame.pack(pady=(0, 20))
        
        # Start/Stop automation
        self.automation_button = tk.Button(button_frame,
                                          text="▶️ Start Automation",
                                          font=('Segoe UI', 12, 'bold'),
                                          bg=self.colors['purple_primary'],
                                          fg='white',
                                          activebackground=self.colors['purple_hover'],
                                          relief='flat',
                                          bd=0,
                                          padx=30,
                                          pady=15,
                                          cursor='hand2',
                                          command=self.toggle_automation)
        self.automation_button.pack(side=tk.LEFT, padx=10)
        
        # Single cycle button
        single_cycle_btn = tk.Button(button_frame,
                                    text="🔄 Run Single Cycle",
                                    font=('Segoe UI', 11),
                                    bg=self.colors['bg_tertiary'],
                                    fg=self.colors['text_primary'],
                                    activebackground=self.colors['border'],
                                    relief='flat',
                                    bd=0,
                                    padx=20,
                                    pady=10,
                                    cursor='hand2',
                                    command=self.run_single_cycle)
        single_cycle_btn.pack(side=tk.LEFT, padx=10)
        
        # Configuration button
        config_btn = tk.Button(button_frame,
                              text="⚙️ Configuration",
                              font=('Segoe UI', 11),
                              bg=self.colors['bg_tertiary'],
                              fg=self.colors['text_primary'],
                              activebackground=self.colors['border'],
                              relief='flat',
                              bd=0,
                              padx=20,
                              pady=10,
                              cursor='hand2',
                              command=self.open_configuration)
        config_btn.pack(side=tk.LEFT, padx=10)
        
        # Live activity log
        log_frame = tk.LabelFrame(automation_frame,
                                 text="📋 Live Activity Log",
                                 font=('Segoe UI', 12, 'bold'),
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['text_primary'],
                                 bd=1, relief='solid')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Activity log text area
        self.activity_log = scrolledtext.ScrolledText(log_frame,
                                                     wrap=tk.WORD,
                                                     font=('Consolas', 10),
                                                     bg=self.colors['bg_tertiary'],
                                                     fg=self.colors['text_secondary'],
                                                     insertbackground=self.colors['text_primary'],
                                                     selectbackground=self.colors['purple_primary'])
        self.activity_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add initial log entry
        self.log_activity("🚀 Commander Hub GUI started - Ready for automation")
    
    def create_discovery_tab(self):
        """Job discovery monitoring tab"""
        discovery_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(discovery_frame, text="🔍 Job Discovery")
        
        # Discovery stats
        stats_frame = tk.LabelFrame(discovery_frame,
                                   text="📊 Discovery Statistics",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_primary'],
                                   bd=1, relief='solid')
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # TODO: Implement discovery statistics display
        placeholder_label = tk.Label(stats_frame,
                                    text="🚧 Discovery monitoring coming soon...",
                                    font=('Segoe UI', 14),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_secondary'])
        placeholder_label.pack(pady=40)
    
    def create_applications_tab(self):
        """Application management tab"""
        apps_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(apps_frame, text="📝 Applications")
        
        # Applications list
        apps_list_frame = tk.LabelFrame(apps_frame,
                                       text="📋 Recent Applications",
                                       font=('Segoe UI', 12, 'bold'),
                                       bg=self.colors['bg_secondary'],
                                       fg=self.colors['text_primary'],
                                       bd=1, relief='solid')
        apps_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # TODO: Implement applications list
        placeholder_label = tk.Label(apps_list_frame,
                                    text="📋 Application tracking system coming soon...",
                                    font=('Segoe UI', 14),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_secondary'])
        placeholder_label.pack(pady=40)
    
    def create_ecosystem_tab(self):
        """Ecosystem integration tab"""
        ecosystem_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(ecosystem_frame, text="🔗 Ecosystem")
        
        # Bot integration status
        bots_frame = tk.LabelFrame(ecosystem_frame,
                                  text="🤖 Connected Automation Bots",
                                  font=('Segoe UI', 12, 'bold'),
                                  bg=self.colors['bg_secondary'],
                                  fg=self.colors['text_primary'],
                                  bd=1, relief='solid')
        bots_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.create_bot_status_display(bots_frame)
        
        # Quick launch section
        launch_frame = tk.LabelFrame(ecosystem_frame,
                                    text="🚀 Quick Launch",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_primary'],
                                    bd=1, relief='solid')
        launch_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.create_quick_launch_buttons(launch_frame)
    
    def create_bot_status_display(self, parent):
        """Create bot connection status display"""
        bots_info = [
            ("🎯 Master Dashboard", "Connected", self.colors['success']),
            ("📝 GitHub Dev Logger", "Available", self.colors['text_secondary']),
            ("🎓 Learning Assistant", "Available", self.colors['text_secondary']),
            ("💼 Job Bot Classic", "Available", self.colors['text_secondary']),
            ("🔍 Discovery Engine", "Integrated", self.colors['success'])
        ]
        
        for i, (bot_name, status, color) in enumerate(bots_info):
            bot_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
            bot_frame.pack(fill=tk.X, padx=15, pady=5)
            
            name_label = tk.Label(bot_frame,
                                 text=bot_name,
                                 font=('Segoe UI', 11),
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['text_primary'])
            name_label.pack(side=tk.LEFT)
            
            status_label = tk.Label(bot_frame,
                                   text=f"● {status}",
                                   font=('Segoe UI', 10),
                                   bg=self.colors['bg_secondary'],
                                   fg=color)
            status_label.pack(side=tk.RIGHT)
    
    def create_quick_launch_buttons(self, parent):
        """Create quick launch buttons for other bots"""
        button_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Master Dashboard
        dashboard_btn = tk.Button(button_frame,
                                 text="🎯 Master Dashboard",
                                 font=('Segoe UI', 10),
                                 bg=self.colors['bg_tertiary'],
                                 fg=self.colors['text_primary'],
                                 activebackground=self.colors['border'],
                                 relief='flat',
                                 bd=0,
                                 padx=15,
                                 pady=8,
                                 cursor='hand2',
                                 command=self.launch_master_dashboard)
        dashboard_btn.pack(side=tk.LEFT, padx=5)
        
        # GitHub Dev Logger
        github_btn = tk.Button(button_frame,
                              text="📝 GitHub Logger",
                              font=('Segoe UI', 10),
                              bg=self.colors['bg_tertiary'],
                              fg=self.colors['text_primary'],
                              activebackground=self.colors['border'],
                              relief='flat',
                              bd=0,
                              padx=15,
                              pady=8,
                              cursor='hand2',
                              command=self.launch_github_logger)
        github_btn.pack(side=tk.LEFT, padx=5)
        
        # Learning Assistant
        learning_btn = tk.Button(button_frame,
                                text="🎓 Learning Assistant",
                                font=('Segoe UI', 10),
                                bg=self.colors['bg_tertiary'],
                                fg=self.colors['text_primary'],
                                activebackground=self.colors['border'],
                                relief='flat',
                                bd=0,
                                padx=15,
                                pady=8,
                                cursor='hand2',
                                command=self.launch_learning_assistant)
        learning_btn.pack(side=tk.LEFT, padx=5)
    
    def create_analytics_tab(self):
        """Analytics and metrics tab"""
        analytics_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(analytics_frame, text="📊 Analytics")
        
        # Performance metrics
        metrics_frame = tk.LabelFrame(analytics_frame,
                                     text="📈 Performance Metrics",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg=self.colors['bg_secondary'],
                                     fg=self.colors['text_primary'],
                                     bd=1, relief='solid')
        metrics_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # TODO: Implement analytics dashboard
        placeholder_label = tk.Label(metrics_frame,
                                    text="📊 Advanced analytics dashboard coming soon...",
                                    font=('Segoe UI', 14),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_secondary'])
        placeholder_label.pack(pady=40)
    
    def create_status_bar(self, parent):
        """Create status bar at bottom"""
        status_frame = tk.Frame(parent, 
                               bg=self.colors['bg_secondary'],
                               relief='solid',
                               bd=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # System status
        self.system_status_var = tk.StringVar(value="System: Ready")
        system_label = tk.Label(status_frame,
                               textvariable=self.system_status_var,
                               font=('Segoe UI', 9),
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_secondary'])
        system_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Connection status
        self.connection_status_var = tk.StringVar(value="API: Connected")
        connection_label = tk.Label(status_frame,
                                   textvariable=self.connection_status_var,
                                   font=('Segoe UI', 9),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['success'])
        connection_label.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def log_activity(self, message):
        """Add message to activity log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.activity_log.insert(tk.END, log_entry)
        self.activity_log.see(tk.END)
        
        # Limit log size
        line_count = int(self.activity_log.index('end-1c').split('.')[0])
        if line_count > 1000:
            self.activity_log.delete(1.0, "100.0")
    
    def toggle_automation(self):
        """Toggle automation on/off"""
        if not self.automation_running:
            self.start_automation()
        else:
            self.stop_automation()
    
    def start_automation(self):
        """Start continuous automation"""
        if self.automation_running:
            return
        
        self.automation_running = True
        self.automation_status_var.set("🟢 Automation Running")
        self.automation_button.config(text="⏸️ Stop Automation")
        
        self.log_activity("🚀 Starting continuous automation...")
        
        # Start automation in background thread
        def run_automation():
            try:
                asyncio.run(self.commander.start_continuous_automation())
            except Exception as e:
                self.log_activity(f"❌ Automation error: {e}")
                self.root.after(0, self.stop_automation)
        
        automation_thread = threading.Thread(target=run_automation, daemon=True)
        automation_thread.start()
        
        self.log_activity("✅ Continuous automation started successfully")
    
    def stop_automation(self):
        """Stop automation"""
        self.automation_running = False
        self.commander.is_running = False
        
        self.automation_status_var.set("🔴 Automation Stopped")
        self.automation_button.config(text="▶️ Start Automation")
        
        self.log_activity("⏹️ Automation stopped")
    
    def run_single_cycle(self):
        """Run a single automation cycle"""
        self.log_activity("🔄 Running single automation cycle...")
        
        # TODO: Implement single cycle
        def single_cycle():
            try:
                # Placeholder for single cycle implementation
                time.sleep(2)
                self.root.after(0, lambda: self.log_activity("✅ Single cycle completed"))
            except Exception as e:
                self.root.after(0, lambda: self.log_activity(f"❌ Single cycle error: {e}"))
        
        thread = threading.Thread(target=single_cycle, daemon=True)
        thread.start()
    
    def open_configuration(self):
        """Open configuration dialog"""
        messagebox.showinfo("Configuration", "Configuration panel coming soon!\n\nFor now, edit commander_config.json directly.")
    
    def start_status_monitoring(self):
        """Start background status monitoring"""
        def monitor_status():
            try:
                # Get commander status
                status = asyncio.run(self.commander.get_commander_status())
                
                # Update UI on main thread
                self.root.after(0, lambda: self.update_status_display(status))
            except Exception as e:
                logger.error(f"Status monitoring error: {e}")
        
        def status_loop():
            while True:
                monitor_status()
                time.sleep(30)  # Update every 30 seconds
        
        self.status_thread = threading.Thread(target=status_loop, daemon=True)
        self.status_thread.start()
    
    def update_status_display(self, status):
        """Update status display with latest data"""
        daily_stats = status.get('daily_stats', {})
        
        self.status_vars['jobs_discovered'].set(f"Jobs Discovered: {daily_stats.get('jobs_discovered', 0)}")
        self.status_vars['apps_generated'].set(f"Applications: {daily_stats.get('applications_generated', 0)}")
        self.status_vars['quality_avg'].set(f"Avg Quality: {daily_stats.get('quality_average', 0.0):.1f}/10")
        self.status_vars['last_update'].set(f"Updated: {datetime.now().strftime('%H:%M:%S')}")
        
        # Update system health
        system_health = status.get('system_health', {})
        if all(health == 'operational' for health in system_health.values()):
            self.system_status_var.set("System: All Operational")
        else:
            self.system_status_var.set("System: Check Status")
    
    # Bot launch methods
    def launch_master_dashboard(self):
        """Launch Master Dashboard"""
        try:
            dashboard_path = self.base_path.parent / "AUTOMATION-BOTS" / "04-MASTER-LAUNCHER" / "launch-all-apps.py"
            subprocess.Popen([sys.executable, str(dashboard_path)])
            self.log_activity("🎯 Master Dashboard launched")
        except Exception as e:
            self.log_activity(f"❌ Failed to launch Master Dashboard: {e}")
    
    def launch_github_logger(self):
        """Launch GitHub Dev Logger"""
        try:
            github_path = self.base_path.parent / "AUTOMATION-BOTS" / "02-GITHUB-DEV-LOGGER" / "gui" / "github-dev-logger-gui.py"
            subprocess.Popen([sys.executable, str(github_path)])
            self.log_activity("📝 GitHub Dev Logger launched")
        except Exception as e:
            self.log_activity(f"❌ Failed to launch GitHub Logger: {e}")
    
    def launch_learning_assistant(self):
        """Launch Learning Assistant"""
        try:
            learning_path = self.base_path.parent / "AUTOMATION-BOTS" / "03-LEARNING-ASSISTANT" / "gui" / "learning-assistant.py"
            subprocess.Popen([sys.executable, str(learning_path)])
            self.log_activity("🎓 Learning Assistant launched")
        except Exception as e:
            self.log_activity(f"❌ Failed to launch Learning Assistant: {e}")

def main():
    """Application entry point"""
    root = tk.Tk()
    app = CommanderHubGUI(root)
    
    # Handle window close
    def on_closing():
        if app.automation_running:
            app.stop_automation()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()