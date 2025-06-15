# Halo-Asset-Blender-Development-Toolset

## Toolset Description
The Halo Asset Blender Development Toolset is a Blender addon developed in python to aid with creating assets for multiple Halo titles. This addon requires that you have Blender 4.0.0 or above on your system to function.

Please consider supporting me on KoFi at the following link.

https://ko-fi.com/general101

## Supported Titles and Features
The following games are or will be supported by this script:

 * Halo Custom Edition
 * Halo 2 Vista
 * Halo Combat Evolved Anniversary MCC - Classic
 * Halo 2 Anniversary MCC - Classic
 * Halo 3 MCC
 * Halo 3 ODST MCC
 * Halo Reach MCC (Cinematic cameras specifically Use Foundry if you want levels and meshes.)
 * Halo 4 MCC (Cinematic cameras specifically. Use Foundry if you want levels and meshes.)

Script supports the following features:

Feature                     | Halo Custom Edition/Halo Combat Evolved Anniversary MCC - Classic | Halo 2 Vista/Halo 2 Anniversary MCC - Classic  | Halo 3 MCC/ Halo 3 ODST MCC     | Halo Reach MCC         | Halo 4 MCC
--------------------------- | ----------------------------------------------------------------- | ---------------------------------------------- | ------------------------------- | ---------------------- | ----------------------
Levels (ASS)                | N/A                                                               | Full Support                                   | Partial Support[^1]             | N/A                    | N/A
GBXmodel (JMS)              | Full Support                                                      | N/A                                            | N/A                             | N/A                    | N/A
Render Model (JMS)          | Full Support                                                      | Full Support                                   | Full Support                    | Full Support           | N/A
Collision Geometry (JMS)    | Full Support                                                      | Full Support                                   | Full Support                    | Full Support           | N/A
Physics Models (JMS)        | Full Support                                                      | Partial Support[^2]                            | Partial Support[^2]             | N/A                    | N/A
Animations (JMA)            | Full Support                                                      | Full Support                                   | Full Support                    | Full Support           | N/A
Cinematics(QUA)             | N/A                                                               | N/A                                            | Partial Support (WIP)           | Partial Support (WIP)  | Partial Support (WIP)
JMI Exporting               | Full Support                                                      | Full Support                                   | Full Support                    | Full Support           | N/A
WRL Importing               | Full Support                                                      | Full Support                                   | Full Support                    | N/A                    | N/A
JMS Importing               | Partial Support[^3]                                               | Partial Support[^2][^3]                        | Partial Support[^2][^3]         | Full Support           | N/A
JMA Importing               | Full Support                                                      | Full Support                                   | Full Support                    | Full Support           | N/A
ASS Importing               | N/A                                                               | Partial Support[^3]                            | Partial Support[^3][^1]         | N/A                    | N/A
QUA Importing               | N/A                                                               | N/A                                            | Partial Support                 | Partial Support (WIP)  | Partial Support (WIP)
Structure_BSP Tag Importing | Partial Support                                                   | Partial Support                                | No Support                      | N/A                    | N/A
GBXModel Tag Importing      | Full Support                                                      | N/A                                            | N/A                             | N/A                    | N/A
Model Tag Importing         | Full Support                                                      | Full Support                                   | No Support                      | N/A                    | N/A
Collision Tag Importing     | Full Support                                                      | Full Support                                   | No Support                      | N/A                    | N/A
Animation Tag Importing     | Partial Support[^4]                                               | No Support                                     | No Support                      | N/A                    | N/A
Camera Track Tag Importing  | Full Support                                                      | Full Support                                   | No Support                      | N/A                    | N/A

[^1]: Toolset is currently missing support for importing or exporting certain Halo 3 JMS/ASS features such as the W coordinate in UVW.
[^2]: Car wheel and prismatic constraints are not exported or imported properly. WIP
[^3]: JMS/ASS files imported into Blender do not have their triangles connected properly. This means that imported models are improper due to the exporter using vertex normals instead of loop normals.
[^4]: Imported animations tags currently do not have fixed overlay animations.

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

 * Discord user conscars
   * For testing, suggestions, a bug fix, and the WRL import code that is being used for this project.
   * [WRL to OBJ](https://github.com/csauve/mek/blob/wrl-to-obj-colors/tools_misc/wrl_to_obj.py)

 * Discord user MercyMoon#3864
   * For developing the Halo materials tool Helper scripts in the toolset.

 * Discord user Fulsy#1228
   * For some modifications done to the WaltzStreet version the script was based on.

 * Discord user mosesofegypt
   * For some modifications done to the WaltzStreet version the script was based on, Stubbs related tooling, and advice on animation data.

 * Discord user num0005
   * For help with code reviews and several features.

 * 343 Industries/Discord user kornman00
   * Thanks to Kornman for aiding the development of the toolset by answering questions and 343 Industries/Microsoft for allowing this to happen in the first place.

 * The Sigmmma crew
   * For some tips on importing assets and for MEK defs along with some math used in the Halo 1 tag importing code.
   * [Sigmmma](https://github.com/Sigmmma)

 * Discord user chiefster_4014
   * For contributing to the Halo 1 shader nodes used in this project.

 * Discord user dogbrainludus
   * For contributing to the Halo 1 shader nodes used in this project.
   
 * Discord user meowsandstuff
   * For contributing to the Halo 2 shader nodes used in this project.

 * Discord user general_101
   * Getting the ball rolling I guess?
