#!/usr/bin/env python3
"""
Simple USEtox Template Population Example

This example demonstrates the simplified approach to populating USEtox Excel templates:
1. Call EPI Suite API for chemical data
2. Open Excel template with openpyxl
3. Add chemical data row by row starting from row 6
4. Save the populated template

The USEtoxInput class keeps it simple and focused on the core goal.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path for importing pyepisuite
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from pyepisuite.usetox_input import USEtoxInput, create_usetox_input_from_cas_list


def main():
    """Simple demonstration of USEtox template population."""
    
    print("🧪 Simple USEtox Template Population")
    print("=" * 40)
    
    # Step 1: Define chemicals by CAS numbers
    target_chemicals = [
        "67-56-1",    # Methanol
        "100-41-4",   # Ethylbenzene
        "108-88-3"    # Toluene
    ]
    
    chemical_names = {
        "67-56-1": "Methanol",
        "100-41-4": "Ethylbenzene", 
        "108-88-3": "Toluene"
    }
    
    print(f"\n📋 Target chemicals:")
    for cas in target_chemicals:
        print(f"  • {chemical_names[cas]} (CAS: {cas})")
    
    # Step 2: Create USEtox input using the simple approach
    print(f"\n🔧 Creating USEtox input...")
    output_file = current_dir / "simple_usetox_populated.xlsx"
    template_path = "data/usetox3/AA_Model_substance_data_Default.xlsx"
    
    try:
        # Use the convenience function
        usetox_input = create_usetox_input_from_cas_list(
            cas_list=target_chemicals,
            output_path=str(output_file),
            template_path=template_path
        )
        
        # Get summary
        summary = usetox_input.get_summary()
        print(f"\n📊 Results:")
        print(f"  • Chemicals added: {summary['chemicals_added']}")
        print(f"  • Current row: {summary['current_row']}")
        print(f"  • File size: {output_file.stat().st_size / 1024:.1f} KB")
        
        print(f"\n✅ Success! USEtox template populated and saved to:")
        print(f"📁 {output_file}")
        
        print(f"\n🎯 Key features of this approach:")
        print(f"  ✓ Simple and focused - just populate Excel template")
        print(f"  ✓ Uses openpyxl directly (no pandas DataFrame complexity)")
        print(f"  ✓ Starts at row 6 as required by USEtox format")
        print(f"  ✓ Maps EPI Suite properties to exact Excel columns")
        print(f"  ✓ Handles unit conversions automatically")
        print(f"  ✓ Ready for USEtox import")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def demonstrate_manual_addition():
    """Demonstrate manual addition of chemicals."""
    
    print(f"\n" + "=" * 50)
    print("🛠️  Manual Chemical Addition Example")
    print("=" * 50)
    
    try:
        # Create USEtoxInput instance
        usetox = USEtoxInput("data/usetox3/AA_Model_substance_data_Default.xlsx")
        
        # Manually add a chemical with known properties
        sample_data = {
            'cas': '50-00-0',
            'name': 'Formaldehyde',
            'molecular_weight': 30.03,
            'log_kow_estimated': 0.35,
            'water_solubility_logkow_estimated': 400000,  # mg/L
            'vapor_pressure_estimated': 3900,  # mmHg
            'atmospheric_half_life_estimated': 47.2,  # hours
        }
        
        row_num = usetox.add_chemical_from_episuite(sample_data)
        print(f"✅ Manually added Formaldehyde at row {row_num}")
        
        # Check what was added
        cas_value = usetox.worksheet[f'B{row_num}'].value
        name_value = usetox.worksheet[f'C{row_num}'].value
        mw_value = usetox.worksheet[f'F{row_num}'].value
        kow_value = usetox.worksheet[f'K{row_num}'].value  # Should be converted from log
        
        print(f"  📊 Values in Excel:")
        print(f"    CAS (B{row_num}): {cas_value}")
        print(f"    Name (C{row_num}): {name_value}")
        print(f"    MW (F{row_num}): {mw_value}")
        print(f"    Kow (K{row_num}): {kow_value:.1f}")  # Should be 10^0.35 ≈ 2.24
        
        # Save manual example
        output_file = Path(__file__).parent / "manual_usetox_example.xlsx"
        usetox.save_excel(str(output_file))
        print(f"💾 Saved manual example to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error in manual addition: {e}")


if __name__ == "__main__":
    main()
    demonstrate_manual_addition()
