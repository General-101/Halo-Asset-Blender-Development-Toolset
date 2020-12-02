# Halo-Asset-Blender-Development-Toolset
An exporter for Blender to create assets for H2V/CE

Credit to Cyboryxmen for making the original JMS script known as WaltzStreet that was used as a reference
for this script. 

Credit to Discord user Aerial Dave#2236 for making the original ASS script known as blend2halo2 that was used as a reference
for this script. 

Additional credits to...

Discord user con#4702 for testing, suggestions, and a bug fix.

Discord user Fulsy#1228 for some modifications done to the WaltzStreet version the script was based on.

Discord user MosesofEgypt#2751 for some modifications done to the WaltzStreet version the script was based
on.

Discord user num0005#8646 for help with code reviews and several features.

The Blendkrieg toolset for some tips on importing assets.

https://github.com/Sigmmma/Blendkrieg

Script is fully capable of exporting render, collision, and physics geometry in the form a JMS text file
for both CE and Halo 2. Script also has support for exporting animations done using the pose system 
to a JMA text file for importing in both CE and Halo 2. On top of that this script also supports exporting 
to an ASS text file for Halo 2 level importing.

Info about how this tool can be used for Halo 2 can be found here.

https://general-101.github.io/HEK-Docs/w/home.html

https://num0005.github.io/h2codez_docs/w/home.html

Contact General_101#9814 for further info or questions about this version of the script.

Requires Blender 2.8 public release or above

TUTORIAL - HOW TO EXPORT MASTER CHIEF'S HCE MODEL INTO BLENDER AND IMPORT BACK TO THE GAME

Since usage of the plugin is not immediately obvious, here is a tutorial that covers every aspect of getting Chief's model in and out of the game - this includes matters that are outside of the scope of the plugin itself, such as map decompilation and compilation.

Required tools:
-Mozz's Editing Kit Essentials which contains:
  -Refinery with GUI
  -Mozzarilla
  -Pool (you can use Tool if you prefer it)
-Invader, in case map compilation by the above causes problems (e.g. game throwing "Gathering Exception Data" at certain points)

Steps:
1. Run Refinery GUI.
2. Load any map featuring the default Chief model.
3. Switch to data extraction.
4. The Chief's model should be stored the following way in hierarchy view:

characters/cyborg/cyborg.gbxmodel

5. At this point you can choose what do you want to extract - you can extract just the gbxmodel, the files you want (e.g. the gbxmodel along with textures stored in bitmaps directory) or the entire cyborg directory, or even the entire map if you want. However, this will assume you have not yet decompiled your map yet, and that's necessary for recompiling the model back to the map. So decompile the entire map.
6. Run extraction - you can extract the data anywhere on your PC, however, if you decompile the entire map, it's best that it goes to <your Halo CE folder>/tags (the data has to be stored there if you want to compile the map), but make sure you've backed up its contents if you had any work files there.
7. Your model will become converted to JMS files (Jointed Model Skeleton), stored in <extraction directory>/cyborg/models. In case of Chief's model it should contain 5 files - each of them is a separate Level of Detail (LOD) model. Unless you'll be making separate LOD models, you will be interested only in _base superhigh.jms file.
8. In Blender, Import _base superhigh.jms with Game Version set to Halo CE.
9. (OPTIONAL) At this point you are free to edit the model as you wish - however, it is highly recommended to skip this step the first time to ensure the modding pipeline itself has no issues - this will allow you to establish if any given problem past this step lies within the pipeline or your model.
10. Export the model as a JMS with Game Version set to Halo CE and LOD to Super High.
11. The model you will receive should be named unnamed supprhigh.JMS regardless of what name you set - rename it to _base superhigh.jms
12. Copy the new _base superhigh.jms to <your Halo CE folder>/data/characters/cyborg/models directory. If it does not exist, create it. (CRITICAL NOTE: Attempts to compile the data anywhere else than from the data directory will create broken files)
13. Using Tool or Pool (however having the directory set to your Halo CE folder) input the following command:
  
  tool model characters\cyborg
  
14. You should now have the model converted to cyborg.gbxmodel in <your Halo CE folder>/tags/characters/cyborg/models.
15. Using Mozzarilla, load up cyborg.gbxmodel and make sure it has the same node list checksum as the remaining tags in folder, e.g. in the animations array of cyborg.model_animations.
16. (OPTIONAL) you can now load the map in Sapien and check if your model has any issues, as Sapien does not require compiled maps. Assuming the map you have compiled was e.g. Pillar of Autumn, load up <your Halo CE folder>/tags/levels/a10/a10.scenario, and create an instance of Chief (cyborg) anywhere.
17. Recompile the map (be sure the backup the original map in your maps folder) - using Pool, type in the following command:
  
  build-cache-file ""
  
 And right-click on the parentheses, which will prompt you to select the appropriate scenario tag. Select the same a10.scenario tag as in previous step, assuming the decompiled level is Pillar of Autumn.
18. If everything went okay, you should be able to play the level without any crashes or issues (which may occur mid-game, so be sure to test your level).

However, in case you are getting "Gathering Exception Data" crashes mid-game, you most likely have compiled the level with tags that got broken during the extraction. To fix that, do the following:

19. Using Invader, type the following command to fix the tags (assuming your command line directory is set to <your Halo CE folder> and Invader is installed in <your Halo CE folder>/Invader):
  
  Invader\invader-bludgeon --all -T everything
  
20. Also using Invader, type the following command to compile the map:

  Invader\invader-build -P -t "E:\Gry\Halo CE\tags" -g custom "E:\Gry\Halo CE\tags\levels\a10\a10.scenario"
  
21. The map should now run without any issues.
