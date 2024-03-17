# Copyright 2023-2024 David Goddard.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain a
# copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

from .. import _persistent


logger = logging.getLogger(__name__)


class SQLGenerator:

    def __init__(self, selects=None, froms=None):

        self.selects = []
        self.froms = []
        self.wheres = []
        self.sorts = []
        self.groups = []
        self.extra = []
        self.parameters = {}

        if selects:
            self.add_select(selects)
        
        if froms:
            self.add_from(froms)


    def add_select(self, select_clause):

        if not select_clause:
            return

        if isinstance(select_clause, list):
            self.selects.extend(select_clause)
        else:
            self.selects.append(select_clause)


    def add_from(self, from_clause, join_type=None, on_clause=None):

        if not from_clause:
            return

        if join_type and on_clause:
            join_clause = f"{join_type} {from_clause} ON {on_clause}"
            self.froms.append(join_clause)
        else:
            self.froms.append(from_clause)


    def add_group(self, group_clause):

        if not group_clause:
            return

        if isinstance(group_clause, list):
            self.groups.extend(group_clause)
        else:
            self.groups.append(group_clause)


    def add_where_with_operator(self, column, value, operator='=', optional=False):

        if operator.lower() == 'in' and isinstance(value, list):
            placeholders = ', '.join([f":{column}_{i}" for i in range(len(value))])
            clause = f"{column} IN ({placeholders})"
            for i, val in enumerate(value):
                self.parameters[f"{column}_{i}"] = val
        elif value is not None or (value is None and optional):
            clause = f"{column} {operator} :{column}"
            self.parameters[column] = value
        else:
            raise ValueError(f"Value for required parameter '{column}' is None.")
        
        self.wheres.append(clause)


    def add_where(self, clause_or_params, optional=False):
    
        if not clause_or_params:
            return

        if isinstance(clause_or_params, dict):
            for key, value in clause_or_params.items():
                if value is None and not optional:
                    raise ValueError(f"Value for required parameter '{key}' is None.")
                elif value is not None:
                    clause = f"{key} = :{key}"
                    self.wheres.append(clause)
                    self.parameters[key] = value
        elif isinstance(clause_or_params, str):
            self.wheres.append(clause_or_params)
        else:
            raise TypeError("Clause or parameters must be a string (for plain clauses) or a dictionary (for parameterised clauses).")


    def add_where_not_null(self, columns):
    
        if not columns:
            return

        if isinstance(columns, list):
            for column in columns:
                clause = f"{column} is not null"
                self.wheres.append(clause)
        else:
            clause = f"{columns} is not null"
            self.wheres.append(clause)


    def add_sort(self, sort_clause):

        if not sort_clause:
            return

        if isinstance(sort_clause, list):
            self.sorts.extend(sort_clause)
        else:
            self.sorts.append(sort_clause)


    def add_extra(self, extra_clause):

        if not extra_clause:
            return

        if isinstance(extra_clause, list):
            self.extra.extend(extra_clause)
        else:
            self.extra.append(extra_clause)


    def generate_sql(self):

        query = ''
        if self.selects:
            query += 'SELECT ' + ', '.join(self.selects) + ' '
        if self.froms:
            query += 'FROM ' + ', '.join(self.froms) + ' '
        if self.wheres:
            query += 'WHERE ' + ' AND '.join(self.wheres) + ' '
        if self.groups:
            query += 'GROUP BY ' + ', '.join(self.groups) + ' '
        if self.sorts:
            query += 'ORDER BY ' + ', '.join(self.sorts) + ' '
        if self.extra:
            query += ' ' + ', '.join(self.extra) + ' '
        return query.strip()


    def get_parameters(self):

        return self.parameters


    def get_query(self):

        return self.generate_sql(), self.get_parameters()
    