from seamless.highlevel import Context, Cell, Transformer
ctx = Context()

ctx.attract_test = Transformer()
ctx.attract_test.language = "docker"
ctx.attract_test.docker_image = "rpbs/attract"
ctx.attract_test.docker_options = {
    "shm_size":"8gb",
    "device_requests":[
        {"count":-1, "capabilities":[['gpu']]}
    ]
}
code = open("../attract-script/attract.sh").read()
code = code.replace("trap ", "#trap ")
code += """
cat result.dat > RESULT
"""
ctx.attract_test.code = code
ctx.attract_test["receptor.pdb"] = open("../examples/1AVXA.pdb").read()
ctx.attract_test["ligand.pdb"] = open("../ligands/7CEIB.pdb").read()
ctx.result = ctx.attract_test.result
ctx.result.celltype = "text"
ctx.result.mount("attract-test-result.txt", "w")
ctx.compute()
print(ctx.attract_test.status)
print(ctx.attract_test.exception)