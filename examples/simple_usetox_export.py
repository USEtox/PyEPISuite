#!/usr/bin/env python3
"""
Simple PyEPISuite to Excel Export Example

This example demonstrates how to:
1. Search for chemicals by CAS numbers
2. Get EPI Suite predictions  
3. Convert to DataFrame
4. Export to Excel (USEtox-ready format)

This is a simplified version that focuses on the core functionality
without dependencies on external template files.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path for importing pyepisuite
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

def main():
    """Main function demonstrating the workflow."""
    
    print("🧪 PyEPISuite Simple Excel Export Example")
    print("=" * 45)
    
    try:
        from pyepisuite.utils import search_episuite_by_cas, submit_to_episuite
        from pyepisuite.dataframe_utils import episuite_to_dataframe
        import pandas as pd
        
        # Step 1: Define target chemicals
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
        
        print(f"\n📋 Searching for {len(target_chemicals)} chemicals:")
        for cas in target_chemicals:
            print(f"  • {chemical_names.get(cas, 'Unknown')} (CAS: {cas})")
        
        # Step 2: Search EPI Suite database
        print(f"\n🔍 Searching EPI Suite database...")
        chemical_ids = search_episuite_by_cas(target_chemicals)
        
        # Handle CAS number padding from EPI Suite
        def normalize_cas(cas_number):
            """Remove leading zeros from CAS number parts."""
            parts = cas_number.split('-')
            if len(parts) == 3:
                return f"{parts[0].lstrip('0') or '0'}-{parts[1].lstrip('0') or '0'}-{parts[2]}"
            return cas_number
        
        found_chemicals = []
        for chem in chemical_ids:
            normalized = normalize_cas(chem.cas)
            if normalized in target_chemicals:
                found_chemicals.append(chem)
                print(f"  ✅ Found: {chemical_names.get(normalized, 'Unknown')} ({chem.cas})")
        
        if not found_chemicals:
            print("❌ No chemicals found in EPI Suite database")
            return 1
        
        # Step 3: Get EPI Suite predictions
        print(f"\n⚗️  Getting EPI Suite predictions...")
        epi_results, ecosar_results = submit_to_episuite(found_chemicals)
        print(f"✅ Received predictions for {len(epi_results)} chemicals")
        
        # Step 4: Convert to DataFrame
        print(f"\n📊 Converting to DataFrame...")
        df = episuite_to_dataframe(epi_results)
        print(f"✅ DataFrame created: {df.shape[0]} chemicals × {df.shape[1]} properties")
        
        # Step 5: Prepare USEtox-compatible data
        print(f"\n🔧 Preparing USEtox-compatible data...")
        
        # Select and rename columns for USEtox compatibility
        usetox_mapping = {
            'cas': 'CAS_RN',
            'name': 'Chemical_Name', 
            'molecular_weight': 'MW_g_mol',
            'log_kow_estimated': 'Log_Kow',
            'water_solubility_logkow_estimated': 'Solubility_mg_L',
            'vapor_pressure_estimated': 'Vapor_Pressure_mmHg',
            'henrys_law_constant_estimated': 'Henrys_Constant_atm_m3_mol',
            'atmospheric_half_life_estimated': 'Atmospheric_Half_Life_hours',
            'log_koc_estimated': 'Log_Koc',
            'bioconcentration_factor': 'BCF',
            'river_half_life_hours': 'Water_Half_Life_hours',
        }
        
        # Create USEtox-ready DataFrame
        usetox_df = pd.DataFrame()
        for orig_col, new_col in usetox_mapping.items():
            if orig_col in df.columns:
                usetox_df[new_col] = df[orig_col]
        
        # Add derived/converted columns for USEtox
        if 'Log_Kow' in usetox_df.columns:
            usetox_df['Kow'] = 10 ** usetox_df['Log_Kow']  # Convert log Kow to Kow
        
        if 'Log_Koc' in usetox_df.columns:
            usetox_df['Koc'] = 10 ** usetox_df['Log_Koc']  # Convert log Koc to Koc
            
        # Add data source column
        usetox_df['Data_Source'] = 'PyEPISuite_Estimated'
        
        print(f"✅ USEtox-ready DataFrame created with {len(usetox_df.columns)} columns")
        
        # Step 6: Display summary
        print(f"\n📈 Chemical Data Summary:")
        print("-" * 35)
        
        for idx, row in usetox_df.iterrows():
            print(f"\n{row['Chemical_Name']} (CAS: {row['CAS_RN']}):")
            if 'MW_g_mol' in row and pd.notna(row['MW_g_mol']):
                print(f"  Molecular Weight: {row['MW_g_mol']:.2f} g/mol")
            if 'Log_Kow' in row and pd.notna(row['Log_Kow']):
                print(f"  Log Kow: {row['Log_Kow']:.2f}")
            if 'Kow' in row and pd.notna(row['Kow']):
                print(f"  Kow: {row['Kow']:.1f}")
            if 'Solubility_mg_L' in row and pd.notna(row['Solubility_mg_L']):
                print(f"  Water Solubility: {row['Solubility_mg_L']:.2f} mg/L")
            if 'BCF' in row and pd.notna(row['BCF']):
                print(f"  Bioconcentration Factor: {row['BCF']:.1f}")
        
        # Step 7: Export to Excel
        print(f"\n📤 Exporting to Excel...")
        
        output_file = current_dir / "pyepisuite_usetox_ready.xlsx"
        
        # Create Excel file with multiple sheets
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # USEtox-ready data
            usetox_df.to_excel(writer, sheet_name='USEtox_Ready', index=False)
            
            # Original full EPI Suite data
            df.to_excel(writer, sheet_name='Full_EPI_Suite_Data', index=False)
            
            # Summary sheet
            summary_data = {
                'Property': ['Number of Chemicals', 'Data Source', 'Export Date', 'Software'],
                'Value': [len(usetox_df), 'PyEPISuite API', pd.Timestamp.now().strftime('%Y-%m-%d'), 'PyEPISuite v1.0.0']
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"✅ Excel file created: {output_file}")
        print(f"💾 File size: {output_file.stat().st_size / 1024:.1f} KB")
        
        # Step 8: Show what's included
        print(f"\n📋 Excel file contains:")
        print(f"  📊 Sheet 'USEtox_Ready': {len(usetox_df)} chemicals with USEtox-compatible properties")
        print(f"  📊 Sheet 'Full_EPI_Suite_Data': Complete EPI Suite results ({len(df.columns)} properties)")
        print(f"  📊 Sheet 'Summary': Export metadata and information")
        
        print(f"\n🔧 USEtox-compatible properties included:")
        for col in usetox_df.columns:
            non_null_count = usetox_df[col].notna().sum()
            print(f"  • {col}: {non_null_count}/{len(usetox_df)} values")
        
        print(f"\n🎉 Export completed successfully!")
        print(f"📚 Next steps:")
        print(f"  1. Open the Excel file to review the data")
        print(f"  2. Use the 'USEtox_Ready' sheet for USEtox import")
        print(f"  3. Refer to 'Full_EPI_Suite_Data' for complete property information")
        print(f"  4. Import into USEtox software for environmental impact assessment")
        
        return 0
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure PyEPISuite is installed: pip install -e .")
        return 1
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
