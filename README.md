# Halo-Asset-Blender-Development-Toolset

## Toolset Description
The Halo Asset Blender Development Toolset is a Blender addon developed in python to aid with creating assets for multiple Halo titles. This addon requires that you have Blender 2.83 LTS or above on your system to function.

## Supported Titles and Features
The following games are or will be supported by this script:

 * Halo Custom Edition
 * Halo 2 Vista
 * Halo Combat Evolved Anniversary MCC - Classic
 * Halo 2 Anniversary MCC - Classic
 * Halo 3 MCC
 * Halo 3 ODST MCC

Script supports the following features:

Feature                    | Halo Custom Edition/Halo Combat Evolved Anniversary MCC - Classic | Halo 2 Vista/Halo 2 Anniversary MCC - Classic  | Halo 3 MCC/ Halo 3 ODST MCC
-------------------------- | ----------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------
Levels(JMS/ASS)            | Full Support                                                      | Full Support                                   | Partial Support(See 1)     
GBXmodel/Render Model(JMS) | Full Support                                                      | Full Support                                   | Full Support 
Collision Geometry(JMS)    | Full Support                                                      | Full Support                                   | Full Support 
Physics Models(JMS)        | Full Support                                                      | Partial Support(See 2)                         | Partial Support(See 2)
Animations(JMA)            | Full Support                                                      | Full Support                                   | Full Support
JMI Exporting              | Full Support                                                      | Full Support                                   | Full Support
WRL Importing              | Full Support                                                      | Partial Support(See 3)                         | Partial Support(See 3)
JMS Importing              | Partial Support(See 4)                                            | Partial Support(See 2 and 4)                   | Partial Support(See 2 and 4)
JMA Importing              | Full Support                                                      | Full Support                                   | Full Support
ASS Importing              | N/A                                                               | Partial Support(See 4)                         | Partial Support(See 4 and 1) 

 1. Toolset is currently missing support for importing or exporting certain Halo 3 JMS/ASS features such as the W coordinate.
 2. Car wheel and pristmatic constraints are not exported properly. WIP
 3. WRL 2.0 are partially supported. The importer can generate the error geometrty but does not group the error geometry at this time.
 4. JMS/ASS files imported into Blender do not have their triangles connected properly. This means that imported models are improper due to the exporter using vertex normals instead of loop normals.

## Documentation
See the following links for information on exporting or importing assets from these tools:

[C20 Docs](https://c20.reclaimers.net/)

[H2Codez Docs](https://num0005.github.io/h2codez_docs/w/home.html)

## Credits

 * Cyboryxmen
   * For making the original JMS script known as WaltzStreet that was used as a reference.
   * [WaltzStreet](http://forum.halomaps.org/index.cfm?page=topic&topicID=42486)

 * Discord user Aerial Dave#2236
   * For making the original ASS script known as blend2halo2 that was used as a reference.
   * [Blend2Halo2](http://forum.halomaps.org/index.cfm?page=topic&topicID=48139)

 * Discord user con#4702
   * For testing, suggestions, a bug fix, and the WRL import code that is being used for this project.
   * [WRL to OBJ](https://github.com/csauve/mek/blob/wrl-to-obj-colors/tools_misc/wrl_to_obj.py)

 * Discord user Fulsy#1228
   * For some modifications done to the WaltzStreet version the script was based on.

 * Discord user MosesofEgypt#2751
   * For some modifications done to the WaltzStreet version the script was based.

 * Discord user num0005#8646
   * For help with code reviews and several features.

 * 343 Industries/Discord user kornman00#4155
   * Thanks to Kornman for aiding the development of the toolset by answering questions and 343 Industries/Microsoft for allowing this to happen in the first place.

 * The Sigmmma crew
   * For some tips on importing assets.
   * [Blendkrieg](https://github.com/Sigmmma/Blendkrieg)

 * The contributors behind PyPreprocessor
   * For providing their code for use in projects like this one.
   * [PyPreprocessor](https://github.com/interpreters/pypreprocessor)

 * The contributors behind Tatsu
   * For providing their code for use in projects like this one.
   * [Tatsu](https://github.com/neogeny/TatSu)

 * Discord user General_101#9814
   * Getting the ball rolling I guess?
