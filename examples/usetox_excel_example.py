#!/usr/bin/env python3
"""
PyEPISuite USEtox Excel Export Example

This example demonstrates how to:
1. Search for chemicals by CAS numbers using PyEPISuite
2. Retrieve EPI Suite predictions for chemical properties
3. Convert the results to a pandas DataFrame
4. Export the data to a USEtox-compatible Excel format

The USEtox format is used for environmental impact assessment and 
life cycle assessment calculations.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path for importing pyepisuite
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

try:
    from pyepisuite.utils import search_episuite_by_cas, submit_to_episuite
    from pyepisuite.dataframe_utils import episuite_to_dataframe
    from pyepisuite.usetox_input import create_usetox_input_from_episuite
    print("✅ Successfully imported PyEPISuite modules")
except ImportError as e:
    print(f"❌ Error importing PyEPISuite: {e}")
    print("Make sure you have installed PyEPISuite: pip install -e .")
    sys.exit(1)


def main():
    """Main function demonstrating USEtox Excel export workflow."""
    
    print("🧪 PyEPISuite USEtox Excel Export Example")
    print("=" * 50)
    
    # Step 1: Define chemicals of interest by CAS numbers
    chemicals_of_interest = {
        "50-00-0": "Formaldehyde",           # Common industrial chemical
        "67-56-1": "Methanol",              # Solvent
        "100-41-4": "Ethylbenzene"          # Industrial chemical
    }
    
    cas_numbers = list(chemicals_of_interest.keys())
    
    print(f"\n📋 Searching for {len(cas_numbers)} chemicals:")
    for cas, name in chemicals_of_interest.items():
        print(f"  • {name} (CAS: {cas})")
    
    try:
        # Step 2: Search for chemicals in EPI Suite database
        print("\n🔍 Searching EPI Suite database...")
        chemical_ids = search_episuite_by_cas(cas_numbers)
        
        # Note: EPI Suite returns CAS numbers with zero-padding (e.g., "000050-00-0")
        # We need to handle this padding to match our input CAS numbers
        def normalize_cas(cas_number):
            """Normalize CAS number by removing leading zeros from each part."""
            parts = cas_number.split('-')
            if len(parts) == 3:
                # Remove leading zeros from first two parts
                return f"{parts[0].lstrip('0') or '0'}-{parts[1].lstrip('0') or '0'}-{parts[2]}"
            return cas_number
        
        # Create mapping between normalized and original CAS numbers
        cas_mapping = {}
        for chem in chemical_ids:
            normalized = normalize_cas(chem.cas)
            if normalized in cas_numbers:
                cas_mapping[chem.cas] = normalized
        
        found_chemicals = [id_obj for id_obj in chemical_ids if id_obj.cas in cas_mapping]
        
        print(f"✅ Found {len(found_chemicals)} chemicals in EPI Suite database")
        
        # Show what was actually found
        if found_chemicals:
            print("   Found chemicals:")
            for chem in found_chemicals:
                original_cas = cas_mapping[chem.cas]
                chemical_name = chemicals_of_interest.get(original_cas, "Unknown")
                print(f"     • {chemical_name} (EPI Suite CAS: {chem.cas} → Input CAS: {original_cas})")
        
        if not found_chemicals:
            print("❌ No chemicals found in EPI Suite database")
            return
        
        # Step 3: Submit chemicals for EPI Suite predictions
        print("\n⚗️  Submitting chemicals for EPI Suite predictions...")
        epi_results, ecosar_results = submit_to_episuite(found_chemicals)
        print(f"✅ Received predictions for {len(epi_results)} chemicals")
        
        # Step 4: Convert results to DataFrame
        print("\n📊 Converting results to DataFrame format...")
        episuite_df = episuite_to_dataframe(epi_results)
        
        print(f"✅ Created DataFrame with {len(episuite_df)} chemicals and {len(episuite_df.columns)} properties")
        print("\nKey properties included:")
        key_properties = [
            'cas', 'name', 'molecular_weight', 'log_kow_estimated', 
            'water_solubility_logkow_estimated', 'vapor_pressure_estimated',
            'henrys_law_constant_estimated', 'atmospheric_half_life_estimated',
            'bioconcentration_factor', 'log_koc_estimated'
        ]
        
        for prop in key_properties:
            if prop in episuite_df.columns:
                print(f"  ✓ {prop}")
        
        # Display summary of retrieved data
        print("\n📈 Summary of retrieved chemical data:")
        print("-" * 40)
        for idx, row in episuite_df.iterrows():
            print(f"\n{row['name']} (CAS: {row['cas']}):")
            print(f"  Molecular Weight: {row['molecular_weight']:.2f} g/mol")
            print(f"  Log Kow: {row['log_kow_estimated']:.2f}")
            if 'water_solubility_logkow_estimated' in row and pd.notna(row['water_solubility_logkow_estimated']):
                print(f"  Water Solubility: {row['water_solubility_logkow_estimated']:.2f} mg/L")
            if 'atmospheric_half_life_estimated' in row and pd.notna(row['atmospheric_half_life_estimated']):
                print(f"  Atmospheric Half-life: {row['atmospheric_half_life_estimated']:.1f} hours")
            if 'bioconcentration_factor' in row and pd.notna(row['bioconcentration_factor']):
                print(f"  Bioconcentration Factor: {row['bioconcentration_factor']:.1f}")
        
        # Step 5: Export to USEtox Excel format
        print("\n📤 Exporting to USEtox Excel format...")
        output_file = "usetox_chemical_data.xlsx"
        output_path = current_dir / output_file
        
        # Add some experimental data examples (optional)
        experimental_data = {
            "50-00-0": {  # Formaldehyde - add some experimental values
                "Sol25": 400.0,  # g/L (very high solubility)
                "Data source": "Experimental + PyEPISuite"
            }
        }
        
        try:
            # Create USEtox input file using the convenience function
            template_path = "data/usetox3/AA_Model_substance_data_Default.xlsx"
            usetox_result = create_usetox_input_from_episuite(
                episuite_df=episuite_df,
                output_path=str(output_path),
                template_path=template_path,
                experimental_data=experimental_data
            )
            
            print(f"\n🎉 Successfully created USEtox Excel file!")
            print(f"📁 File location: {output_path}")
            print(f"💾 File size: {output_path.stat().st_size / 1024:.1f} KB")
            
            # Display additional information about the export
            stats = usetox_result.get_summary_statistics()
            print(f"\n📊 Export Statistics:")
            print(f"  • Total chemicals: {stats['total_chemicals']}")
            print(f"  • Properties populated: {stats['properties_populated']}")
            print(f"  • Missing values: {stats['missing_values']}")
            
            # Show data source analysis
            source_analysis = usetox_result.get_data_source_analysis()
            print(f"\n🔍 Data Source Analysis:")
            for source_type, count in source_analysis.items():
                print(f"  • {source_type}: {count}")
            
            print(f"\n✨ The Excel file is ready for use with USEtox software!")
            print(f"📋 Key USEtox properties populated:")
            
            # Show which USEtox properties were successfully populated
            validation = usetox_result.validate_data()
            if validation['populated_properties']:
                for prop in validation['populated_properties'][:10]:  # Show first 10
                    excel_col = usetox_result.get_excel_column_letter(prop)
                    print(f"  ✓ {prop} (Excel column {excel_col})")
                if len(validation['populated_properties']) > 10:
                    print(f"  ... and {len(validation['populated_properties']) - 10} more properties")
            
            if validation['warnings']:
                print(f"\n⚠️  Warnings ({len(validation['warnings'])}):")
                for warning in validation['warnings'][:3]:  # Show first 3 warnings
                    print(f"  • {warning}")
                if len(validation['warnings']) > 3:
                    print(f"  ... and {len(validation['warnings']) - 3} more warnings")
            
        except Exception as e:
            print(f"❌ Error creating USEtox file: {e}")
            print("This might be due to missing USEtox template file or unit conversion issues.")
            print("Note: The USEtox module requires specific unit formats and template files.")
            print("Falling back to basic DataFrame export...")
            
            # Fallback: Export the DataFrame directly
            fallback_file = current_dir / "episuite_results_fallback.xlsx"
            episuite_df.to_excel(fallback_file, index=False)
            print(f"✅ Saved basic results to: {fallback_file}")
        
        # Step 6: Demonstrate additional USEtox features
        print(f"\n🔧 Additional Features Demonstrated:")
        print(f"  ✓ Automatic unit conversions (log Kow → Kow, mmHg → Pa)")
        print(f"  ✓ Experimental data prioritization over estimated values")
        print(f"  ✓ Excel column mapping for USEtox compatibility")
        print(f"  ✓ Data validation and quality checks")
        print(f"  ✓ Comprehensive data source tracking")
        
        print(f"\n📚 Next Steps:")
        print(f"  1. Open the Excel file in USEtox software")
        print(f"  2. Review and validate the populated data")
        print(f"  3. Add any missing experimental data manually")
        print(f"  4. Run USEtox calculations for environmental impact assessment")
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        print(f"Please check your internet connection and try again.")
        return 1
    
    return 0


if __name__ == "__main__":
    # Import pandas here to avoid issues if not available
    try:
        import pandas as pd
        import numpy as np
    except ImportError as e:
        print(f"❌ Error importing required packages: {e}")
        print("Please install required packages: pip install pandas numpy openpyxl")
        sys.exit(1)
    
    exit_code = main()
    sys.exit(exit_code)
