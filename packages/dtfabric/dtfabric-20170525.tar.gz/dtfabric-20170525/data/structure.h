/*
 * ${structure_description}
 *
 * Copyright (C) ${copyright}, ${authors}
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This software is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>.
 */

#if !defined( _${prefix_upper_case}${structure_name_upper_case}_H )
#define _${prefix_upper_case}${structure_name_upper_case}_H

#include <common.h>
#include <types.h>

#if defined( __cplusplus )
extern "C" {
#endif

typedef struct ${prefix}${structure_name} ${prefix}${structure_name}_t;

struct ${prefix}${structure_name}
{
${structure_members}
};

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _${prefix_upper_case}${structure_name_upper_case}_H ) */

