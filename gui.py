"""
GUI module for XML to SQL Converter.
Separated from business logic to maintain decoupling.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
from conversion_service import ConversionService


class GUIController:
    """
    Controller for the GUI, orchestrates UI and business logic interaction.
    """
    
    def __init__(self, root):
        self.root = root
        self.service = ConversionService()
        self.setup_window()
        self.create_widgets()
        self.setup_styles()
    
    def setup_window(self):
        """Configure main window properties."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        w = int(screen_width * 0.80)
        h = int(screen_height * 0.70)
        x = int((screen_width - w) * 0.5)
        y = int((screen_height - h) * 0.5)
        
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.title("XML to SQL Converter")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(1, weight=1)
    
    def setup_styles(self):
        """Configure text widget styles."""
        self.query_out.tag_configure("sqlkeywords", foreground="blue", font=("Courier", 10, "bold"))
        self.query_out.tag_configure("error", foreground="red", font=("Courier", 9))
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Menu bar
        self.create_menu_bar()
        
        # Input section
        self.create_input_section()
        
        # Button section
        self.create_button_section()
        
        # Output section
        self.create_output_section()
        
        # Status bar
        self.create_status_bar()
    
    def create_menu_bar(self):
        """Create menu bar."""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open XML", command=self.open_xml_file)
        file_menu.add_command(label="Save SQL", command=self.save_sql_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menu_bar, tearoff=0)
        tools_menu.add_command(label="XML Structure", command=self.show_xml_structure)
        tools_menu.add_command(label="Clear All", command=self.clear_all)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        
        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Supported Converters", command=self.show_supported_converters)
        menu_bar.add_cascade(label="Help", menu=help_menu)
    
    def create_input_section(self):
        """Create input XML section."""
        # Label
        input_label = ttk.Label(
            self.root,
            text="Input XML",
            font=("Arial", 12, "bold"),
            foreground="darkblue"
        )
        input_label.grid(row=0, column=0, pady=10, sticky="w", padx=10)
        
        # Frame with text and scrollbar
        input_frame = tk.Frame(self.root)
        input_frame.grid(row=1, column=0, padx=10, sticky="news")
        input_frame.rowconfigure(0, weight=1)
        input_frame.columnconfigure(0, weight=1)
        
        self.query_inp = tk.Text(input_frame, height=30, width=40, wrap=tk.WORD)
        self.query_inp.grid(row=0, column=0, sticky="news")
        
        input_scrollbar = tk.Scrollbar(input_frame, command=self.query_inp.yview)
        input_scrollbar.grid(row=0, column=1, sticky="ns")
        self.query_inp.config(yscrollcommand=input_scrollbar.set)
        
        # Context menu for input
        self.create_context_menu(self.query_inp)
    
    def create_button_section(self):
        """Create middle button section."""
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=1, padx=10, sticky="ew")
        button_frame.rowconfigure(0, weight=1)
        button_frame.rowconfigure(4, weight=1)
        
        # Convert button
        convert_btn = ttk.Button(
            button_frame,
            text="Convert\n>>",
            command=self.do_convert,
            width=10
        )
        convert_btn.grid(row=1, column=0, pady=10, sticky="ew")
        
        # Converter type selector
        ttk.Label(button_frame, text="Converter:").grid(row=2, column=0, pady=5)
        self.converter_var = tk.StringVar(value="Auto")
        converter_combo = ttk.Combobox(
            button_frame,
            textvariable=self.converter_var,
            values=["Auto"] + self.service.get_supported_converters(),
            state="readonly",
            width=8
        )
        converter_combo.grid(row=3, column=0, sticky="ew")
    
    def create_output_section(self):
        """Create output SQL section."""
        # Label
        output_label = ttk.Label(
            self.root,
            text="Output SQL",
            font=("Arial", 12, "bold"),
            foreground="darkblue"
        )
        output_label.grid(row=0, column=2, pady=10, sticky="w", padx=10)
        
        # Frame with text and scrollbar
        output_frame = tk.Frame(self.root)
        output_frame.grid(row=1, column=2, padx=10, sticky="news")
        output_frame.rowconfigure(0, weight=1)
        output_frame.columnconfigure(0, weight=1)
        
        self.query_out = tk.Text(output_frame, height=30, width=40, wrap=tk.WORD)
        self.query_out.grid(row=0, column=0, sticky="news")
        
        output_scrollbar = tk.Scrollbar(output_frame, command=self.query_out.yview)
        output_scrollbar.grid(row=0, column=1, sticky="ns")
        self.query_out.config(yscrollcommand=output_scrollbar.set, state="disabled")
        
        # Context menu for output
        self.create_context_menu(self.query_out)
        
        # Buttons below output
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=2, column=2, padx=10, sticky="e", pady=5)
        
        copy_btn = ttk.Button(button_frame, text="Copy", command=self.do_copy)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = ttk.Button(button_frame, text="Export", command=self.save_sql_file)
        export_btn.pack(side=tk.LEFT, padx=5)
    
    def create_status_bar(self):
        """Create status bar."""
        status_frame = tk.Frame(self.root, relief=tk.SUNKEN, bd=1)
        status_frame.grid(row=3, column=0, columnspan=3, sticky="ew")
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = tk.Label(status_frame, textvariable=self.status_var, justify=tk.LEFT)
        status_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    def create_context_menu(self, text_widget):
        """Create right-click context menu for text widget."""
        popup_menu = tk.Menu(self.root, tearoff=0)
        popup_menu.add_command(label="Copy", command=lambda: self.do_copy_widget(text_widget))
        popup_menu.add_command(label="Paste", command=lambda: self.do_paste_widget(text_widget))
        popup_menu.add_command(label="Clear", command=lambda: self.do_clear_widget(text_widget))
        
        def show_menu(e):
            popup_menu.tk_popup(e.x_root, e.y_root)
        
        text_widget.bind("<Button-3>", show_menu)
    
    def do_convert(self):
        """Convert XML to SQL."""
        xml_string = self.query_inp.get("1.0", tk.END).strip()
        
        if not xml_string:
            messagebox.showwarning("Warning", "Please enter XML content")
            self.update_status("Error: Empty XML")
            return
        
        self.update_status("Converting...")
        self.root.update()
        
        # Get converter type
        converter_type = self.converter_var.get()
        if converter_type == "Auto":
            converter_type = None
        
        # Convert
        sql = self.service.convert_xml_string(xml_string, converter_type)
        
        # Display result
        self.query_out.config(state="normal")
        self.query_out.delete("1.0", tk.END)
        
        if sql.startswith("-- Error"):
            self.query_out.insert("1.0", sql)
            self.query_out.tag_add("error", "1.0", tk.END)
            self.update_status(f"Error: {self.service.get_last_error()}")
        else:
            self.query_out.insert("1.0", sql)
            self.highlight_sql_keywords()
            used_converter = self.service.get_last_converter_type() or "Unknown"
            self.update_status(f"Converted using {used_converter}")
        
        self.query_out.config(state="disabled")
    
    def highlight_sql_keywords(self):
        """Highlight SQL keywords in output."""
        keywords = [
            "SELECT", "FROM", "JOIN", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN",
            "ON", "WHERE", "AND", "OR", "INSERT", "INTO", "VALUES", "UPDATE",
            "DELETE", "SET", "CREATE", "TABLE", "DROP", "ALTER", "AS",
            "UNION", "UNION ALL", "GROUP BY", "ORDER BY", "HAVING",
            "DISTINCT", "LIMIT", "OFFSET", "CASE", "WHEN", "THEN", "ELSE", "END"
        ]
        
        pattern = r"\b(" + "|".join(keywords) + r")\b"
        
        self.query_out.tag_remove("sqlkeywords", "1.0", tk.END)
        
        for match in re.finditer(pattern, self.query_out.get("1.0", tk.END), re.IGNORECASE):
            start_idx = f"1.0 + {match.start()} chars"
            end_idx = f"1.0 + {match.end()} chars"
            self.query_out.tag_add("sqlkeywords", start_idx, end_idx)
    
    def do_copy(self):
        """Copy output SQL to clipboard."""
        self.do_copy_widget(self.query_out)
    
    def do_copy_widget(self, widget):
        """Copy text from widget to clipboard."""
        try:
            text = widget.get("1.0", tk.END).strip()
            if text:
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
                self.update_status("Copied to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Copy failed: {str(e)}")
    
    def do_paste_widget(self, widget):
        """Paste from clipboard to widget."""
        try:
            text = self.root.clipboard_get()
            widget.config(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert("1.0", text)
            widget.config(state="disabled")
            self.update_status("Pasted from clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Paste failed: {str(e)}")
    
    def do_clear_widget(self, widget):
        """Clear widget content."""
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.config(state="disabled")
    
    def clear_all(self):
        """Clear all content."""
        self.query_inp.delete("1.0", tk.END)
        self.query_out.config(state="normal")
        self.query_out.delete("1.0", tk.END)
        self.query_out.config(state="disabled")
        self.update_status("Cleared all")
    
    def open_xml_file(self):
        """Open XML file."""
        filepath = filedialog.askopenfilename(
            title="Open XML File",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.query_inp.delete("1.0", tk.END)
                self.query_inp.insert("1.0", content)
                self.update_status(f"Loaded: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")
    
    def save_sql_file(self):
        """Save SQL output to file."""
        if not self.query_out.get("1.0", tk.END).strip():
            messagebox.showwarning("Warning", "No SQL to save")
            return
        
        filepath = filedialog.asksaveasfilename(
            title="Save SQL File",
            defaultextension=".sql",
            filetypes=[("SQL files", "*.sql"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(self.query_out.get("1.0", tk.END))
                messagebox.showinfo("Success", f"Saved to: {filepath}")
                self.update_status(f"Saved: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def show_xml_structure(self):
        """Show XML structure preview."""
        xml_string = self.query_inp.get("1.0", tk.END).strip()
        
        if not xml_string:
            messagebox.showwarning("Warning", "Please enter XML content")
            return
        
        structure = self.service.get_xml_structure(xml_string)
        
        # Create a new window for structure preview
        struct_window = tk.Toplevel(self.root)
        struct_window.title("XML Structure Preview")
        struct_window.geometry("600x400")
        
        text_widget = tk.Text(struct_window, wrap=tk.NONE, font=("Courier", 9))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(text_widget)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        text_widget.insert("1.0", structure)
        text_widget.config(state="disabled")
    
    def show_supported_converters(self):
        """Show supported converters."""
        converters = self.service.get_supported_converters()
        msg = "Supported Converters:\n\n"
        
        for conv in converters:
            msg += f"• {conv}\n"
        
        msg += "\nAuto-detection will choose the best converter based on XML structure."
        
        messagebox.showinfo("Supported Converters", msg)
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About",
            "XML to SQL Converter\n"
            "Version: 2.0\n\n"
            "A flexible, decoupled tool for converting\n"
            "various XML formats to SQL statements.\n\n"
            "Supports multiple conversion strategies\n"
            "with auto-detection capability."
        )
    
    def update_status(self, message: str):
        """Update status bar message."""
        self.status_var.set(message)


def main():
    """Application entry point."""
    root = tk.Tk()
    app = GUIController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
