
PROJNAME = "IPOPS"

import os, sys, shutil

import seamless
seamless.set_ncores(4)  # Try to run 3 docking runs in parallel, plus status graph 
seamless.database_sink.connect()
seamless.database_cache.connect()

from seamless.highlevel import Context, Cell, Transformer

ctx = None
webctx = None
save = None

def pr(*args):
    print(*args, file=sys.stderr)

async def define_graph(ctx):
    """Code to define the graph
    Leave this function empty if you want load() to load the graph from graph/PROJNAME.seamless 
    """

    '''
    background = ["1AVXB", "2SNIB", "7CEIB"] #, "1ACBB", "1ATNB"]

    ctx.receptor = Cell("text")
    ctx.receptor.set(open("examples/1AVXA.pdb").read())

    code = open("attract-script/attract.sh").read()
    code = code.replace("trap ", "#trap ")
    code += """
cat result.dat > RESULT
"""

    ctx.attract = Context()
    ctx.attract.result = Context()
    for pdbcode in background:
        pdbfile = "ligands/{}.pdb".format(pdbcode)
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
    '''
    
async def load():
    from seamless.metalevel.bind_status_graph import bind_status_graph_async
    import json

    global ctx, webctx, save

    try:
        ctx
    except NameError:
        pass
    else:
        if ctx is not None:
            pr('"ctx" already exists. To reload, do "ctx = None" or "del ctx" before load()')
            return
    
    for f in (
        "web/index-CONFLICT.html",
        "web/index-CONFLICT.js",
        "web/webform-CONFLICT.txt",
    ):
        if os.path.exists(f):
            if open(f).read().rstrip("\n ") in ("", "No conflict"):
                continue
            dest = f + "-BAK"
            if os.path.exists(dest):
                os.remove(dest)            
            pr("Existing '{}' found, moving to '{}'".format(f, dest))
            shutil.move(f, dest)
    ctx = Context()
    empty_graph = await ctx._get_graph_async(copy=True)
    await define_graph(ctx)
    new_graph = await ctx._get_graph_async(copy=True)
    graph_file = "graph/" + PROJNAME + ".seamless"
    ctx.load_vault("vault")
    if new_graph != empty_graph:
        pr("*** define_graph() function detected. Not loading '{}'***\n".format(graph_file))
    else:
        pr("*** define_graph() function is empty. Loading '{}' ***\n".format(graph_file))
        graph = json.load(open(graph_file))        
        ctx.set_graph(graph, mounts=True, shares=True)
        await ctx.translation(force=True)

    status_graph = json.load(open("graph/" + PROJNAME + "-webctx.seamless"))

    webctx = await bind_status_graph_async(
        ctx, status_graph,
        mounts=True,
        shares=True
    )
    def save():
        import os, itertools, shutil

        def backup(filename):
            if not os.path.exists(filename):
                return filename
            for n in itertools.count():
                n2 = n if n else ""
                new_filename = "{}.bak{}".format(filename, n2)
                if not os.path.exists(new_filename):
                    break
            shutil.move(filename, new_filename)
            return filename

        ctx.save_graph(backup("graph/" + PROJNAME + ".seamless"))
        webctx.save_graph(backup("graph/" + PROJNAME + "-monitoring.seamless"))
        ctx.save_vault("vault")
        webctx.save_vault("vault")

    pr("""Project loaded.

    Main context is "ctx"
    Web/status context is "webctx"

    Open http://localhost:<REST server port> to see the web page
    Open http://localhost:<REST server port>/status/status.html to see the status

    Run save() to save the project
    """)
