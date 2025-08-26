#!/usr/bin/env python3
"""
AI Job Hunt Commander GUI - Professional Application Automation Interface
========================================================================

Modern GUI interface for the AI Job Hunt Commander that matches the existing
automation bot ecosystem styling and provides comprehensive job application automation.

Author: Trey (Infrastructure Engineer to AI/Automation Specialist)
Purpose: Professional GUI for complete job application automation
Connection: Integrates seamlessly with the automation bot ecosystem
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import sys
import threading
import json
from pathlib import Path
from datetime import datetime

# Add the src directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

try:
    from main_application_engine import ApplicationEngine
except ImportError as e:
    print(f"Error importing AI Job Hunt Commander modules: {e}")
    sys.exit(1)

class AIJobHuntCommanderGUI:
    """
    Professional GUI for AI Job Hunt Commander
    
    Matches the existing automation bot ecosystem styling while providing
    comprehensive job application automation capabilities.
    """
    
    def __init__(self, root):
        self.root = root
        self.engine = ApplicationEngine(output_dir="Generated_Applications")
        self.current_package = None
        
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        
        # Display welcome message
        self.add_log_message("🤖 AI Job Hunt Commander initialized")
        self.add_log_message("🎯 Ready for professional application automation")
    
    def setup_window(self):
        """Configure main window with professional styling"""
        self.root.title("AI Job Hunt Commander - Professional Application Automation")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1000x800+{x}+{y}")
        
        # Set minimum size
        self.root.minsize(800, 600)
    
    def setup_styles(self):
        """Setup professional styling matching automation bot ecosystem"""
        self.style = ttk.Style()
        
        # Use modern theme
        try:
            self.style.theme_use('vista')
        except:
            try:
                self.style.theme_use('clam')
            except:
                pass
        
        # Configure custom styles
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Arial', 10))
        self.style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        self.style.configure('Secondary.TButton', font=('Arial', 9))
    
    def create_widgets(self):
        """Create professional interface matching bot ecosystem style"""
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header section
        self.create_header(main_container)
        
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create tabs
        self.create_application_tab()
        self.create_analytics_tab()
        self.create_integration_tab()
        self.create_settings_tab()
    
    def create_header(self, parent):
        """Create professional header section"""
        header_frame = tk.Frame(parent, bg='#f0f0f0')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Main title
        title_label = tk.Label(header_frame,
                              text="🤖 AI Job Hunt Commander",
                              font=('Arial', 18, 'bold'),
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="Professional Application Automation | Infrastructure → AI Career Transition",
                                 font=('Arial', 10),
                                 bg='#f0f0f0', fg='#7f8c8d')
        subtitle_label.pack(pady=(0, 5))
        
        # Status indicator
        status_label = tk.Label(header_frame,
                               text="🟢 AI Engine Ready | OpenAI Integration Available | Triple-Duty Strategy Active",
                               font=('Arial', 9, 'bold'),
                               bg='#f0f0f0', fg='#27ae60')
        status_label.pack(pady=(5, 0))
    
    def create_application_tab(self):
        """Create main application generation tab"""
        app_frame = ttk.Frame(self.notebook)
        self.notebook.add(app_frame, text="📋 Generate Application")
        
        # Input section
        input_frame = tk.LabelFrame(app_frame, text="Job Information Input", 
                                   font=('Arial', 10, 'bold'), padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Company name input
        tk.Label(input_frame, text="Company Name:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.company_entry = tk.Entry(input_frame, font=('Arial', 10), width=50)
        self.company_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='ew')
        
        # Job title input
        tk.Label(input_frame, text="Job Title:", font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.job_title_entry = tk.Entry(input_frame, font=('Arial', 10), width=50)
        self.job_title_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky='ew')
        
        # Job URL input (for future Layer 2 integration)
        tk.Label(input_frame, text="Job URL (Layer 2):", font=('Arial', 9)).grid(row=2, column=0, sticky='w', pady=5)
        self.job_url_entry = tk.Entry(input_frame, font=('Arial', 10), width=50)
        self.job_url_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky='ew')
        
        # Configure grid weights
        input_frame.columnconfigure(1, weight=1)
        
        # Action buttons
        button_frame = tk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Generate application button
        generate_btn = tk.Button(button_frame, 
                                text="🚀 Generate Complete Application Package",
                                command=self.generate_application,
                                font=('Arial', 11, 'bold'),
                                bg='#3498db', fg='white',
                                activebackground='#2980b9', activeforeground='white',
                                relief='flat', bd=0, padx=20, pady=10,
                                cursor='hand2')
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        clear_btn = tk.Button(button_frame,
                             text="🗑️ Clear Form", 
                             command=self.clear_form,
                             font=('Arial', 10),
                             bg='#95a5a6', fg='white',
                             activebackground='#7f8c8d', activeforeground='white',
                             relief='flat', bd=0, padx=15, pady=8,
                             cursor='hand2')
        clear_btn.pack(side=tk.LEFT)
        
        # Results section
        results_frame = tk.LabelFrame(app_frame, text="Application Generation Results", 
                                     font=('Arial', 10, 'bold'), padx=10, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Results text area with scrolling
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                     font=('Consolas', 9),
                                                     wrap=tk.WORD, height=15)
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Results action buttons
        results_button_frame = tk.Frame(results_frame)
        results_button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.open_files_btn = tk.Button(results_button_frame,
                                       text="📁 Open Generated Files",
                                       command=self.open_generated_files,
                                       font=('Arial', 9),
                                       bg='#27ae60', fg='white',
                                       activebackground='#219a52', activeforeground='white',
                                       relief='flat', bd=0, padx=12, pady=6,
                                       cursor='hand2', state='disabled')
        self.open_files_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.copy_summary_btn = tk.Button(results_button_frame,
                                         text="📋 Copy Summary",
                                         command=self.copy_results_summary,
                                         font=('Arial', 9),
                                         bg='#f39c12', fg='white',
                                         activebackground='#e67e22', activeforeground='white',
                                         relief='flat', bd=0, padx=12, pady=6,
                                         cursor='hand2', state='disabled')
        self.copy_summary_btn.pack(side=tk.LEFT)
    
    def create_analytics_tab(self):
        """Create analytics dashboard tab"""
        analytics_frame = ttk.Frame(self.notebook)
        self.notebook.add(analytics_frame, text="📊 Analytics")
        
        # Analytics header
        analytics_header = tk.Label(analytics_frame,
                                   text="📈 Application Analytics Dashboard",
                                   font=('Arial', 14, 'bold'))
        analytics_header.pack(pady=20)
        
        # Refresh analytics button
        refresh_btn = tk.Button(analytics_frame,
                               text="🔄 Refresh Analytics",
                               command=self.refresh_analytics,
                               font=('Arial', 10, 'bold'),
                               bg='#9b59b6', fg='white',
                               activebackground='#8e44ad', activeforeground='white',
                               relief='flat', bd=0, padx=15, pady=8,
                               cursor='hand2')
        refresh_btn.pack(pady=(0, 20))
        
        # Analytics display
        self.analytics_text = scrolledtext.ScrolledText(analytics_frame,
                                                       font=('Consolas', 10),
                                                       wrap=tk.WORD, height=25)
        self.analytics_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    def create_integration_tab(self):
        """Create ecosystem integration tab"""
        integration_frame = ttk.Frame(self.notebook)
        self.notebook.add(integration_frame, text="🔗 Ecosystem Integration")
        
        # Integration header
        integration_header = tk.Label(integration_frame,
                                     text="🤖 Automation Bot Ecosystem Integration",
                                     font=('Arial', 14, 'bold'))
        integration_header.pack(pady=20)
        
        # Integration options
        integration_options = tk.Frame(integration_frame)
        integration_options.pack(fill=tk.X, padx=20, pady=20)
        
        # GitHub Dev Logger integration
        github_frame = tk.LabelFrame(integration_options, text="GitHub Development Logger Integration",
                                    font=('Arial', 10, 'bold'), padx=10, pady=10)
        github_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(github_frame, text="Generate development logs from job application automation:",
                font=('Arial', 9)).pack(anchor='w', pady=5)
        
        github_btn = tk.Button(github_frame,
                              text="📝 Generate GitHub Dev Content",
                              command=self.generate_github_content,
                              font=('Arial', 9),
                              bg='#34495e', fg='white',
                              activebackground='#2c3e50', activeforeground='white',
                              relief='flat', bd=0, padx=12, pady=6,
                              cursor='hand2')
        github_btn.pack(anchor='w', pady=5)
        
        # Tailored Apply Bot integration
        tailored_frame = tk.LabelFrame(integration_options, text="Tailored Apply Bot Integration",
                                      font=('Arial', 10, 'bold'), padx=10, pady=10)
        tailored_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(tailored_frame, text="Enhanced with AI Job Hunt Commander capabilities:",
                font=('Arial', 9)).pack(anchor='w', pady=5)
        
        tailored_btn = tk.Button(tailored_frame,
                                text="🔗 Launch Tailored Apply Bot",
                                command=self.launch_tailored_apply,
                                font=('Arial', 9),
                                bg='#e74c3c', fg='white',
                                activebackground='#c0392b', activeforeground='white',
                                relief='flat', bd=0, padx=12, pady=6,
                                cursor='hand2')
        tailored_btn.pack(anchor='w', pady=5)
        
        # Master Launcher integration
        master_frame = tk.LabelFrame(integration_options, text="Master Launcher Integration",
                                    font=('Arial', 10, 'bold'), padx=10, pady=10)
        master_frame.pack(fill=tk.X)
        
        tk.Label(master_frame, text="Return to the master automation suite launcher:",
                font=('Arial', 9)).pack(anchor='w', pady=5)
        
        master_btn = tk.Button(master_frame,
                              text="🏠 Return to Master Launcher",
                              command=self.return_to_master,
                              font=('Arial', 9),
                              bg='#16a085', fg='white',
                              activebackground='#138d75', activeforeground='white',
                              relief='flat', bd=0, padx=12, pady=6,
                              cursor='hand2')
        master_btn.pack(anchor='w', pady=5)
    
    def create_settings_tab(self):
        """Create settings and configuration tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Settings header
        settings_header = tk.Label(settings_frame,
                                  text="⚙️ AI Job Hunt Commander Settings",
                                  font=('Arial', 14, 'bold'))
        settings_header.pack(pady=20)
        
        # OpenAI configuration
        openai_frame = tk.LabelFrame(settings_frame, text="OpenAI Configuration",
                                    font=('Arial', 10, 'bold'), padx=10, pady=10)
        openai_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        tk.Label(openai_frame, text="OpenAI API Key (for enhanced AI features):",
                font=('Arial', 9)).pack(anchor='w', pady=5)
        
        self.openai_key_entry = tk.Entry(openai_frame, font=('Arial', 10), width=60, show='*')
        self.openai_key_entry.pack(fill=tk.X, pady=5)
        
        # Output directory configuration
        output_frame = tk.LabelFrame(settings_frame, text="Output Configuration",
                                    font=('Arial', 10, 'bold'), padx=10, pady=10)
        output_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        tk.Label(output_frame, text="Generated Applications Directory:",
                font=('Arial', 9)).pack(anchor='w', pady=5)
        
        dir_frame = tk.Frame(output_frame)
        dir_frame.pack(fill=tk.X, pady=5)
        
        self.output_dir_entry = tk.Entry(dir_frame, font=('Arial', 10))
        self.output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.output_dir_entry.insert(0, "Generated_Applications")
        
        browse_btn = tk.Button(dir_frame,
                              text="📁 Browse",
                              command=self.browse_output_directory,
                              font=('Arial', 9),
                              bg='#95a5a6', fg='white',
                              activebackground='#7f8c8d', activeforeground='white',
                              relief='flat', bd=0, padx=10, pady=6,
                              cursor='hand2')
        browse_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Save settings button
        save_btn = tk.Button(settings_frame,
                            text="💾 Save Settings",
                            command=self.save_settings,
                            font=('Arial', 10, 'bold'),
                            bg='#27ae60', fg='white',
                            activebackground='#229954', activeforeground='white',
                            relief='flat', bd=0, padx=20, pady=10,
                            cursor='hand2')
        save_btn.pack(pady=20)
    
    def generate_application(self):
        """Generate complete application package"""
        company = self.company_entry.get().strip()
        job_title = self.job_title_entry.get().strip()
        
        if not company or not job_title:
            messagebox.showerror("Input Error", "Please enter both company name and job title.")
            return
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.add_log_message("🚀 Starting AI-powered application generation...")
        self.add_log_message(f"🏢 Company: {company}")
        self.add_log_message(f"💼 Position: {job_title}")
        
        # Disable generate button during processing
        self.disable_generate_button()
        
        # Run generation in separate thread
        generation_thread = threading.Thread(
            target=self._generate_application_thread,
            args=(company, job_title)
        )
        generation_thread.daemon = True
        generation_thread.start()
    
    def _generate_application_thread(self, company, job_title):
        """Application generation thread"""
        try:
            # Generate application package
            package = self.engine.process_job_application(
                company_name=company,
                job_title=job_title
            )
            
            # Schedule GUI updates on main thread
            self.root.after(0, self._handle_generation_success, package)
            
        except Exception as e:
            self.root.after(0, self._handle_generation_error, str(e))
    
    def _handle_generation_success(self, package):
        """Handle successful application generation"""
        if package:
            self.current_package = package
            self.add_log_message("")
            self.add_log_message("🎉 APPLICATION PACKAGE COMPLETED!")
            self.add_log_message("=" * 60)
            self.add_log_message(f"📋 Application ID: {package['application_id']}")
            self.add_log_message(f"⭐ Quality Score: {package['application_score']:.1f}/10")
            self.add_log_message(f"📄 Files Generated: {len(package['files_generated'])}")
            
            self.add_log_message("")
            self.add_log_message("📁 Generated Files:")
            for file_path in package['files_generated']:
                self.add_log_message(f"   • {Path(file_path).name}")
            
            self.add_log_message("")
            self.add_log_message("💡 Next Steps:")
            for i, step in enumerate(package['next_steps'][:5], 1):
                self.add_log_message(f"   {i}. {step}")
            
            # Enable result buttons
            self.open_files_btn.config(state='normal')
            self.copy_summary_btn.config(state='normal')
        else:
            self.add_log_message("❌ Application generation failed. Please try again.")
        
        # Re-enable generate button
        self.enable_generate_button()
    
    def _handle_generation_error(self, error_message):
        """Handle application generation error"""
        self.add_log_message(f"❌ Error generating application: {error_message}")
        self.enable_generate_button()
    
    def add_log_message(self, message):
        """Add message to results log"""
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()
    
    def disable_generate_button(self):
        """Disable generate button during processing"""
        for widget in self.root.winfo_children():
            self._set_widget_state(widget, 'disabled')
    
    def enable_generate_button(self):
        """Re-enable generate button after processing"""
        for widget in self.root.winfo_children():
            self._set_widget_state(widget, 'normal')
    
    def _set_widget_state(self, widget, state):
        """Recursively set widget state"""
        try:
            if hasattr(widget, 'config'):
                widget.config(state=state)
        except:
            pass
        
        for child in widget.winfo_children():
            self._set_widget_state(child, state)
    
    def clear_form(self):
        """Clear input form"""
        self.company_entry.delete(0, tk.END)
        self.job_title_entry.delete(0, tk.END)
        self.job_url_entry.delete(0, tk.END)
        self.results_text.delete(1.0, tk.END)
        self.open_files_btn.config(state='disabled')
        self.copy_summary_btn.config(state='disabled')
        self.current_package = None
    
    def open_generated_files(self):
        """Open generated files directory"""
        if self.current_package:
            try:
                import os
                app_dir = Path(self.current_package['files_generated'][0]).parent
                if os.name == 'nt':
                    os.startfile(str(app_dir))
                else:
                    subprocess.Popen(['open', str(app_dir)])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open files directory: {e}")
    
    def copy_results_summary(self):
        """Copy results summary to clipboard"""
        if self.current_package:
            try:
                summary = f"""AI Job Hunt Commander - Application Summary
Company: {self.current_package['job_information']['company']}
Position: {self.current_package['job_information']['title']}
Application ID: {self.current_package['application_id']}
Quality Score: {self.current_package['application_score']:.1f}/10
Files Generated: {len(self.current_package['files_generated'])}

Generated by Infrastructure → AI Career Transition Toolkit"""
                
                self.root.clipboard_clear()
                self.root.clipboard_append(summary)
                messagebox.showinfo("Copied", "Application summary copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not copy summary: {e}")
    
    def refresh_analytics(self):
        """Refresh analytics dashboard"""
        try:
            self.analytics_text.delete(1.0, tk.END)
            analytics = self.engine.get_application_analytics()
            
            if analytics.get('total_applications', 0) == 0:
                self.analytics_text.insert(tk.END, "📊 APPLICATION ANALYTICS DASHBOARD\n")
                self.analytics_text.insert(tk.END, "=" * 50 + "\n\n")
                self.analytics_text.insert(tk.END, "📝 No applications generated yet.\n")
                self.analytics_text.insert(tk.END, "💡 Generate your first application to see analytics!\n")
                return
            
            # Display analytics
            self.analytics_text.insert(tk.END, "📊 APPLICATION ANALYTICS DASHBOARD\n")
            self.analytics_text.insert(tk.END, "=" * 50 + "\n\n")
            self.analytics_text.insert(tk.END, f"📈 Total Applications: {analytics['total_applications']}\n")
            self.analytics_text.insert(tk.END, f"⭐ Average Score: {analytics['average_score']:.1f}/10\n")
            self.analytics_text.insert(tk.END, f"🏢 Companies Applied: {analytics['companies_applied']}\n\n")
            
            # Score distribution
            dist = analytics['score_distribution']
            self.analytics_text.insert(tk.END, "📊 Score Distribution:\n")
            self.analytics_text.insert(tk.END, f"   🟢 High (8.0+): {dist['high']} applications\n")
            self.analytics_text.insert(tk.END, f"   🟡 Medium (6.0-7.9): {dist['medium']} applications\n")
            self.analytics_text.insert(tk.END, f"   🔴 Low (<6.0): {dist['low']} applications\n\n")
            
            # Recent applications
            if analytics['recent_applications']:
                self.analytics_text.insert(tk.END, "📋 Recent Applications:\n")
                for app in analytics['recent_applications']:
                    self.analytics_text.insert(tk.END, 
                        f"   • {app['company']} - {app['title']} ({app['score']:.1f}/10) [{app['date']}]\n")
            
        except Exception as e:
            self.analytics_text.insert(tk.END, f"❌ Error loading analytics: {e}\n")
    
    def generate_github_content(self):
        """Generate GitHub development log content"""
        if self.current_package:
            content = f"""🤖 AI Job Hunt Commander Activity Log

📋 Application Generated:
   Company: {self.current_package['job_information']['company']}
   Position: {self.current_package['job_information']['title']}
   Quality Score: {self.current_package['application_score']:.1f}/10

🔧 Technologies Used:
   • Python automation
   • OpenAI integration
   • AI-powered content generation
   • Resume customization algorithms
   
🎯 Career Transition Progress:
   Infrastructure → AI/Automation specialist development continues with
   practical application automation showcasing real-world AI engineering skills.

#JobSearch #Automation #AI #CareerTransition #InfrastructureToAI"""
            
            messagebox.showinfo("GitHub Content", "Content generated! Copy and use with GitHub Dev Logger Bot:\n\n" + content[:200] + "...")
        else:
            messagebox.showwarning("No Application", "Generate an application first to create GitHub content.")
    
    def launch_tailored_apply(self):
        """Launch Tailored Apply Bot"""
        try:
            import subprocess
            script_path = Path(__file__).parent.parent.parent / "01-JOB-APPLICATION-GENERATOR" / "gui" / "job-bot-gui.py"
            subprocess.Popen([sys.executable, str(script_path)])
            messagebox.showinfo("Launched", "Tailored Apply Bot GUI launched!")
        except Exception as e:
            messagebox.showerror("Launch Error", f"Could not launch Tailored Apply Bot: {e}")
    
    def return_to_master(self):
        """Return to Master Launcher"""
        try:
            import subprocess
            script_path = Path(__file__).parent.parent.parent / "04-MASTER-LAUNCHER" / "launch-all-apps.py"
            subprocess.Popen([sys.executable, str(script_path)])
            messagebox.showinfo("Launched", "Master Launcher opened!")
        except Exception as e:
            messagebox.showerror("Launch Error", f"Could not launch Master Launcher: {e}")
    
    def browse_output_directory(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, directory)
    
    def save_settings(self):
        """Save application settings"""
        try:
            settings = {
                'openai_api_key': self.openai_key_entry.get(),
                'output_directory': self.output_dir_entry.get(),
                'saved_at': datetime.now().isoformat()
            }
            
            settings_path = Path(__file__).parent.parent / 'ai_job_hunt_commander_settings.json'
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=2)
            
            messagebox.showinfo("Settings Saved", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save settings: {e}")

def main():
    """Main GUI application entry point"""
    root = tk.Tk()
    app = AIJobHuntCommanderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()