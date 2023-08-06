#     Copyright 2017, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Assignment related nodes.

The most simple assignment statement ``a = b`` is what we have here. All others
are either re-formulated using temporary variables, e.g. ``a, b = c`` or are
attribute, slice, subscript assignments.

The deletion is a separate node unlike in CPython where assigning to ``NULL`` is
internally what deletion is. But deleting is something entirely different to us
during code generation, which is why we keep them separate.

Tracing assignments in SSA form is the core of optimization for which we use
the traces.

"""

from nuitka import Options
from nuitka.ModuleRegistry import getOwnerFromCodeName

from .NodeBases import NodeBase, StatementChildrenHavingBase
from .NodeMakingHelpers import (
    makeStatementExpressionOnlyReplacementNode,
    makeStatementsSequenceReplacementNode
)
from .VariableRefNodes import ExpressionTempVariableRef, ExpressionVariableRef


class StatementAssignmentVariable(StatementChildrenHavingBase):
    """ Assignment to a variable from an expression.

        All assignment forms that are not to attributes, slices, subscripts
        use this.

        The source might be a complex expression. The target can be any kind
        of variable, temporary, local, global, etc.

        Assigning a variable is something we trace in a new version, this is
        hidden behind target variable reference, which has this version once
        it can be determined.
    """

    kind = "STATEMENT_ASSIGNMENT_VARIABLE"

    named_children = (
        "source",
        "variable_ref"
    )

    inplace_suspect = None

    def __init__(self, variable_ref, source, source_ref):
        assert variable_ref is not None, source_ref
        assert source is not None, source_ref

        assert variable_ref.isTargetVariableRef()

        StatementChildrenHavingBase.__init__(
            self,
            values     = {
                "source"       : source,
                "variable_ref" : variable_ref
            },
            source_ref = source_ref
        )

        self.variable_trace = None

    def getDetail(self):
        variable_ref = self.getTargetVariableRef()
        variable = variable_ref.getVariable()

        if variable is not None:
            return "to variable %s" % variable
        else:
            return "to variable %s" % self.getTargetVariableRef()

    getTargetVariableRef = StatementChildrenHavingBase.childGetter(
        "variable_ref"
    )
    getAssignSource = StatementChildrenHavingBase.childGetter(
        "source"
    )
    setAssignSource = StatementChildrenHavingBase.childSetter(
        "source"
    )

    def markAsInplaceSuspect(self):
        self.inplace_suspect = True

    def isInplaceSuspect(self):
        return self.inplace_suspect

    def mayRaiseException(self, exception_type):
        return self.getAssignSource().mayRaiseException(exception_type)

    def computeStatement(self, trace_collection):
        # This is very complex stuff, pylint: disable=too-many-branches,too-many-return-statements

        # TODO: Way too ugly to have global trace kinds just here, and needs to
        # be abstracted somehow. But for now we let it live here: pylint: disable=too-many-statements

        source = self.getAssignSource()

        if source.isExpressionSideEffects():
            # If the assignment source has side effects, we can put them into a
            # sequence and compute that instead.
            statements = [
                makeStatementExpressionOnlyReplacementNode(
                    side_effect,
                    self
                )
                for side_effect in
                source.getSideEffects()
            ]

            statements.append(self)

            # Remember out parent, we will assign it for the sequence to use.
            parent = self.parent

            # Need to update ourselves to no longer reference the side effects,
            # but go to the wrapped thing.
            self.setAssignSource(source.getExpression())

            result = makeStatementsSequenceReplacementNode(
                statements = statements,
                node       = self,
            )
            result.parent = parent

            return (
                result.computeStatementsSequence(trace_collection),
                "new_statements",
"""\
Side effects of assignments promoted to statements."""
            )

        # Let assignment source may re-compute first.
        trace_collection.onExpression(self.getAssignSource())
        source = self.getAssignSource()

        # No assignment will occur, if the assignment source raises, so give up
        # on this, and return it as the only side effect.
        if source.willRaiseException(BaseException):
            result = makeStatementExpressionOnlyReplacementNode(
                expression = source,
                node       = self
            )

            return result, "new_raise", """\
Assignment raises exception in assigned value, removed assignment."""

        variable_ref = self.getTargetVariableRef()
        variable = variable_ref.getVariable()

        # Not allowed anymore at this point.
        assert variable is not None

        # Assigning from and to the same variable, can be optimized away
        # immediately, there is no point in doing it. Exceptions are of course
        # module variables that collide with built-in names.

        # TODO: The variable type checks ought to become unnecessary, as they
        # are to be a feature of the trace. Assigning from known assigned is
        # supposed to be possible to eliminate. If we get that wrong, we are
        # doing it wrong.
        if not variable.isModuleVariable() and \
             source.isExpressionVariableRef() and \
             source.getVariable() == variable:

            # A variable access that has a side effect, must be preserved,
            # so it can e.g. raise an exception, otherwise we can be fully
            # removed.
            if source.mayHaveSideEffects():
                result = makeStatementExpressionOnlyReplacementNode(
                    expression = source,
                    node       = self
                )

                return result, "new_statements", """\
Reduced assignment of %s from itself to mere access of it.""" % variable.getDescription()
            else:
                return None, "new_statements", """\
Removed assignment of %s from itself which is known to be defined.""" % variable.getDescription()



        # Set-up the trace to the trace collection, so future references will
        # find this assignment.
        self.variable_trace = trace_collection.onVariableSet(
            assign_node = self
        )

        provider = self.getParentVariableProvider()

        if variable.hasAccessesOutsideOf(provider) is False:
            last_trace = variable.getMatchingAssignTrace(self)

            if last_trace is not None:
                if variable.isLocalVariable() or variable.isTempVariable():
                    if source.isCompileTimeConstant():

                        # Can safely forward propagate only non-mutable constants.
                        if not source.isMutable():

                            if variable.isTempVariable() or \
                               (not provider.isExpressionClassBody() and \
                                not provider.isUnoptimized()
                                ):

                                if last_trace.hasDefiniteUsages():
                                    self.variable_trace.setReplacementNode(
                                        lambda usage : source.makeClone()
                                    )
                                    propagated = True
                                else:
                                    propagated = False

                                if not last_trace.hasPotentialUsages() and not last_trace.hasNameUsages():
                                    if not last_trace.getPrevious().isUninitTrace():
                                        # TODO: We could well decide, if that's even necessary, but for now
                                        # the "StatementDelVariable" is tasked with that.
                                        result = StatementDelVariable(
                                            variable_ref = self.getTargetVariableRef(),
                                            tolerant     = True,
                                            source_ref   = self.getSourceReference()
                                        )
                                    else:
                                        result = None

                                    return (
                                        result,
                                        "new_statements",
                                        "Dropped %s assignment statement to '%s'." % (
                                           "propagated" if propagated else "dead",
                                           self.getTargetVariableRef().getVariableName()
                                        )
                                    )
                        else:
                            # Something might be possible still.

                            pass
                    elif False and Options.isExperimental() and \
                        source.isExpressionFunctionCreation() and \
                        source.getFunctionRef().getFunctionBody().isExpressionFunctionBody() and \
                        not source.getDefaults() and  \
                        not source.getKwDefaults() and \
                        not source.getAnnotations():
                        # TODO: These are very mutable, right?

                        provider = self.getParentVariableProvider()

                        if variable.isTempVariable() or \
                           (not provider.isUnoptimized() and \
                            not provider.isExpressionClassBody()):

                            if last_trace.getDefiniteUsages() <= 1 and \
                               not last_trace.hasPotentialUsages() and \
                               not last_trace.hasNameUsages():

                                if last_trace.getDefiniteUsages() == 1:
                                    self.variable_trace.setReplacementNode(
                                        lambda usage : source.makeClone()
                                    )
                                    propagated = True
                                else:
                                    propagated = False

                                if not last_trace.getPrevious().isUninitTrace():
                                    # TODO: We could well decide, if that's even necessary.
                                    result = StatementDelVariable(
                                        variable_ref = self.getTargetVariableRef(),
                                        tolerant     = True,
                                        source_ref   = self.getSourceReference()
                                    )
                                else:
                                    result = None

                                return (
                                    result,
                                    "new_statements",
                                    "Dropped %s assignment statement to '%s'." % (
                                       "propagated" if propagated else "dead",
                                       self.getTargetVariableRef().getVariableName()
                                    )
                                )
                    else:
                        # More cases thinkable.
                        pass

        return self, None, None

    def needsReleasePreviousValue(self):
        previous = self.variable_trace.getPrevious()

        if previous.mustNotHaveValue():
            return False
        elif previous.mustHaveValue():
            return True
        else:
            return None


class StatementDelVariable(StatementChildrenHavingBase):
    """ Deleting a variable.

        All del forms that are not to attributes, slices, subscripts
        use this.

        The target can be any kind of variable, temporary, local, global, etc.

        Deleting a variable is something we trace in a new version, this is
        hidden behind target variable reference, which has this version once
        it can be determined.

        Tolerance means that the value might be unset. That can happen with
        re-formulation of ours, and Python3 exception variables.
    """
    kind = "STATEMENT_DEL_VARIABLE"

    named_children = (
        "variable_ref",
    )

    def __init__(self, variable_ref, tolerant, source_ref):
        assert variable_ref is not None
        assert variable_ref.isTargetVariableRef()

        if type(tolerant) is str:
            tolerant = tolerant == "True"

        assert tolerant is True or tolerant is False, repr(tolerant)

        StatementChildrenHavingBase.__init__(
            self,
            values     = {
                "variable_ref" : variable_ref
            },
            source_ref = source_ref
        )

        self.variable_trace = None
        self.previous_trace = None

        self.tolerant = tolerant

    def getDetail(self):
        variable_ref = self.getTargetVariableRef()
        variable = variable_ref.getVariable()

        if variable is not None:
            return "to variable %s" % variable
        else:
            return "to variable %s" % self.getTargetVariableRef()

    def getDetails(self):
        return {
            "tolerant" : self.tolerant
        }

    # TODO: Value propagation needs to make a difference based on this.
    def isTolerant(self):
        return self.tolerant

    getTargetVariableRef = StatementChildrenHavingBase.childGetter(
        "variable_ref"
    )

    def computeStatement(self, trace_collection):
        variable_ref = self.getTargetVariableRef()
        variable = variable_ref.getVariable()

        self.previous_trace = trace_collection.getVariableCurrentTrace(variable)

        # First eliminate us entirely if we can.
        if self.tolerant and self.previous_trace.isUninitTrace():
            return (
                None,
                "new_statements",
                "Removed tolerant 'del' statement of '%s' without effect." % (
                    variable.getName(),
                )
            )

        # The "del" is a potential use of a value. TODO: This could be made more
        # beautiful indication, as it's not any kind of usage.
        self.previous_trace.addPotentialUsage()

        # If not tolerant, we may exception exit now during the __del__
        if not self.tolerant and not self.previous_trace.mustHaveValue():
            trace_collection.onExceptionRaiseExit(BaseException)

        # Record the deletion, needs to start a new version then.
        trace_collection.onVariableDel(
            variable_ref = variable_ref
        )

        trace_collection.onVariableContentEscapes(variable)

        # Any code could be run, note that.
        trace_collection.onControlFlowEscape(self)

        # Need to fetch the potentially invalidated variable. A "del" on a
        # or shared value, may easily assign the global variable in "__del__".
        self.variable_trace = trace_collection.getVariableCurrentTrace(variable)

        return self, None, None

    def mayHaveSideEffects(self):
        return True

    def mayRaiseException(self, exception_type):
        if self.tolerant:
            return False
        else:
            if self.variable_trace is not None:
                variable = self.getTargetVariableRef().getVariable()

                # Temporary variables deletions won't raise, just because we
                # don't create them that way. We can avoid going through SSA in
                # these cases.
                if variable.isTempVariable():
                    return False

                # If SSA knows, that's fine.
                if self.previous_trace is not None and \
                   self.previous_trace.mustHaveValue():
                    return False

            return True


class StatementReleaseVariable(NodeBase):
    """ Releasing a variable.

        Just release the value, which of course is not to be used afterwards.

        Typical code: Function exit, try/finally release of temporary
        variables.
    """

    kind = "STATEMENT_RELEASE_VARIABLE"

    __slots__ = "variable", "variable_trace"

    def __init__(self, variable, source_ref):
        assert variable is not None, source_ref

        NodeBase.__init__(
            self,
            source_ref = source_ref
        )

        self.variable = variable

        self.variable_trace = None

    def getDetail(self):
        return "of variable %s" % self.variable

    def getDetails(self):
        return {
            "variable" : self.variable
        }

    def getDetailsForDisplay(self):
        return {
            "variable_name" : self.variable.getName(),
            "owner"    : self.variable.getOwner().getCodeName()
        }

    @classmethod
    def fromXML(cls, provider, source_ref, **args):
        assert cls is StatementReleaseVariable, cls

        owner = getOwnerFromCodeName(args["owner"])
        assert owner is not None, args["owner"]

        variable = owner.getProvidedVariable(args["variable_name"])

        return cls(
            variable   = variable,
            source_ref = source_ref
        )

    def getVariable(self):
        return self.variable

    def getVariableVersion(self):
        return self.variable_trace.getVersion()

    def setVariable(self, variable):
        self.variable = variable

    def computeStatement(self, trace_collection):
        self.variable_trace = trace_collection.onVariableRelease(
            variable = self.variable
        )

        if self.variable_trace.isUninitTrace():
            return (
                None,
                "new_statements",
                "Uninitialized %s is not released." % (
                    self.variable.getDescription()
                )
            )

        trace_collection.onVariableContentEscapes(self.variable)

        # Any code could be run, note that.
        trace_collection.onControlFlowEscape(self)

        # TODO: We might be able to remove ourselves based on the trace
        # we belong to.

        return self, None, None

    def mayHaveSideEffects(self):
        # May execute __del__ code, it would be sweet to be able to predict
        # that another reference will still be active for a value though.
        return True

    def mayRaiseException(self, exception_type):
        # By default, __del__ is not allowed to raise an exception.
        return False


class ExpressionTargetVariableRef(ExpressionVariableRef):
    kind = "EXPRESSION_TARGET_VARIABLE_REF"

    __slots__ = "variable_version",

    # TODO: Remove default and correct argument order later.
    def __init__(self, variable_name, source_ref, variable = None, version = None):
        ExpressionVariableRef.__init__(self, variable_name, source_ref)

        self.variable_version = version

        # TODO: Remove setVariable, once not needed anymore and in-line to
        # here.
        if variable is not None:
            self.setVariable(variable)
            assert variable.getName() == variable_name

    def getDetailsForDisplay(self):
        result = {
            "variable_name" : self.variable_name,
            "version"       : self.variable_version,
        }

        if self.variable is not None:
            result["owner"] = self.variable.getOwner().getCodeName()

        return result

    @classmethod
    def fromXML(cls, provider, source_ref, **args):
        assert cls is ExpressionTargetVariableRef, cls

        owner = getOwnerFromCodeName(args["owner"])
        assert owner is not None, args["owner"]

        variable = owner.getProvidedVariable(args["variable_name"])

        return cls(
            variable_name = variable.getName(),
            variable      = variable,
            version       = int(args["version"]),
            source_ref    = source_ref
        )

    def computeExpression(self, trace_collection):
        assert False, self.parent

    @staticmethod
    def isTargetVariableRef():
        return True

    def getVariableVersion(self):
        assert self.variable_version is not None, self

        return self.variable_version

    def setVariable(self, variable):
        ExpressionVariableRef.setVariable(self, variable)

        self.variable_version = variable.allocateTargetNumber()
        assert self.variable_version is not None


class ExpressionTargetTempVariableRef(ExpressionTempVariableRef):
    kind = "EXPRESSION_TARGET_TEMP_VARIABLE_REF"

    __slots__ = "variable_version",

    def __init__(self, variable, source_ref, version = None):
        ExpressionTempVariableRef.__init__(self, variable, source_ref)

        if version is None:
            version = variable.allocateTargetNumber()

        self.variable_version = version

    def getDetailsForDisplay(self):
        return {
            "temp_name" : self.variable.getName(),
            "version"   : self.variable_version,
            "owner"     : self.variable.getOwner().getCodeName()
        }

    @classmethod
    def fromXML(cls, provider, source_ref, **args):
        assert cls is ExpressionTargetTempVariableRef, cls

        owner = getOwnerFromCodeName(args["owner"])
        variable = owner.createTempVariable(args["temp_name"])
        version = int(args["version"])

        variable.version_number = max(variable.version_number, version)

        return cls(
            variable   = variable,
            version    = version,
            source_ref = source_ref
        )


    def computeExpression(self, trace_collection):
        assert False, self.parent

    @staticmethod
    def isTargetVariableRef():
        return True

    def getVariableVersion(self):
        return self.variable_version

    # Python3 only, it updates temporary variables that are closure variables.
    def setVariable(self, variable):
        ExpressionTempVariableRef.setVariable(self, variable)

        self.variable_version = self.variable.allocateTargetNumber()
