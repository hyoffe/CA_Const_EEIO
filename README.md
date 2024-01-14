# Setting National Construction Sector GHG Budgets
EEIO/CA Model for construction emissions

##Overview:
The code in this folder supports the study on Canada's construction greenhouse gas emissions.
The code uses an EEIO approach based on openIO Canada. CIRAIG's MRIO model.
A preprint summary of this work is found at: https://csbe.civmin.utoronto.ca/research/ghg-emissions-in-canadas-construction-sector/

## Citation
If you use or refer to the results, calculations, or data from this repository, please cite the original study: 
Yoffe, H., Rankin, K. H., Bachmann, C., Posen, I. D., & Saxe, S. (2023). Setting National Construction Sector GHG Budgets. (Under review) [https://csbe.civmin.utoronto.ca/research/ghg-emissions-in-canadas-construction-sector/]

## Usage
To use the code:
1. generate the IOtables from Open IO Canada @ https://ciraig.org/index.php/project/open-io-canada/
generated tables are used as tanles.Y -> tables_Y , tables.A ->Tables_A etc.

2. run each notebook file following the instructions.
Datafiles include summary CSVs and DF used to generate analysis and classification of emissions by province, materials, origin, etc.

## Files and Directory Structure
### Data Files:
Files in the Data folder include exports:
1. ca_gfcf_co2e_by_country.csv 
    Total emission by country, kgCO2e, consumption.
2. ca_gfcf_construction_co2e.csv
    DF (16197 rows x 13 columns) Gross fixed capital formation -construction emissions for each Canadian province/territory. Rows include all 492/200 commodities for each DF (16197 rows x 13 columns) province/country of source origin.
    Calculated by (CS)(L(Ydiag))diag
3. ca_gfcfc_material_emissions_by_const_sector.csv
    DF (23 rows x 54 columns) summary of emission type across all construction sectors
    calculated by (CS)(A(Ydiag))diag + (CS)Y(diag)
4. ca_res_struct_CO2e.csv
    Residential structure emissions across Canadian provinces and territories. KgCO2e consumption.
    Calculated by (CS)(L(Ydiag))diag
5. province_construction_emissions_ciraig.csv - 
    Comparison emission table for
    GFCFC(CIRAIG) / Residential_buildign(CIRAIG) / res build(StatCA, 0.27 multiplier)

### \Data\lists
1. material_lca_classification09.csv
    material mapping. used to generate source type (LCA A1-A5) analysis
2. material_lca_classification09_lean.csv
    Lean material mapping file is used to generate Sankey diagrams. The file aggregates small emission types to Other.
### \Data\Sankey
includes DF files to generate the Sankey diagram (used by 006_plot_material_sankey02ipynb)

# Calculation Files include:
001_LY
    Example code for calculating sector emissions (CS)(LY) - for each commodity
    Dataframe - Residential building DF. CA by province. (CS)(LY)
    Dataframe - GFCF DF. CA by province. (CS)(LY)

002_ALY+Y (LCA)_02
    Calculates the total emissions of GFCG Construction and presents it in a Lifecycle emission approach (Blue): 
    Product (A1-A3) and construction (A4-A5) stage by the intermediate output. i.e. the LCA emissions of each commodity.

003_X
1. Comparison emission table for GFCF construction (CIRAIG) / Residential_buildign (CIRAIG) / res build(StatCA, 0.27 multiplier)
2. Emission/msq for Residential construction calculation based on natural resource Canada data residential development/yr data (kgCO2e/m2)

004_total_economy
1. calculates the total emissions of Canada's economy

006_plot_sankey_lean_02_BlueGreen
1. File for generating Sankey diagrams - requires DF CSV generated in 007

007_material_by_gfcfs_const_DF
1. Creating a DF of emissions from all gfcfc sub-sectors (tables_Y) - classifies by material list
    1.1 calc each gfcfc sub-sector separately and concatenate to one DF
    1.2 calc each province gfcfc and sub-sectors separately and join them to one DF
    Material classification added
2. Requieres material classification list file (in Lists folder).
3. This file also generates the total output X tables for GFCF construction in all sectors.
   long proceesssing time (requieres CIRAIGs A,L,Y,C,S tables)
009_plot_world_lc_green
1. Creates global emission source maps (consumption)

010_material_analysis_res
1. Creates an all-province DF for the residential GFCFC sub-sector. Maps material classification of commodities
   requires total output data frames and material classification DF.


   ## License

This project is licensed under the MIT License

### MIT License

MIT License

Copyright (c) 2023, Hatzav Yoffe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.