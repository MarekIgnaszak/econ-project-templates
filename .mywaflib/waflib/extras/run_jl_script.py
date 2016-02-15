#!/usr/bin/env python
# encoding: utf-8
# Hans-Martin von Gaudecker and Zurich students, 2016-

"""
Run a Julia script in the directory specified by **ctx.bldnode**.

Strings supplied to the **prepend** and **append** keywords will
be added to the command line.

Usage::

    ctx(
        features='run_jl_script',
        source='some_script.jl',
        target=['some_table.tex', 'some_figure.eps'],
        deps='some_data.csv',
        append='',
        prepend=''
    )

"""

from waflib import Task, TaskGen, Logs


JULIA_COMMANDS = ['julia']


def configure(conf):
    conf.find_program(JULIA_COMMANDS, var='JLCMD', mandatory=False)
    if not conf.env.JLCMD:
        conf.fatal("No Julia interpreter found!")


@Task.update_outputs
class run_jl_script(Task.Task):

    """Run a Julia script."""

    run_str = '${PREPEND} "${JLCMD}" "${SRC[0].abspath()}" ${APPEND}'
    shell = True

    def exec_command(self, cmd, **kw):
        bld = self.generator.bld
        try:
            if not kw.get('cwd', None):
                kw['cwd'] = bld.cwd
        except AttributeError:
            bld.cwd = kw['cwd'] = bld.variant_dir
        if not self.buffer_output:
            kw["stdout"] = kw["stderr"] = None
        return bld.exec_command(cmd, **kw)

    def keyword(self):
        """
        Override the 'Compiling' default.

        """

        return 'Running'

    def __str__(self):
        """
        More useful output.

        """

        return "{prepend} [Julia] {fn} {append}".format(
                prepend=self.env.PREPEND,
                fn=self.inputs[0].path_from(self.inputs[0].ctx.launch_node()),
                append=self.env.APPEND
            )


@TaskGen.feature('run_jl_script')
@TaskGen.before_method('process_source')
def apply_run_jl_script(tg):
    """Task generator for running a single Julia module.

    The generated task will honor the PYTHONPATH environmental variable
    as well as a PYTHONPATH attribute of the build context environment.

    Attributes:

                    * source -- A **single** source node or string. (required)
                    * target -- A single target or list of targets (nodes or strings).
                    * deps -- A single dependency or list of dependencies
                      (nodes or strings)
                    * prepend -- A string that will be prepended to the command
                    * append -- A string that will be appended to the command

    """

    # Convert sources and targets to nodes
    src_node = tg.path.find_resource(tg.source)
    if not src_node:
        tg.bld.fatal(
            'Cannot find input file %s for processing' % tg.source
        )
    tgt_nodes = [tg.path.find_or_declare(t) for t in tg.to_list(tg.target)]

    # Create the task.
    tsk = tg.create_task('run_jl_script', src=src_node, tgt=tgt_nodes)

    tsk.env.APPEND = getattr(tg, 'append', '')
    tsk.env.PREPEND = getattr(tg, 'prepend', '')
    tsk.buffer_output = getattr(tg, 'buffer_output', True)

    # dependencies (if the attribute 'deps' changes, trigger a recompilation)
    for x in tg.to_list(getattr(tg, 'deps', [])):
        node = tg.path.find_resource(x)
        if not node:
            tg.bld.fatal(
                'Could not find dependency %r for running %r'
                % (x, src_node.relpath())
            )
        tsk.dep_nodes.append(node)
    Logs.debug(
        'deps: found dependencies %r for running %r' % (
            tsk.dep_nodes, src_node.relpath()
        )
    )

    # Bypass the execution of process_source by setting the source to an empty list
    tg.source = []
