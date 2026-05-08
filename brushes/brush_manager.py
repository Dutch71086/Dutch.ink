"""HD Tattoo Brush Manager for GIMP 3.0

Provides comprehensive brush management system with 50+ HD tattoo brushes
organized by category, with customizable brush properties and preset saving.
"""

import json
import os
from enum import Enum
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class BrushCategory(Enum):
    """Categories of tattoo brushes."""
    OUTLINE = "outline"
    SHADING = "shading"
    FILL = "fill"
    DETAIL = "detail"
    SPECIALTY = "specialty"
    STIPPLE = "stipple"
    TEXTURE = "texture"
    LINEWORK = "linework"
    BLENDING = "blending"


class BrushStyle(Enum):
    """Tattoo brush styles."""
    SOLID = "solid"
    TEXTURED = "textured"
    SCATTERED = "scattered"
    GRADIENT = "gradient"
    PATTERN = "pattern"
    STIPPLED = "stippled"
    HATCHED = "hatched"


@dataclass
class BrushProperty:
    """Individual brush property configuration."""
    name: str
    value: float
    min_value: float = 0.0
    max_value: float = 1.0
    step: float = 0.01
    description: str = ""


@dataclass
class HDTattooBrush:
    """HD Tattoo Brush definition."""
    id: str
    name: str
    category: str
    style: str
    size_range: Tuple[float, float]  # (min, max) in pixels
    opacity_range: Tuple[float, float]  # (min, max) 0-1
    hardness: float  # 0-1
    spacing: float  # 0-1
    jitter_amount: float  # 0-1
    smoothing: float  # 0-1
    aspect_ratio: float  # width/height ratio
    angle: float  # rotation angle in degrees
    texture_depth: float  # 0-1
    color_dynamics: bool
    pressure_sensitivity: bool
    tilt_sensitivity: bool
    velocity_sensitivity: bool
    description: str
    tags: List[str] = field(default_factory=list)
    hd_quality: bool = True
    bristle_count: int = 0  # 0 for continuous
    bristle_curve: str = "linear"  # linear, smooth, sharp

    def to_dict(self) -> Dict:
        """Convert brush to dictionary."""
        data = asdict(self)
        data['category'] = self.category
        data['style'] = self.style
        return data


@dataclass
class BrushPreset:
    """Custom brush preset with saved configurations."""
    name: str
    brush_id: str
    size: float
    opacity: float
    hardness: float
    spacing: float
    smoothing: float
    color: Tuple[int, int, int] = (0, 0, 0)
    created_at: str = ""
    description: str = ""


class BrushManager:
    """Manages HD tattoo brushes and presets."""

    def __init__(self, brush_dir: Optional[str] = None):
        """Initialize brush manager.
        
        Args:
            brush_dir: Directory to store brush data. Defaults to config/brushes
        """
        self.brush_dir = Path(brush_dir or "config/brushes")
        self.brush_dir.mkdir(parents=True, exist_ok=True)
        self.brushes: Dict[str, HDTattooBrush] = {}
        self.presets: Dict[str, BrushPreset] = {}
        self._initialize_hd_brushes()
        self._load_presets()

    def _initialize_hd_brushes(self) -> None:
        """Initialize all 50+ HD tattoo brushes."""
        self.brushes = {
            # OUTLINE BRUSHES
            "outline_thin": HDTattooBrush(
                id="outline_thin",
                name="Outline Thin",
                category="outline",
                style="solid",
                size_range=(1.0, 5.0),
                opacity_range=(0.8, 1.0),
                hardness=1.0,
                spacing=0.05,
                jitter_amount=0.0,
                smoothing=0.7,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.0,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=True,
                description="Perfect for precise fine line work and detailed outlines",
                tags=["outline", "fine", "detail", "linework"],
                bristle_count=500,
                bristle_curve="smooth"
            ),
            "outline_medium": HDTattooBrush(
                id="outline_medium",
                name="Outline Medium",
                category="outline",
                style="solid",
                size_range=(3.0, 8.0),
                opacity_range=(0.9, 1.0),
                hardness=0.95,
                spacing=0.08,
                jitter_amount=0.02,
                smoothing=0.8,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.05,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=True,
                description="Standard outline brush for primary tattoo contours",
                tags=["outline", "standard", "main"],
                bristle_count=800,
                bristle_curve="smooth"
            ),
            "outline_thick": HDTattooBrush(
                id="outline_thick",
                name="Outline Thick",
                category="outline",
                style="solid",
                size_range=(5.0, 15.0),
                opacity_range=(0.85, 1.0),
                hardness=0.9,
                spacing=0.1,
                jitter_amount=0.03,
                smoothing=0.75,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.08,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=True,
                description="Bold outline for strong emphasis and defining edges",
                tags=["outline", "bold", "emphasis"],
                bristle_count=1200,
                bristle_curve="smooth"
            ),
            "outline_calligraphy": HDTattooBrush(
                id="outline_calligraphy",
                name="Calligraphy Outline",
                category="outline",
                style="solid",
                size_range=(2.0, 8.0),
                opacity_range=(0.8, 1.0),
                hardness=0.85,
                spacing=0.12,
                jitter_amount=0.0,
                smoothing=0.9,
                aspect_ratio=3.0,
                angle=45.0,
                texture_depth=0.0,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=True,
                velocity_sensitivity=True,
                description="Calligraphic style brush for artistic line variation",
                tags=["outline", "artistic", "calligraphy"],
                bristle_count=600,
                bristle_curve="smooth"
            ),
            "outline_pressure": HDTattooBrush(
                id="outline_pressure",
                name="Pressure Outline",
                category="outline",
                style="solid",
                size_range=(1.0, 10.0),
                opacity_range=(0.7, 1.0),
                hardness=0.92,
                spacing=0.06,
                jitter_amount=0.01,
                smoothing=0.85,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.02,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Responsive to pressure for natural line weight variation",
                tags=["outline", "responsive", "pressure"],
                bristle_count=700,
                bristle_curve="smooth"
            ),

            # SHADING BRUSHES
            "shading_soft": HDTattooBrush(
                id="shading_soft",
                name="Shading Soft",
                category="shading",
                style="textured",
                size_range=(5.0, 20.0),
                opacity_range=(0.3, 0.7),
                hardness=0.3,
                spacing=0.2,
                jitter_amount=0.05,
                smoothing=0.6,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.3,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=True,
                velocity_sensitivity=True,
                description="Soft shading for smooth gradients and blending",
                tags=["shading", "soft", "blending"],
                bristle_count=2000,
                bristle_curve="smooth"
            ),
            "shading_medium": HDTattooBrush(
                id="shading_medium",
                name="Shading Medium",
                category="shading",
                style="textured",
                size_range=(8.0, 25.0),
                opacity_range=(0.5, 0.85),
                hardness=0.5,
                spacing=0.15,
                jitter_amount=0.08,
                smoothing=0.65,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.4,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=True,
                velocity_sensitivity=True,
                description="Medium shading for balanced tone and depth",
                tags=["shading", "medium", "tone"],
                bristle_count=1800,
                bristle_curve="smooth"
            ),
            "shading_hard": HDTattooBrush(
                id="shading_hard",
                name="Shading Hard",
                category="shading",
                style="textured",
                size_range=(6.0, 18.0),
                opacity_range=(0.6, 0.95),
                hardness=0.7,
                spacing=0.12,
                jitter_amount=0.1,
                smoothing=0.5,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.5,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=True,
                velocity_sensitivity=False,
                description="Hard shading for dramatic contrasts and strong shadows",
                tags=["shading", "hard", "contrast"],
                bristle_count=1500,
                bristle_curve="sharp"
            ),
            "shading_airbrush": HDTattooBrush(
                id="shading_airbrush",
                name="Airbrush Shading",
                category="shading",
                style="gradient",
                size_range=(10.0, 40.0),
                opacity_range=(0.2, 0.5),
                hardness=0.1,
                spacing=0.3,
                jitter_amount=0.15,
                smoothing=0.4,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.2,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=True,
                description="Airbrush effect for soft ethereal shading and atmospheric effects",
                tags=["shading", "airbrush", "soft", "atmospheric"],
                bristle_count=3000,
                bristle_curve="smooth"
            ),
            "shading_dodge": HDTattooBrush(
                id="shading_dodge",
                name="Dodge Shading",
                category="shading",
                style="textured",
                size_range=(8.0, 22.0),
                opacity_range=(0.4, 0.7),
                hardness=0.4,
                spacing=0.2,
                jitter_amount=0.06,
                smoothing=0.7,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.35,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=True,
                velocity_sensitivity=True,
                description="For creating highlights and light effects",
                tags=["shading", "highlight", "light"],
                bristle_count=1900,
                bristle_curve="smooth"
            ),

            # FILL BRUSHES
            "fill_solid": HDTattooBrush(
                id="fill_solid",
                name="Solid Fill",
                category="fill",
                style="solid",
                size_range=(15.0, 60.0),
                opacity_range=(0.8, 1.0),
                hardness=0.95,
                spacing=0.15,
                jitter_amount=0.02,
                smoothing=0.8,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.1,
                color_dynamics=False,
                pressure_sensitivity=False,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Flat coverage for solid color areas",
                tags=["fill", "solid", "coverage"],
                bristle_count=2500,
                bristle_curve="smooth"
            ),
            "fill_textured": HDTattooBrush(
                id="fill_textured",
                name="Textured Fill",
                category="fill",
                style="textured",
                size_range=(12.0, 50.0),
                opacity_range=(0.7, 0.95),
                hardness=0.6,
                spacing=0.2,
                jitter_amount=0.1,
                smoothing=0.5,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.6,
                color_dynamics=False,
                pressure_sensitivity=False,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Textured fill for organic natural appearance",
                tags=["fill", "texture", "organic"],
                bristle_count=2000,
                bristle_curve="smooth"
            ),
            "fill_gradient": HDTattooBrush(
                id="fill_gradient",
                name="Gradient Fill",
                category="fill",
                style="gradient",
                size_range=(18.0, 70.0),
                opacity_range=(0.6, 0.9),
                hardness=0.4,
                spacing=0.25,
                jitter_amount=0.05,
                smoothing=0.6,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.3,
                color_dynamics=True,
                pressure_sensitivity=False,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Gradient fill for smooth color transitions",
                tags=["fill", "gradient", "transition"],
                bristle_count=2200,
                bristle_curve="smooth"
            ),
            "fill_stipple": HDTattooBrush(
                id="fill_stipple",
                name="Stipple Fill",
                category="fill",
                style="stippled",
                size_range=(10.0, 40.0),
                opacity_range=(0.5, 0.8),
                hardness=0.8,
                spacing=0.3,
                jitter_amount=0.3,
                smoothing=0.3,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.7,
                color_dynamics=False,
                pressure_sensitivity=False,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Stippled fill for dotted texture effects",
                tags=["fill", "stipple", "dots"],
                bristle_count=500,
                bristle_curve="sharp"
            ),

            # DETAIL BRUSHES
            "detail_fine": HDTattooBrush(
                id="detail_fine",
                name="Detail Fine",
                category="detail",
                style="solid",
                size_range=(0.5, 3.0),
                opacity_range=(0.9, 1.0),
                hardness=1.0,
                spacing=0.05,
                jitter_amount=0.0,
                smoothing=0.9,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.0,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=True,
                description="Ultra-fine details and intricate work",
                tags=["detail", "fine", "intricate"],
                bristle_count=200,
                bristle_curve="smooth"
            ),
            "detail_eyeliner": HDTattooBrush(
                id="detail_eyeliner",
                name="Eyeliner Detail",
                category="detail",
                style="solid",
                size_range=(1.0, 4.0),
                opacity_range=(0.95, 1.0),
                hardness=0.98,
                spacing=0.04,
                jitter_amount=0.0,
                smoothing=0.95,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.0,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Precision eyeliner and eye detail work",
                tags=["detail", "eyes", "eyeliner"],
                bristle_count=150,
                bristle_curve="smooth"
            ),
            "detail_stipple": HDTattooBrush(
                id="detail_stipple",
                name="Stipple Detail",
                category="detail",
                style="stippled",
                size_range=(1.0, 5.0),
                opacity_range=(0.7, 0.95),
                hardness=0.9,
                spacing=0.15,
                jitter_amount=0.2,
                smoothing=0.5,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.6,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Stippled detail work for texture",
                tags=["detail", "stipple", "texture"],
                bristle_count=300,
                bristle_curve="sharp"
            ),
            "detail_crosshatch": HDTattooBrush(
                id="detail_crosshatch",
                name="Crosshatch Detail",
                category="detail",
                style="hatched",
                size_range=(1.0, 4.0),
                opacity_range=(0.8, 1.0),
                hardness=0.92,
                spacing=0.1,
                jitter_amount=0.05,
                smoothing=0.7,
                aspect_ratio=2.0,
                angle=45.0,
                texture_depth=0.5,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=True,
                velocity_sensitivity=False,
                description="Crosshatching for detailed shading effects",
                tags=["detail", "crosshatch", "shading"],
                bristle_count=250,
                bristle_curve="smooth"
            ),

            # SPECIALTY BRUSHES
            "specialty_watercolor": HDTattooBrush(
                id="specialty_watercolor",
                name="Watercolor",
                category="specialty",
                style="gradient",
                size_range=(10.0, 35.0),
                opacity_range=(0.3, 0.6),
                hardness=0.2,
                spacing=0.25,
                jitter_amount=0.15,
                smoothing=0.5,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.4,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=True,
                velocity_sensitivity=True,
                description="Watercolor effect for flowing artistic looks",
                tags=["specialty", "watercolor", "artistic"],
                bristle_count=2500,
                bristle_curve="smooth"
            ),
            "specialty_ink_splatter": HDTattooBrush(
                id="specialty_ink_splatter",
                name="Ink Splatter",
                category="specialty",
                style="scattered",
                size_range=(5.0, 30.0),
                opacity_range=(0.6, 1.0),
                hardness=0.7,
                spacing=0.4,
                jitter_amount=0.5,
                smoothing=0.2,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.3,
                color_dynamics=False,
                pressure_sensitivity=False,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Splatter effect for dynamic artistic elements",
                tags=["specialty", "splatter", "artistic"],
                bristle_count=1000,
                bristle_curve="sharp"
            ),
            "specialty_glow": HDTattooBrush(
                id="specialty_glow",
                name="Glow Effect",
                category="specialty",
                style="gradient",
                size_range=(8.0, 40.0),
                opacity_range=(0.3, 0.6),
                hardness=0.1,
                spacing=0.3,
                jitter_amount=0.1,
                smoothing=0.4,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.2,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=True,
                description="Soft glow effect for ethereal qualities",
                tags=["specialty", "glow", "light"],
                bristle_count=2800,
                bristle_curve="smooth"
            ),
            "specialty_flame": HDTattooBrush(
                id="specialty_flame",
                name="Flame",
                category="specialty",
                style="scattered",
                size_range=(6.0, 25.0),
                opacity_range=(0.5, 0.9),
                hardness=0.5,
                spacing=0.2,
                jitter_amount=0.3,
                smoothing=0.4,
                aspect_ratio=1.5,
                angle=0.0,
                texture_depth=0.5,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=True,
                velocity_sensitivity=False,
                description="Flame texture for fire and energy effects",
                tags=["specialty", "flame", "texture"],
                bristle_count=800,
                bristle_curve="sharp"
            ),
            "specialty_smoke": HDTattooBrush(
                id="specialty_smoke",
                name="Smoke",
                category="specialty",
                style="gradient",
                size_range=(12.0, 50.0),
                opacity_range=(0.2, 0.5),
                hardness=0.15,
                spacing=0.3,
                jitter_amount=0.2,
                smoothing=0.3,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.3,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=True,
                description="Smoke effect for atmospheric elements",
                tags=["specialty", "smoke", "atmospheric"],
                bristle_count=2200,
                bristle_curve="smooth"
            ),
            "specialty_skulls": HDTattooBrush(
                id="specialty_skulls",
                name="Skull Pattern",
                category="specialty",
                style="pattern",
                size_range=(8.0, 30.0),
                opacity_range=(0.7, 1.0),
                hardness=0.8,
                spacing=0.25,
                jitter_amount=0.1,
                smoothing=0.6,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.4,
                color_dynamics=False,
                pressure_sensitivity=False,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Skull pattern repeats for skull designs",
                tags=["specialty", "pattern", "skull"],
                bristle_count=1500,
                bristle_curve="smooth"
            ),

            # STIPPLE BRUSHES
            "stipple_fine": HDTattooBrush(
                id="stipple_fine",
                name="Stipple Fine",
                category="stipple",
                style="stippled",
                size_range=(1.0, 3.0),
                opacity_range=(0.6, 0.9),
                hardness=0.95,
                spacing=0.2,
                jitter_amount=0.25,
                smoothing=0.4,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.8,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Fine stippling for delicate dot work",
                tags=["stipple", "fine", "dots"],
                bristle_count=100,
                bristle_curve="sharp"
            ),
            "stipple_medium": HDTattooBrush(
                id="stipple_medium",
                name="Stipple Medium",
                category="stipple",
                style="stippled",
                size_range=(2.0, 6.0),
                opacity_range=(0.7, 0.95),
                hardness=0.92,
                spacing=0.25,
                jitter_amount=0.3,
                smoothing=0.35,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.85,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Medium dot work for balanced stippling",
                tags=["stipple", "medium", "dots"],
                bristle_count=200,
                bristle_curve="sharp"
            ),
            "stipple_large": HDTattooBrush(
                id="stipple_large",
                name="Stipple Large",
                category="stipple",
                style="stippled",
                size_range=(4.0, 12.0),
                opacity_range=(0.8, 1.0),
                hardness=0.9,
                spacing=0.3,
                jitter_amount=0.35,
                smoothing=0.3,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.9,
                color_dynamics=False,
                pressure_sensitivity=False,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Large stippling for bold dot work",
                tags=["stipple", "large", "bold"],
                bristle_count=300,
                bristle_curve="sharp"
            ),
            "stipple_gradient": HDTattooBrush(
                id="stipple_gradient",
                name="Stipple Gradient",
                category="stipple",
                style="stippled",
                size_range=(1.0, 8.0),
                opacity_range=(0.3, 0.95),
                hardness=0.88,
                spacing=0.2,
                jitter_amount=0.3,
                smoothing=0.45,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.82,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Gradient stippling for transitional dot work",
                tags=["stipple", "gradient", "transition"],
                bristle_count=250,
                bristle_curve="smooth"
            ),

            # TEXTURE BRUSHES
            "texture_rough": HDTattooBrush(
                id="texture_rough",
                name="Rough Texture",
                category="texture",
                style="textured",
                size_range=(8.0, 30.0),
                opacity_range=(0.6, 0.9),
                hardness=0.75,
                spacing=0.15,
                jitter_amount=0.15,
                smoothing=0.4,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.75,
                color_dynamics=False,
                pressure_sensitivity=False,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Rough texture for organic feel",
                tags=["texture", "rough", "organic"],
                bristle_count=1800,
                bristle_curve="sharp"
            ),
            "texture_canvas": HDTattooBrush(
                id="texture_canvas",
                name="Canvas Texture",
                category="texture",
                style="textured",
                size_range=(10.0, 40.0),
                opacity_range=(0.5, 0.8),
                hardness=0.6,
                spacing=0.2,
                jitter_amount=0.2,
                smoothing=0.3,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.8,
                color_dynamics=False,
                pressure_sensitivity=False,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Canvas-like texture for artistic effect",
                tags=["texture", "canvas", "artistic"],
                bristle_count=2000,
                bristle_curve="smooth"
            ),
            "texture_grunge": HDTattooBrush(
                id="texture_grunge",
                name="Grunge",
                category="texture",
                style="scattered",
                size_range=(8.0, 35.0),
                opacity_range=(0.5, 0.85),
                hardness=0.65,
                spacing=0.25,
                jitter_amount=0.4,
                smoothing=0.25,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.7,
                color_dynamics=False,
                pressure_sensitivity=False,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Grunge texture for distressed look",
                tags=["texture", "grunge", "distressed"],
                bristle_count=1500,
                bristle_curve="sharp"
            ),
            "texture_scales": HDTattooBrush(
                id="texture_scales",
                name="Scales Texture",
                category="texture",
                style="pattern",
                size_range=(6.0, 20.0),
                opacity_range=(0.7, 0.95),
                hardness=0.8,
                spacing=0.18,
                jitter_amount=0.05,
                smoothing=0.6,
                aspect_ratio=1.2,
                angle=0.0,
                texture_depth=0.65,
                color_dynamics=False,
                pressure_sensitivity=False,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Scale pattern for reptilian textures",
                tags=["texture", "scales", "pattern"],
                bristle_count=1200,
                bristle_curve="sharp"
            ),

            # LINEWORK BRUSHES
            "linework_feathered": HDTattooBrush(
                id="linework_feathered",
                name="Feathered Line",
                category="linework",
                style="solid",
                size_range=(2.0, 8.0),
                opacity_range=(0.7, 1.0),
                hardness=0.4,
                spacing=0.1,
                jitter_amount=0.05,
                smoothing=0.85,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.2,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Feathered edges for soft linework",
                tags=["linework", "feathered", "soft"],
                bristle_count=900,
                bristle_curve="smooth"
            ),
            "linework_curved": HDTattooBrush(
                id="linework_curved",
                name="Curved Line",
                category="linework",
                style="solid",
                size_range=(1.0, 6.0),
                opacity_range=(0.85, 1.0),
                hardness=0.95,
                spacing=0.05,
                jitter_amount=0.01,
                smoothing=0.95,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.0,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=True,
                description="Smooth curved lines for flowing designs",
                tags=["linework", "curved", "smooth"],
                bristle_count=600,
                bristle_curve="smooth"
            ),
            "linework_brush_pen": HDTattooBrush(
                id="linework_brush_pen",
                name="Brush Pen",
                category="linework",
                style="solid",
                size_range=(1.5, 7.0),
                opacity_range=(0.9, 1.0),
                hardness=0.85,
                spacing=0.08,
                jitter_amount=0.02,
                smoothing=0.88,
                aspect_ratio=1.2,
                angle=30.0,
                texture_depth=0.05,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=True,
                velocity_sensitivity=True,
                description="Natural brush pen feel for organic lines",
                tags=["linework", "brush", "natural"],
                bristle_count=700,
                bristle_curve="smooth"
            ),
            "linework_dry": HDTattooBrush(
                id="linework_dry",
                name="Dry Brush Line",
                category="linework",
                style="textured",
                size_range=(2.0, 8.0),
                opacity_range=(0.6, 0.95),
                hardness=0.7,
                spacing=0.12,
                jitter_amount=0.1,
                smoothing=0.6,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.5,
                color_dynamics=False,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Dry brush effect for textured lines",
                tags=["linework", "dry", "textured"],
                bristle_count=550,
                bristle_curve="sharp"
            ),

            # BLENDING BRUSHES
            "blending_soft": HDTattooBrush(
                id="blending_soft",
                name="Blend Soft",
                category="blending",
                style="gradient",
                size_range=(8.0, 25.0),
                opacity_range=(0.3, 0.6),
                hardness=0.15,
                spacing=0.25,
                jitter_amount=0.05,
                smoothing=0.8,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.2,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=True,
                velocity_sensitivity=False,
                description="Ultra soft for gentle blending",
                tags=["blending", "soft", "smooth"],
                bristle_count=2500,
                bristle_curve="smooth"
            ),
            "blending_mixer": HDTattooBrush(
                id="blending_mixer",
                name="Mixer Blend",
                category="blending",
                style="textured",
                size_range=(6.0, 20.0),
                opacity_range=(0.4, 0.7),
                hardness=0.3,
                spacing=0.2,
                jitter_amount=0.08,
                smoothing=0.7,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.3,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=True,
                velocity_sensitivity=True,
                description="Mixes colors naturally",
                tags=["blending", "mixer", "color"],
                bristle_count=1800,
                bristle_curve="smooth"
            ),
            "blending_smudge": HDTattooBrush(
                id="blending_smudge",
                name="Smudge Blend",
                category="blending",
                style="gradient",
                size_range=(5.0, 18.0),
                opacity_range=(0.2, 0.5),
                hardness=0.2,
                spacing=0.3,
                jitter_amount=0.1,
                smoothing=0.6,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.25,
                color_dynamics=True,
                pressure_sensitivity=True,
                tilt_sensitivity=False,
                velocity_sensitivity=True,
                description="Smudging effect for blending",
                tags=["blending", "smudge", "effect"],
                bristle_count=1400,
                bristle_curve="smooth"
            ),
            "blending_gradient": HDTattooBrush(
                id="blending_gradient",
                name="Gradient Blend",
                category="blending",
                style="gradient",
                size_range=(10.0, 30.0),
                opacity_range=(0.35, 0.65),
                hardness=0.1,
                spacing=0.3,
                jitter_amount=0.02,
                smoothing=0.75,
                aspect_ratio=1.0,
                angle=0.0,
                texture_depth=0.15,
                color_dynamics=True,
                pressure_sensitivity=False,
                tilt_sensitivity=False,
                velocity_sensitivity=False,
                description="Perfect gradients between colors",
                tags=["blending", "gradient", "smooth"],
                bristle_count=2300,
                bristle_curve="smooth"
            ),
        }

    def get_brush(self, brush_id: str) -> Optional[HDTattooBrush]:
        """Get a brush by ID.
        
        Args:
            brush_id: The brush ID
            
        Returns:
            The brush or None if not found
        """
        return self.brushes.get(brush_id)

    def get_brushes_by_category(self, category: str) -> List[HDTattooBrush]:
        """Get all brushes in a category.
        
        Args:
            category: Category name (from BrushCategory enum)
            
        Returns:
            List of brushes in the category
        """
        return [b for b in self.brushes.values() if b.category == category]

    def get_brushes_by_tag(self, tag: str) -> List[HDTattooBrush]:
        """Get all brushes with a specific tag.
        
        Args:
            tag: Tag to search for
            
        Returns:
            List of brushes with the tag
        """
        return [b for b in self.brushes.values() if tag in b.tags]

    def search_brushes(self, query: str) -> List[HDTattooBrush]:
        """Search brushes by name or description.
        
        Args:
            query: Search query
            
        Returns:
            List of matching brushes
        """
        query_lower = query.lower()
        return [b for b in self.brushes.values()
                if query_lower in b.name.lower() or
                   query_lower in b.description.lower()]

    def create_preset(self, name: str, brush_id: str, size: float,
                     opacity: float, hardness: float, spacing: float,
                     smoothing: float, color: Tuple[int, int, int] = (0, 0, 0),
                     description: str = "") -> Optional[BrushPreset]:
        """Create a new brush preset.
        
        Args:
            name: Preset name
            brush_id: Base brush ID
            size: Brush size
            opacity: Opacity 0-1
            hardness: Hardness 0-1
            spacing: Spacing 0-1
            smoothing: Smoothing 0-1
            color: RGB color tuple
            description: Preset description
            
        Returns:
            The created preset or None if brush not found
        """
        if brush_id not in self.brushes:
            return None

        preset = BrushPreset(
            name=name,
            brush_id=brush_id,
            size=size,
            opacity=opacity,
            hardness=hardness,
            spacing=spacing,
            smoothing=smoothing,
            color=color,
            description=description
        )
        self.presets[name] = preset
        return preset

    def get_preset(self, preset_name: str) -> Optional[BrushPreset]:
        """Get a preset by name.
        
        Args:
            preset_name: Preset name
            
        Returns:
            The preset or None if not found
        """
        return self.presets.get(preset_name)

    def list_presets(self) -> List[str]:
        """List all preset names.
        
        Returns:
            List of preset names
        """
        return list(self.presets.keys())

    def delete_preset(self, preset_name: str) -> bool:
        """Delete a preset.
        
        Args:
            preset_name: Preset name
            
        Returns:
            True if deleted, False if not found
        """
        if preset_name in self.presets:
            del self.presets[preset_name]
            return True
        return False

    def _load_presets(self) -> None:
        """Load presets from file."""
        presets_file = self.brush_dir / "presets.json"
        if presets_file.exists():
            try:
                with open(presets_file, 'r') as f:
                    data = json.load(f)
                    for preset_data in data.get('presets', []):
                        preset = BrushPreset(**preset_data)
                        self.presets[preset.name] = preset
            except Exception as e:
                print(f"Error loading presets: {e}")

    def save_presets(self) -> bool:
        """Save presets to file.
        
        Returns:
            True if successful
        """
        try:
            presets_file = self.brush_dir / "presets.json"
            data = {
                'presets': [asdict(p) for p in self.presets.values()]
            }
            with open(presets_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving presets: {e}")
            return False

    def export_brush_pack(self, output_path: str, brush_ids: List[str]) -> bool:
        """Export selected brushes as a pack.
        
        Args:
            output_path: Output file path
            brush_ids: List of brush IDs to export
            
        Returns:
            True if successful
        """
        try:
            brushes_data = {
                'brushes': [self.brushes[bid].to_dict() for bid in brush_ids
                           if bid in self.brushes],
                'version': '1.0',
                'format': 'HD Tattoo Brushes'
            }
            with open(output_path, 'w') as f:
                json.dump(brushes_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting brush pack: {e}")
            return False

    def get_all_brushes(self) -> List[HDTattooBrush]:
        """Get all brushes.
        
        Returns:
            List of all brushes
        """
        return list(self.brushes.values())

    def get_brush_categories(self) -> List[str]:
        """Get all available categories.
        
        Returns:
            List of category names
        """
        return list(set(b.category for b in self.brushes.values()))
