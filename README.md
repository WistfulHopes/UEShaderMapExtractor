# UEShaderMapExtractor
Extracts and helps identify shaders from Unreal material shadermaps. Note that this tool only works on D3D11/D3D12 games that use LZ4 compression at the moment. Support for other shader and compression types is currently unimplemented.

Usage:

1. Export a JSON of your material from this FModel build: https://github.com/WistfulHopes/FModel/releases/tag/4.4.1.2-shadermap
2. With Python 3, run this command: `python parseAndDecompressShaders.py (exported JSON file)`. Make sure `decompress_shader.exe` is in the same directory. This will extract and decompress the DXBC/DXIL shaders from the exported JSON.
3. Dump FNames from your game using your preferred UE4 SDK dumper.
4. Navigate to the ShaderHash folder, and run this command: `shaderhash (FName string) (FName internal number)`. You should run this command for a vertex factory (eg. FLocalVertexFactory) and a shader type (eg. TBasePassPSFNoLightMapPolicy). This will print the hashes for the given names.
5. In the exported JSON, search for the vertex factory hash. This should bring you to "VertexFactoryTypeName". Then, search for the shader type hash. This should be in the "ShaderTypes" array right below the VertexFactoryTypeName. Then, in the "Shaders" array below it, find the shader at the same index as the shader type hash. Search for "ResourceIndex". The value right next to it is the index of the exported DXBC/DXIL file that contains the code for that shader (eg. ResourceIndex 10, {MaterialName}.json10.dxbc).
6. For easier analysis of the shader, run this tool on the exported DXBC files: https://github.com/Quon/HLSLDecompiler/releases/tag/0.2
7. In the case of DXIL files, use https://github.com/microsoft/DirectXShaderCompiler to disassemble the shaders.
