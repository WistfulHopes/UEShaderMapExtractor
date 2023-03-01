# UEShaderMapExtractor
Extracts and helps identify shaders from Unreal material shadermaps. Note that this tool only works on D3D11/D3D12 games that use LZ4 compression at the moment. Support for other shader and compression types is currently unimplemented.

## Usage:

Depending on whether or not your game uses shader archives, the first steps will be different.

### No shader archives

1. Export a JSON of your material from this FModel build: https://github.com/WistfulHopes/FModel/releases/tag/4.4.1.2-shadermap
2. With Python 3, run this command: `python parseAndDecompressShaders.py (exported JSON file)`. Make sure `decompress_shader.exe` is in the same directory. This will extract and decompress the DXBC/DXIL shaders from the exported JSON.

### With shader archives

1. Export the JSON and binary form of the shader archive from this FModel build: https://github.com/WistfulHopes/FModel/releases/tag/4.4.1.2-shadermap
2. In your material, search for "ResourceHash". Store the hash for the next step.
3. With Python 3, run this command: `python extractShaderFromArchive.py (exported JSON file) (exported archive binary) (hash) (output name)`. Make sure `decompress_shader.exe` is in the same directory. This will extract and decompress the DXBC/DXIL shaders from the exported JSON and archive, using the hash to identify the shadermap.

### Identify shaders

1. Dump FNames from your game using your preferred UE4 SDK dumper. If you can't do this, **skip to step 3.**
2. Navigate to the ShaderHash folder, and run this command: `shaderhash (FName string) (FName internal number)`. You should run this command for a vertex factory (eg. FLocalVertexFactory) and a shader type (eg. TBasePassPSFNoLightMapPolicy). This will print the hashes for the given names. **Skip to step 4.**
3. Take the vertex factory type name and shader hashes from the list at the bottom of this README. For a skeletal mesh, you want FGPUSkinPassthroughVertexFactory for the vertex factory, TBasePassVSFNoLightMapPolicy for the vertex shader, and TBasePassPSFNoLightMapPolicy for the pixel shader.
4. In the exported JSON, search for the vertex factory hash. This should bring you to "VertexFactoryTypeName". Then, search for the shader type hash. This should be in the "ShaderTypes" array right below the VertexFactoryTypeName. Then, in the "Shaders" array below it, find the shader at the same index as the shader type hash. Search for "ResourceIndex". The value right next to it is the index of the exported DXBC/DXIL file that contains the code for that shader (eg. ResourceIndex 10, {MaterialName}.json10.dxbc).
5. For easier analysis of the shader, run this tool on the exported DXBC files: https://github.com/Quon/HLSLDecompiler/releases/tag/0.2
6. In the case of DXIL files, use https://github.com/microsoft/DirectXShaderCompiler to disassemble the shaders.

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

