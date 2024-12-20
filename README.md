# PIPA
**PIPA** (Planetarium with Interstellar Positional Astronomy) is a free open source planetarium program based entirely on **Python3**. It uses the astrometric data from the **High Precision PARallax COllecting Satellite (Hipparcos)** mission to show in 3D what the sky from other stars would look like.

![alphacentauriA](/images/HIP71683.png)

The image above is a portion of the sky as seen from Alpha Centauri A (HIP 71683). Our star, the Sun, is shown in green for reference.

## Installation
The following libraries are required to run this project. The versions specified below have been tested for compatibility and are recommended for optimal performance:

### Required
- **python** == 3.9.20
- **vpython** == 7.6.5
- **skyfield** == 1.49
- **numpy** == 2.0.2  
- **pandas** == 2.2.3

### Environment Setup

We recommend creating a new Conda environment to manage dependencies and avoid conflicts with other projects. Follow these steps:

1. Create a new Conda environment (replace `<env_name>` with the name of your enviroment):
   ```
   conda create --name <env_name> python=3.9.20
   ```
2. Activate the environment:
    ```
    conda activate <env_name>
    ```
3. Install packages:
    ```
    conda install vpython=7.6.5 skyfield=1.49 numpy=2.0.2 pandas=2.2.3
    ```
4. To verify that the dependencies are correctly installed, you can list the installed packages:
    ```
    conda list
    ```

## Instructions
The code is pretty self-contained; just run ``pipa.py`` and a navigable 3D sky should start running in a browser window. If you want to see what the sky looks like from other stars, set `C_star` to the HIP ID of the star of interest. Note that the our Sun does not have a HIP ID, so set `C_star = -1` if you want to see the sky from Earth. If you want to render more stars, set `m_filt` to the largest apparent magnitude you want to be displayed.

```python
# Filtering Variables
m_filt = 6.5 # 6 is around the naked-eye limit

# HIP Number of the Center Star
C_star = 71683 # The Sun: -1
```

## Acknowledgments
This project made use of data from the **High Precision PARallax COllecting Satellite (Hipparcos)** mission. We specifically utilized the data published in:

ESA, 1997, The Hipparcos and Tycho Catalogues, ESA SP-1200

For further information on the Hipparcos mission and data, visit [ESA's Hipparcos page](https://www.cosmos.esa.int/web/hipparcos/catalogues).
