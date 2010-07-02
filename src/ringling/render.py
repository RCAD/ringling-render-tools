from pymel import *
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def get_render_globals():
    return core.SCENE.defaultRenderGlobals

def get_frame_range():
    rg = get_render_globals()
    return (rg.startFrame.get(), rg.endFrame.get())




win = window(title="Send to Farm")
layout = columnLayout()
local_ribgen = checkBox(label = "Local Ribgen", value=True, parent=layout)
chunk_label = text(label="Chunk Size:")
chunk_size = intField(value=5)
submit_btn = button(label="Submit", parent=layout)

def submit_job(*args):
    frange = get_frame_range()
    fcount = len(range(int(frange[0]),int(frange[1])))+1
    chunks = chunk_size.getValue()
    if fcount < chunks:
        log.warning('Chunk size is higher than frame range!')
        log.warning('Setting chunk size to frame count.')
        chunks = fcount
    do_ribgen_now = local_ribgen.getValue()     
    if do_ribgen_now:
        mel.rman('genrib')
    else:
        # add remote task for rib gen
        pass
    log.debug(str((do_ribgen_now,fcount,chunks)))
submit_btn.setCommand(submit_job)
win.show()