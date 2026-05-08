"""HD Tattoo Brush UI Components for GIMP 3.0

Provides GTK4 UI components for brush selection, preview, and management.
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib
from typing import Callable, Optional, List
from brushes.brush_manager import HDTattooBrush, BrushManager, BrushCategory


class BrushPreviewCanvas(Gtk.DrawingArea):
    """Canvas for previewing brush strokes."""

    def __init__(self):
        super().__init__()
        self.set_size_request(200, 200)
        self.set_css_classes(["brush-preview"])
        self.brush: Optional[HDTattooBrush] = None
        self.connect("draw", self._on_draw)

    def set_brush(self, brush: HDTattooBrush) -> None:
        """Set the brush to preview.
        
        Args:
            brush: Brush to preview
        """
        self.brush = brush
        self.queue_draw()

    def _on_draw(self, widget, ctx):
        """Draw brush preview."""
        if not self.brush:
            return False

        width = widget.get_width()
        height = widget.get_height()

        # Background
        ctx.set_source_rgb(0.95, 0.95, 0.95)
        ctx.paint()

        # Grid
        ctx.set_source_rgb(0.9, 0.9, 0.9)
        ctx.set_line_width(0.5)
        for i in range(0, width, 20):
            ctx.move_to(i, 0)
            ctx.line_to(i, height)
        for i in range(0, height, 20):
            ctx.move_to(0, i)
            ctx.line_to(width, i)
        ctx.stroke()

        # Sample strokes
        ctx.set_source_rgb(0.2, 0.2, 0.2)
        brush = self.brush

        # Vertical stroke
        ctx.set_line_width(max(1, brush.size_range[0]))
        ctx.move_to(50, 30)
        ctx.line_to(50, 170)
        ctx.stroke()

        # Horizontal stroke
        ctx.set_line_width(max(1, brush.size_range[0] * 1.5))
        ctx.move_to(90, 100)
        ctx.line_to(190, 100)
        ctx.stroke()

        # Diagonal stroke
        ctx.set_line_width(max(1, brush.size_range[0] * 0.8))
        ctx.move_to(100, 30)
        ctx.line_to(180, 170)
        ctx.stroke()

        return False


class BrushPropertyPanel(Gtk.Box):
    """Panel for displaying and editing brush properties."""

    def __init__(self, on_property_changed: Optional[Callable] = None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_margin_start(10)
        self.set_margin_end(10)

        self.on_property_changed = on_property_changed
        self.brush: Optional[HDTattooBrush] = None
        self.property_widgets: dict = {}

    def set_brush(self, brush: HDTattooBrush) -> None:
        """Set the brush to display properties for.
        
        Args:
            brush: Brush to display
        """
        self.brush = brush
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the property UI."""
        # Clear existing
        for child in list(self):
            self.remove(child)
        self.property_widgets.clear()

        if not self.brush:
            return

        # Title
        title = Gtk.Label(label=self.brush.name)
        title.set_css_classes(["title", "heading"])
        self.append(title)

        # Description
        desc = Gtk.Label(label=self.brush.description)
        desc.set_wrap(True)
        desc.set_css_classes(["description"])
        self.append(desc)

        # Size range
        size_box = self._create_labeled_row("Size Range:")
        size_label = Gtk.Label(
            label=f"{self.brush.size_range[0]:.1f} - {self.brush.size_range[1]:.1f}px"
        )
        size_box.append(size_label)
        self.append(size_box)

        # Opacity range
        opacity_box = self._create_labeled_row("Opacity Range:")
        opacity_label = Gtk.Label(
            label=f"{self.brush.opacity_range[0]:.0%} - {self.brush.opacity_range[1]:.0%}"
        )
        opacity_box.append(opacity_label)
        self.append(opacity_box)

        # Hardness
        hardness_box = self._create_labeled_row("Hardness:", show_slider=True)
        hardness_scale = Gtk.Scale(
            adjustment=Gtk.Adjustment(
                value=self.brush.hardness, lower=0, upper=1,
                step_increment=0.01, page_increment=0.1
            ),
            orientation=Gtk.Orientation.HORIZONTAL
        )
        hardness_scale.set_draw_value(True)
        hardness_scale.set_digits(2)
        hardness_box.append(hardness_scale)
        self.property_widgets['hardness'] = hardness_scale
        self.append(hardness_box)

        # Spacing
        spacing_box = self._create_labeled_row("Spacing:", show_slider=True)
        spacing_scale = Gtk.Scale(
            adjustment=Gtk.Adjustment(
                value=self.brush.spacing, lower=0, upper=1,
                step_increment=0.01, page_increment=0.1
            ),
            orientation=Gtk.Orientation.HORIZONTAL
        )
        spacing_scale.set_draw_value(True)
        spacing_scale.set_digits(2)
        spacing_box.append(spacing_scale)
        self.property_widgets['spacing'] = spacing_scale
        self.append(spacing_box)

        # Jitter
        jitter_box = self._create_labeled_row("Jitter:", show_slider=True)
        jitter_scale = Gtk.Scale(
            adjustment=Gtk.Adjustment(
                value=self.brush.jitter_amount, lower=0, upper=1,
                step_increment=0.01, page_increment=0.1
            ),
            orientation=Gtk.Orientation.HORIZONTAL
        )
        jitter_scale.set_draw_value(True)
        jitter_scale.set_digits(2)
        jitter_box.append(jitter_scale)
        self.property_widgets['jitter'] = jitter_scale
        self.append(jitter_box)

        # Smoothing
        smoothing_box = self._create_labeled_row("Smoothing:", show_slider=True)
        smoothing_scale = Gtk.Scale(
            adjustment=Gtk.Adjustment(
                value=self.brush.smoothing, lower=0, upper=1,
                step_increment=0.01, page_increment=0.1
            ),
            orientation=Gtk.Orientation.HORIZONTAL
        )
        smoothing_scale.set_draw_value(True)
        smoothing_scale.set_digits(2)
        smoothing_box.append(smoothing_scale)
        self.property_widgets['smoothing'] = smoothing_scale
        self.append(smoothing_box)

        # Texture depth
        texture_box = self._create_labeled_row("Texture Depth:", show_slider=True)
        texture_scale = Gtk.Scale(
            adjustment=Gtk.Adjustment(
                value=self.brush.texture_depth, lower=0, upper=1,
                step_increment=0.01, page_increment=0.1
            ),
            orientation=Gtk.Orientation.HORIZONTAL
        )
        texture_scale.set_draw_value(True)
        texture_scale.set_digits(2)
        texture_box.append(texture_scale)
        self.property_widgets['texture'] = texture_scale
        self.append(texture_box)

        # Toggles
        toggle_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        toggle_box.set_margin_top(10)

        for attr, label in [
            ('color_dynamics', 'Color Dynamics'),
            ('pressure_sensitivity', 'Pressure Sensitivity'),
            ('tilt_sensitivity', 'Tilt Sensitivity'),
            ('velocity_sensitivity', 'Velocity Sensitivity')
        ]:
            toggle = Gtk.CheckButton(label=label)
            toggle.set_active(getattr(self.brush, attr))
            toggle_box.append(toggle)
            self.property_widgets[attr] = toggle

        self.append(toggle_box)

        # Tags
        if self.brush.tags:
            tags_label = Gtk.Label(label="Tags:")
            tags_label.set_css_classes(["heading"])
            self.append(tags_label)
            tags_flow = Gtk.FlowBox()
            tags_flow.set_selection_mode(Gtk.SelectionMode.NONE)
            for tag in self.brush.tags:
                tag_btn = Gtk.Button(label=tag)
                tag_btn.set_css_classes(["tag"])
                tags_flow.append(tag_btn)
            self.append(tags_flow)

    def _create_labeled_row(self, label_text: str,
                          show_slider: bool = False) -> Gtk.Box:
        """Create a labeled row for properties.
        
        Args:
            label_text: Text for the label
            show_slider: Whether this row contains a slider
            
        Returns:
            A Box containing the label and space for content
        """
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL
            if show_slider else Gtk.Orientation.HORIZONTAL,
            spacing=5
        )
        label = Gtk.Label(label=label_text)
        label.set_xalign(0.0)
        box.append(label)
        return box

    def get_property_values(self) -> dict:
        """Get current property values.
        
        Returns:
            Dictionary of property values
        """
        values = {}
        for prop, widget in self.property_widgets.items():
            if isinstance(widget, Gtk.Scale):
                values[prop] = widget.get_adjustment().get_value()
            elif isinstance(widget, Gtk.CheckButton):
                values[prop] = widget.get_active()
        return values


class BrushCategorySelector(Gtk.Box):
    """Selector for brush categories."""

    def __init__(self, on_category_selected: Callable,
                 brush_manager: BrushManager):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.set_margin_top(5)
        self.set_margin_bottom(5)
        self.set_margin_start(5)
        self.set_margin_end(5)
        self.set_homogeneous(False)

        self.on_category_selected = on_category_selected
        self.brush_manager = brush_manager
        self.buttons: dict = {}

        # Create buttons for each category
        for category in brush_manager.get_brush_categories():
            btn = Gtk.ToggleButton(label=category.capitalize())
            btn.connect("toggled", self._on_category_toggled, category)
            self.buttons[category] = btn
            self.append(btn)

    def _on_category_toggled(self, button: Gtk.ToggleButton,
                            category: str) -> None:
        """Handle category button toggle."""
        if button.get_active():
            # Deactivate other buttons
            for cat, btn in self.buttons.items():
                if cat != category:
                    btn.set_active(False)
            self.on_category_selected(category)

    def get_selected_category(self) -> Optional[str]:
        """Get the currently selected category.
        
        Returns:
            Category name or None
        """
        for category, btn in self.buttons.items():
            if btn.get_active():
                return category
        return None


class BrushLibraryPanel(Gtk.Box):
    """Panel showing brush library with scroll."""

    def __init__(self, brush_manager: BrushManager,
                 on_brush_selected: Callable):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.brush_manager = brush_manager
        self.on_brush_selected = on_brush_selected

        # Search box
        search_box = Gtk.SearchEntry()
        search_box.set_placeholder_text("Search brushes...")
        search_box.connect("search-changed", self._on_search_changed)
        self.append(search_box)
        self.search_entry = search_box

        # Category selector
        self.category_selector = BrushCategorySelector(
            self._on_category_selected, brush_manager
        )
        self.append(self.category_selector)

        # Scrolled window for brush list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)

        self.brush_list = Gtk.ListBox()
        self.brush_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.brush_list.connect("row-selected", self._on_brush_row_selected)
        scrolled.set_child(self.brush_list)

        self.append(scrolled)
        self._populate_brush_list()

    def _populate_brush_list(self, brushes: Optional[List[HDTattooBrush]] = None) -> None:
        """Populate the brush list.
        
        Args:
            brushes: List of brushes to show, or None for all
        """
        # Clear existing
        for child in list(self.brush_list):
            self.brush_list.remove(child)

        if brushes is None:
            brushes = self.brush_manager.get_all_brushes()

        for brush in sorted(brushes, key=lambda b: b.name):
            row = self._create_brush_row(brush)
            self.brush_list.append(row)

    def _create_brush_row(self, brush: HDTattooBrush) -> Gtk.ListBoxRow:
        """Create a list box row for a brush.
        
        Args:
            brush: Brush to create row for
            
        Returns:
            A ListBoxRow
        """
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        box.set_margin_top(5)
        box.set_margin_bottom(5)
        box.set_margin_start(10)
        box.set_margin_end(10)

        name_label = Gtk.Label(label=brush.name, xalign=0.0)
        name_label.set_css_classes(["heading"])
        box.append(name_label)

        desc_label = Gtk.Label(label=brush.description, xalign=0.0)
        desc_label.set_wrap(True)
        desc_label.set_css_classes(["dim-label"])
        box.append(desc_label)

        row.set_child(box)
        row.brush = brush  # Attach brush to row
        return row

    def _on_brush_row_selected(self, listbox: Gtk.ListBox,
                              row: Optional[Gtk.ListBoxRow]) -> None:
        """Handle brush row selection."""
        if row and hasattr(row, 'brush'):
            self.on_brush_selected(row.brush)

    def _on_search_changed(self, entry: Gtk.SearchEntry) -> None:
        """Handle search text change."""
        query = entry.get_text()
        if query:
            brushes = self.brush_manager.search_brushes(query)
        else:
            brushes = None
        self._populate_brush_list(brushes)

    def _on_category_selected(self, category: str) -> None:
        """Handle category selection."""
        brushes = self.brush_manager.get_brushes_by_category(category)
        self._populate_brush_list(brushes)
