
## <a name="task10"></a>Task 11 - Options for making materials

Google Colab Link: [Task_11](https://colab.research.google.com/drive/1pY3dcsHu7nC3Mv3WmqUWLSCzr0gaeuvE).

Please allow 20 minutes for this task.

Expected outputs from this task are in the [presentation](https://slides.com/openmc_workshop/neutronics_workshop#/23).

Material construction is a fundamental part of creating neutronics models. This task aims to demonstrate material construction in greater depth than previously seen.

There are several ways to create neutronics materials - OpenMC itself can be used, however, other tools also exist. In this task, we will look at the [neutronics_material_maker](https://github.com/ukaea/neutronics_material_maker/tree/openmc_version); an open source code which aims to simplify material creation for use in neutronics models.

### Creating materials using in-build OpenMC functions

First, we will look at how materials can be created in OpenMC. OpenMC offers the ability to create materials from isotopes and elements, where elements are a combination of all naturally occurring isotopes at natural abundance. Specific isotopes, rather than elements, are required in some circumstances such as creating a material with a particular composition.

**Creating Materials from isotopes**

Here, we will create some materials purely using isotopes.

Open the script below which shows how to create two materials from isotopes.

```1_example_materials_from_isotopes.py```

Look through the script and try to understand how this is done.

As shown, a material object is specified with a name, to which isotopes can be added using the *add_nuclide* function. The material density can also be set using the *set_density* function.

The script shows how water can be created. To do this, all natural isotopes of hydrogen and oxygen must be combined at their natural abundances. To make this easier, we use the NATURAL_ABUNDANCE dictionary which contains the relative natural abundances of each isotope for each element.

- Try making Lithium Orthosilicate (Li4SiO4) from isotopes using the NATURAL_ABUNDANCE dictionary. HINT: Take a look at the [data.py](https://github.com/openmc-dev/openmc/blob/develop/openmc/data/data.py) script to see which isotopes exist in the NATURAL_ABUNDANCE dictionary.

- Try running the script to print the materials created to the terminal.

Constructing materials from isotopes is inefficient as many nuclides must be added to the material, however, is necessary to create materials with specific compositions.

Look at the script to see how enriched Li4SiO4 can be made using isotopes. Pay particular attention to how the relative proportions of Li6 and Li7 change as the value of *enrichment_fraction* is changed.

- Try printing enriched Li4SiO4 to the terminal.

**Creating Materials from elements**

As mentioned, constructing materials from isotopes is inefficient and should be reserved for when it is required. Otherwise, materials can be constructed from elements using the *add_element* function.

Take a look at the script below.

```2_example_materials_from_elements.py```

See how constructing water from elements rather than isotopes greatly reduces the number of lines of code required.

- Try constructing natural Li4SiO4 from elements.

Enriched materials can also be constructed from elements - OpenMC allows two-isotope elements to be enriched.

Look at the script to see how Li4SiO4 can be constructed and enriched using the OpenMC material enrichment arguments.

- Try printing enriched Li4SiO4 to the terminal.


### Creating materials using the 'neutronics_material_maker' tool

Constructing materials using in-build OpenMC functions can make it difficult to account for material properties such as packing fraction, temperature, pressure etc. The *neutronics_material_maker* aims to simplify material construction and make it easier to account for these properties.

The neutronics_material_maker allows 'Material' and 'MultiMaterial' objects to be specified from which neutronics materials can be created. The objects accept arguments such as 'temperature_in_C' (or K), 'pressure_in_Pa', 'packing_fraction', OpenMC enrichment arguments + others which modify the properties of the material.

Some materials require arguments to be passed to correctly calculate its properties. For example, some material densities such as H2O and He are calculated by the [CoolProp](http://www.coolprop.org/) package which requires temperature and pressure to be specified.

Take a look at the script below.

```3_example_materials_from_material_maker.py```

The script shows how water and Li4SiO4 can be constructed using the Material class and their properties changed via arguments. These Material objects are then converted to neutronics materials (which can be used in OpenMC) using the *.neutronics_material* function.

- Take some time to go through this script and understand how to construct Material objects. Further guidance on usage can be found in the neutronics_material_maker [GitHub repository](https://github.com/ukaea/neutronics_material_maker/tree/openmc_version).

- Some materials have pre-defined default properties which can be seen [here](https://github.com/ukaea/neutronics_material_maker/blob/openmc_version/neutronics_material_maker/materials_fusion_breeders.py). However, they can be overwritten by defining them in the Material() object.


### Parameter Studies

Because the neutronics_material_maker makes it easy to adjust material properties, we can use it to perform parameter studies of materials.

Take a look at the next example script.

```4_example_materials_parameter_study.py```

The script shows how the tool can be used to perform three parameter studies of different materials by calculating their density as a function of different parameters. (Note: Only possible with materials which use CoolProp package to calculate density.)

Run the script to produce graphs of:

- water density as a function of temperature (at constant pressure)
- helium density as a function of temperature (at constant pressure)
- helium density as a function of pressure (at constant temperature)

as shown below.

<p align="center"><img src="images/water_density_vs_temperature.png" height="400"></p>
<p align="center"><img src="images/helium_density_vs_temperature.png" height="400"></p>
<p align="center"><img src="images/helium_density_vs_pressure.png" height="400"></p>

Examine the script to understand how the Material class is used to iteratively construct neutronics materials and how material density is extracted.

(Note: A density parameter study like this is not possible using in-built OpenMC functions as material densities must be specified explicitly.)


### Creating multimaterials using the 'neutronics_material_maker' tool

The neutronics_material_maker also allows materials to be combined to create homogenised MultiMaterial objects. Like Material objects, MultiMaterial objects can be converted to neutronics materials for use in OpenMC.

The MultiMaterial class is based on the *mix_materials* function in OpenMC, and accepts arguments of:

- material_name
- materials : a list of Material objects to be combined
- fracs : a list of conbination fractions for each material object
- percent_type : combination fraction type ('ao', 'wo' or 'vo') 

Take a look at the next example script.

```5_example_materials_mixed.py```

The script shows how the MultiMaterial class can be used to construct a homogeneous material of helium and Li4SiO4. It also shows how the *mix_materials* function can be used to construct a homogeneous material of tungsten carbide and water.

- Take some time to read the script and understand the MultiMaterial and mix_materials functions.

The main difference between the two functions is that the MultiMaterial function accepts a list of Material objects as the 'materials' argument, whereas the mix_materials function accepts a list of neutronics materials.

- Run the script to see how changing the fraction of each material in a two-material multimaterial changes its density. The script should produce a graph similar to below.

<p align="center"><img src="images/density_vs_volume_fraction.png" height="450"></p>

As expected, when the combination fraction of one material is zero, the multimaterial density is equal to the density of the other material. When the combination fraction of one material is one, the multimaterial density is equal to the density of that material.


