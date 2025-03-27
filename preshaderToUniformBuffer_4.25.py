import json
import sys
import struct


f = open(sys.argv[1])

data = json.load(f)
  
index = 0

material = data[0]
resources = material['LoadedMaterialResources']

for resource in resources:
    def extract_swizzle(data):
        list = []
        list.append(struct.unpack('<B', data[1:2])[0])
        list.append(struct.unpack('<B', data[2:3])[0])
        list.append(struct.unpack('<B', data[3:4])[0])
        list.append(struct.unpack('<B', data[4:5])[0])
        list.append(struct.unpack('<B', data[5:6])[0])
        return (list)


    def extract_append(data):
        list = []
        list.append([struct.unpack('<B', data[1:])])
        return (list)


    def read_preshader_sub(data):
        opcode = struct.unpack('<b', data[0:1])[0]

        match opcode:
            case 1:
                return {"ConstantZero": ([])}
            case 2:
                list = []
                list.append(struct.unpack('<f', data[1:5])[0])
                list.append(struct.unpack('<f', data[5:9])[0])
                list.append(struct.unpack('<f', data[9:13])[0])
                list.append(struct.unpack('<f', data[13:17])[0])
                return {"Constant": list}
            case 4:
                idx = struct.unpack('<H', data[1:3])[0]
                return {"VectorParameter": ([vector_params[idx]['ParameterName']])}
            case 3:
                idx = struct.unpack('<H', data[1:3])[0]
                return {"ScalarParameter": ([scalar_params[idx]['ParameterName']])}
            case 5:
                return {"Add": []}
            case 6:
                return {"Sub": []}
            case 7:
                return {"Mul": []}
            case 8:
                return {"Div": []}
            case 9:
                return {"Fmod": []}
            case 10:
                return {"Min": []}
            case 11:
                return {"Max": []}
            case 12:
                return {"Clamp": []}
            case 20:
                return {"Dot": []}
            case 21:
                return {"Cross": []}
            case 22:
                return {"Sqrt": []}
            case 13:
                return {"Sin": []}
            case 14:
                return {"Cos": []}
            case 15:
                return {"Tan": []}
            case 16:
                return {"Asin": []}
            case 17:
                return {"Acos": []}
            case 18:
                return {"Atan": []}
            case 19:
                return {"Atan2": []}
            case 25:
                return {"Abs": []}
            case 24:
                return {"Saturate": []}
            case 26:
                return {"Floor": []}
            case 27:
                return {"Ceil": []}
            case 28:
                return {"Round": []}
            case 29:
                return {"Truncate": []}
            case 30:
                return {"Sign": []}
            case 31:
                return {"Frac": []}
            case 32:
                return {"Fractional": []}
            case 33:
                return {"Log2": []}
            case 34:
                return {"Log10": []}
            case 35:
                return {"ComponentSwizzle": extract_swizzle(data)}
            case 36:
                return {"AppendVector": extract_append(data)}
            case 37:
                return {"EvaluateTextureSize": ([struct.unpack('<i', data[1:5])[0]])}
            case 38:
                return {"EvaluateTexelSize": ([struct.unpack('<i', data[1:5])[0]])}
            case 39:
                return {"EvaluateExternalTextureCoordinateScaleRotation": ([])}
            case 40:
                return {"ExternalTextureCoordinateOffset": ([])}
            case 41:
                return {"RuntimeVirtualTextureUniform": ([])}


    def read_preshader(data):
        ret = []
        
        while len(data) > 0:
            opcode = struct.unpack('<b', data[0:1])[0]
            ret.append(read_preshader_sub(data))
            
            count = 0
            
            match opcode:
                case 1:
                    count = 1
                case 2:
                    count = 17
                case 4:
                    count = 3
                case 3:
                    count = 3
                case 5:
                    count = 1
                case 6:
                    count = 1
                case 7:
                    count = 1
                case 8:
                    count = 1
                case 9:
                    count = 1
                case 10:
                    count = 1
                case 11:
                    count = 1
                case 12:
                    count = 1
                case 20:
                    count = 1
                case 21:
                    count = 1
                case 22:
                    count = 1
                case 13:
                    count = 1
                case 14:
                    count = 1
                case 15:
                    count = 1
                case 16:
                    count = 1
                case 17:
                    count = 1
                case 18:
                    count = 1
                case 19:
                    count = 1
                case 25:
                    count = 1
                case 24:
                    count = 1
                case 26:
                    count = 1
                case 27:
                    count = 1
                case 28:
                    count = 1
                case 29:
                    count = 1
                case 30:
                    count = 1
                case 31:
                    count = 1
                case 32:
                    count = 1
                case 33:
                    count = 1
                case 34:
                    count = 1
                case 35:
                    count = 6
                case 36:
                    count = 2
                case 37:
                    count = 5
                case 38:
                    count = 5
                case 39:
                    count = 29
                case 40:
                    count = 29
                case 41:
                    count = 17
            
            data = data[count:]
                
        return ret
        
    shader_map = resource['LoadedShaderMap']
    quality_level = shader_map['ShaderMapId']['QualityLevel']
    feature_level = shader_map['ShaderMapId']['FeatureLevel']
    content = shader_map['Content']
    compilation_output = content['MaterialCompilationOutput']
    uniform_expression_set = compilation_output['UniformExpressionSet']
    vector_preshaders = uniform_expression_set['UniformVectorPreshaders']
    scalar_preshaders = uniform_expression_set['UniformScalarPreshaders']
    
    vector_params = uniform_expression_set['UniformVectorParameters']
    scalar_params = uniform_expression_set['UniformScalarParameters']
    
    name = sys.argv[1] + "_" + quality_level + "_" + feature_level
    
    preshader_file = open(name + "_preshader.bin", "rb")
    preshader = preshader_file.read()
    preshader_file.close()
    
    parsed_preshader = {
        "vectors": [],
        "scalars": []
    }
    
    for vector in vector_preshaders:
        offset = vector['OpcodeOffset']
        size = vector['OpcodeSize']
        parsed_preshader["vectors"].append(read_preshader(preshader[offset:offset+size]))
    
    for scalar in scalar_preshaders:
        offset = scalar['OpcodeOffset']
        size = scalar['OpcodeSize']
        parsed_preshader["scalars"].append(read_preshader(preshader[offset:offset+size]))
    
    o = open(name + "_preshader.json", "w")
    o.write(json.dumps(parsed_preshader, indent=4))
    o.close()
  
f.close()
