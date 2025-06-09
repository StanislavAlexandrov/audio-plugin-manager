import tkinter as tk
from tkinter import ttk, messagebox
import os
import pathlib
import subprocess
import shutil

# ==============================================================================
# PLUGIN DATABASE (Your database remains unchanged)
# ==============================================================================
PLUGIN_DATABASE = {
    "ADPTR MetricAB": ("A referencing tool to A/B your mix against other tracks.", 5),
    "Atlas": ("An AI-powered drum machine that organizes samples into a visual map.", 4),
    "Auburn Sounds Graillon": ("A vocal processing plugin for pitch correction and creative effects.", 4),
    "BBC Symphony Orchestra": ("A detailed orchestral sample library by Spitfire Audio.", 5),
    "CHOW Tape Model": ("A physical model of an analog tape machine for saturation effects.", 4),
    "Cthulhu": ("A MIDI chord and arpeggiator tool for generating harmonic ideas.", 5),
    "Cymatics Memory": ("A vintage effects plugin designed to emulate lo-fi hardware.", 3),
    "Decimort2": ("A high-quality bit crusher for adding vintage digital character.", 4),
    "Dexed": ("A highly accurate and free FM synthesizer modeled on the Yamaha DX7.", 4),
    "DimensionExpander": ("A free chorus/spatial tool from Xfer Records to widen stereo image.", 4),
    "Diva": ("A virtual analog synth known for its authentic, hardware-like sound.", 5),
    "DSEQ3": ("A dynamic spectral equalizer that intelligently removes harsh frequencies.", 4),
    "EchoBoy": ("A comprehensive delay plugin emulating a vast range of delay units.", 5),
    "FabFilter Pro-C": ("An industry-standard compressor with multiple versatile styles.", 5),
    "FabFilter Pro-DS": ("A transparent and intelligent de-esser for taming sibilance.", 5),
    "FabFilter Pro-G": ("A flexible and powerful gate/expander for dynamic control.", 5),
    "FabFilter Pro-L": ("A world-class true peak limiter for mastering and loud mixes.", 5),
    "FabFilter Pro-MB": ("A powerful multiband compressor/expander with a visual workflow.", 5),
    "FabFilter Pro-Q": ("The industry-standard equalizer, prized for its features and UI.", 5),
    "FabFilter Pro-R": ("A natural-sounding algorithmic reverb with musical controls.", 5),
    "FabFilter Saturn": ("An advanced multiband saturation and distortion plugin.", 5),
    "FabFilter Simplon": ("A simple and effective dual-filter plugin.", 3),
    "FabFilter Timeless": ("A creative tape delay plugin with extensive modulation options.", 5),
    "FabFilter Twin": ("A powerful virtual analog synthesizer with a flexible modulation system.", 4),
    "FabFilter Volcano": ("A creative filter effect with multiple modulatable filters.", 4),
    "Fresh Air": ("A dynamic high-frequency processor that adds clarity and shimmer.", 4),
    "Infiltrator": ("A powerful multi-effects plugin for stacking and sequencing effects.", 4),
    "Neutron": ("A comprehensive channel strip with an AI Mix Assistant.", 5),
    "Ozone": ("An all-in-one AI-powered mastering suite.", 5),
    "RX 9": ("The industry-standard audio repair and restoration tool.", 5),
    "RX 10": ("The industry-standard audio repair and restoration tool.", 5),
    "Tonal Balance Control": ("A mastering utility that visualizes spectral balance.", 4),
    "VocalSynth": ("A creative vocal processing plugin for unique synthesized vocal sounds.", 4),
    "Vinyl": ("A lo-fi effect that simulates the dust and character of a vinyl record.", 4),
    "KClip3": ("A clipper and saturator designed for loud and transparent mastering.", 4),
    "Kickstart 2": ("A simple utility for creating instant sidechain compression effects.", 4),
    "Kontakt": ("The industry-standard sampler platform for countless instruments.", 5),
    "LABS": ("A free instrument platform by Spitfire Audio with unique sounds.", 5),
    "LFOTool": ("A utility for highly customizable LFO-based modulation effects.", 5),
    "Little Plate": ("A plate reverb emulating the classic EMT 140 for vintage sound.", 4),
    "Manipulator": ("A real-time vocal processor for dramatic pitch and timbre shifting.", 4),
    "Melodyne": ("A sophisticated tool for detailed pitch and time editing of audio notes.", 5),
    "MODO BASS": ("A physically modeled electric bass instrument.", 4),
    "Nexus": ("A ROM-synthesizer packed with production-ready sounds.", 4),
    "OTT": ("An aggressive, multiband, upward/downward compressor effect.", 5),
    "Oxford Inflator": ("A unique processor to increase loudness and perceived warmth.", 5),
    "PhaseMistress": ("A rich and versatile phaser effect modeled on classic hardware.", 4),
    "RC-20 Retro Color": ("A multi-effects plugin for adding vintage, lo-fi character.", 5),
    "Relay": ("An iZotope utility for inter-plugin communication.", 3),
    "RoughRider3": ("A free and aggressive compressor for adding punch.", 3),
    "RX950": ("An effect emulating the crunchy 12-bit sound of the Akai S950 sampler.", 4),
    "Saturation Knob": ("A simple, free one-knob saturator for adding warmth.", 4),
    "Serato Sample": ("An intuitive sampler for chopping and manipulating samples.", 4),
    "Serum": ("An iconic wavetable synthesizer, famous for its sound and visual workflow.", 5),
    "ShaperBox": ("A multi-effects tool for controlling effects with custom LFO shapes.", 4),
    "smart:EQ": ("An AI-powered equalizer that suggests corrective EQ curves.", 4),
    "SPAN": ("A free and highly flexible real-time audio spectrum analyzer.", 5),
    "Spire": ("A powerful polyphonic synthesizer combining multiple synth engines.", 4),
    "StandardCLIP": ("A versatile soft and hard clipper for loudness control.", 3),
    "Sylenth1": ("A classic virtual analog synth known for its warm sound and low CPU use.", 5),
    "TAL-Chorus-LX": ("A free, high-quality emulation of the Roland Juno-60 chorus.", 4),
    "TAL-U-NO-LX": ("A popular and accurate software emulation of the Roland Juno-60 synth.", 4),
    "Thermal": ("A multi-band distortion plugin for interactive distortion effects.", 4),
    "Transient Master": ("A simple tool for shaping the attack and sustain of sounds.", 4),
    "ValhallaDelay": ("A versatile delay plugin with vintage and modern delay modes.", 5),
    "ValhallaShimmer": ("A reverb plugin known for its massive, ethereal, pitch-shifted decays.", 5),
    "ValhallaSupermassive": ("A free reverb/delay known for huge, lush, and abstract spaces.", 5),
    "ValhallaVintageVerb": ("A reverb plugin emulating classic hardware digital reverbs of the 70s/80s.", 5),
    "Vital": ("A powerful and free spectral warping wavetable synthesizer.", 5),
    "Wider": ("A free stereo widening plugin that maintains mono-compatibility.", 4),
}


# --- Constants ---
PLUGIN_PATHS = {
    "VST": ["/Library/Audio/Plug-Ins/VST/", "~/Library/Audio/Plug-Ins/VST/"],
    "VST3": ["/Library/Audio/Plug-Ins/VST3/", "~/Library/Audio/Plug-Ins/VST3/"],
    "AU (Components)": ["/Library/Audio/Plug-Ins/Components/", "~/Library/Audio/Plug-Ins/Components/"],
}
PLUGIN_EXTENSIONS = {
    "VST": ".vst",
    "VST3": ".vst3",
    "AU (Components)": ".component",
}


def find_plugin_info(plugin_name):
    """
    Finds plugin info from the database using flexible matching.
    It checks if a known database key is contained within the plugin name.
    """
    if plugin_name in PLUGIN_DATABASE:
        return PLUGIN_DATABASE[plugin_name]
    
    for key, value in PLUGIN_DATABASE.items():
        if key.lower() in plugin_name.lower():
            return value
    return None, None


class PluginManager(tk.Tk):
    """
    A Tkinter application to scan, display, and delete audio plugins on macOS,
    with an integrated plugin information database.
    """
    def __init__(self):
        super().__init__()
        self.title("macOS Audio Plugin Manager")
        self.geometry("1000x700")

        # --- Style Configuration ---
        style = ttk.Style(self)
        style.configure("Treeview", rowheight=25)

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Top Controls ---
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))

        self.scan_button = ttk.Button(controls_frame, text="Scan for Plugins", command=self.scan_and_display_plugins)
        self.scan_button.pack(side=tk.LEFT)

        self.delete_button = ttk.Button(controls_frame, text="Delete Selected", command=self.delete_selected_plugins, state=tk.DISABLED)
        self.delete_button.pack(side=tk.RIGHT)
        
        self.status_label = ttk.Label(controls_frame, text="Ready. Click 'Scan for Plugins' to begin.")
        self.status_label.pack(side=tk.LEFT, padx=20)

        # --- Treeview for Plugin Display ---
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Enable multiple selections
        self.tree = ttk.Treeview(tree_frame, columns=("type", "path"), show="tree headings", selectmode="extended")
        self.tree.heading("#0", text="Plugin / Description")
        self.tree.heading("type", text="Format")
        self.tree.heading("path", text="Full Path")

        self.tree.column("#0", width=300, anchor=tk.W)
        self.tree.column("type", width=120, anchor=tk.W)
        self.tree.column("path", width=580, anchor=tk.W)

        self.tree.tag_configure("description", foreground="gray40")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Event Bindings ---
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def scan_plugins(self):
        self.status_label.config(text="Scanning...")
        self.update_idletasks()
        
        found_plugins = {}
        for plugin_type, paths in PLUGIN_PATHS.items():
            extension = PLUGIN_EXTENSIONS[plugin_type]
            for path_str in paths:
                p = pathlib.Path(path_str).expanduser()
                if not p.exists(): continue
                
                for item in p.glob(f"**/*{extension}"):
                    base_name = item.stem.replace('_x64', '').replace('AU64', '')
                    if base_name.startswith('.'): continue
                        
                    if base_name not in found_plugins:
                        found_plugins[base_name] = []
                    
                    found_plugins[base_name].append({
                        "type": plugin_type,
                        "path": str(item),
                        "filename": item.name
                    })
        self.status_label.config(text=f"Scan complete. Found {sum(len(v) for v in found_plugins.values())} plugin files.")
        return found_plugins

    def populate_tree(self, plugins, open_groups=None):
        """Populates the tree, optionally keeping specified groups open."""
        if open_groups is None:
            open_groups = set()

        for i in self.tree.get_children():
            self.tree.delete(i)
        
        sorted_plugin_names = sorted(plugins.keys(), key=lambda s: s.lower())
        
        for name in sorted_plugin_names:
            # Check if this group should be open
            is_open = name in open_groups
            parent_id = self.tree.insert("", tk.END, text=name, open=is_open, tags=('group',))
            
            description, stars = find_plugin_info(name)
            if description and stars:
                star_rating = "★" * stars + "☆" * (5 - stars)
                desc_text = f"    {star_rating} {description}"
                self.tree.insert(parent_id, tk.END, text=desc_text, tags=('description',), values=("Info", ""))

            for details in plugins[name]:
                display_text = f"  ↳ {details['filename']}"
                self.tree.insert(
                    parent_id,
                    tk.END,
                    text=display_text,
                    values=(details["type"], details["path"]),
                    tags=('plugin_file',)
                )

    def scan_and_display_plugins(self, open_groups=None):
        """Scans and repopulates the tree, preserving open group state."""
        plugins = self.scan_plugins()
        self.populate_tree(plugins, open_groups)

    def on_tree_select(self, event):
        """NEW: Enables delete button if any selected item is a deletable file."""
        selected_items = self.tree.selection()
        if not selected_items:
            self.delete_button.config(state=tk.DISABLED)
            return

        # Check if at least one of the selected items is a real plugin file
        is_any_file_selected = any(
            'plugin_file' in self.tree.item(item_id, "tags") 
            for item_id in selected_items
        )

        if is_any_file_selected:
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.delete_button.config(state=tk.DISABLED)

    def delete_selected_plugins(self):
        """
        NEW AND IMPROVED: Deletes all selected plugin files, handles multiple
        system files with a single password prompt, and preserves the open
        state of non-deleted groups.
        """
        selected_items = self.tree.selection()
        if not selected_items: return

        # --- BONUS POINTS: Record which groups are currently open ---
        open_groups_before_delete = set()
        for item_id in self.tree.get_children(''): # Get top-level items
            if self.tree.item(item_id, 'open'):
                group_name = self.tree.item(item_id, 'text')
                open_groups_before_delete.add(group_name)

        # --- Step 1: Collect all valid file paths to delete ---
        paths_to_delete = []
        for item_id in selected_items:
            item_tags = self.tree.item(item_id, "tags")
            if 'plugin_file' in item_tags:
                plugin_path_str = self.tree.item(item_id, "values")[1]
                paths_to_delete.append(plugin_path_str)

        if not paths_to_delete:
            messagebox.showwarning("Selection Error", "No plugin files selected. Please select one or more files (indented with ↳) to delete.")
            return

        # --- Step 2: Confirm with the user ---
        file_list = "\n".join(f"- {os.path.basename(p)}" for p in paths_to_delete)
        confirmed = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to permanently delete these {len(paths_to_delete)} files?\n\n{file_list}"
        )
        if not confirmed: return

        # --- Step 3: Separate files into user-level and system-level ---
        user_files = []
        system_files = []
        user_home_path = pathlib.Path.home()

        for path_str in paths_to_delete:
            p = pathlib.Path(path_str)
            if p.is_relative_to(user_home_path):
                user_files.append(p)
            else:
                system_files.append(str(p)) # Keep as string for shell command

        # --- Step 4: Delete the files ---
        try:
            # Delete user files directly (no password needed)
            if user_files:
                self.status_label.config(text=f"Deleting {len(user_files)} user plugin(s)...")
                self.update_idletasks()
                for p in user_files:
                    if p.is_dir(): shutil.rmtree(p)
                    else: os.remove(p)
            
            # Delete system files with a single admin command
            if system_files:
                self.status_label.config(text=f"Deleting {len(system_files)} system plugin(s)... Password may be required.")
                self.update_idletasks()
                
                # Quote each path to handle spaces, then join them for the shell command
                quoted_paths = [f'\\"{path}\\"' for path in system_files]
                rm_command = f'rm -rf {" ".join(quoted_paths)}'
                
                # Build and run the AppleScript
                script = f'do shell script "{rm_command}" with administrator privileges'
                result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)

                if result.returncode != 0:
                    error_message = result.stderr.strip()
                    if "User canceled" in error_message:
                        raise RuntimeError("Deletion was cancelled by the user.")
                    else:
                        raise RuntimeError(f"Admin deletion failed:\n\n{error_message}")

            messagebox.showinfo("Success", f"Successfully deleted {len(paths_to_delete)} plugin file(s).")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="An error occurred during deletion.")
        
        finally:
            # --- Step 5: Refresh the list, preserving the open state ---
            self.scan_and_display_plugins(open_groups=open_groups_before_delete)


if __name__ == "__main__":
    app = PluginManager()
    app.mainloop()