# Copyright 2016 Eotvos Lorand University, Budapest, Hungary
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from utils.codegen import format_type

#[ #ifndef __ACTIONS_H__
#[ #define __ACTIONS_H__

#[ #include "dataplane.h"
#[ #include "common.h"

#[ #define FIELD(name, length) uint8_t name[(length + 7) / 8];

def unique_stable(items):
    """Returns only the first occurrence of the items in a list.
    Equivalent to unique_everseen from Python 3."""
    from collections import OrderedDict
    return list(OrderedDict.fromkeys(items))

#{ enum actions {
for table in hlir16.tables:
    for action in unique_stable(table.actions):
        #[ action_${action.action_object.name},
#[ action_,
#} };

# TODO remove this; instead:
# TODO in set_additional_attrs, replace all type references with the referenced types
def resolve_typeref(hlir16, f):
    if f.type.node_type == 'Type_Name':
        tref = f.type.type_ref
        return hlir16.objects.get(tref.name).type('type_ref')

    return f.type


for ctl in hlir16.controls:
    for act in ctl.actions:
        #{ struct action_${act.name}_params {
        for param in act.parameters.parameters:
            paramtype = resolve_typeref(hlir16, param)
            #[ FIELD(${param.name}, ${paramtype.size});

        #[ FIELD(DUMMY_FIELD, 0);
        #} };

#{ struct all_metadatas_t {
for metainst in hlir16.metadata_insts:
    if hasattr(metainst.type, 'type_ref'):
        metatype = metainst.type.type_ref
        #[ struct ${metatype.name} meta_${metatype.name};
    else:
        # note: in the case of an array type,
        #       the array brackets have to go after the variable name
        varname = "metafield_" + metainst.name
        formatted = format_type(metainst.type, varname)
        #[ $formatted;
#} };

for table in hlir16.tables:
    #{ struct ${table.name}_action {
    #[     int action_id;
    #{     union {
    for action in table.actions:
        # TODO what if the action is not a method call?
        # TODO what if there are more actions?
        action_method_name = action.expression.method.ref.name
        #[         struct action_${action.action_object.name}_params ${action_method_name}_params;
    #}     };
    #} };



for table in hlir16.tables:
    #[ void apply_table_${table.name}(packet_descriptor_t *pd, lookup_table_t** tables);
    for action in table.actions:
        aname = action.action_object.name
        mname = action.expression.method.ref.name

        #[ void action_code_$aname(packet_descriptor_t *pd, lookup_table_t **tables, struct action_${mname}_params);


# TODO: The controls shouldn't be accessed through an instance declaration parameter
for ctl in hlir16.objects['P4Control']:
    #{ typedef struct control_locals_${ctl.name}_s {
    for local_var_decl in ctl.controlLocals['Declaration_Variable'] + ctl.controlLocals['Declaration_Instance']:
        if local_var_decl.type.node_type == 'Type_Name':
            #[ ${format_type(local_var_decl.type, resolve_names = False)}_t ${local_var_decl.name};
        else:
            #[ ${format_type(local_var_decl.type, resolve_names = False)} ${local_var_decl.name};
    #} } control_locals_${ctl.name}_t;

#[ #endif
