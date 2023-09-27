import streamlit as st
import pandas as pd
import numpy as np
import csv
from openpyxl import Workbook
import altair as alt
from pathlib import Path

#General settings
st.set_page_config(page_title="Thin film analysis", page_icon="🔬", layout="wide")

if "social_media" not in st.session_state:
    st.session_state.social_media = {
    "Linktree": "https://linktr.ee/imafidon_oe",
    "LinkedIn": "https://linkedin.com/in/oisedebame-imafidon-92921b228",
    "Github": "https://github.com/OisedebameE",
    "Twitter": "https://twitter.com/imafidon_oe",
    "Medium": "https://medium.com/@Imafidon.E.O",
    "Substack": "https://imafidon_oe.substack.com/"
    }

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent
css_file = current_dir / "styles" / "main.css"

# --- LOAD CSS & PICTURES ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
                      
st.title("Enter user data")

#Accepting user data
thinfilmNo = st.number_input("How many thin films?", min_value=0, max_value=100, step=1, value=0, format="%d")

sampleIDs = []
deposition_voltages = []
times = []
temps = []
pHs = []
molar_masses = []
densities = []
ns = []
currents = []
areas = []
PECs = []
text_files = []
excel_files = []
mean_dict = {}

for i in range(int(thinfilmNo)):
    sampleID = st.text_input(f"Enter sampleID {i+1}:")
    sampleIDs.append(sampleID)

    deposition_voltage = st.number_input(f"Enter {sampleID} Deposition Voltage:", min_value=0, max_value=10000, step=1, value=0, key=f"deposition_voltage_{i}")
    deposition_voltages.append(deposition_voltage)

    time = st.number_input(f"Enter {sampleID} Deposition Time (secs):", min_value=0, max_value=50000, step=1, value=0, key=f"time_{i}")
    times.append(time)

    temp = st.number_input(f"Enter {sampleID} Temperature (C):", min_value=0, max_value=200, step=1, value=0, key=f"temp_{i}")
    temps.append(temp)

    pH = st.number_input(f"Enter {sampleID} pH:", min_value=0.0, max_value=14.0, step=0.1, value=0.0, key=f"pH_{i}")
    pHs.append(pH)

    molar_mass = st.number_input(f"Enter {sampleID} Molar Mass (g/mol):", min_value=0.0, max_value=50000.0, step=0.1, value=0.000,format= "%f", key=f"molar_mass_{i}")
    molar_masses.append(molar_mass)

    density = st.number_input(f"Enter {sampleID} Density (g/cm^3):", min_value=0.0, max_value=5000.0, step=0.1, value=0.00,format= "%f", key=f"density_{i}")
    densities.append(density)

    n = st.number_input(f"Enter {sampleID} n-Value:", min_value=0.0, max_value=10000.0, step=0.1, value=0.0000,format= "%f", key=f"n_{i}")
    ns.append(n)

    current = st.number_input(f"Enter {sampleID} Current (A):", min_value=0.000000, max_value=10000.0, step=0.001, value=0.0000,format="%.7f", key=f"current_{i}")
    currents.append(current)

    area = st.number_input(f"Enter {sampleID} Area (cm^2):", min_value=0.0, max_value=1000.0, step=0.1, value=0.0,format= "%f", key=f"area_{i}")
    areas.append(area)

    PEC = st.number_input(f"Enter {sampleID} P.E.C (V):", min_value=0.0, max_value=1000.0, step=0.1, value=0.00000,format="%.5f", key=f"PEC_{i}")
    PECs.append(PEC)

    txt_file = st.file_uploader(f"Upload text file for {sampleID}", type=["txt"], key=f"text_file_{i}")
    text_files.append(txt_file)

Input_data = {
    "sampleID": sampleIDs,
    "Cathodic Deposition Voltage (mV)": deposition_voltages,
    "Deposition Time (sec)": times,
    "Deposition Temperature (C)": temps,
    "pH": pHs,
    "Molar_Mass (g/mol)": molar_masses,
    "Density (g/dm^3)": densities,
    "n value": ns,
    "Current (amps)": currents,
    "Area (cm^2)": areas,
    "PEC signal (V)": PECs,
}
st.session_state.Input_dataset = pd.DataFrame(Input_data)

# Basic data exploration analysis
st.session_state.Input_dataset["Average current density (Acm^-2)"] = st.session_state.Input_dataset["Current (amps)"] / st.session_state.Input_dataset["Area (cm^2)"]
st.session_state.Input_dataset["Thickness (cm)"] = (st.session_state.Input_dataset["Average current density (Acm^-2)"] * st.session_state.Input_dataset["Deposition Time (sec)"] * st.session_state.Input_dataset["Molar_Mass (g/mol)"]) / (st.session_state.Input_dataset["n value"] * st.session_state.Input_dataset["Density (g/dm^3)"] * 96485)
st.session_state.Input_dataset["Thickness (nm)"] = st.session_state.Input_dataset["Thickness (cm)"] * 10000000
st.session_state.Input_dataset["PEC signal (mV)"] = st.session_state.Input_dataset["PEC signal (V)"] * 1000

wavelengths = []
absorbances = []
transmittances = []
reflectancess = []
absorption_coeffs = []
refractive_indexs = []
extinction_coeffs = []
optical_conds = []
dielectric_cons = []

#Converting and clean txt file to excel file.
for txt_data in text_files:
    if txt_data is not None:
        text_file_content = txt_data.read().decode("utf-8")
        reader = csv.reader(text_file_content.splitlines())
        data = list(reader)

        workbook = Workbook()
        sheet = workbook.active
        file_name = txt_data.name.split(".")[0]
        headings = [f"{file_name} Wavelength(nm)", f"{file_name} Absorbance(arbunit)"]
        sheet.append(headings)

        for row in data:
            sheet.append(row)

        excel_file = f"data.xlsx"
        workbook.save(excel_file)

        single_excel_file = pd.read_excel(excel_file)

        single_excel_file[f"{file_name} Wavelength(nm)"] = pd.to_numeric(single_excel_file[f"{file_name} Wavelength(nm)"], errors='coerce')
        single_excel_file[f"{file_name} Absorbance(arbunit)"] = pd.to_numeric(single_excel_file[f"{file_name} Absorbance(arbunit)"], errors='coerce')
        
        filtered_excel_file = single_excel_file[(single_excel_file[f"{file_name} Wavelength(nm)"] >= 300.0) & (single_excel_file[f"{file_name} Wavelength(nm)"] <= 900.0)]

        #Making colunm names formatable.
        absorbance_arb = f"{file_name} Absorbance(arbunit)"
        wavelength_nm = f"{file_name} Wavelength(nm)"
        absorbance_nm_2 = f"{file_name} Absorbance(arbunit)^2"
        absorbance_nm_half = f"{file_name} Absorbance(arbunit)^(1/2)"
        wavelength_cm = f"{file_name} Wavelength(cm)"
        wavelength_m = f"{file_name} Wavelength(m)"
        transmittance_arb = f"{file_name} Transmittance(arbunit)"
        reflectance_arb = f"{file_name} Reflectance(arbunit)"
        abs_tran_ref = f"{file_name} Ref+Tran+Abs"
        Eg = f"{file_name} PhotonEnergy(Eg)"
        n = f"{file_name} RefractiveIndex(n)"
        alpha = f"{file_name} AbsorptionCoefficient(a)nm^-1"
        alpha_cm = f"{file_name} AbsorptionCoefficient(a)cm^-1"
        K = f"{file_name} ExtinctionCoefficient(K)"
        opt = f"{file_name} OpticalConductivity(O)(s^-1)"
        Er = f"{file_name} Er"
        Ei= f"{file_name} Ei"
        E = f"{file_name} DielectricConstant(E=Er+Ei)"
        alpha_hv = f"{file_name} ahv"
        alpha_hv_2 = f"{file_name} ahv^2"

        # More basic data exploration analysis to produce useful columns
        filtered_excel_file[absorbance_nm_2] = filtered_excel_file[absorbance_arb] ** 2
        filtered_excel_file[absorbance_nm_half] = np.sqrt(filtered_excel_file[absorbance_arb])
        filtered_excel_file[wavelength_cm] = filtered_excel_file[wavelength_nm] * 0.0000001
        filtered_excel_file[wavelength_m] = filtered_excel_file[wavelength_cm] / 100
        filtered_excel_file[transmittance_arb] = np.exp(-2.303 * filtered_excel_file[absorbance_arb])
        filtered_excel_file[reflectance_arb] = 1 - (filtered_excel_file[absorbance_arb] + filtered_excel_file[transmittance_arb])
        filtered_excel_file[abs_tran_ref] = filtered_excel_file[absorbance_arb] + filtered_excel_file[transmittance_arb] + filtered_excel_file[reflectance_arb]
        filtered_excel_file[Eg] = 1240 / filtered_excel_file[wavelength_nm]
        filtered_excel_file[n] = (1 + np.sqrt(filtered_excel_file[reflectance_arb])) / (1 - np.sqrt(filtered_excel_file[reflectance_arb]))

        for index, row in st.session_state.Input_dataset.iterrows():
            thickness = row["Thickness (nm)"]
            filtered_excel_file[alpha] = ((2.303 * filtered_excel_file[absorbance_arb]) / thickness)
            filtered_excel_file[alpha_cm] = ((2.303 * filtered_excel_file[absorbance_arb]) / (thickness * 0.0000001))
            filtered_excel_file[K] = ((filtered_excel_file[alpha_cm] * filtered_excel_file[wavelength_cm]) / (4 * np.pi))
            filtered_excel_file[opt] = ((filtered_excel_file[n] * filtered_excel_file[K] * 299792458) / filtered_excel_file[wavelength_m])
            filtered_excel_file[Er] = (filtered_excel_file[n].pow(2)) + (filtered_excel_file[K].pow(2))
            filtered_excel_file[Ei] = (2 * filtered_excel_file[n] * filtered_excel_file[K])
            filtered_excel_file[E] = filtered_excel_file[Er] + filtered_excel_file[Ei]
            filtered_excel_file[alpha_hv] = filtered_excel_file[Eg] * filtered_excel_file[alpha_cm]
            filtered_excel_file[alpha_hv_2] = filtered_excel_file[alpha_hv].pow(2)

        absorbance = filtered_excel_file[absorbance_arb].mean()
        transmittance = filtered_excel_file[transmittance_arb].mean()
        reflectances = filtered_excel_file[reflectance_arb].mean()
        absorption_coeff = filtered_excel_file[alpha_cm].mean()
        refractive_index = filtered_excel_file[n].mean()
        extinction_coeff = filtered_excel_file[K].mean()
        optical_cond = filtered_excel_file[opt].mean()
        dielectric_con = filtered_excel_file[E].mean()

        absorbances.append(absorbance)
        transmittances.append(transmittance)
        reflectancess.append(reflectances)
        absorption_coeffs.append(absorption_coeff)
        refractive_indexs.append(refractive_index)
        extinction_coeffs.append(extinction_coeff)
        optical_conds.append(optical_cond)
        dielectric_cons.append(dielectric_con)

        # Append the filtered_excel_file to excel_files
        excel_files.append(filtered_excel_file)
        
optical_data = {
    'sampleID': sampleIDs,
    'Average Absorbance (A)': absorbances,
    'Average Transmittance (T)': transmittances,
    'Average Reflectance(R)': reflectancess,
    'Absorption coefficient(a)cm^-1': absorption_coeffs,
    'Refractive index(n)': refractive_indexs,
    'Extinction coefficient(K)': extinction_coeffs,
    'Optical conductivity(O)(s^-1)':optical_conds,
    'Dielectric constant(E=Er+Ei)': dielectric_cons,
}

if ((len(excel_files) == thinfilmNo) & (thinfilmNo != 0)):
    st.session_state.Optical_data = pd.DataFrame(optical_data)
    st.success("👍🏻 files uploaded successfully")
    st.write("---")
    st.session_state.ThinfilmDataset = pd.concat(excel_files, axis=1)
    st.session_state.ThinfilmDataset.fillna(0, inplace=True)

    # Save data to CSV
    general_csv_file_path = "ThinfilmDataset.csv"
    st.session_state.ThinfilmDataset.to_csv(general_csv_file_path, index=False)
    
    optical_csv_file_path = "Optical_ThinfilmDataset.csv"
    st.session_state.Optical_data.to_csv(optical_csv_file_path, index=False)

    electrical_csv_file_path = "Electrical_ThinfilmDataset.csv"
    st.session_state.Input_dataset.to_csv(electrical_csv_file_path, index=False)
    
    #Downloading user data
    st.session_state.number_of_roles = 5
    st.table(st.session_state.Optical_data)

    st.markdown("### Download your optical dataset")
    st.download_button(label="Click me", data=open(optical_csv_file_path, "rb").read(), file_name=optical_csv_file_path, mime="text/csv")
    st.write("---")

    st.dataframe(st.session_state.Input_dataset)
    st.markdown("### Download your electrical dataset")
    st.download_button(label="Click me", data=open(electrical_csv_file_path, "rb").read(), file_name=electrical_csv_file_path, mime="text/csv")
    st.write("---")

    decrement = st.button("Show fewer columns")
    increment = st.button("Show more columns")

    if increment:
        st.session_state.number_of_roles +=1

    if decrement:
        st.session_state.number_of_roles -=1

    
    st.dataframe(st.session_state.ThinfilmDataset.head(st.session_state.number_of_roles))
    st.markdown("### Download your complete dataset")
    st.download_button(label="Click me", data=open(general_csv_file_path, "rb").read(), file_name="ThinfilmDataset.csv", mime="text/csv")
    st.success("You can now visualize your data")
    st.write("---")

#Preping user visualization from thin film dataset       
if "ThinfilmDataset" in st.session_state:
    st.success("👈 Click on the sidebar to create and customize your graph ")
    st.sidebar.title("Format chat")
    visualization_type = st.sidebar.radio ("View graphs", ["Optical properties","Electrical properties"])
    if visualization_type == "Optical properties":
        x_column = st.sidebar.selectbox('Select the column for the X-axis', st.session_state.ThinfilmDataset.columns)
        y_columns = st.sidebar.multiselect('Select the column(s) for the Y-axis', st.session_state.ThinfilmDataset.columns)
        x_axis_title = st.sidebar.text_input("Enter x axis title:")
        y_axis_title = st.sidebar.text_input("Enter y axis title:")
        if y_columns:
            x_slider = st.sidebar.slider('Select the values for X-axis',
                                float(st.session_state.ThinfilmDataset[x_column].min()),
                                float(st.session_state.ThinfilmDataset[x_column].max()),
                                (float(st.session_state.ThinfilmDataset[x_column].min()), float(st.session_state.ThinfilmDataset[x_column].max())))
            st.session_state.filtered_dataset = st.session_state.ThinfilmDataset[(st.session_state.ThinfilmDataset[x_column] >= x_slider[0]) & (st.session_state.ThinfilmDataset[x_column] <= x_slider[1])]
            y_columns_data = st.session_state.filtered_dataset[y_columns]
            y_min = y_columns_data.min().min()
            y_max = y_columns_data.max().max()

            y_min = float(y_min) if not pd.isna(y_min) else float(y_columns_data.min().dropna().min())
            y_max = float(y_max) if not pd.isna(y_max) else float(y_columns_data.max().dropna().max())

            y_slider = st.sidebar.slider('Select the values for Y-axis', y_min, y_max, (y_min, y_max))

            st.session_state.filtered_dataset = st.session_state.filtered_dataset.dropna(subset=y_columns, how='any')
            st.session_state.filtered_dataset = st.session_state.filtered_dataset[(st.session_state.filtered_dataset[y_columns].min(axis=1) >= y_slider[0]) & (st.session_state.filtered_dataset[y_columns].max(axis=1) <= y_slider[1])]

            melted_data = st.session_state.filtered_dataset.melt(id_vars=[x_column], value_vars=y_columns)

            chart = alt.Chart(melted_data).mark_line().encode(
            x=alt.X(x_column, type='quantitative', title=x_axis_title),
            y=alt.Y('value:Q', title=y_axis_title),
            color= 'variable:N',
            ).properties(
                width=1000,
                height=600
                ).interactive()
            chart = chart.configure_axis(
            grid=False,
            domain=True,
            labelFontSize=14,
            titleFontSize=18,
            tickColor='#000000',    # Tick color (same as background color)
            )

            st.write("#")
            st.success("You can save your plot 👉🏻")
            st.altair_chart(chart)
            st.write("---")
            st.write(f"Plotting line graph of {x_column} vs {', '.join(y_columns)}")
        else:
            st.write("Please select at least one column for the Y-axis.")
                                                
    if visualization_type == "Electrical properties":
        
        X_columns = st.sidebar.selectbox('Select the column for the X-axis', st.session_state.Input_dataset.columns)
        Y_columns = st.sidebar.multiselect('Select the column(s) for the Y-axis', st.session_state.Input_dataset.columns)
        X_axis_title = st.sidebar.text_input("Enter X axis title:")
        Y_axis_title = st.sidebar.text_input("Enter Y axis title:")

        if Y_columns:
            X_slider = st.sidebar.slider('Select the values for X-axis',
                                            float(st.session_state.Input_dataset[X_columns].min()),
                                            float(st.session_state.Input_dataset[X_columns].max()),
                                            (float(st.session_state.Input_dataset[X_columns].min()), float(st.session_state.Input_dataset[X_columns].max())))

            st.session_state.filtered_datasets = st.session_state.Input_dataset[
                (st.session_state.Input_dataset[X_columns] >= X_slider[0]) & (st.session_state.Input_dataset[X_columns] <= X_slider[1])
            ]

            Y_columns_data = st.session_state.filtered_datasets[Y_columns]
            Y_min = Y_columns_data.min().min()
            Y_max = Y_columns_data.max().max()

            Y_min = float(Y_min) if not pd.isna(Y_min) else float(Y_columns_data.min().dropna().min())
            Y_max = float(Y_max) if not pd.isna(Y_max) else float(Y_columns_data.max().dropna().max())

            Y_slider = st.sidebar.slider('Select the values for Y-axis', Y_min, Y_max, (Y_min, Y_max))

            st.session_state.filtered_datasets = st.session_state.filtered_datasets.dropna(subset=Y_columns, how='any')
            st.session_state.filtered_datasets = st.session_state.filtered_datasets[
                (st.session_state.filtered_datasets[Y_columns].min(axis=1) >= Y_slider[0]) & (st.session_state.filtered_datasets[Y_columns].max(axis=1) <= Y_slider[1])
            ]
            
            melted_Data = st.session_state.filtered_datasets.melt(id_vars=[X_columns], value_vars=Y_columns)

            chart_electric = alt.Chart(melted_Data).mark_line().encode(
                x=alt.X(X_columns, type='quantitative', title=X_axis_title),
                y=alt.Y('value:Q', title=Y_axis_title),
                color= alt.Color('variable:N').legend(None),
            ).properties(
                width=1000,
                height=600
            ).interactive()
            chart_electric = chart_electric.configure_axis(
            grid=False,
            domain=True,
            labelFontSize=14,
            titleFontSize=18,
            tickColor='#000000',    # Tick color (same as background color)
            )
        
            
            st.write("#")
            st.success("You can save your plot 👉🏻")
            st.altair_chart(chart_electric)

            st.write("#")
            st.write(f"Plotting line graph of {X_columns} vs {', '.join(Y_columns)}")
            st.write("---")
            
            cols = st.columns(len(st.session_state.social_media))
            for index, (platform, link) in enumerate(st.session_state.social_media.items()):
                cols[index].write(f"[{platform}]({link})")
        else:
            st.write("Please select at least one column for the Y-axis.")
