# file created by DCUplink 1 Jan 2024
# File is used by selecting files within a content drawer folder and then running this script via the tools menu execute python script
# this script requires the python plugins to be installed under the plugin tab
# this script was tested on unreal 5.0.x
# configure LOD settings first float is for screen percentage which static mesh preview editor can show you for figuring out best results before puting it here
# the second float value is for triangle percentage which will reduce the total triangles the model has at that LOD number
# based on screen size of the model be warned this will impact things if you have a nice model that you want to look decent from a distance

# this script is the result of experimenting with options to process a large amount of FBX models as part of the model workflow for game creation
# the current FBX import utility only configures the screen percentage not the triangle complexity values so this was devised as a work around
# this script does not handle invalid characters in the file path of the assets selected in the content drawer and will error on those during the script but will continue to try and apply changes to the rest of the supplied assets
# review your output log for any assets that failed to be processed correctly.

# Feel free to follow my game on steam https://store.steampowered.com/app/1917160/

import unreal

# Function to get selected static meshes in Content Browser
def get_selected_static_meshes():
    editor_utility = unreal.EditorUtilityLibrary()
    selected_assets = editor_utility.get_selected_assets()
    static_meshes = [asset for asset in selected_assets if isinstance(asset, unreal.StaticMesh)]
    return static_meshes

# Function to apply LODs to a static mesh
def apply_lods(static_mesh):
    # Check if the mesh is complex enough.
    number_of_vertices = unreal.EditorStaticMeshLibrary.get_number_verts(static_mesh, 0)
    if number_of_vertices < 10:
        return
    print("Treating asset: " + static_mesh.get_name())
    print("Existing LOD count: " + str(unreal.EditorStaticMeshLibrary.get_lod_count(static_mesh)))
    
    # Set up options for auto-generating the levels of detail.
    options = unreal.EditorScriptingMeshReductionOptions()
    # Define new levels of detail.
    options.reduction_settings = [
        unreal.EditorScriptingMeshReductionSettings(1.0, 1.0),
        unreal.EditorScriptingMeshReductionSettings(0.98, 0.98),
        unreal.EditorScriptingMeshReductionSettings(0.97, 0.97),
        unreal.EditorScriptingMeshReductionSettings(0.95, 0.95),
        unreal.EditorScriptingMeshReductionSettings(0.92, 0.92),
        unreal.EditorScriptingMeshReductionSettings(0.90, 0.90),
        unreal.EditorScriptingMeshReductionSettings(0.85, 0.85),
        unreal.EditorScriptingMeshReductionSettings(0.70, 0.70),
        unreal.EditorScriptingMeshReductionSettings(0.60, 0.60)
    ]
    # Use the screen space thresholds set above, rather than auto-computing them.
    options.auto_compute_lod_screen_size = False
    # Set the options on the Static Mesh Asset.
    unreal.EditorStaticMeshLibrary.set_lods(static_mesh, options)
    # Save the changes.
    unreal.EditorAssetLibrary.save_loaded_asset(static_mesh)
    print("New LOD count: " + str(unreal.EditorStaticMeshLibrary.get_lod_count(static_mesh)))

# Get selected static meshes
selected_static_meshes = get_selected_static_meshes()

# Apply LODs to each selected static mesh
for mesh in selected_static_meshes:
    apply_lods(mesh)
