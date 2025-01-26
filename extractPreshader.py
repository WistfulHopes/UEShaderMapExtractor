import json
import sys, getopt, os
import base64
import subprocess

f = open(sys.argv[1])

data = json.load(f)
  
index = 0

material = data[0]
resources = material['LoadedMaterialResources']

for resource in resources:
    shader_map = resource['LoadedShaderMap']
    quality_level = shader_map['ShaderMapId']['QualityLevel']
    feature_level = shader_map['ShaderMapId']['FeatureLevel']
    content = shader_map['Content']
    compilation_output = content['MaterialCompilationOutput']
    uniform_expression_set = compilation_output['UniformExpressionSet']
    
    preshader_data = uniform_expression_set['UniformPreshaderData']['Data']
    
    name = sys.argv[1] + "_" + quality_level + "_" + feature_level
    
    o = open(name + "_preshader.bin", "wb")
    o.write(base64.b64decode(preshader_data))
    o.close()
  
f.close()
