import re
import threading
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from Inputs.inputFromSheets import inputFromSheets
from runAlgorithm import ALGORITHMS, run_selected_algorithm

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


def _person_cell(person: object, person_score: float | None) -> str:
    person_id = getattr(person, "id", str(person))
    score_part = "" if person_score is None else f" [{round(person_score, 2)}]"
    return f"{person_id}{score_part}"


def _split_table_like_value_calc(table: list[object], scores: list[float | None]) -> tuple[list[object], list[object], list[float | None], list[float | None]]:
    # Keep the same index split used by ValueCalc/printer: top is [:len//2], bottom is [len//2:]
    split_index = len(table) // 2
    return table[:split_index], table[split_index:], scores[:split_index], scores[split_index:]


def format_result_text(result: dict, show_scores: bool) -> str:
    total_score = f"{result['total_value']}" if show_scores else "hidden"
    lines = [
        f"Algorithm: {result['algorithm']}",
        f"People: {result['people_count']}",
        f"Total score: {total_score}",
        "",
        "Pretty arrangement:",
    ]

    for index, table in enumerate(result["arrangement"], start=1):
        table_score = None
        people_scores = [None] * len(table)
        if show_scores:
            table_score = round(result["table_values"][index - 1], 2)
            people_scores = [round(v, 2) for v in result["people_values"][index - 1]]

        table_header = f"Table {index} ({len(table)} seats)"
        if table_score is not None:
            table_header += f"  score={table_score}"
        lines.append(table_header)

        if not table:
            lines.append("  [empty]")
            lines.append("")
            continue

        top_side, bottom_side, top_scores, bottom_scores = _split_table_like_value_calc(table, people_scores)

        top_cells = [_person_cell(person, score if show_scores else None) for person, score in zip(top_side, top_scores)]
        bottom_cells = [_person_cell(person, score if show_scores else None) for person, score in zip(bottom_side, bottom_scores)]

        column_count = max(len(top_cells), len(bottom_cells))
        width = max(14, max(len(cell) for cell in top_cells + bottom_cells))
        divider = "  +" + "+".join("-" * (width + 2) for _ in range(column_count)) + "+"

        def _row(cells: list[str]) -> str:
            padded = cells + [""] * (column_count - len(cells))
            return "  |" + "|".join(f" {cell:<{width}} " for cell in padded) + "|"

        lines.append("  Side A")
        lines.append(divider)
        lines.append(_row(top_cells))
        lines.append(divider)
        lines.append("  Side B")
        lines.append(_row(bottom_cells))
        lines.append(divider)
        lines.append("")

    return "\n".join(lines)


class SeatingApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Seating Arrangement Runner")
        self.root.geometry("900x560")

        self.algorithm_names = [str(name) for name in sorted(ALGORITHMS)]

        self.file_path_var = tk.StringVar()
        self.algorithm_var = tk.StringVar(value=self.algorithm_names[0])
        self.table_sizes_var = tk.StringVar(value="8,8")
        self.status_var = tk.StringVar(value="Ready")
        self.show_scores_var = tk.BooleanVar(value=True)
        self.last_result: dict | None = None
        self.last_source_xlsx = ""

        self.run_button: ttk.Button
        self.meta_box: ScrolledText
        self.tables_canvas: tk.Canvas
        self.tables_frame: ttk.Frame
        self._tables_window_id: int
        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Google Sheets file (.xlsx)").grid(row=0, column=0, sticky="w")
        file_entry = ttk.Entry(frame, textvariable=self.file_path_var, width=86)
        file_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(frame, text="Browse", command=self._browse_file).grid(row=1, column=1, sticky="ew")

        ttk.Label(frame, text="Algorithm").grid(row=2, column=0, sticky="w", pady=(12, 0))
        algorithm_box = ttk.Combobox(
            frame,
            textvariable=self.algorithm_var,
            values=self.algorithm_names,
            state="readonly",
            width=50,
        )
        algorithm_box.grid(row=3, column=0, sticky="w")

        ttk.Label(frame, text="Empty arrangement (single size: 8, or list: 8,8,6)").grid(row=4, column=0, sticky="w", pady=(12, 0))
        ttk.Entry(frame, textvariable=self.table_sizes_var, width=50).grid(row=5, column=0, sticky="w")

        ttk.Checkbutton(
            frame,
            text="Show scores",
            variable=self.show_scores_var,
            command=self._refresh_output,
        ).grid(row=5, column=1, sticky="e")

        self.run_button = ttk.Button(frame, text="Convert + Run", command=self._run_clicked)
        self.run_button.grid(row=6, column=0, sticky="w", pady=(14, 0))

        ttk.Label(frame, textvariable=self.status_var).grid(row=6, column=1, sticky="e", pady=(14, 0))

        self.meta_box = ScrolledText(frame, wrap=tk.WORD, height=6)
        self.meta_box.configure(font=("Consolas", 10))
        self.meta_box.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        tables_outer = ttk.Frame(frame)
        tables_outer.grid(row=8, column=0, columnspan=2, sticky="nsew", pady=(10, 0))

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
        frame.rowconfigure(8, weight=1)

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
            algorithm_name = self.algorithm_var.get().strip()

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
                single_size = arrangement_value
                result = run_selected_algorithm(
                    algorithm_name,
                    people_payload,
                    attribute_payload,
                    default_table_size=single_size,
                )
            elif arrangement_mode == "list" and isinstance(arrangement_value, list):
                size_list = [int(value) for value in arrangement_value]
                result = run_selected_algorithm(
                    algorithm_name,
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

        result_text = format_result_text(self.last_result, self.show_scores_var.get())
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


