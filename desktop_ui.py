import re
import threading
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from Inputs.inputFromSheets import inputFromSheets
from runAlgorithm import (
    ALGORITHMS,
    BUILD_ALGORITHMS,
    DISRUPTION_ALGORITHMS,
    OPTIMIZING_ALGORITHMS,
    run_composite_pipeline,
    run_selected_algorithm,
)

TABLE_SIZE_SPLIT = re.compile(r"[,;\s]+")


def parse_table_sizes(raw_value: str) -> tuple[str, int | list[int]]:
    values = [part.strip() for part in TABLE_SIZE_SPLIT.split(raw_value.strip()) if part.strip()]
    if not values:
        raise ValueError("Please add table size input, e.g. 8 or 8,8,6")

    table_sizes: list[int] = []
    for value in values:
        try:
            size = int(value)
        except ValueError as error:
            raise ValueError(f"Invalid table size '{value}'. Use positive integers.") from error
        if size <= 0:
            raise ValueError("Table sizes must be positive integers")
        table_sizes.append(size)

    if len(table_sizes) == 1:
        return "single", table_sizes[0]
    return "list", table_sizes


def _split_table_like_value_calc(table: list[object], scores: list[float | None]) -> tuple[list[object], list[object], list[float | None], list[float | None]]:
    # Keep the same index split used by ValueCalc/printer: top is [:len//2], bottom is [len//2:]
    split_index = len(table) // 2
    return table[:split_index], table[split_index:], scores[:split_index], scores[split_index:]


def format_result_summary(result: dict, show_scores: bool) -> str:
    lines = []
    if "build_algorithm" in result:
        stages = result.get("stages", [])
        lines.append(f"Mode: custom pipeline")
        lines.append(f"Build: {result['build_algorithm']}")
        lines.append(f"Stages: {', '.join(stages) if stages else '(none)'}")
    else:
        lines.append("Mode: standard algorithm")
        lines.append(f"Algorithm: {result['algorithm']}")

    lines.append(f"People: {result['people_count']}")
    lines.append(f"Total score: {round(float(result['total_value']), 2) if show_scores else 'hidden'}")
    lines.append(f"Tables: {len(result.get('arrangement', []))}")
    return "\n".join(lines)


class SeatingApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Seating Arrangement Runner")
        self.root.geometry("900x560")

        self.build_algorithm_names = [str(name) for name in sorted(BUILD_ALGORITHMS)]
        self.optimizing_algorithm_names = [str(name) for name in sorted(OPTIMIZING_ALGORITHMS)]
        self.disruption_algorithm_names = [str(name) for name in sorted(DISRUPTION_ALGORITHMS)]
        self.standard_algorithm_names = [str(name) for name in sorted(ALGORITHMS)]
        self.algorithm_picker_names = self.standard_algorithm_names + ["buildOwn"]
        self.available_stage_items: list[dict[str, str]] = []
        for name in self.optimizing_algorithm_names:
            self.available_stage_items.append({"category": "optimizing", "name": name})
        for name in self.disruption_algorithm_names:
            self.available_stage_items.append({"category": "disruption", "name": name})

        self.file_path_var = tk.StringVar()
        default_selected_algorithm = self.algorithm_picker_names[0] if self.algorithm_picker_names else "buildOwn"
        self.selected_algorithm_var = tk.StringVar(value=default_selected_algorithm)
        self.build_algorithm_var = tk.StringVar(value=self.build_algorithm_names[0])
        self.table_sizes_var = tk.StringVar(value="8")
        self.status_var = tk.StringVar(value="Ready")
        self.show_scores_var = tk.BooleanVar(value=True)
        self.last_result: dict | None = None
        self.last_source_xlsx = ""
        self.pipeline_items: list[dict[str, str]] = []

        self.run_button: ttk.Button
        self.meta_box: ScrolledText
        self.tables_canvas: tk.Canvas
        self.tables_frame: ttk.Frame
        self.algorithm_picker_box: ttk.Combobox
        self.build_algorithm_box: ttk.Combobox
        self.available_stages_listbox: tk.Listbox
        self.pipeline_listbox: tk.Listbox
        self.pipeline_remove_button: ttk.Button
        self.custom_frame: ttk.LabelFrame
        self._tables_window_id: int
        self._drag_item: dict[str, str] | None = None
        self._drag_source: str | None = None
        self._drag_index: int | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Google Sheets file (.xlsx)").grid(row=0, column=0, sticky="w")
        file_entry = ttk.Entry(frame, textvariable=self.file_path_var, width=86)
        file_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(frame, text="Browse", command=self._browse_file).grid(row=1, column=1, sticky="ew")

        algorithm_frame = ttk.LabelFrame(frame, text="Algorithm", padding=10)
        algorithm_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        ttk.Label(algorithm_frame, text="Pick one algorithm (choose 'buildOwn' to build a custom composite)").grid(row=0, column=0, sticky="w")
        self.algorithm_picker_box = ttk.Combobox(
            algorithm_frame,
            textvariable=self.selected_algorithm_var,
            values=self.algorithm_picker_names,
            state="readonly",
            width=50,
        )
        self.algorithm_picker_box.grid(row=1, column=0, sticky="w")
        self.algorithm_picker_box.bind("<<ComboboxSelected>>", lambda _event: self._update_mode_ui())

        self.custom_frame = ttk.LabelFrame(frame, text="Custom pipeline builder", padding=10)
        self.custom_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(12, 0))

        ttk.Label(self.custom_frame, text="Build step").grid(row=0, column=0, sticky="w")
        self.build_algorithm_box = ttk.Combobox(
            self.custom_frame,
            textvariable=self.build_algorithm_var,
            values=self.build_algorithm_names,
            state="readonly",
            width=42,
        )
        self.build_algorithm_box.grid(row=1, column=0, sticky="w", pady=(4, 8))

        ttk.Label(self.custom_frame, text="Drag stages from here").grid(row=0, column=1, sticky="w")
        ttk.Label(self.custom_frame, text="Drop/reorder stages here").grid(row=0, column=3, sticky="w")

        self.available_stages_listbox = tk.Listbox(self.custom_frame, height=7, activestyle="dotbox", exportselection=False)
        available_scrollbar = ttk.Scrollbar(self.custom_frame, orient="vertical", command=self.available_stages_listbox.yview)
        self.available_stages_listbox.configure(yscrollcommand=available_scrollbar.set)
        self.available_stages_listbox.grid(row=1, column=1, sticky="nsew", padx=(12, 0))
        available_scrollbar.grid(row=1, column=2, sticky="ns")

        self.pipeline_listbox = tk.Listbox(self.custom_frame, height=7, activestyle="dotbox", exportselection=False)
        pipeline_scrollbar = ttk.Scrollbar(self.custom_frame, orient="vertical", command=self.pipeline_listbox.yview)
        self.pipeline_listbox.configure(yscrollcommand=pipeline_scrollbar.set)
        self.pipeline_listbox.grid(row=1, column=3, sticky="nsew", padx=(12, 0))
        pipeline_scrollbar.grid(row=1, column=4, sticky="ns")

        self.pipeline_remove_button = ttk.Button(self.custom_frame, text="Remove selected stage", command=self._remove_selected_stage)
        self.pipeline_remove_button.grid(row=2, column=3, sticky="w", pady=(8, 0), padx=(12, 0))

        ttk.Label(self.custom_frame, text="Tip: drag a stage into the right list. Drag inside the right list to reorder.").grid(
            row=2,
            column=1,
            sticky="w",
            pady=(8, 0),
            padx=(12, 0),
        )

        settings_frame = ttk.LabelFrame(frame, text="Input settings", padding=10)
        settings_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        ttk.Label(settings_frame, text="Empty arrangement (single size: 8, or list: 8,8,6)").grid(row=0, column=0, sticky="w")
        ttk.Entry(settings_frame, textvariable=self.table_sizes_var, width=50).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(
            settings_frame,
            text="Show scores",
            variable=self.show_scores_var,
            command=self._refresh_output,
        ).grid(row=1, column=1, sticky="e", padx=(12, 0))

        self.run_button = ttk.Button(frame, text="Build + Run", command=self._run_clicked)
        self.run_button.grid(row=5, column=0, sticky="w", pady=(14, 0))

        ttk.Label(frame, textvariable=self.status_var).grid(row=5, column=1, sticky="e", pady=(14, 0))

        self.meta_box = ScrolledText(frame, wrap=tk.WORD, height=6)
        self.meta_box.configure(font=("Consolas", 10))
        self.meta_box.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        tables_outer = ttk.Frame(frame)
        tables_outer.grid(row=7, column=0, columnspan=2, sticky="nsew", pady=(10, 0))

        self.tables_canvas = tk.Canvas(tables_outer, highlightthickness=0)
        vertical_scroll = ttk.Scrollbar(tables_outer, orient="vertical", command=self.tables_canvas.yview)
        self.tables_canvas.configure(yscrollcommand=vertical_scroll.set)

        self.tables_frame = ttk.Frame(self.tables_canvas)
        self._tables_window_id = self.tables_canvas.create_window((0, 0), window=self.tables_frame, anchor="nw")

        self.tables_canvas.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        tables_outer.columnconfigure(0, weight=1)
        tables_outer.rowconfigure(0, weight=1)

        self.tables_frame.bind("<Configure>", self._on_tables_frame_configure)
        self.tables_canvas.bind("<Configure>", self._on_tables_canvas_configure)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        frame.rowconfigure(7, weight=1)

        self.custom_frame.columnconfigure(1, weight=1)
        self.custom_frame.columnconfigure(3, weight=1)
        self.custom_frame.rowconfigure(1, weight=1)

        self.available_stages_listbox.bind("<ButtonPress-1>", self._on_available_drag_start)
        self.pipeline_listbox.bind("<ButtonPress-1>", self._on_pipeline_drag_start)
        self.available_stages_listbox.bind("<B1-Motion>", self._on_drag_motion)
        self.pipeline_listbox.bind("<B1-Motion>", self._on_drag_motion)
        self.root.bind_all("<ButtonRelease-1>", self._on_global_drop, add="+")

        self._refresh_available_stages_list()
        self._update_mode_ui()

    def _format_pipeline_item(self, item: dict[str, str]) -> str:
        return f"{item['category'].title()}: {item['name']}"

    def _refresh_available_stages_list(self) -> None:
        self.available_stages_listbox.delete(0, tk.END)
        for item in self.available_stage_items:
            self.available_stages_listbox.insert(tk.END, self._format_pipeline_item(item))

    def _refresh_pipeline_list(self) -> None:
        self.pipeline_listbox.delete(0, tk.END)
        for item in self.pipeline_items:
            self.pipeline_listbox.insert(tk.END, self._format_pipeline_item(item))

    def _update_mode_ui(self) -> None:
        is_build_own = self.selected_algorithm_var.get() == "buildOwn"
        if is_build_own:
            self.custom_frame.grid()
        else:
            self.custom_frame.grid_remove()

        self.build_algorithm_box.configure(state="readonly" if is_build_own else "disabled")
        self.available_stages_listbox.configure(state="normal" if is_build_own else "disabled")
        self.pipeline_listbox.configure(state="normal" if is_build_own else "disabled")
        self.pipeline_remove_button.configure(state=tk.NORMAL if is_build_own else tk.DISABLED)

    def _set_drag_state(self, source: str, index: int, item: dict[str, str]) -> None:
        self._drag_source = source
        self._drag_index = index
        self._drag_item = {"category": item["category"], "name": item["name"]}

    def _reset_drag_state(self) -> None:
        self._drag_source = None
        self._drag_index = None
        self._drag_item = None

    def _listbox_drop_index(self, listbox: tk.Listbox, local_y: int) -> int:
        size = listbox.size()
        if size == 0:
            return 0

        nearest_index = listbox.nearest(local_y)
        nearest_index = max(0, min(nearest_index, size - 1))
        bbox = listbox.bbox(nearest_index)
        if bbox and local_y > (bbox[1] + (bbox[3] // 2)):
            nearest_index += 1
        return max(0, min(nearest_index, size))

    def _on_available_drag_start(self, event: tk.Event) -> None:
        if self.selected_algorithm_var.get() != "buildOwn":
            return
        if self.available_stages_listbox.size() == 0:
            return

        index = self.available_stages_listbox.nearest(event.y)
        if index < 0 or index >= len(self.available_stage_items):
            return
        self.available_stages_listbox.selection_clear(0, tk.END)
        self.available_stages_listbox.selection_set(index)
        item = self.available_stage_items[index]
        if not isinstance(item, dict):
            return
        self._set_drag_state("available", index, item)

    def _on_pipeline_drag_start(self, event: tk.Event) -> None:
        if self.selected_algorithm_var.get() != "buildOwn":
            return
        if self.pipeline_listbox.size() == 0:
            return

        index = self.pipeline_listbox.nearest(event.y)
        if index < 0 or index >= len(self.pipeline_items):
            return
        self.pipeline_listbox.selection_clear(0, tk.END)
        self.pipeline_listbox.selection_set(index)
        item = self.pipeline_items[index]
        if not isinstance(item, dict):
            return
        self._set_drag_state("pipeline", index, item)

    def _on_drag_motion(self, event: tk.Event) -> None:
        if self.selected_algorithm_var.get() != "buildOwn":
            return
        if self._drag_item is None:
            return
        target = self.root.winfo_containing(event.x_root, event.y_root)
        if target is not self.pipeline_listbox:
            return
        local_y = event.y_root - self.pipeline_listbox.winfo_rooty()
        size = self.pipeline_listbox.size()
        if size <= 0:
            self.pipeline_listbox.selection_clear(0, tk.END)
            return
        index = self._listbox_drop_index(self.pipeline_listbox, local_y)
        highlight_index = min(index, size - 1)
        self.pipeline_listbox.selection_clear(0, tk.END)
        self.pipeline_listbox.selection_set(highlight_index)

    def _on_global_drop(self, event: tk.Event) -> None:
        if self._drag_item is None:
            return
        if self.selected_algorithm_var.get() != "buildOwn":
            self._reset_drag_state()
            return

        target = self.root.winfo_containing(event.x_root, event.y_root)
        if target is not self.pipeline_listbox:
            self._reset_drag_state()
            return

        local_y = event.y_root - self.pipeline_listbox.winfo_rooty()
        drop_index = self._listbox_drop_index(self.pipeline_listbox, local_y)

        if self._drag_source == "available":
            self.pipeline_items.insert(drop_index, {"category": self._drag_item["category"], "name": self._drag_item["name"]})
            selected_index = drop_index
        elif self._drag_source == "pipeline" and self._drag_index is not None and 0 <= self._drag_index < len(self.pipeline_items):
            item = self.pipeline_items.pop(self._drag_index)
            if drop_index > self._drag_index:
                drop_index -= 1
            drop_index = max(0, min(drop_index, len(self.pipeline_items)))
            self.pipeline_items.insert(drop_index, item)
            selected_index = drop_index
        else:
            self._reset_drag_state()
            return

        self._refresh_pipeline_list()
        self.pipeline_listbox.selection_clear(0, tk.END)
        self.pipeline_listbox.selection_set(selected_index)
        self.pipeline_listbox.see(selected_index)
        self._reset_drag_state()

    def _selected_pipeline_index(self) -> int | None:
        selection = self.pipeline_listbox.curselection()
        if not selection:
            return None
        return int(selection[0])

    def _remove_selected_stage(self) -> None:
        index = self._selected_pipeline_index()
        if index is None:
            return
        del self.pipeline_items[index]
        self._refresh_pipeline_list()
        if self.pipeline_items:
            new_index = min(index, len(self.pipeline_items) - 1)
            self.pipeline_listbox.selection_set(new_index)
            self.pipeline_listbox.see(new_index)

    def _browse_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select .xlsx file",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        )
        if file_path:
            self.file_path_var.set(file_path)

    def _run_clicked(self) -> None:
        self.run_button.configure(state=tk.DISABLED)
        self.status_var.set("Running...")
        self.last_result = None
        self.meta_box.delete("1.0", tk.END)
        self._clear_tables()
        threading.Thread(target=self._run_workflow, daemon=True).start()

    def _run_workflow(self) -> None:
        try:
            xlsx_path = Path(self.file_path_var.get().strip())
            if not xlsx_path.exists():
                raise FileNotFoundError("Selected .xlsx file was not found")

            arrangement_mode, arrangement_value = parse_table_sizes(self.table_sizes_var.get())
            selected_algorithm = self.selected_algorithm_var.get().strip()
            build_algorithm_name = self.build_algorithm_var.get().strip()
            stage_names = [item["name"] for item in self.pipeline_items]

            sheet_result = inputFromSheets(xlsx_path, write_output=False)
            people_payload = {
                "schema_version": 1,
                "people": sheet_result.get("people", []),
            }
            attribute_payload = {
                "schema_version": 1,
                "attribute_set": sheet_result.get("attribute_set", []),
            }

            if arrangement_mode == "single" and isinstance(arrangement_value, int):
                if selected_algorithm != "buildOwn":
                    result = run_selected_algorithm(
                        selected_algorithm,
                        people_payload,
                        attribute_payload,
                        default_table_size=arrangement_value,
                    )
                else:
                    result = run_composite_pipeline(
                        build_algorithm_name,
                        stage_names,
                        people_payload,
                        attribute_payload,
                        default_table_size=arrangement_value,
                    )
            elif arrangement_mode == "list" and isinstance(arrangement_value, list):
                size_list = [int(value) for value in arrangement_value]
                if selected_algorithm != "buildOwn":
                    result = run_selected_algorithm(
                        selected_algorithm,
                        people_payload,
                        attribute_payload,
                        table_sizes=size_list,
                    )
                else:
                    result = run_composite_pipeline(
                        build_algorithm_name,
                        stage_names,
                        people_payload,
                        attribute_payload,
                        table_sizes=size_list,
                    )
            else:
                raise ValueError("Invalid table size input mode")

            self.root.after(0, self._on_success, result, str(xlsx_path))
        except Exception as error:
            details = "".join(traceback.format_exception_only(type(error), error)).strip()
            self.root.after(0, self._on_failure, details)

    def _on_success(self, result: dict, source_xlsx: str) -> None:
        self.last_result = result
        self.last_source_xlsx = source_xlsx
        self._refresh_output()
        self.status_var.set("Done")
        self.run_button.configure(state=tk.NORMAL)

    def _refresh_output(self) -> None:
        if self.last_result is None:
            return

        result_text = format_result_summary(self.last_result, self.show_scores_var.get())
        self.meta_box.delete("1.0", tk.END)
        self.meta_box.insert(
            tk.END,
            f"Input source: {self.last_source_xlsx}\nMode: in-memory conversion (no JSON files written)\n\n{result_text}\n",
        )
        self._render_tables(self.last_result, self.show_scores_var.get())

    def _on_tables_frame_configure(self, _event: tk.Event) -> None:
        self.tables_canvas.configure(scrollregion=self.tables_canvas.bbox("all"))

    def _on_tables_canvas_configure(self, event: tk.Event) -> None:
        self.tables_canvas.itemconfig(self._tables_window_id, width=event.width)

    def _clear_tables(self) -> None:
        for child in self.tables_frame.winfo_children():
            child.destroy()

    def _seat_text(self, person: object, score: float | None, show_scores: bool) -> tuple[str, bool]:
        person_id = str(getattr(person, "id", str(person)))
        is_empty = person_id.lower() == "empty"
        if show_scores and score is not None:
            return f"{person_id}\n{round(score, 2)}", is_empty
        return person_id, is_empty

    def _render_tables(self, result: dict, show_scores: bool) -> None:
        self._clear_tables()

        occupied_bg = "#e6ecf5"
        empty_bg = "#d0d0d0"
        occupied_fg = "#111111"
        empty_fg = "#666666"

        for table_index, table in enumerate(result["arrangement"], start=1):
            table_score = None
            people_scores: list[float | None] = [None] * len(table)
            if show_scores:
                table_score = float(result["table_values"][table_index - 1])
                people_scores = [float(v) for v in result["people_values"][table_index - 1]]

            header = f"Table {table_index} ({len(table)} seats)"
            if table_score is not None:
                header += f"  score={round(table_score, 2)}"

            card = ttk.LabelFrame(self.tables_frame, text=header, padding=10)
            card.grid(row=table_index - 1, column=0, sticky="ew", padx=4, pady=6)
            card.columnconfigure(1, weight=1)

            if not table:
                ttk.Label(card, text="[empty]").grid(row=0, column=0, sticky="w")
                continue

            top_side, bottom_side, top_scores, bottom_scores = _split_table_like_value_calc(table, people_scores)
            column_count = max(len(top_side), len(bottom_side))

            for col in range(column_count):
                if col < len(top_side):
                    label_text, is_empty = self._seat_text(top_side[col], top_scores[col], show_scores)
                else:
                    label_text, is_empty = "", True
                seat_bg = empty_bg if is_empty else occupied_bg
                seat_fg = empty_fg if is_empty else occupied_fg
                seat = tk.Label(
                    card,
                    text=label_text,
                    relief="ridge",
                    bd=1,
                    padx=8,
                    pady=6,
                    bg=seat_bg,
                    fg=seat_fg,
                    justify="center",
                )
                seat.grid(row=0, column=col + 1, sticky="nsew", padx=3, pady=(0, 4))
                card.columnconfigure(col + 1, weight=1)

            table_surface = tk.Canvas(card, height=28, highlightthickness=1, highlightbackground="#8b6f47", bg="#dac3a3")
            table_surface.grid(row=1, column=1, columnspan=column_count, sticky="ew", padx=3, pady=(2, 6))
            table_surface.create_text(8, 14, text="table", anchor="w", fill="#5a4630")

            for col in range(column_count):
                if col < len(bottom_side):
                    label_text, is_empty = self._seat_text(bottom_side[col], bottom_scores[col], show_scores)
                else:
                    label_text, is_empty = "", True
                seat_bg = empty_bg if is_empty else occupied_bg
                seat_fg = empty_fg if is_empty else occupied_fg
                seat = tk.Label(
                    card,
                    text=label_text,
                    relief="ridge",
                    bd=1,
                    padx=8,
                    pady=6,
                    bg=seat_bg,
                    fg=seat_fg,
                    justify="center",
                )
                seat.grid(row=2, column=col + 1, sticky="nsew", padx=3, pady=(0, 2))

    def _on_failure(self, error_message: str) -> None:
        self.status_var.set("Failed")
        self.run_button.configure(state=tk.NORMAL)
        messagebox.showerror("Run failed", error_message)


def main() -> None:
    root = tk.Tk()
    app = SeatingApp(root)
    root.minsize(760, 460)
    root.mainloop()


if __name__ == "__main__":
    main()


