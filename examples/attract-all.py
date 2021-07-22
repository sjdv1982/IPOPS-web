from seamless.highlevel import Context, Cell, Transformer
ctx = Context()

#########################################################

import seamless
seamless.set_ncores(3)  # Try to run 3 docking runs in parallel 

background = ["1AVXB", "2SNIB", "7CEIB"]

ctx.receptor = Cell("text")
ctx.receptor.set(open("../examples/1AVXA.pdb").read())

code = open("../attract-script/attract.sh").read()
code = code.replace("trap ", "#trap ")
code += """
cat result.dat > RESULT
"""

ctx.attract = Context()
ctx.attract.result = Context()
for pdbcode in background:
    pdbfile = "../ligands/{}.pdb".format(pdbcode)
    pdbdata = open(pdbfile).read()

    dock = Transformer()
    setattr(ctx.attract, pdbcode, dock)
    dock.language = "docker"
    dock.docker_image = "rpbs/attract"
    dock.docker_options = {
        "shm_size":"8gb",
        "device_requests":[
            {"count":-1, "capabilities":[['gpu']]}
        ]
    }
    dock.code = code
    dock["receptor.pdb"] = ctx.receptor
    
    dock["ligand.pdb"] = pdbdata
    result = Cell("text")
    setattr(ctx.attract.result, pdbcode, dock.result)
    result = getattr(ctx.attract.result, pdbcode)
    result.celltype = "text"

#ctx.compute()