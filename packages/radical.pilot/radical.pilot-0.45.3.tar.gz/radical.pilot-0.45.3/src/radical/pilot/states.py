#pylint: disable=C0301, C0103, W0212

__copyright__ = "Copyright 2013-2014, http://radical.rutgers.edu"
__license__   = "MIT"


import datetime

# -----------------------------------------------------------------------------
# The state "struct" encapsulates a state and its timestamp.
class State(object):
    __slots__ = ('state', 'timestamp')

    # ----------------------------------------
    #
    def __init__(self, state, timestamp):
        """Le constructeur.
        """
        self.state = state
        self.timestamp = timestamp

    # ----------------------------------------
    #
    def __eq__(self, other):
        """Comparison operator for 'equal'. Compares 'State' as well 
           as 'str' types.
        """
        if type(other) == str:
            return self.state == other
        else:
            return self.state == other.state

    # ----------------------------------------
    #
    def __ne__(self, other):
        """Comparison operator for 'not equal'. Compares 'State' as well 
           as 'str' types.
        """
        if type(other) == str:
            return not self.__eq__(other)
        else:
            return not self.__eq__(other.state)

    # ----------------------------------------
    #
    def as_dict(self):
        """Returns the state and its timestamp as a Python dictionary.
        """
        return {"state": self.state, "timestamp": self.timestamp}

    # ----------------------------------------
    #
    def __str__(self):
        """Returns the string representation of the state. The string 
           representation is just the state as string without its timestamp.
        """
        return self.state

# -----------------------------------------------------------------------------
# Common States
NEW                          = 'New'
DONE                         = 'Done'
CANCELING                    = 'Canceling'
CANCELED                     = 'Canceled'
FAILED                       = 'Failed'
PENDING                      = 'Pending'
INITIAL                      = [NEW]
FINAL                        = [DONE, FAILED, CANCELED]

# -----------------------------------------------------------------------------
# ComputePilot States
PENDING_LAUNCH               = 'PendingLaunch'
LAUNCHING                    = 'Launching'
PENDING_ACTIVE               = 'PendingActive'
ACTIVE                       = 'Active'

pilot_state_value = {
    NEW                          :  1,
    PENDING_LAUNCH               :  2,
    LAUNCHING                    :  3,
    PENDING_ACTIVE               :  4,
    ACTIVE                       :  5,
    DONE                         :  6,
    FAILED                       :  6,
    CANCELED                     :  6
    }

pilot_state_by_value = {
     1 : NEW                          ,
     2 : PENDING_LAUNCH               ,
     3 : LAUNCHING                    ,
     4 : PENDING_ACTIVE               ,
     5 : ACTIVE                       ,
     6 : FINAL
    }

# -----------------------------------------------------------------------------
# ComputeUnit States
UNSCHEDULED                  = 'Unscheduled'
PENDING_INPUT_STAGING        = 'PendingInputStaging'
STAGING_INPUT                = 'StagingInput'
AGENT_STAGING_INPUT_PENDING  = 'AgentStagingInputPending'
AGENT_STAGING_INPUT          = 'AgentStagingInput'
PENDING_EXECUTION            = 'PendingExecution'
SCHEDULING                   = 'Scheduling'
ALLOCATING_PENDING           = 'AllocatingPending'
ALLOCATING                   = 'Allocating'
EXECUTING_PENDING            = 'ExecutingPending'
EXECUTING                    = 'Executing'
AGENT_EXECUTING              = 'Executing'
AGENT_STAGING_OUTPUT_PENDING = 'AgentStagingOutputPending'
AGENT_STAGING_OUTPUT         = 'AgentStagingOutput'
PENDING_OUTPUT_STAGING       = 'PendingOutputStaging'
STAGING_OUTPUT               = 'StagingOutput'


unit_state_value = {
    NEW                          :  1,
    UNSCHEDULED                  :  2,
    SCHEDULING                   :  3,
    PENDING_INPUT_STAGING        :  4,
    STAGING_INPUT                :  5,
    AGENT_STAGING_INPUT_PENDING  :  6,
    AGENT_STAGING_INPUT          :  7,
    ALLOCATING_PENDING           :  8,
    ALLOCATING                   :  9,
    PENDING_EXECUTION            : 10,
    EXECUTING_PENDING            : 10,
    EXECUTING                    : 11,
    AGENT_STAGING_OUTPUT_PENDING : 12,
    AGENT_STAGING_OUTPUT         : 13,
    PENDING_OUTPUT_STAGING       : 14,
    STAGING_OUTPUT               : 15,
    DONE                         : 16,
    FAILED                       : 16,
    CANCELED                     : 16,
    }

unit_state_by_value = {
     1 : NEW                          ,
     2 : UNSCHEDULED                  ,
     3 : SCHEDULING                   ,
     4 : PENDING_INPUT_STAGING        ,
     5 : STAGING_INPUT                ,
     6 : AGENT_STAGING_INPUT_PENDING  ,
     7 : AGENT_STAGING_INPUT          ,
     8 : ALLOCATING_PENDING           ,
     9 : ALLOCATING                   ,
    10 : EXECUTING_PENDING            ,
    11 : EXECUTING                    ,
    12 : AGENT_STAGING_OUTPUT_PENDING ,
    13 : AGENT_STAGING_OUTPUT         ,
    14 : PENDING_OUTPUT_STAGING       ,
    15 : STAGING_OUTPUT               ,
    16 : FINAL
    }
