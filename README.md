# UEShaderMapExtractor
Extracts and helps identify shaders from Unreal material shadermaps. Supports materials from UE4.25 and above.

## Usage

### Setup

1. Download [FModel](https://github.com/4sval/FModel).
2. Enable "Serialize Inline Shader Maps" in Settings.
![image](https://github.com/user-attachments/assets/c4f13c4c-8323-44da-9574-f3e78d2a5563)


Depending on whether or not your game uses shader archives, the first steps will be different.

### No shader archives

1. Export a JSON of your material from FModel.
2. With Python 3, run this command: `python parseAndDecompressShaders.py (exported JSON file)`. Make sure `decompress_shader.exe` is in the same directory. This will extract and decompress the DXBC/DXIL shaders from the exported JSON.

### With shader archives

1. Export the JSON and binary form of the shader archive from FModel.
2. In your material, search for "ResourceHash". Store the hash for the next step.
3. With Python 3, run this command: `python extractShaderFromArchive.py (exported JSON file) (exported archive binary) (hash) (output name)`. Make sure `decompress_shader.exe` is in the same directory. This will extract and decompress the DXBC/DXIL shaders from the exported JSON and archive, using the hash to identify the shadermap.
    - If the game is using UE5 and IO Store, use `python extractShaderFromArchive_UE5.py (exported JSON file) (exported archive binary) (hash) (output name)`.

### Identify shaders

1. Dump FNames from your game using your preferred UE4 SDK dumper. If you can't do this, **skip to step 3.**
2. Navigate to the ShaderHash folder, and run this command: `shaderhash (FName string) (FName internal number)`. You should run this command for a vertex factory (eg. FLocalVertexFactory) and a shader type (eg. TBasePassPSFNoLightMapPolicy). This will print the hashes for the given names. **Skip to step 4.**
3. Take the vertex factory type name and shader hashes from the list at the bottom of this README. For a skeletal mesh, you want FGPUSkinPassthroughVertexFactory for the vertex factory, TBasePassVSFNoLightMapPolicy for the vertex shader, and TBasePassPSFNoLightMapPolicy for the pixel shader.
4. In the exported JSON, search for the vertex factory hash. This should bring you to "VertexFactoryTypeName". Then, search for the shader type hash. This should be in the "ShaderTypes" array right below the VertexFactoryTypeName. Then, in the "Shaders" array below it, find the shader at the same index as the shader type hash. Search for "ResourceIndex". The value right next to it is the index of the exported DXBC/DXIL file that contains the code for that shader (eg. ResourceIndex 10, {MaterialName}.json10.dxbc).
5. For easier analysis of the shader, run this tool on the exported DXBC files: https://github.com/Quon/HLSLDecompiler/releases/tag/0.2
6. In the case of DXIL files, use https://github.com/microsoft/DirectXShaderCompiler to disassemble the shaders.

### Identify material buffer layout

Note: replace `extractPreshader.py` with the one that fits your UE4/5 version.

1. With Python 3, run this command: `python extractPreshader.py (exported JSON file)`. This will output a new JSON in the directory, with "_preshader.json" at the end.
2. The last cbuffer in your decompiled shader should be the "Material" cbuffer, which this preshader JSON maps to.
    - Vectors come first in the cbuffer, and take up one whole index. This means that cbuffer\[0] is equivalent to the first vector entry of the preshader JSON.
    - Scalars come last in the cbuffer, and take up one *component* of an index. This means that if you have 40 vectors in your cbuffer, then cbuffer\[40].x is equal to the first scalar entry of the preshader JSON, cbuffer\[40].y to the second, etc.
  
## Vertex Factory hashes

FLocalVertexfactory: 11475683181038621400

FGPUSkinPassthroughVertexFactory: 7884826846012382956

FParticleSpriteVertexFactory: 1936260693301728965

FMeshParticleVertexFactory: 3257961110001812583

FNiagaraSpriteVertexFactory: 13168243933419104092

FNiagaraMeshVertexFactory: 3257961110001812583

FNiagaraRibbonVertexFactory: 549208615835106585


## Vertex Shader hashes

TBasePassVSFNoLightMapPolicy: 16833942227387653686


## Pixel Shader hashes

TBasePassPSFNoLightMapPolicy: 4974208445782451494

