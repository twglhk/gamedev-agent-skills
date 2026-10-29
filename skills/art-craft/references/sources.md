# Sources

A practice in the skill needs two independent sources, an official doc, or your own measurement; anything resting on one source is marked as a proposal. Excerpt-only reads are marked.

## External

| # | Title · author | URL | Published | Claim it supports |
| --- | --- | --- | --- | --- |
| 1 | Skyrim's Modular Level Design (GDC 2013) · Joel Burgess, Nate Purkeypile | http://blog.joelburgess.com/2013/04/skyrims-modular-level-design-gdc-2013.html | 2013-04-19 | Kits are systems on a grid; a proof phase with almost no mesh detail and no textures tests proportions and kit logic before art; footprints are multiples of each other |
| 2 | The Birth of Ascent · Chris Carney, Salvatore Garrozzo (Riot) | https://playvalorant.com/en-gb/news/dev/the-birth-of-ascent/ | 2020-07-20 | Block-in answers layout before art; a "clean zone" between about 1 and 9 ft keeps silhouettes readable, detail above and below |
| 3 | Guilty Gear Xrd's Art Style (GDC 2015 handout) · Junya C. Motomura (Arc System Works) | https://www.ggxrd.com/Motomura_Junya_GuiltyGearXrd.pdf · talk https://archive.org/details/GDC2015Motomura | 2015 | Under cel shading, small normal noise becomes a large blotch; normals and thresholds are controlled by hand |
| 4 | The Ultimate Trim: Texturing Techniques of Sunset Overdrive (GDC 2015) · Morten Olsen (Insomniac) | https://www.gdcvault.com/play/1022323/The-Ultimate-Trim-Texturing-Techniques · slides https://www.slideshare.net/slideshow/the-ultimate-trim-texturing-techniques-of-sunset-overdrive/287177630 | 2015 | One shared trim layout saves production time, memory and performance; bevels baked into trim normals (proposal only) |
| 5 | Illustrative Rendering in Team Fortress 2 (NPAR 2007) · Mitchell, Francke, Eng (Valve) | https://dtsheet.com/doc/1443576/slides (mirror) | 2007 | Environments: value contrast, simple forms, minimal visual noise; characters readable under all lighting |
| 6 | How to Reduce Visual Confusion in Your Game · Peter Angstadt | https://www.gamedeveloper.com/design/how-to-reduce-visual-confusion-in-your-game | 2015-03-12 | Desaturate a screenshot to check it reads on values alone (excerpt) |
| 7 | Level Art: Color and Lighting · Frozenbyte wiki | https://wiki.frozenbyte.com/index.php/Level_Art:_Color_and_Lighting | undated | Important things need value contrast; darker edges where the player isn't meant to go (excerpt) |
| 8 | VALORANT Shaders and Gameplay Clarity · Brandon Wang (Riot) | https://technology.riotgames.com/news/valorant-shaders-and-gameplay-clarity | 2020-06-30 | Characters must stand out from the environment; players mentally block out the environment; environment shading stays cheap |
| 9 | Text to 3D API · Meshy docs | https://docs.meshy.ai/en/api/text-to-3d | living page | Preview then refine; `remove_lighting` model limits; Smart Topology sets face count from `target_polycount` (100 to 15,000); models retire |
| 10 | The PBR Guide, 3rd ed. · Wes McDermott (Allegorithmic) | https://learndownload.adobe.com/pub/learn/substance-3d-designer/the-pbr-guide.pdf | 2018-02 | Base colour holds no lighting information such as ambient occlusion |
| 11 | PBR Authoring Guide · Studio 397 | https://docs.studio-397.com/pages/viewpage.action?pageId=37945362 | undated | Albedo holds base colour with no lighting; lighting comes from the engine |
| 12 | Standard Material 3D · Godot docs | https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html | living page | Godot expects OpenGL-style (Y+) normal maps; meshes need normals and tangents |
| 13 | Content survey (AI disclosure) · Steamworks | https://partner.steamgames.com/doc/gettingstarted/contentsurvey | living page | Pre-generated AI content players see is disclosed on the store page |
| 14 | glTF 2.0 · Blender manual | https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html | living page | Exporter reads Principled BSDF base colour, metal/rough, emission; Apply Modifiers and Tangents options |
| 15 | The Gothic Sensibilities of Darkest Dungeon · Kevin VanOrd, quoting Chris Bourassa | https://www.gamespot.com/articles/the-gothic-sensibilities-of-darkest-dungeon/1100-6424880/ | 2015-01-27 | Black only in the inks; strong linework lets colour hits land without losing readability |
| 16 | TFT: Reckoning Arenas from Concept to Life · Rodger Caudill (Riot) | https://teamfighttactics.leagueoflegends.com/en-us/news/dev/tft-reckoning-arenas-from-concept-to-life/ | 2021-05-25 | Auto-battler arenas as a reference class (excerpt) |
| 17 | Comparing Team Fortress 2 & Overwatch Art Direction · Xavier Coelho-Kostolny | https://80.lv/articles/comparing-team-fortress-2-and-overwatch-art-direction | 2017-09-11 | A value hierarchy on characters makes them read |
| 18 | What Grayscale Misses · Egor Nikolaev | https://enikolaev.com/blog/from-grayscale-to-a-perceptual-lightness-checker-in-unity/ | 2026-08-09 | A lightness check is a proxy, not a verdict; it knows nothing of motion, focus or intent |
| 19 | Outlines · NedMakesGames | https://nedmakesgames.github.io/blog/outlines | 2021-02-03 | Inverted hull is per-object and weak on complex meshes; edge detection covers the screen in one pass (excerpt) |
| 20 | godot-toon-outline · EMBYRDEV | https://github.com/EMBYRDEV/godot-toon-outline | Godot 4.0 era | A Godot toon outline "does not work well with TAA enabled" (excerpt) |
| 21 | Little Demon Trist: Model & SFX · Trevor Carr (Riot) | https://nexus.leagueoflegends.com/en-us/2019/04/little-demon-trist-model-sfx/ | 2019-04-17 | A top-down game's character mesh is about 7,000 to 10,000 triangles, sized to camera distance |
| 22 | Dota 2 Workshop technical requirements · Valve | https://www.dota2.com/workshop/requirements/tiny · https://www.dota2.com/workshop/requirements/zuus | living page | Per-slot LoD0/LoD1 triangle limits and texture sizes for a fixed high camera |
| 23 | Texels Per Meter · CRYENGINE docs | https://www.cryengine.com/docs/static/engines/cryengine-5/categories/23756816/pages/52199429 | living page | Texel density has a target and a debug view to check it |
| 24 | Texel Density · Maxon Cinema 4D help | https://help.maxon.net/c4d/en-us/Content/html/Texel_Density.html | living page | About 1024 px/m first person, 512 third person, 256 or less top-down (excerpt) |
| 25 | Teamfight Tactics: Fates art blast · ArtStation Magazine | https://magazine.artstation.com/2020/10/riot-games-teamfight-tactics-fates-league-of-legends-art-blast/ | 2020-10-06 | TFT arenas: anchors, base materials, culture kit, points of interest; points of interest get the most fidelity (excerpt) |
| 26 | Apple M4 10-Core GPU benchmarks · Notebookcheck | https://www.notebookcheck.net/Apple-M4-10-core-GPU-Benchmarks-and-Specs.835807.0.html | living page | M4 10-core GPU performs almost like a GTX 1650 Laptop (excerpt) |
| 27 | Steam Deck compatibility review · Steamworks | https://partner.steamgames.com/doc/steamdeck/compat | living page | Deck Verified expects playable frame rates at default settings, 30 fps baseline, 1280×800 |
| 28 | mcp-for-blender (formerly blender-mcp) · Siddharth Ahuja | https://github.com/ahujasid/mcp-for-blender | 2025 | Runs Python in a live Blender from an agent |
| 29 | blender-agent-skills · oh-ashen-one | https://github.com/oh-ashen-one/blender-agent-skills | 2026 | Staged scene building that survives crashes, a screenshot gate, one Blender port per session (excerpt) |
| 30 | Blender skills README · scenario-labs | https://github.com/scenario-labs/skills/blob/main/skills/dcc/blender/README.md | 2026 | Headless bpy can't use sculpt brushes (excerpt) |

## Godot docs (stable, 4.x)

| # | Page | URL | Claim it supports |
| --- | --- | --- | --- |
| G1 | Optimizing 3D performance | https://docs.godotengine.org/en/stable/tutorials/performance/optimizing_3d_performance.html | Automatic instancing only for same mesh and material, opaque or alpha-scissor; few transparent objects |
| G2 | GPU optimization | https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html | Reuse materials; pixel cost is usually the desktop bottleneck; avoid sub-pixel triangles; post and shadows cost per pixel |
| G3 | Optimization using MultiMeshes | https://docs.godotengine.org/en/stable/tutorials/performance/using_multimesh.html | One draw for thousands of instances; no per-instance culling |
| G4 | Mesh level of detail (LOD) | https://docs.godotengine.org/en/stable/tutorials/3d/mesh_lod.html | glTF meshes get LODs on import; picked by the AABB's nearest point; may break skinned meshes |
| G5 | Visibility ranges (HLOD) | https://docs.godotengine.org/en/stable/tutorials/3d/visibility_ranges.html | Artist-made LOD by distance |
| G6 | Occlusion culling | https://docs.godotengine.org/en/stable/tutorials/3d/occlusion_culling.html | Helps many-room interiors; Forward+'s depth prepass cuts the gain |
| G7 | Reducing stutter from shader compilations | https://docs.godotengine.org/en/stable/tutorials/performance/pipeline_compilations.html | New materials, MSAA changes and probes compile pipelines |
| G8 | Spatial shaders | https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html | `light()` runs per light per pixel; `cull_front` for inverted hulls |
| G9 | Environment and post-processing | https://docs.godotengine.org/en/stable/tutorials/3d/environment_and_post_processing.html | SSR skips transparent surfaces; fog cost by volume size; AgX slowest tonemapper |
| G10 | Advanced post-processing | https://docs.godotengine.org/en/stable/tutorials/shaders/advanced_postprocessing.html | Full-screen quad reading depth and normal-roughness textures (Forward+) |
| G11 | 3D antialiasing | https://docs.godotengine.org/en/stable/tutorials/3d/3d_antialiasing.html | MSAA suits cartoon styles; TAA ghosts; FXAA cheapest and blurry |
| G12 | Using Lightmap GI | https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/using_lightmap_gi.html | Near-free at run time, but baked lights can't change at run time |
| G13 | 3D lights and shadows | https://docs.godotengine.org/en/stable/tutorials/3d/lights_and_shadows.html | PSSM 4 splits draw a large object up to five times; distance and map size set cost |
| G14 | Importing images | https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html | VRAM compression cuts memory 4 to 6×; 2048² RGBA 21.33 MiB lossless vs 5.33 MiB compressed with mipmaps; normal maps to RGTC; Size Limit |
| G15 | Performance (class) | https://docs.godotengine.org/en/stable/classes/class_performance.html | Monitors for draws, primitives, texture and video memory, pipeline compilations |
| G16 | System requirements | https://docs.godotengine.org/en/stable/about/system_requirements.html | Forward+ needs Vulkan 1.0, D3D12 or Metal 3 |
