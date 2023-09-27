import streamlit as st
from pathlib import Path
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="Thin Film Analysis",
    page_icon="🔬",
    layout="wide"
)

# Define paths to CSS and images
current_dir = Path(__file__).parent
css_file = current_dir / "styles" / "main.css"
textFile1 = current_dir / "assets" / "E1.txt"
textFile2 = current_dir / "assets" / "E2.txt"
textFile3 = current_dir / "assets" / "E3.txt"
pic1 = current_dir / "assets" / "2-1.jpg"
pic2 = current_dir / "assets" / "Absorbance.png"
pic3 = current_dir / "assets" / "Reflectance.png"
pic4 = current_dir / "assets" / "Thickness.png"
pic5 = current_dir / "assets" / "Current_density.png"


# Load CSS
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

pic1 = Image.open(pic1)
pic2 = Image.open(pic2)
pic3 = Image.open(pic3)
pic4 = Image.open(pic4)
pic5 = Image.open(pic5)

# User information
email = "Eliaimafidon234@gmail.com"
project_description = "A data analysis web app for thin film semiconductors"
project_type = "Thin Film Semiconductor Data Analysis"
creator = "Created by: Imafidon Oisedebame E"
date = "1 September 2023"

# Define social media links
if "social_media" not in st.session_state:
    st.session_state.social_media = {
    "Linktree": "https://linktr.ee/imafidon_oe",
    "LinkedIn": "https://linkedin.com/in/oisedebame-imafidon-92921b228",
    "Github": "https://github.com/OisedebameE",
    "Twitter": "https://twitter.com/imafidon_oe",
    "Medium": "https://medium.com/@Imafidon.E.O",
    "Substack": "https://imafidon_oe.substack.com/"
    }

# Contact form HTML
contact_form = """
<form action = "https://formsubmit.co/Eliaimafidon234@gmail.com" method = "POST">
    <input type = "hidden" name= "_captcha" value = "false">
    <input type = "text" name = "name" placeholder = "Your name" required>
    <input type = "email" name = "email" placeholder = "Your email" required>
    <textarea name ="message" placeholder = "Your message here"></textarea>
    <button type = "submit">Send</button>
</form>
"""
# Table of contents
table_of_contents = """
    ✅ Introduction\n
    ✅ Objective\n
    ✅ Analysis Approach\n
    ✅ Academic Use Case\n
    ✅ Example: Personal Project\n
    ✅ Key Findings\n
    ✅ Conclusion\n
    ✅ Appendix
"""

# Introduction
introduction = """A semiconductor is a material that exhibits moderate electrical conductivity, 
falling between insulators and conductors. It acts as an insulator at extremely low temperatures 
and demonstrates some electrical conductivity at room temperature, although less than conductors (e.g., copper) and insulators (e.g., quartz). 
Semiconductors vary in resistance, typically ranging between 10^-5 and 100 ohm meters. 
They serve as the foundation for advanced solar panels.\n
Thin film solar cells represent a novel solar technology that surpasses traditional C-Si solar cells. 
A thin film is a layer of material, just a few nanometers to micrometers thick, which enhances the properties of the underlying material. 
This layer is applied through deposition, a process that conserves materials, resulting in a lightweight, cost-efficient, and environmentally friendly solution.\n
One method for creating thin film semiconductor solar cells is electrodeposition, 
which allows us to adjust the material's band gap by depositing metals or semiconductors onto a conductive surface using an electric current passed through an electrolyte containing metal or semiconductor ions. This technique builds upon Michael Faraday's discovery of electrolysis in 1834.
"""

# Objective
objective = """This analytical web app aims to provide insights into the optical and electrical properties of semiconductor thin films.
The objectives include:\n
⏩ Generating a dataset for evaluating thin film performance across specific parameters.\n
⏩ Understanding overall thin film performance through visualization of various properties.\n
⏩ Providing a theoretical estimation of thin film thickness.
"""

# Academic use case
academic_use_case = """Researchers in condensed matter physics can utilize this web app to understand 
the behavior of semiconductor thin films under various growth conditions through automating the creation of necessary datasets which can be visualized on the platform."""

# Personal project example
personal_project = """For a personal project, three samples of copper selenide (CuSe) thin film were prepared using the electrodeposition technique at a consistent pH of 2.40 ± 0.02 and a temperature of 60°C. 
These samples were deposited on glass slides/FTO at different cathodic potentials: -800 mV, -1000 mV, and -1200 mV, labeled as E1, E2, and E3 respectively. After conducting UV/VIS spectrophotometer and PEC cell tests, the data was obtained and analyzed.
The data obtained for the thin films from the UV/VIS spectrophotometer are in text format and examples of them are as followed:"""

# Optical properties
optical_properties = """
        #### Optical properties:\n
        The optical properties of a material referred to its interactions with electromagnetic radiation in the visible, ultraviolet, and infrared regions of the electromagnetic spectrum. 
        These interactions can include absorption, reflection, transmission, etc.\n
        Note: 
        The spectroscopy data ranges from an electromagnetic (EM) spectrum wavelength of 300 nm to 900 nm. 
        However, due to the solar spectrum's composition of visible and ultraviolet regions, the graph begins at 420 nm. 
        This implies that the thin film's behavior is prominent in the visible and ultraviolet regions of the EM spectrum.
        """
absorbance = """
        ##### Absorbance\n 
        The absorbance response of the CuSe thin films shows a clear relationship with incident photon wavelength, with higher deposition voltages leading to increased absorbance. """
reflectance = """
        ##### Reflectance\n
        Reflectance spectra exhibit low values across the visible to near-infrared regions, indicating the potential efficiency of CuSe thin films in electronic devices, 
        particularly as absorber layers in thin-film solar cells."""
summary = """
        These optical properties suggest that CuSe thin films are well-suited for applications requiring efficient absorption of electromagnetic radiation."""

# Electrical properties
electrical_properties = """
         #### Electrical properties:\n
         Electrical properties of a material referred to how it behaves in the presence of an electric field or an electric current. 
         These properties are determined by the electronic structure of the material, and they are important in many applications, including electronics, power generation, and energy storage."""
thickness = """
             ##### Thickness\n
             The thickness of CuSe layers is directly proportional to the deposition voltage, with higher cathodic potentials resulting in thicker layers. 
             This trend aligns with Faraday's first and second laws of electrolysis."""
current_density = """
        ##### Current density\n
        Deposition voltage positively correlates with deposition current density, consistent with Ohm's law."""
conclusion = """
            ### Conclusion\n
            This analytical web application offers an efficient and time-saving solution for scientists in their research of semiconductor thin film technology in the field of condensed matter physics.
            It enables the rapid evaluation of thin film performance across specific parameters by automating the creation of necessary datasets which can be visualized on the same platform.
            The insights gained from the visualization further emphasize the potential of CuSe thin films in electronic devices, particularly in the development of thin-film solar cells.
            This web application represents a significant advancement in the field, enabling the analysis of multiple thin films in a fraction of the time it would take using traditional data visualization tools methods. Researchers can now explore a broader range of possibilities and accelerate their research efforts."""
appendix = """
           ### Appendix\n
           Additional data and detailed experimental procedures are available in the appendix for reference and further analysis."""

# User interface layout
col1, col2 = st.columns(2, gap="small")
with col2:
    st.write(project_description)
    st.title(project_type)
    st.write(creator)
    st.write(date)
    st.write(email)

with col1:
    st.image(pic1, use_column_width=True)

st.write("#")
st.write("## Table of Contents")
st.write(table_of_contents)
st.write("#")
st.subheader("Introduction")
st.write(introduction)
st.write("#")
st.subheader("Objective")
st.write(objective)
st.write("#")
st.subheader("Academic Use Case")
st.write(academic_use_case)
st.write("#")
st.write("---")
st.subheader("Personal Project")
st.write(personal_project)
st.download_button(label="E1.txt", data=open(textFile1, "rb").read(), file_name="E1", mime="text/csv")
st.download_button(label="E2.txt", data=open(textFile2, "rb").read(), file_name="E2", mime="text/csv")
st.download_button(label="E3.txt", data=open(textFile3, "rb").read(), file_name="E3", mime="text/csv")
st.write("#")
st.write("## Key findings")
st.write(optical_properties)
st.write("#")
st.write(absorbance)
st.image(pic2, use_column_width=True)
st.write("#")
st.write(reflectance)
st.image(pic3, use_column_width=True)
st.write("#")
st.write(summary)
st.write("#")
st.write(electrical_properties)
st.write("#")
st.write(thickness)
st.image(pic4, use_column_width=True)
st.write("#")
st.write(current_density)
st.image(pic5, use_column_width=True)
st.write("#")
st.write("Read more about the project")
st.markdown('[Here](https://medium.com/@Imafidon.E.O/condensed-matter-research-effect-of-varying-deposition-cathodic-potential-on-the-optoelectronic-827d3df710a6)')
st.write("---")
st.write("#")
st.write(conclusion)
st.write("#")
st.write(appendix)
st.markdown('[Here](https://medium.com/@Imafidon.E.O)')
st.write("---")
col3, col4 = st.columns([1,3])
with col4:
    st.header("""Get in touch with me 📮""")
    st.markdown(contact_form, unsafe_allow_html= True)
st.write("---")

# Render social media links
cols = st.columns(len(st.session_state.social_media))
for index, (platform, link) in enumerate(st.session_state.social_media.items()):
    cols[index].write(f"[{platform}]({link})")
