import tkinter as tk
from tkinter import ttk, messagebox
import os
import pathlib
import subprocess
import shutil

# ==============================================================================
# PLUGIN DATABASE
# Maps a recognizable part of a plugin's name to its description and a
# star rating for "Industry Impact & Reputation".
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
        # NOTE: Tag configuration is now done AFTER the treeview is created.

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Top Controls ---
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))

        self.scan_button = ttk.Button(controls_frame, text="Scan for Plugins", command=self.scan_and_display_plugins)
        self.scan_button.pack(side=tk.LEFT)

        self.delete_button = ttk.Button(controls_frame, text="Delete Selected", command=self.delete_selected_plugin, state=tk.DISABLED)
        self.delete_button.pack(side=tk.RIGHT)
        
        self.status_label = ttk.Label(controls_frame, text="Ready. Click 'Scan for Plugins' to begin.")
        self.status_label.pack(side=tk.LEFT, padx=20)

        # --- Treeview for Plugin Display ---
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=("type", "path"), show="tree headings")
        self.tree.heading("#0", text="Plugin / Description")
        self.tree.heading("type", text="Format")
        self.tree.heading("path", text="Full Path")

        self.tree.column("#0", width=300, anchor=tk.W)
        self.tree.column("type", width=120, anchor=tk.W)
        self.tree.column("path", width=580, anchor=tk.W)

        # ****** CORRECTED CODE IS HERE ******
        # Custom tag for the description row, configured on the tree itself.
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

    def populate_tree(self, plugins):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        sorted_plugin_names = sorted(plugins.keys(), key=lambda s: s.lower())
        
        for name in sorted_plugin_names:
            parent_id = self.tree.insert("", tk.END, text=name, open=False, tags=('group',))
            
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

    def scan_and_display_plugins(self):
        plugins = self.scan_plugins()
        self.populate_tree(plugins)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            self.delete_button.config(state=tk.DISABLED)
            return

        item_id = selected_item[0]
        item_tags = self.tree.item(item_id, "tags")

        if 'plugin_file' in item_tags:
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.delete_button.config(state=tk.DISABLED)

    def delete_selected_plugin(self):
        selected_item = self.tree.selection()
        if not selected_item: return

        item_id = selected_item[0]
        item_tags = self.tree.item(item_id, "tags")

        if 'plugin_file' not in item_tags:
            messagebox.showwarning("Selection Error", "You can only delete plugin files, not descriptions or group names.")
            return

        item_details = self.tree.item(item_id)
        plugin_path_str = item_details["values"][1]
        
        confirmed = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to permanently delete this file?\n\n{plugin_path_str}"
        )
        if not confirmed: return

        plugin_path = pathlib.Path(plugin_path_str)
        user_home_path = pathlib.Path.home()

        try:
            if plugin_path.is_relative_to(user_home_path):
                self.status_label.config(text=f"Deleting user plugin...")
                self.update_idletasks()
                if plugin_path.is_dir(): shutil.rmtree(plugin_path)
                else: os.remove(plugin_path)
                messagebox.showinfo("Success", f"Successfully deleted (no password needed):\n{plugin_path_str}")
            else:
                self.status_label.config(text=f"Deleting system plugin... Password may be required.")
                self.update_idletasks()
                script = f'do shell script "rm -rf \\"{plugin_path_str}\\"" with administrator privileges'
                result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)

                if result.returncode == 0:
                    messagebox.showinfo("Success", f"Successfully deleted:\n{plugin_path_str}")
                else:
                    error_message = result.stderr.strip()
                    if "User canceled" in error_message: raise RuntimeError("Deletion was cancelled by user.")
                    else: raise RuntimeError(f"Deletion failed:\n\n{error_message}")
            
            self.scan_and_display_plugins()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="An error occurred during deletion.")


if __name__ == "__main__":
    app = PluginManager()
    app.mainloop()