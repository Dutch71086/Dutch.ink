"""Example usage of the HD Tattoo Brush Manager.

Demonstrates how to use brushes, create presets, search, and manage the library.
"""

from brushes.brush_manager import BrushManager, BrushCategory


def main():
    """Main example function."""
    # Initialize the brush manager
    print("=" * 60)
    print("HD Tattoo Brush Manager - Usage Examples")
    print("=" * 60)

    manager = BrushManager()

    # Example 1: Get all brushes
    print("\n1. Total brushes available:")
    all_brushes = manager.get_all_brushes()
    print(f"   Total: {len(all_brushes)} brushes")

    # Example 2: Get brushes by category
    print("\n2. Brushes by category:")
    for category in manager.get_brush_categories():
        brushes = manager.get_brushes_by_category(category)
        print(f"   {category.upper()}: {len(brushes)} brushes")
        for brush in brushes[:2]:  # Show first 2
            print(f"      - {brush.name}")

    # Example 3: Get specific brush
    print("\n3. Getting specific brush:")
    outline_brush = manager.get_brush("outline_medium")
    if outline_brush:
        print(f"   Name: {outline_brush.name}")
        print(f"   Size Range: {outline_brush.size_range}")
        print(f"   Hardness: {outline_brush.hardness}")
        print(f"   Tags: {outline_brush.tags}")

    # Example 4: Search brushes
    print("\n4. Searching for 'shading' brushes:")
    shading_brushes = manager.search_brushes("shading")
    for brush in shading_brushes:
        print(f"   - {brush.name}: {brush.description[:50]}...")

    # Example 5: Get brushes by tag
    print("\n5. Brushes with 'outline' tag:")
    outline_tagged = manager.get_brushes_by_tag("outline")
    for brush in outline_tagged:
        print(f"   - {brush.name}")

    # Example 6: Create a preset
    print("\n6. Creating custom preset:")
    preset = manager.create_preset(
        name="My Custom Outline",
        brush_id="outline_medium",
        size=6.0,
        opacity=0.95,
        hardness=0.92,
        spacing=0.1,
        smoothing=0.8,
        color=(0, 0, 0),
        description="My preferred outline settings"
    )
    if preset:
        print(f"   ✓ Created preset: {preset.name}")
        print(f"   Base Brush: {preset.brush_id}")
        print(f"   Size: {preset.size}")
        print(f"   Opacity: {preset.opacity:.0%}")

    # Example 7: Get preset
    print("\n7. Retrieving preset:")
    retrieved_preset = manager.get_preset("My Custom Outline")
    if retrieved_preset:
        print(f"   ✓ Found preset: {retrieved_preset.name}")

    # Example 8: List all presets
    print("\n8. All saved presets:")
    presets = manager.list_presets()
    for preset_name in presets:
        print(f"   - {preset_name}")

    # Example 9: Create more presets
    print("\n9. Creating preset collection:")
    presets_config = [
        {
            "name": "Fine Detail Work",
            "brush_id": "detail_fine",
            "size": 1.5,
            "opacity": 0.98,
            "hardness": 1.0,
            "spacing": 0.05,
            "smoothing": 0.9,
        },
        {
            "name": "Soft Shading",
            "brush_id": "shading_soft",
            "size": 15.0,
            "opacity": 0.5,
            "hardness": 0.3,
            "spacing": 0.2,
            "smoothing": 0.6,
            "color": (100, 100, 100),
        },
        {
            "name": "Bold Fill",
            "brush_id": "fill_solid",
            "size": 25.0,
            "opacity": 0.9,
            "hardness": 0.95,
            "spacing": 0.15,
            "smoothing": 0.8,
        },
    ]

    for config in presets_config:
        manager.create_preset(**config)
        print(f"   ✓ Created: {config['name']}")

    # Example 10: Display brush details
    print("\n10. Detailed brush information:")
    brush = manager.get_brush("shading_soft")
    if brush:
        print(f"\n    Brush: {brush.name}")
        print(f"    Category: {brush.category}")
        print(f"    Style: {brush.style}")
        print(f"    Description: {brush.description}")
        print(f"    Size Range: {brush.size_range[0]}-{brush.size_range[1]}px")
        print(f"    Opacity Range: {brush.opacity_range[0]:.0%}-{brush.opacity_range[1]:.0%}")
        print(f"    Hardness: {brush.hardness}")
        print(f"    Spacing: {brush.spacing}")
        print(f"    Jitter: {brush.jitter_amount}")
        print(f"    Smoothing: {brush.smoothing}")
        print(f"    Texture Depth: {brush.texture_depth}")
        print(f"    Aspect Ratio: {brush.aspect_ratio}")
        print(f"    Angle: {brush.angle}°")
        print(f"    Bristle Count: {brush.bristle_count}")
        print(f"    Bristle Curve: {brush.bristle_curve}")
        print(f"    Color Dynamics: {'Yes' if brush.color_dynamics else 'No'}")
        print(f"    Pressure Sensitive: {'Yes' if brush.pressure_sensitivity else 'No'}")
        print(f"    Tilt Sensitive: {'Yes' if brush.tilt_sensitivity else 'No'}")
        print(f"    Velocity Sensitive: {'Yes' if brush.velocity_sensitivity else 'No'}")
        print(f"    HD Quality: {'Yes' if brush.hd_quality else 'No'}")
        print(f"    Tags: {', '.join(brush.tags)}")

    # Example 11: Export brush pack
    print("\n11. Exporting brush pack:")
    brushes_to_export = [
        "outline_medium",
        "outline_thin",
        "shading_soft",
        "detail_fine",
    ]
    success = manager.export_brush_pack("my_brush_pack.json", brushes_to_export)
    if success:
        print(f"   ✓ Exported {len(brushes_to_export)} brushes to my_brush_pack.json")

    # Example 12: Save presets
    print("\n12. Saving presets to file:")
    success = manager.save_presets()
    if success:
        print("   ✓ Presets saved successfully")

    # Example 13: Statistics
    print("\n13. Brush statistics:")
    all_brushes = manager.get_all_brushes()
    pressure_sensitive = sum(1 for b in all_brushes if b.pressure_sensitivity)
    tilt_sensitive = sum(1 for b in all_brushes if b.tilt_sensitivity)
    color_dynamics = sum(1 for b in all_brushes if b.color_dynamics)
    print(f"   Total brushes: {len(all_brushes)}")
    print(f"   Pressure sensitive: {pressure_sensitive}")
    print(f"   Tilt sensitive: {tilt_sensitive}")
    print(f"   With color dynamics: {color_dynamics}")
    print(f"   Average bristle count: {sum(b.bristle_count for b in all_brushes) / len(all_brushes):.0f}")

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
